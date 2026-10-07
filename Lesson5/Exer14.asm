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
titleText       db 'MOBILE PHONE DISPLAY'
titleTextLen    EQU $ - titleText
topFrame        db '+--------------------+'
topFrameLen     EQU $ - topFrame
speaker         db '|        [====]      |'
speakerLen      EQU $ - speaker
blankFrame      db '|                    |'
blankFrameLen   EQU $ - blankFrame
screenTop       db '|  +--------------+  |'
screenTopLen    EQU $ - screenTop
screenBrand     db '|  | MOBILE UI    |  |'
screenBrandLen  EQU $ - screenBrand
screenSignal    db '|  | SIGNAL: FULL |  |'
screenSignalLen EQU $ - screenSignal
screenTime      db '|  | TIME 10:45 AM|  |'
screenTimeLen   EQU $ - screenTime
screenMessage   db '|  | NEW MESSAGE  |  |'
screenMessageLen EQU $ - screenMessage
screenSender    db '|  | FROM: ALEX   |  |'
screenSenderLen EQU $ - screenSender
screenBattery   db '|  | BATTERY: 100%|  |'
screenBatteryLen EQU $ - screenBattery
screenBottom    db '|  +--------------+  |'
screenBottomLen EQU $ - screenBottom
keypadRow1      db '|    [1] [2] [3]     |'
keypadRow1Len   EQU $ - keypadRow1
keypadRow2      db '|    [4] [5] [6]     |'
keypadRow2Len   EQU $ - keypadRow2
keypadRow3      db '|    [7] [8] [9]     |'
keypadRow3Len   EQU $ - keypadRow3
keypadRow4      db '|    [*] [0] [#]     |'
keypadRow4Len   EQU $ - keypadRow4
bottomFrame     db '+--------------------+'
bottomFrameLen  EQU $ - bottomFrame
captionText     db 'LCD: NEW MESSAGE FROM ALEX'
captionTextLen  EQU $ - captionText

.CODE
main PROC
    mov ax, 0003h
    int 10h

    mov ax, @data
    mov ds, ax
    mov es, ax

    PRINT_AT 1, 30, titleText, titleTextLen, 0Bh

    PRINT_AT 3, 29, topFrame, topFrameLen, 1Fh
    PRINT_AT 4, 29, speaker, speakerLen, 1Fh
    PRINT_AT 5, 29, blankFrame, blankFrameLen, 1Fh

    PRINT_AT 6, 29, screenTop, screenTopLen, 1Fh
    PRINT_AT 7, 29, screenBrand, screenBrandLen, 0Ah
    PRINT_AT 8, 29, screenSignal, screenSignalLen, 0Ah
    PRINT_AT 9, 29, screenTime, screenTimeLen, 0Ah
    PRINT_AT 10, 29, screenMessage, screenMessageLen, 0Ah
    PRINT_AT 11, 29, screenSender, screenSenderLen, 0Ah
    PRINT_AT 12, 29, screenBattery, screenBatteryLen, 0Ah
    PRINT_AT 13, 29, blankFrame, blankFrameLen, 1Fh
    PRINT_AT 14, 29, screenBottom, screenBottomLen, 1Fh
    PRINT_AT 15, 29, blankFrame, blankFrameLen, 1Fh

    PRINT_AT 16, 29, keypadRow1, keypadRow1Len, 17h
    PRINT_AT 17, 29, keypadRow2, keypadRow2Len, 17h
    PRINT_AT 18, 29, keypadRow3, keypadRow3Len, 17h
    PRINT_AT 19, 29, keypadRow4, keypadRow4Len, 17h
    PRINT_AT 20, 29, bottomFrame, bottomFrameLen, 1Fh

    PRINT_AT 22, 27, captionText, captionTextLen, 0Fh

    mov ax, 4C00h
    int 21h
main ENDP

END main
