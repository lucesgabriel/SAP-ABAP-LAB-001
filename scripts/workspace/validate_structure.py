#!/usr/bin/env python
"""Validate local organization and relative Markdown links, without contacting SAP.

Cubre: archivos requeridos del laboratorio (incluido knowledge-base/, prompts/, checklists/,
standards/, cases/), plantillas y metadatos de projects/ y cases/, y enlaces Markdown locales.
No valida secretos ni taxonomía: eso lo hace lint_knowledge_base.py.
"""
from __future__ import annotations

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from projects import PROJECT_FILES, ROOT, read_metadata  # noqa: E402
from new_case import ALL_CASE_FILES, CASE_FILES, CASE_FOLDER_RE, read_case_metadata  # noqa: E402

REQUIRED = (
    "AGENTS.md", "CLAUDE.md", "CONTEXT.txt", "README.md",
    "config/system.yaml", "config/README.md", "docs/README.md",
    "docs/guides/organization.md", "docs/guides/daily-workflow.md",
    "docs/guides/self-improvement-loop.md",
    "docs/CLAUDE-DESKTOP-PROJECT-INSTRUCTIONS.md", "docs/TOOL-CATALOG.md",
    "docs/MANUAL-SAP-ABAP-LAB-001.md", "docs/MANUAL-SAP-ABAP-LAB-001.pdf",
    "projects/README.md", "learning/README.md", "learning/roadmap.md",
    "learning/lessons.md", "learning/decisions.md", "learning/patterns.md",
    "learning/backlog.md", "learning/templates/README.md",
    "learning/templates/exercise.md", "learning/templates/session.md",
    "learning/exercises/README.md", "learning/sessions/README.md",
    "knowledge-base/README.md", "knowledge-base/taxonomy.md",
    "knowledge-base/error-catalog.md", "knowledge-base/solution-patterns.md",
    "knowledge-base/decision-registry.md", "knowledge-base/released-api-recipes.md",
    "knowledge-base/lessons-learned-index.md",
    "cases/README.md", "cases/_index.md", "cases/_status.md",
    "prompts/README.md", "prompts/00-nuevo-proyecto.md", "prompts/01-disenar-solucion.md",
    "prompts/02-construir-con-arc1.md", "prompts/03-revisar-calidad.md",
    "prompts/04-generar-caso-practica.md", "prompts/05-retrospectiva-cierre.md",
    "checklists/README.md", "checklists/abap-quality-gate.md",
    "checklists/rap-release-gate.md", "checklists/clean-core-gate.md",
    "standards/README.md", "standards/naming-conventions.md",
    "standards/technology-decision-matrix.md",
    "scripts/README.md", "scripts/workspace/kb.py", "scripts/workspace/projects.py",
    "scripts/workspace/new_case.py", "scripts/workspace/close_project.py",
    "scripts/workspace/lint_knowledge_base.py",
    "scripts/workspace/validate_structure.py", "artifacts/README.md",
    "scripts/workspace/books.py", "scripts/workspace/skill_router.py",
    "config/books.json", "config/skills-routing.json", "docs/guides/reference-library.md",
)
SKIP_DIRS = {".git", "artifacts", "__pycache__", ".venv", "node_modules", "logs", ".cache", ".pytest_cache"}


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
    cases = root / "cases"
    template = cases / "_template"
    for relative in CASE_FILES:
        if not (template / relative).is_file():
            errors.append(f"Falta archivo de plantilla de caso: _template/{relative}")
    if cases.is_dir():
        for directory in sorted(cases.iterdir()):
            if not directory.is_dir() or directory.name.startswith("_"):
                continue
            if not CASE_FOLDER_RE.match(directory.name):
                errors.append(f"Carpeta de caso con nombre inválido: cases/{directory.name}")
                continue
            count += 1
            for relative in ALL_CASE_FILES:
                if not (directory / relative).is_file():
                    errors.append(f"Falta archivo de caso: {directory.name}/{relative}")
            try:
                read_case_metadata(directory)
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
    print(f"Estructura local: {'FAIL' if errors else 'PASS'} | {count} proyecto(s)/caso(s) | {len(errors)} error(es)")
    print("Alcance: archivos, metadatos y enlaces locales inline; no valida anclas, secretos ni SAP. "
          "Para taxonomía y secretos: python scripts/workspace/lint_knowledge_base.py")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
