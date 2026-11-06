# Convenciones De Nombres

Prefijo de cliente del laboratorio: `Z`. Sufijo personal opcional `_GL` cuando se quiera distinguir autor (como en `ZCL_EQUIPOS_CLOUD_GL`). Los nombres de objeto se verifican en SAP antes de usarse en un brief o diseño; un nombre libre en el diseño no garantiza que esté libre en el sistema.

## Paquetes

| Uso | Nombre | Notas |
|---|---|---|
| Desechable | `$TMP` | Sin transporte; el compilador no impone versión de lenguaje (`ATC-001`). |
| Entrenamiento durable | `ZLAB_<DOMINIO>` (`ZLAB_OO`, `ZLAB_RAP`, `ZLAB_CDS`) | Crear con capa/target verificados; registrar en `config/system.yaml` cuando existan. |
| Cloud-ready | `ZLAB_CLOUD_<tema>` con versión de lenguaje "ABAP for Cloud Development" | Decisión `D-007`. |

## Objetos ABAP

| Tipo | Patrón | Ejemplo |
|---|---|---|
| Clase global | `ZCL_<tema>[_<sufijo>]` | `ZCL_EQUIPOS_CLOUD_GL` |
| Interfaz | `ZIF_<tema>` | `ZIF_EQUIPOS_READER` |
| Clase de excepción | `ZCX_<tema>` | `ZCX_EQUIPO_NOT_FOUND` |
| Clase de test local | `LTC_<tema>` en include de test | `LTC_GET_EQUIPOS` |
| Report (solo clásico) | `ZR_<tema>` | `ZR_ALV_EQUIPOS_GL` |
| Tabla | `Z<tema>` (≤16) con `_D` para draft | `ZLAB_ORDEN`, `ZLAB_ORDEN_D` |
| Elemento de datos / dominio | `ZDE_<campo>` / `ZDO_<campo>` | `ZDE_PRIORIDAD` |
| CDS vista base (RAP) | `ZR_<Entidad>` | `ZR_MaintOrder` |
| CDS proyección (RAP) | `ZC_<Entidad>` | `ZC_MaintOrder` |
| CDS interface view (reuso) | `ZI_<Entidad>` | `ZI_EquipmentBasic` |
| CDS consumo / analítica | `ZC_<Entidad>Query` | `ZC_EquipmentQuery` |
| Metadata extension | mismo nombre que la proyección | `ZC_MaintOrder` |
| Access control (DCL) | mismo nombre que la vista | `ZR_MaintOrder` |
| Behavior definition | mismo nombre que la vista raíz | `ZR_MaintOrder` |
| Behavior pool | `ZBP_<Entidad>` | `ZBP_MaintOrder` |
| Service definition | `ZSD_<Entidad>` | `ZSD_MaintOrder` |
| Service binding | `ZSB_<Entidad>_O4` / `_O2` / `_WEB` | `ZSB_MaintOrder_O4` |
| AMDP | clase `ZCL_<tema>_AMDP`, método `<verbo>_<objeto>` | `ZCL_EQUIPOS_AMDP=>GET_SUMMARY` |
| BAdI implementation | `ZIM_<badi>_<tema>` | `ZIM_WORKORDER_CHECK` |
| Enhancement implementation | `ZEI_<objeto>_<tema>` | `ZEI_IW31_VALIDAR` |

## Dentro del código (Clean ABAP)

- Métodos: verbo + objeto en inglés o español consistente dentro de la clase (`get_equipos`, `get_criterios_default`). Sin prefijos húngaros en nombres de métodos.
- Variables locales: `lv_`/`ls_`/`lt_`/`lo_` aceptados por compatibilidad con el código existente del laboratorio; en código nuevo cloud se prefiere sin prefijo cuando el tipo es evidente (`DATA(equipos) = ...`). Elegir un estilo por clase y no mezclar.
- Parámetros: `is_`/`it_`/`iv_` (import), `es_`/`et_`/`ev_` (export), `rs_`/`rt_`/`rv_` (returning), `cs_`/`ct_`/`cv_` (changing), o sin prefijo en estilo cloud; consistente por clase.
- Tipos: `ty_<nombre>` (estructura), `ty_t_<nombre>` (tabla), `ty_r_<nombre>` (rango).
- Constantes: `co_<nombre>` o enumeraciones `BEGIN OF ENUM`.
- Símbolos de texto para cualquier literal visible al usuario (`ATC-002`).
- Un método, una responsabilidad; máximo ~40 líneas como guía; sin `SELECT` dentro de loops.

## Archivos locales del laboratorio

| Elemento | Patrón | Ejemplo |
|---|---|---|
| Proyecto | `<prefijo>-<NNN>-<tema>` | `rap-002-ordenes-draft` |
| Caso | `ABAP-CASE-<DOM>-<NNN>-<slug>` (lo asigna el generador) | `ABAP-CASE-RAP-001-ordenes-con-draft` |
| Código exportado | `<objeto en minúsculas>.<tipo>.abap` | `zcl_equipos_cloud_gl.clas.abap` |
| Evidencia | `YYYY-MM-DD-<tema>.md` | `2026-09-20-console-run.md` |
| Códigos KB | `<CAP>-NNN`, `P-NNN`, `D-NNN`, `R-NNN` | `OO-001`, `P-003` |

## Changelog

| Fecha | Cambio |
|---|---|
| 2026-10-01 | Versión inicial, consolidando `learning/patterns.md`, `docs/guides/organization.md` y los nombres usados en `abap-001`. |
