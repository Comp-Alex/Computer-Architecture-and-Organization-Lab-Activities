# Exer14

## Purpose
Draws a small mobile-phone shape with colored screen details.

## Assembly form
- BIOS `INT 10h`, `AH=02h` selects each line's row and column.
- BIOS `INT 10h`, `AH=09h` writes each colored character.
- The individual elements form the phone outline and its screen marking.
- DOS `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer14.asm
tlink Exer14.obj
Exer14.exe
```