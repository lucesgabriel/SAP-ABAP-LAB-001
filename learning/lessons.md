# Lecciones comprobadas

Registra aquí únicamente aprendizajes reutilizables confirmados por ejecución, documentación oficial o lectura directa del sistema.

> Desde 2026-10-01 cada lección enlaza su versión codificada en `knowledge-base/` (errores `<CAP>-NNN`, patrones `P-NNN`, decisiones `D-NNN`, recetas `R-NNN`). Las lecciones nuevas nacen en `docs/error-log.md` / `docs/decision-log.md` del proyecto y llegan al KB con `close_project.py`; aquí solo se añade la narrativa cuando aporta contexto que no cabe en el catálogo.

## Formato
### YYYY-MM-DD — Título breve
- **Contexto:**
- **Evidencia:**
- **Lección:**
- **Aplicación futura:**
- **Reemplaza/obsoleta:**
- **Códigos KB:**

## Lecciones iniciales
### 2026-08-21 — La configuración del agente no demuestra autenticación SAP
- **Contexto:** ARC-1 puede publicar sus esquemas antes de completar una llamada ADT.
- **Evidencia:** se ejecutó `SAPRead(type="SYSTEM")` correctamente contra el sistema.
- **Lección:** declarar la conexión lista solo después de una lectura SAP no destructiva.
- **Aplicación futura:** incluir una lectura `SYSTEM` o búsqueda inocua en cada validación de cliente.
- **Reemplaza/obsoleta:** ninguna.
- **Códigos KB:** `TOOL-003`, `D-002`.

### 2026-08-21 — Separar secretos del workspace
- **Contexto:** el contexto inicial contenía una contraseña en texto plano.
- **Evidencia:** se retiró del archivo y ARC-1 siguió usando su almacén privado.
- **Lección:** el repositorio contiene solo metadatos no secretos e interpolaciones.
- **Aplicación futura:** ejecutar el validador antes de commits y entregas.
- **Reemplaza/obsoleta:** cualquier práctica de guardar credenciales en `CONTEXT.txt`.
- **Códigos KB:** `SEC-002`, `D-003`.

### 2026-09-14 — CSRF sobre HTTP: la cookie `secure` y el parseo de `set-cookie`
- **Contexto:** POST a `API_MAINTNOTIFICATION` (OData V2) devolvía siempre `403 CSRF token validation failed`, desde Bruno y desde `/IWFND/GW_CLIENT`, con el token correctamente capturado.
- **Evidencia:** `scripts/diag-csrf.ps1` ejecutado el 14-sep-2026. SAP responde `set-cookie: sap-usercontext=sap-client=100; path=/,SAP_SESSIONID_S4H_100=...; path=/; secure; HttpOnly; SameSite=None`. Reinyectando ambas cookies con `Secure=$false` el POST devuelve **201** (aviso 10000942, confirmado en QMEL) y dos GET consecutivos comparten el mismo token.
- **Lección:** dos causas distintas producen el mismo mensaje. (1) `SAP_SESSIONID_*` lleva flag `secure`; sobre `http://` ningún cliente estándar la reenvía, así que cada petición abre sesión nueva y el token muere con la anterior. (2) SAP manda las dos cookies en UNA cadena separadas por **coma**: `split(";")[0]` se queda con `sap-usercontext` y descarta el `SAP_SESSIONID`. Hay que recorrer pares `nombre=valor` con regex filtrando atributos.
- **Aplicación futura:** ante `CSRF token validation failed`, comparar el `SAP_SESSIONID` de dos respuestas seguidas **antes** de tocar el token: si difieren, el problema es la cookie, no el CSRF. En clientes sobre HTTP, enviar `Cookie` como cabecera explícita. En `/IWFND/GW_CLIENT` nunca pegar el token a mano: lo gestiona el cliente.
- **Reemplaza/obsoleta:** ninguna.
- **Códigos KB:** `API-001`, `P-004`, `R-006`.

### 2026-09-14 — Bruno: Safe Mode ignora los scripts en silencio y `res.getHeader` no tiene tipo estable
- **Contexto:** con el diagnóstico de la cookie ya resuelto en PowerShell (201), el mismo POST seguía dando 403 desde Bruno. Tres correcciones sucesivas del código no movieron el síntoma.
- **Evidencia:** las variables `{{csrfToken}}` y `{{sapCookie}}` aparecían en ROJO (sin resolver) y un `throw` deliberado en `script:pre-request` no llegaba a abortar la petición: los bloques `script:` no se ejecutaban. Tras pasar la colección a Developer Mode, el `throw` sí disparó y reveló el segundo fallo: `sapCookie` valía `[object Object]`, porque `res.getHeader("set-cookie")` devuelve un OBJETO en esta versión, ni array ni string. Normalizando las tres formas, POST = **201**, aviso 10000945 confirmado en QMEL.
- **Lección:** (1) el Safe Mode de Bruno descarta los bloques `script:` sin emitir ningún error; el único indicio es que las variables quedan sin resolver. Código correcto + sandbox apagado = síntoma idéntico a código roto. (2) `res.getHeader()` no garantiza el tipo de retorno: normalizar array / objeto / string antes de parsear.
- **Aplicación futura:** cuando un cliente HTTP parezca "no hacer caso" a un script, verificar primero que lo está ejecutando (un `throw` deliberado lo prueba en un intento) antes de seguir corrigiendo la lógica. Aplica igual a Groovy en CPI al leer cabeceras del Message.
- **Reemplaza/obsoleta:** ninguna.
- **Códigos KB:** `TOOL-001`, `TOOL-002`.

### 2026-09-20 — Crear proyectos sin sobrescribir y validar la organización local
- **Contexto:** el laboratorio necesitaba separar proyectos y aprendizaje conservando rutas existentes.
- **Evidencia:** [verificación de organización](../docs/maintenance/2026-09-20-organization.md); cuatro pruebas locales pasan, incluida la conservación de contenido existente al intentar crear un identificador repetido.
- **Lección:** una plantilla por proyecto con metadatos locales permite generar y listar trabajos; comprobar archivos y enlaces detecta defectos de organización antes de trabajar en SAP.
- **Aplicación futura:** usar `scripts/workspace/projects.py` al iniciar un proyecto y `scripts/workspace/validate_structure.py` al cerrar una sesión. Estas comprobaciones no acreditan activación ni pruebas ABAP.
- **Reemplaza/obsoleta:** ninguna; complementa el validador existente del entorno.
- **Códigos KB:** `D-006`.

### 2026-09-20 — Report ALV → clase ABAP Cloud: ATC como prueba del antes/después
- **Contexto:** versión cloud de `ZR_ALV_EQUIPOS_GL` (EQUI/EQKT + pantalla de selección + SALV) en `projects/abap-001-equipos-cloud`.
- **Evidencia:** ATC `ABAP_CLOUD_READINESS` vía ARC-1: report original 41 hallazgos (34 P1, 7 P2); `ZCL_EQUIPOS_CLOUD_GL` 0 hallazgos. `I_Equipment` e `I_EquipmentText` con contrato C1 liberado (`SAPRead type=API_STATE`).
- **Lección:** en `$TMP` on-premise la clase se compila como ABAP estándar, así que el compilador no detecta usos no liberados; la variante ATC `ABAP_CLOUD_READINESS` sí. `cl_abap_context_info=>get_user_language_abap_format( )` declara `CX_ABAP_CONTEXT_INFO_ERROR` y hay que capturarla.
- **Aplicación futura:** antes de elegir la vista CDS de reemplazo, comprobar `API_STATE` (C1 + uso en ABAP Cloud); ejecutar la variante ATC sobre el objeto original y el nuevo y guardar ambos recuentos como evidencia.
- **Reemplaza/obsoleta:** ninguna.
- **Códigos KB:** `P-001`, `P-005`, `ATC-001`, `OO-001`, `R-001` a `R-005`, `D-008`.
