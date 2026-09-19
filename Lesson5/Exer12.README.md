# Exer12

## Purpose
Displays a custom colored logo using BIOS cursor positioning and character output.

## Assembly form
- The cursor is positioned with BIOS `INT 10h`, `AH=02h`.
- BIOS `INT 10h`, `AH=09h` writes the colored logo characters.
- The logo uses different coordinates and color attributes for each character.
- DOS `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer12.asm
tlink Exer12.obj
Exer12.exe
```