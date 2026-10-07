# Exer14

## Purpose
Draws a colored mobile phone and sample message on the LCD using BIOS video interrupt `10h`.

## BIOS services
- `INT 10h`, `AX=0003h` selects 80-column text mode.
- `INT 10h`, `AH=13h` prints a string at a screen coordinate using the selected color attribute.
- `DH` contains the zero-based row; `DL` contains the zero-based column.
- `DS:BP` points to the string, `CX` is its length, and `BL` contains its color attribute.
- DOS `INT 21h`, `AX=4C00h` exits.

## Expected output and coordinate graph
The 22-character-wide phone frame begins at row 3, column 29. The handset and screen use a blue border; the LCD uses green text on black, and the keypad uses light-gray text on a blue background.

```text
80 columns (0-79)

                  Row 1, Col 30: MOBILE PHONE DISPLAY

Row 3, Col 29:   +--------------------+
Row 4:           |        [====]      |   speaker
Row 5:           |                    |
Row 6:           |  +--------------+  |   LCD starts
Row 7:           |  | MOBILE UI    |  |
Row 8:           |  | SIGNAL: FULL |  |
Row 9:           |  | TIME 10:45 AM|  |
Row 10:          |  | NEW MESSAGE  |  |
Row 11:          |  | FROM: ALEX   |  |
Row 12:          |  | BATTERY: 100%|  |
Row 13:          |                    |
Row 14:          |  +--------------+  |   LCD ends
Row 15:          |                    |
Row 16:          |    [1] [2] [3]     |
Row 17:          |    [4] [5] [6]     |
Row 18:          |    [7] [8] [9]     |
Row 19:          |    [*] [0] [#]     |
Row 20:          +--------------------+

                  Row 22, Col 27: LCD: NEW MESSAGE FROM ALEX
```

## Assemble and run
```text
tasm Exer14.asm
tlink Exer14.obj
Exer14.exe
```
