# Taxonomía Del Knowledge Base ABAP

Taxonomía obligatoria para clasificar errores, decisiones, patrones y recetas. Todo registro en `error-catalog.md`, `solution-patterns.md`, `decision-registry.md`, `released-api-recipes.md` y en los logs por proyecto (`docs/error-log.md`, `docs/decision-log.md`) usa estos tags exactos. El linter (`scripts/workspace/lint_knowledge_base.py`) rechaza cualquier tag fuera de esta lista.

## Capability (área ABAP afectada)

| Tag | Cubre |
|---|---|
| `OO` | ABAP Objects, Clean ABAP, clases globales/locales, interfaces, excepciones, `IF_OO_ADT_CLASSRUN`. |
| `CDS` | Core Data Services: view entities, asociaciones, anotaciones, access control (DCL), metadata extensions, table functions. |
| `RAP` | RESTful ABAP Programming Model: BDEF, behavior pool, EML, draft, acciones, validaciones, determinaciones, service definition/binding. |
| `SQL` | ABAP SQL moderno, AMDP, SQLScript, rendimiento de acceso a datos, `cl_osql_test_environment`. |
| `DDIC` | Diccionario: tablas, estructuras, elementos de datos, dominios, ayudas de búsqueda, índices. |
| `ENH` | Extensibilidad: BAdI, enhancement spots, user exits, key-user extensibility, implicit/explicit enhancements. |
| `API` | Consumo o exposición de APIs: OData V2/V4, HTTP client, released APIs (C0–C4), SEGW, comunicación con sistemas externos. |
| `UI` | Fiori Elements, UI5, FLP, anotaciones `@UI`, despliegue de repositorio UI5. |
| `CTS` | Transportes: paquetes, órdenes, capas, gCTS, abapGit, versión de lenguaje del paquete, `$TMP` vs Z/Y. |
| `ATC` | ABAP Test Cockpit, variantes de chequeo, Cloud Readiness, Clean Core, exenciones, prioridad de hallazgos. |
| `UNIT` | ABAP Unit, test doubles, CDS/SQL test environment, RAP BO test double, inyección de dependencias. |
| `TOOL` | Herramientas del laboratorio: ARC-1 MCP, ADT, Eclipse, Bruno/Postman, scripts del workspace, Claude/Hermes/Codex. |
| `SEC` | Autorizaciones, objetos de autorización, IAM, CSRF, certificados TLS, secretos. |
| `MULTI` | El registro cruza varias capabilities. |

## Categoría (naturaleza técnica)

| Tag | Cubre |
|---|---|
| `SYNTAX` | Errores de sintaxis, advertencias del compilador, ABAP Doc, símbolos de texto, pretty printer. |
| `ACTIVATION` | Activación, objetos inactivos, orden de dependencias, activación batch, inconsistencias de DDIC. |
| `DEPENDENCY` | Where-used, dependencias entre objetos, APIs no liberadas, release contracts, paquetes/interfaces de paquete. |
| `DATA_MODEL` | Modelado CDS/DDIC, semántica de moneda/unidad, claves, asociaciones, cardinalidad. |
| `BEHAVIOR` | Lógica RAP: validaciones, determinaciones, acciones, draft, numbering, locking, ETags. |
| `CLEAN_CORE` | Nivel de clean core (A/B/C/D), cloud readiness, wrappers, sustitución de objetos SAP por APIs liberadas. |
| `PERFORMANCE` | Selecciones, loops, índices, buffering, memoria, `SELECT` en loops, paralelismo, AMDP vs ABAP. |
| `AUTHORIZATION` | `AUTHORITY-CHECK`, DCL, roles, IAM apps, S_DEVELOP, acceso a datos. |
| `CONNECTIVITY` | HTTP/OData, destinos, CSRF, cookies, TLS, ICF, endpoints, comunicación con sistemas externos. |
| `TESTING` | Diseño de pruebas, test doubles, fixtures, cobertura, datos sintéticos. |
| `TRANSPORT` | Órdenes, paquetes, capas, liberación, gCTS, abapGit, versión de lenguaje. |
| `TOOLING` | Comportamiento de ARC-1, ADT, Bruno/Postman, scripts, agentes; falsos positivos de herramientas. |
| `NAMING` | Convenciones de nombres de objetos, paquetes, métodos, variables. |
| `OPERATIONS` | Runbook, evidencias, reversión, monitoreo, proceso del laboratorio. |

## Severidad

| Tag | Significa |
|---|---|
| `BLOCKER` | Impide escribir, activar, transportar o ejecutar. |
| `MAJOR` | Funcional fallando o hallazgo ATC prioridad 1/2; workaround posible; requiere fix antes de dar por terminado. |
| `MINOR` | Cosmético, documental, hallazgo informativo u optimización. |

## Reutilizable

| Tag | Significa |
|---|---|
| `REUSE_YES` | La solución sirve para futuros proyectos con contexto similar. |
| `REUSE_PARTIAL` | La idea sirve; los detalles dependen del sistema, paquete o release. |
| `REUSE_NO` | Caso muy específico, no generalizable. No se promueve al KB. |

## Origen del aprendizaje

| Tag | Significa |
|---|---|
| `DESIGN` | Detectado leyendo contexto en SAP o diseñando. |
| `BUILD` | Detectado al escribir código (lint, sintaxis). |
| `ACTIVATE` | Detectado al activar o al leer objetos inactivos. |
| `TEST` | Detectado en ABAP Unit, ATC, ejecución en consola o pruebas HTTP. |
| `TRANSPORT` | Detectado al asignar paquete, orden o al liberar. |
| `PROD` | Detectado en un sistema productivo o de cliente real. |

## Formato de registro

Cada entrada en los catálogos lleva una línea de metadatos con todos los tags aplicables:

```text
**TAGS:** OO, CLEAN_CORE, MAJOR, REUSE_YES, TEST
```

- Errores (`error-catalog.md`): capability + categoría + severidad + reutilizable + origen.
- Patrones (`solution-patterns.md`): capability + categoría + reutilizable.
- Decisiones (`decision-registry.md`): capability + categoría + reutilizable.
- Recetas (`released-api-recipes.md`): capability + categoría + reutilizable.

Múltiples capabilities o categorías se separan con coma. Si la entrada cruza capabilities, usar `MULTI` como capability y dejar las específicas en categoría o en el texto.

## Códigos

| Catálogo | Formato | Ejemplo |
|---|---|---|
| Errores | `<CAPABILITY>-<NNN>` secuencial por capability | `RAP-003`, `TOOL-002` |
| Patrones | `P-<NNN>` | `P-001` |
| Decisiones | `D-<NNN>` | `D-004` |
| Recetas | `R-<NNN>` | `R-002` |
| Casos de práctica | `ABAP-CASE-<DOMINIO>-<NNN>` | `ABAP-CASE-RAP-001` |

Los códigos nunca se reutilizan ni se renumeran. Una entrada obsoleta se marca `**Estado:** obsoleta` con la fecha y el código que la reemplaza.

## Dominios de casos de práctica

| Dominio | Capability KB | Cubre |
|---|---|---|
| `OO` | `OO` | Clases, Clean ABAP, refactor de reports a clases. |
| `CDS` | `CDS` | Vistas, asociaciones, anotaciones, access control. |
| `RAP` | `RAP` | Business objects managed/unmanaged, draft, acciones, OData. |
| `SQL` | `SQL` | ABAP SQL moderno, AMDP, rendimiento. |
| `ENH` | `ENH` | BAdI, enhancements, clean core de extensiones. |
| `API` | `API` | Consumir/exponer OData y HTTP, released APIs. |
| `UI` | `UI` | Fiori Elements sobre RAP, anotaciones UI. |
| `MIX` | `MULTI` | Caso integrador que cruza varias capabilities. |

## Changelog

| Fecha | Cambio |
|---|---|
| 2026-10-01 | Versión inicial de la taxonomía ABAP, adaptada del SAP Integration Suite Codex Lab. |
