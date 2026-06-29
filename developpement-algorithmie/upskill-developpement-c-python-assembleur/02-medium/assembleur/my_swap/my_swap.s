section .text
global my_swap

my_swap:	

	mov rax, [rdi] ; On attribue à rax la valeur contenue dans le registre rdi qui récupère le paramètre
	mov rbx, [rsi] ; On attribue à rbx la valeur contenue dans le registre rsi qui récupère le paramètre
	mov [rdi], rbx ; On modifie la valeur contenue dans rdi par rbx
	mov [rsi], rax ; On modifie la valeur contenue dans rdi par rax
