## En curso: Rediseño visual de index.html (Claude Design)
- Milestone actual: 2/2 hecho por nuestra parte. **Falta un paso manual del usuario**:
  ejecutar `python build_dataset.py` y subir el `items_reduced.json` regenerado.
- Qué está hecho:
  - `index.html` rediseñado por completo, **sin tocar la lógica**: siguen intactos y
    copiados tal cual `isValidCombo()`, `sumStats()`, `foldElementalStats()` (con sus
    multiplicadores validados 234 vs 220), `cartesian()`, la carga del dataset desde
    raw.githubusercontent.com y el desglose bajo demanda de los totales elementales.
  - Layout nuevo tipo "ficha de personaje" (inspirado en Zenith/Wakfuli):
    - Columna izquierda: ficha de estadísticas de la combinación seleccionada, en
      **bloques plegables** (Principales / Elemental / Ataque / Defensa / Otros). El
      bloque "Otros" existe como cajón de sastre para que nunca se pierda un stat.
      Los totales elementales siguen siendo clicables y abren el mismo modal de desglose.
    - Columna derecha: **ficha de los 12 slots reales** del personaje (Casco, Amuleto,
      Pechera, Capa, Hombreras, Cinturón, Botas, Anillo 1, Anillo 2, Mano dcha., Mano
      izq., Emblema). Cada slot sigue admitiendo **N candidatos** (híbrido: ficha real +
      comparación de alternativas), con contador en la esquina. Pulsar un slot lo activa,
      filtra el buscador a su tipo y muestra sus candidatos.
    - Los 12 slots usan como `tipo` el valor literal de `slot` que genera
      `POSITION_LABELS` en build_dataset.py; los dos anillos comparten tipo "Anillo".
  - Buscador en tarjetas: icono del objeto con marco del color de la rareza, gema de
    rareza, nivel, slot y los 4 stats más grandes del objeto con su icono del juego.
  - Comparador A/B rehecho **a dos columnas con la diferencia en el centro** (tipo
    Stratfu): columna A morada, columna B verde, columna central con la delta B − A
    ordenada por magnitud, en verde/rojo.
  - Iconos de estadística reales del juego en toda la interfaz (adiós emojis).
  - **`build_dataset.py`: añadido el campo `gfx`** (el identificador del icono).

- Iconos — CHECKLIST COMPLETADO (todo verificado contra datos reales, nada asumido):
  1. **CONFIRMADO** el campo, contra el `items.json` real versión 1.92.1.59 (ejecutado
     por el usuario en su máquina con `inspect_gfx.py`, script de un solo uso que sigue
     en el repo por si hace falta repetirlo tras un parche del juego):
     `definition.item.graphicParameters.gfxId`.
     **No coincide con el `id`** del objeto. Ejemplos reales:
     id 2021 (Amuleto de jalató) → gfxId 1202021 · id 2022 → 1032022 ·
     id 2023 → 1192023 · id 2024 → 1322024 · id 2025 → 1332025.
     Existe también `femaleGfxId`, que en los objetos comprobados vale lo mismo; no se
     guarda porque la web no distingue género.
  2. **HECHO**: `build_dataset.py` guarda ese valor como `gfx` en `items_reduced.json`,
     e imprime al final cuántos objetos lo traen ("objetos con gfx (icono): N / M").
  3. **La URL oficial NO SIRVE**. Probada en navegador con los 5 gfxId reales de arriba:
     `https://s.ankama.com/www/static.ankama.com/wakfu/portal/game/item/115/{gfxId}.png`
     → fallan los 5. La ruta documentada en el foro (2020) ya no existe.
  4. **Se usa wakassets** como fuente, vía GitHub Pages
     (`https://vertylo.github.io/wakassets/{carpeta}/{ID}.png`). Verificado cargando:
     los 5 `items/{gfxId}.png` de arriba (64×64, icono correcto), `characteristics/*`
     (46 iconos de stats), `rarities/0..7.png`, `icons/shield.png` y
     `elements/chromatic.png`. Declarado en un comentario grande en la cabecera de
     `index.html` y en una sección propia del README ("Procedencia de los iconos").
  5. Tabla de equivalencia español -> inglés construida a mano en `index.html`
     (`STAT_ICON_EXACT` + `STAT_ICON_FUZZY`, se comprueba primero exacto y luego por
     fragmento). Los stats elementales plegados sí tienen icono: **`elements/chromatic.png`**
     (icono multicolor de dominio elemental) para "Dominio elemental total" y
     **`icons/shield.png`** para "Resistencia elemental total".
  6. Los **colores de rareza** se han medido pixel a pixel sobre los propios
     `rarities/0..7.png` en vez de inventarlos:
     0 `#939393` · 1 `#d1d1d1` · 2 `#04d376` · 3 `#f57a21` · 4 `#f1c13a` ·
     5 `#f659d4` · 6 `#77b7d8` · 7 `#e570a2`.
     Como sigue sin confirmarse QUÉ nombre tiene cada número, la interfaz **no muestra
     ninguna etiqueta de rareza**: solo la gema y el color del marco.

- Qué falta (paso manual, no se puede hacer desde aquí — la CDN de Ankama bloquea la
  lectura desde navegador por CORS):
  1. El usuario ejecuta `python build_dataset.py` en su máquina.
  2. Sube el `items_reduced.json` regenerado al repo.
  3. Nada más: `index.html` ya lee `it.gfx` y los iconos aparecen solos.
- Archivos tocados: `index.html`, `build_dataset.py`, `README.md`, `inspect_gfx.py` (nuevo).
- Último commit: ver historial, todos con prefijo "WIP:".
- Duda pendiente de confirmar con el usuario: ninguna.

## En cola (sin empezar): Página web de comparación, milestone 2/2 original
- Guardar la última búsqueda en el propio navegador (localStorage).
- Instrucciones en el README de cómo publicarlo con GitHub Pages.
- No se ha hecho en esta sesión porque el usuario pidió "solo visual, cero cambios de
  lógica".

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
