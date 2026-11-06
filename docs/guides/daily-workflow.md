# Flujo de trabajo diario

## Empezar

1. Lee [AGENTS.md](../../AGENTS.md), [decisiones](../../learning/decisions.md) y el [README del knowledge-base](../../knowledge-base/README.md).
2. Ejecuta `python scripts/workspace/projects.py list` desde la raíz y elige un proyecto. Si no existe, usa `create` según el [catálogo de proyectos](../../projects/README.md); para practicar, genera un [caso](../../cases/README.md) con `new_case.py`.
3. Lee su `docs/historical-context.md` y abre cada código citado en el KB. Luego README, diseño y backlog. Elige una tarea pequeña con criterio de aceptación; cambia el estado a `active` en `project.json`.
4. Para trabajar en SAP, usa `SAPContext` y después `SAPSearch`/`SAPRead`; confirma paquete, dependencias, API release y transporte antes de diseñar cambios. Guarda solo el resumen no sensible.

## Desarrollar y verificar

Sigue el flujo obligatorio de `AGENTS.md` (`P-002`): diseño → diff mínimo → lint/sintaxis → escritura → activación → pruebas y lectura posterior. La creación de carpetas no crea paquetes, transportes ni objetos en SAP. Los prompts `prompts/01` a `03` guían cada fase.

- Mantén el plan en `docs/backlog.md` y las decisiones del proyecto en `docs/design.md` y `docs/decision-log.md`.
- Registra cada error resuelto en `docs/error-log.md` **en el momento**, con taxonomía; es más fácil que reconstruirlo al cierre.
- Guarda el código en `src/` e indica en su README de qué lectura o propuesta procede.
- Define criterios en `tests/plan.md`; resume resultados en `evidence/`. No declarar PASS a partir de un archivo generado o de una escritura sin activación comprobada.
- Para varios objetos, sigue el orden de dependencias y la activación batch indicada por las reglas.

## Cerrar la sesión

1. Anota en `docs/journal.md` lo realizado, resultado observado, evidencia y siguiente paso. Para estudio transversal usa una copia de la [plantilla de sesión](../../learning/templates/session.md) en `learning/sessions/`.
2. Mantén las hipótesis como pendientes. Un error resuelto con causa raíz verificada va a `docs/error-log.md` con `YES`/`PARTIAL`; una duda sin verificar, no.
3. Ejecuta `python scripts/workspace/validate_structure.py` y `python scripts/workspace/lint_knowledge_base.py`. Antes de entregar o versionar, ejecuta además el validador existente `python scripts/verify_workspace.py` en el entorno configurado y revisa manualmente los archivos nuevos por datos sensibles.
4. Revisa `git status --short` y `git diff`; revisa también los archivos nuevos, que `git diff` no muestra hasta incorporarlos al índice. Haz commits pequeños cuando decidas versionar.

## Cerrar un proyecto

1. Completa `evidence/completion.md` con objetos/paquetes, cambio exacto, lint/sintaxis, activación, Unit/ATC o motivo de no aplicación, lectura posterior, inactivos, dependencias, transporte, riesgos y reversión.
2. Ejecuta el prompt `prompts/05-retrospectiva-cierre.md`: decide fila por fila qué es reutilizable, redacta patrones/recetas nuevos si los hay, marca `"ready_to_consolidate": true`.
3. `python scripts/workspace/close_project.py --project projects/<id> --dry-run`, revisa los códigos que asignará, y luego sin `--dry-run`. El script deja el proyecto en `completed` y actualiza el KB.
4. Si dejas de mantener un proyecto sin cerrarlo, usa `archived` y registra si quedó terminado o abandonado. Archivar aquí no ejecuta operaciones SAP.

Ver la [guía del loop de auto-mejora](self-improvement-loop.md) para el detalle.

## Revisión de aprendizaje

Al terminar una sesión, identifica un siguiente paso concreto. Periódicamente revisa la [ruta de aprendizaje](../../learning/roadmap.md), retira duplicados y enlaza ejercicios completados a su evidencia o a su caso en `cases/`. Mantén la revisión trimestral del KB registrada en el backlog global; esta guía no programa automatizaciones.
