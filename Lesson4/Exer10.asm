.MODEL SMALL
.STACK 100h
.DATA
shows db 46h,61h,76h,6Fh,72h,69h,74h,65h,20h,54h,56h,20h,53h,68h,6Fh,77h,73h,0Dh,0Ah
      db 31h,2Eh,20h,4Eh,65h,74h,66h,6Ch,69h,78h,0Dh,0Ah
      db 32h,2Eh,20h,41h,64h,75h,6Ch,74h,73h,77h,69h,6Dh,0Dh,0Ah
      db 33h,2Eh,20h,43h,61h,72h,74h,6Fh,6Fh,6Eh,20h,4Eh,65h,74h,77h,6Fh,72h,6Bh,24h
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