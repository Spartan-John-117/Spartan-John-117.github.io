CC = gcc
CFLAGS = -Wall -Wextra -Werror -pedantic -std=c99 -g -I./include -I./include/criterion
OBJ = tests/my_parser.o tests/my_calc.o
TEST_DIR = tests

all: ${OBJ}

test: CFLAGS += -fsanitize=address
test: test_my_parser test_my_calc

test_my_parser: ${OBJ} tests/test_my_parser.o tests/my_parser.o
	$(CC) -lcriterion ${CFLAGS} -o $(TEST_DIR)/test_my_parser tests/test_my_parser.o tests/my_parser.o
	timeout 1m $(TEST_DIR)/test_my_parser

test_my_calc: ${OBJ} tests/test_my_calc.o
	$(CC) -lcriterion ${CFLAGS} -o $(TEST_DIR)/test_my_calc tests/test_my_calc.o ${OBJ}
	timeout 1m $(TEST_DIR)/test_my_calc

tests/%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(TEST_DIR)/*.o *.o .*.swp .*.swo

distclean: clean
	$(RM) $(TEST_DIR)/test_my_parser $(TEST_DIR)/test_my_calc

.PHONY: all clean distclean test test_my_parser test_my_calc