# Flujo de trabajo diario

## Empezar

1. Lee [AGENTS.md](../../AGENTS.md), [decisiones](../../learning/decisions.md) y las lecciones relevantes.
2. Ejecuta `python scripts/workspace/projects.py list` desde la raíz y elige un proyecto. Si no existe, usa `create` según el [catálogo de proyectos](../../projects/README.md).
3. Lee su README, diseño y backlog. Elige una tarea pequeña con criterio de aceptación; cambia el estado a `active` en `project.json`.
4. Para trabajar en SAP, usa `SAPContext` y después `SAPSearch`/`SAPRead`; confirma paquete, dependencias, API release y transporte antes de diseñar cambios. Guarda solo el resumen no sensible.

## Desarrollar y verificar

Sigue el flujo obligatorio de `AGENTS.md`: diseño → diff mínimo → lint/sintaxis → escritura → activación → pruebas y lectura posterior. La creación de carpetas no crea paquetes, transportes ni objetos en SAP.

- Mantén el plan en `docs/backlog.md` y las decisiones del proyecto en `docs/design.md`.
- Guarda el código en `src/` e indica en su README de qué lectura o propuesta procede.
- Define criterios en `tests/plan.md`; resume resultados en `evidence/`. No declarar PASS a partir de un archivo generado o de una escritura sin activación comprobada.
- Para varios objetos, sigue el orden de dependencias y la activación batch indicada por las reglas.

## Cerrar la sesión

1. Anota en `docs/journal.md` lo realizado, resultado observado, evidencia y siguiente paso. Para estudio transversal usa una copia de la [plantilla de sesión](../../learning/templates/session.md) en `learning/sessions/`.
2. Mantén las hipótesis como pendientes. Solo después de verificar, añade una lección reutilizable a `learning/lessons.md` con enlace a la evidencia y sin duplicar una anterior.
3. Si corresponde, actualiza decisiones globales, patrones aprobados o backlog global. No es necesario inventar un patrón por cada sesión.
4. Ejecuta `python scripts/workspace/validate_structure.py`. Antes de entregar o versionar, ejecuta además el validador existente `python scripts/verify_workspace.py` en el entorno configurado y revisa manualmente los archivos nuevos por datos sensibles.
5. Revisa `git status --short` y `git diff`; revisa también los archivos nuevos, que `git diff` no muestra hasta incorporarlos al índice. Haz commits pequeños cuando decidas versionar.

## Cerrar un proyecto

Completa `evidence/completion.md` con objetos/paquetes, cambio exacto, lint/sintaxis, activación, Unit/ATC o motivo de no aplicación, lectura posterior, inactivos, dependencias, transporte, riesgos y reversión. Marca `completed` solo con esos resultados documentados. Si dejas de mantenerlo, usa `archived` y registra si quedó terminado o abandonado. Archivar aquí no ejecuta operaciones SAP.

## Revisión de aprendizaje

Al terminar una sesión, identifica un siguiente paso concreto. Periódicamente revisa la [ruta de aprendizaje](../../learning/roadmap.md), retira duplicados y enlaza ejercicios completados a su evidencia. Mantén la revisión trimestral ya registrada en el backlog global; esta guía no programa automatizaciones.
