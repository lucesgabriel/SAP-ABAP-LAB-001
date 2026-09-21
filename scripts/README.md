# Herramientas del laboratorio

Ejecuta los comandos desde la raíz. Las utilidades nuevas de organización requieren Python 3.10+ y solo usan la biblioteca estándar.

| Herramienta | Uso | Alcance |
| --- | --- | --- |
| [workspace/projects.py](workspace/projects.py) | `python scripts/workspace/projects.py create abap-001-tema --title "Título"` o `list` | Genera archivos locales sin sobrescribir; lista metadatos. |
| [workspace/validate_structure.py](workspace/validate_structure.py) | `python scripts/workspace/validate_structure.py` | Comprueba carpetas, plantillas, metadatos y enlaces Markdown locales. |
| [verify_workspace.py](verify_workspace.py) | `python scripts/verify_workspace.py` | Validador existente: inventario, heurística de secretos y configuración de clientes. Requiere PyYAML y clientes configurados. |
| [build_manual_pdf.py](build_manual_pdf.py) | `python scripts/build_manual_pdf.py` | Genera el PDF del manual; requiere ReportLab. |
| [smoke_test_claude_arc1.py](smoke_test_claude_arc1.py) | Consultar el script antes de usar | Prueba existente mediante cliente Claude y ARC-1; requiere entorno configurado. |
| [diag-csrf.ps1](diag-csrf.ps1) | Consultar alcance antes de ejecutar | Diagnóstico existente vinculado a pruebas HTTP; su uso puede afectar SAP según la operación. |

Los scripts existentes mantienen sus rutas. No ejecutes diagnósticos SAP como comprobación de carpetas. Ningún resultado del validador de estructura demuestra conexión SAP, sanitización, sintaxis ABAP, activación, Unit o ATC.

## Verificar las utilidades de organización

```powershell
python -m unittest discover -s scripts/workspace/tests -v
python scripts/workspace/validate_structure.py
```

Las pruebas usan carpetas temporales fuera de los proyectos reales y no llaman a SAP. Los estados `completed`/`archived` son metadatos locales; su evidencia se revisa manualmente según `AGENTS.md`.
