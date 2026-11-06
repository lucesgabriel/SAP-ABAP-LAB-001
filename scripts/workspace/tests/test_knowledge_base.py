"""Self-improvement loop: case generation, KB lint and project close in a temporary workspace."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import kb
from close_project import close_project
from lint_knowledge_base import run_lint
from new_case import create_case, read_case_metadata
from projects import create_project, read_metadata
from test_projects import make_workspace
from validate_structure import validate

ERROR_ROW = ("| ER-01 | 2026-10-01 | RAP | ACTIVATION | MAJOR | ACTIVATE | Behavior pool no activa "
             "| BDEF inactiva | Activación batch | YES | (pendiente) |")
KNOWN_ROW = ("| ER-02 | 2026-10-01 | OO | SYNTAX | MAJOR | BUILD | Excepción sin capturar "
             "| ver catálogo | TRY/CATCH | YES | OO-001 |")
NO_ROW = ("| ER-03 | 2026-10-01 | RAP | BEHAVIOR | MINOR | TEST | Draft no guarda "
          "| Falta with draft | Añadido | NO | (pendiente) |")
BAD_ROW = ("| ER-04 | 2026-10-01 | RAP | FOO | MAJOR | TEST | Tag inválido | x | y | YES | (pendiente) |")
DECISION_ROW = ("| DC-01 | 2026-10-01 | RAP | BEHAVIOR | Numbering | Early numbering con UUID "
                "| Late numbering | Sin rango | Sin SNRO | PARTIAL | (pendiente) |")


def fill_logs(target: Path, error_rows, decision_rows=()) -> None:
    log = target / "docs" / "error-log.md"
    text = log.read_text(encoding="utf-8")
    log.write_text(text.replace("| ER-01 | YYYY-MM-DD |", "\n".join(error_rows) + "\n| ER-01 | YYYY-MM-DD |", 1),
                   encoding="utf-8")
    if decision_rows:
        log = target / "docs" / "decision-log.md"
        text = log.read_text(encoding="utf-8")
        log.write_text(text.replace("| DC-01 | YYYY-MM-DD |", "\n".join(decision_rows) + "\n| DC-01 | YYYY-MM-DD |", 1),
                       encoding="utf-8")


def mark_ready(target: Path, meta_name: str, **extra) -> None:
    meta_path = target / meta_name
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    meta.update(ready_to_consolidate=True, **extra)
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    completion = target / "evidence" / "completion.md"
    completion.write_text(completion.read_text(encoding="utf-8")
                          .replace("Estado de la entrega: pendiente", "Estado de la entrega: verificada"),
                          encoding="utf-8")


class KnowledgeBaseLoopTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="abap-kb-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        make_workspace(self.root)

    def test_seed_kb_passes_lint(self):
        report = run_lint(self.root)
        self.assertEqual(report.count("ERROR"), 0, [i.message for i in report.issues])

    def test_lint_detects_bad_tags_duplicates_secrets_and_crossrefs(self):
        catalog = self.root / "knowledge-base" / "error-catalog.md"
        catalog.write_text(catalog.read_text(encoding="utf-8") + (
            "\n### OO-001 | Duplicado\n\n**TAGS:** OO, FOO, MAJOR, REUSE_YES, BUILD\n\n- **Síntoma:** ver P-999\n"
            "- **Nota:** password = SuperSecreta123\n"), encoding="utf-8")
        messages = [i.message for i in run_lint(self.root).issues]
        self.assertTrue(any("ID duplicado OO-001" in m for m in messages))
        self.assertTrue(any("fuera de taxonomía: FOO" in m for m in messages))
        self.assertTrue(any("posible secreto" in m for m in messages))
        self.assertTrue(any("inexistente P-999" in m for m in messages))

    def test_create_case_assigns_sequential_ids_and_injects_context(self):
        first = create_case(self.root, domain="OO", topic="Refactor de report ALV a clase", time_min=30)
        second = create_case(self.root, domain="OO", topic="Otro caso", level="avanzado")
        other = create_case(self.root, domain="RAP", topic="BO con draft")
        self.assertEqual(first.name, "ABAP-CASE-OO-001-refactor-de-report-alv-a-clase")
        self.assertEqual(second.name, "ABAP-CASE-OO-002-otro-caso")
        self.assertEqual(other.name, "ABAP-CASE-RAP-001-bo-con-draft")
        meta = read_case_metadata(first)
        self.assertEqual((meta["capability"], meta["time_min"], meta["level"]), ("OO", 30, "intermedio"))
        context = (first / "00-case-brief" / "historical-context.md").read_text(encoding="utf-8")
        self.assertIn("P-001", context)
        self.assertIn("OO-001", context)
        self.assertNotIn("{{", context)
        brief = (first / "00-case-brief" / "case-brief.md").read_text(encoding="utf-8")
        self.assertIn("ABAP-CASE-OO-001", brief)
        self.assertNotIn("{{", brief)
        design = (first / "docs" / "design.md").read_text(encoding="utf-8")
        self.assertIn("../00-case-brief/historical-context.md", design)
        index = (self.root / "cases" / "_index.md").read_text(encoding="utf-8")
        self.assertIn("| OO | ABAP-CASE-OO-003 |", index)
        self.assertIn("`ABAP-CASE-RAP-001`", index)
        self.assertIn("`ABAP-CASE-OO-002`", (self.root / "cases" / "_status.md").read_text(encoding="utf-8"))
        errors, count = validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(count, 3)
        self.assertEqual(run_lint(self.root).count("ERROR"), 0)
        with self.assertRaises(ValueError):
            create_case(self.root, domain="XX", topic="x")

    def test_dry_run_plans_codes_without_writing(self):
        target = create_project(self.root, "rap-002-ordenes", "Órdenes con draft")
        fill_logs(target, [ERROR_ROW, KNOWN_ROW, NO_ROW], [DECISION_ROW])
        mark_ready(target, "project.json")
        before = (self.root / "knowledge-base" / "error-catalog.md").read_text(encoding="utf-8")
        report = close_project(self.root, "projects/rap-002-ordenes", dry_run=True, skip_lint=False, force=False)
        self.assertFalse(report.has_errors(), report.issues)
        messages = " ".join(m for _, m in report.issues)
        self.assertIn("ER-01 → NUEVO RAP-001", messages)
        self.assertIn("ER-02 → existente OO-001", messages)
        self.assertIn("ER-03: REUSE_NO", messages)
        self.assertIn("DC-01 → NUEVO D-012", messages)
        self.assertEqual((self.root / "knowledge-base" / "error-catalog.md").read_text(encoding="utf-8"), before)
        self.assertEqual(read_metadata(target)["status"], "planned")

    def test_close_promotes_rows_updates_index_and_status(self):
        target = create_project(self.root, "rap-002-ordenes", "Órdenes con draft")
        fill_logs(target, [ERROR_ROW, KNOWN_ROW, NO_ROW], [DECISION_ROW])
        mark_ready(target, "project.json")
        design = target / "docs" / "design.md"
        design.write_text(design.read_text(encoding="utf-8").replace("| P-XXX |", "| P-003 |"), encoding="utf-8")
        report = close_project(self.root, "projects/rap-002-ordenes", dry_run=False, skip_lint=False, force=False)
        self.assertFalse(report.has_errors(), report.issues)
        catalog = (self.root / "knowledge-base" / "error-catalog.md").read_text(encoding="utf-8")
        registry = (self.root / "knowledge-base" / "decision-registry.md").read_text(encoding="utf-8")
        self.assertIn("### RAP-001 | Behavior pool no activa", catalog)
        self.assertIn("**TAGS:** RAP, ACTIVATION, MAJOR, REUSE_YES, ACTIVATE", catalog)
        self.assertIn("También visto en:** `projects/rap-002-ordenes` (ER-02", catalog)
        self.assertNotIn("Draft no guarda", catalog)
        self.assertIn("### D-012 | Numbering", registry)
        self.assertIn("REUSE_PARTIAL", registry.split("### D-012")[1][:120])
        self.assertIn("Promovidos RAP-001 desde", catalog)
        log = (target / "docs" / "error-log.md").read_text(encoding="utf-8")
        self.assertIn("| YES | `RAP-001` |", log)
        self.assertIn("| YES | `OO-001` |", log)
        index = (self.root / "knowledge-base" / "lessons-learned-index.md").read_text(encoding="utf-8")
        self.assertIn("| project | rap-002-ordenes | ", index)
        self.assertIn("| OO, RAP | 1 | 1 | 1 |", index)
        meta = read_metadata(target)
        self.assertEqual(meta["status"], "completed")
        self.assertIsNotNone(meta["consolidated_on"])
        self.assertEqual(run_lint(self.root).count("ERROR"), 0)
        # Second close only re-reports existing codes and does not duplicate entries.
        report = close_project(self.root, "projects/rap-002-ordenes", dry_run=False, skip_lint=False, force=False)
        self.assertFalse(report.has_errors(), report.issues)
        self.assertEqual(catalog.count("### RAP-001"), 1)
        self.assertEqual(kb.next_code(catalog, "RAP", kb.ERROR_ID_RE), "RAP-002")

    def test_close_blocks_on_invalid_rows_and_unready_projects(self):
        target = create_project(self.root, "rap-002-ordenes", "Órdenes")
        fill_logs(target, [BAD_ROW])
        report = close_project(self.root, "projects/rap-002-ordenes", dry_run=True, skip_lint=True, force=False)
        messages = " ".join(m for _, m in report.issues)
        self.assertTrue(report.has_errors())
        self.assertIn("ready_to_consolidate es false", messages)
        self.assertIn("categoría inválida 'FOO'", messages)
        report = close_project(self.root, "projects/_template", dry_run=True, skip_lint=True, force=True)
        self.assertTrue(report.has_errors())

    def test_close_case_marks_status_board(self):
        case = create_case(self.root, domain="UI", topic="Fiori sobre RAP")
        fill_logs(case, ["| ER-01 | 2026-10-01 | UI | DEPENDENCY | MAJOR | TEST | Preview sin anotaciones "
                         "| Falta @UI | Añadidas | YES | (pendiente) |"])
        rel = f"cases/{case.name}"
        report = close_project(self.root, rel, dry_run=True, skip_lint=True, force=False)
        self.assertTrue(report.has_errors())  # not resolved yet
        mark_ready(case, "metadata.json", resolved=True)
        report = close_project(self.root, rel, dry_run=False, skip_lint=False, force=False)
        self.assertFalse(report.has_errors(), report.issues)
        self.assertIn("### UI-001 |", (self.root / "knowledge-base" / "error-catalog.md").read_text(encoding="utf-8"))
        status = (self.root / "cases" / "_status.md").read_text(encoding="utf-8")
        self.assertIn("| `ABAP-CASE-UI-001` | Fiori sobre RAP | UI | generado | si | Si | Si |", status)
        self.assertEqual(read_case_metadata(case)["status"], "completed")


if __name__ == "__main__":
    unittest.main()
