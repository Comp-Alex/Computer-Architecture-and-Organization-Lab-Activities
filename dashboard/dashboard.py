#!/usr/bin/env python3
"""Analyze this repository and generate its portfolio README and dashboard data."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
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
AUTOMATION_SUBJECT_PREFIX = "docs: refresh generated repository dashboard"
TODO_PATTERN = re.compile(r"\b(TODO|FIXME)\b\s*[:\-]?\s*(.*)", re.IGNORECASE)
FRAMEWORK_MARKERS = {
    "Django": ("django",),
    "Flask": ("flask",),
    "FastAPI": ("fastapi",),
    "React": ('\"react\"', "from 'react'", 'from \"react\"'),
    "Vue": ('\"vue\"', "from 'vue'", 'from \"vue\"'),
    "Angular": ('\"@angular/core\"',),
    "Spring": ("spring-boot", "org.springframework"),
    "ASP.NET": ("microsoft.aspnetcore", "<project sdk=\"microsoft.net.sdk.web\""),
}
HARDWARE_MARKERS = {
    "8086 / x86": ("8086", "x86", "tasm", "emu8086"),
    "Arduino": ("arduino", "<arduino.h>"),
    "Raspberry Pi": ("raspberry pi", "raspberry-pi"),
    "AVR": ("avr-gcc", "<avr/"),
    "ARM": ("arm-none-eabi", "cortex-m"),
}


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


def git_output(root: Path, *arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout.strip()


def parse_git_date(value: str) -> datetime | None:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed.astimezone(timezone.utc)


def github_repository(config: dict[str, Any]) -> str | None:
    repository = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if repository:
        return repository
    match = re.match(r"https?://github\.com/([^/]+/[^/#]+)", config.get("repository_url", ""))
    return match.group(1).removesuffix(".git") if match else None


def github_counts(config: dict[str, Any]) -> dict[str, Any]:
    repository = github_repository(config)
    if not repository or os.environ.get("GITHUB_ACTIONS") != "true":
        return {"open_issues": None, "open_pull_requests": None, "open_issue_items": []}

    headers = {"Accept": "application/vnd.github+json", "User-Agent": "repository-dashboard"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    counts: dict[str, int | None] = {}
    issue_items = []
    for key, query in (("open_issues", "is:issue is:open"), ("open_pull_requests", "is:pr is:open")):
        url = f"https://api.github.com/search/issues?q=repo:{repository}+{query}"
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                payload = json.loads(response.read().decode("utf-8"))
            counts[key] = int(payload["total_count"])
            if key == "open_issues":
                issue_items = [
                    {"title": item.get("title", "Untitled issue"), "url": item.get("html_url", "")}
                    for item in payload.get("items", [])[:10]
                ]
        except (OSError, urllib.error.URLError, ValueError, KeyError, TypeError):
            counts[key] = None
    return {**counts, "open_issue_items": issue_items}


def analyze_git(root: Path, config: dict[str, Any]) -> dict[str, Any]:
    git_available = git_output(root, "rev-parse", "--is-inside-work-tree") == "true"
    log = git_output(root, "log", "--all", "--format=%H%x1f%an%x1f%aI%x1f%s", "--name-status")
    commits: list[dict[str, Any]] = []
    current_commit: dict[str, Any] | None = None
    commit_files: dict[str, dict[str, str]] = {}
    for line in log.splitlines():
        fields = line.split("\x1f", 3)
        if len(fields) == 4:
            commit_hash, author, date_text, subject = fields
            committed_at = parse_git_date(date_text)
            if not committed_at:
                current_commit = None
                continue
            current_commit = {
                "hash": commit_hash,
                "author": author,
                "date": committed_at,
                "subject": subject,
            }
            commits.append(current_commit)
            commit_files[commit_hash] = {}
        elif line and current_commit:
            status, separator, filename = line.partition("\t")
            if separator:
                commit_files[current_commit["hash"]][filename] = status
        else:
            continue

    excluded_prefix = config.get("automation_commit_subject_prefix", AUTOMATION_SUBJECT_PREFIX)
    project_commits = [
        commit for commit in commits
        if not commit["subject"].startswith(excluded_prefix)
    ]
    now = datetime.now(timezone.utc)
    last_7_days = [commit for commit in project_commits if (now - commit["date"]).days < 7]
    last_30_days = [commit for commit in project_commits if (now - commit["date"]).days < 30]
    previous_30_days = [
        commit for commit in project_commits
        if 30 <= (now - commit["date"]).days < 60
    ]
    branches = {
        branch for branch in git_output(
            root, "for-each-ref", "--format=%(refname:short)", "refs/heads", "refs/remotes"
        ).splitlines()
        if not branch.endswith("/HEAD")
    }
    modified_files: Counter[str] = Counter()
    folder_activity: Counter[str] = Counter()
    for commit in project_commits:
        for filename in commit_files.get(commit["hash"], {}):
            modified_files[filename] += 1
            parent = Path(filename).parent.as_posix()
            folder_activity[parent if parent != "." else "Repository root"] += 1

    activity_days = Counter(commit["date"].date().isoformat() for commit in project_commits)
    activity_months = Counter(commit["date"].strftime("%Y-%m") for commit in project_commits)
    oldest = min((commit["date"] for commit in project_commits), default=None)
    latest = max(project_commits, key=lambda commit: commit["date"], default=None)
    recent = sorted(project_commits, key=lambda commit: commit["date"], reverse=True)[:8]
    recent_files = [
        (commit, filename, status)
        for commit in recent
        for filename, status in commit_files.get(commit["hash"], {}).items()
    ]
    issues = github_counts(config)

    return {
        "available": git_available,
        "total_commits": len(project_commits),
        "commit_growth_30_days": len(last_30_days) - len(previous_30_days),
        "contributors": len({commit["author"] for commit in project_commits}),
        "branches": len(branches),
        "repository_age_days": (now.date() - oldest.date()).days if oldest else None,
        "last_commit": {
            "hash": latest["hash"][:7],
            "author": latest["author"],
            "date": latest["date"].date().isoformat(),
            "subject": latest["subject"],
        } if latest else None,
        "commits_7_days": len(last_7_days),
        "commits_30_days": len(last_30_days),
        "most_modified_files": [
            {"path": path, "commits": count}
            for path, count in modified_files.most_common(5)
        ],
        "most_active_folders": [
            {"path": path, "commits": count}
            for path, count in folder_activity.most_common(5)
        ],
        "most_active_day": activity_days.most_common(1)[0][0] if activity_days else None,
        "most_active_month": activity_months.most_common(1)[0][0] if activity_months else None,
        "active_folders_30_days": sorted({
            Path(filename).parent.as_posix()
            for commit in last_30_days
            for filename in commit_files.get(commit["hash"], {})
        }),
        "recent_commits": [
            {
                "hash": commit["hash"][:7],
                "author": commit["author"],
                "date": commit["date"].date().isoformat(),
                "subject": commit["subject"],
            }
            for commit in recent
        ],
        "recent_additions": sorted({filename for _, filename, status in recent_files if status.startswith("A")})[:10],
        "recent_improvements": sorted({filename for _, filename, status in recent_files if status.startswith("M")})[:10],
        **issues,
    }


def detect_project_intelligence(files: list[Path], root: Path) -> dict[str, Any]:
    names = {path.name.lower() for path in files}
    corpus = "\n".join(
        read_text(path)[:200_000].lower()
        for path in files
        if path.suffix.lower() in SOURCE_EXTENSIONS | {".json", ".toml", ".xml", ".txt", ".md"}
    )
    project_types = []
    if any(path.name.lower().startswith("lesson") and path.is_dir() for path in root.iterdir()):
        project_types.append("Educational / lab repository")
    if any(path.suffix.lower() in SOURCE_EXTENSIONS for path in files):
        project_types.append("Source-code project")
    if ".md" in {path.suffix.lower() for path in files}:
        project_types.append("Documentation repository")
    if not project_types:
        project_types.append("Repository (type not inferred)")
    frameworks = [
        framework for framework, markers in FRAMEWORK_MARKERS.items()
        if any(marker in corpus for marker in markers)
    ]
    hardware = [
        platform for platform, markers in HARDWARE_MARKERS.items()
        if any(marker in corpus for marker in markers)
    ]
    libraries: set[str] = set()
    if "requirements.txt" in names:
        libraries.update(
            line.split("[", 1)[0].split("=", 1)[0].split(">", 1)[0].strip()
            for line in read_text(next(path for path in files if path.name.lower() == "requirements.txt")).splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    if "package.json" in names:
        for path in files:
            if path.name.lower() == "package.json":
                try:
                    package_data = json.loads(read_text(path))
                    libraries.update(package_data.get("dependencies", {}))
                    libraries.update(package_data.get("devDependencies", {}))
                except (json.JSONDecodeError, AttributeError):
                    pass
    return {
        "project_types": project_types,
        "frameworks": sorted(frameworks),
        "hardware_platforms": sorted(hardware),
        "libraries": sorted(library for library in libraries if library),
    }


def scan_todos(files: list[Path], root: Path) -> list[dict[str, str]]:
    todos = []
    for path in files:
        if path.suffix.lower() not in SOURCE_EXTENSIONS:
            continue
        for line_number, line in enumerate(read_text(path).splitlines(), start=1):
            match = TODO_PATTERN.search(line)
            if match:
                todos.append({
                    "kind": match.group(1).upper(),
                    "path": path.relative_to(root).as_posix(),
                    "line": str(line_number),
                    "text": match.group(2).strip() or line.strip(),
                })
    return todos


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
    source_files = [path for path in all_files if path.suffix.lower() in SOURCE_EXTENSIONS]
    nonempty_code_lines = sum(
        sum(bool(line.strip()) for line in read_text(path).splitlines())
        for path in source_files
    )
    documented_modules = sum((path / "README.md").is_file() for path in lesson_dirs)
    test_files = [
        path for path in all_files
        if re.search(r"(^|[/_-])(test|tests|spec|specs)([/_.-]|$)", path.relative_to(root).as_posix(), re.I)
    ]
    coverage_files = [path for path in all_files if path.name.lower() in {"coverage.xml", "coverage.json", "lcov.info"}]

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
    git = analyze_git(root, config)
    project_intelligence = detect_project_intelligence(all_files, root)
    todos = scan_todos(all_files, root)
    lesson_status = []
    active_folders = set(git["active_folders_30_days"])
    for lesson in lessons:
        has_readme = (root / lesson["name"] / "README.md").is_file()
        all_guides_present = all(exercise["guide"] for exercise in lesson["exercises"])
        lesson_status.append({
            "name": lesson["title"],
            "status": (
                "Active" if lesson["name"] in active_folders
                else "Documented" if has_readme and all_guides_present
                else "In progress"
            ),
            "evidence": (
                "Changed in a commit during the last 30 days."
                if lesson["name"] in active_folders
                else "Lesson README and exercise guides are present."
                if has_readme and all_guides_present
                else "Lesson README or one or more exercise guides are missing."
            ),
        })
    issues_or_todos = [
        {
            "status": todo["kind"],
            "title": f"{todo['path']}:{todo['line']}",
            "detail": todo["text"],
        }
        for todo in todos
    ]
    issues_or_todos.extend(
        {
            "status": "ISSUE",
            "title": item["title"],
            "detail": f"[Open issue]({item['url']})" if item["url"] else "Open GitHub issue.",
        }
        for item in git["open_issue_items"]
    )
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
    roadmap = issues_or_todos
    complexity = {
        "source_files": len(source_files),
        "nonempty_code_lines": nonempty_code_lines,
        "top_level_directories": sum(path.is_dir() for path in root.iterdir()),
        "lesson_modules": len(lessons),
    }
    complexity["maturity"] = (
        "Established" if git["total_commits"] >= 100 and git["contributors"] >= 3
        else "Growing" if git["total_commits"] >= 10 or len(lessons) >= 3
        else "Early"
    )
    complexity["maturity_basis"] = "Heuristic based on project commit, contributor, and module counts."
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
        "repository": git,
        "development": {
            "languages": [
                {"name": language, "files": count}
                for language, count in source_counts.items()
            ],
            "documentation": {
                "markdown_files": markdown_files,
                "documented_modules": documented_modules,
                "total_modules": len(lesson_dirs),
                "coverage_percent": round(100 * documented_modules / len(lesson_dirs), 1)
                if lesson_dirs else None,
            },
            "testing": {
                "test_files": len(test_files),
                "coverage_report": bool(coverage_files),
                "coverage_percent": None,
            },
        },
        "project_intelligence": project_intelligence,
        "learning": {
            "modules": lesson_status,
            "documented_modules": [item["name"] for item in lesson_status if item["status"] == "Documented"],
            "active_modules": [item["name"] for item in lesson_status if item["status"] == "Active"],
        },
        "insights": complexity,
        "todos": todos,
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
