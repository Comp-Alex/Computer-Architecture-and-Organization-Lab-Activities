# Exer11

## Purpose
Displays resistor color-coding bands and their labels using BIOS video services.

## Assembly form
- `INT 10h`, `AH=02h` positions the cursor using `DH` for the row and `DL` for the column.
- `INT 10h`, `AH=09h` writes colored spaces for each resistor band and colored `R` labels.
- `AX=0003h` selects the standard text mode before drawing.
- DOS `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer11.asm
tlink Exer11.obj
Exer11.exe
```
