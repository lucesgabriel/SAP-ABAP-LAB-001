# Catálogo Central De Errores ABAP

Catálogo consolidado de errores resueltos en proyectos y casos cerrados. Antes de diseñar o depurar, buscar aquí. Al cerrar un proyecto, los errores marcados `REUSE_YES` o `REUSE_PARTIAL` se promueven con `scripts/workspace/close_project.py`.

> Formato obligatorio: cada error usa los tags de `taxonomy.md`. Buscar con Ctrl+F por tag (`RAP`, `CLEAN_CORE`, `CSRF`) para filtrar. Los códigos son secuenciales por capability y nunca se reutilizan.

## Índice por capability

- [OO - ABAP Objects y Clean ABAP](#oo---abap-objects-y-clean-abap)
- [CDS - Core Data Services](#cds---core-data-services)
- [RAP - RESTful ABAP Programming Model](#rap---restful-abap-programming-model)
- [SQL - ABAP SQL y AMDP](#sql---abap-sql-y-amdp)
- [API - OData, HTTP y released APIs](#api---odata-http-y-released-apis)
- [ATC - Test Cockpit y Clean Core](#atc---test-cockpit-y-clean-core)
- [CTS - Transportes y paquetes](#cts---transportes-y-paquetes)
- [SEC - Seguridad y secretos](#sec---seguridad-y-secretos)
- [TOOL - ARC-1, ADT y clientes HTTP](#tool---arc-1-adt-y-clientes-http)
- [Multi-capability](#multi-capability)

---

## OO - ABAP Objects y Clean ABAP

### OO-001 | `CX_ABAP_CONTEXT_INFO_ERROR` no capturada al leer el idioma del usuario

**TAGS:** OO, SYNTAX, MAJOR, REUSE_YES, BUILD

- **Síntoma:** `SAPDiagnose action=syntax` sobre la versión inactiva avisa que la excepción `CX_ABAP_CONTEXT_INFO_ERROR` no está capturada ni declarada.
- **Causa raíz:** `cl_abap_context_info=>get_user_language_abap_format( )` (reemplazo liberado de `sy-langu`) declara esa excepción y la llamada se escribió como si fuera infalible.
- **Solución:** Envolver la llamada en `TRY ... CATCH cx_abap_context_info_error` y definir un valor por defecto (por ejemplo `'E'`) o propagar con `RAISING` en la firma del método.
- **Prevención:** Antes de usar un método de `CL_ABAP_CONTEXT_INFO`, leer su firma con `SAPRead` y revisar las excepciones declaradas.
- **Proyectos referenciados:** `projects/abap-001-equipos-cloud`.

### OO-002 | ABAP Doc mal ubicado genera warning de sintaxis

**TAGS:** OO, SYNTAX, MINOR, REUSE_YES, BUILD

- **Síntoma:** Warning de sintaxis "ABAP Doc comment is not placed before a declaration" (o equivalente) en la versión inactiva.
- **Causa raíz:** El bloque `"!` quedó separado de la declaración que documenta (línea en blanco intermedia o colocado tras la sentencia).
- **Solución:** Mover el comentario `"!` inmediatamente antes de `METHODS`, `CLASS`, `TYPES` o `DATA` sin líneas en blanco; corregir con `SAPWrite edit_class_definition` o `edit_method`.
- **Prevención:** Revisar `SAPDiagnose action=syntax` sobre la versión inactiva antes de activar.
- **Proyectos referenciados:** `projects/abap-001-equipos-cloud`.

---

## CDS - Core Data Services

_(sin entradas consolidadas todavía; registrar en `docs/error-log.md` del proyecto y promover al cierre)_

---

## RAP - RESTful ABAP Programming Model

_(sin entradas consolidadas todavía)_

---

## SQL - ABAP SQL y AMDP

_(sin entradas consolidadas todavía)_

---

## API - OData, HTTP y released APIs

### API-001 | `403 CSRF token validation failed` persistente en POST OData V2 sobre HTTP

**TAGS:** API, CONNECTIVITY, MAJOR, REUSE_YES, TEST

- **Síntoma:** POST a `API_MAINTNOTIFICATION` (OData V2) devuelve siempre `403 CSRF token validation failed`, desde Bruno y desde `/IWFND/GW_CLIENT`, con el token capturado correctamente en el GET previo.
- **Causa raíz:** Dos causas distintas con el mismo mensaje. (1) SAP envía `SAP_SESSIONID_<SID>_<MANDT>` con flag `secure`; sobre `http://` ningún cliente estándar reenvía esa cookie, así que cada petición abre sesión nueva y el token muere con la anterior. (2) SAP manda `sap-usercontext` y `SAP_SESSIONID` en **una sola cadena** `set-cookie` separadas por coma: `split(";")[0]` se queda con la primera y descarta el `SAP_SESSIONID`.
- **Solución:** Reinyectar ambas cookies como cabecera `Cookie` explícita (con `Secure=false` cuando el canal es HTTP) y parsear `set-cookie` recorriendo pares `nombre=valor` con regex, filtrando atributos. Con eso el POST devuelve `201` y dos GET consecutivos comparten token.
- **Prevención:** Ante `CSRF token validation failed`, comparar el `SAP_SESSIONID` de dos respuestas seguidas **antes** de tocar el token: si difieren, el problema es la cookie. En `/IWFND/GW_CLIENT` nunca pegar el token a mano. Receta `R-006`, patrón `P-004`.
- **Evidencia:** `scripts/diag-csrf.ps1`, 2026-09-14; avisos 10000942 y 10000945 confirmados en `QMEL`.
- **Proyectos referenciados:** `artifacts/bruno/CROWN-API_MAINTNOTIFICATION`.

---

## ATC - Test Cockpit y Clean Core

### ATC-001 | En `$TMP` el compilador no detecta usos no liberados; solo ATC `ABAP_CLOUD_READINESS` lo hace

**TAGS:** ATC, CLEAN_CORE, MAJOR, REUSE_YES, TEST

- **Síntoma:** Una clase escrita "para ABAP Cloud" activa sin errores aunque use tablas SAP, `sy-*` o clases no liberadas.
- **Causa raíz:** `$TMP` on-premise no pertenece a un componente de software con versión de lenguaje "ABAP for Cloud Development"; el objeto se compila como ABAP estándar.
- **Solución:** Ejecutar `SAPDiagnose action=atc variant=ABAP_CLOUD_READINESS` sobre el objeto nuevo y sobre el original; guardar ambos recuentos como evidencia. Para que el compilador imponga las reglas, usar un paquete Z con versión de lenguaje cloud (ver backlog de `abap-001`).
- **Prevención:** Quality gate: todo objeto que pretenda ser cloud-ready pasa la variante ATC aunque active limpio. Patrón `P-005`.
- **Proyectos referenciados:** `projects/abap-001-equipos-cloud` (report original 41 hallazgos: 34 P1, 7 P2; clase nueva 0).

### ATC-002 | Info SLIN "Strings without text elements"

**TAGS:** ATC, SYNTAX, MINOR, REUSE_YES, TEST

- **Síntoma:** ATC con variante por defecto reporta infos "Strings without text elements" en literales usados con `out->write( )`.
- **Causa raíz:** Literales de texto visibles al usuario sin símbolo de texto asociado.
- **Solución:** Crear símbolos de texto (`TEXT-001`, `TEXT-002`) con `SAPWrite edit_text_symbols` y referenciarlos: `|{ TEXT-002 }{ lines( ... ) }|`.
- **Prevención:** Usar símbolos de texto para cualquier literal que llegue a consola o UI; dejar literales solo en código técnico.
- **Proyectos referenciados:** `projects/abap-001-equipos-cloud`.

### ATC-003 | Info de sistema ajena al objeto (zonas horarias `TTZCU`, SAP Note 481835)

**TAGS:** ATC, OPERATIONS, MINOR, REUSE_PARTIAL, TEST

- **Síntoma:** ATC devuelve una info sobre customizing de zonas horarias aunque el objeto no toque fechas ni horas.
- **Causa raíz:** Hallazgo de sistema (customizing de Basis), no del código.
- **Solución:** Documentarlo en la ficha de cierre como "ajeno al objeto, responsabilidad de Basis" y no intentar corregirlo desde el desarrollo.
- **Prevención:** Separar en la evidencia los hallazgos del objeto de los hallazgos de sistema.
- **Proyectos referenciados:** `projects/abap-001-equipos-cloud`.

---

## CTS - Transportes y paquetes

### CTS-001 | Endpoint ICF de abapGit no activo; gCTS disponible

**TAGS:** CTS, TRANSPORT, MINOR, REUSE_PARTIAL, DESIGN

- **Síntoma:** `SAPGit` / abapGit no responde; `config/system.yaml` registra `abapgit: false`.
- **Causa raíz:** El servicio ICF de abapGit no está activo en el sistema de laboratorio.
- **Solución:** Usar gCTS para versionado en SAP mientras se decide activar abapGit (backlog global). El código local en `projects/<id>/src/` sigue siendo copia, no repositorio desplegable.
- **Prevención:** Confirmar capacidades con `SAPContext` antes de prometer un flujo Git.

---

## SEC - Seguridad y secretos

### SEC-001 | Certificado TLS del sistema obliga a `SAP_INSECURE=true` en ARC-1

**TAGS:** SEC, CONNECTIVITY, MAJOR, REUSE_PARTIAL, DESIGN

- **Síntoma:** ARC-1 falla la verificación TLS contra el servidor de aplicación hasta que se habilita la excepción.
- **Causa raíz:** Certificado del sistema no confiable para el cliente local; renovación pendiente por Basis.
- **Solución:** Excepción temporal `SAP_INSECURE=true` en la configuración local del MCP (nunca en el repositorio). Registrada en `config/system.yaml` como `tls_exception`.
- **Prevención:** Mantener en `learning/backlog.md` el retiro de la excepción cuando Basis renueve el certificado; no normalizar la excepción.

### SEC-002 | Contraseña en texto plano en el contexto del workspace

**TAGS:** SEC, OPERATIONS, BLOCKER, REUSE_YES, DESIGN

- **Síntoma:** `CONTEXT.txt` inicial contenía una contraseña SAP.
- **Causa raíz:** Inventario legado copiado sin sanitizar.
- **Solución:** Retirar el secreto; ARC-1 siguió autenticando desde su almacén privado. Validador `scripts/verify_workspace.py` y linter del KB buscan patrones de secretos.
- **Prevención:** El repositorio solo contiene metadatos no secretos. Ejecutar el linter antes de versionar. Decisión `D-003`.

---

## TOOL - ARC-1, ADT y clientes HTTP

### TOOL-001 | Bruno Safe Mode ignora los bloques `script:` en silencio

**TAGS:** TOOL, TOOLING, MAJOR, REUSE_YES, TEST

- **Síntoma:** Con la cookie ya resuelta en PowerShell (`201`), el mismo POST seguía dando `403` desde Bruno. Tres correcciones del script no movieron el síntoma; las variables `{{csrfToken}}` y `{{sapCookie}}` aparecían en rojo (sin resolver).
- **Causa raíz:** El Safe Mode de Bruno descarta los bloques `script:` sin emitir error. Código correcto + sandbox apagado = síntoma idéntico a código roto.
- **Solución:** Pasar la colección a Developer Mode. Un `throw` deliberado en `script:pre-request` prueba en un intento si el script se ejecuta.
- **Prevención:** Cuando un cliente HTTP "no haga caso" a un script, verificar primero que lo ejecuta antes de corregir la lógica. Aplica igual a Groovy en CPI al leer cabeceras.
- **Proyectos referenciados:** `artifacts/bruno/CROWN-API_MAINTNOTIFICATION`.

### TOOL-002 | `res.getHeader("set-cookie")` en Bruno no tiene tipo de retorno estable

**TAGS:** TOOL, TOOLING, MAJOR, REUSE_YES, TEST

- **Síntoma:** La variable `sapCookie` valía `[object Object]`; el POST seguía en `403`.
- **Causa raíz:** `res.getHeader()` devuelve objeto, array o string según la versión; el script asumía string.
- **Solución:** Normalizar las tres formas antes de parsear (array → join, objeto → valores, string → tal cual). Con eso POST = `201`, aviso 10000945 confirmado en `QMEL`.
- **Prevención:** Nunca asumir el tipo de retorno de helpers de cabeceras; normalizar siempre.

### TOOL-003 | Esquemas publicados por ARC-1 no demuestran autenticación SAP

**TAGS:** TOOL, TOOLING, MINOR, REUSE_YES, DESIGN

- **Síntoma:** El MCP lista sus herramientas y parece "conectado" antes de haber completado ninguna llamada ADT.
- **Causa raíz:** La publicación de esquemas ocurre antes de la primera petición autenticada.
- **Solución:** Declarar la conexión lista solo tras una lectura no destructiva (`SAPRead type=SYSTEM` o `SAPContext`).
- **Prevención:** Incluir una lectura inocua en cada validación de cliente.

### TOOL-004 | SAPLint reporta falsos positivos sobre `IF_OO_ADT_CLASSRUN`

**TAGS:** TOOL, TOOLING, MINOR, REUSE_YES, BUILD

- **Síntoma:** 7 avisos de SAPLint sobre `ZCL_EQUIPOS_CLOUD_GL`: 5 por desconocer `IF_OO_ADT_CLASSRUN`, `check_subrc` en un SELECT cuyo resultado evalúa el llamador, `double_space` por alineación de alias.
- **Causa raíz:** El linter local no conoce todas las interfaces liberadas y aplica reglas de estilo que a veces chocan con alineación deliberada.
- **Solución:** Clasificar cada aviso como falso positivo / aceptado / corregido en la ficha de cierre; la fuente de verdad es `SAPDiagnose action=syntax` + activación.
- **Prevención:** No bloquear un cierre por avisos de SAPLint sin clasificarlos; registrar los falsos positivos recurrentes aquí para no reinvestigarlos.
- **Proyectos referenciados:** `projects/abap-001-equipos-cloud`.

### TOOL-005 | Servicio ICF de búsqueda de texto ADT no activo

**TAGS:** TOOL, TOOLING, MINOR, REUSE_PARTIAL, DESIGN

- **Síntoma:** `SAPSearch` no ofrece búsqueda full-text en código fuente; `config/system.yaml` registra `repository_text_search: false`.
- **Causa raíz:** El servicio ICF `textSearch` del repositorio ADT no está activado.
- **Solución:** Buscar por nombre de objeto, paquete y where-used; para texto, leer el objeto completo con `SAPRead`.
- **Prevención:** Evaluar en el backlog global la activación del servicio si el equipo necesita búsqueda full-text.

---

## Multi-capability

_(sin entradas consolidadas todavía)_

---

## Plantilla para nuevas entradas

```markdown
### <CAP>-NNN | Título corto del error

**TAGS:** <capability>, <categoría>, <severidad>, REUSE_YES|REUSE_PARTIAL, <origen>

- **Síntoma:**
- **Causa raíz:**
- **Solución:**
- **Prevención:**
- **Evidencia:** (ruta dentro del proyecto, sanitizada)
- **Proyectos referenciados:**
```

## Changelog

| Fecha | Cambio |
|---|---|
| 2026-10-01 | Versión inicial: 14 errores promovidos desde `learning/lessons.md`, `projects/abap-001-equipos-cloud` y `config/system.yaml`. |
