# {{CASE_ID}} — {{TITLE}}

> Caso de práctica del SAP ABAP LAB 001. ID único, aislado por carpeta, mismo loop de auto-mejora que un proyecto.

## Metadata

| Campo | Valor |
|---|---|
| **Case ID** | `{{CASE_ID}}` |
| **Título** | {{TITLE}} |
| **Dominio** | {{DOMAIN}} ({{DOMAIN_NAME}}) |
| **Capability KB** | `{{CAPABILITY}}` |
| **Nivel** | {{LEVEL}} |
| **Tiempo sugerido** | {{TIME_MIN}} min |
| **Paquete sugerido** | `{{PACKAGE}}` |
| **Generado** | {{DATE}} |
| **Generado por** | `scripts/workspace/new_case.py` |

## Estado

- Brief: generado (completar `00-case-brief/case-brief.md`)
- Histórico consultado: ver `00-case-brief/historical-context.md`
- Build: pendiente
- Verificación (lint / sintaxis / activación / Unit / ATC / lectura): pendiente
- Solución revelada: NO (hasta marcar `Resuelto: Si`)
- Resuelto: No
- Listo para consolidar: No

## Uso con un agente

```text
Usa el workspace SAP ABAP LAB 001.
Resuelve el caso de práctica cases/{{CASE_ID}}-{{SLUG}}.
Lee 00-case-brief/case-brief.md y 00-case-brief/historical-context.md.
NO mires solution/expected-solution.md hasta entregar evidencia o marcar `Resuelto: Si` aquí.
Antes de diseñar, consulta knowledge-base/ y cita los códigos en docs/design.md.
Construye con ARC-1 siguiendo el flujo obligatorio de AGENTS.md (P-002).
```

## Estructura de la carpeta

| Path | Contenido |
|---|---|
| `metadata.json` | Fuente de verdad del estado del caso. |
| `00-case-brief/case-brief.md` | Enunciado completo: contexto, requerimiento, nombres obligatorios, rúbrica, hints. |
| `00-case-brief/historical-context.md` | KB consultado: `P-XXX`, errores conocidos, `D-XXX`, `R-XXX`, casos similares. |
| `docs/design.md` | Diseño citando códigos del KB. |
| `docs/error-log.md`, `docs/decision-log.md` | Logs con taxonomía; se promueven al cierre. |
| `src/` | Código propuesto o leído de SAP (copia; SAP es la fuente). |
| `rubric/checklist-100.md` | Criterios y pesos para autoevaluarse. |
| `solution/expected-solution.md` | OCULTO hasta marcar `Resuelto: Si`. |
| `evidence/` | Resúmenes sanitizados de lint, activación, ATC, Unit, consola. |

## Cuando termines el caso

1. Completa `evidence/completion.md` con evidencia real.
2. Completa `docs/error-log.md` y `docs/decision-log.md` con taxonomía.
3. Marca `Resuelto: Si` y `Listo para consolidar: Si` arriba y en `metadata.json` (`resolved`, `ready_to_consolidate`).
4. Recién entonces abre `solution/expected-solution.md` y compara.
5. Cierra:

```bash
python scripts/workspace/close_project.py --project cases/{{CASE_ID}}-{{SLUG}} --dry-run
python scripts/workspace/close_project.py --project cases/{{CASE_ID}}-{{SLUG}}
```

Los aprendizajes reutilizables se promueven al `knowledge-base/` con códigos secuenciales, igual que un proyecto.
