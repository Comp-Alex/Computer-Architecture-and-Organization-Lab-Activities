# Computer Architecture Dashboard

A static, responsive dashboard for the 8086/DOS assembly lessons. It provides topic cards for CPU architecture, memory systems, instruction sets, and lab activities; searchable lesson cards; exercise and sample filters; and direct links to assembly sources and exercise guides.

## Open the dashboard

The page reads `data.json` with `fetch`, so open it through a local web server rather than directly from the filesystem:

```powershell
python dashboard\dashboard.py
python -m http.server 8000
```

Then visit `http://localhost:8000/dashboard/`. Stop the server with `Ctrl+C`.

The static dashboard can also be hosted from the repository root on GitHub Pages.

## Generate the catalog and repository README

From the repository root, run:

```powershell
python dashboard\dashboard.py
```

The standard-library-only analyzer scans repository files, `Lesson<number>` directories, assembly sources, guides, and documentation. It infers the repository purpose, calculates file and exercise statistics, discovers topic coverage, generates evidence-based progress highlights and roadmap items, then refreshes:

- `dashboard/data.json` — lesson, exercise, sample, and guide metadata consumed by the dashboard.
- `README.md` — the portfolio-ready repository overview, statistics, topic map, progress, roadmap, and lesson index, rendered from [`README_TEMPLATE.md`](README_TEMPLATE.md).

Edit [`config.json`](config.json) to adjust the project name, repository URL, ignored directories, or topic keywords. Add or revise content in lesson folders and documentation; the analyzer discovers the updated repository state automatically. Both outputs are deterministic and only rewritten when their contents change.

To check whether generated output is current without writing files:

```powershell
python dashboard\dashboard.py --check
```

An optional `--root C:\path\to\repository` argument points the analyzer at another checkout. It exits with status 1 when `--check` finds stale or missing output.

## Verify the generator

Run the built-in tests from the repository root:

```powershell
python -m unittest dashboard.test_dashboard
```

No JavaScript framework, package install, or third-party Python dependency is required.
