.MODEL SMALL
.STACK 100h
.CODE
main PROC
    mov cx,26
    mov bl,7Ah
    mov bh,41h
next_pair:
    mov dl,bl
    mov ah,02h
    int 21h
    mov dl,bh
    mov ah,02h
    int 21h
    dec bl
    inc bh
    loop next_pair
    mov ax,4C00h
    int 21h
main ENDP
END main