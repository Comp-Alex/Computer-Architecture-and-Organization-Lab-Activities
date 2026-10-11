# Lesson 1 Sample Problem 1

## Objective
Display a simple message to confirm the TASM environment is ready.

## Program idea
- Store a text string in memory.
- Use DOS function `09h` to print the string.
- Exit cleanly using `INT 21h`.

## Example code
```asm
.DATA
msg db 'TASM EDITOR READY$'
```

## Run
```text
tasm SampleProb1.asm
tlink SampleProb1.obj
SampleProb1.exe
```