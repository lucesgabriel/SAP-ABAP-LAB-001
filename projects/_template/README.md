# {{PROJECT_TITLE}}

Identificador: `{{PROJECT_ID}}` · Capability KB: `{{CAPABILITY}}` · Creado: {{CREATED_ON}}.
Estado y referencias SAP: [project.json](project.json).

## Objetivo

Pendiente: describe el resultado que quieres demostrar y su criterio de aceptación.

## Alcance

- Incluye: pendiente.
- Fuera de alcance: pendiente.
- Siguiente paso: leer el [histórico del KB](docs/historical-context.md), completar el diseño y seleccionar la primera tarea del backlog.

## Estado del loop de auto-mejora

- Histórico del KB consultado: pendiente (marcar al leer `docs/historical-context.md`).
- Códigos citados en el diseño: pendiente.
- Error log y decision log con taxonomía: pendiente.
- Listo para consolidar: No (cambiar `ready_to_consolidate` en `project.json` cuando la ficha de cierre esté completa).

## Navegación

- [Histórico consultado](docs/historical-context.md), [diseño](docs/design.md), [backlog](docs/backlog.md) y [diario](docs/journal.md).
- [Error log](docs/error-log.md) y [decision log](docs/decision-log.md) (se promueven al KB al cierre).
- [Código y procedencia](src/README.md).
- [Plan de pruebas](tests/plan.md).
- [Evidencias](evidence/README.md) y [criterio de terminado](evidence/completion.md).
- [Objetos, transportes y reversión](transports/README.md).
- [Reglas del laboratorio](../../AGENTS.md), [knowledge-base](../../knowledge-base/README.md) y [aprendizaje compartido](../../learning/README.md).

## Cierre

```bash
python scripts/workspace/close_project.py --project projects/{{PROJECT_ID}} --dry-run
python scripts/workspace/close_project.py --project projects/{{PROJECT_ID}}
```

Esta carpeta se crea localmente. No demuestra conexión, escritura, activación ni pruebas en SAP.
