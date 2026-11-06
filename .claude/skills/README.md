# Skills del proyecto (vendorizadas)

Skills comunitarias de la [SAP AI Skills Library](https://skills.cloud.sap) copiadas tras revisar su contenido (`AGENTS.md`: inspeccionar antes de usar). Claude Code las carga automáticamente al abrir este proyecto; no requieren `npx skills add`.

| Skill | Autor | Origen (commit revisado) | Licencia | Cambios locales |
|---|---|---|---|---|
| `abap-rap` | Daniel Krompaß | `DanKromp/skillOverflow` `skills/abap-rap` @ `bfea98869237` (2026-08-28) | Apache-2.0 | Ninguno. |
| `clean-abap-guide` | Attila Berencsi | `attilaberencsi/sapskills` `skills/clean-abap` @ `b7f2dc96cd57` (2026-10-27) | Apache-2.0 | `name` cambiado de `clean-abap` a `clean-abap-guide` para no confundirse con el plugin `clean-abap@claude-abap-skills`. |

## Revisión (2026-11-06)

- **`abap-rap`**: solo markdown y una plantilla `.abap` comentada; sin scripts ni llamadas de red. Se solapa con `sap-abap:rap` y `anthropic-skills:abap-rap-senior`; aporta un checklist corto de errores comunes (projection fina, `IN LOCAL MODE`, `strict ( 2 )`, draft desde el inicio, ETag/lock master). Sus ejemplos usan nombres genéricos (`ZI_Travel`, `ZBP_Travel`): aplicar `standards/naming-conventions.md`.
- **`clean-abap-guide`**: solo markdown; resumen de la guía Clean ABAP. Desaconseja prefijos húngaros salvo que el código existente los estandarice; en este lab manda `standards/naming-conventions.md` (prefijos aceptados por compatibilidad, un estilo por clase).
- **No instalada — `abap-offstack-aunit`** (Alok Mehta, `alokm3hta-star/abap-offstack-testing` @ `a6f79c809f3a`): SkillSpector en rojo en el catálogo. Revisión local: su `run.mjs` ejecuta `git clone` de `open-abap/open-abap-core` en tiempo de ejecución (commit fijado) y depende de paquetes npm de `@abaplint` (versiones fijadas, lockfile solo con `registry.npmjs.org`, sin scripts de instalación). No se encontró nada malicioso, pero exige Node 22, fuentes serializadas por abapGit con `.xml` y GitHub Actions, y este lab aún tiene `src/` sin metadatos XML ni CI. Queda como candidata en `learning/backlog.md`.

## Actualizar

Volver a revisar el diff del repositorio de origen antes de copiar una versión nueva y actualizar la tabla con el commit revisado.
