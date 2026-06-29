section .text
global my_isalpha

my_isalpha:

	xor rax, rax
	cmp rdi, 0x41
	jl .non_alphabet
	cmp rdi, 0x5A
	jl .alphabet
	cmp rdi, 0x61
	jl .non_alphabet
	cmp rdi, 0x7A
	jl .alphabet

.alphabet:
	mov rax, 1
	ret

.non_alphabet:
	mov rax, 0
	ret
	
