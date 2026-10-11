# Lesson 2 Sample Problems

Based on the lab manual topic: basic DOS character output using `INT 21h`.

## Problem 1: Print your name
Write an assembly program that displays your name on the screen using DOS output services.

### Requirements
- Use a message such as `HELLO, CLASS!` or your own student name.
- Display the text as a single line.
- End the program cleanly with a DOS termination interrupt.

## Problem 2: Display the alphabet
Write a program that prints the uppercase English alphabet from `A` to `Z`.

### Requirements
- Use a loop structure.
- Print each character individually.
- Stop after the last letter `Z`.

## Problem 3: Print a pattern
Create a program that displays the following pattern using characters and repeated loops:

```text
*
**
***
****
*****
```

### Requirements
- Use a loop counter.
- Print one row at a time.
- Keep the output readable in DOS output mode.

## Challenge: Mixed output
Write a program that prints a number, a letter, and a symbol in different lines using repeated `INT 21h` output calls.
