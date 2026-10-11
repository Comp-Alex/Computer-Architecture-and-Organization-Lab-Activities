.MODEL SMALL
.STACK 100h

.DATA
bigMsg DB 'BIG RECTANGLE$'
smallMsg DB 'SMALL RECTANGLE$'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Set text mode 80x25
    MOV AH, 00h
    MOV AL, 03h
    INT 10h

    ; Draw large rectangle at row 5, col 10
    MOV DH, 05h
    MOV DL, 10
    MOV CX, 12
    MOV BL, 1Eh

bigRect:
    MOV AH, 02h
    MOV BH, 00h
    INT 10h

    MOV AH, 09h
    MOV AL, ' '
    MOV BH, 00h
    MOV CX, 20
    INT 10h

    INC DH
    LOOP bigRect

    ; Draw small rectangle at row 12, col 20
    MOV DH, 12h
    MOV DL, 20
    MOV CX, 6
    MOV BL, 2Eh

smallRect:
    MOV AH, 02h
    MOV BH, 00h
    INT 10h

    MOV AH, 09h
    MOV AL, ' '
    MOV BH, 00h
    MOV CX, 10
    INT 10h

    INC DH
    LOOP smallRect

    ; Display labels
    MOV AH, 02h
    MOV BH, 00h
    MOV DH, 07h
    MOV DL, 12
    INT 10h
    LEA DX, bigMsg
    MOV AH, 09h
    INT 21h

    MOV AH, 02h
    MOV BH, 00h
    MOV DH, 14h
    MOV DL, 21
    INT 10h
    LEA DX, smallMsg
    MOV AH, 09h
    INT 21h

    MOV AX, 4C00h
    INT 21h
MAIN ENDP
END MAIN
