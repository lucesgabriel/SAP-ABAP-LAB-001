# Proyectos ABAP

Cada carpeta es una unidad de trabajo independiente. `_template/` contiene la base reutilizable; no es un proyecto ejecutado.

## Comandos desde la raíz

```powershell
python scripts/workspace/projects.py create abap-001-primer-reporte --title "Mi primer reporte ABAP"
python scripts/workspace/projects.py list
python scripts/workspace/validate_structure.py
```

El generador no sobrescribe carpetas existentes y solo acepta identificadores como `abap-001-tema`, `cds-002-tema` o `rap-003-tema`. Tampoco conecta con SAP. Completa el paquete y transporte en `project.json` después de verificarlos; ambos empiezan en `null`.

## Contenido de cada proyecto

| Ruta | Función |
| --- | --- |
| `project.json` | Identificador, título, estado, fecha y referencias SAP verificadas. |
| `README.md` | Objetivo, alcance, navegación y siguiente paso. |
| `docs/` | Diseño, backlog y diario del proyecto. |
| `src/` | Código y procedencia de las lecturas/exportaciones. |
| `tests/` | Plan, criterios y datos sintéticos. |
| `evidence/` | Resultados sanitizados y ficha de cierre. |
| `transports/` | Inventario de objetos, dependencias y reversión. |

Edita el campo `status` con uno de: `planned`, `active`, `blocked`, `completed`, `archived`. No muevas la carpeta al cambiar de estado. El listado lee directamente estos metadatos; no hay catálogo manual que sincronizar.

Consulta el [flujo diario](../docs/guides/daily-workflow.md). Si necesitas una excepción de estructura, documéntala antes de cambiar la plantilla y adapta su validador.
