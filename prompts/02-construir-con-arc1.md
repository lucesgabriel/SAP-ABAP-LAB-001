# Prompt: Construir Con ARC-1

Usa el proyecto `projects/<id>/` del workspace `SAP ABAP LAB 001`. El diseño en `docs/design.md` está aprobado. Construye siguiendo el flujo obligatorio de `AGENTS.md` (patrón `P-002`).

## Skills a cargar

`anthropic-skills:abap-senior` para el código; `sap-abap:abap-sql-amdp` si hay SQL moderno o AMDP; la skill de la tecnología usada en el diseño (`sap-abap:rap`, `cds-view-entities`...).

**Libros de referencia.** Ante una duda puntual de sintaxis o comportamiento: `python scripts/workspace/books.py search "<término>" --route <id>`. El código de `supplements` se adapta con nombres del lab; nunca se pega tal cual.

## Tareas

Para cada objeto, en el orden definido en el diseño:

1. **Prevalida** el código propuesto: `SAPLint` y, tras escribir, `SAPDiagnose action=syntax version=inactive`. Clasifica cada aviso de lint como falso positivo / aceptado / a corregir (`TOOL-004`).
2. **Escribe** con `SAPWrite` (create para objetos nuevos; `edit_method` / `edit_class_definition` / `edit_text_symbols` para cambios, `D-009`). Guarda la copia en `src/` indicando procedencia.
3. **Corrige** los warnings de sintaxis en la versión inactiva antes de activar (`OO-001`, `OO-002`).
4. **Activa** con `SAPActivate` (batch si hay dos o más objetos) y comprueba `INACTIVE_OBJECTS` vacío.
5. **Relee** la versión activa (`SAPRead force_refresh`) y confirma que coincide con `src/`.
6. **Registra en el momento**: cada error en `docs/error-log.md` con taxonomía (síntoma, causa raíz, solución, reutilizable), cada cambio de rumbo en `docs/decision-log.md`, el avance en `docs/journal.md` y `docs/backlog.md`.

## Salida esperada

- Objetos activos en SAP y copia en `src/`.
- `docs/error-log.md` con las filas de esta sesión (aunque el error se haya resuelto en segundos: si es reutilizable, vale).
- `evidence/<fecha>-build.md` con resumen sanitizado: objetos, lint, sintaxis, activación, lectura posterior.
- Siguiente paso explícito (pruebas y ATC: prompt 03).

## Restricciones

- Nunca afirmes que un write compila; solo la activación y la lectura posterior lo demuestran.
- Para `delete`, liberación de transportes, `unpublish`, gCTS push/commit, SQL modificador o cualquier acción irreversible: pide confirmación explícita inmediatamente antes.
- No modifiques objetos estándar SAP salvo autorización explícita para el objeto exacto.
- No pegues credenciales, cookies, tokens ni datos de negocio sensibles en ningún archivo.
- Si un error no está en el KB y lo resolviste, es candidato `REUSE_YES` o `REUSE_PARTIAL`: regístralo con detalle suficiente para que otro lo reproduzca.
