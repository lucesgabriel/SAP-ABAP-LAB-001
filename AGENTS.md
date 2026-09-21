# SAP ABAP LAB 001 — Reglas para agentes

## Objetivo
Este repositorio es el centro de trabajo para desarrollar, revisar, probar y documentar soluciones ABAP en el sistema de laboratorio S/4HANA descrito en `config/system.yaml` y `CONTEXT.txt`.

Estas reglas se aplican a Hermes Desktop, Claude Code y cualquier agente que cargue `AGENTS.md`.

## Fuentes de verdad
1. `config/system.yaml`: identidad y capacidades no secretas del sistema.
2. Código y metadatos leídos en vivo con ARC-1: estado actual de SAP.
3. `learning/decisions.md`: decisiones vigentes del proyecto.
4. `learning/lessons.md`: aprendizajes comprobados y reutilizables.
5. `CONTEXT.txt`: inventario legado sanitizado; nunca debe contener contraseñas.

Cuando una nota local contradiga una lectura actual de SAP, prevalece SAP y se corrige la nota.

## Seguridad y secretos
- Nunca escribir contraseñas, tokens, cookies o claves en este repositorio, chats, argumentos de proceso, capturas o manuales.
- Usar exclusivamente el almacén privado ya configurado para ARC-1.
- El servidor ARC-1 puede exponer capacidades amplias; eso no elimina la revisión humana.
- No modificar objetos estándar SAP salvo que el usuario nombre explícitamente el objeto y autorice el cambio concreto.
- Para `delete`, liberación de transportes, `unpublish`, push/commit gCTS, SQL que modifique datos o acciones irreversibles: pedir confirmación explícita inmediatamente antes.
- Consultas de datos: seleccionar solo columnas necesarias, filtros restrictivos y límites pequeños. No exportar masivamente datos personales, financieros, HR o credenciales.

## Flujo obligatorio para cambios ABAP
1. **Entender**: usar `SAPContext` y después `SAPSearch`/`SAPRead`; identificar paquete, dependencias, API release y transportes.
2. **Diseñar**: proponer alcance, objetos, nombres, paquete y estrategia de transporte. Para pruebas desechables usar `$TMP`; para trabajo durable usar paquetes `Z*`/`Y*` y transporte válido.
3. **Preparar**: trabajar con el diff mínimo. Para clases preferir edición de método/unidad sobre reemplazo completo.
4. **Prevalidar**: ejecutar `SAPLint` y `SAPDiagnose action=syntax` cuando aplique. En RAP, ordenar dependencias TABL → DDLS → DCLS → BDEF → SRVD/SRVB.
5. **Escribir**: usar `SAPWrite`; nunca afirmar que una escritura compila solo porque el write respondió correctamente.
6. **Activar**: usar `SAPActivate`; para dos o más objetos usar activación batch.
7. **Verificar**: volver a leer, confirmar `INACTIVE_OBJECTS` limpio, ejecutar ABAP Unit y ATC cuando corresponda, y revisar dependencias/where-used.
8. **Documentar**: registrar únicamente aprendizajes comprobados en `learning/` y actualizar la documentación afectada.

## Criterio de terminado
Una tarea de desarrollo no está terminada hasta que estén documentados:
- objetos afectados y paquete;
- diff o descripción exacta del cambio;
- resultado de lint/sintaxis;
- resultado de activación;
- resultado de pruebas/ATC o motivo explícito por el que no aplican;
- lectura posterior que confirme el estado final;
- riesgos, transporte y pasos de reversión.

## Selección de skills
### Hermes Desktop
Cargar la skill relevante antes de actuar:
- `clean-abap-review`
- `clean-abap-refactor`
- `abap-cloud-rap-design`
- `abap-atc-remediation`
- `abap-clean-core-check`
- `sap-abap-agentic-development`

### Claude Code
Usar los plugins instalados globalmente:
- `/clean-abap:review`
- `/clean-abap:refactor`
- `/abap-cloud-rap:rap-bo-design`
- `/abap-cloud-rap:atc-remediation`
- `/abap-cloud-rap:clean-core-check`

### Claude Desktop
Claude Desktop usa ARC-1 como MCP, pero no carga plugins de Claude Code. Adjuntar o copiar `docs/CLAUDE-DESKTOP-PROJECT-INSTRUCTIONS.md` en las instrucciones del proyecto de Claude Desktop.

## Aprendizaje continuo y automejora
Después de cada entrega verificada:
1. Añadir a `learning/lessons.md` solo una lección reutilizable con evidencia.
2. Registrar decisiones de arquitectura en `learning/decisions.md`.
3. Añadir patrones ABAP aprobados en `learning/patterns.md`.
4. Registrar deuda o mejoras pendientes en `learning/backlog.md`.
5. Eliminar o reemplazar información obsoleta; no acumular duplicados.
6. Nunca convertir una hipótesis, error transitorio o dato sensible en aprendizaje permanente.

Las reglas de este archivo solo se cambian cuando una lección se repite o una decisión de gobernanza lo requiere. Toda automejora debe ser revisable mediante Git.
