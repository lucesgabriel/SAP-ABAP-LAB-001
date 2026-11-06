# Checklist 100% — {{CASE_ID}}

> Marcar TODOS para acercarse al 100%. Cada bloque pesa lo definido en la rúbrica del case-brief.

## Nombres exactos y paquete ({{W_NAMES}}%)

- [ ] Todos los objetos usan el nombre exacto del brief.
- [ ] Prefijos según `standards/naming-conventions.md`.
- [ ] Paquete verificado en SAP (no deducido); `$TMP` solo si el brief lo permite.

## Funcionalidad correcta ({{W_FUNC}}%)

- [ ] `SAPDiagnose action=syntax` limpio sobre la versión inactiva.
- [ ] `SAPActivate` correcto; `INACTIVE_OBJECTS` vacío.
- [ ] Resultado esperado del brief reproducido (consola F9, OData, Fiori preview...).
- [ ] Lectura posterior (`SAPRead force_refresh`) coincide con `src/`.

## Calidad: Clean ABAP, ATC, clean core ({{W_QUALITY}}%)

- [ ] SAPLint ejecutado y avisos clasificados (`TOOL-004`).
- [ ] ATC con la variante indicada; hallazgos del objeto en 0 o justificados.
- [ ] Solo APIs liberadas o wrapper documentado (`D-008`, `R-007`).
- [ ] Sin `SELECT` en loops, columnas explícitas, límites (`D-011`).

## Pruebas ({{W_TEST}}%)

- [ ] ABAP Unit presente cuando la lógica lo permite (test double de CDS/SQL si aplica).
- [ ] Casos límite y de error cubiertos en `tests/plan.md`.

## Seguridad y datos ({{W_SEC}}%)

- [ ] Sin credenciales, tokens ni cookies en código, evidencias ni logs (`SEC-002`).
- [ ] Datos de prueba sintéticos o sanitizados; sin volcados masivos.
- [ ] Autorizaciones / access control consideradas cuando aplica.

## Evidencia y logs ({{W_EVID}}%)

- [ ] `evidence/completion.md` completo con resultados reales.
- [ ] `docs/error-log.md` con tags válidos y filas marcadas `YES/PARTIAL/NO`.
- [ ] `docs/decision-log.md` completo.
- [ ] `docs/design.md` cita los códigos del KB usados.
