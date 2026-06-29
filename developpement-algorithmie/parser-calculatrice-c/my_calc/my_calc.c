#include "my_calc.h"
#include <stdlib.h>
#include <string.h>

//function computes the power of a number a raised to an exponent b
long ipow(long a, long b) {
	long res = 1;
	if (b < 0) {
		return 0;
	}
	for (int i = b; i; i -= 1) {
		res *= a;
	}
	return res;
}

// exponent <- primary:p (Opexp exponent:e #do_exp(_, p, e))?
int exponent(struct parser *p, struct scope *s) {
	int tmp = p->current_pos;
	if (primary(p, s)) {
		struct scope s2 = {0};
		s2.defs = s->defs;
		if (
			read_space(p)
			&& readchar(p, '^')
			&& read_space(p)
			&& exponent(p, &s2)
		) {
			s->current_val = ipow(s->current_val, s2.current_val);
		}
		return 1;
	}
	reset_pos(p, tmp);
	return 0;
}

//mult <- exp:e1 (Opmul exp:e2 #do_mult(_, o, e1, e2))*
int mult(struct parser *p, struct scope *s) {
	int tmp = p->current_pos;

	if (exponent(p, s)) {
		while (1) {
			struct scope s2 = {0};
			s2.defs = s->defs;
			if (
				read_space(p)
				&& begin_capture(p, "m")
				&& readset(p, "*/%")
				&& end_capture(p, "m")
				&& exponent(p, &s2)
			) {
				char *val = get_value(p, get_node(p, "m"));
				switch (val[0]) {
					case '*':
						s->current_val *= s2.current_val;
						break;
					case '/':
						s->current_val /= s2.current_val;
						break;
					case '%':
						s->current_val %= s2.current_val;
						break;
				}
				free(val);
			} else {
				break;
			}
		}
		return 1;
	}

	reset_pos(p, tmp);
	return 0;
}

//add <- mult:e1 (Opadd:o mult:e2 #do_add(_, o, e1, e2))*
int add(struct parser *p, struct scope *s) {
	int tmp = p->current_pos;

	if (mult(p, s)) {
		while (1) {
			struct scope s2 = {0};
			s2.defs = s->defs;
			if (
				read_space(p)
				&& begin_capture(p, "a")
				&& readset(p, "+-")
				&& end_capture(p, "a")
				&& mult(p, &s2)
			) {
				char *val = get_value(p, get_node(p, "a"));
				switch (val[0]) {
					case '+':
						s->current_val += s2.current_val;
						break;
					case '-':
						s->current_val -= s2.current_val;
						break;
				}
				free(val);
			} else {
				break;
			}
		}
		return 1;
	}

	reset_pos(p, tmp);
	return 0;
}

//line <- (Name:n Opassign)? add:e #assign(n,e) #set(_, e) Semicolon
int line(struct parser *p, struct scope *s) {
	int tmp = p->current_pos;
	char *opt_name = NULL;
	if (
		read_space(p)
		&& begin_capture(p, "l")
		&& readid(p)
		&& end_capture(p, "l")
		&& read_space(p)
		&& readchar(p, '=')
		&& read_space(p)
	) {
		opt_name = get_value(p, get_node(p, "l"));
	}

	if (add(p, s)) {
		if (
			read_space(p)
			&& readchar(p, ';')
			&& read_space(p)
		) {
			if (opt_name != NULL) {
				prepend_in_scope(s, opt_name, s->current_val);
			}
			return 1;
		}
	}

	reset_pos(p, tmp);
	return 0;
}

void prepend_in_scope(struct scope *s, char *name, long int val) {
	struct def_list *item = calloc(1, sizeof(*item));
	item->next = s->defs;
	s->defs = item;
	item->name = name;
	item->val = val;
}

struct def_list *get_in_scope(struct scope *s, const char *n) {
	for (struct def_list *item = s->defs; item; item = item->next) {
		if (!strcmp(item->name, n)) {
			return item;
		}
	}
	return NULL;
}

void clean_in_scope(struct scope *s) {
	struct def_list *item = s->defs;

	while (item) {
		struct def_list *next = item->next;
		free(item->name);
		free(item);
		item = next;
	}
}

// Opun		<- space ('+' / '-'):o #set_op(_, o) space
int opun(struct parser *p, int *sign) {
	while (
		read_space(p)
		&& begin_capture(p, "o")
		&& readset(p, "+-") &&
		end_capture(p, "o") &&
		read_space(p)
	) {
		char *val = get_value(p, get_node(p, "o"));
		switch (val[0]) {
			case '+':
				break;
			case '-':
				*sign = *sign * -1;
				break;
		}
		free(val);
	}
	return 0;
}

// primary 	<- (Opun:sign #cacl_sign(_, sign))* (
// 				Val:v #make_node(_, v)
// 				/ Name:n #get_value(_, n)
// 				/ Opar add:n Cpar #set_node(_, n)
int primary(struct parser *p, struct scope *s) {
	int sign = 1;
	opun(p, &sign);
	read_space(p);
	int tmp = p->current_pos;
	if (
		begin_capture(p, "v") &&
		readint(p) &&
		end_capture(p, "v") &&
		read_space(p)
	) {
		char *val = get_value(p, get_node(p, "v"));
		s->current_val = sign * atol(val);
		free(val);
		return 1;
	}

	reset_pos(p, tmp);

	if (
		begin_capture(p, "n") &&
		readid(p) &&
		end_capture(p, "n") &&
		read_space(p)
	) {
		char *val = get_value(p, get_node(p, "n"));
		struct def_list *item = get_in_scope(s, val);
		if (!item) {
			return 0;
		}
		s->current_val = sign * item->val;
		free(val);
		return 1;
	}

	if (
		readchar(p, '(')
		&& read_space(p)
	) {
		struct scope s2 = {0};
		s2.defs = s->defs;
		if (
			add(p, &s2)
			&& read_space(p)
			&& readchar(p, ')')
		) {
			s->current_val = sign * s2.current_val;
			return 1;
		}
	}

	return 0;
}

// Space <- (' '/'\t' / '\n' /"//" [\n]* '\n' / "/*" (!"*/" .)* "*/")*
int read_space(struct parser *p) {
	int tmp = p->current_pos;
	int res = 1;
	while (res == 1) {
		res = readchar(p, ' ');
		res = res || readchar(p, '\t');
		res = res || readchar(p, '\n');
		if (!res && readtext(p, "//")) {
			while (!readeof(p) && readnotset(p, "\n"));

			if (readchar(p, '\n') || readeof(p)) {
				res = 1;
			} else {
				reset_pos(p, tmp);
				res = 0;
			}
		}
		// "/*" (!"*/" .)* ("*/" / EOF)
		if (!res && readtext(p, "/*")) {
			while (1) {
				int tmp2 = p->current_pos;

				if (!readtext(p, "*/") && !readeof(p)) {
					nextpos(p);
				} else {
					reset_pos(p, tmp2);
					break;
				}
			}

			if (readtext(p, "*/") || readeof(p)) {
				res = 1;
			} else {
				reset_pos(p, tmp);
				res = 0;
			}
		}

		if (readeof(p)) {
			break;
		}
	}
	return 1;
}

//calc <- (line:e #set(_, e) )* EOF
int my_calc(struct parser *p, struct scope *s) {
	int tmp = p->current_pos;
	while (line(p, s));

	if (readeof(p)) {
		return 1;
	}

	reset_pos(p, tmp);
	return 0;
}
