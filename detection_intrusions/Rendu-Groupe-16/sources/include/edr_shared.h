#ifndef EDR_SHARED_H
#define EDR_SHARED_H

#define EDR_COMM_LEN 16
#define EDR_PATH_LEN 256

struct edr_path_key {
    char path[EDR_PATH_LEN];
};

enum edr_event_type {
    EDR_EVT_EXEC = 1,
    EDR_EVT_FILE_OPEN = 2,
    EDR_EVT_SOCKET_CONNECT = 3,
    EDR_EVT_TASK_KILL = 4,
    EDR_EVT_MODULE_REQUEST = 5,
};

struct edr_event {
    __u64 ts_ns;
    __u32 pid;
    __u32 uid;
    __u32 type;
    __s32 action;
    __u32 data_u32;
    char comm[EDR_COMM_LEN];
    char detail[EDR_PATH_LEN];
};

#endif
