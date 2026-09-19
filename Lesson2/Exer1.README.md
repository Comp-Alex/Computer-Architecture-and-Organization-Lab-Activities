# Exer1

## Purpose
Prints `Alexander John` one character at a time, followed by a new line.

## Assembly form
- `.MODEL SMALL` selects the small memory model.
- `.STACK 100h` reserves stack space.
- `.DATA` is empty in this exercise.
- `main` initializes `DS`, prints each character, then exits.
- Each character is passed in `DL` and printed directly with DOS `INT 21h`, `AH=02h`.
- DOS `INT 21h` with `AX=4C00h` ends the program.

## Assemble and run
```text
tasm Exer1.asm
tlink Exer1.obj
Exer1.exe
```
Run the commands from this folder in DOSBox, TASM, or a compatible DOS environment.