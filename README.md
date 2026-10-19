<!-- Generated from dashboard/README_TEMPLATE.md by dashboard/dashboard.py. -->

# Computer Architecture and Organization Lab Activities

[![Daily dashboard update](https://github.com/Comp-Alex/Computer-Architecture-and-Organization-Lab-Activities/actions/workflows/dashboard.yml/badge.svg)](https://github.com/Comp-Alex/Computer-Architecture-and-Organization-Lab-Activities/actions/workflows/dashboard.yml)

[Open the interactive dashboard](dashboard/index.html)

> **Automatically analyzed purpose:** A hands-on computer architecture and organization laboratory. Its lessons teach 16-bit x86 assembly programming through DOS/TASM exercises, sample programs, and peripheral-I/O activities.

## Project overview

This repository contains **7 lesson folders**, **38 assembly source files**, **17 numbered exercises**, and **17 exercise guides**.

This portfolio dashboard is generated from the repository's actual folders, source files, and lesson documentation. Counts, topic coverage, progress highlights, and next steps are refreshed automatically; no hand-maintained inventory is required.

## At a glance

| Repository measure | Current total |
| --- | ---: |
| Files analyzed | 80 |
| Lesson folders | 7 |
| Numbered exercises | 17 |
| Assembly source files | 38 |
| Exercise guides | 17 |
| Exercise guide coverage | 100% |

## Repository contents

File counts are derived from the current working tree. The generated README and dashboard data are excluded to keep the statistics stable, along with version-control and cache directories.

| Type | Files |
| --- | ---: |
| Assembly (`.asm`) | 38 |
| Markdown (`.md`) | 34 |
| Python (`.py`) | 2 |
| CSS (`.css`) | 1 |
| HTML (`.html`) | 1 |
| JavaScript (`.js`) | 1 |
| JSON (`.json`) | 1 |
| SVG (`.svg`) | 1 |
| YAML (`.yml`) | 1 |

## Architecture topics

Topic-to-lesson relationships are inferred from the lesson notes and source files using the configurable rules in [`dashboard/config.json`](dashboard/config.json).

| Topic | Lesson coverage |
| --- | --- |
| **CPU architecture** — 8086 foundations, registers, control flow, and processor services. | [Lesson 1](Lesson1/README.md), [Lesson 2](Lesson2/README.md), [Lesson 3](Lesson3/README.md), [Lesson 4](Lesson4/README.md), [Lesson 5](Lesson5/README.md), [Lesson 6](Lesson6/README.md), [Lesson 7](Lesson7/README.md) |
| **Memory systems** — Segmented programs, data and stack areas, and input buffers. | [Lesson 1](Lesson1/README.md), [Lesson 2](Lesson2/README.md), [Lesson 3](Lesson3/README.md), [Lesson 4](Lesson4/README.md), [Lesson 5](Lesson5/README.md), [Lesson 6](Lesson6/README.md), [Lesson 7](Lesson7/README.md) |
| **Instruction sets** — Assembly instructions, DOS and BIOS interrupts, and peripheral I/O. | [Lesson 1](Lesson1/README.md), [Lesson 2](Lesson2/README.md), [Lesson 3](Lesson3/README.md), [Lesson 4](Lesson4/README.md), [Lesson 5](Lesson5/README.md), [Lesson 6](Lesson6/README.md), [Lesson 7](Lesson7/README.md) |
| **Lab activities** — Numbered exercises, sample programs, and lesson problem sets. | [Lesson 1](Lesson1/README.md), [Lesson 2](Lesson2/README.md), [Lesson 3](Lesson3/README.md), [Lesson 4](Lesson4/README.md), [Lesson 5](Lesson5/README.md), [Lesson 6](Lesson6/README.md), [Lesson 7](Lesson7/README.md) |

## Progress and achievements

- Organized **7 lessons** into a browsable, automatically maintained curriculum.
- Indexed **17 numbered exercises** with **17 guides** (100% guide coverage).
- Cataloged **21 sample programs** alongside the exercises.
- Tracked **38 assembly source files** across the repository.

## Learning roadmap

These next steps are automatically selected from repository evidence, such as undocumented exercises, sample programs without dedicated notes, and the presence or absence of an assembly execution harness.

- **NEXT · Validate programs in a DOS-compatible environment** — Add reproducible TASM/DOSBox smoke checks for the 38 assembly sources. The current material describes manual assembly and execution rather than an automated run harness.
- **NEXT · Add context for sample programs** — Add brief purpose and learning-outcome notes for 20 sample assembly programs without dedicated guides; lesson-level notes currently provide the shared context.
- **ONGOING · Keep the lesson index in sync** — The analyzer currently discovers 7 lesson folders (through Lesson 7). Add new lesson folders, source files, and guides to have them indexed automatically.

## Lesson and activity index

| Lesson | Focus | Exercises | Samples | Notes |
| --- | --- | --- | --- | --- |
| [Lesson 1](Lesson1/README.md) | The manual's Lesson 1 covers the TASM editor environment and has no numbered assembly exercise. | — | [Sample1](Lesson1/Sample1.asm), [SampleProb1](Lesson1/SampleProb1.asm), [SampleProb2](Lesson1/SampleProb2.asm), [SampleProblems](Lesson1/SampleProblems.asm), [test](Lesson1/test.asm) | [Lesson notes](Lesson1/README.md) |
| [Lesson 2](Lesson2/README.md) | Basic DOS character output using `INT 21h`. | [Exer1](Lesson2/Exer1.asm), [Exer2](Lesson2/Exer2.asm), [Exer3](Lesson2/Exer3.asm) | — | [Lesson notes](Lesson2/README.md); [Exer1 guide](Lesson2/Exer1.README.md), [Exer2 guide](Lesson2/Exer2.README.md), [Exer3 guide](Lesson2/Exer3.README.md) |
| [Lesson 3](Lesson3/README.md) | Character generation, loops, and formatted output. | [Exer4](Lesson3/Exer4.asm), [Exer5](Lesson3/Exer5.asm), [Exer6](Lesson3/Exer6.asm), [Exer7](Lesson3/Exer7.asm) | [sample1](Lesson3/sample1.asm), [sample2](Lesson3/sample2.asm), [sample3](Lesson3/sample3.asm), [sample4](Lesson3/sample4.asm), [sample5](Lesson3/sample5.asm), [sample6](Lesson3/sample6.asm) | [Lesson notes](Lesson3/README.md); [Exer4 guide](Lesson3/Exer4.README.md), [Exer5 guide](Lesson3/Exer5.README.md), [Exer6 guide](Lesson3/Exer6.README.md), [Exer7 guide](Lesson3/Exer7.README.md) |
| [Lesson 4](Lesson4/README.md) | DOS string output and multi-line text displays. | [Exer8](Lesson4/Exer8.asm), [Exer9](Lesson4/Exer9.asm), [Exer10](Lesson4/Exer10.asm) | [sample8](Lesson4/sample8.asm), [sample9](Lesson4/sample9.asm) | [Lesson notes](Lesson4/README.md); [Exer8 guide](Lesson4/Exer8.README.md), [Exer9 guide](Lesson4/Exer9.README.md), [Exer10 guide](Lesson4/Exer10.README.md) |
| [Lesson 5](Lesson5/README.md) | BIOS video services, cursor positioning, colors, and screen graphics. | [Exer11](Lesson5/Exer11.asm), [Exer12](Lesson5/Exer12.asm), [Exer13](Lesson5/Exer13.asm), [Exer14](Lesson5/Exer14.asm), [Exer15](Lesson5/Exer15.asm) | [sample10](Lesson5/sample10.asm), [sample11](Lesson5/sample11.asm) | [Lesson notes](Lesson5/README.md); [Exer11 guide](Lesson5/Exer11.README.md), [Exer12 guide](Lesson5/Exer12.README.md), [Exer13 guide](Lesson5/Exer13.README.md), [Exer14 guide](Lesson5/Exer14.README.md), [Exer15 guide](Lesson5/Exer15.README.md) |
| [Lesson 6](Lesson6/README.md) | Keyboard input, text buffers, and an interactive game. | [Exer16](Lesson6/Exer16.asm), [Exer17](Lesson6/Exer17.asm) | [sample12](Lesson6/sample12.asm), [sample13](Lesson6/sample13.asm), [sample14](Lesson6/sample14.asm), [sample15](Lesson6/sample15.asm) | [Lesson notes](Lesson6/README.md); [Exer16 guide](Lesson6/Exer16.README.md), [Exer17 guide](Lesson6/Exer17.README.md) |
| [Lesson 7](Lesson7/README.md) | The manual's Lesson 7 covers parallel-port interfacing and sample applications but has no numbered Skills Review exercise. | — | [Sample1](Lesson7/Sample1.asm), [SampleProblems](Lesson7/SampleProblems.asm) | [Lesson notes](Lesson7/README.md) |

## Run the labs

The assembly files use DOS/TASM conventions. Run these commands from the lesson folder in DOSBox or another compatible 16-bit DOS environment:

```text
tasm ExerN.asm
tlink ExerN.obj
ExerN.exe
```

Replace `ExerN` with the exercise filename. Some sample programs may have different input/output behavior; consult each lesson's notes before running.

## Dashboard automation

- The interactive dashboard is available in [`dashboard/`](dashboard/index.html).
- [`dashboard/dashboard.py`](dashboard/dashboard.py) scans the repository, infers its purpose, calculates statistics and progress, and renders this README and the dashboard catalog.
- [`dashboard/README_TEMPLATE.md`](dashboard/README_TEMPLATE.md) defines the generated portfolio README; edit the template or [`dashboard/config.json`](dashboard/config.json), not this generated file.
- [`.github/workflows/dashboard.yml`](.github/workflows/dashboard.yml) refreshes generated documentation daily and supports manual runs.
- The workflow stages and commits only `README.md` and `dashboard/data.json`, and only when their generated contents have changed.

Run the generator locally from the repository root:

```powershell
python dashboard\dashboard.py
```

Verify generated output without changing files:

```powershell
python dashboard\dashboard.py --check
python -m unittest dashboard.test_dashboard
```
