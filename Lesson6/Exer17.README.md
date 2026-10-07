# Exer17

## Purpose
Runs a two-player paper-rock-scissors game with hidden choices and a replay option.

## Interrupt functions
- BIOS `INT 10h`, `AX=0003h` selects 80-column text mode.
- BIOS `INT 10h`, `AH=06h` clears the screen between rounds.
- BIOS `INT 10h`, `AH=02h` positions the title.
- DOS `INT 21h`, `AH=09h` displays `$`-terminated prompts and results.
- DOS `INT 21h`, `AH=07h` reads each choice without echoing it.
- Lowercase choices are converted to uppercase before validation.
- DOS `INT 21h`, `AX=4C00h` exits.

## How to play
- Each player enters `P`, `R`, or `S`. The choice is hidden as it is typed.
- Invalid choices are rejected and that player's input is requested again.
- The game prints the winner and the reason, or reports a tie.
- Enter `Y` to start another round, or `N`/`Q` to quit.

## Result rules

| Player 1 | Player 2 | Result |
| --- | --- | --- |
| P | P | Tie |
| P | R | Player 1 wins — Paper covers Rock |
| P | S | Player 2 wins — Scissors cuts Paper |
| R | P | Player 2 wins — Paper covers Rock |
| R | R | Tie |
| R | S | Player 1 wins — Rock crushes Scissors |
| S | P | Player 1 wins — Scissors cuts Paper |
| S | R | Player 2 wins — Rock crushes Scissors |
| S | S | Tie |

## Assemble and run
```text
tasm Exer17.asm
tlink Exer17.obj
Exer17.exe
```
