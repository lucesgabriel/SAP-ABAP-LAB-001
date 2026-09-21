#!/usr/bin/env python
"""Validate the SAP ABAP LAB workspace without printing secrets."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "CONTEXT.txt",
    "config/system.yaml",
    "docs/CLAUDE-DESKTOP-PROJECT-INSTRUCTIONS.md",
    "docs/TOOL-CATALOG.md",
    "learning/lessons.md",
    "learning/decisions.md",
    "learning/patterns.md",
    "learning/backlog.md",
]
TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".py"}
SECRET_PATTERNS = [
    re.compile(r"(?i)password\s*[:=]\s*(?!\[REMOVED|\$\{|<|REDACTED)(\S+)"),
    re.compile(r"(?i)(api[_-]?key|token|secret)\s*[:=]\s*(?!\$\{|<|REDACTED)(\S{8,})"),
]


def run(command: list[str]) -> tuple[int, str]:
    try:
        p = subprocess.run(command, text=True, capture_output=True, timeout=90)
        return p.returncode, (p.stdout + p.stderr)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []

    for rel in REQUIRED:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    system_path = ROOT / "config/system.yaml"
    if system_path.exists():
        try:
            data = yaml.safe_load(system_path.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or "system" not in data:
                errors.append("config/system.yaml has no system mapping")
        except Exception as exc:
            errors.append(f"invalid config/system.yaml: {exc}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if any(part in {".git", "artifacts", "logs", "__pycache__"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"possible credential in {path.relative_to(ROOT)}")
                break

    rc, out = run(["hermes", "mcp", "list"])
    if rc or "sap_arc1_s4h_100" not in out or "enabled" not in out:
        errors.append("Hermes MCP sap_arc1_s4h_100 is not listed as enabled")
    else:
        notes.append("Hermes ARC-1 entry: enabled")

    rc, out = run(["claude", "plugin", "list"])
    expected_plugins = ("clean-abap@claude-abap-skills", "abap-cloud-rap@claude-abap-skills", "arc-1@arc-1")
    missing_plugins = [p for p in expected_plugins if p not in out]
    if rc or missing_plugins:
        errors.append("missing Claude Code plugins: " + ", ".join(missing_plugins))
    else:
        notes.append("Claude Code ABAP plugins: installed")

    appdata = os.environ.get("APPDATA")
    if appdata:
        claude_cfg = Path(appdata) / "Claude" / "claude_desktop_config.json"
        try:
            cfg = json.loads(claude_cfg.read_text(encoding="utf-8-sig"))
            entry = (cfg.get("mcpServers") or {}).get("sap-arc1-s4h-100")
            if not entry:
                errors.append("Claude Desktop MCP sap-arc1-s4h-100 is missing")
            elif entry.get("env"):
                errors.append("Claude Desktop ARC-1 entry contains an env block; expected secret-free launcher")
            else:
                notes.append("Claude Desktop ARC-1 entry: present and secret-free")
        except Exception as exc:
            errors.append(f"cannot validate Claude Desktop configuration: {exc}")

    print("SAP ABAP LAB 001 workspace validation")
    for note in notes:
        print(f"[OK] {note}")
    for error in errors:
        print(f"[ERROR] {error}")
    print(f"Result: {'PASS' if not errors else 'FAIL'} ({len(errors)} error(s))")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
