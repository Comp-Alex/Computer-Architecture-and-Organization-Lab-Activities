.MODEL SMALL
.STACK 100h
.DATA
promptName db 'Name: $'
promptCourse db 'Course/Section: $'
promptDate db 'Date: $'
nameBuffer db 24,0,24 dup(0)
courseBuffer db 24,0,24 dup(0)
dateBuffer db 24,0,24 dup(0)
.CODE
main PROC
    mov ax,@data
    mov ds,ax
    mov ax,0600h
    mov bh,07h
    mov cx,0000h
    mov dx,184Fh
    int 10h

    mov dh,2
    mov dl,10
    mov bh,0
    mov ah,02h
    int 10h
    mov dx,offset promptName
    mov ah,09h
    int 21h
    mov dx,offset nameBuffer
    mov ah,0Ah
    int 21h

    mov dh,4
    mov dl,10
    mov ah,02h
    int 10h
    mov dx,offset promptCourse
    mov ah,09h
    int 21h
    mov dx,offset courseBuffer
    mov ah,0Ah
    int 21h

    mov dh,6
    mov dl,10
    mov ah,02h
    int 10h
    mov dx,offset promptDate
    mov ah,09h
    int 21h
    mov dx,offset dateBuffer
    mov ah,0Ah
    int 21h
    mov ax,4C00h
    int 21h
main ENDP
END main