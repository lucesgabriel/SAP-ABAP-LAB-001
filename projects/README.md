# Proyectos ABAP

Cada carpeta es una unidad de trabajo independiente. `_template/` contiene la base reutilizable; no es un proyecto ejecutado.

## Comandos desde la raíz

```powershell
python scripts/workspace/projects.py create abap-001-primer-reporte --title "Mi primer reporte ABAP"
python scripts/workspace/projects.py create rap-002-ordenes --title "Órdenes con draft" --capability RAP
python scripts/workspace/projects.py list
python scripts/workspace/projects.py refresh-context rap-002-ordenes
python scripts/workspace/validate_structure.py
```

El generador no sobrescribe carpetas existentes y solo acepta identificadores como `abap-001-tema`, `cds-002-tema` o `rap-003-tema`. El prefijo fija la capability con la que se filtra el `knowledge-base/` al inyectar `docs/historical-context.md` (`abap`→OO, `cds`→CDS, `rap`→RAP, `sql`→SQL, `enh`→ENH, `api`→API, `ui`→UI, `mix`→MULTI); `--capability` la fuerza. Tampoco conecta con SAP. Completa el paquete y transporte en `project.json` después de verificarlos; ambos empiezan en `null`.

## Contenido de cada proyecto

| Ruta | Función |
| --- | --- |
| `project.json` | Identificador, título, estado, fecha, capability, referencias SAP verificadas, `ready_to_consolidate`, `consolidated_on`. |
| `README.md` | Objetivo, alcance, estado del loop, navegación y siguiente paso. |
| `docs/historical-context.md` | Códigos del KB aplicables, inyectados al crear (regenerable). |
| `docs/design.md` | Diseño citando el KB, contexto SAP leído, solución. |
| `docs/error-log.md`, `docs/decision-log.md` | Errores y decisiones con taxonomía; se promueven al KB al cierre. |
| `docs/backlog.md`, `docs/journal.md` | Plan y diario. |
| `src/` | Código y procedencia de las lecturas/exportaciones. |
| `tests/` | Plan, criterios y datos sintéticos. |
| `evidence/` | Resultados sanitizados y ficha de cierre. |
| `transports/` | Inventario de objetos, dependencias y reversión. |

Edita el campo `status` con uno de: `planned`, `active`, `blocked`, `completed`, `archived`. `completed` lo fija `close_project.py`. No muevas la carpeta al cambiar de estado. El listado lee directamente estos metadatos; no hay catálogo manual que sincronizar.

## Cierre

```bash
python scripts/workspace/close_project.py --project projects/<id> --dry-run
python scripts/workspace/close_project.py --project projects/<id>
```

Requiere `"ready_to_consolidate": true` y ficha de cierre completa. Consulta el [flujo diario](../docs/guides/daily-workflow.md) y la [guía del loop](../docs/guides/self-improvement-loop.md). Si necesitas una excepción de estructura, documéntala antes de cambiar la plantilla y adapta su validador.
