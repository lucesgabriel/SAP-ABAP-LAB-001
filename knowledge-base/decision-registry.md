# Registro Central De Decisiones Técnicas

Decisiones con impacto reutilizable identificadas en el laboratorio y en proyectos cerrados. Sirve para justificar una elección similar sin volver a discutirla. Las decisiones de gobernanza del laboratorio (`ADR-NNN` en `learning/decisions.md`) tienen aquí su espejo técnico `D-001` a `D-006`; a partir de `D-007` las decisiones nacen en los `docs/decision-log.md` de cada proyecto y se promueven al cierre.

> Cada entrada tiene tags según `taxonomy.md`. Si una decisión nueva contradice una existente, se actualiza la entrada antigua con la nueva evidencia en lugar de crear una contradictoria.

## Índice

- [Gobernanza del laboratorio](#gobernanza-del-laboratorio)
- [Transportes y paquetes](#transportes-y-paquetes)
- [APIs y clean core](#apis-y-clean-core)
- [Modelo de datos](#modelo-de-datos)
- [Acceso a datos y seguridad](#acceso-a-datos-y-seguridad)

---

## Gobernanza del laboratorio

### D-001 | `AGENTS.md` como contrato portable entre agentes

**TAGS:** TOOL, OPERATIONS, REUSE_YES

- **Pregunta:** ¿Dónde viven las reglas que todos los agentes (Hermes, Claude Code, Claude Desktop, Codex) deben cumplir?
- **Decisión guía:** `AGENTS.md` es la fuente común. `CLAUDE.md` solo actúa como bootstrap para Claude Code / Cowork y remite a `AGENTS.md`.
- **Motivo:** Evita duplicar reglas y permite revisión por Git.
- **Origen:** `ADR-001` en `learning/decisions.md`.

### D-002 | ARC-1 standalone como superficie ABAP principal

**TAGS:** TOOL, TOOLING, REUSE_YES

- **Pregunta:** ¿Con qué herramienta leen y escriben los agentes en SAP?
- **Decisión guía:** `sap_arc1_s4h_100` / `sap-arc1-s4h-100` para contexto, búsqueda, lectura, escritura, activación, diagnóstico, navegación, transportes y gCTS. La conexión se declara lista solo tras una lectura no destructiva (`TOOL-003`).
- **Origen:** `ADR-002`.

### D-003 | Credenciales fuera del proyecto

**TAGS:** SEC, OPERATIONS, REUSE_YES

- **Pregunta:** ¿Dónde se guardan usuario y contraseña SAP?
- **Decisión guía:** Solo en el almacén privado local del cliente MCP; nunca en archivos versionados, chats, capturas ni PDFs. El linter del KB y `verify_workspace.py` buscan patrones de secretos.
- **Errores asociados:** `SEC-002`.
- **Origen:** `ADR-003`.

### D-004 | Acceso técnico amplio con controles de proceso

**TAGS:** TOOL, OPERATIONS, REUSE_YES

- **Pregunta:** ¿Puede ARC-1 exponer escrituras, SQL, transportes y Git?
- **Decisión guía:** Sí, pero `delete`, liberación de transportes, `unpublish`, push/commit gCTS, SQL modificador y cualquier acción irreversible requieren confirmación explícita inmediatamente antes, más verificación posterior.
- **Motivo:** No confundir capacidad técnica con autorización.
- **Origen:** `ADR-004`.

### D-005 | Mejora continua basada en evidencia

**TAGS:** TOOL, OPERATIONS, REUSE_YES

- **Pregunta:** ¿Cuándo se escribe conocimiento permanente?
- **Decisión guía:** Solo después de una entrega verificada (activación + lectura posterior + pruebas/ATC o motivo explícito). Las hipótesis quedan en el diario o en el backlog. Los errores y decisiones se registran con taxonomía en el proyecto y se promueven al KB al cierre con `close_project.py`; nunca se promueven filas `REUSE_NO`.
- **Origen:** `ADR-005`, ampliada el 2026-10-01 con el loop de auto-mejora.

### D-006 | Proyectos independientes y conocimiento compartido

**TAGS:** TOOL, OPERATIONS, REUSE_YES

- **Pregunta:** ¿Cómo se organizan los trabajos?
- **Decisión guía:** Cada proyecto vive en `projects/<id>/` generado desde `_template/`; cada caso de práctica en `cases/ABAP-CASE-<DOM>-<NNN>-<slug>/`. `project.json` / `metadata.json` mantienen el estado local; el listado se calcula. Cerrar o archivar no cambia la ruta. El conocimiento específico permanece en el proyecto; lo reutilizable va al `knowledge-base/`.
- **Origen:** `ADR-006`.

---

## Transportes y paquetes

### D-007 | `$TMP` para experimentos, `Z*`/`Y*` con orden verificada para activos durables

**TAGS:** CTS, TRANSPORT, REUSE_YES

- **Pregunta:** ¿En qué paquete se crea un objeto?
- **Decisión guía:** `$TMP` solo para trabajo desechable o pruebas de concepto. Cualquier objeto que se quiera conservar va a un paquete `Z*`/`Y*` con capa/target y orden de transporte leídos en SAP, nunca deducidos del identificador local. Un objeto cloud-ready que deba ser verificado por el compilador necesita un paquete con versión de lenguaje "ABAP for Cloud Development" (`ATC-001`).
- **Origen:** `learning/patterns.md` (Transportes), `projects/abap-001-equipos-cloud`.

---

## APIs y clean core

### D-008 | Comprobar `API_STATE` antes de elegir la vista CDS o clase de reemplazo

**TAGS:** API, CLEAN_CORE, REUSE_YES

- **Pregunta:** ¿Qué API usar en lugar de una tabla SAP o una clase no liberada?
- **Decisión guía:** Preferir objetos con contrato C1 liberado y "uso en ABAP Cloud = sí", comprobado con `SAPRead type=API_STATE` en el sistema real (no por memoria). Documentar la tabla de reemplazo campo a campo en `docs/design.md`. Si no hay API liberada, evaluar wrapper (nivel B/C) y registrar la decisión.
- **Recetas:** `R-001`, `R-002`, `R-007`.
- **Origen:** `projects/abap-001-equipos-cloud`.

### D-009 | Preferir edición de método sobre reemplazo completo de clase

**TAGS:** OO, OPERATIONS, REUSE_YES

- **Pregunta:** ¿Cómo se corrige una clase existente desde ARC-1?
- **Decisión guía:** `SAPWrite edit_method` / `edit_class_definition` / `edit_text_symbols` con el diff mínimo. Reemplazo completo solo al crear la clase o cuando el cambio afecta a la mayoría del código, y siempre con lectura previa de la versión activa.
- **Patrón asociado:** `P-002`.
- **Origen:** `learning/patterns.md` (Clases).

---

## Modelo de datos

### D-010 | Semántica de moneda y unidad obligatoria en CDS

**TAGS:** CDS, DATA_MODEL, REUSE_YES

- **Pregunta:** ¿Cómo se exponen campos `CURR` / `QUAN` en una vista CDS?
- **Decisión guía:** Siempre con `@Semantics.amount.currencyCode` / `@Semantics.quantity.unitOfMeasure` apuntando al campo de referencia expuesto en la misma vista. Sin esa anotación la vista no debe considerarse terminada aunque active.
- **Origen:** `learning/patterns.md` (CDS y datos).

---

## Acceso a datos y seguridad

### D-011 | Consultas mínimas: columnas explícitas, filtros restrictivos, límites pequeños

**TAGS:** SQL, AUTHORIZATION, REUSE_YES

- **Pregunta:** ¿Cómo se leen datos desde un agente?
- **Decisión guía:** Seleccionar solo las columnas necesarias, con filtros y `UP TO n ROWS` pequeños. Nunca exportar masivamente datos personales, financieros, HR o credenciales. La evidencia guarda muestras sanitizadas, no volcados.
- **Origen:** `AGENTS.md` (Seguridad y secretos), `projects/abap-001-equipos-cloud` (`max_rows` en criterios).

---

## Plantilla para nuevas entradas

```markdown
### D-NNN | Título de la decisión

**TAGS:** <capability>, <categoría>, REUSE_YES|REUSE_PARTIAL

- **Pregunta:**
- **Decisión guía:**
- **Alternativas evaluadas:**
- **Motivo:**
- **Impacto:**
- **Errores / patrones / recetas asociados:**
- **Origen:** <proyecto o caso> (decisión local DC-NN)
```

## Changelog

| Fecha | Cambio |
|---|---|
| 2026-10-01 | Versión inicial: D-001 a D-006 espejo de ADR-001..006; D-007 a D-011 promovidas desde `learning/patterns.md`, `AGENTS.md` y `projects/abap-001-equipos-cloud`. |
