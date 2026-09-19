# Exer15

## Purpose
Draws an eight-by-eight checkerboard with alternating colored squares.

## Assembly form
- BIOS `INT 10h`, `AH=02h` positions the cursor.
- BIOS `INT 10h`, `AH=09h` writes repeated colored blocks.
- Nested row and square loops alternate the color attribute across the board.
- DOS `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer15.asm
tlink Exer15.obj
Exer15.exe
```
