#ifndef _MY_CALC_H
#define _MY_CALC_H
#include "my_parser.h"

struct def_list {
	char *name;
	long int val;
	struct def_list *next;
};

struct scope {
	struct def_list *defs;
	long int current_val;
};

int read_space(struct parser *p);

void prepend_in_scope(struct scope *s, char *name, long int val);

void clean_in_scope(struct scope *s);
int exponent(struct parser *p, struct scope *s);
int mult(struct parser *p, struct scope *s);
int add(struct parser *p, struct scope *s);
int line(struct parser *p, struct scope *s);

struct def_list *get_in_scope(struct scope *, const char *);

int primary(struct parser *p, struct scope *s);

int my_calc(struct parser *p, struct scope *s);

#endif /* _MY_CALC_H */
