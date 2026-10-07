.MODEL SMALL
.STACK 100h

.DATA
titleText db '75% TV COLOR BARS'
titleTextLen EQU $ - titleText
networkText db 'GMA NETWORK - COLOR BAR TEST PATTERN'
networkTextLen EQU $ - networkText

.CODE
main PROC
    mov ax, 0003h
    int 10h

    mov ax, @data
    mov ds, ax
    mov es, ax

    mov dh, 1
    mov dl, 31
    mov bp, OFFSET titleText
    mov cx, titleTextLen
    mov bl, 0Fh
    mov bh, 0
    mov ax, 1301h
    int 10h

    ; Main 7-bar pattern: white, yellow, cyan, green, magenta, red, blue.
    mov dh, 4
    mov dl, 5
    mov bl, 0Fh
    mov si, 10
    call DrawBar

    mov dh, 4
    mov dl, 15
    mov bl, 0Eh
    mov si, 10
    call DrawBar

    mov dh, 4
    mov dl, 25
    mov bl, 0Bh
    mov si, 10
    call DrawBar

    mov dh, 4
    mov dl, 35
    mov bl, 0Ah
    mov si, 10
    call DrawBar

    mov dh, 4
    mov dl, 45
    mov bl, 0Dh
    mov si, 10
    call DrawBar

    mov dh, 4
    mov dl, 55
    mov bl, 0Ch
    mov si, 10
    call DrawBar

    mov dh, 4
    mov dl, 65
    mov bl, 09h
    mov si, 10
    call DrawBar

    ; Lower reference row: blue, black, magenta, black, cyan, black, gray.
    mov dh, 14
    mov dl, 5
    mov bl, 09h
    mov si, 3
    call DrawBar

    mov dh, 14
    mov dl, 15
    mov bl, 00h
    mov si, 3
    call DrawBar

    mov dh, 14
    mov dl, 25
    mov bl, 0Dh
    mov si, 3
    call DrawBar

    mov dh, 14
    mov dl, 35
    mov bl, 00h
    mov si, 3
    call DrawBar

    mov dh, 14
    mov dl, 45
    mov bl, 0Bh
    mov si, 3
    call DrawBar

    mov dh, 14
    mov dl, 55
    mov bl, 00h
    mov si, 3
    call DrawBar

    mov dh, 14
    mov dl, 65
    mov bl, 07h
    mov si, 3
    call DrawBar

    mov dh, 19
    mov dl, 21
    mov bp, OFFSET networkText
    mov cx, networkTextLen
    mov bl, 0Fh
    mov bh, 0
    mov ax, 1301h
    int 10h

    mov ax, 4C00h
    int 21h
main ENDP

DrawBar PROC
    push ax
    push bx
    push cx
    push dx
    push si
    push di

    mov di, 10

DrawBarRow:
    mov ah, 02h
    mov bh, 0
    int 10h

    mov ah, 09h
    mov al, 0DBh
    mov cx, di
    int 10h

    inc dh
    dec si
    jnz DrawBarRow

    pop di
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
DrawBar ENDP

END main
