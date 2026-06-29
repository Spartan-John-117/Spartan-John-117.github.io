section .text
global my_factorial

my_factorial: 

	cmp rdi, 0 		; Vérifier si la valeur de rdi (n) est 0, auquel cas notre récursivité s'arrête
	je default_result	; Si la valeur de rdi est 0, on saute l'instruction default

	push rdi 		; On enregistre la valeur de rdi sur la piler
	dec rdi 		; On décrémente rdi de 1 pour la récusrvité
	call my_factorial 	; Appel de my_factorial pour la récursivité
	pop rdi			; A la fin de la récursivité on récupère la valeur précédente de rdi
	imul rax, rdi		; Multiplication de la valeur de rax par celle de rdi. D'ou l'interêt de
				; récupéré la valeur précédente de rdi. A la fin de la récursivité, rdi vaut 0
				; on ne peut pas multiplier par 0 sans se retrouver dans une boucle infinie
				; Imul sert à gérer les entier positif ou négatif et aussi à stocker le résultat
				; dans rax uniquement (au lieu de deux registres rax rdx avec mul)
	ret
	


default_result:			; Fonction default qui permet de sortir de la récursivité
	mov rax, 1		; Si la valeur de rdi est 0, alors la valeur de rax passe à 1 car
				; la factorielelle de 0 est 1
	ret
	
