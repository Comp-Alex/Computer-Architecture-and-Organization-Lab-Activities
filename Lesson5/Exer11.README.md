# Exer11

## Purpose
Displays the standard four-band resistor color-code digits, multipliers, and tolerance values with BIOS video interrupt `10h`.

## BIOS services
- `INT 10h`, `AH=00h` (`AX=0003h`) selects 80-column text mode.
- `INT 10h`, `AH=13h` writes a string at a specified row and column, with a text attribute.
- Row and column coordinates are zero-based. `DH` holds the row and `DL` holds the column.
- DOS `INT 21h`, `AX=4C00h` exits the program.

## Expected screen and coordinate map
```text
Row 2, Col 25:          RESISTOR COLOR CODE (4-BAND)
Row 3, Col 16:    Digit, multiplier, and standard tolerance values

Row 5: Col 4 COLOR      Col 22 DIGIT   Col 34 MULTIPLIER   Col 54 TOLERANCE
Row 6: Black            0              x1                  --
Row 7: Brown            1              x10                 1%
Row 8: Red              2              x100                2%
Row 9: Orange           3              x1k                 --
Row 10: Yellow          4              x10k                --
Row 11: Green           5              x100k               0.5%
Row 12: Blue            6              x1M                 0.25%
Row 13: Violet          7              x10M                0.1%
Row 14: Gray            8              x100M               0.05%
Row 15: White           9              x1G                 --
Row 16: Gold            --             x0.1                5%
Row 17: Silver          --             x0.01               10%
Row 18: No band         --             --                  20%

Row 20, Col 4: DOS text colors approximate brown and gold.
```

The color names are drawn with the closest available DOS text colors. `--` means the value does not apply to that band color.

## Assemble and run
```text
tasm Exer11.asm
tlink Exer11.obj
Exer11.exe
```
