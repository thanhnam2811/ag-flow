#!/usr/bin/env python3
"""Lightweight repository validator for ag-flow.

Checks:
- Agent Skill YAML frontmatter (`name`, `description`)
- relative Markdown links
- JSON Schema validity
- canonical Work Package YAML example against the schema
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
SCHEMA_PATH = ROOT / "references" / "schemas" / "work-package.schema.json"
EXAMPLE_PATH = ROOT / "references" / "examples" / "work-package.example.yaml"

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_skill_frontmatter(errors: list[str]) -> None:
    skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
    if not skill_files:
        fail(errors, "No skills/*/SKILL.md files found")
        return

    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        lines = text.splitlines()
        rel = path.relative_to(ROOT)
        if not lines or lines[0].strip() != "---":
            fail(errors, f"{rel}: missing opening YAML frontmatter delimiter")
            continue

        try:
            end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        except StopIteration:
            fail(errors, f"{rel}: missing closing YAML frontmatter delimiter")
            continue

        try:
            data = yaml.safe_load("\n".join(lines[1:end])) or {}
        except yaml.YAMLError as exc:
            fail(errors, f"{rel}: invalid YAML frontmatter: {exc}")
            continue

        if not isinstance(data, dict):
            fail(errors, f"{rel}: frontmatter must be a mapping")
            continue

        name = data.get("name")
        description = data.get("description")
        expected_name = path.parent.name

        if not isinstance(name, str) or not name.strip():
            fail(errors, f"{rel}: frontmatter 'name' must be a non-empty string")
        elif name != expected_name:
            fail(errors, f"{rel}: name '{name}' must match directory '{expected_name}'")

        if not isinstance(description, str) or len(description.strip()) < 20:
            fail(errors, f"{rel}: frontmatter 'description' must be a descriptive string (>=20 chars)")


def validate_markdown_links(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue

            target = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not target:
                continue

            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(errors, f"{rel}: link escapes repository: {raw_target}")
                continue

            if not resolved.exists():
                fail(errors, f"{rel}: broken relative link: {raw_target}")


def validate_work_package_schema(errors: list[str]) -> None:
    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"{SCHEMA_PATH.relative_to(ROOT)}: cannot load schema: {exc}")
        return

    try:
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # jsonschema exposes several schema error subclasses
        fail(errors, f"{SCHEMA_PATH.relative_to(ROOT)}: invalid JSON Schema: {exc}")
        return

    try:
        instance = yaml.safe_load(EXAMPLE_PATH.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        fail(errors, f"{EXAMPLE_PATH.relative_to(ROOT)}: cannot load example: {exc}")
        return

    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path)):
        location = ".".join(str(p) for p in error.absolute_path) or "<root>"
        fail(errors, f"{EXAMPLE_PATH.relative_to(ROOT)}:{location}: {error.message}")


def main() -> int:
    errors: list[str] = []
    validate_skill_frontmatter(errors)
    validate_markdown_links(errors)
    validate_work_package_schema(errors)

    if errors:
        print(f"ag-flow validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("ag-flow validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
