.MODEL SMALL
.STACK 100h

.DATA
titleText       db 'PAPER, ROCK, SCISSORS GAME',0Dh,0Ah,0Dh,0Ah,'$'
playerOnePrompt db 'Player 1: Enter P, R, or S (hidden): $'
playerTwoPrompt db 0Dh,0Ah,'Player 2: Enter P, R, or S (hidden): $'
invalidChoice   db 0Dh,0Ah,'Invalid choice. Enter P, R, or S: $'
playAgainPrompt db 0Dh,0Ah,'Play again? (Y/N or Q to quit): $'
invalidContinue db 0Dh,0Ah,'Enter Y to play again or N/Q to quit: $'
playerOneWins   db 0Dh,0Ah,'Player 1 wins!$'
playerTwoWins   db 0Dh,0Ah,'Player 2 wins!$'
tieText         db 0Dh,0Ah,'It is a tie!$'
paperRockText   db 0Dh,0Ah,'Paper covers Rock!$'
scissorsPaperText db 0Dh,0Ah,'Scissors cuts Paper!$'
rockScissorsText db 0Dh,0Ah,'Rock crushes Scissors!$'
playerOneChoice db ?
playerTwoChoice db ?

.CODE
main PROC
    mov ax, @data
    mov ds, ax

    mov ax, 0003h
    int 10h

newRound:
    mov ax, 0600h
    mov bh, 07h
    mov cx, 0000h
    mov dx, 184Fh
    int 10h

    mov ah, 02h
    mov bh, 0
    mov dh, 2
    mov dl, 27
    int 10h

    mov dx, OFFSET titleText
    mov ah, 09h
    int 21h

getPlayerOne:
    mov dx, OFFSET playerOnePrompt
    mov ah, 09h
    int 21h
    mov ah, 07h
    int 21h
    and al, 0DFh
    cmp al, 'P'
    je savePlayerOne
    cmp al, 'R'
    je savePlayerOne
    cmp al, 'S'
    je savePlayerOne
    mov dx, OFFSET invalidChoice
    mov ah, 09h
    int 21h
    jmp getPlayerOne

savePlayerOne:
    mov playerOneChoice, al

getPlayerTwo:
    mov dx, OFFSET playerTwoPrompt
    mov ah, 09h
    int 21h
    mov ah, 07h
    int 21h
    and al, 0DFh
    cmp al, 'P'
    je savePlayerTwo
    cmp al, 'R'
    je savePlayerTwo
    cmp al, 'S'
    je savePlayerTwo
    mov dx, OFFSET invalidChoice
    mov ah, 09h
    int 21h
    jmp getPlayerTwo

savePlayerTwo:
    mov playerTwoChoice, al

    mov al, playerOneChoice
    cmp al, 'P'
    je playerOnePaper
    cmp al, 'R'
    je playerOneRock
    jmp playerOneScissors

playerOnePaper:
    mov al, playerTwoChoice
    cmp al, 'P'
    je showTie
    cmp al, 'R'
    je playerOnePaperWins
    jmp playerTwoScissorsWins

playerOneRock:
    mov al, playerTwoChoice
    cmp al, 'P'
    je playerTwoPaperWins
    cmp al, 'R'
    je showTie
    jmp playerOneRockWins

playerOneScissors:
    mov al, playerTwoChoice
    cmp al, 'P'
    je playerOneScissorsWins
    cmp al, 'R'
    je playerTwoRockWins
    jmp showTie

playerOnePaperWins:
    mov dx, OFFSET playerOneWins
    call PrintResult
    mov dx, OFFSET paperRockText
    jmp showReason

playerTwoPaperWins:
    mov dx, OFFSET playerTwoWins
    call PrintResult
    mov dx, OFFSET paperRockText
    jmp showReason

playerOneScissorsWins:
    mov dx, OFFSET playerOneWins
    call PrintResult
    mov dx, OFFSET scissorsPaperText
    jmp showReason

playerTwoScissorsWins:
    mov dx, OFFSET playerTwoWins
    call PrintResult
    mov dx, OFFSET scissorsPaperText
    jmp showReason

playerOneRockWins:
    mov dx, OFFSET playerOneWins
    call PrintResult
    mov dx, OFFSET rockScissorsText
    jmp showReason

playerTwoRockWins:
    mov dx, OFFSET playerTwoWins
    call PrintResult
    mov dx, OFFSET rockScissorsText

showReason:
    mov ah, 09h
    int 21h
    jmp askReplay

showTie:
    mov dx, OFFSET tieText
    mov ah, 09h
    int 21h

askReplay:
    mov dx, OFFSET playAgainPrompt
    mov ah, 09h
    int 21h
    mov ah, 07h
    int 21h
    and al, 0DFh
    cmp al, 'Y'
    jne checkNo
    jmp newRound
checkNo:
    cmp al, 'N'
    je quit
    cmp al, 'Q'
    je quit
    mov dx, OFFSET invalidContinue
    mov ah, 09h
    int 21h
    mov ah, 07h
    int 21h
    and al, 0DFh
    cmp al, 'Y'
    jne checkNoAfterError
    jmp newRound
checkNoAfterError:
    cmp al, 'N'
    je quit
    cmp al, 'Q'
    je quit
    jmp askReplay

quit:
    mov ax, 4C00h
    int 21h

main ENDP

PrintResult PROC
    mov ah, 09h
    int 21h
    ret
PrintResult ENDP

END main
