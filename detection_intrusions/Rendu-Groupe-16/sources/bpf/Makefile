CLANG ?= clang
BPFTOOL ?= bpftool

BPF_CFLAGS := -O2 -g -target bpf -D__TARGET_ARCH_x86 \
	-Wall -Werror \
	-I. -I../include

all: edr.bpf.o

vmlinux.h:
	$(BPFTOOL) btf dump file /sys/kernel/btf/vmlinux format c > vmlinux.h

edr.bpf.o: edr.bpf.c vmlinux.h ../include/edr_shared.h
	$(CLANG) $(BPF_CFLAGS) -c edr.bpf.c -o edr.bpf.o

clean:
	rm -f edr.bpf.o vmlinux.h

.PHONY: all clean
