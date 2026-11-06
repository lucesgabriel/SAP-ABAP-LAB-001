# Prompt: Generar Un Caso De Práctica

Usa el workspace `SAP ABAP LAB 001`. Quiero practicar `<tema>` en el dominio `<OO|CDS|RAP|SQL|ENH|API|UI|MIX>` a nivel `<basico|intermedio|avanzado|examen>`.

## Skills a cargar

La del dominio del caso (`sap-abap:rap`, `cds-view-entities`, `abap-sql-amdp`, `badi-enhancement`, `odata`, `abap-cloud` para OO/clean core) más `anthropic-skills:abap-senior` para redactar el enunciado y la solución.

**Libros de referencia.** Ancla el caso a un capítulo concreto (`python scripts/workspace/books.py chapters --route <dominio>`) y cítalo en el brief como lectura previa; redacta el enunciado con tus palabras, sin copiar ejercicios del libro.

## Tareas

1. **Crea la estructura formal** (no crees carpetas ad-hoc):

   ```bash
   python scripts/workspace/new_case.py --domain <DOM> --level <nivel> --topic "<tema>" --time <min> --package <paquete o $TMP>
   ```

2. **Lee** `cases/<CASE-ID>-<slug>/00-case-brief/historical-context.md` para conocer los códigos del KB que el caso debe ejercitar o prevenir.

3. **Redacta el brief** en `00-case-brief/case-brief.md` completando TODAS las secciones de la plantilla: contexto empresarial ficticio (Globex, Acme, Initech...), objetivo técnico, requerimiento exacto numerado, nombres obligatorios de objetos según `standards/naming-conventions.md`, datos entregados, entrada/salida esperada, precondiciones, pasos esperados, diseño esperado sin revelar la solución, validaciones, errores comunes (cita códigos del KB) y tres hints progresivos. Usa las skills `abap-senior`, `abap-rap-senior` o `sap-abap:*` según el dominio para que el enunciado sea técnicamente correcto en S/4HANA 2025.

4. **Redacta la solución** en `solution/expected-solution.md`: objetos finales, diseño de referencia, código de referencia completo, verificación esperada (sintaxis, activación, ATC, Unit, resultado) y errores típicos. Marca el archivo como oculto en la cabecera.

5. **Ajusta la rúbrica** en `rubric/checklist-100.md` con ítems concretos del caso en cada bloque.

6. **Verifica** que las tablas/vistas/APIs que el caso usa existen en el sistema (`SAPRead`, `R-007`); si no puedes verificarlo, decláralo en el brief como supuesto a comprobar por quien resuelve.

7. Ejecuta `python scripts/workspace/lint_knowledge_base.py` y `python scripts/workspace/validate_structure.py`.

## Salida esperada

- Caso creado con ID secuencial, brief completo, rúbrica concreta y solución oculta.
- Lista de códigos del KB que el caso ejercita.
- Nota de qué partes del brief dependen de objetos del sistema no verificados.

## Restricciones

- No uses datos, nombres ni montos de clientes reales; ofusca.
- Sin secretos; placeholders `<TU_USUARIO>`.
- No reveles la solución en el brief ni en los hints.
- Namespace reservado: `ABAP-CASE-*` lo asigna el generador; no inventes IDs.
