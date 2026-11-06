# Error Log — abap-001-equipos-cloud

Registra errores técnicos encontrados durante este proyecto (sintaxis, activación, ATC, Unit, conectividad, herramientas). Cada fila con `Reutilizable = YES` o `PARTIAL` se promueve a `knowledge-base/error-catalog.md` al cierre con `scripts/workspace/close_project.py`.

> Tags obligatorios según `knowledge-base/taxonomy.md`. Si el error ya existe en el catálogo, anota su código en la columna `Promovido` en lugar de describirlo de nuevo.

## Tabla maestra de errores

| ID | Fecha | Capability | Categoría | Severidad | Origen | Síntoma | Causa raíz | Solución aplicada | Reutilizable | Promovido (código KB) |
|---|---|---|---|---|---|---|---|---|---|---|
| ER-01 | 2026-09-20 | OO | SYNTAX | MAJOR | BUILD | Warning: `CX_ABAP_CONTEXT_INFO_ERROR` no capturada | `get_user_language_abap_format( )` declara la excepción | TRY/CATCH con idioma por defecto | YES | `OO-001` |
| ER-02 | 2026-09-20 | OO | SYNTAX | MINOR | BUILD | Warning: ABAP Doc mal ubicado | Comentario `"!` separado de la declaración | Reubicado con `edit_class_definition` | YES | `OO-002` |
| ER-03 | 2026-09-20 | ATC | CLEAN_CORE | MAJOR | TEST | La clase activa limpia en `$TMP` pero usaría objetos no liberados sin aviso | `$TMP` no impone versión de lenguaje cloud | ATC `ABAP_CLOUD_READINESS` sobre original y nuevo | YES | `ATC-001` |
| ER-04 | 2026-09-20 | ATC | SYNTAX | MINOR | TEST | Info SLIN strings without text elements | Literales sin símbolo de texto | `edit_text_symbols` 001/002 | YES | `ATC-002` |
| ER-05 | 2026-09-20 | ATC | OPERATIONS | MINOR | TEST | Info de sistema TTZCU (SAP Note 481835) | Customizing de zonas horarias, ajeno al objeto | Documentado como responsabilidad de Basis | PARTIAL | `ATC-003` |
| ER-06 | 2026-09-20 | TOOL | TOOLING | MINOR | BUILD | 7 avisos SAPLint sobre `IF_OO_ADT_CLASSRUN`, `check_subrc`, `double_space` | Linter local no conoce la interfaz; reglas de estilo | Clasificados: 5 falsos positivos, 2 aceptados | YES | `TOOL-004` |
| ER-01 | YYYY-MM-DD | OO / CDS / RAP / SQL / DDIC / ENH / API / UI / CTS / ATC / UNIT / TOOL / SEC / MULTI | SYNTAX / ACTIVATION / DEPENDENCY / DATA_MODEL / BEHAVIOR / CLEAN_CORE / PERFORMANCE / AUTHORIZATION / CONNECTIVITY / TESTING / TRANSPORT / TOOLING / NAMING / OPERATIONS | BLOCKER / MAJOR / MINOR | DESIGN / BUILD / ACTIVATE / TEST / TRANSPORT / PROD | | | | YES / PARTIAL / NO | (pendiente / <CAP>-NNN) |

## Detalle por error

Las filas ER-01 a ER-06 se promovieron al KB al crear el knowledge-base (2026-10-01); el detalle completo está en cada código citado y en [`learning/lessons.md`](../../../learning/lessons.md). Por cada fila nueva, ampliar aquí:

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
3. `python scripts/workspace/close_project.py --project projects/abap-001-equipos-cloud --dry-run` muestra los códigos que asignará antes de escribir.
