section .text
global my_strlen

my_strlen:

	xor rax, rax		; Remise à zéro du registre rax avant de stocker une valeur
	
.loop:				; Création d'une boucle
	cmp byte[rdi], 0	; Si l'octet situé à l'emplacement actuel est vide
	je .done		; On sort de la boucle

	inc rax			; Sinon on incrémente le compteur de 1
	inc rdi			; On déplace le curseur de un, pour lire un nouveau caractère
	jmp .loop		; On répète la boucle pour tester le nouveau caractère

.done:
	ret
