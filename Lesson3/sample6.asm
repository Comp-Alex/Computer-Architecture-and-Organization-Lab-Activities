.MODEL SMALL
.STACK 100h

.CODE
main PROC
    mov ax, @data
    mov ds, ax

    mov cx, 10
    mov bl, 'A'

print_char:
    mov dl, bl
    mov ah, 02h
    int 21h
    inc bl
    loop print_char

    mov ax, 4C00h
    int 21h
main ENDP
END main
