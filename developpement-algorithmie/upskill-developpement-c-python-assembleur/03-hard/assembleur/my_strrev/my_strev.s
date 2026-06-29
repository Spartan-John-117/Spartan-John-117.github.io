section .text
    global my_strrev
    extern malloc, free

my_strrev:
    
    push rbp
    mov rbp, rsp
    sub rsp, 32

    ; Arguments
    mov rdi, rsi  ; rdi = s

    ; Calculate the length of the string
    xor rcx, rcx
    mov rax, rdi
strlen_loop:
    cmp byte [rax + rcx], 0
    je strlen_done
    inc rcx
    jmp strlen_loop
strlen_done:
    ; rcx now contains the length of the string

    ; Allocate memory for the reversed string
    mov rdi, rcx
    add rdi, 1  ; +1 for the null terminator
    call malloc
    mov rbx, rax  ; rbx = allocated memory

    ; Reverse the string
    mov rsi, rdi  ; rsi = length of the string
    dec rsi       ; rsi = length - 1 (index of the last character)
    xor rdx, rdx  ; rdx = 0 (index of the first character)
reverse_loop:
    cmp rdx, rcx
    jge reverse_done
    mov al, [rdi + rdx]
    mov [rbx + rsi], al
    inc rdx
    dec rsi
    jmp reverse_loop
reverse_done:
    ; Null-terminate the reversed string
    mov byte [rbx + rcx], 0

    ; Epilogue
    mov rax, rbx  ; Return the reversed string
    add rsp, 32
    pop rbp
    ret