# Diseño

## Problema y aceptación

Crear una versión ABAP Cloud del report clásico `ZR_ALV_EQUIPOS_GL` (lista de equipos PM con ALV), siguiendo el caso práctico de migración: (1) sustituir tablas SAP por vistas CDS liberadas y (2) eliminar report, pantalla de selección y ALV, reemplazándolos por una clase global con `IF_OO_ADT_CLASSRUN` y salida en la consola de ADT.

Aceptación: ATC `ABAP_CLOUD_READINESS` sin hallazgos en el objeto nuevo. El report original se conserva sin cambios para comparar.

## Contexto leído en SAP

- Fecha y herramienta de lectura: 2026-09-20, ARC-1 (`sap-arc1-s4h-100`).
- Objeto origen: `ZR_ALV_EQUIPOS_GL` (PROG, `$TMP`). ATC `ABAP_CLOUD_READINESS`: 41 hallazgos (34 prioridad 1, 7 prioridad 2): tipo PROG no permitido, sentencias de report/dynpro, FORMs, `sy-langu`/`sy-repid`, acceso a `EQUI`/`EQKT`, clases `CL_SALV_*`.
- APIs de reemplazo y estado de release comprobado (`SAPRead type=API_STATE`):
  - `I_Equipment`: C1 liberado, uso en ABAP Cloud = sí.
  - `I_EquipmentText`: C1 liberado, uso en ABAP Cloud = sí. Sin duplicados por Equipment+Language en este sistema.
- Estrategia de transporte: ninguna; objeto local `$TMP`.

## Solución y decisiones locales

| Clásico (`ZR_ALV_EQUIPOS_GL`) | Cloud (`ZCL_EQUIPOS_CLOUD_GL`) |
| --- | --- |
| `REPORT` + eventos | Clase global `FINAL` + `IF_OO_ADT_CLASSRUN~main` |
| `SELECT-OPTIONS` / `PARAMETERS` | Estructura `ty_criterios` (rangos + `max_rows`) como parámetro de `get_equipos`; valores por defecto en `get_criterios_default` |
| `EQUI` | `I_Equipment` |
| `EQKT` (SPRAS = `sy-langu`) | `I_EquipmentText` (Language = `cl_abap_context_info=>get_user_language_abap_format( )`) |
| `CL_SALV_TABLE` | `out->write( tabla )` |
| `MESSAGE` | `out->write( texto )` |
| `FORM` / `PERFORM` | Métodos |

Mapeo de campos: EQUNR→Equipment, EQKTX→EquipmentName, EQTYP→EquipmentCategory, EQART→TechnicalObjectType, HERST→AssetManufacturerName, TYPBZ→ManufacturerPartTypeName, SERGE→ManufacturerSerialNumber, ERDAT→CreationDate, ERNAM→CreatedByUser.

- Alternativa descartada: modificar el report original (se pidió una versión nueva; además PROG no es un tipo válido en ABAP Cloud).
- Orden: create → sintaxis (inactive) → correcciones → activar → ATC.
- Riesgos y reversión: ver [transportes](../transports/README.md) y la ficha de cierre.
