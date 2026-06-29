#ifndef _MY_FIBO_H
#define _MY_FIBO_H 1

extern unsigned long my_fibo(unsigned long __n);

#endif /* _MY_FIBO_H */

unsigned long  my_fibo(unsigned long  n)
{
	if (n == 0)
		return 0;
	else if (n == 1)
		return 1;
	return  my_fibo(n-1) + my_fibo(n-2);    
}	
