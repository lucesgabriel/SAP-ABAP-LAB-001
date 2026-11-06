# Aprendizaje continuo

Empieza con la [ruta sugerida](roadmap.md). El aprendizaje se demuestra con ejercicios y evidencia; completar una lectura o crear una carpeta no acredita dominio.

Desde 2026-10-01 el conocimiento **codificado y filtrable** vive en [`knowledge-base/`](../knowledge-base/README.md) (errores `<CAP>-NNN`, patrones `P-NNN`, decisiones `D-NNN`, recetas `R-NNN`) y se alimenta cerrando proyectos y casos con `close_project.py`. Esta carpeta conserva la **narrativa** y la ruta de estudio personal.

| Lugar | Qué registrar |
| --- | --- |
| [exercises/](exercises/README.md) | Objetivos de práctica, criterios y enlaces al proyecto o caso que los implementa. |
| [sessions/](sessions/README.md) | Lo observado en una sesión, dudas y siguiente paso. |
| [templates/](templates/README.md) | Formatos para ejercicios y sesiones. |
| [lessons.md](lessons.md) | Lecciones narrativas comprobadas, con evidencia y enlace a su código KB. |
| [decisions.md](decisions.md) | ADR de gobernanza del laboratorio (espejo técnico en `decision-registry.md`). |
| [patterns.md](patterns.md) | Índice corto; los patrones completos están en `solution-patterns.md`. |
| [backlog.md](backlog.md) | Deuda y mejoras globales. |

## Ciclo

Elige una habilidad → genera un caso (`cases/`) o un proyecto → lee el histórico del KB → trabaja → verifica → registra errores y decisiones con taxonomía → cierra con `close_project.py` → el KB crece → el siguiente ejercicio hereda lo aprendido.

Mantén el código en `projects/<id>/src/` o `cases/<id>/src/` y enlázalo desde el ejercicio, sin copiarlo. Antes de añadir una lección narrativa, busca si el KB ya tiene el código; enlázalo en lugar de repetirlo. Las hipótesis siguen en sesiones o backlog.
