# RAP Release Gate

Antes de publicar un service binding o dar por terminado un business object RAP.

## Modelo de datos

- [ ] Tabla(s) con clave técnica adecuada (UUID si early numbering) y campos administrativos (`created_by`, `created_at`, `last_changed_by`, `last_changed_at`, `local_last_changed_at`).
- [ ] Tabla de draft generada/activa si el BO es draft-enabled.
- [ ] Vista base `R_`/`ZR_` y proyección `C_`/`ZC_` con nombres según `standards/naming-conventions.md`.
- [ ] Semántica de moneda/unidad en campos `CURR`/`QUAN` (`D-010`).
- [ ] Asociaciones y composiciones con cardinalidad correcta; `root` definido.

## Comportamiento

- [ ] BDEF base: implementation type (managed/unmanaged), `persistent table`, `lock master`, `authorization master`, `etag master`, numbering.
- [ ] BDEF de proyección con `use` de las operaciones expuestas.
- [ ] Validaciones con mensajes (`reported`) y `failed` correctamente llenos.
- [ ] Determinaciones con trigger adecuado (`on modify` / `on save`).
- [ ] Acciones con `features: instance` cuando dependen del estado.
- [ ] Draft: `with draft`, `draft table`, `draft action Edit/Activate/Discard/Resume` y `total etag`.

## Acceso y exposición

- [ ] DCLS para la vista base (`D-011`); no exponer sin control de acceso.
- [ ] Service definition expone solo las entidades necesarias.
- [ ] Service binding (OData V4 UI o Web API) publicado solo con todos los objetos activos (`P-003`).
- [ ] Anotaciones `@UI` en metadata extension, no en la vista (si hay Fiori).

## Verificación

- [ ] Orden de activación respetado y batch sin inactivos.
- [ ] Preview Fiori o llamada OData reproducida y resumida en `evidence/`.
- [ ] ABAP Unit del behavior pool con RAP BO test double o EML en test.
- [ ] ATC variante por defecto y, si aplica, `ABAP_CLOUD_READINESS`.
- [ ] Decisiones de numbering, locking y draft registradas en `docs/decision-log.md`.
