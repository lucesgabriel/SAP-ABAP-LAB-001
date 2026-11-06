# Prompts Reutilizables

Prompts base para cada fase del loop. Cópialos en Claude Code, Claude Desktop, Hermes o Codex y reemplaza los `<placeholders>`. Todos asumen que el agente ya leyó `AGENTS.md`.

| Prompt | Fase | Qué produce |
|---|---|---|
| [00-nuevo-proyecto.md](00-nuevo-proyecto.md) | Kickoff | Proyecto creado, histórico del KB leído, contexto SAP leído, diseño inicial sin construir. |
| [01-disenar-solucion.md](01-disenar-solucion.md) | Diseño | `docs/design.md` completo citando `P/D/R/<CAP>-XXX`, decision-log inicial, orden de activación. |
| [02-construir-con-arc1.md](02-construir-con-arc1.md) | Build | Objetos escritos y activados con el flujo `P-002`; error-log alimentado en el momento. |
| [03-revisar-calidad.md](03-revisar-calidad.md) | Verificación | ATC, Unit, lint clasificado, lectura posterior; ficha de cierre llena. |
| [04-generar-caso-practica.md](04-generar-caso-practica.md) | Práctica | Caso `ABAP-CASE-<DOM>-<NNN>` con brief completo, rúbrica y solución oculta. |
| [05-retrospectiva-cierre.md](05-retrospectiva-cierre.md) | Cierre | Logs validados, `ready_to_consolidate: true`, `close_project.py` ejecutado, KB enriquecido. |

Regla: ningún prompt salta la consulta al `knowledge-base/` ni el flujo obligatorio de cambios de `AGENTS.md`.
