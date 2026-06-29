section .text
global my_whereami

; lea : sert à récupérer l'adresse en cours. L'adresse de la première
; instruction = l'adresse de la fonction

; Pour être sur de récupère la taille complète de la fonction, on crée une autre
; fonction à la suite, et on retourne son adresse, ce qui correspond à la fin de
; la fonction précédente.

my_whereami:
    lea rax, [my_whereami]     	; On récupère la position de départ de la fonction
								; et on la stocke dans rax

    mov [rdi], rax             	; "Where" est le premier paramètre, il est donc
							   	; stocké dans rdi


    lea rax, [my_whereami_end] 	; On récupère la position de départ de la fonction
								; suivante, et on la stocke dans rax

    sub rax, my_whereami       	; La soustraction de l'adresse de début de la fonction
								; my_wherami_end - l'adresse de début de la fonction
								; my_wherami donne la taille en octets de la fonction
								; my_whereami
	
    ret

my_whereami_end:				; Nouvelle fonction crée pour permettre le calcul 
								; de la fonction my_wherami

