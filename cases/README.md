# Casos De Práctica ABAP

> Área aislada de los proyectos (`projects/`). Cada caso tiene un **ID único** `ABAP-CASE-<DOMINIO>-<NNN>` y vive en su propia carpeta. Consume y enriquece el mismo `knowledge-base/`.

## Generar un caso nuevo

```bash
python scripts/workspace/new_case.py --domain RAP --level intermedio --topic "Órdenes de mantenimiento con draft"
python scripts/workspace/new_case.py --domain OO --level basico --topic "Refactor de report a clase" --time 30 --package ZLAB_OO
python scripts/workspace/new_case.py --domain CDS --topic "Vista de equipos con texto" --dry-run
```

El generador:

1. Asigna el siguiente ID secuencial por dominio (`ABAP-CASE-RAP-001`, `ABAP-CASE-RAP-002`...).
2. Crea la carpeta aislada `cases/<CASE-ID>-<slug>/` copiando `cases/_template/` + los docs estándar de `projects/_template/` (design, logs, journal, tests, evidence, src).
3. Consulta el `knowledge-base/` filtrando por la capability del dominio e inyecta `00-case-brief/historical-context.md` con los códigos `P-XXX`, `D-XXX`, `R-XXX` y `<CAP>-XXX` aplicables.
4. Actualiza `_index.md` y `_status.md`.

El contenido del brief (sección 2 a 18) lo redacta el agente con el prompt `prompts/04-generar-caso-practica.md`, usando las skills `abap-senior` / `abap-rap-senior` / `sap-abap:*` según el dominio. El generador solo crea la estructura.

## Dominios disponibles

| Dominio | Cubre | Capability KB |
|---|---|---|
| `OO` | Clases, Clean ABAP, refactor de reports a clases | OO |
| `CDS` | Vistas, asociaciones, anotaciones, access control | CDS |
| `RAP` | Business objects managed/unmanaged, draft, acciones, OData | RAP |
| `SQL` | ABAP SQL moderno, AMDP, rendimiento | SQL |
| `ENH` | BAdI, enhancements, clean core de extensiones | ENH |
| `API` | Consumir/exponer OData y HTTP, released APIs | API |
| `UI` | Fiori Elements sobre RAP, anotaciones UI | UI |
| `MIX` | Caso integrador que cruza varias capabilities | MULTI |

Niveles: `basico`, `intermedio`, `avanzado`, `examen`.

## Resolver un caso

1. Leer `00-case-brief/case-brief.md` y `00-case-brief/historical-context.md`.
2. **No abrir `solution/expected-solution.md`** hasta marcar `Resuelto: Si`.
3. Diseñar en `docs/design.md` citando el KB.
4. Construir en SAP con ARC-1 siguiendo `AGENTS.md` (`P-002`).
5. Completar `tests/plan.md`, `evidence/completion.md`, `docs/error-log.md`, `docs/decision-log.md`.
6. Marcar `Resuelto: Si` + `Listo para consolidar: Si` (README y `metadata.json`) y cerrar:

```bash
python scripts/workspace/close_project.py --project cases/<CASE-ID>-<slug> --dry-run
python scripts/workspace/close_project.py --project cases/<CASE-ID>-<slug>
```

## Archivos de esta carpeta

- `_template/`: base que copia el generador (README, brief, histórico, rúbrica, solución oculta, metadata).
- `_index.md`: registro de todos los casos generados con ID, dominio, nivel y ruta.
- `_status.md`: tablero corto de estado.

## Reglas

- **IDs únicos y secuenciales** por dominio; validados por `python scripts/workspace/lint_knowledge_base.py`.
- **Sin datos de clientes reales.** Ofuscar nombres, montos y datos antes de copiarlos a un brief.
- **Sin secretos** en `case-brief.md` ni en evidencias; solo placeholders `<TU_*>`.
- **Solución oculta** hasta resolver. Compararla y anotar diferencias en `docs/journal.md`.
- Un caso resuelto sin ficha de cierre completa no se consolida.
