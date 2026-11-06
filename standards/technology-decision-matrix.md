# Matriz De Decisión Tecnológica ABAP

Usa esta matriz para no forzar todos los requerimientos a un report ni a un RAP BO. Deja la clasificación en `docs/design.md` y la justificación en `docs/decision-log.md`.

| Si el requerimiento dice... | Considera primero | Complementa con | Preguntas clave |
|---|---|---|---|
| "Listar / consultar datos con filtros" | CDS view entity (+ consumo vía clase o Fiori) | `IF_OO_ADT_CLASSRUN` para validar; Fiori Elements List Report si hay usuarios | ¿Quién consume? ¿Volumen? ¿Autorizaciones? |
| "Report clásico existente hay que modernizar" | Clase global + CDS liberadas (`P-001`) | ATC antes/después (`P-005`) | ¿Se conserva el original? ¿Nivel clean core? |
| "Crear / modificar / borrar registros con UI" | RAP managed con draft | Fiori Elements Object Page, DCLS | ¿Numbering? ¿Locking? ¿Validaciones? |
| "Persistencia ya existe con lógica propia (BAPI, clase legacy)" | RAP unmanaged | Wrapper de la lógica existente | ¿La API es liberada? ¿Transaccionalidad? |
| "Cálculo pesado sobre muchos registros" | ABAP SQL moderno (CTE, window functions) | AMDP solo si SQL no alcanza | ¿Se puede expresar en SQL? ¿Índices? |
| "Agregación analítica / KPI" | CDS analítica (`@Analytics`) o table function | AMDP table function | ¿Dimensiones? ¿Autorización por datos? |
| "Cambiar comportamiento estándar sin modificar" | BAdI nuevo (enhancement framework) | Key-user extensibility si existe | ¿Hay BAdI liberada? ¿Nivel clean core aceptable? |
| "Consumir servicio externo / S/4 OData" | HTTP client liberado + destino | Receta `R-006` para CSRF | ¿Auth? ¿CSRF? ¿Idempotencia? |
| "Exponer datos a un sistema externo" | RAP + service binding Web API (OData V4) | APIM si hay consumidores externos (ver Integration Suite Lab) | ¿Versionado? ¿Quota? |
| "Validar reglas de negocio reutilizables" | Clase con interfaz + ABAP Unit | Inyección de dependencias para test doubles | ¿Se puede probar sin BD? |
| "Job / proceso en background" | Clase + Application Job (cloud) o report + variante (clásico) | Application log | ¿Reinicio? ¿Monitoreo? |
| "Autorización por datos" | DCL sobre CDS | Objeto de autorización `Z` + `AUTHORITY-CHECK` en clase | ¿Campo de restricción? ¿Rol? |

## Reglas de selección

- Si el valor principal es exponer datos con filtros → empezar por CDS.
- Si hay transacciones (crear/modificar) con UI → RAP managed, draft por defecto.
- Si existe lógica de persistencia legacy fiable → RAP unmanaged envolviéndola, no reescribirla.
- Si es rendimiento → primero SQL moderno; AMDP solo con evidencia de que SQL no alcanza.
- Si es extender estándar → BAdI antes que enhancement implícito; nunca modificación.
- Si es consumo externo → resolver auth/CSRF antes del diseño final (`P-004`).
- Nivel clean core objetivo: `A` por defecto para código nuevo; `B`/`C` solo con decisión registrada.

## Anti-patrones

- Crear un report ALV nuevo cuando el objetivo es cloud readiness.
- Ir a AMDP sin probar ABAP SQL moderno.
- Acceder a tablas SAP cuando existe vista `I_*` liberada (`D-008`).
- RAP unmanaged "porque da más control" sin lógica legacy que lo justifique.
- Publicar service binding con objetos inactivos (`P-003`).
- Exentar hallazgos ATC P1 para pasar un gate.
- Diseñar sin leer `API_STATE`, paquete ni transporte en el sistema real.

## Changelog

| Fecha | Cambio |
|---|---|
| 2026-10-01 | Versión inicial adaptada de la capability decision matrix del Integration Suite Lab. |
