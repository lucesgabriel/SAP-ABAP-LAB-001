# Biblioteca De Patrones De Solución ABAP

Patrones validados en proyectos o casos cerrados del laboratorio. Cada patrón es un esqueleto reutilizable: capability, contexto, componentes mínimos, riesgos y evidencia.

> Antes de diseñar, buscar aquí un patrón base y adaptarlo al objeto real. Si el caso es nuevo y la solución funciona, redactar la entrada `P-NNN` al cierre del proyecto. No guardar propuestas como patrones aprobados: un patrón requiere activación, prueba y lectura posterior en SAP.

---

## P-001 | Report ALV clásico → clase ABAP Cloud con CDS liberadas

**TAGS:** OO, CLEAN_CORE, REUSE_YES

- **Cuándo aplicar:** Hay un report `Z*` con pantalla de selección, acceso a tablas SAP (`EQUI`, `MARA`, `VBAK`...) y salida ALV, y se quiere una versión apta para ABAP Cloud / clean core nivel A.
- **Componentes:**
  - Clase global `FINAL` que implementa `IF_OO_ADT_CLASSRUN`.
  - Estructura de criterios (`ty_criterios`: rangos + `max_rows`) como parámetro del método de lectura; método `get_criterios_default` reemplaza los valores por defecto de la pantalla de selección.
  - Vistas CDS liberadas (`I_*` con contrato C1) en lugar de tablas SAP; `LEFT OUTER JOIN` con `I_*Text` filtrando por idioma.
  - `cl_abap_context_info=>get_user_language_abap_format( )` en lugar de `sy-langu` (capturar `cx_abap_context_info_error`, ver `OO-001`).
  - `out->write( )` en lugar de `CL_SALV_TABLE` y `MESSAGE`; símbolos de texto para literales (`ATC-002`).
  - `FORM`/`PERFORM` → métodos privados.
- **Orden:** `SAPWrite create` → `SAPDiagnose syntax version=inactive` → correcciones por método → `SAPActivate` → `SAPDiagnose atc variant=ABAP_CLOUD_READINESS` sobre original y nuevo → `SAPRead force_refresh`.
- **Riesgos:** Elegir una vista CDS no liberada (comprobar `API_STATE` antes, `D-008`); `$TMP` no impone la versión de lenguaje (`ATC-001`); diferencias semánticas entre tabla y vista (duplicados por idioma, campos calculados).
- **Mitigaciones:** Conservar el report original sin cambios para comparar; documentar la tabla de mapeo campo a campo en `docs/design.md`; recetas `R-001` a `R-005`.
- **Evidencia:** `projects/abap-001-equipos-cloud` — `ZR_ALV_EQUIPOS_GL` (41 hallazgos ATC) → `ZCL_EQUIPOS_CLOUD_GL` (0 hallazgos), ejecución F9 con 322 registros.

---

## P-002 | Flujo de cambio seguro con ARC-1

**TAGS:** TOOL, OPERATIONS, REUSE_YES

- **Cuándo aplicar:** Cualquier escritura en SAP desde un agente (Claude, Hermes, Codex) a través de ARC-1.
- **Componentes:**
  1. `SAPContext` → `SAPSearch`/`SAPRead`: paquete, dependencias, API release, transportes.
  2. Diseño con diff mínimo; para clases preferir `edit_method` / `edit_class_definition` sobre reemplazo completo.
  3. `SAPLint` + `SAPDiagnose action=syntax version=inactive`.
  4. `SAPWrite` (nunca afirmar que compila porque el write respondió).
  5. `SAPActivate` (batch para dos o más objetos).
  6. `SAPRead force_refresh` + `INACTIVE_OBJECTS` limpio + ABAP Unit/ATC cuando aplique.
  7. Ficha de cierre `evidence/completion.md` + logs con taxonomía.
- **Riesgos:** Confundir capacidad técnica con autorización (`D-004`); confirmar acciones irreversibles inmediatamente antes de ejecutarlas.
- **Evidencia:** `learning/patterns.md` (origen), `projects/abap-001-equipos-cloud/evidence/completion.md`.

---

## P-003 | Orden de activación de un business object RAP

**TAGS:** RAP, ACTIVATION, REUSE_YES

- **Cuándo aplicar:** Crear o modificar varios objetos interdependientes de un BO RAP.
- **Componentes:** `TABL` → `DDLS` (vista base, luego proyección) → `DCLS` → `BDEF` (base, luego proyección) → behavior pool (`CLAS`) → `SRVD` → `SRVB`.
- **Orden:** Escritura por lotes en ese orden; activación batch terminal; revisar `INACTIVE_OBJECTS` después de cada lote; ejecutar revisión Clean Core y ATC antes de publicar el service binding.
- **Riesgos:** Activar la proyección antes que la base; publicar el binding con objetos inactivos; olvidar la `DCLS` y exponer datos sin control de acceso.
- **Evidencia:** Documentado desde `learning/patterns.md`; pendiente de validación completa en un proyecto `rap-NNN` (ver `cases/`).

---

## P-004 | Diagnóstico de CSRF en OData: sesión antes que token

**TAGS:** API, CONNECTIVITY, REUSE_YES

- **Cuándo aplicar:** Cualquier `403 CSRF token validation failed` al llamar un servicio OData V2/V4 desde Bruno, Postman, PowerShell, Groovy o un cliente ABAP.
- **Componentes:**
  1. Hacer dos GET consecutivos con `x-csrf-token: fetch` y comparar el `SAP_SESSIONID_*` de ambas respuestas.
  2. Si difieren → problema de cookie: reinyectar `sap-usercontext` y `SAP_SESSIONID` como cabecera `Cookie` explícita (sobre HTTP, `Secure=false`).
  3. Parsear `set-cookie` por pares `nombre=valor` con regex (SAP los manda en una cadena separada por coma).
  4. Solo entonces revisar el token.
- **Riesgos:** Perder horas corrigiendo el token cuando la sesión se reinicia en cada petición (`API-001`); Safe Mode del cliente ignorando scripts (`TOOL-001`).
- **Evidencia:** `scripts/diag-csrf.ps1`, `artifacts/bruno/CROWN-API_MAINTNOTIFICATION`, avisos creados en `QMEL`.

---

## P-005 | ATC antes/después como evidencia de migración clean core

**TAGS:** ATC, CLEAN_CORE, REUSE_YES

- **Cuándo aplicar:** Cualquier refactor cuyo objetivo sea cloud readiness o reducción de nivel clean core (D → C → B → A).
- **Componentes:**
  - `SAPDiagnose action=atc variant=ABAP_CLOUD_READINESS` sobre el objeto original: guardar recuento por prioridad.
  - Mismo chequeo sobre el objeto nuevo.
  - Variante por defecto además, para capturar infos SLIN (`ATC-002`).
  - Tabla "antes/después" en `evidence/completion.md` separando hallazgos del objeto de hallazgos de sistema (`ATC-003`).
- **Riesgos:** Declarar cloud-ready un objeto que solo activó limpio en `$TMP` (`ATC-001`).
- **Evidencia:** `projects/abap-001-equipos-cloud` (41 → 0).

---

## Plantilla para nuevos patrones

```markdown
## P-NNN | Título del patrón

**TAGS:** <capability>, <categoría>, REUSE_YES|REUSE_PARTIAL

- **Cuándo aplicar:**
- **Componentes:**
- **Orden:**
- **Riesgos:**
- **Mitigaciones:**
- **Evidencia:** (proyecto o caso cerrado, ruta a la ficha de cierre)
```

## Changelog

| Fecha | Cambio |
|---|---|
| 2026-10-01 | Versión inicial: P-001 a P-005 promovidos desde `learning/patterns.md`, `learning/lessons.md` y `projects/abap-001-equipos-cloud`. |
