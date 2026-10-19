#!/usr/bin/env python3
"""Analyze this repository and generate its portfolio README and dashboard data."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
LESSON_PATTERN = re.compile(r"Lesson(\d+)", re.IGNORECASE)
EXERCISE_PATTERN = re.compile(r"Exer\d+", re.IGNORECASE)
WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
EXTENSION_NAMES = {
    ".asm": "Assembly",
    ".bat": "Batch",
    ".css": "CSS",
    ".doc": "Legacy document",
    ".docx": "Word document",
    ".html": "HTML",
    ".js": "JavaScript",
    ".json": "JSON",
    ".md": "Markdown",
    ".pdf": "PDF",
    ".ps1": "PowerShell",
    ".py": "Python",
    ".sh": "Shell",
    ".svg": "SVG",
    ".txt": "Text",
    ".yaml": "YAML",
    ".yml": "YAML",
}
SOURCE_EXTENSIONS = {
    ".asm",
    ".bat",
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".css",
    ".go",
    ".h",
    ".html",
    ".java",
    ".js",
    ".jsx",
    ".kt",
    ".php",
    ".ps1",
    ".py",
    ".rb",
    ".rs",
    ".sh",
    ".sql",
    ".ts",
    ".tsx",
}
EXECUTION_CHECK_EXTENSIONS = {".bat", ".ps1", ".py", ".sh", ".yml", ".yaml"}


def natural_key(value: str) -> list[int | str]:
    return [int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", value)]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def load_config(root: Path) -> dict[str, Any]:
    config_path = root / "dashboard" / "config.json"
    if not config_path.is_file():
        raise FileNotFoundError(f"dashboard configuration not found: {config_path}")
    config = json.loads(read_text(config_path))
    if not isinstance(config, dict):
        raise ValueError(f"dashboard configuration must be a JSON object: {config_path}")
    return config


def collect_files(root: Path, excluded_directories: list[str]) -> list[Path]:
    excluded = set(excluded_directories)
    files: list[Path] = []
    for current, directories, filenames in os.walk(root, followlinks=False):
        directories[:] = sorted(
            (name for name in directories if name not in excluded),
            key=natural_key,
        )
        current_path = Path(current)
        for filename in filenames:
            file_path = current_path / filename
            if file_path.is_file() and not file_path.is_symlink():
                files.append(file_path)
    return sorted(files, key=lambda path: natural_key(path.relative_to(root).as_posix()))


def first_lesson_paragraph(readme: Path, fallback: str) -> str:
    if not readme.is_file():
        return fallback
    for line in read_text(readme).splitlines():
        text = line.strip()
        if text and not text.startswith(("#", "[", "|", "```")):
            return text
    return fallback


def exercise_purpose(guide: Path, fallback: str) -> str:
    if not guide.is_file():
        return fallback
    in_purpose = False
    for line in read_text(guide).splitlines():
        text = line.strip()
        if text.startswith("#"):
            in_purpose = text.lower() == "## purpose"
        elif in_purpose and text:
            return text
    return fallback


def topic_matches(text: str, keywords: list[str]) -> bool:
    words = WORD_PATTERN.findall(text.lower())
    word_set = set(words)
    normalized = " ".join(words)
    for keyword in keywords:
        keyword_words = WORD_PATTERN.findall(keyword.lower())
        if not keyword_words:
            continue
        if len(keyword_words) == 1 and keyword_words[0] in word_set:
            return True
        if f" {' '.join(keyword_words)} " in f" {normalized} ":
            return True
    return False


def scan_lesson(lesson_dir: Path, root: Path) -> dict[str, Any]:
    number = int(LESSON_PATTERN.fullmatch(lesson_dir.name).group(1))
    summary = first_lesson_paragraph(
        lesson_dir / "README.md",
        "Lesson materials and assembly activities.",
    )
    exercises: list[dict[str, Any]] = []
    samples: list[dict[str, str]] = []
    searchable_parts = [lesson_dir.name, summary]

    asm_files = sorted(lesson_dir.glob("*.asm"), key=lambda path: natural_key(path.name))
    for source in asm_files:
        source_relative = source.relative_to(root).as_posix()
        source_dashboard = f"../{source_relative}"
        source_text = read_text(source)[:1_000_000]
        searchable_parts.extend((source.stem, source_text))

        if EXERCISE_PATTERN.fullmatch(source.stem):
            expected_guide_name = f"{source.stem}.README.md".lower()
            guide = next(
                (
                    candidate
                    for candidate in lesson_dir.iterdir()
                    if candidate.is_file() and candidate.name.lower() == expected_guide_name
                ),
                None,
            )
            purpose = exercise_purpose(guide, summary) if guide else summary
            searchable_parts.append(purpose)
            exercises.append(
                {
                    "name": source.stem,
                    "source": source_relative,
                    "dashboard_source": source_dashboard,
                    "guide": guide.relative_to(root).as_posix() if guide else None,
                    "dashboard_guide": (
                        f"../{guide.relative_to(root).as_posix()}" if guide else None
                    ),
                    "description": purpose,
                }
            )
        else:
            samples.append(
                {
                    "name": source.stem,
                    "source": source_relative,
                    "dashboard_source": source_dashboard,
                }
            )

    for markdown in sorted(lesson_dir.glob("*.md"), key=lambda path: natural_key(path.name)):
        searchable_parts.append(read_text(markdown)[:250_000])

    return {
        "number": number,
        "name": lesson_dir.name,
        "title": f"Lesson {number}",
        "path": f"{lesson_dir.name}/README.md",
        "dashboard_path": f"../{lesson_dir.name}/README.md",
        "description": summary,
        "exercises": exercises,
        "samples": samples,
        "has_sample_problems": (lesson_dir / "SampleProblems.md").is_file()
        or (lesson_dir / "SampleProblems.asm").is_file(),
        "search_text": "\n".join(searchable_parts).lower(),
    }


def infer_purpose(
    project_name: str,
    lessons: list[dict[str, Any]],
    assembly_files: int,
    markdown_files: int,
) -> str:
    corpus = " ".join(
        [project_name]
        + [lesson["description"] for lesson in lessons]
        + [
            exercise["description"]
            for lesson in lessons
            for exercise in lesson["exercises"]
        ]
    ).lower()
    if assembly_files and any(
        marker in corpus for marker in ("computer architecture", "computer organization", "8086", "tasm")
    ):
        return (
            "A hands-on computer architecture and organization laboratory. Its lessons teach "
            "16-bit x86 assembly programming through DOS/TASM exercises, sample programs, "
            "and peripheral-I/O activities."
        )
    if lessons and assembly_files:
        return (
            f"An instructional repository with {len(lessons)} lesson units and "
            f"{assembly_files} assembly-language program files, organized for practical lab work."
        )
    if lessons:
        return (
            f"An instructional repository organized into {len(lessons)} lesson units, "
            "with lesson material discovered directly from its documentation."
        )
    if assembly_files:
        return (
            f"A programming repository containing {assembly_files} assembly-language "
            "source files and related project documentation."
        )
    if markdown_files:
        return (
            f"A documentation-focused repository containing {markdown_files} Markdown "
            "documents, organized for project reference and collaboration."
        )
    return (
        f"A {project_name} repository. Its purpose is inferred from the source files, "
        "documentation, and directory structure discovered by the dashboard analyzer."
    )


def build_topics(
    lesson_catalog: list[dict[str, Any]],
    topic_rules: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    topics: list[dict[str, Any]] = []
    for rule in topic_rules:
        keywords = rule.get("keywords", [])
        matching_lessons = [
            {
                "number": lesson["number"],
                "title": lesson["title"],
            }
            for lesson in lesson_catalog
            if topic_matches(lesson["search_text"], keywords)
        ]
        topics.append(
            {
                "id": rule["id"],
                "title": rule["title"],
                "description": rule["description"],
                "label": rule.get("label", rule["title"].upper()),
                "lessons": matching_lessons,
            }
        )
    return topics


def build_roadmap(
    lessons: list[dict[str, Any]],
    assembly_files: int,
    sample_guide_count: int,
    execution_harness_found: bool,
) -> list[dict[str, str]]:
    numbered_exercises = [
        exercise for lesson in lessons for exercise in lesson["exercises"]
    ]
    missing_guides = [
        exercise["name"]
        for exercise in numbered_exercises
        if exercise["guide"] is None
    ]
    roadmap: list[dict[str, str]] = []

    if missing_guides:
        roadmap.append(
            {
                "status": "NEXT",
                "title": "Complete exercise guide coverage",
                "detail": (
                    f"Create guides for {len(missing_guides)} currently undocumented "
                    f"exercise(s): {', '.join(missing_guides)}."
                ),
            }
        )

    if assembly_files and not execution_harness_found:
        roadmap.append(
            {
                "status": "NEXT",
                "title": "Validate programs in a DOS-compatible environment",
                "detail": (
                    f"Add reproducible TASM/DOSBox smoke checks for the {assembly_files} "
                    "assembly sources. The current material describes manual assembly and "
                    "execution rather than an automated run harness."
                ),
            }
        )

    total_samples = sum(len(lesson["samples"]) for lesson in lessons)
    undocumented_samples = total_samples - sample_guide_count
    if undocumented_samples > 0:
        roadmap.append(
            {
                "status": "NEXT",
                "title": "Add context for sample programs",
                "detail": (
                    f"Add brief purpose and learning-outcome notes for {undocumented_samples} "
                    "sample assembly programs without dedicated guides; lesson-level notes "
                    "currently provide the shared context."
                ),
            }
        )

    highest_lesson = max((lesson["number"] for lesson in lessons), default=0)
    roadmap.append(
        {
            "status": "ONGOING",
            "title": "Keep the lesson index in sync",
            "detail": (
                f"The analyzer currently discovers {len(lessons)} lesson folders "
                f"(through Lesson {highest_lesson}). Add new lesson folders, source files, "
                "and guides to have them indexed automatically."
                if lessons
                else "Add lesson folders and documentation to populate the project dashboard automatically."
            ),
        }
    )
    return roadmap


def build_catalog(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    excluded_directories = config.get(
        "excluded_directories",
        [".git", "__pycache__", ".venv", "venv", "node_modules"],
    )
    generated_files = {"README.md", "dashboard/data.json"}
    all_files = [
        path
        for path in collect_files(root, excluded_directories)
        if path.relative_to(root).as_posix() not in generated_files
    ]
    lesson_dirs = sorted(
        (
            path
            for path in root.iterdir()
            if path.is_dir() and LESSON_PATTERN.fullmatch(path.name)
        ),
        key=lambda path: natural_key(path.name),
    )
    lessons = [scan_lesson(path, root) for path in lesson_dirs]
    topic_rules = config.get("topics", [])
    topics = build_topics(lessons, topic_rules)
    extension_counts: dict[str, int] = {}
    for path in all_files:
        suffix = path.suffix.lower() or "[no extension]"
        extension_counts[suffix] = extension_counts.get(suffix, 0) + 1

    assembly_files = extension_counts.get(".asm", 0)
    markdown_files = extension_counts.get(".md", 0)
    numbered_exercises = [exercise for lesson in lessons for exercise in lesson["exercises"]]
    sample_files = [sample for lesson in lessons for sample in lesson["samples"]]
    guide_coverage = (
        round(
            100
            * sum(exercise["guide"] is not None for exercise in numbered_exercises)
            / len(numbered_exercises),
            1,
        )
        if numbered_exercises
        else 100.0
    )

    source_counts: dict[str, int] = {}
    for path in all_files:
        suffix = path.suffix.lower()
        if suffix in SOURCE_EXTENSIONS:
            language = EXTENSION_NAMES.get(suffix, suffix.removeprefix(".").upper())
            source_counts[language] = source_counts.get(language, 0) + 1
    source_counts = dict(
        sorted(source_counts.items(), key=lambda item: (-item[1], item[0].lower()))
    )

    harness_pattern = re.compile(
        r"(?:dosbox|emu8086|tasm.{0,40}(?:test|smoke|run)|(?:test|smoke|run).{0,40}tasm)",
        re.IGNORECASE | re.DOTALL,
    )
    execution_harness_found = any(
        path.resolve() != Path(__file__).resolve()
        and path.suffix.lower() in EXECUTION_CHECK_EXTENSIONS
        and harness_pattern.search(read_text(path)[:1_000_000])
        for path in all_files
    )

    project_name = config.get("project_name", root.name.replace("-", " "))
    purpose = infer_purpose(project_name, lessons, assembly_files, markdown_files)
    achievements = []
    if lessons:
        achievements.append(
            f"Organized **{len(lessons)} lessons** into a browsable, automatically maintained curriculum."
        )
    if numbered_exercises:
        achievements.append(
            f"Indexed **{len(numbered_exercises)} numbered exercises** with "
            f"**{sum(exercise['guide'] is not None for exercise in numbered_exercises)} guides** "
            f"({guide_coverage:g}% guide coverage)."
        )
    if sample_files:
        achievements.append(
            f"Cataloged **{len(sample_files)} sample programs** alongside the exercises."
        )
    if assembly_files:
        achievements.append(
            f"Tracked **{assembly_files} assembly source files** across the repository."
        )
    if not achievements:
        achievements.append("Repository inventory and documentation are ready to grow with the project.")

    sample_guide_count = sum(
        (root / lesson["name"] / f"{sample['name']}.README.md").is_file()
        for lesson in lessons
        for sample in lesson["samples"]
    )
    roadmap = build_roadmap(
        lessons,
        assembly_files,
        sample_guide_count,
        execution_harness_found,
    )
    return {
        "project": project_name,
        "repository_url": config.get("repository_url", ""),
        "purpose": purpose,
        "lessons": [
            {key: value for key, value in lesson.items() if key != "search_text"}
            for lesson in lessons
        ],
        "topics": topics,
        "roadmap": roadmap,
        "achievements": achievements,
        "totals": {
            "files": len(all_files),
            "source_files": sum(source_counts.values()),
            "lessons": len(lessons),
            "exercises": len(numbered_exercises),
            "assembly_files": assembly_files,
            "samples": len(sample_files),
            "guides": sum(exercise["guide"] is not None for exercise in numbered_exercises),
            "markdown_files": markdown_files,
            "guide_coverage": guide_coverage,
        },
        "file_types": [
            {
                "extension": extension,
                "label": EXTENSION_NAMES.get(
                    extension,
                    "No extension" if extension == "[no extension]" else "Other",
                ),
                "count": count,
            }
            for extension, count in sorted(
                extension_counts.items(),
                key=lambda item: (-item[1], item[0].lower()),
            )
        ],
    }


def markdown_lesson_links(lesson: dict[str, Any]) -> str:
    exercises = ", ".join(
        f"[{exercise['name']}]({exercise['source']})"
        for exercise in lesson["exercises"]
    ) or "—"
    samples = ", ".join(
        f"[{sample['name']}]({sample['source']})"
        for sample in lesson["samples"]
    ) or "—"
    guides = ", ".join(
        f"[{exercise['name']} guide]({exercise['guide']})"
        for exercise in lesson["exercises"]
        if exercise["guide"]
    )
    notes = f"[Lesson notes]({lesson['path']})"
    if guides:
        notes += f"; {guides}"
    description = lesson["description"].replace("|", "\\|")
    return (
        f"| [{lesson['title']}]({lesson['path']}) | {description} | "
        f"{exercises} | {samples} | {notes} |"
    )


def render_readme(catalog: dict[str, Any], template: str) -> str:
    totals = catalog["totals"]
    badge_url = ""
    repo_url = catalog["repository_url"].rstrip("/")
    if repo_url:
        badge_url = (
            f"[![Daily dashboard update]({repo_url}/actions/workflows/dashboard.yml/badge.svg)]"
            f"({repo_url}/actions/workflows/dashboard.yml)"
        )

    source_lines = ["| Type | Files |", "| --- | ---: |"]
    source_lines.extend(
        f"| {item['label']} (`{item['extension']}`) | {item['count']} |"
        for item in catalog["file_types"]
    )

    topic_lines = ["| Topic | Lesson coverage |"]
    topic_lines.append("| --- | --- |")
    topic_lines.extend(
        f"| **{topic['title']}** — {topic['description']} | "
        + (
            ", ".join(
                f"[{lesson['title']}]({next((item['path'] for item in catalog['lessons'] if item['number'] == lesson['number']), '#')})"
                for lesson in topic["lessons"]
            )
            or "No matching lessons discovered"
        )
        + " |"
        for topic in catalog["topics"]
    )

    roadmap_lines = [
        f"- **{item['status']} · {item['title']}** — {item['detail']}"
        for item in catalog["roadmap"]
    ]
    replacements = {
        "{{PROJECT_NAME}}": catalog["project"],
        "{{REPOSITORY_BADGE}}": badge_url,
        "{{PROJECT_PURPOSE}}": catalog["purpose"],
        "{{PROJECT_OVERVIEW}}": (
            f"This repository contains **{totals['lessons']} lesson folders**, "
            f"**{totals['assembly_files']} assembly source files**, "
            f"**{totals['exercises']} numbered exercises**, and "
            f"**{totals['guides']} exercise guides**."
            if totals["lessons"] or totals["assembly_files"]
            else f"The analyzer inventoried **{totals['files']} repository files**."
        ),
        "{{TOTAL_FILES}}": str(totals["files"]),
        "{{TOTAL_LESSONS}}": str(totals["lessons"]),
        "{{TOTAL_EXERCISES}}": str(totals["exercises"]),
        "{{TOTAL_ASSEMBLY}}": str(totals["assembly_files"]),
        "{{TOTAL_GUIDES}}": str(totals["guides"]),
        "{{GUIDE_COVERAGE}}": f"{totals['guide_coverage']:g}%",
        "{{SOURCE_BREAKDOWN}}": "\n".join(source_lines),
        "{{TOPIC_BREAKDOWN}}": "\n".join(topic_lines),
        "{{ROADMAP}}": "\n".join(roadmap_lines),
        "{{ACHIEVEMENTS}}": "\n".join(f"- {item}" for item in catalog["achievements"]),
        "{{LESSON_INDEX}}": (
            "\n".join(
                [
                    "| Lesson | Focus | Exercises | Samples | Notes |",
                    "| --- | --- | --- | --- | --- |",
                    *(markdown_lesson_links(lesson) for lesson in catalog["lessons"]),
                ]
            )
            if catalog["lessons"]
            else "No `Lesson<number>` folders were found. Add lesson directories and rerun the dashboard generator."
        ),
        "{{ASSEMBLY_RUN_GUIDE}}": (
            "The assembly files use DOS/TASM conventions. Run these commands from the "
            "lesson folder in DOSBox or another compatible 16-bit DOS environment:\n\n"
            "```text\n"
            "tasm ExerN.asm\n"
            "tlink ExerN.obj\n"
            "ExerN.exe\n"
            "```\n\n"
            "Replace `ExerN` with the exercise filename. Some sample programs may have "
            "different input/output behavior; consult each lesson's notes before running."
            if totals["assembly_files"]
            else "No assembly source files were detected yet. This section will be populated when source files are added."
        ),
        "{{DASHBOARD_LINK}}": "[Open the interactive dashboard](dashboard/index.html)",
    }

    rendered = template
    for placeholder, replacement in replacements.items():
        rendered = rendered.replace(placeholder, replacement)
    unresolved = re.findall(r"\{\{[A-Z_]+\}\}", rendered)
    if unresolved:
        raise ValueError(f"README template contains unsupported placeholders: {', '.join(unresolved)}")
    return rendered.rstrip() + "\n"


def write_if_changed(path: Path, content: str) -> bool:
    if path.is_file() and read_text(path) == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=SCRIPT_DIR.parent,
        help="repository root (defaults to the parent folder of this script)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="check generated output without changing files (exit 1 if stale)",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"repository root does not exist or is not a directory: {root}")

    try:
        config = load_config(root)
        catalog = build_catalog(root, config)
        template_path = root / "dashboard" / "README_TEMPLATE.md"
        if not template_path.is_file():
            raise FileNotFoundError(f"README template not found: {template_path}")
        rendered_readme = render_readme(catalog, read_text(template_path))
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Dashboard generation failed: {error}", file=sys.stderr)
        return 2

    outputs = {
        root / "README.md": rendered_readme,
        root / "dashboard" / "data.json": json.dumps(catalog, indent=2, ensure_ascii=False) + "\n",
    }
    if args.check:
        stale = [
            path
            for path, content in outputs.items()
            if not path.is_file() or read_text(path) != content
        ]
        if stale:
            for path in stale:
                print(f"Out of date: {path.relative_to(root)}", file=sys.stderr)
            return 1
        print("Generated README and dashboard data are up to date.")
        return 0

    changed = [path for path, content in outputs.items() if write_if_changed(path, content)]
    if changed:
        for path in changed:
            print(f"Updated {path.relative_to(root)}")
    else:
        print("Generated README and dashboard data are already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
