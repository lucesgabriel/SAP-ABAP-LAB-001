# Case ID: `{{CASE_ID}}` — {{TITLE}}

> Caso de práctica generado por el SAP ABAP LAB 001. Empresa, datos y nombres son ficticios (Globex, Acme, Initech...). Para uso de entrenamiento en el sistema de laboratorio.

## 1. Metadata

| Campo | Valor |
|---|---|
| Nivel | {{LEVEL}} |
| Tiempo sugerido | {{TIME_MIN}} min |
| Dominio | {{DOMAIN}} ({{DOMAIN_NAME}}) |
| Capability KB | `{{CAPABILITY}}` |
| Paquete sugerido | `{{PACKAGE}}` (verificar en SAP antes de crear objetos; `$TMP` si es desechable) |
| Sistema | Ver `config/system.yaml` |

## 2. Contexto empresarial

Pendiente: describe el escenario ficticio (empresa, área, problema de negocio). Si practicas un patrón visto en un cliente real, ofusca nombres, montos y datos.

## 3. Objetivo técnico

Pendiente: qué objeto(s) ABAP se deben crear o modificar y qué deben hacer.

## 4. Requerimiento exacto

1. Pendiente.
2. Pendiente.
3. Pendiente.

## 5. Nombres obligatorios de objetos

> Cualquier desviación resta puntos. Seguir `standards/naming-conventions.md`.

| Tipo | Nombre exacto | Paquete |
|---|---|---|
| CLAS / DDLS / BDEF / SRVD / SRVB / TABL / PROG | Pendiente | `{{PACKAGE}}` |

## 6. Datos entregados

| Item | Valor |
|---|---|
| Tablas / vistas origen | Pendiente (comprobar `API_STATE` con `R-007`) |
| Datos sintéticos de prueba | Pendiente |
| Usuario / autorizaciones | Placeholder `<TU_USUARIO>`; nunca credenciales reales |

## 7. Entrada esperada

```text
Pendiente (criterios de selección, payload OData, parámetros de método...)
```

## 8. Salida esperada

```text
Pendiente (estructura de la tabla de resultado, respuesta OData, consola ADT...)
```

## 9. Precondiciones

- Conexión ARC-1 verificada con una lectura no destructiva (`TOOL-003`).
- Pendiente.

## 10. Pasos esperados

1. `SAPContext` → `SAPSearch`/`SAPRead` del contexto.
2. Diseño en `docs/design.md` citando el KB.
3. Pendiente (escritura, activación, pruebas).

## 11. Diseño esperado (sin revelar la solución)

Pendiente: capas, objetos, orden de activación, APIs liberadas a usar.

## 12. Validaciones

- `SAPDiagnose action=syntax` limpio en la versión inactiva.
- `SAPActivate` correcto e `INACTIVE_OBJECTS` vacío.
- ATC con la variante indicada: pendiente.
- ABAP Unit: pendiente.
- Lectura posterior coincide con `src/`.

## 13. Criterios de éxito (rúbrica)

| Criterio | Peso | Resultado |
|---|---|---|
| Nombres exactos y paquete | {{W_NAMES}}% | ☐ |
| Funcionalidad correcta (activa, ejecuta, resultado esperado) | {{W_FUNC}}% | ☐ |
| Calidad: Clean ABAP, ATC, clean core | {{W_QUALITY}}% | ☐ |
| Pruebas: ABAP Unit / test doubles | {{W_TEST}}% | ☐ |
| Seguridad y datos (autorizaciones, consultas mínimas, sin secretos) | {{W_SEC}}% | ☐ |
| Evidencia y logs con taxonomía | {{W_EVID}}% | ☐ |
| **TOTAL** | **100%** | **__%** |

Umbrales: APROBADO ≥ 70%, OBSERVACIONES 60–69%, REPROBADO < 60%.

## 14. Checklist 100%

Ver `rubric/checklist-100.md`.

## 15. Errores comunes esperados

Ver `00-case-brief/historical-context.md` (filtrado por capability). Añade aquí los específicos del caso.

## 16. Hints progresivos (penalización −5% cada uno)

<details>
<summary>Hint 1 (−5%)</summary>
Pendiente.
</details>

<details>
<summary>Hint 2 (−10%)</summary>
Pendiente.
</details>

<details>
<summary>Hint 3 (−15%)</summary>
Pendiente.
</details>

## 17. Solución esperada

Oculta en `solution/expected-solution.md`. **No abrir hasta marcar `Resuelto: Si` en el README del caso.**

## 18. Variantes

- **A (básico):** pendiente.
- **B (intermedio):** pendiente.
- **C (avanzado):** pendiente.
