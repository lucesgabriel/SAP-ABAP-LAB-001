# Claude Code / Cowork — SAP ABAP LAB 001

Lee y aplica íntegramente `AGENTS.md` antes de trabajar. Este archivo solo adapta el flujo al entorno de Claude; en caso de conflicto manda `AGENTS.md`.

## Plugins y skills disponibles
- `clean-abap@claude-abap-skills`, `abap-cloud-rap@claude-abap-skills`, `arc-1@arc-1`
- Plugin **SAP ABAP** de la SAP AI Skills Library (`sap-abap:*`, 18 skills) y `anthropic-skills:abap-senior` / `abap-rap-senior`
- Qué skill cargar en cada fase: tabla "Selección de skills" de `AGENTS.md`; cada prompt de `prompts/` la repite en su cabecera.
- **Automático:** `.claude/settings.json` habilita estos plugins en el proyecto y sus hooks (`SessionStart`, `UserPromptSubmit`) ejecutan `scripts/workspace/skill_router.py`, que inyecta en cada mensaje las skills, códigos KB y capítulos de libro del dominio detectado. Si aparece el bloque `[SAP-ABAP-LAB-001 · skill-router]`, carga esas skills con la herramienta Skill antes de diseñar o escribir código.
- **Libros:** `config/books.json` + `scripts/workspace/books.py` (`chapters`, `search`, `index`). Cita `slug cap.N p.X`; nunca copies su texto.

## Inicio recomendado
1. Lee `config/system.yaml`, `AGENTS.md`, `knowledge-base/README.md` y `learning/decisions.md`.
2. Confirma la conexión MCP con una lectura no destructiva (`SAPContext` o `SAPRead type=SYSTEM`), no solo por ver las herramientas listadas (`TOOL-003`).
3. Para inspección usa ARC-1; para cambios sigue el flujo obligatorio de `AGENTS.md` (`P-002`).
4. Invoca el skill especializado que corresponda.

## Reglas específicas de Claude (no negociables)

1. **Consulta el KB primero.** Antes de diseñar o construir, lee el `docs/historical-context.md` del proyecto (o del caso) y abre cada código citado en `knowledge-base/`. Cita los reutilizados en `docs/design.md`.

2. **Escala el trabajo ANTES de producir entregables.** Cuando el usuario pida un desarrollo, un ejercicio, un caso o un drill — incluso si lo pide como "guía", "paso a paso", "runbook" o "PDF" — primero crea la estructura con el generador y trabaja dentro de ella. No crees carpetas ad-hoc.

   ```bash
   python scripts/workspace/projects.py create <prefijo>-<NNN>-<tema> --title "<título>"
   python scripts/workspace/new_case.py --domain <DOM> --level <nivel> --topic "<tema>"
   ```

3. **Respeta los namespaces.** Proyectos: `<prefijo>-<NNN>-<tema>` (abap, cds, rap, sql, enh, api, ui, mix...). Casos: `ABAP-CASE-<DOM>-<NNN>` lo asigna el generador. Códigos KB: nunca inventes ni renumeres; `close_project.py` los asigna.

4. **Ubica los entregables donde corresponde:** diseño en `docs/design.md`; errores y decisiones en `docs/error-log.md` / `docs/decision-log.md` con taxonomía; código en `src/`; evidencias sanitizadas en `evidence/`; solución de un caso en `solution/expected-solution.md` (oculta hasta `Resuelto: Si`); salidas regenerables en `artifacts/<id>/`.

5. **Usa los scripts `.py`** (`projects.py`, `new_case.py`, `close_project.py`, `lint_knowledge_base.py`, `validate_structure.py`); solo requieren Python 3.10+ y stdlib.

6. **Valida antes de entregar:**
   ```bash
   python scripts/workspace/lint_knowledge_base.py
   python scripts/workspace/validate_structure.py
   ```

7. **Cierre:** cuando el usuario marque `ready_to_consolidate: true` (y `resolved: true` en casos), ejecuta `close_project.py --dry-run`, muestra los códigos que se asignarán, y luego el cierre real.

## Regla de conexión
No copies credenciales SAP a este repositorio ni a la configuración del proyecto. La autenticación pertenece al almacén privado del cliente MCP. Nunca pegues passwords, tokens, cookies ni service keys en archivos, evidencias o PDFs.
