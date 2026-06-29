#define _POSIX_C_SOURCE 202404L
#include "include/my_calc.h"
#include "include/my_parser.h"
#include <criterion/criterion.h>
#include <stdio.h>

Test(basic, check_space)
{
	{
		struct parser *p = new_parser("   \t\t \n\n  ");
		cr_assert(read_space(p), "Failed to read_space");
		cr_assert(readeof(p), "Failed to read EOF");
		clean_parser(p);
	}
	{
		struct parser *p = new_parser("//  tutu\ntiti");
		cr_assert(read_space(p), "Failed to read_space");
		cr_assert(readtext(p, "titi"), "Failed to read_text");
		cr_assert(read_space(p), "Failed to read_space");
		cr_assert(readeof(p), "Failed to read EOF");
		clean_parser(p);
	}
	{
		struct parser *p = new_parser("/* globus */titi/*bignou*/plop");
		cr_assert(read_space(p), "Failed to read_space");
		cr_assert(readtext(p, "titi"), "Failed to read_text");
		cr_assert(read_space(p), "Failed to read_space");
		cr_assert(readtext(p, "plop"), "Failed to read_text");
		cr_assert(readeof(p), "Failed to read EOF");
		clean_parser(p);
	}
	{
		struct parser *p = new_parser("// globus \n \t\ntiti \n\t\t/*bignou*/plop");
		cr_assert(read_space(p), "Failed to read_space");
		cr_assert(readtext(p, "titi"), "Failed to read_text");
		cr_assert(read_space(p), "Failed to read_space");
		cr_assert(readtext(p, "plop"), "Failed to read_text");
		cr_assert(readeof(p), "Failed to read EOF");
		clean_parser(p);
	}
}

Test(basic, check_primary)
{
	{
		struct parser *p = new_parser("");
        struct scope s;
		cr_assert(!primary(p, &s), "Failed to primary");
		cr_assert(readeof(p), "Failed to read EOF");
		clean_parser(p);
	}
	{
		struct parser *p = new_parser(" 152\n");
		struct scope s;
		cr_assert(primary(p, &s), "Failed to primary");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 152, "Failed to get value");
        clean_parser(p);
	}
	{
		struct scope s = {0};
        prepend_in_scope(&s, strdup("tutu"), 42);
        struct def_list *item = get_in_scope(&s, "tutu");
        cr_assert(item != NULL, "Failed to get_in_scope");
        cr_assert(item->val == 42, "Failed to get value of item");
		struct parser *p = new_parser("  tutu\n");
		cr_assert(primary(p, &s), "Failed to primary");
		cr_assert(readeof(p), "Failed to read EOF");
        cr_assert(s.current_val == 42, "Failed to get tutu");
		clean_parser(p);
        clean_in_scope(&s);
	}
	{
		struct parser *p = new_parser(" +- - - 152\n");
		struct scope s;
		cr_assert(primary(p, &s), "Failed to primary");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == -152, "Failed to get value");
		clean_parser(p);
	}
	{
		struct scope s = {0};
		prepend_in_scope(&s, strdup("tutu"), 42);
		struct def_list *item = get_in_scope(&s, "tutu");
		cr_assert(item != NULL, "Failed to get_in_scope");
		cr_assert(item->val == 42, "Failed to get value of item");
		struct parser *p = new_parser(" - + - \t - tutu\n");
		cr_assert(primary(p, &s), "Failed to primary");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == -42, "Failed to get tutu");
		clean_parser(p);
		clean_in_scope(&s);
	}
}

Test(basic, check_exp) {
	{
		struct scope s = {0};
		struct parser *p = new_parser("2^2");
		cr_assert(exponent(p, &s), "Failed to read exp");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 4, "Failed to get tutu");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		struct parser *p = new_parser("2^-2");
		cr_assert(exponent(p, &s), "Failed to read exp");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 0, "Failed to get 0.25");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		struct parser *p = new_parser("2^3^2");
		cr_assert(exponent(p, &s), "Failed to read exp");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 512, "Failed to get tutu");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		prepend_in_scope(&s, strdup("tutu"), 3);
		struct def_list *item = get_in_scope(&s, "tutu");
		cr_assert(item != NULL, "Failed to get_in_scope");
		cr_assert(item->val == 3, "Failed to get value of item");
		struct parser *p = new_parser("2^tutu^2");
		cr_assert(exponent(p, &s), "Failed to read exp");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 512, "Failed to get tutu");
		clean_parser(p);
		clean_in_scope(&s);
	}

}

Test(basic, check_mult) {
	{
		struct scope s = {0};
		struct parser *p = new_parser("2*2");
		cr_assert(mult(p, &s), "Failed to mult");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 4, "Failed to get 4");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		struct parser *p = new_parser("2*-2");
		cr_assert(mult(p, &s), "Failed to mult");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == -4, "Failed to get -4");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		struct parser *p = new_parser("2*3/2");
		cr_assert(mult(p, &s), "Failed to mult");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 3, "Failed to get 3");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		prepend_in_scope(&s, strdup("tutu"), 3);
		struct def_list *item = get_in_scope(&s, "tutu");
		cr_assert(item != NULL, "Failed to get_in_scope");
		cr_assert(item->val == 3, "Failed to get value of item");
		struct parser *p = new_parser("2*tutu/2");
		cr_assert(mult(p, &s), "Failed to read exp");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 3, "Failed to get 3");
		clean_parser(p);
		clean_in_scope(&s);
	}

}

Test(basic, check_add) {
	{
		struct scope s = {0};
		struct parser *p = new_parser("2+2");
		cr_assert(add(p, &s), "Failed to add");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 4, "Failed to get 4");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		struct parser *p = new_parser("2+-2");
		cr_assert(add(p, &s), "Failed to add");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 0, "Failed to get 0");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		struct parser *p = new_parser("2+3*2");
		cr_assert(add(p, &s), "Failed to add");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 8, "Failed to get 8");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		prepend_in_scope(&s, strdup("tutu"), 3);
		struct def_list *item = get_in_scope(&s, "tutu");
		cr_assert(item != NULL, "Failed to get_in_scope");
		cr_assert(item->val == 3, "Failed to get value of item");
		struct parser *p = new_parser("2+tutu*2");
		cr_assert(add(p, &s), "Failed to add");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 8, "Failed to get 8");
		clean_parser(p);
		clean_in_scope(&s);
	}
}

Test(basic, check_line) {
	{
		struct scope s = {0};
		struct parser *p = new_parser("152;");
		cr_assert(line(p, &s), "Failed to line");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 152, "Failed to get 152");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		struct parser *p = new_parser("-(-(152));");
		cr_assert(line(p, &s), "Failed to line");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 152, "Failed to get 152");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		prepend_in_scope(&s, strdup("tutu"), 3);
		struct parser *p = new_parser("tutu=12;");
		cr_assert(line(p, &s), "Failed to line");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 12, "Failed to get 12");
		struct def_list *item = get_in_scope(&s, "tutu");
		cr_assert(item != NULL, "Failed to get_in_scope");
		cr_assert(item->val == 12, "Failed to get value of item");
		clean_parser(p);
		clean_in_scope(&s);
	}
}

Test(basic, check_calc) {
	{
		struct scope s = {0};
		struct parser *p = new_parser("152;");
		cr_assert(my_calc(p, &s), "Failed to my_calc");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 152, "Failed to get 152");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		struct parser *p = new_parser("-(-(152));");
		cr_assert(my_calc(p, &s), "Failed to my_calc");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 152, "Failed to get 152");
		clean_parser(p);
		clean_in_scope(&s);
	}
	{
		struct scope s = {0};
		prepend_in_scope(&s, strdup("tutu"), 3);
		struct parser *p = new_parser("tutu=12; titi=2*tutu;");
		cr_assert(my_calc(p, &s), "Failed to my_calc");
		cr_assert(readeof(p), "Failed to read EOF");
		cr_assert(s.current_val == 24, "Failed to get 24");
		struct def_list *item = get_in_scope(&s, "tutu");
		cr_assert(item != NULL, "Failed to get_in_scope");
		cr_assert(item->val == 12, "Failed to get value of item");
		struct def_list *item2 = get_in_scope(&s, "titi");
		cr_assert(item2 != NULL, "Failed to get_in_scope titi");
		cr_assert(item2->val == 24, "Failed to get value of item titi");
		clean_parser(p);
		clean_in_scope(&s);
	}
}
