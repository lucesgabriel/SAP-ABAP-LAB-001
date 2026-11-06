# Decisiones de arquitectura

> ADR de gobernanza del laboratorio. Su espejo técnico y las decisiones de proyectos viven en [`knowledge-base/decision-registry.md`](../knowledge-base/decision-registry.md) como `D-NNN`; las nuevas decisiones técnicas nacen en el `docs/decision-log.md` de cada proyecto y se promueven al cierre.

## ADR-001 — AGENTS.md como contrato portable
- **Estado:** aceptada
- **Decisión:** `AGENTS.md` es la fuente común para Hermes Desktop y agentes compatibles. `CLAUDE.md` solo actúa como bootstrap para Claude Code.
- **Motivo:** evita duplicar reglas y permite revisión por Git.

## ADR-002 — ARC-1 standalone como superficie ABAP principal
- **Estado:** aceptada
- **Decisión:** usar `sap_arc1_s4h_100` para contexto, búsqueda, lectura, escritura, activación, diagnóstico, navegación, transportes y Git/gCTS.
- **Motivo:** el servidor fue autenticado mediante una lectura real y expone las capacidades necesarias.

## ADR-003 — Credenciales fuera del proyecto
- **Estado:** aceptada
- **Decisión:** usuario y contraseña operativos se resuelven desde el almacén privado local; nunca desde archivos versionados.
- **Motivo:** reduce exposición y permite compartir el workspace.

## ADR-004 — Acceso técnico amplio con controles de proceso
- **Estado:** aceptada por solicitud del usuario
- **Decisión:** ARC-1 puede exponer escrituras de paquetes, SQL, transportes y Git. Las acciones irreversibles siguen requiriendo confirmación explícita y verificación posterior.
- **Motivo:** habilitar desarrollo completo sin confundir capacidad técnica con autorización para acciones destructivas.

## ADR-005 — Mejora continua basada en evidencia
- **Estado:** aceptada
- **Decisión:** los agentes actualizan `learning/` después de entregas verificadas; no modifican reglas por hipótesis ni acumulan duplicados.
- **Motivo:** mantener conocimiento útil, auditable y reversible.

## ADR-006 — Proyectos independientes y conocimiento compartido
- **Estado:** aceptada por solicitud de organización del usuario, 2026-09-20.
- **Decisión:** cada proyecto local vive en `projects/<id>/`, generado desde `_template/`, con diseño, código, pruebas, evidencias y transportes. `project.json` mantiene su estado; el listado se calcula desde esos archivos. Cerrar o archivar no cambia la ruta.
- **Motivo:** separar trabajos y mantener enlaces estables sin duplicar un catálogo manual. El conocimiento específico permanece en el proyecto; solo conclusiones reutilizables comprobadas pasan a `learning/`.
- **Compatibilidad:** conservar reglas, configuración y rutas existentes; no cambiar objetos SAP como parte de la organización.
- **Evidencia:** [validación de la estructura y utilidades](../docs/maintenance/2026-09-20-organization.md).

## ADR-007 — Loop de auto-mejora con knowledge-base global
- **Estado:** aceptada por solicitud del usuario, 2026-10-01.
- **Decisión:** el laboratorio adopta la filosofía del SAP Integration Suite Codex Lab: un `knowledge-base/` con taxonomía obligatoria y catálogos codificados (`<CAP>-NNN`, `P-NNN`, `D-NNN`, `R-NNN`); cada proyecto o caso nace con un histórico inyectado desde el KB, registra errores y decisiones con taxonomía en `docs/error-log.md` y `docs/decision-log.md`, y se cierra con `scripts/workspace/close_project.py`, que promueve las filas reutilizables con códigos secuenciales. `lint_knowledge_base.py` valida tags, IDs, secretos y referencias. Los casos de práctica viven en `cases/` con ID `ABAP-CASE-<DOM>-<NNN>` y solución oculta.
- **Motivo:** hacer el aprendizaje escalable y consultable: lo aprendido en un proyecto llega automáticamente al siguiente de la misma capability, en lugar de depender de releer `learning/lessons.md`.
- **Compatibilidad:** `projects/`, `learning/`, scripts y manuales conservan rutas; `project.json` añade campos opcionales (`capability`, `ready_to_consolidate`, `consolidated_on`); los proyectos anteriores siguen validando. Nada escribe en SAP.
- **Espejo técnico:** `D-005` (ampliada) y `D-006`.
- **Evidencia:** pruebas `scripts/workspace/tests/test_knowledge_base.py`; KB semilla con 14 errores, 5 patrones, 11 decisiones y 7 recetas promovidos desde `learning/lessons.md`, `learning/patterns.md` y `projects/abap-001-equipos-cloud`.

## ADR-008 — Ruteo automático de skills y biblioteca de referencia
- **Estado:** aceptada por solicitud del usuario, 2026-11-06.
- **Decisión:** `config/skills-routing.json` es la fuente única del mapa fase/dominio → skills (plugin SAP ABAP de Lik Wei Tan, `clean-abap`, `abap-cloud-rap`, `arc-1`, `anthropic-skills:abap-*`) → códigos KB → capítulos de libro. `.claude/settings.json` (versionado) habilita esos plugins a nivel proyecto y registra hooks `SessionStart` y `UserPromptSubmit` que ejecutan `scripts/workspace/skill_router.py`. Los libros de `../books` se catalogan en `config/books.json` (capítulo, página PDF, rutas) y se consultan con `scripts/workspace/books.py`; el índice de texto es local en `artifacts/`.
- **Motivo:** que cada sesión cargue la skill correcta sin depender de recordar la tabla de `AGENTS.md`, y que el diseño cite una fuente concreta (`slug cap.N p.X`) además del KB.
- **Compatibilidad:** sin cambios en SAP ni en la conexión ARC-1. Los libros no se copian al repositorio (copyright); solo se citan. Precedencia: SAP en vivo > KB > libros. Hermes/Codex/Claude Desktop usan `skill_router.py suggest`.
- **Evidencia:** pruebas `scripts/workspace/tests/test_skill_router.py`; `validate_structure.py` y `lint_knowledge_base.py` en verde el 2026-11-06.
