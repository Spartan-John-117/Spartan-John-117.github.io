section .text
global my_max

my_max:

	xor rax, rax
	cmp rdi, rsi
	cmovg rax, rdi
	cmp rsi, rdi
	cmovg rax, rsi
	cmp rdx, rax
	cmovg rax, rdx
	ret

	

