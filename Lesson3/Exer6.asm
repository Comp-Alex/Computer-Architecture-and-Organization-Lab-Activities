.MODEL SMALL
.STACK 100h
.CODE
main PROC
    mov cx,26
    mov bl,61h
    mov bh,5Ah
next_pair:
    mov dl,bl
    mov ah,02h
    int 21h
    mov dl,bh
    mov ah,02h
    int 21h
    mov dl,0Dh
    mov ah,02h
    int 21h
    mov dl,0Ah
    mov ah,02h
    int 21h
    inc bl
    dec bh
    loop next_pair
    mov ax,4C00h
    int 21h
main ENDP
END main