.MODEL SMALL
.STACK 100h

.DATA
msg db 'HELLO FROM LAB 1$'

.CODE
main PROC
    mov ax, @data
    mov ds, ax

    lea dx, msg
    mov ah, 09h
    int 21h

    mov ax, 4C00h
    int 21h
main ENDP
END main
