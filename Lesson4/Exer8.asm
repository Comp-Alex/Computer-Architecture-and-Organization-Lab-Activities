.MODEL SMALL
.STACK 100h
.DATA
message db 43h,6Fh,6Dh,70h,75h,74h,65h,72h,20h,4Fh,72h,67h,61h,6Eh,69h,7Ah,61h,74h,69h,6Fh,6Eh,20h,61h,6Eh,64h,20h,41h,73h,73h,65h,6Dh,62h,6Ch,79h,20h,4Ch,61h,6Eh,67h,75h,61h,67h,65h,0Dh,0Ah,46h,75h,6Eh,63h,74h,69h,6Fh,6Eh,20h,30h,39h,68h,20h,73h,74h,72h,69h,6Eh,67h,20h,64h,69h,73h,70h,6Ch,61h,79h,0Dh,0Ah,24h
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