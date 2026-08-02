## En curso: armas a dos manos ocupan también la mano izquierda (evitar combos imposibles)
- Milestone actual: implementación hecha en `index.html`/`build_dataset.py`, pendiente
  regenerar `items_reduced.json` con el nuevo campo (necesita red del usuario).
- Qué está hecho:
  - Campo real confirmado con datos reales pegados por el usuario (salida de
    `diagnose_weapons2.py`): una arma de mano derecha ocupa las 2 manos si su
    `equipmentDisabledPositions` incluye `"SECOND_WEAPON"` (Hacha, Pala, Martillo, Arco,
    Espada/Bastón "Dos manos" lo tienen; Varita, Espada/Bastón "Una mano", Aguja, Carta,
    Daga, Escudo lo tienen vacío).
  - `build_dataset.py`: nueva función `build_two_handed_set()` + campo `"es_dos_manos"`
    en cada objeto de `items_reduced.json`. Validado con un test unitario contra el JSON
    real de las 11 armas que pegó el usuario (6 de 2 manos detectadas correctamente).
  - `index.html`: decisión de UX confirmada con el usuario — quiere poder comparar en la
    misma tabla "arma de 2 manos sola" vs "1 mano + objeto en la izquierda". Se
    implementó emparejando Mano derecha/Mano izq. en el motor de combinaciones: si el
    candidato de la derecha es de 2 manos, se genera UNA combinación con la izquierda
    "libre" (objeto placeholder `MANO_LIBRE`, stats vacíos) en vez de multiplicar por
    cada candidato de esa mano. El placeholder se excluye del contador de "piezas" y del
    rango de nivel de la ficha (`es_hueco: true`). Probado con test en Node: 2 candidatos
    en cada mano (1 normal + 1 de 2 manos reliquia) → 3 combinaciones crudas (no 4), todas
    válidas, tal como se esperaba.
- Qué falta:
  1. El usuario tiene que regenerar `items_reduced.json` corriendo `python build_dataset.py`
     en su máquina (con red a `wakfu.cdn.ankama.com`) para que el dataset real tenga el
     campo `es_dos_manos` — sin eso, `index.html` no puede detectar armas de 2 manos
     todavía en el dataset publicado (el código ya está listo, solo falta el dato).
  2. Una vez regenerado, commit+push de `items_reduced.json` y probar en el navegador con
     un caso real (una espada de 2 manos + un escudo/daga en la izquierda).
- Archivos tocados en este milestone: `build_dataset.py`, `index.html`, `HANDOFF.md`.
- Último commit: pendiente de este mismo cierre de sesión.
- Sin dudas pendientes de confirmar con el usuario en este milestone (la duda de UX ya
  se resolvió).

<!--
Plantilla para cuando quede trabajo a medias:

## En curso: <nombre de la feature/milestone>
- Milestone actual: X/Y
- Qué está hecho: ...
- Qué falta: ...
- Archivos tocados en este milestone: ...
- Último commit: <hash o mensaje>
- Cualquier decisión o duda pendiente de confirmar con el usuario: ...
-->
