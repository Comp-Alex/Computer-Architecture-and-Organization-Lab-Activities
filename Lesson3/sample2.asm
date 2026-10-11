.MODEL SMALL
.STACK 100h

.CODE
main PROC
    mov ax, @data
    mov ds, ax

    mov cx, 20
    mov dl, 'A'

print_loop:
    mov ah, 02h
    int 21h
    loop print_loop

    mov dl, 0Dh
    mov ah, 02h
    int 21h

    mov dl, 0Ah
    mov ah, 02h
    int 21h

    mov ax, 4C00h
    int 21h
main ENDP
END main
