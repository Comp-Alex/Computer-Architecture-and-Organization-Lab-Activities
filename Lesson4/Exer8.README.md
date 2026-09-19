# Exer8

## Purpose
Displays a multi-line message with DOS string output using hexadecimal ASCII byte values.

## Assembly form
- The message is stored as a `$`-terminated string with hexadecimal character bytes and line breaks.
- DOS `INT 21h`, `AH=09h` displays the complete string.
- DOS `INT 21h`, `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer8.asm
tlink Exer8.obj
Exer8.exe
```
Use a DOS-compatible environment that supports BIOS video interrupts.