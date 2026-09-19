# Exer16

## Purpose
Displays positioned prompts for a name, course/section, and date using screen and keyboard interrupt services.

## Assembly form
- BIOS `INT 10h`, `AH=06h` clears the text screen and `AH=02h` positions each prompt.
- DOS `INT 21h`, `AH=09h` displays each prompt.
- DOS `INT 21h`, `AH=0Ah` reads each line into its own buffer.
- Each input buffer begins with its maximum length, followed by the entered length and storage for the characters.
- `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer16.asm
tlink Exer16.obj
Exer16.exe
```