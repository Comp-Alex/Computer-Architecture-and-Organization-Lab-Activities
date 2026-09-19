.MODEL SMALL
.STACK 100h
.DATA
shows db 46h,61h,76h,6Fh,72h,69h,74h,65h,20h,54h,56h,20h,53h,68h,6Fh,77h,73h,0Dh,0Ah,31h,2Eh,20h,4Eh,65h,77h,73h,72h,6Fh,6Fh,6Dh,0Dh,0Ah,32h,2Eh,20h,53h,63h,69h,65h,6Eh,63h,65h,20h,54h,6Fh,64h,61h,79h,0Dh,0Ah,33h,2Eh,20h,57h,6Fh,72h,6Ch,64h,20h,53h,70h,6Fh,72h,74h,73h,0Dh,0Ah,34h,2Eh,20h,45h,76h,65h,6Eh,69h,6Eh,67h,20h,53h,74h,6Fh,72h,69h,65h,73h,24h
.CODE
main PROC
    mov ax,@data
    mov ds,ax
    mov dx,offset shows
    mov ah,09h
    int 21h
    mov ax,4C00h
    int 21h
main ENDP
END main