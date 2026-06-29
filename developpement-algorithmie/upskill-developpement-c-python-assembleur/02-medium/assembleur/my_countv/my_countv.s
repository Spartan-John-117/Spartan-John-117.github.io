section .text
    global my_countv

my_countv:
    push rbp                            ; Sauvegarde la position du pointeur
                                        ; au début de la fonction, pour pouvoir
                                        ; la retourner à la fin.

    mov rbp, rsp                        ; Initialise le pointeur de base avec
                                        ; la valeur du stack-pointer.

    mov rdi, rdi                        ; rdi = s (adresse de la chaîne)
    mov rsi, rsi                        ; rsi = size (taille de la chaîne)
    mov rdx, rdx                        ; rdx = v (tableau des résultats)

    xor rax, rax                        ; Remet rax à 0 puisque c'est l'indice
                                        ; pour parcourir le tableau "v".

    mov rcx, 6                          ; 6 voyelles

clear_v:                                
    mov dword [rdx + rax*4], 0          ; Calcule l'emplacement de la case dans
                                        ; le tableau et lui attribue une valeur 0.

    inc rax                             ; Incrément rax (indice du tableau) de 1
    loop clear_v                        ; Crée une boucle

    xor rax, rax                        ; On remet rax à 0

next_char:
    cmp rax, rsi                        ; Index (rax) doit être <= à size (rsi)
    jge end_function                    ; Sinon on jump vers la fonction end

    mov bl, byte [rdi + rax]            ; Accède à un octet (caractère) dans rdi
                                        ; à l'indice rax et le charge dans bl qui 
                                        ; est une subdivision de rbx pour contenir
                                        ; un seul octet (et non 4 par défaut).
    cmp bl, 'a'
    je count_a
    cmp bl, 'e'                         ; Compare le caractère en cours avec chaque
    je count_e                          ; voyelle et saute à l'instruction 
    cmp bl, 'i'                         ; correspondante s'il y'a correspondance.
    je count_i
    cmp bl, 'o'
    je count_o
    cmp bl, 'u'
    je count_u
    cmp bl, 'y'
    je count_y
    
    jmp skip                            ; S'il n'y a aucune correspondance, saute à
                                        ; l'instruction skip

count_a:
    inc dword [rdx + 0*4]               ; Si cette fonction est activée, elle incrémente
                                        ; de 1, le registre correspondant
    jmp skip                            ; Saute à l'instruction skip
count_e:
    inc dword [rdx + 1*4]
    jmp skip
count_i:
    inc dword [rdx + 2*4]
    jmp skip
count_o:
    inc dword [rdx + 3*4]
    jmp skip
count_u:
    inc dword [rdx + 4*4]
    jmp skip
count_y:
    inc dword [rdx + 5*4]

skip:
    inc rax                             ; Incrémente l'index de 1
    jmp next_char                       ; Saute à l'instruction next

end_function:
    mov rsp, rbp                        ; Restaure la valeur de rsp avec rbp
    pop rbp                             ; Efface la valeur de rbp
    ret

