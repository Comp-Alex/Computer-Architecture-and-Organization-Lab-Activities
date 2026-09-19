.MODEL SMALL
.STACK 100h
.DATA
card db 2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,0Dh,0Ah,2Ah,20h,20h,20h,20h,20h,20h,53h,54h,55h,44h,45h,4Eh,54h,20h,43h,41h,52h,44h,20h,20h,20h,20h,20h,2Ah,0Dh,0Ah,2Ah,20h,20h,41h,73h,73h,65h,6Dh,62h,6Ch,79h,20h,50h,72h,6Fh,67h,72h,61h,6Dh,6Dh,65h,72h,20h,20h,20h,2Ah,0Dh,0Ah,2Ah,20h,20h,73h,74h,75h,64h,65h,6Eh,74h,40h,65h,78h,61h,6Dh,70h,6Ch,65h,2Eh,63h,6Fh,6Dh,20h,20h,20h,20h,2Ah,0Dh,0Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,2Ah,24h
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