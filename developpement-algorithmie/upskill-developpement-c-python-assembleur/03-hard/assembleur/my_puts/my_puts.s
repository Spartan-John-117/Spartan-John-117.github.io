section .data           ; Contient les données
    newline db 10       ; Caractère de saut de ligne (10 dans le code ASCII)

section .text           ; Contient le code
    global my_puts

my_puts:
    push rbp            ; Sauvegarde la valeur de rbp au début de la fonction
    mov rbp, rsp        ; Initialise rbp avec la valeur de rsp
    mov rdi, [rbp+16]   ; Récupère la valeur de char * dans rdi
    xor rcx, rcx        ; Initialise rcx à 0 pour compter la longueur de la chaîne
    mov rax, rdi        ; Initialise rax avec la valeur de char * pour parcourir la chaîne

find_end:
    cmp byte [rax], 0   ; Compare le caractère actuel avec 0 (fin de la chaîne)
    je end_find         ; Si le caractère est 0, on saute à la fonction end_find
    inc rax             ; Incrémente rax pour passer au caractère suivant
    inc rcx             ; Incrémente rcx pour compter la longueur de la chaîne
    jmp find_end        ; On boucle jusqu'au dernier caractère

end_find:
    mov rax, 1          ; En mettant rax = 1, on appelle sys_write
    mov rdi, 1          ; En mettant rdi = 1 on précsie la sortie stdout (écran)
    mov rsi, rdi        ; On met l'adresse de la chaîne dans rsi
    mov rdx, rcx        ; On met la longueur de la chaîne calculée dans find_end, dans rdx
    syscall             ; On effectue l'appel systeme sys_write

    mov rax, 1          
    mov rdi, 1          
    lea rsi, [newline]  ; On charge la valeur de newline dans rsi. 
                        ; lea est l'équivalent de mov rsi, newline
    mov rdx, 1          ; longueur du saut de ligne
    syscall

    mov eax, 0          ; valeur de retour (0 pour succès)
    pop rbp             ; Restaure la valeur de rbp à la fin de la fonction
    ret