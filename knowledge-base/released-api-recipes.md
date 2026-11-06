# Recetario De Reemplazos Y APIs Liberadas

Equivalente ABAP del recetario de credenciales del Integration Suite Lab: recetas paso a paso para sustituir construcciones clásicas por APIs liberadas (clean core nivel A), consumir servicios OData y comprobar estados de release. Cada receta se valida en un proyecto antes de entrar aquí.

> Antes de migrar un objeto clásico, buscar aquí la receta por tipo de construcción. Si una receta falla en un sistema o release, registrar la variante con el contexto que la diferencia.

## Índice

| Código | Clásico | Reemplazo | Capability |
|---|---|---|---|
| `R-001` | `EQUI` / `EQKT` | `I_Equipment` / `I_EquipmentText` | API |
| `R-002` | `sy-langu` | `cl_abap_context_info=>get_user_language_abap_format( )` | OO |
| `R-003` | `SELECT-OPTIONS` / `PARAMETERS` | Estructura de rangos como parámetro de método | OO |
| `R-004` | `CL_SALV_TABLE` / `WRITE` | `IF_OO_ADT_CLASSRUN` + `out->write( )` | OO |
| `R-005` | `MESSAGE` / literales | Símbolos de texto + `out->write( )` | OO |
| `R-006` | — | Consumir OData V2 con CSRF desde un cliente HTTP | API |
| `R-007` | — | Comprobar el estado de release de una API con ARC-1 | TOOL |

---

## R-001 | Tabla `EQUI`/`EQKT` → vistas `I_Equipment`/`I_EquipmentText`

**TAGS:** API, CLEAN_CORE, REUSE_YES

1. Comprobar con `R-007` que `I_Equipment` e `I_EquipmentText` tienen contrato C1 y uso en ABAP Cloud en el sistema real.
2. Mapear campos (verificado en `abap-001`): `EQUNR→Equipment`, `EQKTX→EquipmentName`, `EQTYP→EquipmentCategory`, `EQART→TechnicalObjectType`, `HERST→AssetManufacturerName`, `TYPBZ→ManufacturerPartTypeName`, `SERGE→ManufacturerSerialNumber`, `ERDAT→CreationDate`, `ERNAM→CreatedByUser`.
3. Texto por idioma: `LEFT OUTER JOIN I_EquipmentText AS t ON t~Equipment = e~Equipment AND t~Language = @lv_language` (idioma obtenido con `R-002`). Confirmar que no hay duplicados por `Equipment + Language` en el sistema.
4. Mantener `ORDER BY` y `UP TO @max_rows ROWS` (`D-011`).
- **Gotchas:** La vista puede no exponer todos los campos de la tabla; documentar los que no tienen equivalente. Equipos sin texto deben seguir apareciendo (JOIN externo).
- **Evidencia:** `projects/abap-001-equipos-cloud/src/zcl_equipos_cloud_gl.clas.abap`, ejecución F9 con 322 registros.

## R-002 | `sy-langu` → `cl_abap_context_info=>get_user_language_abap_format( )`

**TAGS:** OO, CLEAN_CORE, REUSE_YES

```abap
DATA(lv_language) = VALUE sy-langu( ).
TRY.
    lv_language = cl_abap_context_info=>get_user_language_abap_format( ).
  CATCH cx_abap_context_info_error.
    lv_language = 'E'.
ENDTRY.
```

- **Gotchas:** La excepción es obligatoria (`OO-001`). Otros campos `sy-*`: `sy-uname` → `get_user_technical_name( )`, `sy-datum` → `get_system_date( )`, `sy-uzeit` → `get_system_time( )`.

## R-003 | `SELECT-OPTIONS` / `PARAMETERS` → estructura de criterios

**TAGS:** OO, CLEAN_CORE, REUSE_YES

```abap
TYPES: ty_r_equipment TYPE RANGE OF i_equipment-Equipment,
       BEGIN OF ty_criterios,
         equipment TYPE ty_r_equipment,
         category  TYPE RANGE OF i_equipment-EquipmentCategory,
         max_rows  TYPE i,
       END OF ty_criterios.
METHODS get_criterios_default RETURNING VALUE(rs_criterios) TYPE ty_criterios.
METHODS get_equipos IMPORTING is_criterios TYPE ty_criterios
                    RETURNING VALUE(rt_equipos) TYPE ty_t_equipos.
```

- Los valores por defecto de la pantalla de selección pasan a `get_criterios_default`; el `SELECT` usa `WHERE Equipment IN @is_criterios-equipment`.
- **Gotchas:** Un rango vacío equivale a "sin filtro"; documentar el `max_rows` por defecto.

## R-004 | `CL_SALV_TABLE` / `WRITE` → `IF_OO_ADT_CLASSRUN`

**TAGS:** OO, CLEAN_CORE, REUSE_YES

```abap
CLASS zcl_... DEFINITION PUBLIC FINAL CREATE PUBLIC.
  PUBLIC SECTION.
    INTERFACES if_oo_adt_classrun.
ENDCLASS.
...
METHOD if_oo_adt_classrun~main.
  DATA(lt_equipos) = get_equipos( get_criterios_default( ) ).
  out->write( |{ TEXT-002 }{ lines( lt_equipos ) }| ).
  out->write( lt_equipos ).
ENDMETHOD.
```

- Ejecutar con F9 en ADT; guardar en `evidence/` un resumen de la consola (cabecera, columnas, muestra sanitizada).
- **Gotchas:** SAPLint puede no conocer `IF_OO_ADT_CLASSRUN` (`TOOL-004`). No es sustituto de un Fiori app: para UI real usar RAP + Fiori Elements.

## R-005 | `MESSAGE` y literales → símbolos de texto

**TAGS:** OO, CLEAN_CORE, REUSE_YES

1. `SAPWrite edit_text_symbols` con `001 = 'Sin registros'`, `002 = 'Lista de equipos - registros: '`.
2. Referenciar como `TEXT-001` / `TEXT-002` en `out->write( )`.
3. Volver a ejecutar ATC variante por defecto: la info SLIN desaparece (`ATC-002`).
- **Gotchas:** El archivo `src/<clase>.textsymbols.txt` del proyecto es una copia; la fuente es SAP.

## R-006 | Consumir OData V2 con CSRF desde un cliente HTTP

**TAGS:** API, CONNECTIVITY, REUSE_YES

1. `GET <servicio>/$metadata` (o cualquier entidad) con cabeceras `x-csrf-token: fetch` y `sap-client: 100`.
2. Leer `x-csrf-token` **y** `set-cookie` de la respuesta. Parsear `set-cookie` por pares `nombre=valor` con regex (`API-001`); normalizar el tipo de retorno del helper (`TOOL-002`).
3. Construir la cabecera `Cookie: sap-usercontext=...; SAP_SESSIONID_<SID>_<MANDT>=...`. Sobre HTTP, no depender del cookie jar (flag `secure`).
4. `POST` con `x-csrf-token: <token>`, `Cookie`, `Content-Type: application/json`, `Accept: application/json`.
5. Verificar con un `GET` por clave que el registro existe (`QMEL` para avisos).
- **Herramientas:** Bruno en Developer Mode (`TOOL-001`); colección en `artifacts/bruno/CROWN-API_MAINTNOTIFICATION`; diagnóstico `scripts/diag-csrf.ps1`.
- **Gotchas:** En `/IWFND/GW_CLIENT` nunca pegar el token a mano.

## R-007 | Comprobar el estado de release de una API con ARC-1

**TAGS:** TOOL, DEPENDENCY, REUSE_YES

1. `SAPRead type=API_STATE name=I_Equipment` (o la clase/interfaz).
2. Registrar en `docs/design.md`: contrato (`C0`–`C4`), "uso en ABAP Cloud", release mínimo, fecha y sistema de lectura.
3. Si no está liberada: buscar alternativa en la skill `released-abap-classes`, evaluar wrapper (`abap-cloud` nivel B/C) y registrar decisión `DC-NN`.
- **Gotchas:** El estado puede diferir entre releases; no copiar de memoria ni de otro sistema (`D-008`).

---

## Plantilla para nuevas recetas

```markdown
## R-NNN | Clásico → Reemplazo

**TAGS:** <capability>, <categoría>, REUSE_YES|REUSE_PARTIAL

1. Paso.
2. Paso.
- **Gotchas:**
- **Evidencia:** (proyecto, ruta)
```

## Changelog

| Fecha | Cambio |
|---|---|
| 2026-10-01 | Versión inicial: R-001 a R-007 validadas en `projects/abap-001-equipos-cloud` y en la colección Bruno `CROWN-API_MAINTNOTIFICATION`. |
