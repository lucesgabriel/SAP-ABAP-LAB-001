# Knowledge Base SAP ABAP LAB 001

Este es el cerebro reutilizable del laboratorio. Aquí vive lo que se aprende proyecto a proyecto y caso a caso, listo para consultarse al inicio del siguiente trabajo. Es la pieza que convierte el workspace en un sistema de auto-aprendizaje en lugar de una carpeta de proyectos sueltos.

## Regla principal

Antes de diseñar o escribir cualquier objeto ABAP, el agente consulta esta carpeta filtrando por la capability probable y cita los códigos usados en `docs/design.md` del proyecto. Al cerrar cada proyecto o caso, los errores y decisiones reutilizables se promueven aquí con códigos secuenciales mediante `scripts/workspace/close_project.py`.

## Estructura

| Archivo | Uso | Cuándo se actualiza |
|---|---|---|
| `taxonomy.md` | Tags obligatorios: capability, categoría, severidad, reutilizable, origen; formato de códigos. | Cuando se agrega una dimensión de clasificación (raro). |
| `error-catalog.md` | Errores resueltos con código `<CAP>-NNN` (`OO-001`, `API-001`, `TOOL-002`...). | Al cerrar cada proyecto (automático). |
| `solution-patterns.md` | Patrones validados `P-NNN` (report → clase cloud, orden RAP, diagnóstico CSRF...). | Cuando un patrón queda demostrado con evidencia (manual, al cierre). |
| `decision-registry.md` | Decisiones técnicas `D-NNN` con pregunta, decisión guía y evidencia. | Al cerrar cada proyecto (automático). |
| `released-api-recipes.md` | Recetas `R-NNN`: reemplazos clásico → liberado, consumo OData, comprobación de release. | Cuando una receta se valida en un proyecto (manual). |
| `lessons-learned-index.md` | Índice cruzado de proyectos y casos cerrados. | Al cerrar cada proyecto (automático). |

## Flujo de uso

```text
   ┌─ Nuevo proyecto o caso ──────────────────────────────────────┐
   │ 1. projects.py create / new_case.py → inyecta                 │
   │    docs/historical-context.md con códigos del KB filtrados    │
   │    por capability (prefijo del id o dominio del caso)         │
   │ 2. Diseña citando P-XXX, D-XXX, R-XXX en docs/design.md       │
   │ 3. Construye con ARC-1 (P-002); registra errores y            │
   │    decisiones en docs/error-log.md y docs/decision-log.md     │
   │    con taxonomía                                              │
   │ 4. Verifica: lint/sintaxis/activación/Unit/ATC/lectura        │
   │ 5. Retrospectiva (prompts/05) → Listo para consolidar: Si     │
   └─────────────┬─────────────────────────────────────────────────┘
                 ▼
   ┌─ close_project.py --dry-run / close_project.py ──────────────┐
   │ Promueve filas REUSE_YES / REUSE_PARTIAL al KB con códigos    │
   │ secuenciales, actualiza lessons-learned-index y el estado;    │
   │ corre lint_knowledge_base.py antes y después                  │
   └─────────────┬─────────────────────────────────────────────────┘
                 ▼
         knowledge-base crece → el siguiente proyecto lo hereda
```

## Validación

```bash
python scripts/workspace/lint_knowledge_base.py            # tags, IDs únicos y secuenciales, secretos, referencias cruzadas
python scripts/workspace/lint_knowledge_base.py --strict   # los warnings también fallan
```

## Reglas de higiene

- Cada entrada tiene tags válidos según `taxonomy.md`; el linter lo verifica.
- No copiar contraseñas, tokens, cookies ni claves en ninguna parte del KB; solo alias y rutas.
- Si un patrón o receta cambia, añadir una fila al changelog al pie del archivo.
- Si dos proyectos resuelven el mismo error con soluciones distintas, registrar ambas variantes con el contexto que las diferencia.
- Un código nunca se renumera ni se reutiliza; lo obsoleto se marca con fecha y reemplazo.
- `learning/lessons.md` conserva la narrativa de cada lección con su evidencia; el KB conserva la versión codificada y consultable. Al promover, enlazar ambas.
