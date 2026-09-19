# Exer17

## Purpose
Runs a two-player paper-rock-scissors game.

## Assembly form
- The program directly uses DOS `INT 21h`, `AH=09h` for `$`-terminated messages.
- `INT 21h`, `AH=07h` reads a single key without echoing it.
- Lowercase input is converted to uppercase with `AND AL,0DFh`.
- `Q` quits the game; the game compares both players' choices to determine the result.
- `AX=4C00h` exits.

## Assemble and run
```text
tasm Exer17.asm
tlink Exer17.obj
Exer17.exe
```
Enter the supported paper, rock, or scissors keys when prompted.