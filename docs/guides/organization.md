# Organización escalable

## Mapa

```text
SAP-ABAP-LAB-001/
  AGENTS.md, CLAUDE.md, README.md, CONTEXT.txt
  config/                     Inventario no secreto
  knowledge-base/             Cerebro reutilizable del lab
    taxonomy.md               Tags obligatorios y formato de códigos
    error-catalog.md          Errores <CAP>-NNN
    solution-patterns.md      Patrones P-NNN
    decision-registry.md      Decisiones D-NNN
    released-api-recipes.md   Recetas R-NNN
    lessons-learned-index.md  Índice de cierres
  projects/
    _template/                Base que copia el generador
    abap-001-nombre/          Un proyecto, un objetivo, un estado
      project.json            Identidad, estado, capability, paquete, transporte, ready_to_consolidate
      docs/                   historical-context (inyectado), design, backlog, journal, error-log, decision-log
      src/                    Código local y exportaciones revisadas
      tests/                  Plan, casos y datos sintéticos
      evidence/               Resultados revisados y ficha de cierre
      transports/             Objetos, dependencias y reversión
  cases/
    _template/                Brief, histórico, rúbrica, solución oculta, metadata
    ABAP-CASE-RAP-001-tema/   Un caso de práctica aislado (misma estructura docs/src/tests/evidence)
    _index.md, _status.md     Registro y tablero de casos
  prompts/                    00 kickoff · 01 diseño · 02 build · 03 verificación · 04 caso · 05 cierre
  checklists/                 abap-quality-gate · rap-release-gate · clean-core-gate
  standards/                  naming-conventions · technology-decision-matrix
  learning/
    roadmap.md                Ruta sugerida de estudio
    exercises/, sessions/     Prácticas y bitácoras personales
    templates/                Formatos de ejercicio y sesión
    lessons.md                Lecciones narrativas con evidencia (enlazan su código KB)
    decisions.md              ADR de gobernanza del laboratorio
    patterns.md               Índice corto → solution-patterns.md
    backlog.md                Mejoras transversales del laboratorio
  docs/
    guides/                   Organización, flujo diario, loop de auto-mejora
    ...                       Manual y referencias existentes
  scripts/
    workspace/                kb.py, projects.py, new_case.py, close_project.py, lint_knowledge_base.py, validate_structure.py, tests/
    ...                       Utilidades existentes con rutas estables
  artifacts/                  Salidas locales regenerables (ignoradas por Git)
```

## Convenciones

- Carpetas nuevas: minúsculas, sin tildes ni espacios, palabras separadas por guion. Proyecto: `abap-001-tema`, `rap-002-tema`, `cds-003-tema`; tres dígitos como mínimo. El prefijo fija la capability del histórico del KB (`abap`→OO, `cds`→CDS, `rap`→RAP, `sql`→SQL, `enh`→ENH, `api`→API, `ui`→UI, `mix`→MULTI). El identificador no es un nombre de objeto SAP.
- Casos: `ABAP-CASE-<DOM>-<NNN>-<slug>`; el generador asigna el ID y nunca se edita a mano.
- Cada proyecto tiene su propia carpeta incluso si comparte sistema. Su `project.json` es la fuente del estado local; `projects.py list` genera el catálogo sin mantener otra tabla manual.
- Estados: `planned`, `active`, `blocked`, `completed`, `archived`. `completed` lo fija `close_project.py` tras promover lecciones; conserva la ruta al cerrar o archivar.
- Fechas de notas: `YYYY-MM-DD-tema.md`. Usa enlaces relativos dentro de Markdown para que funcionen en otro equipo.
- Código de clases: `src/classes/`; CDS: `src/cds/`; RAP: `src/rap/`; reportes: `src/reports/`. Crea estas subcarpetas solo al necesitarlas. Conserva nombres y serialización originales si importas una exportación abapGit; estas carpetas no constituyen por sí mismas un repositorio abapGit desplegable.
- Las pruebas ABAP Unit pertenecen a su clase/include en `src/`; `tests/` recoge escenarios, criterios y datos sintéticos.
- El código local es una propuesta o copia, según indique su procedencia. La versión activa leída en SAP sigue siendo la fuente de verdad.
- Un proyecto durable necesita paquete Z/Y y transporte válido verificados. No deducirlos del identificador local; `$TMP` se reserva para trabajo desechable (`D-007`).
- Nombres de objetos SAP: `standards/naming-conventions.md`.

## Qué guardar y dónde

| Contenido | Destino |
| --- | --- |
| Diseño y decisiones de un proyecto | `projects/<id>/docs/design.md`, `decision-log.md` |
| Errores encontrados y resueltos en un proyecto | `projects/<id>/docs/error-log.md` (con taxonomía) |
| Código y pruebas vinculadas a objetos | `projects/<id>/src/` |
| Resumen sanitizado de lint, activación, Unit, ATC y lectura posterior | `projects/<id>/evidence/` |
| Inventario de objetos y plan de transporte/reversión | `projects/<id>/transports/` |
| Dudas y experimentos pendientes | Diario del proyecto o `learning/sessions/` |
| Error, decisión, patrón o receta reutilizable y comprobada | `knowledge-base/` vía `close_project.py` (errores/decisiones) o a mano (patrones/recetas) |
| Lección narrativa útil para otros proyectos | `learning/lessons.md`, enlazando el código KB y la evidencia |
| Enunciado, rúbrica y solución de un caso de práctica | `cases/<CASE-ID>-<slug>/` |
| PDFs, respuestas temporales, exportaciones generadas | `artifacts/<id>/` |
| Configuración privada y secretos | Almacén privado externo; nunca estas carpetas |

`artifacts/` está ignorado por Git; eso no lo convierte en almacén de secretos. Mantén allí solo salidas sanitizadas. Antes de versionar una evidencia, revisa cabeceras, capturas, identificadores y datos de negocio. El validador de estructura no inspecciona secretos; el linter del KB sí busca patrones comunes en `knowledge-base/`, `projects/` y `cases/`, pero no sustituye la revisión manual.

## Crecer sin perder orden

1. Crea el proyecto o caso con el generador; lee el histórico inyectado; define un resultado comprobable en el backlog.
2. Añade subcarpetas de código cuando exista contenido, sin copiar árboles vacíos por tecnología.
3. Registra cada objeto compartido con un proyecto propietario y enlaces desde sus consumidores; evita copias divergentes.
4. Mantén el historial específico dentro del proyecto y promueve solo conocimiento reutilizable al KB mediante el cierre.
5. Al cerrar, completa `evidence/completion.md`, ejecuta `close_project.py` y conserva los enlaces. No liberar transportes ni borrar objetos como parte de archivar archivos.

## Compatibilidad y reversión

Los manuales, scripts originales, configuración, colecciones locales y registros de aprendizaje conservan sus rutas. El loop de auto-mejora (2026-10-01) añade `knowledge-base/`, `cases/`, `prompts/`, `checklists/`, `standards/`, tres documentos por proyecto y los scripts `kb.py`, `new_case.py`, `close_project.py` y `lint_knowledge_base.py`; `projects.py` y `validate_structure.py` se extienden sin romper proyectos anteriores (los campos nuevos de `project.json` son opcionales). Nada de esto escribe en SAP. Para revertir, revisa el diff y retira únicamente las incorporaciones de esa entrega, conservando cualquier proyecto o caso creado después. No uses un reset global sobre el trabajo previo.
