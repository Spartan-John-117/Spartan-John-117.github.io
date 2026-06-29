section .text
global my_average

my_average:
	mov rax, rdi
	add rax, rsi
	add rax, rdx
	add rax, rcx
	xor rdx, rdx
	mov rbx, 4
	div rbx
	ret 
