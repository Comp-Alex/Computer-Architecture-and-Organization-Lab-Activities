"""Tests for repository analysis and generated documentation."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from dashboard.dashboard import build_catalog, main, render_readme


class DashboardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.dashboard_dir = self.root / "dashboard"
        self.dashboard_dir.mkdir()
        template = Path(__file__).resolve().parent / "README_TEMPLATE.md"
        (self.dashboard_dir / "README_TEMPLATE.md").write_text(
            template.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        config = json.loads(
            (Path(__file__).resolve().parent / "config.json").read_text(encoding="utf-8")
        )
        (self.dashboard_dir / "config.json").write_text(
            json.dumps(config),
            encoding="utf-8",
        )

        lesson = self.root / "Lesson2"
        lesson.mkdir()
        (lesson / "README.md").write_text(
            "# Lesson 2\n\nBasic DOS character output using INT 21h.\n",
            encoding="utf-8",
        )
        (lesson / "Exer1.asm").write_text(
            "mov ah, 02h\nint 21h\n",
            encoding="utf-8",
        )
        (lesson / "Exer1.README.md").write_text(
            "# Exer1\n\n## Purpose\nPrint a character through DOS.\n",
            encoding="utf-8",
        )
        (lesson / "Sample1.asm").write_text("int 21h\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_analyzer_builds_repository_specific_statistics_and_topics(self) -> None:
        config = json.loads((self.dashboard_dir / "config.json").read_text(encoding="utf-8"))
        catalog = build_catalog(self.root, config)

        self.assertEqual(catalog["totals"]["lessons"], 1)
        self.assertEqual(catalog["totals"]["assembly_files"], 2)
        self.assertEqual(catalog["totals"]["exercises"], 1)
        self.assertEqual(catalog["totals"]["samples"], 1)
        self.assertEqual(catalog["totals"]["guides"], 1)
        self.assertEqual(catalog["totals"]["guide_coverage"], 100.0)
        instruction_topic = next(topic for topic in catalog["topics"] if topic["id"] == "instructions")
        self.assertEqual(instruction_topic["lessons"][0]["number"], 2)
        self.assertIn("16-bit x86 assembly", catalog["purpose"])

    def test_readme_uses_root_relative_links_and_dynamic_sections(self) -> None:
        config = json.loads((self.dashboard_dir / "config.json").read_text(encoding="utf-8"))
        catalog = build_catalog(self.root, config)
        template = (self.dashboard_dir / "README_TEMPLATE.md").read_text(encoding="utf-8")

        readme = render_readme(catalog, template)

        self.assertIn("[Exer1](Lesson2/Exer1.asm)", readme)
        self.assertIn("[Exer1 guide](Lesson2/Exer1.README.md)", readme)
        self.assertIn("**2 assembly source files**", readme)
        self.assertIn("**NEXT · Validate programs in a DOS-compatible environment**", readme)
        self.assertNotIn("{{", readme)

    def test_generator_writes_then_checks_deterministic_outputs(self) -> None:
        self.assertEqual(main(["--root", str(self.root)]), 0)
        readme = (self.root / "README.md").read_text(encoding="utf-8")
        data = json.loads((self.dashboard_dir / "data.json").read_text(encoding="utf-8"))
        self.assertIn("## Learning roadmap", readme)
        self.assertEqual(data["totals"]["assembly_files"], 2)
        self.assertEqual(main(["--root", str(self.root), "--check"]), 0)

        (self.dashboard_dir / "data.json").write_text("{}\n", encoding="utf-8")
        self.assertEqual(main(["--root", str(self.root), "--check"]), 1)

    def test_missing_exercise_guides_are_reported_as_coverage_gaps(self) -> None:
        (self.root / "Lesson2" / "Exer1.README.md").unlink()
        config = json.loads((self.dashboard_dir / "config.json").read_text(encoding="utf-8"))
        catalog = build_catalog(self.root, config)

        self.assertEqual(catalog["totals"]["guides"], 0)
        self.assertEqual(catalog["totals"]["guide_coverage"], 0.0)
        self.assertIn("Complete exercise guide coverage", catalog["roadmap"][0]["title"])


if __name__ == "__main__":
    unittest.main()
