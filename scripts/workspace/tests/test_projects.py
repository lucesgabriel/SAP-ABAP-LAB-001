"""Integration checks in temporary workspaces; never touch live project folders."""
from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from projects import ROOT, create_project, list_projects, read_metadata, refresh_context
from validate_structure import REQUIRED, validate

COPY_PREFIXES = ("projects/_template/", "cases/_template/", "knowledge-base/")
EXISTING_SCRIPTS = ("verify_workspace.py", "build_manual_pdf.py", "smoke_test_claude_arc1.py", "diag-csrf.ps1")


def make_workspace(root: Path) -> None:
    """Copy Markdown, templates and the knowledge-base so link validation exercises real files."""
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in {".git", "artifacts", "__pycache__", ".venv"} for part in relative.parts):
            continue
        rel = relative.as_posix()
        if (relative.parts[0] in {"projects", "cases"} and len(relative.parts) > 2
                and relative.parts[1] != "_template"):
            continue  # real projects/cases stay out of the sandbox
        if path.is_file() and (path.suffix in {".md", ".json"} or rel.startswith(COPY_PREFIXES)):
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
    for relative in REQUIRED:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.touch()
    for name in EXISTING_SCRIPTS:
        (root / "scripts" / name).touch()


class ProjectWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="abap-organization-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        make_workspace(self.root)

    def test_create_list_and_validate_unicode_title(self):
        title = 'Práctica "Órdenes" y tablas'
        target = create_project(self.root, "abap-001-prueba", title)
        data = read_metadata(target)
        self.assertEqual(data["title"], title)
        self.assertIsNone(data["sap_package"])
        self.assertEqual(data["capability"], "OO")
        self.assertFalse(data["ready_to_consolidate"])
        readme = (target / "README.md").read_text(encoding="utf-8")
        self.assertIn(title, readme)
        self.assertNotIn("{{", readme)
        with redirect_stdout(StringIO()) as output:
            self.assertEqual(list_projects(self.root), 0)
        self.assertIn("abap-001-prueba | planned | OO", output.getvalue())
        errors, count = validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(count, 1)

    def test_historical_context_is_injected_from_kb_by_prefix(self):
        target = create_project(self.root, "rap-003-ordenes", "BO de órdenes")
        context = (target / "docs" / "historical-context.md").read_text(encoding="utf-8")
        self.assertIn("`RAP`", context)
        self.assertIn("P-003", context)          # RAP activation-order pattern
        self.assertIn("D-007", context)          # transversal transport decision
        self.assertNotIn("{{", context)
        target = create_project(self.root, "abap-002-clase", "Clase", capability="API")
        context = (target / "docs" / "historical-context.md").read_text(encoding="utf-8")
        self.assertIn("API-001", context)
        self.assertIn("R-006", context)
        # refresh keeps the file in sync with the KB
        (self.root / "knowledge-base" / "error-catalog.md").write_text(
            (self.root / "knowledge-base" / "error-catalog.md").read_text(encoding="utf-8")
            + "\n### API-002 | Nuevo error de prueba\n\n**TAGS:** API, CONNECTIVITY, MINOR, REUSE_YES, TEST\n\n- **Síntoma:** x\n",
            encoding="utf-8")
        refresh_context(self.root, "abap-002-clase")
        self.assertIn("API-002", (target / "docs" / "historical-context.md").read_text(encoding="utf-8"))

    def test_existing_project_is_not_overwritten(self):
        target = create_project(self.root, "abap-001-prueba", "Primero")
        (target / "README.md").write_text("Trabajo del usuario", encoding="utf-8")
        with self.assertRaises(ValueError):
            create_project(self.root, "abap-001-prueba", "Segundo")
        self.assertEqual((target / "README.md").read_text(encoding="utf-8"), "Trabajo del usuario")

    def test_rejects_path_traversal_and_invalid_identifiers(self):
        for value in ("../escape", "C:/escape", "abap-001-../escape", "ABAP-001-prueba", "con", "abap-1-prueba"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                create_project(self.root, value, "Prueba")
        with self.assertRaises(ValueError):
            create_project(self.root, "abap-009-x", "Prueba", capability="NOPE")
        self.assertEqual([p.name for p in (self.root / "projects").iterdir() if p.is_dir()], ["_template"])

    def test_reports_invalid_metadata_missing_files_and_broken_links(self):
        target = create_project(self.root, "rap-002-prueba", "Prueba")
        data = json.loads((target / "project.json").read_text(encoding="utf-8"))
        data["status"] = "unknown"
        (target / "project.json").write_text(json.dumps(data), encoding="utf-8")
        (target / "tests/plan.md").unlink()
        errors, _ = validate(self.root)
        self.assertTrue(any("status inválido" in error for error in errors))
        self.assertTrue(any("Falta archivo de proyecto" in error for error in errors))
        self.assertTrue(any("Enlace local roto" in error for error in errors))

    def test_legacy_project_without_loop_fields_still_validates(self):
        target = create_project(self.root, "abap-005-legacy", "Legacy")
        data = json.loads((target / "project.json").read_text(encoding="utf-8"))
        for field in ("capability", "ready_to_consolidate", "consolidated_on"):
            data.pop(field)
        (target / "project.json").write_text(json.dumps(data), encoding="utf-8")
        self.assertEqual(read_metadata(target)["id"], "abap-005-legacy")


if __name__ == "__main__":
    unittest.main()
