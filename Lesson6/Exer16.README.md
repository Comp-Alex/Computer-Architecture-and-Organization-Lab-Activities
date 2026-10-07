# Exer16

## Purpose
Prompts for student details, then displays them in a positioned record form for the University of Batangas Lipa City.

## Interrupt functions
- BIOS `INT 10h`, `AH=00h` selects 80-column text mode.
- BIOS `INT 10h`, `AH=06h` clears the screen with a blue background and white foreground.
- BIOS `INT 10h`, `AH=02h` positions the cursor for form labels and input.
- DOS `INT 21h`, `AH=09h` displays `$`-terminated labels and borders.
- DOS `INT 21h`, `AH=0Ah` reads each line into its own buffered input area.
- DOS `INT 21h`, `AH=01h` waits for a key before exiting.
- DOS `INT 21h`, `AX=4C00h` exits.

## Expected layout and coordinates
Coordinates are zero-based (row, column). The form border spans columns 11 through 68. The school, address, and programmer name are prefilled; the student fields are entered interactively.

```text
Row 2, Col 11: +----------------------------------------------------------+
Rows 3-19:     |                                                        |
Row 4, Col 24: |             University of Batangas Lipa City            |
Row 5, Col 26: |               Gov. Feliciano Leviste Road,              |
Row 6, Col 30: |                   Lipa City, Philippines                 |
Row 7, Col 24: |             COMPUTER ENGINEERING DEPARTMENT            |
Row 8, Col 34: |                       Student Record                    |
Row 10, Col 20:|         Student Name     : <user input>                 |
Row 11, Col 20:|         Student Number   : <user input>                 |
Row 12, Col 20:|         Year Level       : <user input>                 |
Row 13, Col 20:|         Gender           : <user input>                 |
Row 14, Col 20:|         Birthdate        : <user input>                 |
Row 15, Col 20:|         Age              : <user input>                 |
Row 17, Col 22:|           Programmed by: Alexander John Balagso          |
Row 20, Col 11: +----------------------------------------------------------+
Row 22, Col 30: Press any key to exit.
```

The program prompts directly inside the form for the student fields. Each input accepts up to 27 characters so it stays inside the border. Enter the birthdate and age as text; the program does not calculate age.

## Assemble and run
```text
tasm Exer16.asm
tlink Exer16.obj
Exer16.exe
```
