.MODEL SMALL
.STACK 100h
.CODE
main PROC
    mov ax,0003h
    int 10h
    mov dh,5
    mov dl,30
    mov si,8
row:
    mov bl,70h
    test si,1
    jz even_row
    mov bl,10h
even_row:
    mov di,8
square:
    mov al,20h
    mov cx,4
    mov ah,02h
    int 10h
    mov ah,09h
    mov bh,0
    int 10h
    add dl,4
    xor bl,60h
    dec di
    jnz square
    inc dh
    mov dl,30
    dec si
    jnz row
    mov ax,4C00h
    int 21h
main ENDP
END main