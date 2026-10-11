.model small
.stack
.data
    var1 DB 'Proud to be an Engineer',13,10,'$'
    var2 DB 'Good teachers can produce',13,10,'$'
    var3 DB 'Great Engineers',13,10,'$'
.code
start:
    mov ax,@data
    mov ds,ax
    mov ah,09h
    mov dx,offset var1
    int 21h
    mov ah,09h
    mov dx,offset var2
    int 21h
    mov ah,09h
    mov dx,offset var3
    int 21h
    mov ah,4ch
    int 21h
end start
