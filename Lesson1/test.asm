.model small
.stack 100h
.code

start:
    mov ah, 02h

    mov dl, 'H'
    int 21h

    mov dl, 'e'
    int 21h

    mov dl, 'l'
    int 21h

    mov dl, 'l'
    int 21h

    mov dl, 'o'
    int 21h

    mov dl, ' '
    int 21h

    mov dl, 'C'
    int 21h

    mov dl, 'p'
    int 21h

    mov dl, 'E'
    int 21h

    mov ah, 4Ch
    int 21h

end start