.MODEL SMALL
.STACK 100h

.DATA
line1 DB 'COMPUTER ARCHITECTURE$'
line2 DB 'LAB 5$'
line3 DB 'SCREEN GRAPHICS$'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Set text mode
    MOV AH, 00h
    MOV AL, 03h
    INT 10h

    ; Scroll down 5 lines
    MOV AH, 06h
    MOV AL, 05h
    MOV BH, 1Fh
    MOV CH, 00h
    MOV CL, 00h
    MOV DH, 24
    MOV DL, 79
    INT 10h

    ; Position cursor and print line 1
    MOV AH, 02h
    MOV BH, 00h
    MOV DH, 08h
    MOV DL, 12
    INT 10h
    LEA DX, line1
    MOV AH, 09h
    INT 21h

    ; Position cursor and print line 2
    MOV AH, 02h
    MOV BH, 00h
    MOV DH, 10h
    MOV DL, 18
    INT 10h
    LEA DX, line2
    MOV AH, 09h
    INT 21h

    ; Position cursor and print line 3
    MOV AH, 02h
    MOV BH, 00h
    MOV DH, 12h
    MOV DL, 15
    INT 10h
    LEA DX, line3
    MOV AH, 09h
    INT 21h

    MOV AX, 4C00h
    INT 21h
MAIN ENDP
END MAIN
