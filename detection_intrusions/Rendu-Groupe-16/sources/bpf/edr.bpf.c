#include "vmlinux.h"

#include <bpf/bpf_core_read.h>
#include <bpf/bpf_endian.h>
#include <bpf/bpf_helpers.h>
#include <bpf/bpf_tracing.h>

#include "../include/edr_shared.h"

char LICENSE[] SEC("license") = "GPL";

#ifndef EPERM
#define EPERM 1
#endif

#ifndef AF_INET
#define AF_INET 2
#endif

struct {
    __uint(type, BPF_MAP_TYPE_RINGBUF);
    /* 16 MiB can fail map alloc on small guests; 1 MiB is enough for demos */
    __uint(max_entries, 1 << 20);
} events SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 1024);
    __type(key, struct edr_path_key);
    __type(value, __u8);
    __uint(pinning, LIBBPF_PIN_BY_NAME);
} blocked_exec_paths SEC(".maps");

struct {
    __uint(type, BPF_MAP_TYPE_HASH);
    __uint(max_entries, 1024);
    __type(key, __u32);
    __type(value, __u8);
    __uint(pinning, LIBBPF_PIN_BY_NAME);
} blocked_ipv4 SEC(".maps");

static __always_inline int emit_event(__u32 type, const char *detail, __s32 action, __u32 data_u32)
{
    struct edr_event *evt;
    __u64 id;

    evt = bpf_ringbuf_reserve(&events, sizeof(*evt), 0);
    if (!evt)
        return 0;

    __builtin_memset(evt, 0, sizeof(*evt));
    evt->ts_ns = bpf_ktime_get_ns();
    id = bpf_get_current_pid_tgid();
    evt->pid = (__u32)(id >> 32);
    evt->uid = (__u32)bpf_get_current_uid_gid();
    evt->type = type;
    evt->action = action;
    evt->data_u32 = data_u32;
    bpf_get_current_comm(&evt->comm, sizeof(evt->comm));

    if (detail)
        bpf_probe_read_kernel_str(&evt->detail, sizeof(evt->detail), detail);

    bpf_ringbuf_submit(evt, 0);
    return 0;
}

SEC("lsm/bprm_check_security")
int BPF_PROG(edr_bprm_check_security, struct linux_binprm *bprm, int ret)
{
    struct edr_path_key key = {};
    __u8 *blocked;
    const char *fn;

    if (ret)
        return ret;

    fn = BPF_CORE_READ(bprm, filename);
    if (!fn)
        return 0;

    bpf_probe_read_kernel_str(&key.path, sizeof(key.path), fn);
    blocked = bpf_map_lookup_elem(&blocked_exec_paths, &key);
    if (blocked) {
        emit_event(EDR_EVT_EXEC, fn, -EPERM, 0);
        return -EPERM;
    }

    emit_event(EDR_EVT_EXEC, fn, 0, 0);
    return 0;
}

/* Hook is security_file_open() → (struct file *file) — no open mask in this hook. */
SEC("lsm/file_open")
int BPF_PROG(edr_file_open, struct file *file, int ret)
{
    struct dentry *d;
    const char *name;

    if (ret)
        return ret;

    d = BPF_CORE_READ(file, f_path.dentry);
    if (!d)
        return 0;

    name = (const char *)BPF_CORE_READ(d, d_name.name);
    emit_event(EDR_EVT_FILE_OPEN, name, 0, 0);
    return 0;
}

SEC("lsm/socket_connect")
int BPF_PROG(edr_socket_connect, struct socket *sock, struct sockaddr *address, int addrlen, int ret)
{
    struct sockaddr_in sa4 = {};
    __u32 ip_be;
    __u8 *blocked;

    if (ret)
        return ret;

    if (!address || addrlen < sizeof(sa4))
        return 0;

    bpf_probe_read_kernel(&sa4, sizeof(sa4), address);
    if (sa4.sin_family != AF_INET)
        return 0;

    ip_be = sa4.sin_addr.s_addr;
    blocked = bpf_map_lookup_elem(&blocked_ipv4, &ip_be);
    if (blocked) {
        emit_event(EDR_EVT_SOCKET_CONNECT, "blocked_ipv4", -EPERM, bpf_ntohl(ip_be));
        return -EPERM;
    }

    emit_event(EDR_EVT_SOCKET_CONNECT, "connect_ipv4", 0, bpf_ntohl(ip_be));
    return 0;
}

SEC("lsm/task_kill")
int BPF_PROG(edr_task_kill, struct task_struct *p, struct kernel_siginfo *info, int sig,
             const struct cred *cred, int ret)
{
    const char *comm_k;

    if (ret)
        return ret;

    /* p->comm is a char[]; pass its kernel address, not BPF_CORE_READ of the array. */
    comm_k = (const char *)((void *)p + offsetof(struct task_struct, comm));
    emit_event(EDR_EVT_TASK_KILL, comm_k, 0, (__u32)sig);
    return 0;
}

SEC("lsm/kernel_module_request")
int BPF_PROG(edr_kernel_module_request, char *kmod_name, int ret)
{
    if (ret)
        return ret;
    if (!kmod_name)
        return 0;

    emit_event(EDR_EVT_MODULE_REQUEST, kmod_name, 0, 0);
    return 0;
}
