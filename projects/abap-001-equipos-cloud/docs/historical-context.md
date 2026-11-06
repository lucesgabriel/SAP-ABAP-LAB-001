# Histórico Consultado — abap-001-equipos-cloud

> Inyectado automáticamente por `scripts/workspace/projects.py` al crear el proyecto, filtrando el `knowledge-base/` por la capability `OO` (derivada del prefijo del identificador). Regenerar con `projects.py refresh-context abap-001-equipos-cloud` si el KB cambió.

## Capability principal

`OO`

## Patrón base sugerido

**Base sugerido:** `P-001` — Report ALV clásico → clase ABAP Cloud con CDS liberadas

## Errores conocidos a prevenir (filtrado por capability)

- `OO-001` — `CX_ABAP_CONTEXT_INFO_ERROR` no capturada al leer el idioma del usuario
- `OO-002` — ABAP Doc mal ubicado genera warning de sintaxis

## Decisiones reutilizables aplicables

- `D-001` — `AGENTS.md` como contrato portable entre agentes
- `D-002` — ARC-1 standalone como superficie ABAP principal
- `D-003` — Credenciales fuera del proyecto
- `D-004` — Acceso técnico amplio con controles de proceso
- `D-005` — Mejora continua basada en evidencia
- `D-006` — Proyectos independientes y conocimiento compartido
- `D-007` — `$TMP` para experimentos, `Z*`/`Y*` con orden verificada para activos durables
- `D-008` — Comprobar `API_STATE` antes de elegir la vista CDS o clase de reemplazo
- `D-009` — Preferir edición de método sobre reemplazo completo de clase

## Recetas aplicables

- `R-002` — `sy-langu` → `cl_abap_context_info=>get_user_language_abap_format( )`
- `R-003` — `SELECT-OPTIONS` / `PARAMETERS` → estructura de criterios
- `R-004` — `CL_SALV_TABLE` / `WRITE` → `IF_OO_ADT_CLASSRUN`
- `R-005` — `MESSAGE` y literales → símbolos de texto

## Proyectos y casos cerrados similares

- `abap-001-equipos-cloud` (cerrado 2026-10-01, capabilities OO, ATC, API, TOOL) → `projects/abap-001-equipos-cloud`

## Cómo se usa este histórico

1. Antes de diseñar, leer cada código citado arriba en el `knowledge-base/`.
2. En `docs/design.md` citar los códigos efectivamente reutilizados.
3. Si durante el build aparece un error no listado aquí, registrarlo en `docs/error-log.md` con `YES` o `PARTIAL` para promoverlo al cierre.

## Validación obligatoria

- [ ] Leí todos los códigos listados.
- [ ] Decidí qué patrón `P-XXX` aplico (puede ser ninguno si lo justifico en `docs/design.md`).
- [ ] Identifiqué decisiones `D-XXX` y recetas `R-XXX` que reutilizo.
- [ ] Detecté antipatrones a evitar.
