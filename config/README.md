# Configuración

[system.yaml](system.yaml) es la fuente de verdad local para identidad y capacidades no secretas. Contrasta cualquier dato operativo con una lectura actual de SAP; [CONTEXT.txt](../CONTEXT.txt) es inventario legado.

No guardar usuarios/contraseñas operativos, tokens, cookies ni claves aquí. La autenticación sigue en el almacén privado configurado para ARC-1. Esta reorganización no cambia la conexión ni las capacidades del sistema.
