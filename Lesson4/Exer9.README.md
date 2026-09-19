# Exer9

## Purpose
Displays a personalized calling card using DOS string output.

## Assembly form
- The card is stored as one `$`-terminated string with a border, name, role, and e-mail address.
- DOS `INT 21h`, `AH=09h` displays the complete card.
- DOS `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer9.asm
tlink Exer9.obj
Exer9.exe
```