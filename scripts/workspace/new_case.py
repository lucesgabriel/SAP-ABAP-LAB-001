#!/usr/bin/env python
"""Generador de casos de práctica del SAP ABAP LAB 001.

Asigna un ID secuencial por dominio (ABAP-CASE-<DOMINIO>-<NNN>), crea la carpeta
aislada bajo cases/, copia las plantillas (cases/_template + docs estándar de
projects/_template) y consulta el knowledge-base para inyectar el histórico de la
capability del dominio. No contacta SAP. Solo biblioteca estándar.

Uso:
    python scripts/workspace/new_case.py --domain RAP --level intermedio --topic "Órdenes con draft"
    python scripts/workspace/new_case.py --domain OO --topic "Refactor report" --time 30 --package ZLAB_OO
    python scripts/workspace/new_case.py --domain CDS --topic "Vista equipos" --dry-run
"""
from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys
import unicodedata

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb  # noqa: E402

ROOT = kb.ROOT
VALID_LEVELS = ("basico", "intermedio", "avanzado", "examen")
RUBRIC_WEIGHTS = {"W_NAMES": 15, "W_FUNC": 35, "W_QUALITY": 20, "W_TEST": 10, "W_SEC": 10, "W_EVID": 10}
CASE_ID_RE = re.compile(r"^ABAP-CASE-(?P<domain>[A-Z]+)-(?P<num>\d{3})$")
CASE_FOLDER_RE = re.compile(r"^(?P<id>ABAP-CASE-(?P<domain>[A-Z]+)-(?P<num>\d{3}))-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$")

# Archivos propios del caso (desde cases/_template) y heredados del proyecto estándar.
CASE_FILES = (
    "README.md", "metadata.json", "00-case-brief/case-brief.md",
    "00-case-brief/historical-context.md", "rubric/checklist-100.md",
    "solution/expected-solution.md",
)
INHERITED_FILES = (
    "docs/design.md", "docs/backlog.md", "docs/journal.md", "docs/error-log.md",
    "docs/decision-log.md", "src/README.md", "tests/plan.md", "evidence/README.md",
    "evidence/completion.md", "transports/README.md",
)
ALL_CASE_FILES = CASE_FILES + INHERITED_FILES


def slugify(value: str) -> str:
    norm = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower()
    norm = re.sub(r"[^a-z0-9]+", "-", norm).strip("-")
    if not norm:
        raise ValueError(f"No se pudo generar un slug para '{value}'.")
    return norm[:60].rstrip("-")


def next_case_id(cases_dir: Path, domain: str) -> str:
    used = []
    if cases_dir.is_dir():
        for entry in cases_dir.iterdir():
            match = CASE_FOLDER_RE.match(entry.name)
            if entry.is_dir() and match and match.group("domain") == domain:
                used.append(int(match.group("num")))
    return f"{kb.CASE_PREFIX}-{domain}-{(max(used) + 1) if used else 1:03d}"


def read_case_metadata(directory: Path) -> dict:
    data = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    match = CASE_FOLDER_RE.match(directory.name)
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("metadata.json inválido o schema_version distinto de 1")
    if not match or data.get("id") != match.group("id"):
        raise ValueError("id del caso inválido o distinto del nombre de carpeta")
    if data.get("domain") not in kb.CASE_DOMAINS:
        raise ValueError("domain inválido")
    if data.get("capability") not in kb.CAPABILITIES:
        raise ValueError("capability inválida")
    if data.get("level") not in VALID_LEVELS:
        raise ValueError("level inválido")
    if data.get("status") not in {"planned", "active", "blocked", "completed", "archived"}:
        raise ValueError("status inválido")
    for field in ("resolved", "ready_to_consolidate"):
        if not isinstance(data.get(field), bool):
            raise ValueError(f"{field} debe ser true o false")
    try:
        date.fromisoformat(data.get("created_on", ""))
    except (TypeError, ValueError):
        raise ValueError("created_on debe ser una fecha ISO") from None
    return data


def render(text: str, values: dict) -> str:
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: str(values.get(m.group(1), m.group(0))), text)


def _insert_table_row(lines: list[str], row: str, header_marker: str) -> None:
    """Insert `row` after the last row of the first table whose header contains header_marker."""
    for i, line in enumerate(lines):
        if line.startswith("|") and header_marker in line:
            insert_at = i + 2  # skip the |---| separator
            while insert_at < len(lines) and lines[insert_at].startswith("|"):
                insert_at += 1
            lines.insert(insert_at, row)
            return
    lines.append(row)


def update_index(index_path: Path, case_id: str, title: str, domain: str, level: str,
                 time_min: int, folder_rel: str) -> None:
    lines = index_path.read_text(encoding="utf-8").splitlines()
    _insert_table_row(lines, f"| `{case_id}` | {title} | {domain} | {level} | {time_min} min | generado | `{folder_rel}` |",
                      "Case ID")
    num = int(case_id.rsplit("-", 1)[1])
    for i, line in enumerate(lines):
        if line.startswith(f"| {domain} | {kb.CASE_PREFIX}-{domain}-"):
            lines[i] = f"| {domain} | {kb.CASE_PREFIX}-{domain}-{num + 1:03d} |"
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def update_status(status_path: Path, case_id: str, title: str, domain: str) -> None:
    lines = status_path.read_text(encoding="utf-8").splitlines()
    _insert_table_row(lines, f"| `{case_id}` | {title} | {domain} | generado | si | No | No |", "Case ID")
    for i, line in enumerate(lines):
        if line.startswith("Última actualización:"):
            lines[i] = f"Última actualización: {date.today().isoformat()}"
    status_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def create_case(root: Path, *, domain: str, topic: str, level: str = "intermedio",
                time_min: int = 45, package: str = "$TMP", dry_run: bool = False) -> Path:
    if domain not in kb.CASE_DOMAINS:
        raise ValueError(f"Dominio inválido: {domain}. Válidos: {', '.join(kb.CASE_DOMAINS)}")
    if level not in VALID_LEVELS:
        raise ValueError(f"Nivel inválido: {level}")
    title = topic.strip()
    if not title or any(ord(c) < 32 for c in title):
        raise ValueError("El tema debe ser texto no vacío en una sola línea.")
    if time_min <= 0:
        raise ValueError("--time debe ser positivo")
    capability, domain_name = kb.CASE_DOMAINS[domain]
    cases_dir = root / "cases"
    template = cases_dir / "_template"
    project_template = root / "projects" / "_template"
    for relative in CASE_FILES:
        if not (template / relative).is_file():
            raise ValueError(f"Plantilla de caso incompleta: {relative}")
    for relative in INHERITED_FILES:
        if not (project_template / relative).is_file():
            raise ValueError(f"Plantilla de proyecto incompleta: {relative}")
    case_id = next_case_id(cases_dir, domain)
    slug = slugify(title)
    folder = cases_dir / f"{case_id}-{slug}"
    if folder.exists():
        raise ValueError(f"La carpeta ya existe: {folder}")
    today = date.today().isoformat()
    values = {
        "CASE_ID": case_id, "PROJECT_ID": case_id, "PROJECT_TITLE": title, "TITLE": title,
        "SLUG": slug, "DOMAIN": domain, "DOMAIN_NAME": domain_name, "CAPABILITY": capability,
        "LEVEL": level, "TIME_MIN": time_min, "PACKAGE": package, "DATE": today, "CREATED_ON": today,
        **RUBRIC_WEIGHTS,
    }
    if dry_run:
        print(f"[dry-run] Crearía {folder.relative_to(root)} (capability {capability})")
        for relative in ALL_CASE_FILES:
            print(f"[dry-run]   {relative}")
        return folder
    for relative in CASE_FILES:
        src = template / relative
        dst = folder / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        if relative == "00-case-brief/historical-context.md":
            text = kb.render_historical_context(src.read_text(encoding="utf-8"), ident=case_id,
                                                capability=capability, kb_dir=root / "knowledge-base")
        else:
            text = render(src.read_text(encoding="utf-8"), values)
        dst.write_text(text, encoding="utf-8")
    for relative in INHERITED_FILES:
        dst = folder / relative
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(render((project_template / relative).read_text(encoding="utf-8"), values),
                       encoding="utf-8")
    # Los docs heredados apuntan a rutas del proyecto; en un caso cambian el histórico y el metadato.
    design = folder / "docs" / "design.md"
    design.write_text(design.read_text(encoding="utf-8")
                      .replace("(historical-context.md)", "(../00-case-brief/historical-context.md)"),
                      encoding="utf-8")
    transports = folder / "transports" / "README.md"
    transports.write_text(transports.read_text(encoding="utf-8").replace("project.json", "metadata.json"),
                          encoding="utf-8")
    meta = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
    meta["time_min"] = time_min
    (folder / "metadata.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8")
    update_index(cases_dir / "_index.md", case_id, title, domain, level, time_min,
                 folder.relative_to(root).as_posix())
    update_status(cases_dir / "_status.md", case_id, title, domain)
    return folder


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--domain", required=True, choices=sorted(kb.CASE_DOMAINS))
    parser.add_argument("--topic", required=True, help="Título breve del caso.")
    parser.add_argument("--level", default="intermedio", choices=VALID_LEVELS)
    parser.add_argument("--time", type=int, default=45, help="Tiempo sugerido en minutos.")
    parser.add_argument("--package", default="$TMP", help="Paquete sugerido (verificar en SAP).")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        folder = create_case(ROOT, domain=args.domain, topic=args.topic, level=args.level,
                             time_min=args.time, package=args.package, dry_run=args.dry_run)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if not args.dry_run:
        print(f"Caso creado: {folder.relative_to(ROOT)}")
        print("Siguiente paso: redactar 00-case-brief/case-brief.md con prompts/04-generar-caso-practica.md "
              "y leer 00-case-brief/historical-context.md antes de diseñar.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
