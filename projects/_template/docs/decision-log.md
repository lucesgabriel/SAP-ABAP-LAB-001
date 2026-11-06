# Decision Log — {{PROJECT_ID}}

Registra decisiones técnicas tomadas en este proyecto (paquete, APIs de reemplazo, orden de activación, estrategia de pruebas, transporte). Las reutilizables se promueven a `knowledge-base/decision-registry.md` al cierre.

> Tags obligatorios según `knowledge-base/taxonomy.md`. Si la decisión confirma una `D-NNN` existente, anótala en `Promovido` y describe solo lo nuevo.

## Tabla maestra de decisiones

| ID | Fecha | Capability | Categoría | Tema | Decisión | Alternativas evaluadas | Motivo | Impacto | Reutilizable | Promovido (código KB) |
|---|---|---|---|---|---|---|---|---|---|---|
| DC-01 | YYYY-MM-DD | OO / CDS / RAP / SQL / DDIC / ENH / API / UI / CTS / ATC / UNIT / TOOL / SEC / MULTI | SYNTAX / ACTIVATION / DEPENDENCY / DATA_MODEL / BEHAVIOR / CLEAN_CORE / PERFORMANCE / AUTHORIZATION / CONNECTIVITY / TESTING / TRANSPORT / TOOLING / NAMING / OPERATIONS | | | | | | YES / PARTIAL / NO | (pendiente / D-NNN) |

## Detalle por decisión

### DC-XX | Título corto de la decisión

**TAGS:** <capability>, <categoría>, REUSE_YES|REUSE_PARTIAL|REUSE_NO

- **Pregunta:**
- **Contexto:**
- **Decisión:**
- **Alternativas evaluadas:**
  - Alt 1: pros / contras / por qué se descarta.
  - Alt 2: pros / contras / por qué se descarta.
- **Motivo:**
- **Impacto técnico:**
- **Impacto operativo (transporte, reversión):**
- **Decisión / patrón / receta del KB consultada:** (D-XXX, P-XXX, R-XXX)

## Decisiones obligatorias que deben quedar claras

Verificar que estos puntos tengan una decisión registrada antes de cerrar:

- Paquete (`$TMP` vs `Z*`/`Y*`) y orden de transporte verificada (`D-007`).
- APIs de reemplazo y su estado de release comprobado (`D-008`).
- Orden de escritura/activación cuando hay varios objetos (`P-003`).
- Estrategia de pruebas: ABAP Unit, test doubles, ATC variante, ejecución en consola.
- Nivel clean core objetivo (A/B/C/D) y justificación.
- Qué se conserva del objeto original y por qué.
- Pasos de reversión.

## Cómo se consolida al cierre

1. Las decisiones `YES` / `PARTIAL` se promueven a `knowledge-base/decision-registry.md` con el siguiente `D-NNN`.
2. Si confirma o refina una existente, se añade nota cruzada en lugar de duplicar.
3. `close_project.py` automatiza el paso anterior.
