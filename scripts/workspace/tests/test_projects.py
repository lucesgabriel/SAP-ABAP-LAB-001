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
from projects import ROOT, create_project, list_projects, read_metadata
from validate_structure import REQUIRED, validate


class ProjectWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="abap-organization-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Copy documents so link validation exercises the real delivered template.
        for path in ROOT.rglob("*"):
            relative = path.relative_to(ROOT)
            if any(part in {".git", "artifacts", "__pycache__"} for part in relative.parts):
                continue
            if path.is_file() and (path.suffix == ".md" or relative.as_posix().startswith("projects/_template/")):
                target = self.root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, target)
        for relative in REQUIRED:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                path.touch()
        for name in ("verify_workspace.py", "build_manual_pdf.py", "smoke_test_claude_arc1.py", "diag-csrf.ps1"):
            (self.root / "scripts" / name).touch()

    def test_create_list_and_validate_unicode_title(self):
        title = 'Práctica "Órdenes" y tablas'
        target = create_project(self.root, "abap-001-prueba", title)
        data = read_metadata(target)
        self.assertEqual(data["title"], title)
        self.assertIsNone(data["sap_package"])
        self.assertIn(title, (target / "README.md").read_text(encoding="utf-8"))
        self.assertNotIn("{{PROJECT_ID}}", (target / "README.md").read_text(encoding="utf-8"))
        with redirect_stdout(StringIO()) as output:
            self.assertEqual(list_projects(self.root), 0)
        self.assertIn("abap-001-prueba | planned", output.getvalue())
        errors, count = validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(count, 1)

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


if __name__ == "__main__":
    unittest.main()
