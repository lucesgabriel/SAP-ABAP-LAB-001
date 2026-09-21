# Decisiones de arquitectura

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
