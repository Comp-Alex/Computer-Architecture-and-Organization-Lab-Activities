# Exer2

## Purpose
Displays personal-information fields as text lines using direct character output.

## Assembly form
- `.MODEL SMALL`, `.STACK 100h`, `.DATA`, and `.CODE` define the program layout.
- Each character is placed directly in `DL` using its hexadecimal ASCII value.
- DOS `INT 21h` with `AH=02h` prints the character in `DL`.
- Carriage return (`0Dh`) and line feed (`0Ah`) move to the next line.
- Output is written inline without data declarations or subroutine calls.
- DOS `AX=4C00h` terminates the program.

## Assemble and run
```text
tasm Exer2.asm
tlink Exer2.obj
Exer2.exe
```
Run from this folder in DOSBox, TASM, or a compatible DOS environment.