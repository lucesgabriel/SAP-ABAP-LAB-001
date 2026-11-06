# Backlog de mejora

- [ ] Solicitar a Basis la renovación del certificado TLS y retirar `SAP_INSECURE=true` de Hermes y Claude Desktop.
- [ ] Evaluar activación del servicio ICF de búsqueda de texto ADT si el equipo necesita búsqueda full-text.
- [ ] Decidir si se activa abapGit; gCTS ya está disponible.
- [ ] Definir paquete(s) `Z*` de entrenamiento y capa/target de transporte preferidos.
- [ ] Ejecutar un ciclo de vida controlado de objeto desechable antes del primer proyecto real: crear → lint/sintaxis → activar → Unit/ATC → leer → borrar con confirmación.
- [ ] Revisar trimestralmente `learning/` y retirar reglas obsoletas.
- [ ] Aplicar la nueva plantilla al primer proyecto ABAP real y contrastar la ficha de cierre con evidencia SAP; la organización local ya está verificada, pero no acredita un ciclo ABAP ejecutado.
- [ ] Cerrar formalmente `projects/abap-001-equipos-cloud` con `close_project.py` (los códigos ya existen en el KB; el cierre debe dejar `completed` y la fila oficial en `lessons-learned-index.md`), incluyendo el ABAP Unit pendiente.
- [ ] Validar `P-003` (orden de activación RAP) en un proyecto `rap-NNN` real y actualizar su evidencia en `solution-patterns.md`.
- [ ] Generar el primer caso de práctica por dominio (`OO`, `CDS`, `RAP`) con `new_case.py` y redactar brief + solución con `prompts/04`.
- [ ] Evaluar una tarea agendada semanal que ejecute `close_project.py` sobre proyectos con `ready_to_consolidate: true` (equivalente a `sap-codex-lab-weekly-consolidation` del Integration Suite Lab).
- [ ] Revisar trimestralmente el `knowledge-base/`: obsoletos con fecha y reemplazo, nunca renumerar.
- [ ] Localizar el repositorio de las skills comunitarias de la SAP AI Skills Library que no están instaladas — **ABAP RAP** (Daniel Krompaß), **Clean ABAP** (Attila Berencsi) y **Off-Stack ABAP Unit + abaplint CI** (Alok Mehta) — inspeccionar su contenido y, si aportan, añadirlas a `.claude/settings.json` y a `config/skills-routing.json`.
- [ ] Completar páginas `null` de `hana-2021` en `config/books.json` (el PDF no expone destinos en el índice) y regenerar `docs/guides/reference-library.md` con `books.py render`.
- [ ] Tras el primer proyecto que cite libros, revisar si el ruteo de `config/skills-routing.json` sugirió los capítulos correctos y ajustar palabras clave.

