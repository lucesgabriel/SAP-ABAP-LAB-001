# Ficha de cierre

Estado de la entrega: pendiente. Fecha: pendiente.

| Comprobación | Resultado / motivo de no aplicación | Evidencia |
| --- | --- | --- |
| Objetos afectados y paquete | Pendiente | Pendiente |
| Diff o descripción exacta del cambio | Pendiente | Pendiente |
| SAPLint (avisos clasificados: falso positivo / aceptado / corregido) | No ejecutado | Pendiente |
| SAPDiagnose: sintaxis | No ejecutado | Pendiente |
| Activación (batch para varios objetos) | No ejecutado | Pendiente |
| Lectura posterior del estado final | No ejecutado | Pendiente |
| INACTIVE_OBJECTS limpio | No ejecutado | Pendiente |
| ABAP Unit | No ejecutado | Pendiente |
| ATC (variante y recuento antes/después si es migración) | No ejecutado | Pendiente |
| Dependencias y where-used | No ejecutado | Pendiente |
| Transporte y riesgos | Pendiente | Pendiente |
| Pasos de reversión | Pendiente | Pendiente |

## Aprendizaje y pendientes

- Códigos del KB citados en el diseño y confirmados en la práctica: pendiente.
- Filas de `docs/error-log.md` con `YES`/`PARTIAL` listas para promover: pendiente.
- Filas de `docs/decision-log.md` con `YES`/`PARTIAL` listas para promover: pendiente.
- Patrón o receta nuevos propuestos (redactar a mano en el KB al cierre): pendiente.
- Lección narrativa en `learning/lessons.md`, si corresponde: pendiente.
- Deuda pendiente y siguiente paso: pendiente.

## Cierre

1. Completar esta ficha con evidencia real (no declarar PASS desde un write).
2. Ejecutar el prompt `prompts/05-retrospectiva-cierre.md`.
3. Poner `"ready_to_consolidate": true` en `project.json`.
4. `python scripts/workspace/close_project.py --project projects/<id> --dry-run` y luego sin `--dry-run`.

No cambiar `project.json` a `completed` mientras falte evidencia requerida por `AGENTS.md`. Las operaciones irreversibles mantienen su confirmación explícita inmediata.
