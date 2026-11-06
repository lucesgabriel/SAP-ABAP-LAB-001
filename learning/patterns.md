# Patrones ABAP aprobados

Desde 2026-10-01 los patrones completos viven en [`knowledge-base/solution-patterns.md`](../knowledge-base/solution-patterns.md) con código `P-NNN`, tags y evidencia. Este archivo queda como índice corto.

| Código | Patrón | Origen |
| --- | --- | --- |
| `P-001` | Report ALV clásico → clase ABAP Cloud con CDS liberadas | `projects/abap-001-equipos-cloud` |
| `P-002` | Flujo de cambio seguro con ARC-1: `contexto → lectura → diff mínimo → lint/sintaxis → escritura → activación → pruebas/ATC → lectura posterior` | Reglas del laboratorio |
| `P-003` | Orden de activación RAP: TABL → DDLS → DCLS → BDEF → behavior pool → SRVD → SRVB | Reglas del laboratorio (pendiente de validar en un proyecto `rap-NNN`) |
| `P-004` | Diagnóstico CSRF en OData: comparar `SAP_SESSIONID` antes que el token | `scripts/diag-csrf.ps1`, colección Bruno |
| `P-005` | ATC antes/después como evidencia de migración clean core | `projects/abap-001-equipos-cloud` |

Reglas cortas que siguen vigentes y están codificadas como decisiones:

- Preferir edición de método sobre reemplazo completo de clase (`D-009`).
- Semántica de moneda/unidad en campos CURR/QUAN (`D-010`).
- Consultas con columnas y filas mínimas (`D-011`).
- Preferir APIs liberadas y contratos C0–C4 adecuados, comprobando `API_STATE` (`D-008`, `R-007`).
- `$TMP` para experimentos; `Z*`/`Y*` con transporte verificado para activos durables (`D-007`).

No guardar propuestas como patrones aprobados: un patrón nuevo se redacta en `solution-patterns.md` al cierre de un proyecto, con activación, prueba y lectura posterior demostradas.
