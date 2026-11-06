# Error Log — {{PROJECT_ID}}

Registra errores técnicos encontrados durante este proyecto (sintaxis, activación, ATC, Unit, conectividad, herramientas). Cada fila con `Reutilizable = YES` o `PARTIAL` se promueve a `knowledge-base/error-catalog.md` al cierre con `scripts/workspace/close_project.py`.

> Tags obligatorios según `knowledge-base/taxonomy.md`. Si el error ya existe en el catálogo, anota su código en la columna `Promovido` en lugar de describirlo de nuevo.

## Tabla maestra de errores

| ID | Fecha | Capability | Categoría | Severidad | Origen | Síntoma | Causa raíz | Solución aplicada | Reutilizable | Promovido (código KB) |
|---|---|---|---|---|---|---|---|---|---|---|
| ER-01 | YYYY-MM-DD | OO / CDS / RAP / SQL / DDIC / ENH / API / UI / CTS / ATC / UNIT / TOOL / SEC / MULTI | SYNTAX / ACTIVATION / DEPENDENCY / DATA_MODEL / BEHAVIOR / CLEAN_CORE / PERFORMANCE / AUTHORIZATION / CONNECTIVITY / TESTING / TRANSPORT / TOOLING / NAMING / OPERATIONS | BLOCKER / MAJOR / MINOR | DESIGN / BUILD / ACTIVATE / TEST / TRANSPORT / PROD | | | | YES / PARTIAL / NO | (pendiente / <CAP>-NNN) |

## Detalle por error

Por cada fila relevante, ampliar aquí:

### ER-XX | Título corto del error

**TAGS:** <capability>, <categoría>, <severidad>, REUSE_YES|REUSE_PARTIAL|REUSE_NO, <origen>

- **Síntoma:**
- **Cuándo apareció:** (SAPDiagnose syntax, SAPActivate, ATC, Unit, F9, Bruno...)
- **Contexto técnico:** (objeto, paquete, versión activa/inactiva, herramienta)
- **Causa raíz:**
- **Solución aplicada:**
- **Workaround si la solución definitiva no fue posible:**
- **Prevención futura:**
- **Evidencia:** (ruta sanitizada en `evidence/`)
- **Skill / receta / código KB consultado:**

## Errores recurrentes a vigilar (precarga desde KB)

Ver `docs/historical-context.md` para la lista filtrada por capability. Clásicos transversales:

- `OO-001`: excepción de `CL_ABAP_CONTEXT_INFO` sin capturar.
- `ATC-001`: en `$TMP` solo la variante `ABAP_CLOUD_READINESS` detecta usos no liberados.
- `TOOL-003`: esquemas de ARC-1 publicados no demuestran autenticación.
- `TOOL-004`: falsos positivos de SAPLint; clasificar antes de corregir.
- `SEC-002`: ningún secreto en archivos del proyecto.

## Cómo se consolida al cierre

1. Marcar `Promovido` con el código existente si el error ya estaba en el catálogo (se añade referencia al proyecto, no se duplica).
2. Las filas nuevas con `YES` / `PARTIAL` reciben el siguiente código `<CAP>-NNN` disponible.
3. `python scripts/workspace/close_project.py --project projects/{{PROJECT_ID}} --dry-run` muestra los códigos que asignará antes de escribir.
