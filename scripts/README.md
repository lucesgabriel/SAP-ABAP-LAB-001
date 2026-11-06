# Herramientas del laboratorio

Ejecuta los comandos desde la raíz. Las utilidades de `workspace/` requieren Python 3.10+ y solo usan la biblioteca estándar; ninguna contacta SAP.

## Loop de auto-mejora (`scripts/workspace/`)

| Herramienta | Uso | Alcance |
| --- | --- | --- |
| [workspace/projects.py](workspace/projects.py) | `create <id> --title "Título" [--capability RAP]`, `list`, `refresh-context <id>` | Genera el proyecto desde la plantilla e inyecta `docs/historical-context.md` desde el KB. |
| [workspace/new_case.py](workspace/new_case.py) | `--domain RAP --topic "Tema" [--level intermedio] [--time 45] [--package $TMP] [--dry-run]` | Genera un caso `ABAP-CASE-<DOM>-<NNN>` aislado con brief, histórico, rúbrica y solución oculta; actualiza `cases/_index.md` y `_status.md`. |
| [workspace/close_project.py](workspace/close_project.py) | `--project projects/<id>` o `cases/<id>` `[--dry-run] [--skip-lint] [--force]` | Promueve filas `YES`/`PARTIAL` de `docs/error-log.md` y `docs/decision-log.md` al KB con códigos secuenciales; referencia cruzada si ya existían; actualiza índice y estado. |
| [workspace/lint_knowledge_base.py](workspace/lint_knowledge_base.py) | `[--strict] [--root <raíz>]` | Tags vs taxonomía, IDs únicos y secuenciales, secretos, referencias cruzadas, IDs y metadata de casos. |
| [workspace/validate_structure.py](workspace/validate_structure.py) | sin argumentos | Archivos requeridos, plantillas, metadatos de proyectos y casos, enlaces Markdown locales. |
| [workspace/skill_router.py](workspace/skill_router.py) | `session-start`, `prompt` (stdin JSON del hook), `suggest "<petición>"` | Ruteo automático fase/dominio → skills, códigos KB y capítulos de libro desde `config/skills-routing.json`; lo llaman los hooks de `.claude/settings.json`. Nunca bloquea: ante error sale con 0 y sin salida. |
| [workspace/books.py](workspace/books.py) | `list`, `chapters --route <id>`, `index [--book <slug>] [--force]`, `search "<término>" [--route <id>] [--book <slug>]`, `render` | Biblioteca local (`../books` o `SAP_LAB_BOOKS_ROOT`) catalogada en `config/books.json`. El índice de texto va a `artifacts/books-index/` (ignorado por git); usa `pdftotext` o `pypdf` si existen. |
| [workspace/kb.py](workspace/kb.py) | módulo | Taxonomía, parseo de catálogos, siguiente código y render del histórico; lo usan las demás. |

## Utilidades existentes

| Herramienta | Uso | Alcance |
| --- | --- | --- |
| [verify_workspace.py](verify_workspace.py) | `python scripts/verify_workspace.py` | Validador existente: inventario, heurística de secretos y configuración de clientes. Requiere PyYAML y clientes configurados. |
| [build_manual_pdf.py](build_manual_pdf.py) | `python scripts/build_manual_pdf.py` | Genera el PDF del manual; requiere ReportLab. |
| [smoke_test_claude_arc1.py](smoke_test_claude_arc1.py) | Consultar el script antes de usar | Prueba existente mediante cliente Claude y ARC-1; requiere entorno configurado. |
| [diag-csrf.ps1](diag-csrf.ps1) | Consultar alcance antes de ejecutar | Diagnóstico existente vinculado a pruebas HTTP (`API-001`, `P-004`); su uso puede afectar SAP según la operación. |

Los scripts existentes mantienen sus rutas. No ejecutes diagnósticos SAP como comprobación de carpetas. Ningún resultado del validador, del linter ni del cierre demuestra conexión SAP, sanitización completa, sintaxis ABAP, activación, Unit o ATC.

## Verificar las utilidades

```powershell
python -m unittest discover -s scripts/workspace/tests -v
python scripts/workspace/validate_structure.py
python scripts/workspace/lint_knowledge_base.py
```

Las pruebas usan carpetas temporales fuera de los proyectos reales y no llaman a SAP. Los estados `completed`/`archived` son metadatos locales; su evidencia se revisa manualmente según `AGENTS.md`.
