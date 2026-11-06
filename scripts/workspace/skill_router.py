#!/usr/bin/env python
"""Ruteo automático de skills y libros para cada sesión y cada mensaje del usuario.

Lo invocan los hooks de ``.claude/settings.json``:

* ``session-start``: imprime el mapa fase → skill, el estado de la biblioteca y los comandos.
* ``prompt``: lee el JSON del hook ``UserPromptSubmit`` por stdin, detecta el dominio por palabras
  clave (``config/skills-routing.json``) y devuelve como contexto las skills a cargar, los códigos
  del KB y los capítulos de libro recomendados. Si no detecta nada, no imprime nada.

También sirve fuera de Claude (Hermes, Codex) para consultar a mano:

    python scripts/workspace/skill_router.py suggest "crear un BO RAP con draft y validaciones"

Nunca falla el hook: ante cualquier error sale con código 0 y sin salida.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from books import books_root, chapters_for_routes, format_chapter, index_dir, load_catalog  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
ROUTING = Path("config/skills-routing.json")


def load_routing(root: Path = ROOT) -> dict:
    return json.loads((root / ROUTING).read_text(encoding="utf-8"))


def _pattern(keyword: str) -> re.Pattern[str]:
    escaped = re.escape(keyword.lower())
    left = r"(?<![\w])" if re.match(r"\w", keyword) else ""
    right = r"(?![\w])" if re.search(r"\w$", keyword) else ""
    return re.compile(left + escaped + right)


def match_routes(text: str, routing: dict) -> list[tuple[dict, list[str]]]:
    """Rutas que coinciden con el texto, ordenadas por número de palabras clave distintas."""
    low = text.lower()
    scored = []
    for order, route in enumerate(routing["routes"]):
        hits = [kw for kw in route["keywords"] if _pattern(kw).search(low)]
        if hits:
            scored.append((-len(hits), order, route, hits))
    scored.sort(key=lambda item: (item[0], item[1]))
    limit = routing.get("max_routes_per_prompt", 3)
    return [(route, hits) for _, _, route, hits in scored[:limit]]


SYSTEM_MARKERS = ("<task-notification>", "[SYSTEM NOTIFICATION", "<system-reminder>", "<side-sessions-event>",
                  "<ci-monitor-event>")


# Comandos y eventos de la app que llegan envueltos en una etiqueta propia, p. ej.
# <create-pr-command>, <commit-command>, <side-sessions-event>, <task-notification>.
APP_TAG = re.compile(r"^<[a-z][a-z0-9-]*-(?:command|event|notification)\b")


def is_system_message(text: str) -> bool:
    """Eventos y comandos automáticos de la app; no son peticiones redactadas por el usuario."""
    head = text.lstrip()[:200]
    return bool(APP_TAG.match(head)) or any(marker in head for marker in SYSTEM_MARKERS)


def suggest(text: str, root: Path = ROOT) -> str:
    if is_system_message(text):
        return ""
    routing = load_routing(root)
    matches = match_routes(text, routing)
    if not matches:
        return ""
    skills: list[str] = []
    kb: list[str] = []
    for route, _ in matches:
        for skill in route["skills"]:
            if skill not in skills:
                skills.append(skill)
        for code in route.get("kb", []):
            if code not in kb:
                kb.append(code)
    lines = [
        "[SAP-ABAP-LAB-001 · skill-router]",
        "Dominio detectado: " + "; ".join(f"{r['label']} ({', '.join(h[:3])})" for r, h in matches),
        "Antes de diseñar o escribir código, carga con la herramienta Skill (en este orden, solo las "
        "pertinentes): " + ", ".join(f"`{s}`" for s in skills[:6]) + ".",
    ]
    if kb:
        lines.append("Consulta en knowledge-base/ y checklists/: " + ", ".join(f"`{c}`" for c in kb) + ".")
    try:
        catalog = load_catalog(root)
        chapters = chapters_for_routes(catalog, [r["id"] for r, _ in matches],
                                       limit=routing.get("max_book_refs", 4))
        if chapters:
            lines.append("Libros de referencia (cita slug + capítulo + página; no copies texto): "
                         + "; ".join(format_chapter(ch) for ch in chapters) + ".")
            if index_dir(catalog, root).is_dir():
                lines.append("Para buscar en ellos: `python scripts/workspace/books.py search \"<término>\" "
                             f"--route {matches[0][0]['id']}`.")
    except (OSError, ValueError, KeyError):
        pass
    lines.append("La skill propone; lo que cuenta es lo leído y activado en SAP con ARC-1 (flujo P-002).")
    return "\n".join(lines)


def session_banner(root: Path = ROOT) -> str:
    routing = load_routing(root)
    lines = [
        "[SAP-ABAP-LAB-001 · arranque] Lee AGENTS.md y aplica el flujo P-002. Confirma ARC-1 con una "
        "lectura no destructiva (TOOL-003) antes de afirmar conexión.",
        "Skills por fase (cárgalas con la herramienta Skill al entrar en cada fase):",
    ]
    lines += [f"- {p['phase']}: " + ", ".join(f"`{s}`" for s in p["skills"]) for p in routing["phases"]]
    lines.append("Skills por dominio (el hook UserPromptSubmit las sugiere en cada mensaje): "
                 + "; ".join(f"{r['id']}→`{r['skills'][0]}`" for r in routing["routes"]) + ".")
    skip = routing.get("do_not_load_by_default", {})
    if skip:
        lines.append("No cargar por defecto: " + ", ".join(f"`{k}`" for k in skip) + " (ver AGENTS.md).")
    try:
        catalog = load_catalog(root)
        source = books_root(catalog, root)
        indexed = index_dir(catalog, root).is_dir()
        state = "disponible" if source.is_dir() else "NO encontrada"
        lines.append(f"Biblioteca de referencia {state} ({len(catalog['books'])} libros, "
                     f"{'indexada' if indexed else 'sin índice: python scripts/workspace/books.py index'}). "
                     "Catálogo: docs/guides/reference-library.md.")
    except (OSError, ValueError, KeyError):
        pass
    return "\n".join(lines)


def _read_prompt_from_stdin() -> str:
    raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
    if not raw.strip():
        return ""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return raw
    return str(payload.get("prompt", "")) if isinstance(payload, dict) else ""


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    mode = args[0] if args else "session-start"
    try:
        if mode == "session-start":
            output = session_banner()
        elif mode == "prompt":
            prompt = _read_prompt_from_stdin()
            output = suggest(prompt) if len(prompt.strip()) >= 3 else ""
        elif mode == "suggest":
            output = suggest(" ".join(args[1:])) or "Sin dominio detectado."
        else:
            print(f"Modo desconocido: {mode}", file=sys.stderr)
            return 2
    except Exception:  # noqa: BLE001 - un hook nunca debe bloquear al usuario
        return 0
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
