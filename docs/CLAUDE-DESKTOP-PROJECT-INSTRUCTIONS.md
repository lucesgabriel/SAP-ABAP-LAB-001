# Claude Desktop Project Instructions — SAP ABAP LAB 001

Trabaja exclusivamente con el sistema y las reglas descritas en los archivos de conocimiento de este Project.

## Archivos que debes leer primero
1. `AGENTS.md`
2. `config/system.yaml`
3. `learning/decisions.md`
4. `learning/lessons.md`

## Herramientas
Usa el MCP local `sap-arc1-s4h-100`. Antes de prometer una capacidad, consulta la lista de herramientas disponible en la sesión.

Flujo para cambios:
`SAPContext` → `SAPSearch`/`SAPRead` → `SAPLint`/`SAPDiagnose` → revisión del cambio → `SAPWrite` → `SAPActivate` → lectura posterior → ABAP Unit/ATC.

## Límites operativos
- Nunca pidas ni almacenes la contraseña SAP en el chat o en archivos del Project.
- No modifiques objetos estándar SAP sin autorización explícita del usuario para el objeto exacto.
- Pide confirmación inmediatamente antes de borrar, liberar transportes, publicar/despublicar servicios, ejecutar SQL modificador o hacer operaciones Git/gCTS mutantes.
- Minimiza consultas de datos y evita exponer datos sensibles al proveedor del modelo.
- Una escritura exitosa no demuestra compilación: la activación y la lectura posterior son obligatorias.

## Skills
Los plugins `clean-abap` y `abap-cloud-rap` pertenecen a Claude Code y no se cargan automáticamente en Claude Desktop. En Claude Desktop aplica las reglas equivalentes de `AGENTS.md` y usa ARC-1 directamente.

## Aprendizaje continuo
Al finalizar una tarea verificada, propone una actualización pequeña y deduplicada en `learning/`. No escribas hipótesis, secretos ni resultados no comprobados como conocimiento permanente.
