section .text
global my_fillstruct

	; xmm0 : premier registre pouvant contenir un nombre à virgule flottante (precis ASM p.95)

	; Le champ "i" est stocké sur la pile à l'adresse rdi car c'est le premier argument attendu

	; Le champ "d" est stocké sur la pile à l'adresse rdi+8 car il est le deuxième argument attendu
	; et qu'en 64bit on décale de 8octets en 8octets

my_fillstruct:
	mov [rdi], rsi 				; Copie la valeur de rsi dans le premier champ
								; de _my_struct situé à l'adresse donnée par rdi (correspond à i)

	sub rsp, 8 					; Décale le stack pointer de 8 octets pour créer
								; un emplacement libre pour stocker le flottant

	movsd [rsp], xmm0			; Copie la valeur contenue dans xmm0 à l'emplacement précedemment créé.
								; movsd (precis ASM p.52)

	fld qword [rsp]				; Copie la valeur contenue à l'emplacement rsp (de taille 8 octets)
								; sur le dessus de la pile FPU (floting point unit) à l'emplacement 0
								; (décale la valeur	précédante (emplacement +1), s'il y'en a une.)

	fstp qword [rdi + 8]		; Stocke la valeur précemment placée sur le dessus de la FPU
								; à l'emplacement rdi + 8

	add rsp, 8					; Décale le stack pointer de 8 octets pour libérer l'espace
								; réservé en début de fonction

	ret
