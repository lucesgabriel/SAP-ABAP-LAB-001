# Claude Desktop Project Instructions — SAP ABAP LAB 001

Trabaja exclusivamente con el sistema y las reglas descritas en los archivos de conocimiento de este Project. Responde en español; términos SAP en inglés.

## Archivos que debes leer primero
1. `AGENTS.md` (reglas y loop de auto-mejora)
2. `config/system.yaml`
3. `knowledge-base/README.md` y `knowledge-base/taxonomy.md`
4. `learning/decisions.md`

## Knowledge-base (consulta obligatoria)
Antes de diseñar o construir, lee el `docs/historical-context.md` del proyecto (o `00-case-brief/historical-context.md` del caso) y abre en `knowledge-base/` cada código citado: errores `<CAP>-NNN`, patrones `P-NNN`, decisiones `D-NNN`, recetas `R-NNN`. Cita los reutilizados en `docs/design.md`. Si trabajas sin la carpeta montada, pide al usuario el contenido del histórico.

## Herramientas
Usa el MCP local `sap-arc1-s4h-100`. Antes de prometer una capacidad, consulta la lista de herramientas disponible en la sesión y confirma la conexión con una lectura no destructiva (`SAPContext` o `SAPRead type=SYSTEM`), no solo por ver las herramientas listadas.

Flujo para cambios (`P-002`):
`SAPContext` → `SAPSearch`/`SAPRead` → diseño con diff mínimo → `SAPLint`/`SAPDiagnose syntax` → `SAPWrite` → `SAPActivate` → lectura posterior → ABAP Unit/ATC.

## Registro en el momento
- Cada error resuelto → fila en `docs/error-log.md` con capability, categoría, severidad, origen y `YES`/`PARTIAL`/`NO` según `knowledge-base/taxonomy.md`.
- Cada decisión → fila en `docs/decision-log.md` con alternativas, motivo e impacto.
- Al cerrar, el usuario ejecuta `scripts/workspace/close_project.py`; tú preparas los logs para que pase el `--dry-run` sin errores.

## Límites operativos
- Nunca pidas ni almacenes la contraseña SAP en el chat o en archivos del Project.
- No modifiques objetos estándar SAP sin autorización explícita del usuario para el objeto exacto.
- Pide confirmación inmediatamente antes de borrar, liberar transportes, publicar/despublicar servicios, ejecutar SQL modificador o hacer operaciones Git/gCTS mutantes.
- Minimiza consultas de datos y evita exponer datos sensibles al proveedor del modelo.
- Una escritura exitosa no demuestra compilación: la activación y la lectura posterior son obligatorias.
- En `$TMP` el compilador no impone la versión de lenguaje cloud; solo ATC `ABAP_CLOUD_READINESS` lo demuestra (`ATC-001`).

## Skills
Los plugins `clean-abap` y `abap-cloud-rap` pertenecen a Claude Code y no se cargan automáticamente en Claude Desktop. En Claude Desktop aplica las reglas equivalentes de `AGENTS.md`, `standards/naming-conventions.md` y `standards/technology-decision-matrix.md`, y usa ARC-1 directamente.

## Aprendizaje continuo
Al finalizar una tarea verificada, deja los logs del proyecto listos para el cierre y propone, si corresponde, un patrón `P-NNN` o receta `R-NNN` con su evidencia. No escribas hipótesis, secretos ni resultados no comprobados como conocimiento permanente.
