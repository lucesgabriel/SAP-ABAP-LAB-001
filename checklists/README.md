# Checklists (Quality Gates)

Gates transversales que se ejecutan antes de construir, antes de verificar y antes de cerrar. Se copian al proyecto solo si se quiere dejar constancia; si no, se referencian desde `evidence/completion.md`.

| Checklist | Cuándo |
|---|---|
| [abap-quality-gate.md](abap-quality-gate.md) | Todo proyecto o caso: KB, diseño, build, test, cierre. |
| [rap-release-gate.md](rap-release-gate.md) | Antes de publicar un service binding o dar por terminado un BO RAP. |
| [clean-core-gate.md](clean-core-gate.md) | Cuando el objetivo es cloud readiness o reducir nivel clean core. |

Un ítem sin marcar no bloquea por sí solo; bloquea no tener registrado por qué no se marcó.
