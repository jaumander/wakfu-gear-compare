## En curso: armas a dos manos ocupan también la mano izquierda (evitar combos imposibles)
- Milestone actual: investigación (aún no hay milestones numerados, es un fix pequeño y
  aislado, no una feature grande — no hace falta ALCANCE en PROJECT.md para esto).
- Qué está hecho: se subió `diagnose_weapons2.py` (raíz del repo), que vuelca el JSON
  crudo de TODOS los itemTypes que pueden ir en mano derecha o izquierda (equipos con
  `FIRST_WEAPON`/`SECOND_WEAPON` en `equipmentPositions`). El objetivo es localizar el
  campo real de Ankama que marca "esta arma ocupa las 2 manos" (varas, arcos... vs
  espadas, dagas de 1 mano), para luego:
    1. Guardar ese flag en `items_reduced.json` (nuevo campo, ej. `"dos_manos": true/false`)
       en `build_dataset.py`.
    2. En `index.html`, impedir añadir un candidato al slot "Mano izq." si el slot
       "Mano derecha" tiene un arma de 2 manos activa (y viceversa: si se añade una de
       2 manos a mano derecha, vaciar/bloquear mano izq., con aviso al usuario).
- Qué falta: **el usuario aún no ha pegado la salida de `diagnose_weapons2.py`** — su
  primer intento fue en la carpeta equivocada (un ZIP descargado en
  `Downloads\wakfu-gear-compare-main`, sin `.git`, que no tiene el script porque no está
  clonado con git). Hay que decirle que vuelva a `C:\Users\user\wakfu-gear-compare` (la
  carpeta que sí clonó con git al principio del proyecto) y allí:
  ```
  git pull
  python diagnose_weapons2.py
  ```
  y pegar la salida completa (o al menos 2-3 tipos de arma de 2 manos conocidos como
  "Vara"/"Arco" y 2-3 de 1 mano como "Espada"/"Daga", para comparar el JSON).
- Archivos tocados en este milestone: `diagnose_weapons2.py` (nuevo, ya commiteado y
  pusheado). `build_dataset.py` e `index.html` TODAVÍA NO se han tocado — no asumir
  ningún campo ni implementar nada hasta ver el JSON real.
- Último commit: "WIP: diagnose_weapons2 - dump crudo de itemTypes de armas para
  localizar el campo de 2 manos" (ya en `main`).
- Duda pendiente de confirmar con el usuario: ninguna decisión de producto tomada
  todavía sobre CÓMO debe comportarse la UI exactamente al chocar 2 manos (¿vaciar el
  otro slot automáticamente con aviso? ¿impedir añadir directamente con un mensaje?) —
  decidir con el usuario una vez se sepa el campo real y se pueda implementar.

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
