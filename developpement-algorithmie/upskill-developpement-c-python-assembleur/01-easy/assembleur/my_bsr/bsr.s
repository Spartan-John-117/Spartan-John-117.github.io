section .text
global my_bsr
	
my_bsr:
	BSR rax,rdi
	ret
	
