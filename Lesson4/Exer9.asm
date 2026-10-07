.MODEL SMALL
.STACK 100h
.DATA
card db 2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,0Dh,0Ah
     db 2Ah,20h,41h,4Ch,45h,58h,41h,4Eh,44h,45h,52h,20h,4Ahh,4Fh,48h,4Eh,20h,43h,2Eh,20h,42h,41h,4Ch,41h,47h,53h,4Fh,20h,20h,2Ah,0Dh,0Ah
     db 2Ah,20h,43h,6Fh,6Dh,70h,75h,74h,65h,72h,20h,45h,6Eh,67h,69h,6Eh,65h,65h,72h,20h,20h,20h,20h,20h,20h,20h,2Ah,0Dh,0Ah
     db 2Ah,20h,45h,6Dh,61h,69h,6Ch,3Ah,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,2Ah,0Dh,0Ah
     db 2Ah,20h,61h,6Ch,65h,78h,61h,6Eh,64h,65h,72h,6Ah,6Fh,68h,6Eh,62h,61h,6Ch,61h,67h,73h,6Fh,40h,20h,20h,20h,20h,20h,20h,2Ah,0Dh,0Ah
     db 2Ah,20h,67h,6Dh,61h,69h,6Ch,2Eh,63h,6Fh,6Dh,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,20h,2Ah,0Dh,0Ah
     db 2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,24h
.CODE
main PROC
    mov ax,@data
    mov ds,ax
    mov dx,offset card
    mov ah,09h
    int 21h
    mov ax,4C00h
    int 21h
main ENDP
END main