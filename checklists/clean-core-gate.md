# Clean Core Gate

Cuando el objetivo del proyecto es cloud readiness o reducir el nivel clean core (D → C → B → A).

## Antes de diseñar

- [ ] Nivel objetivo definido y registrado (`A` solo APIs liberadas; `B` wrappers sobre no liberadas; `C` objetos clásicos sin modificar estándar; `D` modificaciones).
- [ ] ATC `ABAP_CLOUD_READINESS` sobre el objeto original ejecutado y recuento por prioridad guardado (`P-005`).
- [ ] Inventario de construcciones a reemplazar: tablas SAP, `sy-*`, `CL_SALV_*`, `MESSAGE`, `FORM`, dynpro, `CALL FUNCTION` no liberadas.

## Reemplazos

- [ ] Para cada construcción, receta `R-XXX` aplicada o decisión registrada si no hay reemplazo.
- [ ] `API_STATE` leído en el sistema real para cada vista/clase liberada (`D-008`, `R-007`).
- [ ] Excepciones de las APIs liberadas capturadas (`OO-001`).
- [ ] Literales de usuario con símbolos de texto (`ATC-002`).
- [ ] Sin acceso directo a tablas SAP; sin `sy-langu`/`sy-uname`/`sy-datum`.

## Verificación

- [ ] ATC `ABAP_CLOUD_READINESS` sobre el objeto nuevo: 0 hallazgos o cada uno con decisión registrada.
- [ ] Recordatorio: en `$TMP` el compilador no impone la versión de lenguaje; solo ATC lo demuestra (`ATC-001`). Para imponerla, paquete con versión "ABAP for Cloud Development" (`D-007`).
- [ ] Hallazgos de sistema separados de hallazgos del objeto (`ATC-003`).
- [ ] Tabla antes/después en `evidence/completion.md`.
- [ ] Objeto original conservado sin cambios para comparar (si es migración).

## Cierre

- [ ] Nuevas recetas de reemplazo descubiertas redactadas en `released-api-recipes.md`.
- [ ] Decisiones de wrapper o aceptación de nivel B/C promovidas al registry.
