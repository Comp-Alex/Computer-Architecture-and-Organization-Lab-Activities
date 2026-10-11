.MODEL SMALL
.STACK 100h

.DATA
prompt DB 'ENTER YOUR NAME: $'
name DB 20, ?, 20 DUP(0)

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    ; Clear screen
    MOV AH, 06h
    MOV AL, 00h
    MOV BH, 07h
    MOV CH, 00h
    MOV CL, 00h
    MOV DH, 24
    MOV DL, 79
    INT 10h

    ; Position cursor
    MOV AH, 02h
    MOV BH, 00h
    MOV DH, 10
    MOV DL, 20
    INT 10h

    LEA DX, prompt
    MOV AH, 09h
    INT 21h

    LEA DX, name
    MOV AH, 0Ah
    INT 21h

    MOV AX, 4C00h
    INT 21h
MAIN ENDP
END MAIN
