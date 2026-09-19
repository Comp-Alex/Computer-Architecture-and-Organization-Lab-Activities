# Exer10

## Purpose
Displays a list of favorite television shows using DOS string output.

## Assembly form
- The list is stored as a `$`-terminated string with one show per line.
- DOS `INT 21h`, `AH=09h` displays the complete list.
- DOS `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer10.asm
tlink Exer10.obj
Exer10.exe
```
