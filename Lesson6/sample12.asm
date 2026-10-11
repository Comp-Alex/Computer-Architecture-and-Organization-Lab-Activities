.MODEL SMALL
.STACK 100h

.DATA
prompt DB 'PRESS 10 KEYS: $'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, prompt
    MOV AH, 09h
    INT 21h

    MOV CX, 10

readLoop:
    MOV AH, 01h
    INT 21h
    MOV DL, AL
    MOV AH, 02h
    INT 21h
    LOOP readLoop

    MOV AH, 02h
    MOV DL, 0Dh
    INT 21h
    MOV DL, 0Ah
    INT 21h

    MOV AX, 4C00h
    INT 21h
MAIN ENDP
END MAIN
