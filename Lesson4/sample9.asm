.model small
.stack
.data
p1  DB '_+88________ROCK_N_ROLL!!!_______ ',13,10,'$'
p2  DB '_+880_____________________________',13,10,'$'
p3  DB '_++88___________BABY!!____________',13,10,'$'
p4  DB '_++88_____________________________',13,10,'$'
p5  DB '__+880_________________________++_',13,10,'$'
p6  DB '__+888________________________+88_',13,10,'$'
p7  DB '__++880______________________+88__',13,10,'$'
p8  DB '__++888_____+++88__________+++8__',13,10,'$'
p9  DB '__++8888__+++8880++88____+++88___',13,10,'$'
p10 DB '__+++8888+++8880++8888__++888____',13,10,'$'
p11 DB '___++888++8888+++888888++888_____',13,10,'$'
p12 DB '___++88++8888++8888888++888______',13,10,'$'
p13 DB '___++++++888888888888888888______',13,10,'$'
p14 DB '____++++++88888888888888888______',13,10,'$'
p15 DB '_______+++++++088888888888_______',13,10,'$'
p16 DB '_______+++++++088888888888_______',13,10,'$'
p17 DB '________+++++++8888888888________',13,10,'$'
p18 DB '________+++++++0088888888________',13,10,'$'
p19 DB '________++++++0088888888_________',13,10,'$'
p20 DB '________+++++0008888888__________',13,10,'$'
p21 DB '________############_____________',13,10,'$'
p22 DB '________############_____________',13,10,'$'
p23 DB '________############_____________',13,10,'$'
.code
start:
    mov ax,@data
    mov ds,ax
    mov ah,09h
    mov dx,offset p1
    int 21h
    mov ah,09h
    mov dx,offset p2
    int 21h
    mov ah,09h
    mov dx,offset p3
    int 21h
    mov ah,09h
    mov dx,offset p4
    int 21h
    mov ah,09h
    mov dx,offset p5
    int 21h
    mov ah,09h
    mov dx,offset p6
    int 21h
    mov ah,09h
    mov dx,offset p7
    int 21h
    mov ah,09h
    mov dx,offset p8
    int 21h
    mov ah,09h
    mov dx,offset p9
    int 21h
    mov ah,09h
    mov dx,offset p10
    int 21h
    mov ah,09h
    mov dx,offset p11
    int 21h
    mov ah,09h
    mov dx,offset p12
    int 21h
    mov ah,09h
    mov dx,offset p13
    int 21h
    mov ah,09h
    mov dx,offset p14
    int 21h
    mov ah,09h
    mov dx,offset p15
    int 21h
    mov ah,09h
    mov dx,offset p16
    int 21h
    mov ah,09h
    mov dx,offset p17
    int 21h
    mov ah,09h
    mov dx,offset p18
    int 21h
    mov ah,09h
    mov dx,offset p19
    int 21h
    mov ah,09h
    mov dx,offset p20
    int 21h
    mov ah,09h
    mov dx,offset p21
    int 21h
    mov ah,09h
    mov dx,offset p22
    int 21h
    mov ah,09h
    mov dx,offset p23
    int 21h
    mov ah,4ch
    int 21h
end start
