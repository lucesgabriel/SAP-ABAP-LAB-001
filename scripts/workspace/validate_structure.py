#!/usr/bin/env python
"""Validate local organization and relative Markdown links, without contacting SAP."""
from __future__ import annotations

from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from projects import PROJECT_FILES, ROOT, read_metadata

REQUIRED = (
    "AGENTS.md", "CLAUDE.md", "CONTEXT.txt", "README.md",
    "config/system.yaml", "config/README.md", "docs/README.md",
    "docs/guides/organization.md", "docs/guides/daily-workflow.md",
    "docs/CLAUDE-DESKTOP-PROJECT-INSTRUCTIONS.md", "docs/TOOL-CATALOG.md",
    "docs/MANUAL-SAP-ABAP-LAB-001.md", "docs/MANUAL-SAP-ABAP-LAB-001.pdf",
    "projects/README.md", "learning/README.md", "learning/roadmap.md",
    "learning/lessons.md", "learning/decisions.md", "learning/patterns.md",
    "learning/backlog.md", "learning/templates/README.md",
    "learning/templates/exercise.md", "learning/templates/session.md",
    "learning/exercises/README.md", "learning/sessions/README.md",
    "scripts/README.md", "scripts/workspace/projects.py",
    "scripts/workspace/validate_structure.py", "artifacts/README.md",
)
SKIP_DIRS = {".git", "artifacts", "__pycache__", ".venv", "node_modules", "logs", ".cache"}


def validate(root: Path) -> tuple[list[str], int]:
    errors = []
    for relative in REQUIRED:
        if not (root / relative).is_file():
            errors.append(f"Falta archivo requerido: {relative}")
    base = root / "projects"
    count = 0
    directories = [base / "_template"]
    if base.is_dir():
        directories.extend(path for path in sorted(base.iterdir())
                           if path.is_dir() and path.name != "_template")
    for directory in directories:
        for relative in PROJECT_FILES:
            if not (directory / relative).is_file():
                errors.append(f"Falta archivo de proyecto: {directory.name}/{relative}")
        if directory.name == "_template":
            continue
        count += 1
        try:
            read_metadata(directory)
        except (OSError, ValueError) as exc:
            errors.append(f"{directory.name}: {exc}")
    # Check inline Markdown file links; external URLs and heading anchors are excluded.
    # Not a full Markdown parser: reference-style links and anchor existence are not checked.
    for path in root.rglob("*.md"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        for match in re.finditer(r"\[[^\]\n]+\]\(([^)\n]+)\)", text):
            target = match.group(1).strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = path.parent / unquote(parsed.path)
            if not destination.exists():
                errors.append(f"Enlace local roto en {path.relative_to(root)}: {target}")
    return errors, count


def main() -> int:
    errors, count = validate(ROOT)
    for error in errors:
        print(f"[ERROR] {error}")
    print(f"Estructura local: {'FAIL' if errors else 'PASS'} | {count} proyecto(s) | {len(errors)} error(es)")
    print("Alcance: archivos, metadatos y enlaces locales inline; no valida anclas, secretos ni SAP.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
