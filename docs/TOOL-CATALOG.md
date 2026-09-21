# Catálogo operativo — ARC-1 y skills ABAP

## ARC-1 1.1.0 con política de desarrollo completa
La lista en vivo del cliente siempre prevalece. Con las gates de escritura, datos, SQL, transporte y Git activas, ARC-1 publica doce herramientas:

| Herramienta | Uso principal | ¿Puede mutar SAP? |
|---|---|---|
| `SAPContext` | Entender intención, contratos, dependencias e impacto | No |
| `SAPSearch` | Buscar objetos, TADIR y código | No |
| `SAPRead` | Leer fuente, DDIC, paquetes, sistema, tablas y borradores | No |
| `SAPNavigate` | Definiciones, where-used y jerarquías | No |
| `SAPLint` | abaplint, formato y fixes locales | No, salvo que luego se escriba |
| `SAPDiagnose` | Sintaxis, ABAP Unit, ATC y diagnóstico | Ejecuta pruebas/checks |
| `SAPWrite` | Crear, actualizar, borrar y editar objetos | Sí |
| `SAPActivate` | Activar objetos y publicar/despublicar SRVB | Sí |
| `SAPManage` | Capacidades, paquetes, FLP y API release | Algunas acciones |
| `SAPTransport` | CTS: listar, crear, liberar, borrar y reasignar | Algunas acciones |
| `SAPGit` | gCTS/abapGit según disponibilidad y gates | Algunas acciones |
| `SAPQuery` | SELECT Open SQL de solo lectura | Lee datos |

## Skills de Hermes Desktop
- `clean-abap-review`: revisión estructurada de Clean ABAP.
- `clean-abap-refactor`: refactor behavior-preserving.
- `abap-cloud-rap-design`: diseño y construcción de BO RAP.
- `abap-atc-remediation`: clasificación, corrección y reejecución de ATC.
- `abap-clean-core-check`: auditoría Clean Core/APIs liberadas.
- `sap-abap-agentic-development`: conexión, permisos, verificación y seguridad MCP/ADT.

## Plugins y skills de Claude Code
- `/clean-abap:review`
- `/clean-abap:refactor`
- `/abap-cloud-rap:rap-bo-design`
- `/abap-cloud-rap:atc-remediation`
- `/abap-cloud-rap:clean-core-check`
- Plugin `arc-1@arc-1`

## Claude Desktop
Claude Desktop dispone del MCP local `sap-arc1-s4h-100`. Los plugins de Claude Code no se cargan en Claude Desktop; usar `docs/CLAUDE-DESKTOP-PROJECT-INSTRUCTIONS.md` como instrucciones/conocimiento del Project.

## Capacidades verificadas del sistema
- SAP S/4HANA 2025 on-premise, ABAP Platform 2025, SAP_BASIS 816.
- HANA, RAP/CDS, AMDP, UI5/Fiori, UI5 Repository Deploy, CTS, gCTS y FLP disponibles.
- abapGit no disponible porque su endpoint ICF no está activo.
- Búsqueda de texto ADT no disponible porque su servicio ICF no está activo.
- Autenticación ARC-1 verificada mediante `SAPRead(type="SYSTEM")`.
