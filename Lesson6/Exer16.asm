.MODEL SMALL
.STACK 100h

PRINT_AT MACRO row, column, text
    mov ah, 02h
    mov bh, 0
    mov dh, row
    mov dl, column
    int 10h
    mov dx, OFFSET text
    mov ah, 09h
    int 21h
ENDM

INPUT_AT MACRO row, column, inputBuffer
    mov ah, 02h
    mov bh, 0
    mov dh, row
    mov dl, column
    int 10h
    mov dx, OFFSET inputBuffer
    mov ah, 0Ah
    int 21h
ENDM

.DATA
topBorder       db '+',56 dup('-'),'+','$'
bottomBorder    db '+',56 dup('-'),'+','$'
universityText  db 'University of Batangas Lipa City$'
streetText      db 'Gov. Feliciano Leviste Road,$'
cityText        db 'Lipa City, Philippines$'
departmentText  db 'COMPUTER ENGINEERING DEPARTMENT$'
recordTitle     db 'Student Record$'
studentNameLabel    db 'Student Name     : $'
studentNumberLabel  db 'Student Number   : $'
yearLevelLabel      db 'Year Level       : $'
genderLabel         db 'Gender           : $'
birthdateLabel      db 'Birthdate        : $'
ageLabel            db 'Age              : $'
programmerText      db 'Programmed by: Alexander John Balagso$'
exitPrompt          db 'Press any key to exit.$'
screenRow           db 3

studentNameBuffer   db 28,0,28 dup(0)
studentNumberBuffer db 28,0,28 dup(0)
yearLevelBuffer     db 28,0,28 dup(0)
genderBuffer        db 28,0,28 dup(0)
birthdateBuffer     db 28,0,28 dup(0)
ageBuffer           db 28,0,28 dup(0)

.CODE
main PROC
    mov ax, 0003h
    int 10h

    mov ax, @data
    mov ds, ax

    mov ax, 0600h
    mov bh, 1Fh
    mov cx, 0000h
    mov dx, 184Fh
    int 10h

    PRINT_AT 2, 11, topBorder

    mov byte ptr screenRow, 3
DrawSides:
    mov ah, 02h
    mov bh, 0
    mov dh, screenRow
    mov dl, 11
    int 10h
    mov dl, '|'
    mov ah, 02h
    int 21h

    mov ah, 02h
    mov bh, 0
    mov dh, screenRow
    mov dl, 68
    int 10h
    mov dl, '|'
    mov ah, 02h
    int 21h

    inc byte ptr screenRow
    cmp byte ptr screenRow, 20
    jb DrawSides

    PRINT_AT 4, 24, universityText
    PRINT_AT 5, 26, streetText
    PRINT_AT 6, 30, cityText

    PRINT_AT 7, 24, departmentText
    PRINT_AT 8, 34, recordTitle

    PRINT_AT 10, 20, studentNameLabel
    INPUT_AT 10, 39, studentNameBuffer

    PRINT_AT 11, 20, studentNumberLabel
    INPUT_AT 11, 39, studentNumberBuffer

    PRINT_AT 12, 20, yearLevelLabel
    INPUT_AT 12, 39, yearLevelBuffer

    PRINT_AT 13, 20, genderLabel
    INPUT_AT 13, 39, genderBuffer

    PRINT_AT 14, 20, birthdateLabel
    INPUT_AT 14, 39, birthdateBuffer

    PRINT_AT 15, 20, ageLabel
    INPUT_AT 15, 39, ageBuffer

    PRINT_AT 17, 22, programmerText

    PRINT_AT 20, 11, bottomBorder
    PRINT_AT 22, 30, exitPrompt

    mov ah, 01h
    int 21h

    mov ax, 4C00h
    int 21h
main ENDP

END main
