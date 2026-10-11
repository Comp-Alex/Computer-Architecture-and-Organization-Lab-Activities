.MODEL SMALL
.STACK 100h

.CODE
main PROC
    mov ax, @data
    mov ds, ax

    mov ch, 0
    mov cl, 0

loop_row:
    cmp cl, 20
    je done

    mov dl, 'A'
    mov ah, 02h
    int 21h

    mov dl, 0Ah
    mov ah, 02h
    int 21h

    inc cl
    jmp loop_row

done:
    mov ax, 4C00h
    int 21h
main ENDP
END main
