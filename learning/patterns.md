# Patrones ABAP aprobados

## Flujo de cambio seguro
`contexto → lectura → diff mínimo → lint/sintaxis → escritura → activación → pruebas/ATC → lectura posterior`

## Clases
- Preferir edición de método sobre reemplazo completo de clase.
- Añadir ABAP Unit en el include de test cuando la lógica lo permita.
- Activar y volver a leer la versión activa.

## RAP
- Orden de dependencias: TABL → DDLS → DCLS → BDEF → behavior pool → SRVD → SRVB.
- Para objetos interdependientes usar escritura por lotes y activación terminal/batch.
- Ejecutar revisión Clean Core y ATC antes de publicar servicios.

## CDS y datos
- Definir semántica de moneda/unidad para campos CURR/QUAN.
- En consultas seleccionar columnas y filas mínimas.
- Preferir APIs liberadas y contratos C0–C4 adecuados.

## Transportes
- `$TMP` para experimentos desechables.
- Paquetes `Z*`/`Y*` para activos durables.
- Consultar capa/target y transporte; no inventar IDs.
