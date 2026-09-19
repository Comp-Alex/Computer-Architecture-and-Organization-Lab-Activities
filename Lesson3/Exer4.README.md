# Exer4

## Purpose
Generates and prints the pairs `AaBbCc...Zz`.

## Assembly form
- `BL` starts at `A` and `BH` starts at `a`.
- `CX=26` controls the loop with `LOOP`.
- Each iteration prints the uppercase character, then the lowercase character, and increments both registers.
- Characters are printed directly with DOS `INT 21h`, `AH=02h`, using `DL`.
- `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer4.asm
tlink Exer4.obj
Exer4.exe
```