#define _GNU_SOURCE

#include <arpa/inet.h>
#include <errno.h>
#include <signal.h>
#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <time.h>
#include <unistd.h>

#include <bpf/bpf.h>
#include <bpf/libbpf.h>

#include "../include/edr_shared.h"

#define EDR_BPF_OBJ_PATH_DEV "../bpf/edr.bpf.o"
#define EDR_BPF_OBJ_PATH_INSTALLED "/usr/local/lib/edr/edr.bpf.o"
#define EDR_BPF_PIN_PATH "/sys/fs/bpf/edr"
#define EDR_LOG_PATH "/var/log/edr.log"
#define EDR_STATUS_PATH "/run/edrd.status"

static volatile sig_atomic_t g_stop;
static FILE *g_log_file;

static int libbpf_print_cb(enum libbpf_print_level level, const char *fmt, va_list ap)
{
    (void)level;
    return vfprintf(stderr, fmt, ap);
}

static void handle_signal(int signo)
{
    (void)signo;
    g_stop = 1;
}

static int bump_memlock(void)
{
    struct rlimit rlim = {
        .rlim_cur = RLIM_INFINITY,
        .rlim_max = RLIM_INFINITY,
    };

    return setrlimit(RLIMIT_MEMLOCK, &rlim);
}

static int ensure_bpf_pin_path(void)
{
    if (mkdir(EDR_BPF_PIN_PATH, 0755) == 0)
        return 0;
    if (errno == EEXIST)
        return 0;
    return -1;
}

/* Anciens pins (libbpf par défaut /sys/fs/bpf/<nom>) incompatibles avec pin_root_path. */
static void unlink_legacy_bpffs_pins(void)
{
    unlink("/sys/fs/bpf/blocked_exec_paths");
    unlink("/sys/fs/bpf/blocked_ipv4");
}

static void write_status_file(void)
{
    FILE *fp = fopen(EDR_STATUS_PATH, "w");
    if (!fp)
        return;

    fprintf(fp, "pid=%d\n", getpid());
    fprintf(fp, "hooks=bprm_check_security,file_open,socket_connect,task_kill,kernel_module_request\n");
    fclose(fp);
}

static const char *event_type_to_str(__u32 type)
{
    switch (type) {
    case EDR_EVT_EXEC:
        return "exec";
    case EDR_EVT_FILE_OPEN:
        return "file_open";
    case EDR_EVT_SOCKET_CONNECT:
        return "socket_connect";
    case EDR_EVT_TASK_KILL:
        return "task_kill";
    case EDR_EVT_MODULE_REQUEST:
        return "kernel_module_request";
    default:
        return "unknown";
    }
}

static void format_ip(__u32 ip_host, char *out, size_t out_sz)
{
    struct in_addr addr = { .s_addr = htonl(ip_host) };
    if (!inet_ntop(AF_INET, &addr, out, out_sz))
        snprintf(out, out_sz, "invalid");
}

static void log_event_line(const struct edr_event *evt)
{
    struct timespec ts;
    struct tm tmv;
    char ts_buf[64];
    char extra[64] = "-";
    const char *action = (evt->action == -EPERM) ? "blocked" : "allowed";

    ts.tv_sec = (time_t)(evt->ts_ns / 1000000000ULL);
    ts.tv_nsec = (long)(evt->ts_ns % 1000000000ULL);
    localtime_r(&ts.tv_sec, &tmv);
    strftime(ts_buf, sizeof(ts_buf), "%Y-%m-%d %H:%M:%S", &tmv);

    if (evt->type == EDR_EVT_SOCKET_CONNECT)
        format_ip(evt->data_u32, extra, sizeof(extra));
    else if (evt->data_u32 != 0)
        snprintf(extra, sizeof(extra), "%u", evt->data_u32);

    fprintf(g_log_file,
            "ts=%s.%09ld pid=%u uid=%u comm=%s event=%s action=%s detail=%s data=%s\n",
            ts_buf, ts.tv_nsec, evt->pid, evt->uid, evt->comm, event_type_to_str(evt->type),
            action, evt->detail[0] ? evt->detail : "-", extra);
    fflush(g_log_file);
}

static int on_rb_event(void *ctx, void *data, size_t data_sz)
{
    const struct edr_event *evt = data;
    (void)ctx;

    if (data_sz < sizeof(*evt))
        return 0;

    log_event_line(evt);
    return 0;
}

static const char *const lsm_prog_names[] = {
    "edr_bprm_check_security",
    "edr_file_open",
    "edr_socket_connect",
    "edr_task_kill",
    "edr_kernel_module_request",
};

static int setup_and_run(void)
{
    struct bpf_object *obj = NULL;
    struct bpf_program *prog;
    struct bpf_link *links[16] = {};
    int link_count = 0;
    int ring_fd;
    struct ring_buffer *rb = NULL;
    int err = 0;
    size_t i;
    LIBBPF_OPTS(bpf_object_open_opts, open_opts, .pin_root_path = EDR_BPF_PIN_PATH);

    err = ensure_bpf_pin_path();
    if (err) {
        fprintf(stderr, "edrd: cannot create %s\n", EDR_BPF_PIN_PATH);
        return -1;
    }
    unlink_legacy_bpffs_pins();

    obj = bpf_object__open_file(EDR_BPF_OBJ_PATH_INSTALLED, &open_opts);
    if (libbpf_get_error(obj))
        obj = bpf_object__open_file(EDR_BPF_OBJ_PATH_DEV, &open_opts);
    if (libbpf_get_error(obj)) {
        fprintf(stderr, "edrd: bpf_object__open_file failed\n");
        return -1;
    }

    err = bpf_object__load(obj);
    if (err) {
        fprintf(stderr, "edrd: bpf_object__load failed: %d (%s)\n", err,
                err < 0 ? strerror(-err) : strerror(errno));
        goto out;
    }

    for (i = 0; i < sizeof(lsm_prog_names) / sizeof(lsm_prog_names[0]); i++) {
        const char *name = lsm_prog_names[i];
        long lerr;

        if (link_count >= (int)(sizeof(links) / sizeof(links[0]))) {
            err = -1;
            goto out;
        }
        prog = bpf_object__find_program_by_name(obj, name);
        if (!prog) {
            fprintf(stderr, "edrd: program %s not found in BPF object\n", name);
            err = -1;
            goto out;
        }
        links[link_count] = bpf_program__attach_lsm(prog);
        lerr = libbpf_get_error(links[link_count]);
        if (lerr) {
            fprintf(stderr, "edrd: attach_lsm failed for %s: %ld", name, lerr);
            if (lerr < 0)
                fprintf(stderr, " (%s)", strerror((int)-lerr));
            fprintf(stderr, "\n");
            err = -1;
            links[link_count] = NULL;
            goto out;
        }
        link_count++;
    }

    err = bpf_object__pin_maps(obj, EDR_BPF_PIN_PATH);
    if (err && err != -EEXIST) {
        fprintf(stderr, "edrd: bpf_object__pin_maps failed: %d\n", err);
        goto out;
    }

    ring_fd = bpf_object__find_map_fd_by_name(obj, "events");
    if (ring_fd < 0) {
        err = -1;
        goto out;
    }

    rb = ring_buffer__new(ring_fd, on_rb_event, NULL, NULL);
    if (!rb) {
        err = -1;
        goto out;
    }

    write_status_file();

    while (!g_stop) {
        err = ring_buffer__poll(rb, 200);
        if (err == -EINTR)
            break;
        if (err < 0)
            goto out;
    }

    err = 0;

out:
    if (rb)
        ring_buffer__free(rb);
    while (link_count-- > 0)
        bpf_link__destroy(links[link_count]);
    if (obj)
        bpf_object__close(obj);
    return err;
}

int main(void)
{
    int err;

    libbpf_set_print(libbpf_print_cb);

    signal(SIGINT, handle_signal);
    signal(SIGTERM, handle_signal);

    if (bump_memlock() != 0) {
        fprintf(stderr, "failed to raise memlock: %s\n", strerror(errno));
        return 1;
    }

    g_log_file = fopen(EDR_LOG_PATH, "a");
    if (!g_log_file) {
        fprintf(stderr, "failed to open %s: %s\n", EDR_LOG_PATH, strerror(errno));
        return 1;
    }

    err = setup_and_run();
    fclose(g_log_file);
    unlink(EDR_STATUS_PATH);

    if (err) {
        fprintf(stderr, "edrd failed: %d\n", err);
        return 1;
    }
    return 0;
}
