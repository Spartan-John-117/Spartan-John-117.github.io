CC ?= cc
CFLAGS ?= -O2 -g -Wall -Wextra -Werror
LDFLAGS ?=
LDLIBS += -lbpf -lelf -lz

all: edrd

edrd: edrd.c ../include/edr_shared.h
	$(CC) $(CFLAGS) -I../include edrd.c -o edrd $(LDFLAGS) $(LDLIBS)

clean:
	rm -f edrd

.PHONY: all clean
