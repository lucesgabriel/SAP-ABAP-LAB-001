# ABAP Quality Gate

Ejecutar antes de construir, antes de probar y antes de cerrar.

## Knowledge-base (consulta inicial obligatoria)

- [ ] `docs/historical-context.md` leído; cada código abierto en el KB.
- [ ] `knowledge-base/solution-patterns.md`: patrón base citado en `docs/design.md` (o justificado que no aplica).
- [ ] `knowledge-base/error-catalog.md`: errores a prevenir copiados a `docs/error-log.md`.
- [ ] `knowledge-base/decision-registry.md`: decisiones reutilizadas citadas.
- [ ] `knowledge-base/released-api-recipes.md`: recetas aplicables identificadas.
- [ ] `knowledge-base/lessons-learned-index.md`: proyectos similares revisados.

## Requerimiento

- [ ] Objetivo de negocio y resultado observable claros.
- [ ] Objetos existentes, paquete y dependencias leídos en SAP (fecha y herramienta).
- [ ] Tecnología elegida con `standards/technology-decision-matrix.md`.
- [ ] Nivel clean core objetivo definido.

## Diseño

- [ ] Tabla de objetos con nombres según `standards/naming-conventions.md` y paquete verificado (`D-007`).
- [ ] Tabla de reemplazos clásico → liberado con `API_STATE` leído (`D-008`, `R-007`).
- [ ] Orden de escritura/activación definido (RAP: `P-003`).
- [ ] Estrategia de pruebas definida (Unit, ATC variante, funcional).
- [ ] `docs/decision-log.md` con paquete, APIs, pruebas y clean core.
- [ ] Pasos de reversión descritos en `transports/README.md`.

## Build

- [ ] SAPLint ejecutado y avisos clasificados (`TOOL-004`).
- [ ] `SAPDiagnose action=syntax version=inactive` limpio antes de activar.
- [ ] Cambios con diff mínimo (`D-009`); objetos estándar intactos salvo autorización explícita.
- [ ] Activación correcta; `INACTIVE_OBJECTS` vacío.
- [ ] Lectura posterior coincide con `src/`.
- [ ] Sin secretos ni datos sensibles en `src/`, `evidence/`, logs.
- [ ] Errores de la sesión registrados en `docs/error-log.md` con taxonomía.

## Test

- [ ] Caso principal reproducido con resultado esperado.
- [ ] Casos límite y de error en `tests/plan.md` con resultado real.
- [ ] ABAP Unit ejecutado (o motivo concreto de no aplicación).
- [ ] ATC con la variante definida; hallazgos P1 en 0 o con decisión registrada.
- [ ] Evidencias sanitizadas en `evidence/`.

## Cierre

- [ ] `evidence/completion.md` completo con evidencia real.
- [ ] `docs/error-log.md` y `docs/decision-log.md` con tags válidos y `YES`/`PARTIAL`/`NO` decididos.
- [ ] Patrón o receta nuevos redactados en el KB si procede.
- [ ] `ready_to_consolidate: true`.
- [ ] `close_project.py --dry-run` revisado y luego ejecutado.
- [ ] `lint_knowledge_base.py` y `validate_structure.py` en PASS.
- [ ] `git status` revisado; commits pequeños.
