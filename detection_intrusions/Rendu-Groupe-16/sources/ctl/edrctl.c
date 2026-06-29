#define _GNU_SOURCE

#include <arpa/inet.h>
#include <errno.h>
#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <bpf/bpf.h>

#include "../include/edr_shared.h"

#define EDR_STATUS_PATH "/run/edrd.status"
#define EDR_LOG_PATH "/var/log/edr.log"
#define EDR_PIN_DIR "/sys/fs/bpf/edr"

static void usage(const char *prog)
{
    fprintf(stderr,
            "Usage:\n"
            "  %s status\n"
            "  %s watch\n"
            "  %s block add <chemin|ip>\n"
            "  %s block list\n",
            prog, prog, prog, prog);
}

static int cmd_status(void)
{
    FILE *fp = fopen(EDR_STATUS_PATH, "r");
    char line[512];
    int pid = -1;
    bool have_hooks = false;

    if (!fp) {
        printf("edrd: down (status file missing)\n");
        return 1;
    }

    while (fgets(line, sizeof(line), fp)) {
        if (sscanf(line, "pid=%d", &pid) == 1)
            continue;
        if (strncmp(line, "hooks=", 6) == 0) {
            have_hooks = true;
            line[strcspn(line, "\n")] = '\0';
            printf("hooks actifs: %s\n", line + 6);
        }
    }
    fclose(fp);

    if (pid <= 0 || kill(pid, 0) != 0) {
        printf("edrd: down\n");
        return 1;
    }

    printf("edrd: up (pid=%d)\n", pid);
    if (!have_hooks)
        printf("hooks actifs: unknown\n");
    return 0;
}

static int cmd_watch(void)
{
    FILE *fp;
    char line[1024];

    fp = fopen(EDR_LOG_PATH, "r");
    if (!fp) {
        fprintf(stderr, "failed to open %s: %s\n", EDR_LOG_PATH, strerror(errno));
        return 1;
    }

    fseek(fp, 0, SEEK_END);
    printf("watching %s (Ctrl+C to stop)\n", EDR_LOG_PATH);

    while (1) {
        if (fgets(line, sizeof(line), fp)) {
            fputs(line, stdout);
            fflush(stdout);
            continue;
        }
        clearerr(fp);
        usleep(200000);
    }
}

static int open_map(const char *name)
{
    char path[512];
    snprintf(path, sizeof(path), "%s/%s", EDR_PIN_DIR, name);
    return bpf_obj_get(path);
}

static int cmd_block_add(const char *arg)
{
    struct in_addr addr4;
    __u8 value = 1;
    int map_fd;

    if (inet_pton(AF_INET, arg, &addr4) == 1) {
        __u32 ip_be = addr4.s_addr;
        map_fd = open_map("blocked_ipv4");
        if (map_fd < 0) {
            fprintf(stderr, "failed to open blocked_ipv4 map: %s\n", strerror(errno));
            return 1;
        }
        if (bpf_map_update_elem(map_fd, &ip_be, &value, BPF_ANY) != 0) {
            close(map_fd);
            fprintf(stderr, "failed to add ip rule: %s\n", strerror(errno));
            return 1;
        }
        close(map_fd);
        printf("added block ip: %s\n", arg);
        return 0;
    } else {
        struct edr_path_key key = {};
        map_fd = open_map("blocked_exec_paths");
        if (map_fd < 0) {
            fprintf(stderr, "failed to open blocked_exec_paths map: %s\n", strerror(errno));
            return 1;
        }
        snprintf(key.path, sizeof(key.path), "%s", arg);
        if (bpf_map_update_elem(map_fd, &key, &value, BPF_ANY) != 0) {
            close(map_fd);
            fprintf(stderr, "failed to add path rule: %s\n", strerror(errno));
            return 1;
        }
        close(map_fd);
        printf("added block path: %s\n", arg);
        return 0;
    }
}

static int list_blocked_ipv4(void)
{
    int map_fd = open_map("blocked_ipv4");
    __u32 key = 0, next_key;
    __u8 value;
    bool first = true;

    if (map_fd < 0) {
        fprintf(stderr, "failed to open blocked_ipv4 map: %s\n", strerror(errno));
        return 1;
    }

    printf("[blocked ipv4]\n");
    while (bpf_map_get_next_key(map_fd, first ? NULL : &key, &next_key) == 0) {
        char ipbuf[INET_ADDRSTRLEN] = {0};
        struct in_addr addr = { .s_addr = next_key };
        if (bpf_map_lookup_elem(map_fd, &next_key, &value) == 0)
            inet_ntop(AF_INET, &addr, ipbuf, sizeof(ipbuf));
        printf("- %s\n", ipbuf[0] ? ipbuf : "invalid");
        key = next_key;
        first = false;
    }
    close(map_fd);
    return 0;
}

static int list_blocked_paths(void)
{
    int map_fd = open_map("blocked_exec_paths");
    struct edr_path_key key = {}, next_key = {};
    __u8 value;
    bool first = true;

    if (map_fd < 0) {
        fprintf(stderr, "failed to open blocked_exec_paths map: %s\n", strerror(errno));
        return 1;
    }

    printf("[blocked paths]\n");
    while (bpf_map_get_next_key(map_fd, first ? NULL : &key, &next_key) == 0) {
        if (bpf_map_lookup_elem(map_fd, &next_key, &value) == 0)
            printf("- %s\n", next_key.path);
        key = next_key;
        first = false;
    }
    close(map_fd);
    return 0;
}

static int cmd_block_list(void)
{
    int rc1 = list_blocked_paths();
    int rc2 = list_blocked_ipv4();
    return (rc1 || rc2) ? 1 : 0;
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        usage(argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "status") == 0)
        return cmd_status();

    if (strcmp(argv[1], "watch") == 0)
        return cmd_watch();

    if (strcmp(argv[1], "block") == 0) {
        if (argc >= 4 && strcmp(argv[2], "add") == 0)
            return cmd_block_add(argv[3]);
        if (argc == 3 && strcmp(argv[2], "list") == 0)
            return cmd_block_list();
    }

    usage(argv[0]);
    return 1;
}
