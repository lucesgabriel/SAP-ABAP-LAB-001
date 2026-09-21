#!/usr/bin/env python
"""Create and list local ABAP projects. No SAP calls or external dependencies."""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
ID_PATTERN = re.compile(r"[a-z][a-z0-9]*-[0-9]{3,}-[a-z0-9]+(?:-[a-z0-9]+)*")
STATUSES = {"planned", "active", "blocked", "completed", "archived"}
PROJECT_FILES = (
    "project.json", "README.md", "docs/design.md", "docs/backlog.md",
    "docs/journal.md", "src/README.md", "tests/plan.md", "evidence/README.md",
    "evidence/completion.md", "transports/README.md",
)


def read_metadata(directory: Path) -> dict:
    data = json.loads((directory / "project.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("project.json debe contener un objeto JSON")
    if data.get("schema_version") != 1:
        raise ValueError("schema_version debe ser 1")
    if data.get("id") != directory.name or not ID_PATTERN.fullmatch(directory.name):
        raise ValueError("id inválido o distinto del nombre de carpeta")
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        raise ValueError("title debe ser texto no vacío")
    if not isinstance(data.get("status"), str) or data["status"] not in STATUSES:
        raise ValueError("status inválido")
    try:
        date.fromisoformat(data.get("created_on", ""))
    except (TypeError, ValueError):
        raise ValueError("created_on debe ser una fecha ISO") from None
    if data.get("system_config") != "../../config/system.yaml":
        raise ValueError("system_config debe apuntar a ../../config/system.yaml")
    for field in ("sap_package", "transport_request"):
        if field not in data or (data[field] is not None and
                                 (not isinstance(data[field], str) or not data[field].strip())):
            raise ValueError(f"{field} debe ser null o texto no vacío")
    return data


def create_project(root: Path, project_id: str, title: str) -> Path:
    if not ID_PATTERN.fullmatch(project_id):
        raise ValueError("Identificador inválido; usa abap-001-tema (minúsculas y guiones).")
    title = title.strip()
    if not title or any(ord(char) < 32 for char in title):
        raise ValueError("El título debe ser texto no vacío en una sola línea.")
    base = root.resolve() / "projects"
    template = base / "_template"
    target = base / project_id
    if base.is_symlink() or base.resolve().parent != root.resolve():
        raise ValueError("projects debe permanecer dentro del laboratorio.")
    if target.exists() or target.is_symlink():
        raise ValueError("El proyecto ya existe; no se sobrescribió ningún archivo.")
    for relative in PROJECT_FILES:
        if not (template / relative).is_file():
            raise ValueError(f"Plantilla incompleta: {relative}")
    if template.is_symlink() or any(path.is_symlink() for path in template.rglob("*")):
        raise ValueError("La plantilla no debe contener enlaces simbólicos.")
    created_on = date.today().isoformat()
    data = json.loads((template / "project.json").read_text(encoding="utf-8"))
    data.update(id=project_id, title=title, created_on=created_on, status="planned")
    # copytree rejects an existing destination, including a concurrent creation.
    shutil.copytree(template, target)
    for path in target.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        # A callback avoids recursively replacing tokens supplied in the title.
        values = {"PROJECT_ID": project_id, "PROJECT_TITLE": title, "CREATED_ON": created_on}
        text = re.sub(r"\{\{(PROJECT_ID|PROJECT_TITLE|CREATED_ON)\}\}",
                      lambda match: values[match.group(1)], text)
        path.write_text(text, encoding="utf-8")
    (target / "project.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target


def list_projects(root: Path) -> int:
    base = root / "projects"
    if not base.is_dir():
        print("ERROR: falta la carpeta projects", file=sys.stderr)
        return 1
    found = False
    errors = 0
    for directory in sorted(base.iterdir()):
        if not directory.is_dir() or directory.name == "_template":
            continue
        found = True
        try:
            data = read_metadata(directory)
            print(f"{data['id']} | {data['status']} | {data['title']}")
        except (OSError, ValueError) as exc:
            print(f"ERROR: {directory.name}: {exc}", file=sys.stderr)
            errors += 1
    if not found:
        print("Sin proyectos todavía. Usa el comando create para comenzar.")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create", help="Crear un proyecto desde la plantilla")
    create.add_argument("project_id")
    create.add_argument("--title", required=True)
    sub.add_parser("list", help="Listar proyectos y estados locales")
    args = parser.parse_args()
    try:
        if args.command == "list":
            return list_projects(ROOT)
        target = create_project(ROOT, args.project_id, args.title)
        print(f"Proyecto local creado: {target}")
        print("Siguiente paso: completar project.json, docs/design.md y docs/backlog.md.")
        return 0
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
