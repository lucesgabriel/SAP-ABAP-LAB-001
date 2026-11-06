#!/usr/bin/env python
"""Biblioteca local de referencia (libros SAP PRESS y apuntes) para el laboratorio.

Los libros viven fuera del repositorio (por defecto ``../books``; se puede cambiar con la
variable ``SAP_LAB_BOOKS_ROOT``). El catálogo con capítulos, páginas y rutas de skill está en
``config/books.json``. El índice de texto se genera en ``artifacts/books-index/`` (ignorado por
git) y nunca se versiona: los libros tienen copyright, solo se citan libro, capítulo y página.

Uso:
    python scripts/workspace/books.py list
    python scripts/workspace/books.py chapters --route rap
    python scripts/workspace/books.py index [--book rap-2025] [--force]
    python scripts/workspace/books.py search "behavior definition" "draft" [--route rap] [--book rap-2025]
    python scripts/workspace/books.py render [--output docs/guides/reference-library.md]

Solo usa la biblioteca estándar. Para extraer PDF usa ``pdftotext`` (Git for Windows lo trae en
``mingw64/bin``) y, si no existe, ``pypdf`` cuando esté instalado.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
CATALOG = Path("config/books.json")
PDFTOTEXT_CANDIDATES = (
    r"C:\Program Files\Git\mingw64\bin\pdftotext.exe",
    r"C:\Program Files (x86)\Git\mingw64\bin\pdftotext.exe",
)


def load_catalog(root: Path = ROOT) -> dict:
    return json.loads((root / CATALOG).read_text(encoding="utf-8"))


def books_root(catalog: dict, root: Path = ROOT) -> Path:
    env = os.environ.get(catalog.get("root_env", "SAP_LAB_BOOKS_ROOT"))
    if env:
        return Path(env)
    return (root / catalog.get("default_root", "../books")).resolve()


def index_dir(catalog: dict, root: Path = ROOT) -> Path:
    return root / catalog.get("index_dir", "artifacts/books-index")


def _all_chapters(catalog: dict) -> list[dict]:
    chapters = []
    for book_order, book in enumerate(catalog["books"]):
        for index, chapter in enumerate(book.get("chapters", [])):
            chapters.append({"slug": book["slug"], "book_title": book["title"],
                             "_order": (book_order, index), **chapter})
    return chapters


def chapters_for_routes(catalog: dict, route_ids: list[str], limit: int | None = None) -> list[dict]:
    """Capítulos de las rutas dadas.

    Sin ``limit``: todos los capítulos que tocan alguna ruta, primero los de ruta principal.
    Con ``limit``: selección en ronda entre rutas (cada ruta aporta su mejor capítulo por turno),
    prefiriendo capítulos ``key``, ruta principal y libros aún no citados.
    """
    chapters = _all_chapters(catalog)
    if limit is None:
        rank = {route: position for position, route in enumerate(route_ids)}
        hits = [ch for ch in chapters if any(r in rank for r in ch.get("routes", []))]
        hits.sort(key=lambda ch: (ch["routes"][0] not in rank, ch["_order"]))
        return hits
    pools = {}
    for route in route_ids:
        primary = [ch for ch in chapters if ch.get("routes", [None])[0] == route]
        pools[route] = primary or [ch for ch in chapters if route in ch.get("routes", [])]
    picked: list[dict] = []
    used_books: set[str] = set()
    progress = True
    while len(picked) < limit and progress:
        progress = False
        for route in route_ids:
            candidates = [ch for ch in pools[route] if ch not in picked]
            if not candidates or len(picked) >= limit:
                continue
            candidates.sort(key=lambda ch: (not ch.get("key", False), ch["slug"] in used_books, ch["_order"]))
            choice = candidates[0]
            picked.append(choice)
            used_books.add(choice["slug"])
            progress = True
    return picked


def format_chapter(chapter: dict) -> str:
    where = f" (p.{chapter['page']})" if chapter.get("page") else ""
    label = "libro completo" if chapter["n"] == "*" else f"cap.{chapter['n']}"
    title = "" if chapter["n"] == "*" else f" {chapter['title']}"
    return f"`{chapter['slug']}` {label}{title}{where}"


def find_pdftotext() -> str | None:
    found = shutil.which("pdftotext")
    if found:
        return found
    for candidate in PDFTOTEXT_CANDIDATES:
        if Path(candidate).is_file():
            return candidate
    return None


def extract_text(pdf: Path) -> str:
    tool = find_pdftotext()
    if tool:
        completed = subprocess.run([tool, "-enc", "UTF-8", "-q", str(pdf), "-"],
                                   capture_output=True, check=False)
        if completed.returncode == 0 and completed.stdout:
            return completed.stdout.decode("utf-8", errors="replace")
    try:
        import pypdf  # type: ignore[import-not-found]
    except ImportError as exc:
        raise RuntimeError("No hay pdftotext ni pypdf para extraer texto del PDF") from exc
    reader = pypdf.PdfReader(str(pdf))
    return "\f".join((page.extract_text() or "") for page in reader.pages)


def build_index(catalog: dict, root: Path = ROOT, only: str | None = None, force: bool = False) -> list[str]:
    source_root = books_root(catalog, root)
    target_dir = index_dir(catalog, root)
    target_dir.mkdir(parents=True, exist_ok=True)
    report = []
    for book in catalog["books"]:
        if only and book["slug"] != only:
            continue
        target = target_dir / f"{book['slug']}.txt"
        if target.exists() and not force:
            report.append(f"= {book['slug']}: ya indexado")
            continue
        txt = source_root / book["txt"] if book.get("txt") else None
        pdf = source_root / book["pdf"]
        try:
            if txt and txt.is_file():
                text = txt.read_text(encoding="utf-8", errors="replace")
            elif pdf.is_file():
                text = extract_text(pdf)
            else:
                report.append(f"! {book['slug']}: no se encontró {pdf}")
                continue
        except RuntimeError as exc:
            report.append(f"! {book['slug']}: {exc}")
            continue
        target.write_text(text, encoding="utf-8")
        report.append(f"+ {book['slug']}: {text.count(chr(12)) + 1} páginas")
    return report


def search(catalog: dict, terms: list[str], root: Path = ROOT, book: str | None = None,
           route: str | None = None, limit: int = 10, context: int = 160) -> list[str]:
    folder = index_dir(catalog, root)
    lowered = [term.lower() for term in terms if term.strip()]
    if not lowered:
        return []
    selected = []
    for entry in catalog["books"]:
        if book and entry["slug"] != book:
            continue
        if route and not any(route in ch.get("routes", []) for ch in entry.get("chapters", [])):
            continue
        selected.append(entry)
    results = []
    for entry in selected:
        path = folder / f"{entry['slug']}.txt"
        if not path.is_file():
            continue
        pages = path.read_text(encoding="utf-8", errors="replace").split("\f")
        for number, page in enumerate(pages, start=1):
            low = page.lower()
            if not all(term in low for term in lowered):
                continue
            at = low.find(lowered[0])
            start, end = max(0, at - context // 2), min(len(page), at + len(lowered[0]) + context // 2)
            snippet = re.sub(r"\s+", " ", page[start:end]).strip()
            results.append(f"{entry['slug']} p.{number}: …{snippet}…")
            if len(results) >= limit:
                return results
    return results


def render_markdown(catalog: dict, routing: dict | None = None) -> str:
    labels = {r["id"]: r["label"] for r in (routing or {}).get("routes", [])}
    lines = [
        "# Biblioteca de referencia",
        "",
        "> Generado con `python scripts/workspace/books.py render`. No editar a mano: cambiar `config/books.json`.",
        "",
        "Los libros viven fuera del repositorio, en la raíz de libros (`../books` o `SAP_LAB_BOOKS_ROOT`).",
        "Se citan por `slug`, capítulo y página del PDF; nunca se copia su texto al KB ni a entregables.",
        "",
        "| Slug | Libro | Dominios | Material adicional |",
        "|---|---|---|---|",
    ]
    for book in catalog["books"]:
        extra = book.get("supplements_note", "")
        lines.append(f"| `{book['slug']}` | {book['title']} | {', '.join(book.get('domains', []))} | {extra} |")
    lines += ["", "## Capítulos por ruta de skill", ""]
    route_ids = [r["id"] for r in (routing or {}).get("routes", [])] or sorted(
        {route for b in catalog["books"] for ch in b.get("chapters", []) for route in ch.get("routes", [])})
    for route in route_ids:
        chapters = chapters_for_routes(catalog, [route])
        if not chapters:
            continue
        lines.append(f"### `{route}` — {labels.get(route, route)}")
        lines.append("")
        lines += [f"- {format_chapter(ch)}" for ch in chapters]
        lines.append("")
    lines += ["## Fuera del alcance de este laboratorio", ""]
    lines += [f"- {item}" for item in catalog.get("out_of_scope", [])]
    lines += ["", "## Uso", "", "```bash",
              "python scripts/workspace/books.py index                       # una vez; genera artifacts/books-index/",
              "python scripts/workspace/books.py search \"draft\" \"etag\" --route rap",
              "python scripts/workspace/books.py chapters --route cds",
              "```", ""]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list")
    p_chapters = sub.add_parser("chapters")
    p_chapters.add_argument("--route", action="append", required=True)
    p_index = sub.add_parser("index")
    p_index.add_argument("--book")
    p_index.add_argument("--force", action="store_true")
    p_search = sub.add_parser("search")
    p_search.add_argument("terms", nargs="+")
    p_search.add_argument("--book")
    p_search.add_argument("--route")
    p_search.add_argument("--limit", type=int, default=10)
    p_render = sub.add_parser("render")
    p_render.add_argument("--output", default="docs/guides/reference-library.md")
    args = parser.parse_args(argv)

    catalog = load_catalog()
    if args.command == "list":
        source, folder = books_root(catalog), index_dir(catalog)
        print(f"Raíz de libros: {source} ({'existe' if source.is_dir() else 'NO existe'})")
        for book in catalog["books"]:
            present = "ok" if (source / book["pdf"]).is_file() else "falta"
            indexed = "indexado" if (folder / f"{book['slug']}.txt").is_file() else "sin índice"
            print(f"{book['slug']:<18} {present:<6} {indexed:<11} {book['title']}")
    elif args.command == "chapters":
        for chapter in chapters_for_routes(catalog, args.route):
            print(f"- {format_chapter(chapter)}")
    elif args.command == "index":
        print("\n".join(build_index(catalog, only=args.book, force=args.force)))
    elif args.command == "search":
        if not index_dir(catalog).is_dir():
            print("Sin índice. Ejecuta primero: python scripts/workspace/books.py index", file=sys.stderr)
            return 1
        results = search(catalog, args.terms, book=args.book, route=args.route, limit=args.limit)
        print("\n".join(results) if results else "Sin coincidencias.")
    elif args.command == "render":
        routing_path = ROOT / "config/skills-routing.json"
        routing = json.loads(routing_path.read_text(encoding="utf-8")) if routing_path.is_file() else None
        output = ROOT / args.output
        output.write_text(render_markdown(catalog, routing), encoding="utf-8", newline="\n")
        print(f"Escrito {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
