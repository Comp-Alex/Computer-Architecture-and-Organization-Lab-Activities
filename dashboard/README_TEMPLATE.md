<!-- Generated from dashboard/README_TEMPLATE.md by dashboard/dashboard.py. -->

# {{PROJECT_NAME}}

{{REPOSITORY_BADGE}}

{{DASHBOARD_LINK}}

> **Automatically analyzed purpose:** {{PROJECT_PURPOSE}}

## Project overview

{{PROJECT_OVERVIEW}}

This portfolio dashboard is generated from the repository's actual folders, source files, and lesson documentation. Counts, topic coverage, progress highlights, and next steps are refreshed automatically; no hand-maintained inventory is required.

## At a glance

| Repository measure | Current total |
| --- | ---: |
| Files analyzed | {{TOTAL_FILES}} |
| Lesson folders | {{TOTAL_LESSONS}} |
| Numbered exercises | {{TOTAL_EXERCISES}} |
| Assembly source files | {{TOTAL_ASSEMBLY}} |
| Exercise guides | {{TOTAL_GUIDES}} |
| Exercise guide coverage | {{GUIDE_COVERAGE}} |

## Repository contents

File counts are derived from the current working tree. The generated README and dashboard data are excluded to keep the statistics stable, along with version-control and cache directories.

{{SOURCE_BREAKDOWN}}

## Architecture topics

Topic-to-lesson relationships are inferred from the lesson notes and source files using the configurable rules in [`dashboard/config.json`](dashboard/config.json).

{{TOPIC_BREAKDOWN}}

## Progress and achievements

{{ACHIEVEMENTS}}

## Learning roadmap

These next steps are automatically selected from repository evidence, such as undocumented exercises, sample programs without dedicated notes, and the presence or absence of an assembly execution harness.

{{ROADMAP}}

## Lesson and activity index

{{LESSON_INDEX}}

## Run the labs

{{ASSEMBLY_RUN_GUIDE}}

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
