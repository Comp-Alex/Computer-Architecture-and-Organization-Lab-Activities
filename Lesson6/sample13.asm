.MODEL SMALL
.STACK 100h

.DATA
upperMsg DB 'UPPERCASE LETTER$'
lowerMsg DB 'LOWERCASE LETTER$'

.CODE
MAIN PROC
    MOV AX, @DATA
    MOV DS, AX

    MOV AH, 07h
    INT 21h
    MOV BL, AL

    MOV AH, 02h
    MOV DL, 0Dh
    INT 21h
    MOV DL, 0Ah
    INT 21h

    CMP BL, 'A'
    JB exit
    CMP BL, 'Z'
    JBE upper
    CMP BL, 'a'
    JB exit
    CMP BL, 'z'
    JBE lower
    JMP exit

upper:
    LEA DX, upperMsg
    MOV AH, 09h
    INT 21h
    JMP exit

lower:
    LEA DX, lowerMsg
    MOV AH, 09h
    INT 21h

exit:
    MOV AX, 4C00h
    INT 21h
MAIN ENDP
END MAIN
