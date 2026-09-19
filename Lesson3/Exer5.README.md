# Exer5

## Purpose
Generates alternating pairs beginning with `zA`, then `yB`, through `aZ`.

## Assembly form
- `BL` begins at lowercase `z` and decrements each loop.
- `BH` begins at uppercase `A` and increments each loop.
- `CX=26` repeats the pair-generation loop.
- Characters are printed directly through DOS `INT 21h`, `AH=02h`.
- `AX=4C00h` terminates the program.

## Assemble and run
```text
tasm Exer5.asm
tlink Exer5.obj
Exer5.exe
```