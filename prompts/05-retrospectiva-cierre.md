# Prompt: Retrospectiva Y Cierre

Usa `projects/<id>/` (o `cases/<CASE-ID>-<slug>/`) del workspace `SAP ABAP LAB 001`. Objetivo: cerrar el trabajo, extraer aprendizajes reutilizables y alimentar el `knowledge-base/` para que el próximo proyecto los herede desde el día cero.

## Tareas

1. **Verifica el estado de cierre:**
   - [ ] `evidence/completion.md` completo con evidencia real (lint clasificado, sintaxis, activación, lectura posterior, INACTIVE_OBJECTS, Unit, ATC, dependencias, transporte, reversión).
   - [ ] `docs/design.md` cita los códigos del KB usados (sección "Knowledge-base consultado").
   - [ ] `tests/plan.md` con resultados reales.
   - [ ] Para casos: `Resuelto: Si` y comparación con `solution/expected-solution.md` anotada en `docs/journal.md`.

2. **Revisa `docs/error-log.md`:**
   - Cada fila tiene capability, categoría, severidad, origen y `YES`/`PARTIAL`/`NO` válidos (`knowledge-base/taxonomy.md`).
   - Si el error ya existe en `error-catalog.md`, pon su código en `Promovido` (se añadirá referencia cruzada, no duplicado).
   - Las filas `YES`/`PARTIAL` nuevas tienen sección de detalle `### ER-XX | Título` con síntoma, causa raíz, solución, prevención y evidencia: ese texto es el que entra al KB.
   - Marca `NO` lo que es específico de este objeto y no sirve a otros.

3. **Revisa `docs/decision-log.md`** con el mismo criterio. Si una decisión confirma una `D-NNN`, cítala en `Promovido`; si la contradice, descríbelo para actualizar la entrada del registry a mano.

4. **Patrones y recetas.** ¿Surgió un patrón nuevo demostrado (activado, probado, releído)? Redacta `P-NNN` en `solution-patterns.md`. ¿Una receta de reemplazo nueva o un gotcha de una existente? Actualiza `released-api-recipes.md`. Añade fila al changelog del archivo.

5. **Lección narrativa.** Si hay una lección con evidencia que merece explicación larga, añádela a `learning/lessons.md` enlazando el código KB; no dupliques lo que ya dice el catálogo.

6. **Marca listo** `"ready_to_consolidate": true` en `project.json` (o `metadata.json`, junto con `"resolved": true`).

7. **Cierra:**

   ```bash
   python scripts/workspace/close_project.py --project <ruta> --dry-run
   python scripts/workspace/close_project.py --project <ruta>
   python scripts/workspace/lint_knowledge_base.py
   python scripts/workspace/validate_structure.py
   ```

8. **Higiene:** ningún secreto en el proyecto ni en el KB; changelogs actualizados; `git status` revisado antes de versionar.

## Salida esperada

- Lista de códigos KB promovidos (errores, decisiones, patrones, recetas) con su origen.
- Estado `completed` y `consolidated_on` en el metadato del proyecto/caso.
- Resumen ejecutivo de 3–5 aprendizajes que el próximo proyecto debe heredar.
- Deuda pendiente trasladada a `learning/backlog.md` (global) o al backlog del proyecto.

## Restricciones

- No promover `REUSE_NO`.
- No promover hipótesis: solo lo verificado en SAP.
- No copiar secretos ni datos de negocio al KB.
- Si dos proyectos resuelven lo mismo con soluciones distintas, registrar ambas con el contexto que las diferencia.
