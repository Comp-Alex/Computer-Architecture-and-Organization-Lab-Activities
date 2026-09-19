# Exer13

## Purpose
Displays standard-style colored television bars using BIOS video services.

## Assembly form
- BIOS `INT 10h`, `AH=02h` positions the cursor.
- BIOS `INT 10h`, `AH=09h` writes repeated characters with a color attribute.
- Five bars use separate colors and fixed screen coordinates.
- DOS `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer13.asm
tlink Exer13.obj
Exer13.exe
```
