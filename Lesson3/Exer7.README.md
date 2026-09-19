# Exer7

## Purpose
Prints pairs such as `A z`, `B y`, and `C x` in a descending diagonal alignment.

## Assembly form
- `BL` starts at uppercase `A` and increments.
- `BH` starts at lowercase `z` and decrements.
- `CX=26` repeats the loop.
- Increasing indentation is printed before each pair, with a space between its two characters, followed by carriage return and line feed.
- DOS `INT 21h`, `AH=02h` outputs each space, character, and line break directly.
- `AX=4C00h` ends the program.

## Assemble and run
```text
tasm Exer7.asm
tlink Exer7.obj
Exer7.exe
```