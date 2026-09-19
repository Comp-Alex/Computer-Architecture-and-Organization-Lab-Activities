.MODEL SMALL
.STACK 100h
.DATA
.CODE
main PROC
    mov ax, @data
    mov ds, ax

    mov dl, 41H
    mov ah,02h
    int 21h
    mov dl, 6CH
    mov ah,02h
    int 21h
    mov dl, 65H
    mov ah,02h
    int 21h
    mov dl, 78H
    mov ah,02h
    int 21h
    mov dl, 61H
    mov ah,02h
    int 21h
    mov dl, 6EH
    mov ah,02h
    int 21h
    mov dl, 64H
    mov ah,02h
    int 21h
    mov dl, 65H
    mov ah,02h
    int 21h
    mov dl, 72H
    mov ah,02h
    int 21h
    mov dl, 20H
    mov ah,02h
    int 21h
    mov dl, 4AH
    mov ah,02h
    int 21h
    mov dl, 6FH
    mov ah,02h
    int 21h
    mov dl, 68H
    mov ah,02h
    int 21h
    mov dl, 6EH
    mov ah,02h
    int 21h

    mov dl, 0Dh
    mov ah,02h
    int 21h
    mov dl, 0Ah
    mov ah,02h
    int 21h

    mov dl, 43H
    mov ah,02h
    int 21h
    mov dl, 2EH
    mov ah,02h
    int 21h

    mov dl, 0Dh
    mov ah,02h
    int 21h
    mov dl, 0Ah
    mov ah,02h
    int 21h

    mov dl, 42H
    mov ah,02h
    int 21h
    mov dl, 61H
    mov ah,02h
    int 21h
    mov dl, 6CH
    mov ah,02h
    int 21h
    mov dl, 61H
    mov ah,02h
    int 21h
    mov dl, 67H
    mov ah,02h
    int 21h
    mov dl, 73H
    mov ah,02h
    int 21h
    mov dl, 6FH
    mov ah,02h
    int 21h
    
    mov ax, 4C00h
    int 21h
main ENDP

END main 