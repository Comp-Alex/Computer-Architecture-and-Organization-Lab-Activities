# Computer Architecture and Organization Lab Activities

Assembly exercises organized by lesson.

| Lesson | Exercises | Documentation |
| --- | --- | --- |
| Lesson 1 | TASM editor environment; no numbered assembly exercise | [Lesson notes](Lesson1/README.md) |
| Lesson 2 | [Exer1.asm](Lesson2/Exer1.asm), [Exer2.asm](Lesson2/Exer2.asm), [Exer3.asm](Lesson2/Exer3.asm) | [Exer1 guide](Lesson2/Exer1.README.md), [Exer2 guide](Lesson2/Exer2.README.md), [Exer3 guide](Lesson2/Exer3.README.md) |
| Lesson 3 | [Exer4.asm](Lesson3/Exer4.asm), [Exer5.asm](Lesson3/Exer5.asm), [Exer6.asm](Lesson3/Exer6.asm), [Exer7.asm](Lesson3/Exer7.asm) | [Exer4 guide](Lesson3/Exer4.README.md), [Exer5 guide](Lesson3/Exer5.README.md), [Exer6 guide](Lesson3/Exer6.README.md), [Exer7 guide](Lesson3/Exer7.README.md) |
| Lesson 4 | [Exer8.asm](Lesson4/Exer8.asm), [Exer9.asm](Lesson4/Exer9.asm), [Exer10.asm](Lesson4/Exer10.asm) | [Exer8 guide](Lesson4/Exer8.README.md), [Exer9 guide](Lesson4/Exer9.README.md), [Exer10 guide](Lesson4/Exer10.README.md) |
| Lesson 5 | [Exer11.asm](Lesson5/Exer11.asm), [Exer12.asm](Lesson5/Exer12.asm), [Exer13.asm](Lesson5/Exer13.asm), [Exer14.asm](Lesson5/Exer14.asm), [Exer15.asm](Lesson5/Exer15.asm) | [Exer11 guide](Lesson5/Exer11.README.md), [Exer12 guide](Lesson5/Exer12.README.md), [Exer13 guide](Lesson5/Exer13.README.md), [Exer14 guide](Lesson5/Exer14.README.md), [Exer15 guide](Lesson5/Exer15.README.md) |
| Lesson 6 | [Exer16.asm](Lesson6/Exer16.asm), [Exer17.asm](Lesson6/Exer17.asm) | [Exer16 guide](Lesson6/Exer16.README.md), [Exer17 guide](Lesson6/Exer17.README.md) |
| Lesson 7 | Parallel-port interfacing; no numbered Skills Review exercise | [Lesson notes](Lesson7/README.md) |

The source uses DOS/TASM syntax and requires a DOS-compatible 16-bit assembler and linker. Exercises requesting personal details use neutral sample values.

## Workflow

1. Open the exercise guide next to its `.asm` file.
2. Assemble and link from the exercise folder:

```text
tasm ExerN.asm
tlink ExerN.obj
ExerN.exe
```

Run the commands in DOSBox or another DOS-compatible environment. Replace `ExerN` with the exercise number.