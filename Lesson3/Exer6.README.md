# Exer6

## Purpose
Prints pairs such as `aZ`, `bY`, and `cX`, with one pair per line.

## Assembly form
- `BL` starts at lowercase `a` and increments.
- `BH` starts at uppercase `Z` and decrements.
- `CX=26` controls the loop.
- Each pair is followed by a carriage return and line feed using DOS `INT 21h`, `AH=02h`.
- `AX=4C00h` exits to DOS.

## Assemble and run
```text
tasm Exer6.asm
tlink Exer6.obj
Exer6.exe
```