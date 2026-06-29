section .text
global my_sum

my_sum:

	mov rax, rdi 		; On initialise rax avec la valeur de rdi
	add rax, rsi		; On ajoute rsi au registre rax
	add rax, rdx		; On ajoute rdx au registre rax 
	add rax, rcx		; On ajoute rcx au registre rax
	add rax,  r8		; On ajoute r8 au registre rax
	add rax,  r9		; On ajoute r9 au registre rax
	
	mov rbx, [rsp+8]	; On initialise rbx avec la valeur contenue à l'adresse rsp+8 (soit le 7e argument)
	add rax, rbx		; On ajoute rbx au registre rax

	ret
