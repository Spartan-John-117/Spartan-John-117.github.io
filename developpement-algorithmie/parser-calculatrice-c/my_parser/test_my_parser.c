#include "my_parser.h"
#include <criterion/criterion.h>
#include <stdio.h>


Test(basic, check_eof)
{
    {
        struct parser *p = new_parser("");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("tutu");
        cr_assert(!readeof(p), "failed to readeof");
        clean_parser(p);
    }
}

Test(basic, check_char)
{
    {
        struct parser *p = new_parser("");
        cr_assert(!readchar(p, 'x'), "failed to readchar");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("tutu");
        cr_assert(readchar(p, 't'), "failed to readchar");
        cr_assert(readchar(p, 'u'), "failed to readchar");
        cr_assert(readchar(p, 't'), "failed to readchar");
        cr_assert(readchar(p, 'u'), "failed to readchar");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
}
Test(basic, check_text)
{
    {
        struct parser *p = new_parser("");
        cr_assert(!readtext(p, "tutu"), "failed to readtext");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("tutu");
        cr_assert(readtext(p, "tutu"), "failed to readtext");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("tu");
        cr_assert(!readtext(p, "tutu"), "failed to readtext");
        cr_assert(readtext(p, "tu"), "failed to readtext");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("tuta");
        cr_assert(readtext(p, "tu"), "failed to readtext");
        cr_assert(readtext(p, "ta"), "failed to readtext");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
}
Test(basic, check_range)
{
    {
        struct parser *p = new_parser("");
        cr_assert(!readrange(p, 'a', 'z'), "failed to readrange");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("1t2t3x");
        cr_assert(readrange(p, '0', '9'), "failed to readrange");
        cr_assert(readrange(p, 'a', 'z'), "failed to readrange");
        cr_assert(readrange(p, '0', '9'), "failed to readrange");
        cr_assert(readrange(p, 'a', 'z'), "failed to readrange");
        cr_assert(readrange(p, '0', '9'), "failed to readrange");
        cr_assert(readrange(p, 'a', 'z'), "failed to readrange");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
}
Test(basic, check_int)
{
    {
        struct parser *p = new_parser("");
        cr_assert(!readint(p), "failed to readint");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("12345");
        cr_assert(readint(p), "failed to readint");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("12345tutu");
        cr_assert(readint(p), "failed to readint");
        cr_assert(readtext(p, "tutu"), "failed to readtext");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("tutu12345titi");
        cr_assert(readtext(p, "tutu"), "failed to readtext");
        cr_assert(readint(p), "failed to readint");
        cr_assert(readtext(p, "titi"), "failed to readtext");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
}
Test(basic, check_id)
{
    {
        struct parser *p = new_parser("");
        cr_assert(!readid(p), "failed to readid");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("12345_juju15");
        cr_assert(!readid(p), "failed to readid");
        cr_assert(readint(p), "failed to readint");
        cr_assert(readid(p), "failed to readid");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("tutu12titi");
        cr_assert(readid(p), "failed to readid");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
}

int              readfloat_dec(struct parser *p);

Test(basic, check_float_dec)
{
    {
        struct parser *p = new_parser("");
        cr_assert(!readfloat_dec(p), "failed to readid");
        clean_parser(p);  
    }
    {
        struct parser *p = new_parser("34.");
        cr_assert(readfloat_dec(p), "failed to readfloat_dec");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    } 
    {
        struct parser *p = new_parser("45.1");
        cr_assert(readfloat_dec(p), "failed to readfloat_dec");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("345.tutu");
        cr_assert(readfloat_dec(p), "failed to readfloat_dec");
        cr_assert(readtext(p, "tutu"), "failed to readtext");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
}

int              readfloat_frac(struct parser *p);

Test(basic, check_float_frac)
{
    {
        struct parser *p = new_parser("");
        cr_assert(!readfloat_frac(p), "failed to readfloat_frac");
        clean_parser(p);  
    }
    {
        struct parser *p = new_parser(".14");
        cr_assert(readfloat_frac(p), "failed to readfloat_frac");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("45.1.14");
        cr_assert(readfloat_dec(p), "failed to readfloat_dec");
        cr_assert(readfloat_frac(p), "failed to readfloat_frac");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("qwerty.14");
        cr_assert(readtext(p, "qwerty"), "failed to readtext");
        cr_assert(readfloat_frac(p), "failed to readfloat_frac");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser(".qwerty");
        cr_assert(!readfloat_frac(p), "failed to readfloat_frac");
        cr_assert(readtext(p, ".qwerty"), "failed to readtext");
        cr_assert(readeof(p), "failed to readeof");
        clean_parser(p);
    }
}

int              readfloat_exp(struct parser *p);

Test(basic, check_float_exp)
{
    {
        struct parser *p = new_parser("");
        cr_assert(!readfloat_exp(p), "failed to readfloat_exp");
        clean_parser(p);  
    }
    {
        struct parser *p = new_parser("e32");
        cr_assert(readfloat_exp(p), "failed to readfloat_exp");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("E32");
        cr_assert(readfloat_exp(p), "failed to readfloat_exp");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("e-32");
        cr_assert(readfloat_exp(p), "failed to readfloat_exp");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("e+32");
        cr_assert(readfloat_exp(p), "failed to readfloat_exp");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("E+32");
        cr_assert(readfloat_exp(p), "failed to readfloat_exp");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("E-32");
        cr_assert(readfloat_exp(p), "failed to readfloat_exp");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("10E-32");
        cr_assert(readint(p), "failed to readint");
        cr_assert(readfloat_exp(p), "failed to readfloat_exp");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("E-ed");
        cr_assert(!readfloat_exp(p), "failed to readfloat_exp");
        cr_assert(readtext(p, "E-ed"), "failed to readtext");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("Execute");
        cr_assert(!readfloat_exp(p), "failed to readfloat_exp");
        cr_assert(readtext(p, "Execute"), "failed to readtext");
        clean_parser(p);
    }
}

int                     readfloat(struct parser *p);

Test(basic, check_float)
{
    {
        struct parser *p = new_parser("");
        cr_assert(!readfloat(p), "failed to readfloat");
        clean_parser(p);  
    }
    {
        struct parser *p = new_parser("10.32e-32");
        cr_assert(readfloat(p), "failed to readfloat");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("10.32E+32");
        cr_assert(readfloat(p), "failed to readfloat");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("10.32E-32tutu");
        cr_assert(readfloat(p), "failed to readfloat");
        cr_assert(readtext(p, "tutu"), "failed to readtext");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser("10.32tutu");
        cr_assert(readfloat(p), "failed to readfloat");
        cr_assert(readtext(p, "tutu"), "failed to readtext");
        clean_parser(p);
    }
    {
        struct parser *p = new_parser(".32tutu");
        cr_assert(readfloat(p), "failed to readfloat");
        cr_assert(readtext(p, "tutu"), "failed to readtext");
        clean_parser(p);
    }
    
}