#!/usr/bin/env python
"""Linter del knowledge-base y de los IDs de casos de práctica.

Valida:
  - tags de cada entrada contra la taxonomía (capability, categoría, severidad, reutilizable, origen);
  - IDs únicos y secuenciales por catálogo / capability;
  - patrones de secretos pegados accidentalmente (KB, projects/, cases/);
  - referencias cruzadas a códigos inexistentes;
  - carpetas de cases/ con ID válido, único, secuencial y metadata coherente.

Uso:
    python scripts/workspace/lint_knowledge_base.py
    python scripts/workspace/lint_knowledge_base.py --strict      # warnings también fallan
    python scripts/workspace/lint_knowledge_base.py --root <otra raíz>

Exit codes: 0 OK, 1 errores (o warnings con --strict), 2 uso incorrecto.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb  # noqa: E402

SECRET_PATTERNS = [
    re.compile(r"(?i)\b(password|passwd|pwd|contrase[nñ]a)\s*[:=]\s*\S{4,}"),
    re.compile(r"(?i)\b(client[_-]?secret|api[_-]?key|access[_-]?token|bearer)\s*[:=]\s*[A-Za-z0-9._\-]{12,}"),
    re.compile(r"\bSAP_SESSIONID_[A-Z0-9]+_\d{3}=[A-Za-z0-9%_\-]{20,}"),
    re.compile(r"\bMYSAPSSO2=[A-Za-z0-9%_\-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----"),
]
SECRET_ALLOWLIST = ("<TU_", "placeholder", "ejemplo", "example", "nunca", "never", "{{", "alias",
                    "SAP_SESSIONID_<SID>", "SAP_SESSIONID_*", "SAP_SESSIONID_S4H_100=...")
SKIP_DIRS = {".git", "artifacts", "__pycache__", ".venv", "node_modules", ".pytest_cache", "logs"}


@dataclass
class Issue:
    level: str
    path: str
    line: int
    message: str


@dataclass
class Report:
    issues: list[Issue] = field(default_factory=list)

    def error(self, path, line, msg):
        self.issues.append(Issue("ERROR", path, line, msg))

    def warn(self, path, line, msg):
        self.issues.append(Issue("WARN", path, line, msg))

    def count(self, level):
        return sum(1 for i in self.issues if i.level == level)


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def check_tags(entries: list[dict], path: str, report: Report, *, require_severity: bool,
               require_origin: bool) -> None:
    for entry in entries:
        tags = entry["tags"]
        if not tags:
            report.error(path, entry["line"], f"{entry['code']}: falta la línea **TAGS:**")
            continue
        unknown = [t for t in tags if t not in kb.ALL_TAGS]
        if unknown:
            report.error(path, entry["line"], f"{entry['code']}: tags fuera de taxonomía: {', '.join(unknown)}")
        tagset = set(tags)
        if not tagset & kb.CAPABILITIES:
            report.error(path, entry["line"], f"{entry['code']}: falta capability")
        if not tagset & kb.CATEGORIES:
            report.error(path, entry["line"], f"{entry['code']}: falta categoría")
        if require_severity and not tagset & kb.SEVERITIES:
            report.error(path, entry["line"], f"{entry['code']}: falta severidad")
        if not tagset & kb.REUSES:
            report.error(path, entry["line"], f"{entry['code']}: falta REUSE_*")
        if "REUSE_NO" in tagset:
            report.warn(path, entry["line"], f"{entry['code']}: REUSE_NO no debería estar en el KB global")
        if require_origin and not tagset & kb.ORIGINS:
            report.error(path, entry["line"], f"{entry['code']}: falta origen")
        if "MULTI" in tagset and len(tagset & kb.CAPABILITIES) > 1:
            report.warn(path, entry["line"], f"{entry['code']}: MULTI combinado con otra capability")


def check_ids(entries: list[dict], path: str, report: Report, *, per_prefix: bool) -> None:
    seen: dict[str, int] = {}
    groups: dict[str, list[int]] = {}
    for entry in entries:
        code = entry["code"]
        if code in seen:
            report.error(path, entry["line"], f"ID duplicado {code} (ya en línea {seen[code]})")
        seen[code] = entry["line"]
        prefix, num = code.rsplit("-", 1)
        groups.setdefault(prefix if per_prefix else "ALL", []).append(int(num))
    for prefix, nums in groups.items():
        expected = list(range(1, len(nums) + 1))
        if sorted(nums) != expected:
            missing = sorted(set(expected) - set(nums))
            report.warn(path, 0, f"IDs no secuenciales para {prefix}: faltan {missing or 'n/a'}; "
                                 f"máximo {max(nums):03d} con {len(nums)} entradas")


def check_secrets(path: Path, text: str, root: Path, report: Report) -> None:
    for pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            snippet = text[max(0, match.start() - 40): match.end() + 40]
            if any(a.lower() in snippet.lower() for a in SECRET_ALLOWLIST):
                continue
            line = text.count("\n", 0, match.start()) + 1
            report.error(rel(path, root), line, f"posible secreto: '{match.group(0)[:40]}...'")


def check_crossrefs(text: str, path: str, known: set[str], report: Report) -> None:
    for match in kb.CROSSREF_RE.finditer(kb.strip_fenced_code(text)):
        code = match.group(0)
        if code not in known:
            line = text.count("\n", 0, match.start()) + 1
            report.warn(path, line, f"referencia a código inexistente {code}")


def check_cases(cases_dir: Path, root: Path, report: Report) -> None:
    if not cases_dir.is_dir():
        return
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from new_case import CASE_FOLDER_RE, read_case_metadata  # noqa: E402
    by_domain: dict[str, list[int]] = {}
    for entry in sorted(cases_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("_"):
            continue
        match = CASE_FOLDER_RE.match(entry.name)
        path = rel(entry, root)
        if not match:
            report.error(path, 0, "nombre de carpeta de caso inválido (ABAP-CASE-<DOM>-<NNN>-<slug>)")
            continue
        if match.group("domain") not in kb.CASE_DOMAINS:
            report.error(path, 0, f"dominio desconocido {match.group('domain')}")
        by_domain.setdefault(match.group("domain"), []).append(int(match.group("num")))
        try:
            meta = read_case_metadata(entry)
            if meta["capability"] != kb.CASE_DOMAINS.get(meta["domain"], ("?",))[0]:
                report.warn(path, 0, "capability de metadata.json no coincide con el dominio")
        except (OSError, ValueError) as exc:
            report.error(path, 0, f"metadata.json: {exc}")
        for relative in ("README.md", "00-case-brief/case-brief.md", "00-case-brief/historical-context.md",
                         "docs/error-log.md", "docs/decision-log.md", "evidence/completion.md"):
            if not (entry / relative).is_file():
                report.error(path, 0, f"falta {relative}")
    for domain, nums in by_domain.items():
        dup = {n for n in nums if nums.count(n) > 1}
        if dup:
            report.error(rel(cases_dir, root), 0, f"IDs duplicados en {domain}: {sorted(dup)}")
        if sorted(set(nums)) != list(range(1, max(nums) + 1)):
            report.warn(rel(cases_dir, root), 0, f"IDs no secuenciales en {domain}: {sorted(nums)}")


def run_lint(root: Path) -> Report:
    report = Report()
    kb_dir = root / "knowledge-base"
    if not kb_dir.is_dir():
        report.error("knowledge-base", 0, "no existe la carpeta knowledge-base/")
        return report
    catalogs = {
        "errors": (kb.ERROR_ID_RE, True, True, True),
        "patterns": (kb.PATTERN_ID_RE, False, False, False),
        "decisions": (kb.DECISION_ID_RE, False, False, False),
        "recipes": (kb.RECIPE_ID_RE, False, False, False),
    }
    known: set[str] = set()
    texts: dict[str, str] = {}
    for name, (id_re, per_prefix, sev, origin) in catalogs.items():
        path = kb_dir / kb.KB_FILES[name]
        if not path.is_file():
            report.error(rel(path, root), 0, "archivo del KB faltante")
            continue
        text = path.read_text(encoding="utf-8")
        texts[name] = text
        entries = kb.parse_entries(text, id_re)
        check_tags(entries, rel(path, root), report, require_severity=sev, require_origin=origin)
        check_ids(entries, rel(path, root), report, per_prefix=per_prefix)
        known.update(e["code"] for e in entries)
    for name in ("taxonomy", "index"):
        path = kb_dir / kb.KB_FILES[name]
        if not path.is_file():
            report.error(rel(path, root), 0, "archivo del KB faltante")
    for name, text in texts.items():
        check_crossrefs(text, rel(kb_dir / kb.KB_FILES[name], root), known, report)
    # Secretos en KB, proyectos y casos (Markdown, JSON, ABAP, texto).
    for base in (kb_dir, root / "projects", root / "cases"):
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".md", ".json", ".abap", ".txt", ".yaml", ".yml"}:
                continue
            if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
                continue
            try:
                check_secrets(path, path.read_text(encoding="utf-8"), root, report)
            except UnicodeDecodeError:
                report.warn(rel(path, root), 0, "no se pudo leer como UTF-8")
    check_cases(root / "cases", root, report)
    return report


def render(report: Report) -> str:
    lines = []
    for issue in sorted(report.issues, key=lambda i: (i.level != "ERROR", i.path, i.line)):
        where = f"{issue.path}:{issue.line}" if issue.line else issue.path
        lines.append(f"[{issue.level}] {where} — {issue.message}")
    errors, warns = report.count("ERROR"), report.count("WARN")
    lines.append(f"Knowledge-base: {'FAIL' if errors else 'OK'} | {errors} error(es) | {warns} warning(s)")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=str(kb.ROOT), help="Raíz del laboratorio.")
    parser.add_argument("--strict", action="store_true", help="Los warnings también hacen fallar.")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"ERROR: raíz inexistente {root}", file=sys.stderr)
        return 2
    report = run_lint(root)
    print(render(report))
    if report.count("ERROR") or (args.strict and report.count("WARN")):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
