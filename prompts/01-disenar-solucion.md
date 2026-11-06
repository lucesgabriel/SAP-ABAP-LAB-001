# Prompt: Diseñar La Solución

Usa el proyecto `projects/<id>/` del workspace `SAP ABAP LAB 001`. El contexto SAP ya está leído en `docs/design.md`. Completa el diseño detallado; no construyas todavía.

## Skills a cargar

Según la tecnología elegida: `sap-abap:abap-cloud` + `sap-abap:released-abap-classes` (siempre); `sap-abap:rap` / `sap-abap:cds-view-entities` / `sap-abap:odata` / `anthropic-skills:abap-rap-senior` (RAP); `sap-abap:badi-enhancement` / `sap-abap:authorization-iam` (extensiones, DCL); `sap-abap:abap-cloud-migration` (si es migración de código clásico).

**Libros de referencia.** Lee los capítulos de la ruta elegida (`python scripts/workspace/books.py chapters --route <rap|cds|odata|enh|auth|cloud>`) y cítalos en "Knowledge-base consultado"; si el libro y el sistema difieren, prevalece la lectura SAP y se registra la decisión.

## Tareas

1. **Patrón base.** Elige el `P-XXX` de `knowledge-base/solution-patterns.md` más cercano (o justifica que no aplica ninguno). Adapta sus componentes al objeto real; no copies nombres de otro proyecto.

2. **Objetos y nombres.** Lista cada objeto a crear/modificar con tipo, nombre según `standards/naming-conventions.md`, paquete verificado y si es nuevo o cambio mínimo sobre uno existente (`D-009`).

3. **APIs y clean core.** Para cada tabla SAP, clase o campo `sy-*` que la solución use, indica el reemplazo liberado (recetas `R-XXX`) y el `API_STATE` leído. Si no hay reemplazo, registra la decisión de wrapper o de aceptar nivel B/C en `docs/decision-log.md`.

4. **Orden de escritura y activación.** Para varios objetos, lista el orden (RAP: `P-003`) y qué se activa en batch.

5. **Estrategia de pruebas.** ABAP Unit (test doubles de CDS/SQL cuando aplique), ATC con la variante indicada (`ABAP_CLOUD_READINESS` si el objetivo es cloud), ejecución en consola o preview Fiori. Vuelca los casos en `tests/plan.md` con resultado esperado verificable.

6. **Errores a prevenir.** Copia a `docs/error-log.md` (sección "Errores recurrentes a vigilar") los códigos del histórico que aplican a este diseño.

7. **Decisiones.** Registra en `docs/decision-log.md` cada elección con alternativas, motivo e impacto, con taxonomía válida.

8. **Pasa el checklist** `checklists/abap-quality-gate.md` sección Diseño (y `rap-release-gate.md` / `clean-core-gate.md` si aplican).

## Salida esperada

- `docs/design.md` completo: KB citado, tabla de objetos, tabla de reemplazos, orden de activación, pruebas, reversión.
- `docs/decision-log.md` con al menos: paquete/transporte, APIs de reemplazo, estrategia de pruebas, nivel clean core.
- `tests/plan.md` con casos principal, límite y error.
- Lista de riesgos abiertos.

## Restricciones

- Diseña con el diff mínimo sobre objetos existentes.
- No modifiques objetos estándar SAP salvo autorización explícita del usuario para el objeto exacto.
- Si una skill propone código, trátalo como propuesta: lo que cuenta es lo leído y activado en SAP.
