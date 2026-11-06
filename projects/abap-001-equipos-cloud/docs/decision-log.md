# Decision Log — abap-001-equipos-cloud

Registra decisiones técnicas tomadas en este proyecto (paquete, APIs de reemplazo, orden de activación, estrategia de pruebas, transporte). Las reutilizables se promueven a `knowledge-base/decision-registry.md` al cierre.

> Tags obligatorios según `knowledge-base/taxonomy.md`. Si la decisión confirma una `D-NNN` existente, anótala en `Promovido` y describe solo lo nuevo.

## Tabla maestra de decisiones

| ID | Fecha | Capability | Categoría | Tema | Decisión | Alternativas evaluadas | Motivo | Impacto | Reutilizable | Promovido (código KB) |
|---|---|---|---|---|---|---|---|---|---|---|
| DC-01 | 2026-09-20 | CTS | TRANSPORT | Paquete | `$TMP` sin transporte | Paquete Z con versión de lenguaje cloud | Prueba de concepto; el original se conserva | ATC acredita cloud readiness, no el compilador | YES | `D-007` |
| DC-02 | 2026-09-20 | API | CLEAN_CORE | Vistas de reemplazo | `I_Equipment` + `I_EquipmentText` (C1) | Acceso directo a EQUI/EQKT; otra vista no liberada | `API_STATE` leído: C1, uso en ABAP Cloud = sí | Sin objetos no liberados en la clase | YES | `D-008` |
| DC-03 | 2026-09-20 | OO | OPERATIONS | Forma de corregir | `edit_method` / `edit_class_definition` / `edit_text_symbols` | Reemplazo completo de la clase | Diff mínimo y lectura previa | Menos riesgo de regresión | YES | `D-009` |
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
