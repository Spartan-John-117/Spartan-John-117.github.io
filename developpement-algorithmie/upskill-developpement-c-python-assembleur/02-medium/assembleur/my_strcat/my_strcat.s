section .text
    global my_strcat

my_strcat:
                                ; rdi = dst (destination string)
                                ; rsi = src (source string)
    mov rax, rdi                ; Enregistrer l'emplacement de dst pour le retourner    
                                ; en fin de fonction

find_end:                       ; Instruction qui :
    cmp byte [rdi], 0           ; Compare le caractère actuel avec 0
    je append_src               ; si c'est un 0, on saute à la fonction append
    inc rdi                     ; sinon on passe au caractère suivant
    jmp find_end                ; Si on arrive à cette instruction, on boucle

append_src:
    xor rcx, rcx                ; Met rcx à zéro
    mov cl, byte [rsi]          ; Copie le caractère contenu dans rsi dans un sous-registre de 
                                ; rcx (cl, ne fait que 8bits alors que rcx  en fait 64)
    mov [rdi], cl               ; Enregistre les 8bits de poids faible (le caractère sans 
                                ; les 0 à la suite) à l'adresse de rdi obtenue à la fin de
                                ; la boucle find

    test cl, cl                 ; Vérifie si le caractère est nul (fin de chaîne de caractères)
    je done                     ; Si oui, la copie est terminée
    inc rdi                     ; Avancer dans dst
    inc rsi                     ; Avancer dans src
    jmp append_src              ; création d'une boucle

done:
    ; Retourner l'adresse de dst
    ret

