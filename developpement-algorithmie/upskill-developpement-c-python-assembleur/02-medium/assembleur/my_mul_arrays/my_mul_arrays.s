section .text
global my_mul_arrays

my_mul_arrays:
    push rbp
    mov rbp, rsp

    xor rax, rax                    ; Initialiser rax à 0
    xor rcx, rcx                    ; Initialiser l'indice à 0

.loop:
    cmp rcx, 4                      ; Vérifie si l'indice >= 4
    jge .end

    mov rdx, [rdi + rcx*4]          ; rdi contient a, on le stocke dans rdx
    imul rdx, [rsi + rcx*4]         ; a * b et stocke dans rdx
    add rax, rdx                    

    inc rcx                         ; Incrémenter l'indice
    jmp .loop                       ; boucle

.end:
    mov rsp, rbp
    pop rbp
    ret                            

