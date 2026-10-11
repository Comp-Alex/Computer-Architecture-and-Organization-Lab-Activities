# Lesson 7 Sample Problems

Based on the lab manual topic: parallel-port interfacing and starter sample applications.

## Problem 1: Port status check
Write a short explanation of how a parallel port can be read and written using I/O instructions.

### Requirements
- Define what a port is in the context of PC hardware.
- Explain how data is sent to the port.
- Describe a simple status check operation.

## Problem 2: Send a byte to the port
Create a sample program that sends a byte value to a parallel port register.

### Requirements
- Use an output instruction to write the value.
- Choose a simple byte such as `01010101b`.
- Explain what the output represents.

## Problem 3: Port toggling pattern
Design a program that turns a device on and off using repeated writes to the parallel port.

### Requirements
- Use a loop.
- Send a sequence of values such as `00h`, `FFh`, and `0Fh`.
- Explain the purpose of a simple on/off toggle in hardware control.

## Challenge: Hardware control application
Create a small sample design for a controlled output interface that can be used to light LEDs or trigger a simple device through the parallel port.

### Deliverable
A brief design note with the port address, output pattern, and expected behavior.
