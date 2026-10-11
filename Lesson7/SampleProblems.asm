.MODEL SMALL
.STACK 100h

.CODE
main PROC
    mov dx, 0378h
    mov al, 55h
    out dx, al

    mov cx, 5

wait_loop:
    nop
    loop wait_loop

    mov al, 0AAh
    out dx, al

    mov ax, 4C00h
    int 21h
main ENDP
END main
