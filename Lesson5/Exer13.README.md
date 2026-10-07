# Exer13

## Purpose
Displays the standard seven-bar television color sequence and a lower reference strip, followed by local network identification.

## BIOS services
- `INT 10h`, `AX=0003h` selects 80-column text mode.
- `INT 10h`, `AH=02h` positions the cursor; `DH` is the zero-based row and `DL` is the zero-based column.
- `INT 10h`, `AH=09h` prints repeated solid-block characters (`DBh`) with the selected color attribute.
- `INT 10h`, `AH=13h` prints the title and network identification strings at chosen coordinates.
- DOS `INT 21h`, `AX=4C00h` exits.

## Expected output and coordinates
Each main color bar is 10 columns wide and 10 rows high. The seven bars together are 70 columns wide. The reference strip is 10 columns wide and 3 rows high per segment.

```text
80 columns (0-79)
          Row 1, Col 31: 75% TV COLOR BARS

Col:      5         15        25        35        45        55        65
Rows 4-13: WHITE     YELLOW    CYAN      GREEN     MAGENTA   RED       BLUE
           |10x10|   |10x10|   |10x10|   |10x10|   |10x10|   |10x10|   |10x10|

Rows 14-16: BLUE      BLACK     MAGENTA   BLACK     CYAN      BLACK     GRAY
            |10x3|    |10x3|    |10x3|    |10x3|    |10x3|    |10x3|    |10x3|

          Row 19, Col 21: GMA NETWORK - COLOR BAR TEST PATTERN
```

The solid blocks use the closest standard DOS 16-color text attributes. Black reference segments blend into the screen background.

## Assemble and run
```text
tasm Exer13.asm
tlink Exer13.obj
Exer13.exe
```
