# Prompt: Nuevo Proyecto ABAP

Usa el workspace `SAP ABAP LAB 001`. Tengo un nuevo requerimiento ABAP. Primero analiza; no construyas todavía.

## Requerimiento

```text
<pega aquí el requerimiento: objetivo de negocio, objetos existentes, resultado esperado, restricciones>
```

## Skills a cargar

`sap-abap:abap-cloud` (nivel clean core y restricciones) y `sap-abap:released-abap-classes` (reemplazos liberados). Si el requerimiento es RAP/CDS, añade `sap-abap:rap` o `sap-abap:cds-view-entities`. Ver tabla en `AGENTS.md` → Selección de skills.

**Libros de referencia.** Ejecuta `python scripts/workspace/skill_router.py suggest "<requerimiento>"` (en Claude Code lo hace el hook) y anota en `docs/design.md` los capítulos de libro sugeridos (`slug cap.N p.X`).

## Tareas

1. **Crea el proyecto** (elige el prefijo según la capability principal: `abap`/`oo`, `cds`, `rap`, `sql`, `enh`, `api`, `ui`, `mix`):

   ```bash
   python scripts/workspace/projects.py create <prefijo>-<NNN>-<tema> --title "<título>"
   ```

2. **Lee el histórico inyectado** en `projects/<id>/docs/historical-context.md` y, para cada código listado, abre la entrada en `knowledge-base/` (`error-catalog.md`, `solution-patterns.md`, `decision-registry.md`, `released-api-recipes.md`). Indica cuáles aplican y cuáles no, y por qué.

3. **Lee el contexto en SAP** con ARC-1 (`SAPContext` → `SAPSearch`/`SAPRead`): paquete, objetos existentes, dependencias, estado de release de las APIs candidatas (`R-007`), transportes. Declara la conexión lista solo tras una lectura real (`TOOL-003`). Guarda únicamente el resumen no sensible.

4. **Clasifica la solución** con `standards/technology-decision-matrix.md`: report/clase, CDS, RAP, AMDP, BAdI, consumo OData... y el nivel clean core objetivo (A/B/C/D).

5. **Completa** `docs/design.md` (sección "Knowledge-base consultado" obligatoria), `docs/backlog.md` (tareas con criterio de aceptación) y la primera decisión en `docs/decision-log.md` (paquete y transporte, `D-007`).

6. **Lista preguntas abiertas y riesgos** distinguiendo hechos (leídos en SAP), supuestos y decisiones.

## Salida esperada

- Proyecto creado y `project.json` con `capability` correcta.
- Tabla de códigos del KB aplicables / descartados con motivo.
- Resumen del contexto SAP leído (fecha, herramienta, objetos, API_STATE).
- Diseño inicial con tecnología elegida, objetos propuestos, orden de activación y nivel clean core.
- Lista de pendientes que impiden construir sin supuestos.

## Restricciones

- No inventes paquetes, órdenes de transporte, nombres de vistas liberadas ni resultados de ATC.
- No escribas en SAP en esta fase.
- Si usaste una skill (`abap-senior`, `abap-rap-senior`, `sap-abap:*`), indica cuál y qué conclusión tomaste.
