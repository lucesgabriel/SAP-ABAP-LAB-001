"""Pruebas del ruteo de skills y de la biblioteca de libros; no leen PDFs reales ni llaman a SAP."""
from contextlib import redirect_stdout
from io import BytesIO, StringIO, TextIOWrapper
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import books  # noqa: E402
import skill_router  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]


class RoutingConfigTests(unittest.TestCase):
    def setUp(self):
        self.routing = skill_router.load_routing(ROOT)
        self.catalog = books.load_catalog(ROOT)

    def test_route_ids_unique_and_books_reference_known_routes(self):
        ids = [route["id"] for route in self.routing["routes"]]
        self.assertEqual(len(ids), len(set(ids)))
        for book in self.catalog["books"]:
            for chapter in book["chapters"]:
                for route in chapter["routes"]:
                    self.assertIn(route, ids, f"{book['slug']} cap.{chapter['n']} usa ruta desconocida {route}")

    def test_book_slugs_unique(self):
        slugs = [book["slug"] for book in self.catalog["books"]]
        self.assertEqual(len(slugs), len(set(slugs)))

    def test_every_route_has_skills(self):
        for route in self.routing["routes"]:
            self.assertTrue(route["skills"], route["id"])
            self.assertTrue(route["keywords"], route["id"])


class MatchTests(unittest.TestCase):
    def setUp(self):
        self.routing = skill_router.load_routing(ROOT)

    def ids(self, text):
        return [route["id"] for route, _ in skill_router.match_routes(text, self.routing)]

    def test_rap_prompt(self):
        self.assertEqual(self.ids("Crear un BO RAP managed con draft y validaciones")[0], "rap")

    def test_word_boundaries(self):
        self.assertNotIn("rap", self.ids("un párrafo sobre trapos"))
        self.assertNotIn("rap", self.ids("unmanagedx"))

    def test_spanish_and_symbols(self):
        self.assertIn("unit", self.ids("necesito pruebas unitarias con test double"))
        self.assertIn("cloud", self.ids("reemplazar sy-datum por API liberada"))

    def test_ignores_system_notifications(self):
        event = "<task-notification><summary>maintenance notification rap cds</summary></task-notification>"
        self.assertEqual(skill_router.suggest(event, ROOT), "")
        self.assertNotIn("pm", self.ids("tabla de mantenimiento y notification por correo"))

    def test_no_match_returns_empty(self):
        self.assertEqual(skill_router.suggest("hola, buenos días", ROOT), "")

    def test_suggest_lists_skills_kb_and_books(self):
        text = skill_router.suggest("behavior definition con draft", ROOT)
        self.assertIn("`sap-abap:rap`", text)
        self.assertIn("P-003", text)
        self.assertIn("`rap-2025` cap.3", text)

    def test_respects_route_limit(self):
        text = "rap cds odata amdp badi authority-check atc abap unit alv"
        self.assertLessEqual(len(self.ids(text)), self.routing["max_routes_per_prompt"])


class HookTests(unittest.TestCase):
    def run_hook(self, args, stdin_text=""):
        stdin = TextIOWrapper(BytesIO(stdin_text.encode("utf-8")), encoding="utf-8")
        with mock.patch.object(sys, "stdin", stdin), redirect_stdout(StringIO()) as out:
            code = skill_router.main(args)
        return code, out.getvalue()

    def test_prompt_hook_reads_json(self):
        code, out = self.run_hook(["prompt"], json.dumps({"prompt": "crear una CDS view entity con asociaciones"}))
        self.assertEqual(code, 0)
        self.assertIn("sap-abap:cds-view-entities", out)

    def test_prompt_hook_silent_without_match(self):
        code, out = self.run_hook(["prompt"], json.dumps({"prompt": "gracias"}))
        self.assertEqual((code, out), (0, ""))

    def test_hook_never_fails_on_bad_input(self):
        code, _ = self.run_hook(["prompt"], "{no es json")
        self.assertEqual(code, 0)

    def test_session_banner(self):
        code, out = self.run_hook(["session-start"])
        self.assertEqual(code, 0)
        self.assertIn("P-002", out)
        self.assertIn("sap-abap:abap-cloud", out)


class BooksSearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="abap-books-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "config").mkdir()
        shutil.copyfile(ROOT / "config/books.json", self.root / "config/books.json")
        library = self.root / "library"
        (library / "Demo").mkdir(parents=True)
        (library / "Demo/demo.txt").write_text("Intro\fBehavior definition with draft\fETag handling",
                                               encoding="utf-8")
        catalog = books.load_catalog(self.root)
        catalog["books"] = [{"slug": "demo", "title": "Demo", "pdf": "Demo/demo.pdf", "txt": "Demo/demo.txt",
                             "chapters": [{"n": "1", "title": "Demo", "page": 2, "routes": ["rap"]}]}]
        self.catalog = catalog
        self.env = mock.patch.dict("os.environ", {catalog["root_env"]: str(library)})
        self.env.start()
        self.addCleanup(self.env.stop)

    def test_index_and_search_by_page(self):
        report = books.build_index(self.catalog, self.root)
        self.assertTrue(report[0].startswith("+ demo"))
        hits = books.search(self.catalog, ["draft", "behavior"], self.root)
        self.assertEqual(len(hits), 1)
        self.assertTrue(hits[0].startswith("demo p.2:"))
        self.assertEqual(books.search(self.catalog, ["draft"], self.root, route="cds"), [])

    def test_index_is_idempotent(self):
        books.build_index(self.catalog, self.root)
        self.assertTrue(books.build_index(self.catalog, self.root)[0].startswith("= demo"))

    def test_render_mentions_every_book(self):
        catalog = books.load_catalog(ROOT)
        text = books.render_markdown(catalog, skill_router.load_routing(ROOT))
        for book in catalog["books"]:
            self.assertIn(f"`{book['slug']}`", text)


if __name__ == "__main__":
    unittest.main()
