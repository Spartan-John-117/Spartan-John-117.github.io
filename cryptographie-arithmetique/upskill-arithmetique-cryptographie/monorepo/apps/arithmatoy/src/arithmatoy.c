#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "utils.h"

int VERBOSE = 0;

const char *get_all_digits() { return "0123456789abcdefghijklmnopqrstuvwxyz"; }
const size_t ALL_DIGIT_COUNT = 36;

void arithmatoy_free(char *number) { free(number); }

char *arithmatoy_add(unsigned int base, const char *lhs, const char *rhs) {
  size_t len1 = strlen(lhs);
  size_t len2 = strlen(rhs);
  size_t maxlen = (len1 > len2 ? len1 : len2) + 2;
  char *result = malloc(maxlen);
  if (!result) return NULL;
  size_t i = len1, j = len2, k = 0;
  unsigned int carry = 0;

  if (VERBOSE) {
    fprintf(stderr, "add: entering function\n");
  }

    while (i > 0 || j > 0 || carry > 0) {
    if (i == 0 && j == 0 && carry > 0 && VERBOSE) {
      fprintf(stderr, "add: final carry %u\n", carry);
    }

    unsigned int d1 = (i > 0) ? get_digit_value(lhs[--i]) : 0;
    unsigned int d2 = (j > 0) ? get_digit_value(rhs[--j]) : 0;

    if (VERBOSE) {
      fprintf(stderr, "add: digit %u digit %u carry %u\n", d1, d2, carry);
    }

    unsigned int sum = d1 + d2 + carry;
    unsigned int digit = sum % base;
    unsigned int next_carry = sum / base;

    if (VERBOSE) {
      fprintf(stderr, "add: result: digit %u carry %u\n", digit, next_carry);
    }

    result[k++] = to_digit(digit);
    carry = next_carry;
  }

  result[k] = '\0';
  reverse(result);
  const char *final = drop_leading_zeros(result);
  char *final_result = strdup(final);
  free(result);

  if (VERBOSE) {
    fprintf(stderr, "add: final result %s\n", final_result);
  }

  return final_result;
}

char *arithmatoy_sub(unsigned int base, const char *lhs, const char *rhs) {
  lhs = drop_leading_zeros(lhs);
  rhs = drop_leading_zeros(rhs);

  if (VERBOSE) {
    fprintf(stderr, "sub: entering function\n");
  }

  size_t len1 = strlen(lhs);
  size_t len2 = strlen(rhs);
  size_t maxlen = (len1 > len2 ? len1 : len2) + 1;
  char *result = malloc(maxlen + 1);
  if (!result) return NULL;
  size_t i = len1, j = len2, k = 0;
  unsigned int borrow = 0;

  while (i > 0 || j > 0) {
    unsigned int d1 = (i > 0) ? get_digit_value(lhs[--i]) : 0;
    unsigned int d2 = (j > 0) ? get_digit_value(rhs[--j]) : 0;

    if (VERBOSE) {
      fprintf(stderr, "sub: digit %u digit %u borrow %u\n", d1, d2, borrow);
    }

    unsigned int subtrahend = d2 + borrow;
    unsigned int digit;
    if (d1 < subtrahend) {
      digit = base + d1 - subtrahend;
      borrow = 1;
    } else {
      digit = d1 - subtrahend;
      borrow = 0;
    }

    if (VERBOSE) {
      fprintf(stderr, "sub: result: digit %u borrow %u\n", digit, borrow);
    }

    result[k++] = to_digit(digit);
  }

  result[k] = '\0';
  reverse(result);
  const char *final = drop_leading_zeros(result);
  char *final_result = strdup(final);
  free(result);

  if (VERBOSE) {
    fprintf(stderr, "sub: final result %s\n", final_result);
  }

  return final_result;
}

char *arithmatoy_mul(unsigned int base, const char *lhs, const char *rhs) {
  size_t len1 = strlen(lhs);
  size_t len2 = strlen(rhs);
  size_t maxlen = len1 + len2 + 2;
  char *result = malloc(maxlen);
  if (!result) return NULL;
  strcpy(result, "0");

  for (ssize_t j = len2 - 1; j >= 0; --j) {
    unsigned int d2 = get_digit_value(rhs[j]);

    if (VERBOSE) {
      fprintf(stderr, "mul: digit %u number %s\n", d2, lhs);
    }

    if (d2 == 0) {
      continue;
    }

    char *partial = malloc(len1 + len2 + 2);
    if (!partial) {
      free(result);
      return NULL;
    }

    size_t k = 0;
    unsigned int carry = 0;

    for (ssize_t i = len1 - 1; i >= 0; --i) {
      unsigned int d1 = get_digit_value(lhs[i]);
      unsigned int prod = d1 * d2 + carry;
      unsigned int digit = prod % base;
      carry = prod / base;
      partial[k++] = to_digit(digit);
    }

    if (carry > 0) {
      partial[k++] = to_digit(carry);
    }

    partial[k] = '\0';
    reverse(partial);

    size_t partial_len = strlen(partial);
    size_t zeros = len2 - 1 - j;
    char *shifted = malloc(partial_len + zeros + 1);
    if (!shifted) {
      free(partial);
      free(result);
      return NULL;
    }

    strcpy(shifted, partial);
    for (size_t z = 0; z < zeros; ++z) {
      shifted[partial_len + z] = '0';
    }
    shifted[partial_len + zeros] = '\0';
    free(partial);

    char *sum = arithmatoy_add(base, result, shifted);
    free(result);
    free(shifted);
    if (!sum) {
      return NULL;
    }
    result = sum;
  }

  const char *final = drop_leading_zeros(result);
  char *final_result = strdup(final);
  free(result);
  return final_result;
}

// Utility functions

unsigned int get_digit_value(char digit) {
  if (digit >= '0' && digit <= '9') {
    return digit - '0';
  }
  if (digit >= 'a' && digit <= 'z') {
    return 10 + (digit - 'a');
  }
  return -1;
}

char to_digit(unsigned int value) {
  if (value >= ALL_DIGIT_COUNT) {
    debug_abort("Invalid value for to_digit()");
    return 0;
  }
  return get_all_digits()[value];
}

char *reverse(char *str) {
  const size_t length = strlen(str);
  const size_t bound = length / 2;
  for (size_t i = 0; i < bound; ++i) {
    char tmp = str[i];
    const size_t mirror = length - i - 1;
    str[i] = str[mirror];
    str[mirror] = tmp;
  }
  return str;
}

const char *drop_leading_zeros(const char *number) {
  if (*number == '\0') return number;
  while (*number == '0') ++number;
  if (*number == '\0') --number;
  return number;
}

void debug_abort(const char *debug_msg) {
  fprintf(stderr, "%s\n", debug_msg);
  exit(EXIT_FAILURE);
}