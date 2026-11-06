# Prompt: Revisar Calidad Y Verificar

Usa el proyecto `projects/<id>/` del workspace `SAP ABAP LAB 001`. Los objetos están activos. Verifica y documenta; no cierres todavía.

## Skills a cargar

`sap-abap:abap` (abaplint + Clean ABAP), `sap-abap:atc-cloudification` (variantes y niveles clean core), `sap-abap:abap-unit-testing` (test doubles). Como segunda revisión de estilo: `/clean-abap:review` en Claude Code o la skill Clean ABAP de Attila Berencsi.

**Libros de referencia.** Referencia de estilo: `clean-abap-2020` (libro completo); pruebas: `attf-2022` cap.5 y `cds-2024` cap.16; herramientas: `complete-2022` cap.21.

## Tareas

1. **ATC.** Ejecuta `SAPDiagnose action=atc` con la variante que el diseño definió (`ABAP_CLOUD_READINESS` para cloud readiness; además la variante por defecto para infos SLIN, `ATC-002`). Si es una migración, ejecuta la variante sobre el objeto original y el nuevo y registra ambos recuentos por prioridad (`P-005`). Separa hallazgos del objeto de hallazgos de sistema (`ATC-003`).

2. **ABAP Unit.** Ejecuta las pruebas de la clase; si no existen, escribe al menos un test de la lógica principal con test double (`cl_cds_test_environment` / `cl_osql_test_environment` / RAP BO test double) cuando aplique. Si no aplica, explica el motivo concreto en la ficha de cierre.

3. **Funcional.** Reproduce el resultado esperado del diseño (consola F9, OData, preview Fiori) y guarda un resumen sanitizado en `evidence/`.

4. **Clean ABAP y clean core.** Pasa `checklists/abap-quality-gate.md` (secciones Build y Test), `checklists/clean-core-gate.md` si el objetivo es cloud y `checklists/rap-release-gate.md` si hay service binding. Usa las skills `clean-abap`/`abap` para la revisión y corrige con el diff mínimo; cada corrección vuelve a pasar por sintaxis → activación → lectura.

5. **Dependencias.** Confirma where-used y que solo se usan APIs liberadas o wrappers documentados (`D-008`).

6. **Ficha de cierre.** Completa `evidence/completion.md` fila por fila con el resultado real y la evidencia enlazada. No declares PASS desde un write.

7. **Logs.** Añade a `docs/error-log.md` los hallazgos ATC/Unit que requirieron corrección; a `docs/decision-log.md` las decisiones de aceptar o exentar hallazgos.

## Salida esperada

- Tabla ATC antes/después (si aplica) y recuento final por prioridad.
- Resultado de ABAP Unit (o motivo de no aplicación).
- `evidence/completion.md` completo salvo transporte si aún no corresponde.
- Lista de hallazgos aceptados con justificación.

## Restricciones

- Un hallazgo ATC prioridad 1 no se acepta sin decisión registrada y justificada.
- No exentes hallazgos para "pasar": registra la deuda en el backlog.
- Evidencias sin datos sensibles ni volcados masivos (`D-011`).
