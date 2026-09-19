# Exer3

## Purpose
Prints a four-line bordered name box containing `Alexander John` and `Balagso`.

## Assembly form
- The border and name are printed character by character by loading hexadecimal ASCII values into `DL`.
- DOS `INT 21h`, `AH=02h` displays each character.
- `0Dh` (carriage return) and `0Ah` (line feed) separate the four lines.
- Each line uses an 18-character width so the `@` borders align.
- No `DB` data declarations or subroutine calls are used.
- `AX=4C00h` exits to DOS.

## Assemble and run
```text
tasm Exer3.asm
tlink Exer3.obj
Exer3.exe
```