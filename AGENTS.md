# SAP ABAP LAB 001 — Reglas para agentes

Responde en español. Mantén los términos SAP técnicos en inglés cuando sean nombres de producto, objeto o herramienta: ABAP Cloud, RAP, CDS, behavior definition, service binding, ATC, ABAP Unit, clean core, ADT, gCTS.

## Objetivo
Este repositorio es el centro de trabajo para desarrollar, revisar, probar y documentar soluciones ABAP en el sistema de laboratorio S/4HANA descrito en `config/system.yaml`, **y para que cada proyecto deje conocimiento reutilizable al siguiente** a través del `knowledge-base/`.

Estas reglas se aplican a Hermes Desktop, Claude Code, Claude Desktop / Cowork, Codex y cualquier agente que cargue `AGENTS.md`.

## Fuentes de verdad
1. `config/system.yaml`: identidad y capacidades no secretas del sistema.
2. Código y metadatos leídos en vivo con ARC-1: estado actual de SAP.
3. `knowledge-base/`: errores (`<CAP>-NNN`), patrones (`P-NNN`), decisiones (`D-NNN`) y recetas (`R-NNN`) consolidados; `taxonomy.md` define los tags.
4. `learning/decisions.md` (ADR de gobernanza) y `learning/lessons.md` (lecciones narrativas con evidencia).
5. `CONTEXT.txt`: inventario legado sanitizado; nunca debe contener contraseñas.

Cuando una nota local contradiga una lectura actual de SAP, prevalece SAP y se corrige la nota. Cuando una entrada del KB quede obsoleta, se marca con fecha y reemplazo; nunca se renumera.

## Loop de auto-mejora (obligatorio)

El laboratorio mantiene un **knowledge-base global** que se consulta al abrir cada proyecto o caso y se enriquece al cerrarlo. Esto es lo que diferencia este lab de una carpeta de proyectos.

1. **Al abrir un proyecto o caso**, el generador inyecta `docs/historical-context.md` (o `00-case-brief/historical-context.md`) con los códigos del KB filtrados por capability. Léelos todos y cita en `docs/design.md` (sección "Knowledge-base consultado") los que reutilizas: `P-001`, `D-008`, `R-002`, `OO-001`, etc. Si ninguno aplica, justifícalo.

   ```bash
   python scripts/workspace/projects.py create rap-002-tema --title "Título"      # proyecto
   python scripts/workspace/new_case.py --domain RAP --topic "Tema" --level intermedio   # caso de práctica
   python scripts/workspace/projects.py refresh-context rap-002-tema              # si el KB cambió
   ```

2. **Durante build y verificación**, registra en el momento:
   - `docs/error-log.md`: cada error con capability, categoría, severidad, origen y `YES`/`PARTIAL`/`NO` (`knowledge-base/taxonomy.md`). Si ya existe en el catálogo, cita su código en `Promovido`.
   - `docs/decision-log.md`: cada decisión con alternativas, motivo e impacto.

3. **Al cerrar**, ejecuta `prompts/05-retrospectiva-cierre.md`, marca `"ready_to_consolidate": true` (y `"resolved": true` en casos) y corre:

   ```bash
   python scripts/workspace/close_project.py --project projects/<id> --dry-run
   python scripts/workspace/close_project.py --project projects/<id>
   ```

   Las filas `YES`/`PARTIAL` se promueven al KB con el siguiente código secuencial; las ya conocidas reciben referencia cruzada; `lessons-learned-index.md` y el estado del proyecto se actualizan. Nunca se promueve `REUSE_NO` ni hipótesis.

4. **Patrones y recetas** se redactan a mano al cierre (`solution-patterns.md`, `released-api-recipes.md`) solo cuando están demostrados con activación, prueba y lectura posterior.

5. **Validación en cualquier momento:**

   ```bash
   python scripts/workspace/lint_knowledge_base.py          # tags, IDs, secretos, referencias cruzadas, IDs de casos
   python scripts/workspace/validate_structure.py           # archivos, metadatos, enlaces
   python -m unittest discover -s scripts/workspace/tests   # pruebas de las utilidades
   ```

## Casos de práctica (`cases/`)

Aparte de los proyectos (`projects/`), el laboratorio genera **casos de práctica** con ID único `ABAP-CASE-<DOMINIO>-<NNN>` (dominios `OO, CDS, RAP, SQL, ENH, API, UI, MIX`) aislados en su carpeta. Mismo loop: consultan el KB al nacer y lo enriquecen al cerrarse.

- Cuando el usuario pida "generar un caso", "practicar X", "armar un drill" o "simular examen": usar `prompts/04-generar-caso-practica.md`, que primero ejecuta `new_case.py` y luego redacta el brief con las skills ABAP.
- `solution/expected-solution.md` permanece **oculta** hasta marcar `Resuelto: Si`.
- Empresas y datos ficticios; sin secretos; sin datos de clientes reales.

## Seguridad y secretos
- Nunca escribir contraseñas, tokens, cookies o claves en este repositorio, chats, argumentos de proceso, capturas o manuales. El linter del KB busca patrones de secretos.
- Usar exclusivamente el almacén privado ya configurado para ARC-1.
- El servidor ARC-1 puede exponer capacidades amplias; eso no elimina la revisión humana.
- No modificar objetos estándar SAP salvo que el usuario nombre explícitamente el objeto y autorice el cambio concreto.
- Para `delete`, liberación de transportes, `unpublish`, push/commit gCTS, SQL que modifique datos o acciones irreversibles: pedir confirmación explícita inmediatamente antes.
- Consultas de datos: seleccionar solo columnas necesarias, filtros restrictivos y límites pequeños. No exportar masivamente datos personales, financieros, HR o credenciales.

## Flujo obligatorio para cambios ABAP (`P-002`)
1. **Entender**: usar `SAPContext` y después `SAPSearch`/`SAPRead`; identificar paquete, dependencias, API release (`R-007`) y transportes. La conexión está lista solo tras una lectura no destructiva (`TOOL-003`).
2. **Diseñar**: elegir tecnología con `standards/technology-decision-matrix.md`, nombres con `standards/naming-conventions.md`, paquete y transporte (`D-007`). Para pruebas desechables usar `$TMP`; para trabajo durable, paquetes `Z*`/`Y*` y transporte válido.
3. **Preparar**: trabajar con el diff mínimo. Para clases preferir edición de método sobre reemplazo completo (`D-009`).
4. **Prevalidar**: ejecutar `SAPLint` (clasificar avisos, `TOOL-004`) y `SAPDiagnose action=syntax` sobre la versión inactiva. En RAP, ordenar dependencias TABL → DDLS → DCLS → BDEF → behavior pool → SRVD → SRVB (`P-003`).
5. **Escribir**: usar `SAPWrite`; nunca afirmar que una escritura compila solo porque el write respondió correctamente.
6. **Activar**: usar `SAPActivate`; para dos o más objetos usar activación batch.
7. **Verificar**: volver a leer, confirmar `INACTIVE_OBJECTS` limpio, ejecutar ABAP Unit y ATC cuando corresponda (variante `ABAP_CLOUD_READINESS` si el objetivo es cloud, `ATC-001`), y revisar dependencias/where-used.
8. **Documentar**: ficha de cierre, logs con taxonomía, y solo aprendizajes comprobados en `learning/` y el KB.

## Criterio de terminado
Una tarea de desarrollo no está terminada hasta que estén documentados en `evidence/completion.md`:
- objetos afectados y paquete;
- diff o descripción exacta del cambio;
- resultado de lint (clasificado) y sintaxis;
- resultado de activación;
- resultado de pruebas/ATC o motivo explícito por el que no aplican;
- lectura posterior que confirme el estado final;
- riesgos, transporte y pasos de reversión;
- `docs/error-log.md` y `docs/decision-log.md` con taxonomía válida y `YES`/`PARTIAL`/`NO` decidido.

Los checklists de `checklists/` resumen estos puntos por fase.

## Selección de skills

Fuente principal: el plugin **SAP ABAP** de la SAP AI Skills Library (Lik Wei Tan, 18 skills, prefijo `sap-abap:` en Claude Code / Cowork). Cargar la skill de la fase antes de actuar; una skill propone código, lo que cuenta es lo leído y activado en SAP.

### Qué skill cargar en cada fase

| Fase / prompt | Skill principal | Complementarias | Para qué |
|---|---|---|---|
| Kickoff y diseño (`prompts/00`, `01`) | `sap-abap:abap-cloud` | `sap-abap:released-abap-classes`, `sap-abap:abap-cloud-migration` | Nivel clean core objetivo, reemplazos liberados (`D-008`, `R-00x`, `P-001`). |
| Diseño RAP / CDS / OData | `sap-abap:rap` | `sap-abap:cds-view-entities`, `sap-abap:odata`, `anthropic-skills:abap-rap-senior`, `abap-rap` (Krompaß, checklist de errores comunes) | BO, proyecciones, service binding (`P-003`, `rap-release-gate`). |
| Diseño de extensiones y autorizaciones | `sap-abap:badi-enhancement` | `sap-abap:authorization-iam` | Dominio `ENH`, DCL, objetos de autorización. |
| Build clásico / Clean ABAP (`prompts/02`) | `anthropic-skills:abap-senior` | `sap-abap:abap-sql-amdp` | Código ABAP, SQL moderno, AMDP solo con evidencia. |
| Verificación (`prompts/03`) | `sap-abap:abap` (abaplint + Clean ABAP) | `sap-abap:atc-cloudification`, `sap-abap:abap-unit-testing`; `/clean-abap:review` o `clean-abap-guide` (Clean ABAP de Attila Berencsi) como segunda revisión de estilo | Lint clasificado (`TOOL-004`), ATC (`ATC-001`, `P-005`), ABAP Unit con test doubles. |
| Caso de práctica (`prompts/04`) | La del dominio del caso (tabla anterior) | `anthropic-skills:abap-senior` para el enunciado | Brief técnicamente correcto en S/4HANA 2025. |

### Ruteo automático (hooks)
`config/skills-routing.json` es la fuente única del ruteo fase/dominio → skill → libros. En Claude Code, `.claude/settings.json` habilita los plugins del lab a nivel proyecto y ejecuta `scripts/workspace/skill_router.py`:
- **SessionStart**: inyecta el mapa de skills por fase y el estado de la biblioteca.
- **UserPromptSubmit**: detecta el dominio del mensaje (RAP, CDS, OData, SQL, ENH, ATC, Unit, clásico...) e inyecta qué skills cargar, qué códigos del KB consultar y qué capítulos de libro leer.

Cuando el hook sugiera skills, cárgalas con la herramienta Skill antes de diseñar o escribir código (solo las pertinentes). Otros agentes obtienen lo mismo con `python scripts/workspace/skill_router.py suggest "<petición>"`. Para cambiar el ruteo se edita el JSON, no el script.

No cargar por defecto en este sistema: `sap-abap:btp-abap-environment` (el laboratorio es S/4HANA on-premise, no Steampunk), `sap-abap:abapgit` (endpoint ICF inactivo, se usa gCTS — `CTS-001`), `sap-abap:rap-business-events`, `sap-abap:sap-fiori-url-generator`. Skills comunitarias vendorizadas en `.claude/skills/` (`abap-rap`, `clean-abap-guide`): revisadas y con origen y commit en `.claude/skills/README.md`; ante conflicto mandan `standards/` y el KB. **Off-Stack ABAP Unit + abaplint CI** (Alok Mehta) no está instalada: candidata en `learning/backlog.md`.

### Hermes Desktop
Equivalentes locales: `clean-abap-review`, `clean-abap-refactor`, `abap-cloud-rap-design`, `abap-atc-remediation`, `abap-clean-core-check`, `sap-abap-agentic-development`.

### Claude Code / Cowork
Plugins: `clean-abap@claude-abap-skills` (`/clean-abap:review`, `/clean-abap:refactor`), `abap-cloud-rap@claude-abap-skills` (`/abap-cloud-rap:rap-bo-design`, `/abap-cloud-rap:atc-remediation`, `/abap-cloud-rap:clean-core-check`), `arc-1@arc-1`, más las skills `sap-abap:*` y `anthropic-skills:abap-senior` / `abap-rap-senior` de la tabla.

### Claude Desktop
Claude Desktop usa ARC-1 como MCP, pero no carga plugins de Claude Code. Adjuntar o copiar `docs/CLAUDE-DESKTOP-PROJECT-INSTRUCTIONS.md` en las instrucciones del proyecto de Claude Desktop.

Si el usuario entrega una skill `.skill`, inspeccionar su contenido antes de usarla.

## Biblioteca de referencia (libros)
Los libros SAP PRESS y apuntes viven **fuera** del repositorio (`../books`, o `SAP_LAB_BOOKS_ROOT`). `config/books.json` los cataloga con capítulo, página del PDF y ruta de skill; `docs/guides/reference-library.md` es su vista generada.

- Consulta el capítulo que sugiere el hook o `python scripts/workspace/books.py chapters --route <id>`; busca términos con `python scripts/workspace/books.py search "<término>" --route <id>` (requiere `books.py index` una vez; el índice queda en `artifacts/`, ignorado por git).
- Precedencia: lectura SAP en vivo > `knowledge-base/` > libros. Un libro describe una release concreta; si contradice el sistema S/4HANA 2025, prevalece el sistema y se registra en `docs/decision-log.md`.
- Cita libros como `slug cap.N p.X` en `docs/design.md` (sección "Knowledge-base consultado") y en briefs de casos. No copies texto, listados ni figuras al repositorio, al KB ni a PDFs generados: resume con tus palabras.
- El código de los `supplements` (por ejemplo, la app abapGit de `cookbook-2026` o los objetos de `rap-2025`) es referencia: se adapta con nombres del lab y pasa el flujo `P-002` completo.

## Prompts, checklists y standards
- `prompts/00` a `05`: kickoff, diseño, build, verificación, caso de práctica, cierre.
- `checklists/`: `abap-quality-gate.md` (siempre), `rap-release-gate.md` (RAP), `clean-core-gate.md` (cloud readiness).
- `standards/`: `naming-conventions.md`, `technology-decision-matrix.md`.

## Aprendizaje continuo y automejora
Después de cada entrega verificada:
1. Cerrar el proyecto con `close_project.py` para promover errores y decisiones al KB.
2. Redactar patrones (`P-NNN`) y recetas (`R-NNN`) nuevos solo con evidencia.
3. Añadir a `learning/lessons.md` únicamente lecciones narrativas con evidencia, enlazando su código KB.
4. Registrar decisiones de gobernanza del laboratorio en `learning/decisions.md` (ADR) y su espejo técnico en `decision-registry.md`.
5. Registrar deuda o mejoras pendientes en `learning/backlog.md`.
6. Eliminar o reemplazar información obsoleta; no acumular duplicados.
7. Nunca convertir una hipótesis, error transitorio o dato sensible en aprendizaje permanente.

Las reglas de este archivo solo se cambian cuando una lección se repite o una decisión de gobernanza lo requiere. Toda automejora debe ser revisable mediante Git.
