.MODEL SMALL
.STACK 100h
.DATA
titleText db 0Dh,0Ah,50h,41h,50h,45h,52h,20h,52h,4Fh,43h,4Bh,20h,53h,43h,49h,53h,53h,4Fh,52h,53h,0Dh,0Ah,24h
playerOne db 0Dh,0Ah,50h,6Ch,61h,79h,65h,72h,20h,31h,20h,28h,50h,2Fh,52h,2Fh,53h,2Ch,20h,51h,20h,71h,75h,69h,74h,73h,29h,3Ah,20h,24h
playerTwo db 0Dh,0Ah,50h,6Ch,61h,79h,65h,72h,20h,32h,20h,28h,50h,2Fh,52h,2Fh,53h,29h,3Ah,20h,24h
resultText db 0Dh,0Ah,52h,65h,73h,75h,6Ch,74h,3Ah,20h,24h
tieText db 54h,69h,65h,24h
oneText db 50h,6Ch,61h,79h,65h,72h,20h,31h,20h,77h,69h,6Eh,73h,24h
twoText db 50h,6Ch,61h,79h,65h,72h,20h,32h,20h,77h,69h,6Eh,73h,24h
invalidText db 49h,6Eh,76h,61h,6Ch,69h,64h,20h,69h,6Eh,70h,75h,74h,24h
.CODE
main PROC
    mov ax,@data
    mov ds,ax
again:
    mov dx,offset titleText
    mov ah,09h
    int 21h
    mov dx,offset playerOne
    mov ah,09h
    int 21h
    mov ah,07h
    int 21h
    and al,0DFh
    cmp al,51h
    je quit
    mov bl,al
    mov dx,offset playerTwo
    mov ah,09h
    int 21h
    mov ah,07h
    int 21h
    and al,0DFh
    mov bh,al
    mov dx,offset resultText
    mov ah,09h
    int 21h
    cmp bl,50h
    je one_paper
    cmp bl,52h
    je one_rock
    cmp bl,53h
    je one_scissors
    mov dx,offset invalidText
    jmp show_result
one_paper:
    cmp bh,50h
    je tie
    cmp bh,53h
    je player_two
    jmp player_one
one_rock:
    cmp bh,52h
    je tie
    cmp bh,50h
    je player_two
    jmp player_one
one_scissors:
    cmp bh,53h
    je tie
    cmp bh,52h
    je player_two
    jmp player_one
tie:
    mov dx,offset tieText
    jmp show_result
player_one:
    mov dx,offset oneText
    jmp show_result
player_two:
    mov dx,offset twoText
show_result:
    mov ah,09h
    int 21h
    jmp again
quit:
    mov ax,4C00h
    int 21h
main ENDP
END main