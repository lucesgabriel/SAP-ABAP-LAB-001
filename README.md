# SAP ABAP LAB 001

Workspace compartido para Hermes Desktop, Claude Code y Claude Desktop, orientado al desarrollo ABAP moderno sobre SAP S/4HANA 2025.

## Dónde trabajar

| Carpeta / archivo | Para qué sirve |
| --- | --- |
| [projects/](projects/README.md) | Un espacio independiente por proyecto: código, diseño, pruebas, evidencias y transportes. |
| [learning/](learning/README.md) | Ruta de estudio, ejercicios, sesiones y conocimiento comprobado compartido. |
| [docs/](docs/README.md) | Guías de organización, flujo diario y operación del laboratorio. |
| [scripts/](scripts/README.md) | Crear y validar proyectos; utilidades existentes de operación. |
| [config/](config/README.md) | Inventario no secreto del sistema. |
| [artifacts/](artifacts/README.md) | Archivos generados y herramientas locales, excluidos de Git salvo su guía. |
| [AGENTS.md](AGENTS.md) / [CLAUDE.md](CLAUDE.md) | Reglas de agentes y entrada para Claude Code. |
| [CONTEXT.txt](CONTEXT.txt) | Inventario legado sanitizado; la configuración y SAP en vivo prevalecen. |

Empieza por la [guía de organización](docs/guides/organization.md) y el [flujo diario](docs/guides/daily-workflow.md).

## Crear tu primer proyecto

Desde la raíz, con Python 3.10 o posterior (sin paquetes adicionales para estos comandos):

```powershell
python scripts/workspace/projects.py create abap-001-primer-reporte --title "Mi primer reporte ABAP"
python scripts/workspace/projects.py list
python scripts/workspace/validate_structure.py
```

Abre `projects/abap-001-primer-reporte/README.md` y completa `project.json`, `docs/design.md` y `docs/backlog.md`. El comando solo crea archivos locales; los nombres de paquete y transporte se completan después de verificarlos en SAP. Consulta la [ruta de aprendizaje](learning/roadmap.md) para elegir el ejercicio.

## Inicio rápido
1. Abre esta carpeta como proyecto/workspace.
2. Lee `AGENTS.md`.
3. Ejecuta `python scripts/workspace/validate_structure.py` para revisar la organización local. Para la validación del entorno de clientes, ejecuta `python scripts/verify_workspace.py` (requiere PyYAML y los clientes configurados).
4. En Hermes usa las skills SAP instaladas y el MCP `sap_arc1_s4h_100`.
5. En Claude Code usa los comandos `/clean-abap:*` y `/abap-cloud-rap:*`.
6. En Claude Desktop crea/abre un Project y añade `docs/CLAUDE-DESKTOP-PROJECT-INSTRUCTIONS.md` a sus instrucciones/conocimiento.

## Estado de seguridad
Las credenciales no viven en el repositorio. ARC-1 se autentica mediante el almacén privado local. La excepción TLS `SAP_INSECURE=true` es temporal y debe eliminarse cuando Basis renueve el certificado del sistema.
