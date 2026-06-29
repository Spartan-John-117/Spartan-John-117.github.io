CC = gcc
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c99 -g -I./include -I./include/criterion
OBJ = my_parser.o

all: ${OBJ}

test: ${OBJ} test.o my_parser.o
	$(CC) -L./lib -lcriterion -o test test.o my_parser.o
	timeout 1m ./test

clean:
	$(RM) *.o .*.swp .*.swo

distclean: clean
	$(RM) test

.PHONY: all clean distclean test
