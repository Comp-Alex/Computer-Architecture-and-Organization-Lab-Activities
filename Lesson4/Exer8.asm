.MODEL SMALL
.STACK 100h
.DATA
message db 43h,3Ah,5Ch,54h,41h,53h,4Dh,3Eh,61h,75h,74h,68h,6Fh,72h,0Dh,0Ah
        db 41h,6Ch,65h,78h,61h,6Eh,64h,65h,72h,20h,4Ah,6Fh,68h,6Eh,20h,42h,61h,6Ch,61h,67h,73h,6Fh,0Dh,0Ah
        db 43h,6Fh,6Dh,70h,75h,74h,65h,72h,20h,45h,6Eh,67h,69h,6Eh,65h,65h,72h,69h,6Eh,67h,0Dh,0Ah
        db 43h,3Ah,5Ch,54h,41h,53h,4Dh,3Eh,24h
.CODE
main PROC
    mov ax,@data
    mov ds,ax
    mov dx,offset message
    mov ah,09h
    int 21h
    mov ax,4C00h
    int 21h
main ENDP
END main