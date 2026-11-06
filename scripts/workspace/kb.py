#!/usr/bin/env python
"""Shared access to the knowledge-base: taxonomy, catalog parsing, next codes and context rendering.

Pure stdlib. Never contacts SAP. Used by projects.py, new_case.py, close_project.py and
lint_knowledge_base.py so that every tool reads the same files the same way.
"""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
KB_DIR = ROOT / "knowledge-base"

# --- Taxonomy (must match knowledge-base/taxonomy.md) ---------------------------------
CAPABILITIES = {"OO", "CDS", "RAP", "SQL", "DDIC", "ENH", "API", "UI", "CTS", "ATC", "UNIT",
                "TOOL", "SEC", "MULTI"}
CATEGORIES = {"SYNTAX", "ACTIVATION", "DEPENDENCY", "DATA_MODEL", "BEHAVIOR", "CLEAN_CORE",
              "PERFORMANCE", "AUTHORIZATION", "CONNECTIVITY", "TESTING", "TRANSPORT", "TOOLING",
              "NAMING", "OPERATIONS"}
SEVERITIES = {"BLOCKER", "MAJOR", "MINOR"}
REUSES = {"REUSE_YES", "REUSE_PARTIAL", "REUSE_NO"}
ORIGINS = {"DESIGN", "BUILD", "ACTIVATE", "TEST", "TRANSPORT", "PROD"}
ALL_TAGS = CAPABILITIES | CATEGORIES | SEVERITIES | REUSES | ORIGINS
# Tags treated as transversal when filtering decisions by capability: governance and
# tooling decisions apply to every project regardless of its capability.
TRANSVERSAL_CATEGORIES = {"OPERATIONS", "CLEAN_CORE", "TRANSPORT", "TOOL", "SEC"}

# Project id prefix -> capability used to filter the KB when injecting context.
PREFIX_TO_CAPABILITY = {
    "abap": "OO", "oo": "OO", "clean": "OO",
    "cds": "CDS",
    "rap": "RAP",
    "sql": "SQL", "amdp": "SQL",
    "ddic": "DDIC",
    "enh": "ENH", "badi": "ENH",
    "api": "API", "odata": "API", "http": "API",
    "ui": "UI", "fiori": "UI", "ui5": "UI",
    "cts": "CTS", "git": "CTS",
    "atc": "ATC",
    "unit": "UNIT", "test": "UNIT",
    "tool": "TOOL", "arc1": "TOOL",
    "sec": "SEC", "auth": "SEC",
    "mix": "MULTI",
}

# Practice-case domain -> (capability, human name)
CASE_DOMAINS = {
    "OO":  ("OO",    "ABAP Objects y Clean ABAP"),
    "CDS": ("CDS",   "Core Data Services"),
    "RAP": ("RAP",   "RESTful ABAP Programming Model"),
    "SQL": ("SQL",   "ABAP SQL y AMDP"),
    "ENH": ("ENH",   "BAdI y extensibilidad"),
    "API": ("API",   "OData, HTTP y released APIs"),
    "UI":  ("UI",    "Fiori Elements y UI5"),
    "MIX": ("MULTI", "Caso integrador multi-capability"),
}
CASE_PREFIX = "ABAP-CASE"

KB_FILES = {
    "taxonomy": "taxonomy.md",
    "errors": "error-catalog.md",
    "patterns": "solution-patterns.md",
    "decisions": "decision-registry.md",
    "recipes": "released-api-recipes.md",
    "index": "lessons-learned-index.md",
}

ERROR_ID_RE = re.compile(r"^###\s+(?P<code>(?:%s)-\d{3})\s*\|\s*(?P<title>[^\n]+)$"
                         % "|".join(sorted(CAPABILITIES)), re.MULTILINE)
PATTERN_ID_RE = re.compile(r"^##\s+(?P<code>P-\d{3})\s*\|\s*(?P<title>[^\n]+)$", re.MULTILINE)
DECISION_ID_RE = re.compile(r"^###\s+(?P<code>D-\d{3})\s*\|\s*(?P<title>[^\n]+)$", re.MULTILINE)
RECIPE_ID_RE = re.compile(r"^##\s+(?P<code>R-\d{3})\s*\|\s*(?P<title>[^\n]+)$", re.MULTILINE)
TAGS_LINE_RE = re.compile(r"^\*\*TAGS:\*\*\s*(?P<tags>.+?)\s*$", re.MULTILINE)
CROSSREF_RE = re.compile(r"\b(?:%s|P|D|R)-\d{3}\b" % "|".join(sorted(CAPABILITIES)))


def read_kb(name: str, kb_dir: Path = KB_DIR) -> str:
    path = kb_dir / KB_FILES[name]
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def parse_tags(line: str) -> list[str]:
    return [t.strip() for t in line.split(",") if t.strip()]


def parse_entries(text: str, id_re: re.Pattern) -> list[dict]:
    """Return [{code, title, tags, line}] for each heading matched by id_re.

    The TAGS line is the first `**TAGS:**` after the heading and before the next heading.
    Fenced code blocks (templates) are ignored so examples do not count as entries.
    """
    text = strip_fenced_code(text)
    entries = []
    matches = list(id_re.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[match.end():end]
        tags_match = TAGS_LINE_RE.search(body)
        tags = parse_tags(tags_match.group("tags")) if tags_match else []
        entries.append({
            "code": match.group("code"),
            "title": match.group("title").strip(),
            "tags": tags,
            "line": text.count("\n", 0, match.start()) + 1,
        })
    return entries


def _matches(entry: dict, capability: str, *, transversal: bool = False) -> bool:
    tags = set(entry["tags"])
    if capability == "MULTI":
        return True
    if capability in tags or "MULTI" in tags:
        return True
    return transversal and bool(tags & TRANSVERSAL_CATEGORIES)


def load_errors(capability: str, kb_dir: Path = KB_DIR) -> list[dict]:
    return [e for e in parse_entries(read_kb("errors", kb_dir), ERROR_ID_RE) if _matches(e, capability)]


def load_patterns(capability: str, kb_dir: Path = KB_DIR) -> list[dict]:
    return [e for e in parse_entries(read_kb("patterns", kb_dir), PATTERN_ID_RE) if _matches(e, capability)]


def load_decisions(capability: str, kb_dir: Path = KB_DIR) -> list[dict]:
    return [e for e in parse_entries(read_kb("decisions", kb_dir), DECISION_ID_RE)
            if _matches(e, capability, transversal=True)]


def load_recipes(capability: str, kb_dir: Path = KB_DIR) -> list[dict]:
    return [e for e in parse_entries(read_kb("recipes", kb_dir), RECIPE_ID_RE) if _matches(e, capability)]


def load_similar(capability: str, kb_dir: Path = KB_DIR) -> list[str]:
    rows = []
    for line in read_kb("index", kb_dir).splitlines():
        if not line.startswith("|") or "---" in line or line.startswith("| Tipo"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 8:
            continue
        caps = {c.strip() for c in cells[3].split(",")}
        if capability == "MULTI" or capability in caps:
            rows.append(f"- `{cells[1]}` (cerrado {cells[2]}, capabilities {cells[3]}) → {cells[7]}")
    return rows


def next_code(text: str, prefix: str, id_re: re.Pattern) -> str:
    """Next sequential code for `prefix` (e.g. 'OO' or 'D') given the catalog text."""
    used = [int(e["code"].rsplit("-", 1)[1]) for e in parse_entries(text, id_re)
            if e["code"].rsplit("-", 1)[0] == prefix]
    return f"{prefix}-{(max(used) + 1) if used else 1:03d}"


def capability_for_project_id(project_id: str) -> str:
    prefix = project_id.split("-", 1)[0].lower()
    return PREFIX_TO_CAPABILITY.get(prefix, "MULTI")


def render_historical_context(template_text: str, *, ident: str, capability: str,
                              kb_dir: Path = KB_DIR) -> str:
    def fmt(items: list[dict]) -> str:
        if not items:
            return "_(ninguno consolidado aún para esta capability)_"
        return "\n".join(f"- `{e['code']}` — {e['title']}" for e in items)

    patterns = load_patterns(capability, kb_dir)
    if patterns:
        base = patterns[0]
        pattern_text = f"**Base sugerido:** `{base['code']}` — {base['title']}"
        if len(patterns) > 1:
            pattern_text += "\n\n**Complementarios:**\n" + "\n".join(
                f"- `{p['code']}` — {p['title']}" for p in patterns[1:])
    else:
        pattern_text = "_(no hay patrón consolidado; documentar en docs/design.md si surge uno nuevo)_"
    similar = load_similar(capability, kb_dir)
    values = {
        "PROJECT_ID": ident, "CASE_ID": ident, "CAPABILITY": capability,
        "PATTERN_BASE": pattern_text,
        "KNOWN_ERRORS": fmt(load_errors(capability, kb_dir)),
        "REUSABLE_DECISIONS": fmt(load_decisions(capability, kb_dir)),
        "RECIPES": fmt(load_recipes(capability, kb_dir)),
        "SIMILAR_PROJECTS": "\n".join(similar) if similar else
                            "_(no hay proyectos cerrados similares en lessons-learned-index todavía)_",
    }
    return re.sub(r"\{\{([A-Z_]+)\}\}", lambda m: values.get(m.group(1), m.group(0)), template_text)
