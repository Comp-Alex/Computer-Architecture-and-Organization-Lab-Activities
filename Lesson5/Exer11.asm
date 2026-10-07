.MODEL SMALL
.STACK 100h

PRINT_AT MACRO row, column, text, textLength, textColor
    mov dh, row
    mov dl, column
    mov bp, OFFSET text
    mov cx, textLength
    mov bl, textColor
    mov bh, 0
    mov ax, 1301h
    int 10h
ENDM

.DATA
titleText       db 'RESISTOR COLOR CODE (4-BAND)'
titleTextLen    EQU $ - titleText
subtitleText    db 'Digit, multiplier, and standard tolerance values'
subtitleTextLen EQU $ - subtitleText
colorHeading    db 'COLOR'
colorHeadingLen EQU $ - colorHeading
digitHeading    db 'DIGIT'
digitHeadingLen EQU $ - digitHeading
multHeading     db 'MULTIPLIER'
multHeadingLen  EQU $ - multHeading
toleranceHeading    db 'TOLERANCE'
toleranceHeadingLen EQU $ - toleranceHeading

blackName       db 'Black'
blackNameLen    EQU $ - blackName
blackValues     db '0           x1                  --'
blackValuesLen  EQU $ - blackValues
brownName       db 'Brown'
brownNameLen    EQU $ - brownName
brownValues     db '1           x10                 1%'
brownValuesLen  EQU $ - brownValues
redName         db 'Red'
redNameLen      EQU $ - redName
redValues       db '2           x100                2%'
redValuesLen    EQU $ - redValues
orangeName      db 'Orange'
orangeNameLen   EQU $ - orangeName
orangeValues    db '3           x1k                 --'
orangeValuesLen EQU $ - orangeValues
yellowName      db 'Yellow'
yellowNameLen   EQU $ - yellowName
yellowValues    db '4           x10k                --'
yellowValuesLen EQU $ - yellowValues
greenName       db 'Green'
greenNameLen    EQU $ - greenName
greenValues     db '5           x100k               0.5%'
greenValuesLen  EQU $ - greenValues
blueName        db 'Blue'
blueNameLen     EQU $ - blueName
blueValues      db '6           x1M                 0.25%'
blueValuesLen   EQU $ - blueValues
violetName      db 'Violet'
violetNameLen   EQU $ - violetName
violetValues    db '7           x10M                0.1%'
violetValuesLen EQU $ - violetValues
grayName        db 'Gray'
grayNameLen     EQU $ - grayName
grayValues      db '8           x100M               0.05%'
grayValuesLen   EQU $ - grayValues
whiteName       db 'White'
whiteNameLen    EQU $ - whiteName
whiteValues     db '9           x1G                 --'
whiteValuesLen  EQU $ - whiteValues
goldName        db 'Gold'
goldNameLen     EQU $ - goldName
goldValues      db '--          x0.1                5%'
goldValuesLen   EQU $ - goldValues
silverName      db 'Silver'
silverNameLen   EQU $ - silverName
silverValues    db '--          x0.01               10%'
silverValuesLen EQU $ - silverValues
noBandName      db 'No band'
noBandNameLen   EQU $ - noBandName
noBandValues    db '--          --                  20%'
noBandValuesLen EQU $ - noBandValues
noteText        db 'DOS text colors approximate brown and gold.'
noteTextLen     EQU $ - noteText

.CODE
main PROC
    mov ax, 0003h
    int 10h

    mov ax, @data
    mov ds, ax
    mov es, ax

    PRINT_AT 2, 25, titleText, titleTextLen, 0Bh
    PRINT_AT 3, 16, subtitleText, subtitleTextLen, 0Fh

    PRINT_AT 5, 4, colorHeading, colorHeadingLen, 0Eh
    PRINT_AT 5, 22, digitHeading, digitHeadingLen, 0Eh
    PRINT_AT 5, 34, multHeading, multHeadingLen, 0Eh
    PRINT_AT 5, 54, toleranceHeading, toleranceHeadingLen, 0Eh

    PRINT_AT 6, 4, blackName, blackNameLen, 08h
    PRINT_AT 6, 22, blackValues, blackValuesLen, 0Fh
    PRINT_AT 7, 4, brownName, brownNameLen, 06h
    PRINT_AT 7, 22, brownValues, brownValuesLen, 0Fh
    PRINT_AT 8, 4, redName, redNameLen, 0Ch
    PRINT_AT 8, 22, redValues, redValuesLen, 0Fh
    PRINT_AT 9, 4, orangeName, orangeNameLen, 06h
    PRINT_AT 9, 22, orangeValues, orangeValuesLen, 0Fh
    PRINT_AT 10, 4, yellowName, yellowNameLen, 0Eh
    PRINT_AT 10, 22, yellowValues, yellowValuesLen, 0Fh
    PRINT_AT 11, 4, greenName, greenNameLen, 02h
    PRINT_AT 11, 22, greenValues, greenValuesLen, 0Fh
    PRINT_AT 12, 4, blueName, blueNameLen, 01h
    PRINT_AT 12, 22, blueValues, blueValuesLen, 0Fh
    PRINT_AT 13, 4, violetName, violetNameLen, 05h
    PRINT_AT 13, 22, violetValues, violetValuesLen, 0Fh
    PRINT_AT 14, 4, grayName, grayNameLen, 07h
    PRINT_AT 14, 22, grayValues, grayValuesLen, 0Fh
    PRINT_AT 15, 4, whiteName, whiteNameLen, 0Fh
    PRINT_AT 15, 22, whiteValues, whiteValuesLen, 0Fh
    PRINT_AT 16, 4, goldName, goldNameLen, 0Eh
    PRINT_AT 16, 22, goldValues, goldValuesLen, 0Fh
    PRINT_AT 17, 4, silverName, silverNameLen, 07h
    PRINT_AT 17, 22, silverValues, silverValuesLen, 0Fh
    PRINT_AT 18, 4, noBandName, noBandNameLen, 07h
    PRINT_AT 18, 22, noBandValues, noBandValuesLen, 0Fh

    PRINT_AT 20, 4, noteText, noteTextLen, 07h

    mov ax, 4C00h
    int 21h
main ENDP

END main
