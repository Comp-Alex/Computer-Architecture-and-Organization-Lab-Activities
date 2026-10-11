.MODEL SMALL
.STACK 100h

.DATA
prompt DB 'ENTER Y OR N: $'
yesMsg DB 'YES$'
noMsg DB 'NO$'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    LEA DX, prompt
    MOV AH, 09h
    INT 21h

    MOV AH, 01h
    INT 21h
    MOV BL, AL

    MOV AH, 02h
    MOV DL, 0Dh
    INT 21h
    MOV DL, 0Ah
    INT 21h

    CMP BL, 'Y'
    JE printYes
    CMP BL, 'y'
    JE printYes
    CMP BL, 'N'
    JE printNo
    CMP BL, 'n'
    JE printNo
    JMP exit

printYes:
    LEA DX, yesMsg
    MOV AH, 09h
    INT 21h
    JMP exit

printNo:
    LEA DX, noMsg
    MOV AH, 09h
    INT 21h

exit:
    MOV AX, 4C00h
    INT 21h
MAIN ENDP
END MAIN
