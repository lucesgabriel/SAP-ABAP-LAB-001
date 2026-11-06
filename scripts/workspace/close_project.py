#!/usr/bin/env python
"""Cierra un proyecto o caso del laboratorio y promueve lecciones al knowledge-base global.

Lee `docs/error-log.md` y `docs/decision-log.md`, valida la taxonomía de cada fila,
asigna el siguiente código secuencial a las filas `YES`/`PARTIAL` no promovidas,
las escribe en `knowledge-base/error-catalog.md` / `decision-registry.md`, actualiza
`lessons-learned-index.md`, el estado del proyecto/caso y corre el linter antes y después.

  - --dry-run: reporta TODO lo que haría (incluidos los códigos que asignaría) sin escribir.
  - Recolecta inconsistencias y las reporta al final; no aborta en la primera.
  - No contacta SAP. Solo biblioteca estándar.

Uso:
  python scripts/workspace/close_project.py --project projects/abap-001-tema --dry-run
  python scripts/workspace/close_project.py --project projects/abap-001-tema
  python scripts/workspace/close_project.py --project cases/ABAP-CASE-RAP-001-tema

Exit codes: 0 cierre exitoso (o dry-run sin errores); 1 inconsistencias bloqueantes; 2 uso incorrecto.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import date
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb  # noqa: E402
import lint_knowledge_base as lint  # noqa: E402
from projects import read_metadata as read_project_metadata  # noqa: E402
from new_case import read_case_metadata  # noqa: E402

CAPABILITY_SECTIONS = {
    "OO": "OO - ABAP Objects y Clean ABAP", "CDS": "CDS - Core Data Services",
    "RAP": "RAP - RESTful ABAP Programming Model", "SQL": "SQL - ABAP SQL y AMDP",
    "DDIC": "DDIC - Diccionario", "ENH": "ENH - BAdI y extensibilidad",
    "API": "API - OData, HTTP y released APIs", "UI": "UI - Fiori Elements y UI5",
    "CTS": "CTS - Transportes y paquetes", "ATC": "ATC - Test Cockpit y Clean Core",
    "UNIT": "UNIT - ABAP Unit", "TOOL": "TOOL - ARC-1, ADT y clientes HTTP",
    "SEC": "SEC - Seguridad y secretos", "MULTI": "Multi-capability",
}
PLACEHOLDER_RE = re.compile(r"^_\(sin entradas consolidadas todavía[^\n]*\)_\n?", re.MULTILINE)
TEMPLATE_HEADING = "## Plantilla para nuevas entradas"
CHANGELOG_HEADING = "## Changelog"


@dataclass
class Row:
    raw: dict[str, str]
    line: int

    def get(self, *keys: str) -> str:
        for key in keys:
            for k, v in self.raw.items():
                if k.lower() == key.lower() and v.strip():
                    return v.strip()
        return ""

    @property
    def id(self) -> str:
        return self.get("ID")

    @property
    def reuse(self) -> str:
        value = self.get("Reutilizable").upper().replace("REUSE_", "")
        return value if value in {"YES", "PARTIAL", "NO"} else ""

    @property
    def promoted(self) -> str:
        value = self.get("Promovido (código KB)", "Promovido")
        return "" if value.lower().startswith(("(pendiente", "pendiente", "(")) else value.strip("`")

    def is_placeholder(self) -> bool:
        return self.get("Fecha") == "YYYY-MM-DD" or " / " in self.get("Capability")


@dataclass
class Report:
    issues: list[tuple[str, str]] = field(default_factory=list)

    def info(self, msg):
        self.issues.append(("INFO", msg))

    def warn(self, msg):
        self.issues.append(("WARN", msg))

    def error(self, msg):
        self.issues.append(("ERROR", msg))

    def has_errors(self):
        return any(level == "ERROR" for level, _ in self.issues)


# ---------------------------------------------------------------------------
# Parsing de logs
# ---------------------------------------------------------------------------

def parse_log_table(path: Path, report: Report) -> tuple[list[Row], list[str], int, list[str]]:
    """Devuelve (filas, líneas del archivo, índice de la fila header, nombres de columnas)."""
    if not path.is_file():
        report.error(f"No se encontró {path}")
        return [], [], -1, []
    lines = path.read_text(encoding="utf-8").splitlines()
    header_idx = next((i for i, l in enumerate(lines) if l.startswith("| ID |") or l.startswith("|ID|")), -1)
    if header_idx < 0:
        report.error(f"{path.name}: no se encontró la tabla maestra (header `| ID |`)")
        return [], lines, -1, []
    columns = [c.strip() for c in lines[header_idx].strip().strip("|").split("|")]
    rows: list[Row] = []
    for i in range(header_idx + 2, len(lines)):
        line = lines[i]
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != len(columns):
            report.warn(f"{path.name}:{i + 1}: fila con {len(cells)} columnas, se esperaban {len(columns)}; se ignora")
            continue
        row = Row(dict(zip(columns, cells)), i)
        if row.is_placeholder() or not row.id:
            continue
        rows.append(row)
    return rows, lines, header_idx, columns


def parse_details(text: str) -> dict[str, dict[str, str]]:
    """Secciones `### ER-XX | Título` con sus bullets `- **Campo:** valor`."""
    details: dict[str, dict[str, str]] = {}
    for match in re.finditer(r"^###\s+((?:ER|DC)-\d+)\s*\|\s*([^\n]+)\n(.*?)(?=^###\s|\Z)", text, re.M | re.S):
        fields = {"_title": match.group(2).strip()}
        for bullet in re.finditer(r"^- \*\*([^*]+):\*\*\s*(.*)$", match.group(3), re.M):
            fields[bullet.group(1).strip().lower()] = bullet.group(2).strip()
        details[match.group(1)] = fields
    return details


def validate_row(row: Row, path_name: str, report: Report, *, is_error: bool) -> bool:
    ok = True
    caps = {c.strip() for c in row.get("Capability").split(",") if c.strip()}
    if not caps or not caps <= kb.CAPABILITIES:
        report.error(f"{path_name} {row.id}: capability inválida '{row.get('Capability')}'")
        ok = False
    cats = {c.strip() for c in row.get("Categoría", "Categoria").split(",") if c.strip()}
    if not cats or not cats <= kb.CATEGORIES:
        report.error(f"{path_name} {row.id}: categoría inválida '{row.get('Categoría', 'Categoria')}'")
        ok = False
    if is_error:
        if row.get("Severidad") not in kb.SEVERITIES:
            report.error(f"{path_name} {row.id}: severidad inválida '{row.get('Severidad')}'")
            ok = False
        if row.get("Origen") not in kb.ORIGINS:
            report.error(f"{path_name} {row.id}: origen inválido '{row.get('Origen')}'")
            ok = False
    if not row.reuse:
        report.error(f"{path_name} {row.id}: Reutilizable debe ser YES / PARTIAL / NO")
        ok = False
    try:
        date.fromisoformat(row.get("Fecha"))
    except ValueError:
        report.warn(f"{path_name} {row.id}: fecha '{row.get('Fecha')}' no es ISO")
    return ok


# ---------------------------------------------------------------------------
# Render de entradas del KB
# ---------------------------------------------------------------------------

def capability_of(row: Row) -> str:
    caps = [c.strip() for c in row.get("Capability").split(",") if c.strip()]
    return caps[0] if len(caps) == 1 else "MULTI"


def render_error_entry(code: str, row: Row, detail: dict[str, str], origin_path: str) -> str:
    cap = capability_of(row)
    tags = f"{cap}, {row.get('Categoría', 'Categoria')}, {row.get('Severidad')}, REUSE_{row.reuse}, {row.get('Origen')}"
    title = detail.get("_title") or row.get("Síntoma", "Sintoma")[:90]
    return "\n".join([
        f"### {code} | {title}",
        "",
        f"**TAGS:** {tags}",
        "",
        f"- **Síntoma:** {detail.get('síntoma') or row.get('Síntoma', 'Sintoma')}",
        f"- **Causa raíz:** {detail.get('causa raíz') or row.get('Causa raíz', 'Causa raiz')}",
        f"- **Solución:** {detail.get('solución aplicada') or row.get('Solución aplicada', 'Solucion aplicada')}",
        f"- **Prevención:** {detail.get('prevención futura') or 'Pendiente de redactar.'}",
        f"- **Evidencia:** {detail.get('evidencia') or 'Ver ficha de cierre del proyecto.'}",
        f"- **Proyectos referenciados:** `{origin_path}` ({row.id}, {row.get('Fecha')}).",
        "",
    ])


def render_decision_entry(code: str, row: Row, detail: dict[str, str], origin_path: str) -> str:
    cap = capability_of(row)
    tags = f"{cap}, {row.get('Categoría', 'Categoria')}, REUSE_{row.reuse}"
    title = detail.get("_title") or row.get("Tema")
    return "\n".join([
        f"### {code} | {title}",
        "",
        f"**TAGS:** {tags}",
        "",
        f"- **Pregunta:** {detail.get('pregunta') or row.get('Tema')}",
        f"- **Decisión guía:** {detail.get('decisión') or row.get('Decisión', 'Decision')}",
        f"- **Alternativas evaluadas:** {row.get('Alternativas evaluadas') or 'Pendiente.'}",
        f"- **Motivo:** {detail.get('motivo') or row.get('Motivo') or 'Pendiente.'}",
        f"- **Impacto:** {row.get('Impacto') or detail.get('impacto técnico') or 'Pendiente.'}",
        f"- **Origen:** `{origin_path}` (decisión local {row.id}, {row.get('Fecha')}).",
        "",
    ])


def insert_error_entry(catalog: str, cap: str, entry: str) -> str:
    heading = f"## {CAPABILITY_SECTIONS[cap]}"
    if heading not in catalog:
        multi = f"## {CAPABILITY_SECTIONS['MULTI']}"
        catalog = catalog.replace(multi, f"{heading}\n\n{entry}\n---\n\n{multi}", 1)
        return catalog
    start = catalog.index(heading)
    end = catalog.find("\n---\n", start)
    if end < 0:
        end = catalog.find(f"\n{TEMPLATE_HEADING}", start)
    section = catalog[start:end]
    section = PLACEHOLDER_RE.sub("", section).rstrip("\n") + "\n\n" + entry
    return catalog[:start] + section + catalog[end:]


def insert_decision_entry(registry: str, entry: str) -> str:
    marker = f"---\n\n{TEMPLATE_HEADING}"
    if marker in registry:
        return registry.replace(marker, f"{entry}\n{marker}", 1)
    return registry.rstrip("\n") + "\n\n" + entry


def append_crossref(catalog: str, code: str, id_re: re.Pattern, origin_path: str, local_id: str, today: str) -> str:
    """Añade 'También visto en' a una entrada existente si el proyecto aún no está citado."""
    entries = kb.parse_entries(catalog, id_re)
    for i, entry in enumerate(entries):
        if entry["code"] != code:
            continue
        start = catalog.index(f"| {entry['title']}", catalog.index(f"{entry['code']} |"))
        next_start = len(catalog)
        if i + 1 < len(entries):
            next_start = catalog.index(f"{entries[i + 1]['code']} | {entries[i + 1]['title']}")
            next_start = catalog.rfind("\n#", 0, next_start)
        else:
            for stop in ("\n---\n", f"\n{TEMPLATE_HEADING}", f"\n{CHANGELOG_HEADING}"):
                pos = catalog.find(stop, start)
                if 0 <= pos < next_start:
                    next_start = pos
        block = catalog[start:next_start]
        if origin_path in block:
            return catalog
        block = block.rstrip("\n") + f"\n- **También visto en:** `{origin_path}` ({local_id}, {today}).\n"
        return catalog[:start] + block + catalog[next_start:]
    return catalog


def add_changelog(text: str, today: str, message: str) -> str:
    if CHANGELOG_HEADING not in text:
        return text.rstrip("\n") + f"\n\n{CHANGELOG_HEADING}\n\n| Fecha | Cambio |\n|---|---|\n| {today} | {message} |\n"
    idx = text.index(CHANGELOG_HEADING)
    sep = text.find("|---|---|", idx)
    if sep < 0:
        return text.rstrip("\n") + f"\n| {today} | {message} |\n"
    line_end = text.index("\n", sep)
    return text[:line_end + 1] + f"| {today} | {message} |\n" + text[line_end + 1:]


def update_promoted_column(lines: list[str], header_idx: int, columns: list[str], row: Row, code: str) -> None:
    cells = [c.strip() for c in lines[row.line].strip().strip("|").split("|")]
    col = next((i for i, c in enumerate(columns) if c.lower().startswith("promovido")), len(columns) - 1)
    cells[col] = f"`{code}`"
    lines[row.line] = "| " + " | ".join(cells) + " |"


# ---------------------------------------------------------------------------
# Cierre
# ---------------------------------------------------------------------------

def load_target(root: Path, project: str, report: Report) -> tuple[Path | None, str, dict]:
    target = (root / project).resolve()
    if not target.is_dir() or target.name == "_template":
        report.error(f"Proyecto o caso inexistente: {project}")
        return None, "", {}
    try:
        if target.parent == (root / "projects").resolve():
            return target, "project", read_project_metadata(target)
        if target.parent == (root / "cases").resolve():
            return target, "case", read_case_metadata(target)
    except (OSError, ValueError) as exc:
        report.error(f"Metadatos inválidos en {project}: {exc}")
        return None, "", {}
    report.error(f"{project} debe estar bajo projects/ o cases/")
    return None, "", {}


def close_project(root: Path, project: str, *, dry_run: bool, skip_lint: bool, force: bool) -> Report:
    report = Report()
    today = date.today().isoformat()
    target, kind, meta = load_target(root, project, report)
    if target is None:
        return report
    origin_path = target.relative_to(root).as_posix()
    kb_dir = root / "knowledge-base"

    if not meta.get("ready_to_consolidate") and not force:
        report.error("ready_to_consolidate es false; completa la ficha de cierre y marca true (o usa --force).")
    if kind == "case" and not meta.get("resolved") and not force:
        report.error("El caso no está marcado como resuelto (metadata.json → resolved).")
    completion = target / "evidence" / "completion.md"
    if not completion.is_file():
        report.error("Falta evidence/completion.md")
    elif "Estado de la entrega: pendiente" in completion.read_text(encoding="utf-8"):
        report.warn("evidence/completion.md sigue en 'pendiente'; el cierre solo documental es dudoso.")
    if meta.get("consolidated_on"):
        report.warn(f"Ya consolidado el {meta['consolidated_on']}; se volverán a revisar solo filas sin código.")

    if not skip_lint:
        before = lint.run_lint(root)
        if before.count("ERROR"):
            report.error(f"El linter del KB reporta {before.count('ERROR')} error(es) antes de escribir; corrige primero.")

    err_rows, err_lines, err_header, err_cols = parse_log_table(target / "docs" / "error-log.md", report)
    dec_rows, dec_lines, dec_header, dec_cols = parse_log_table(target / "docs" / "decision-log.md", report)
    err_details = parse_details((target / "docs" / "error-log.md").read_text(encoding="utf-8")) if err_lines else {}
    dec_details = parse_details((target / "docs" / "decision-log.md").read_text(encoding="utf-8")) if dec_lines else {}

    catalog = kb.read_kb("errors", kb_dir)
    registry = kb.read_kb("decisions", kb_dir)
    known_errors = {e["code"] for e in kb.parse_entries(catalog, kb.ERROR_ID_RE)}
    known_decisions = {e["code"] for e in kb.parse_entries(registry, kb.DECISION_ID_RE)}
    plan_errors: list[tuple[Row, str, bool]] = []  # (row, code, is_new)
    plan_decisions: list[tuple[Row, str, bool]] = []
    capabilities: set[str] = set()

    for row in err_rows:
        if not validate_row(row, "error-log.md", report, is_error=True):
            continue
        capabilities.update(c.strip() for c in row.get("Capability").split(","))
        if row.reuse == "NO":
            report.info(f"error-log {row.id}: REUSE_NO, no se promueve")
            continue
        if row.promoted:
            if row.promoted in known_errors:
                plan_errors.append((row, row.promoted, False))
            else:
                report.error(f"error-log {row.id}: Promovido cita {row.promoted} que no existe en el catálogo")
            continue
        code = kb.next_code(catalog, capability_of(row), kb.ERROR_ID_RE)
        catalog = insert_error_entry(catalog, capability_of(row),
                                     render_error_entry(code, row, err_details.get(row.id, {}), origin_path))
        plan_errors.append((row, code, True))

    for row in dec_rows:
        if not validate_row(row, "decision-log.md", report, is_error=False):
            continue
        capabilities.update(c.strip() for c in row.get("Capability").split(","))
        if row.reuse == "NO":
            report.info(f"decision-log {row.id}: REUSE_NO, no se promueve")
            continue
        if row.promoted:
            if row.promoted in known_decisions:
                plan_decisions.append((row, row.promoted, False))
            else:
                report.error(f"decision-log {row.id}: Promovido cita {row.promoted} que no existe en el registry")
            continue
        code = kb.next_code(registry, "D", kb.DECISION_ID_RE)
        registry = insert_decision_entry(registry, render_decision_entry(code, row, dec_details.get(row.id, {}), origin_path))
        plan_decisions.append((row, code, True))

    for row, code, is_new in plan_errors:
        report.info(f"error-log {row.id} → {'NUEVO ' if is_new else 'existente '}{code}")
    for row, code, is_new in plan_decisions:
        report.info(f"decision-log {row.id} → {'NUEVO ' if is_new else 'existente '}{code}")

    design = target / "docs" / "design.md"
    patterns_cited = sorted({m.group(0) for m in re.finditer(r"\bP-\d{3}\b", design.read_text(encoding="utf-8"))}
                            if design.is_file() else set())
    if not patterns_cited:
        report.warn("docs/design.md no cita ningún patrón P-XXX; si no aplica ninguno, debería justificarlo.")

    if report.has_errors():
        return report
    if dry_run:
        report.info("dry-run: no se escribió nada.")
        return report

    # --- Escritura -----------------------------------------------------------------
    new_err = [c for _, c, n in plan_errors if n]
    new_dec = [c for _, c, n in plan_decisions if n]
    for row, code, is_new in plan_errors:
        if not is_new:
            catalog = append_crossref(catalog, code, kb.ERROR_ID_RE, origin_path, row.id, today)
        update_promoted_column(err_lines, err_header, err_cols, row, code)
    for row, code, is_new in plan_decisions:
        if not is_new:
            registry = append_crossref(registry, code, kb.DECISION_ID_RE, origin_path, row.id, today)
        update_promoted_column(dec_lines, dec_header, dec_cols, row, code)
    if new_err:
        catalog = add_changelog(catalog, today, f"Promovidos {', '.join(new_err)} desde `{origin_path}`.")
    if new_dec:
        registry = add_changelog(registry, today, f"Promovidas {', '.join(new_dec)} desde `{origin_path}`.")
    (kb_dir / kb.KB_FILES["errors"]).write_text(catalog, encoding="utf-8")
    (kb_dir / kb.KB_FILES["decisions"]).write_text(registry, encoding="utf-8")
    if err_lines:
        (target / "docs" / "error-log.md").write_text("\n".join(err_lines) + "\n", encoding="utf-8")
    if dec_lines:
        (target / "docs" / "decision-log.md").write_text("\n".join(dec_lines) + "\n", encoding="utf-8")

    index_path = kb_dir / kb.KB_FILES["index"]
    index_lines = index_path.read_text(encoding="utf-8").splitlines()
    caps_text = ", ".join(sorted(capabilities)) or meta.get("capability", "MULTI")
    row = (f"| {kind} | {meta['id']} | {today} | {caps_text} | {len(new_err)} | {len(new_dec)} | "
           f"{len(patterns_cited)} | `{origin_path}` |")
    header = next(i for i, l in enumerate(index_lines) if l.startswith("| Tipo |"))
    insert_at = header + 2
    while insert_at < len(index_lines) and index_lines[insert_at].startswith("|"):
        insert_at += 1
    index_lines.insert(insert_at, row)
    index_text = add_changelog("\n".join(index_lines) + "\n", today,
                               f"Cerrado `{origin_path}`: {len(new_err)} errores y {len(new_dec)} decisiones promovidas.")
    index_path.write_text(index_text, encoding="utf-8")

    meta_file = target / ("project.json" if kind == "project" else "metadata.json")
    meta["status"] = "completed"
    meta["consolidated_on"] = today
    meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if kind == "case":
        status_path = root / "cases" / "_status.md"
        if status_path.is_file():
            lines = status_path.read_text(encoding="utf-8").splitlines()
            for i, line in enumerate(lines):
                if line.startswith(f"| `{meta['id']}` |"):
                    cells = [c.strip() for c in line.strip().strip("|").split("|")]
                    cells[-2], cells[-1] = "Si", "Si"
                    lines[i] = "| " + " | ".join(cells) + " |"
                if line.startswith("Última actualización:"):
                    lines[i] = f"Última actualización: {today}"
            status_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if not skip_lint:
        after = lint.run_lint(root)
        if after.count("ERROR"):
            report.error(f"El linter del KB reporta {after.count('ERROR')} error(es) DESPUÉS de escribir; revisa el diff.")
    report.info(f"Cierre completado: {len(new_err)} errores y {len(new_dec)} decisiones nuevas en el KB; "
                f"{meta_file.name} → completed ({today}).")
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--project", required=True, help="Ruta relativa: projects/<id> o cases/<CASE-ID>-<slug>")
    parser.add_argument("--root", default=str(kb.ROOT))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-lint", action="store_true")
    parser.add_argument("--force", action="store_true", help="Ignora ready_to_consolidate / resolved.")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"ERROR: raíz inexistente {root}", file=sys.stderr)
        return 2
    report = close_project(root, args.project, dry_run=args.dry_run, skip_lint=args.skip_lint, force=args.force)
    for level, msg in report.issues:
        print(f"[{level}] {msg}")
    return 1 if report.has_errors() else 0


if __name__ == "__main__":
    raise SystemExit(main())
