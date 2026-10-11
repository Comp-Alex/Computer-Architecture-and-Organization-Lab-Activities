.MODEL SMALL
.STACK 100h

.CODE
main PROC
    mov ax, @data
    mov ds, ax

    mov cx, 10
    mov bl, '9'

print_num:
    mov dl, bl
    mov ah, 02h
    int 21h
    dec bl
    loop print_num

    mov ax, 4C00h
    int 21h
main ENDP
END main
