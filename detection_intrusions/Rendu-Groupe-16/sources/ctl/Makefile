CC ?= cc
CFLAGS ?= -O2 -g -Wall -Wextra -Werror
LDFLAGS ?=
LDLIBS += -lbpf -lelf -lz

all: edrctl

edrctl: edrctl.c ../include/edr_shared.h
	$(CC) $(CFLAGS) -I../include edrctl.c -o edrctl $(LDFLAGS) $(LDLIBS)

clean:
	rm -f edrctl

.PHONY: all clean
