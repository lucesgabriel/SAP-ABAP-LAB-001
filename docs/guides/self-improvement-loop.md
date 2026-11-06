# Loop de auto-mejora

Cómo el laboratorio aprende de cada proyecto. Complementa la [organización](organization.md) y el [flujo diario](daily-workflow.md).

## Piezas

| Pieza | Dónde | Qué hace |
| --- | --- | --- |
| Knowledge-base | `knowledge-base/` | Catálogos codificados: errores `<CAP>-NNN`, patrones `P-NNN`, decisiones `D-NNN`, recetas `R-NNN`, índice de cierres, taxonomía. |
| Histórico inyectado | `projects/<id>/docs/historical-context.md`, `cases/<id>/00-case-brief/historical-context.md` | Lo que el KB ya sabe de la capability del trabajo, generado al crearlo. |
| Logs con taxonomía | `docs/error-log.md`, `docs/decision-log.md` | Dónde se registra, en el momento, cada error y decisión del trabajo. |
| Cierre | `scripts/workspace/close_project.py` | Promueve filas `YES`/`PARTIAL` al KB con códigos secuenciales; referencia cruzada si ya existían; actualiza índice y estado. |
| Linter | `scripts/workspace/lint_knowledge_base.py` | Tags válidos, IDs únicos y secuenciales, secretos, referencias cruzadas, IDs de casos. |
| Prompts y checklists | `prompts/`, `checklists/` | Guían cada fase para que la consulta y el registro no se salten. |

## Ciclo paso a paso

1. **Crear.** `projects.py create` o `new_case.py`. El prefijo del id (o el dominio del caso) fija la capability: `abap`→OO, `cds`→CDS, `rap`→RAP, `sql`→SQL, `enh`→ENH, `api`→API, `ui`→UI, `mix`→MULTI. `--capability` permite forzarla.
2. **Consultar.** Leer el histórico y abrir cada código en el KB. Citar en `docs/design.md` los reutilizados. Si el KB cambió durante el proyecto: `projects.py refresh-context <id>`.
3. **Construir y registrar.** Flujo `P-002` con ARC-1. Cada error resuelto va a `docs/error-log.md` con capability, categoría, severidad, origen y `YES`/`PARTIAL`/`NO`; cada elección a `docs/decision-log.md`. Las filas nuevas `YES`/`PARTIAL` llevan sección de detalle `### ER-XX | Título` con síntoma, causa raíz, solución, prevención y evidencia: ese texto es el que entra al KB.
4. **Verificar.** Ficha de cierre con evidencia real. Checklists.
5. **Retrospectiva.** `prompts/05`: decidir qué es reutilizable, redactar patrones/recetas nuevos a mano, marcar `ready_to_consolidate`.
6. **Cerrar.** `close_project.py --dry-run` muestra los códigos que asignará; sin `--dry-run` escribe. Lint antes y después.
7. **Heredar.** El siguiente proyecto de la misma capability recibe lo aprendido en su histórico.

## Qué se promueve y qué no

| Se promueve | No se promueve |
| --- | --- |
| Error con causa raíz y solución verificadas en SAP, `YES`/`PARTIAL` | Hipótesis, errores transitorios, `NO` |
| Decisión con alternativas y motivo, aplicable a otro proyecto | Preferencias sin justificación |
| Patrón demostrado (activado, probado, releído) | Propuesta de una skill no ejecutada |
| Receta de reemplazo validada con `API_STATE` leído | Reemplazo copiado de memoria |

## Relación con `learning/`

- `learning/lessons.md` guarda la **narrativa** (contexto, evidencia, lección, aplicación futura). El KB guarda la **versión codificada y filtrable**. Al promover, enlazar ambas; no duplicar el texto.
- `learning/decisions.md` guarda los ADR de gobernanza del laboratorio; `decision-registry.md` su espejo técnico `D-001`..`D-006` y las decisiones de proyectos a partir de `D-007`.
- `learning/patterns.md` queda como índice corto que remite a `solution-patterns.md`.
- `learning/roadmap.md`, `exercises/`, `sessions/` siguen siendo la ruta de estudio personal; los casos de `cases/` son su versión formal con rúbrica y cierre.

## Mantenimiento

- Revisar trimestralmente el KB: marcar obsoletos con fecha y reemplazo; nunca renumerar.
- Si el linter falla tras un cierre, revisar el diff antes de corregir a mano.
- Si dos proyectos resuelven lo mismo de forma distinta, registrar ambas variantes con el contexto que las diferencia.
