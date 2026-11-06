# Índice De Lecciones Aprendidas Por Proyecto

Registro cruzado de proyectos y casos cerrados con enlace a sus `docs/error-log.md` y `docs/decision-log.md`. Lo actualiza `scripts/workspace/close_project.py`.

| Tipo | Proyecto / caso | Fecha cierre | Capabilities | Errores promovidos | Decisiones promovidas | Patrones validados | Enlace |
|---|---|---|---|---|---|---|---|
| seed | abap-001-equipos-cloud | 2026-10-01 | OO, ATC, API, TOOL | 6 | 3 | 2 | `projects/abap-001-equipos-cloud` |
| seed | bruno-csrf-maintnotification | 2026-10-01 | API, TOOL | 3 | 0 | 1 | `artifacts/bruno/CROWN-API_MAINTNOTIFICATION` |

## Cómo se construye este índice

Cuando un proyecto o caso se cierra:

1. El prompt `prompts/05-retrospectiva-cierre.md` revisa `docs/error-log.md` y `docs/decision-log.md`.
2. Cada error con `REUSE_YES` o `REUSE_PARTIAL` se promueve a `error-catalog.md` con el siguiente código `<CAP>-NNN`.
3. Cada decisión reutilizable se promueve a `decision-registry.md` con el siguiente `D-NNN`.
4. Los patrones y recetas nuevos se redactan a mano en `solution-patterns.md` / `released-api-recipes.md` (el script solo los cuenta si el log los cita).
5. El proyecto se agrega como fila aquí y su `project.json` / `metadata.json` queda en `completed` / `closed`.

## Búsquedas rápidas

- Por capability: Ctrl+F `RAP`, `CDS`, `OO`, `API`, `ATC`...
- Por tema: Ctrl+F `CSRF`, `clean core`, `activación`...
- Por proyecto: Ctrl+F el identificador local.

## Changelog

| Fecha | Cambio |
|---|---|
| 2026-10-01 | Filas semilla: consolidación manual de `learning/lessons.md` y `abap-001` al crear el knowledge-base. |
