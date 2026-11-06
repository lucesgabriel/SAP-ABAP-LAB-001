# SAP ABAP LAB 001

Workspace compartido para Hermes Desktop, Claude Code, Claude Desktop / Cowork y Codex, orientado al desarrollo ABAP moderno sobre SAP S/4HANA 2025. Diseñado para que **cada proyecto aproveche lo aprendido en los anteriores y deje conocimiento para los siguientes**, con la misma filosofía que el SAP Integration Suite Codex Lab.

## Objetivo

Usar un agente como copiloto técnico para:

- entender un requerimiento ABAP y leer el contexto real en SAP con ARC-1;
- diseñar la solución (clase, CDS, RAP, AMDP, BAdI, OData) citando el conocimiento previo;
- construir con el flujo seguro `contexto → diff mínimo → lint/sintaxis → escritura → activación → pruebas/ATC → lectura posterior`;
- registrar errores y decisiones con taxonomía para no repetirlos;
- **auto-mejorar el lab** cerrando cada proyecto o caso contra un knowledge-base central.

## Loop de auto-mejora

```text
   ┌─ Nuevo proyecto o caso de práctica ───────────────────────────┐
   │                                                                │
   │  1. El generador inyecta el histórico del KB filtrado por      │
   │     capability (errores, patrones, decisiones, recetas)        │
   │  2. Diseña citando códigos (P-001, D-008, R-002, OO-001...)    │
   │  3. Construye con ARC-1 y registra errores/decisiones en los   │
   │     logs del proyecto con taxonomía                            │
   │  4. Verifica: lint, sintaxis, activación, Unit, ATC, lectura   │
   │  5. Retrospectiva: ready_to_consolidate = true                 │
   │                                                                │
   └─────────────┬──────────────────────────────────────────────────┘
                 ▼
   ┌─ close_project.py (--dry-run, luego real) ────────────────────┐
   │  Promueve filas REUSE_YES / REUSE_PARTIAL al knowledge-base    │
   │  con códigos secuenciales por capability; referencia cruzada   │
   │  si ya existían; actualiza lessons-learned-index y estado;     │
   │  lint antes y después                                          │
   └─────────────┬──────────────────────────────────────────────────┘
                 ▼
         knowledge-base crece → el siguiente proyecto lo hereda
```

## Cómo usar este laboratorio

1. Abre esta carpeta como workspace: `D:\SAP ABAP BTP CPI Training\SAP-ABAP-LAB-001`. Lee `AGENTS.md` (o `CLAUDE.md` en Claude) y la [guía del loop](docs/guides/self-improvement-loop.md).

2. Para un requerimiento nuevo, crea el proyecto (el prefijo elige la capability del histórico):

   ```bash
   python scripts/workspace/projects.py create rap-002-ordenes-draft --title "Órdenes PM con draft"
   python scripts/workspace/projects.py list
   ```

   Abre `projects/<id>/docs/historical-context.md` y usa `prompts/00-nuevo-proyecto.md`.

3. Diseña, construye y verifica con `prompts/01` a `03`. Los errores van a `docs/error-log.md` y las decisiones a `docs/decision-log.md` en el momento en que ocurren.

4. Para practicar, genera un caso aislado con ID único:

   ```bash
   python scripts/workspace/new_case.py --domain RAP --level intermedio --topic "Órdenes con draft"
   ```

   Redacta el brief con `prompts/04-generar-caso-practica.md`. La solución queda oculta hasta resolverlo.

5. Al cerrar, ejecuta `prompts/05-retrospectiva-cierre.md` y:

   ```bash
   python scripts/workspace/close_project.py --project projects/<id> --dry-run
   python scripts/workspace/close_project.py --project projects/<id>
   ```

6. Valida en cualquier momento:

   ```bash
   python scripts/workspace/lint_knowledge_base.py
   python scripts/workspace/validate_structure.py
   python -m unittest discover -s scripts/workspace/tests
   ```

## Estructura

| Carpeta / archivo | Uso |
| --- | --- |
| [knowledge-base/](knowledge-base/README.md) | **Cerebro reutilizable del lab.** Taxonomía, errores `<CAP>-NNN`, patrones `P-NNN`, decisiones `D-NNN`, recetas `R-NNN`, índice de cierres. |
| [projects/](projects/README.md) | Un espacio independiente por proyecto: histórico del KB, diseño, logs, código, pruebas, evidencias, transportes. |
| [cases/](cases/README.md) | Casos de práctica `ABAP-CASE-<DOM>-<NNN>` aislados, con brief, rúbrica y solución oculta. |
| [prompts/](prompts/README.md) | Prompts reutilizables: kickoff (00), diseño (01), build (02), verificación (03), caso (04), cierre (05). |
| [checklists/](checklists/README.md) | Quality gates: ABAP, RAP release, clean core. |
| [standards/](standards/README.md) | Convenciones de nombres y matriz de decisión tecnológica. |
| [learning/](learning/README.md) | Ruta de estudio, ejercicios, sesiones, ADR de gobernanza, lecciones narrativas, backlog global. |
| [docs/](docs/README.md) | Guías de organización, flujo diario, loop de auto-mejora y manual operativo. |
| [scripts/](scripts/README.md) | Generadores, cierre, linter, validador y utilidades existentes. |
| [config/](config/README.md) | Inventario no secreto del sistema. |
| [artifacts/](artifacts/README.md) | Salidas regenerables y colecciones locales, excluidas de Git salvo su guía. |
| [AGENTS.md](AGENTS.md) / [CLAUDE.md](CLAUDE.md) | Reglas de agentes y adaptación para Claude. |
| [CONTEXT.txt](CONTEXT.txt) | Inventario legado sanitizado; la configuración y SAP en vivo prevalecen. |

## Knowledge base

| Archivo | Contenido |
|---|---|
| `knowledge-base/taxonomy.md` | Tags obligatorios (capability, categoría, severidad, reutilizable, origen) y formato de códigos. |
| `knowledge-base/error-catalog.md` | Errores resueltos con código por capability (`OO-001`, `API-001`, `ATC-001`, `TOOL-002`...). |
| `knowledge-base/solution-patterns.md` | Patrones validados (`P-001` report → clase cloud, `P-003` orden RAP, `P-004` diagnóstico CSRF...). |
| `knowledge-base/decision-registry.md` | Decisiones técnicas `D-NNN` (paquetes, APIs liberadas, pruebas, seguridad). |
| `knowledge-base/released-api-recipes.md` | Recetas `R-NNN`: reemplazos clásico → liberado, consumo OData con CSRF, comprobación de `API_STATE`. |
| `knowledge-base/lessons-learned-index.md` | Índice cruzado de proyectos y casos cerrados. |

## Regla principal

Cada requerimiento parte del contexto real leído en SAP, no de un proyecto anterior. `abap-001-equipos-cloud` sirve para aprender el patrón `P-001`, las recetas `R-001` a `R-005` y los errores `OO-001`, `ATC-001`, `TOOL-004`, pero no se copia su código sin confirmar objetos, paquete, `API_STATE` y nivel clean core del nuevo caso.

Para elegir tecnología usa `standards/technology-decision-matrix.md` antes de diseñar. Para dudas técnicas, primero el `knowledge-base/`, luego las skills ABAP instaladas, luego documentación SAP.

## Estado de seguridad
Las credenciales no viven en el repositorio. ARC-1 se autentica mediante el almacén privado local. La excepción TLS `SAP_INSECURE=true` es temporal (`SEC-001`) y debe eliminarse cuando Basis renueve el certificado del sistema.
