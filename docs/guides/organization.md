# Organización escalable

## Mapa

```text
SAP-ABAP-LAB-001/
  AGENTS.md, CLAUDE.md, README.md, CONTEXT.txt
  config/                     Inventario no secreto
  docs/
    guides/                   Organización y flujo diario
    ...                       Manual y referencias existentes
  projects/
    _template/                Base que copia el generador
    abap-001-nombre/           Un proyecto, un objetivo, un estado
      project.json            Identidad, estado, paquete y transporte
      docs/                   Diseño, backlog y diario
      src/                    Código local y exportaciones revisadas
      tests/                  Plan, casos y datos sintéticos
      evidence/               Resultados revisados y cierre
      transports/             Objetos, dependencias y reversión
  learning/
    roadmap.md                Ruta sugerida de estudio
    exercises/                Prácticas con objetivo y criterio de logro
    sessions/                 Bitácoras de aprendizaje
    templates/                Formatos de ejercicio y sesión
    lessons.md                Lecciones comprobadas reutilizables
    decisions.md              Decisiones globales vigentes
    patterns.md               Patrones aprobados
    backlog.md                Mejoras transversales del laboratorio
  scripts/
    workspace/                Generación, listado y validación local
    ...                       Utilidades existentes con rutas estables
  artifacts/                  Salidas locales regenerables
```

## Convenciones

- Carpetas nuevas: minúsculas, sin tildes ni espacios, palabras separadas por guion. Proyecto: `abap-001-tema`, `rap-002-tema`, `cds-003-tema`; tres dígitos como mínimo. El identificador no es un nombre de objeto SAP.
- Cada proyecto tiene su propia carpeta incluso si comparte sistema. Su `project.json` es la fuente del estado local; `projects.py list` genera el catálogo sin mantener otra tabla manual.
- Estados: `planned`, `active`, `blocked`, `completed`, `archived`. Conserva la ruta al cerrar o archivar para no romper enlaces. Registra el motivo del bloqueo en su backlog.
- Fechas de notas: `YYYY-MM-DD-tema.md`. Usa enlaces relativos dentro de Markdown para que funcionen en otro equipo.
- Código de clases: `src/classes/`; CDS: `src/cds/`; RAP: `src/rap/`; reportes: `src/reports/`. Crea estas subcarpetas solo al necesitarlas. Conserva nombres y serialización originales si importas una exportación abapGit; estas carpetas no constituyen por sí mismas un repositorio abapGit desplegable.
- Las pruebas ABAP Unit pertenecen a su clase/include en `src/`; `tests/` recoge escenarios, criterios y datos sintéticos.
- El código local es una propuesta o copia, según indique su procedencia. La versión activa leída en SAP sigue siendo la fuente de verdad.
- Un proyecto durable necesita paquete Z/Y y transporte válido verificados. No deducirlos del identificador local; `$TMP` se reserva para trabajo desechable.

## Qué guardar y dónde

| Contenido | Destino |
| --- | --- |
| Diseño y decisiones de un proyecto | `projects/<id>/docs/` |
| Código y pruebas vinculadas a objetos | `projects/<id>/src/` |
| Resumen sanitizado de lint, activación, Unit, ATC y lectura posterior | `projects/<id>/evidence/` |
| Inventario de objetos y plan de transporte/reversión | `projects/<id>/transports/` |
| Dudas y experimentos pendientes | Diario del proyecto o `learning/sessions/` |
| Lección útil para otros proyectos y ya comprobada | `learning/lessons.md`, enlazando la evidencia |
| PDFs, respuestas temporales, exportaciones generadas | `artifacts/<id>/` |
| Configuración privada y secretos | Almacén privado externo; nunca estas carpetas |

`artifacts/` está ignorado por Git; eso no lo convierte en almacén de secretos. Mantén allí solo salidas sanitizadas. Antes de versionar una evidencia, revisa cabeceras, capturas, identificadores y datos de negocio. El validador de estructura no inspecciona secretos ni garantiza sanitización.

## Crecer sin perder orden

1. Crea el proyecto con la plantilla; define un resultado comprobable en el backlog.
2. Añade subcarpetas de código cuando exista contenido, sin copiar árboles vacíos por tecnología.
3. Registra cada objeto compartido con un proyecto propietario y enlaces desde sus consumidores; evita copias divergentes.
4. Mantén el historial específico dentro del proyecto y promueve solo conocimiento reutilizable a `learning/`.
5. Al cerrar, completa `evidence/completion.md`, actualiza el estado y conserva los enlaces. No liberar transportes ni borrar objetos como parte de archivar archivos.

## Compatibilidad y reversión

No se han trasladado los manuales, scripts originales, configuración, colecciones locales ni registros de aprendizaje. Las reglas de `AGENTS.md` siguen intactas. La estructura nueva se añade mediante archivos revisables con Git; no requiere escribir en SAP. Para revertir esta organización, revisa el diff y retira únicamente las incorporaciones de esta entrega, conservando cualquier proyecto creado después. No uses un reset global sobre el trabajo previo.
