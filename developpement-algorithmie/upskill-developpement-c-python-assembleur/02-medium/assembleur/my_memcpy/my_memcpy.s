section .text
global my_memcpy

my_memcpy:
                            ; rdi - dst (destination)
                            ; rsi - src (source)
                            ; edx - n (sous-regsitre 32bits de rdx)

    push rdi                ; Sauvegarde les deux registres
    push rsi

    test edx, edx           ; On vérifie si n = 0
    jz .done                ; Si oui, le programme est terminé

.copy_loop:
    mov al, byte [rsi]      ; Charger un seul octet depuis src
    mov byte [rdi], al      ; Copier l'octet vers dst
    inc rsi                 ; Incrémenter le pointeur src
    inc rdi                 ; Incrémenter le pointeur dst
    dec edx                 ; Décrémenter n
    jnz .copy_loop          ; Tant que l'opération au-dessus != 0
                            ; on boucle

.done:
    mov rax, rdi
    pop rsi
    pop rdi
    ret

