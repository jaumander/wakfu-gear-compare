## En curso: Rediseño visual de index.html (Claude Design)
- Milestone actual: 1/2 hecho (rediseño completo), 2/2 pendiente (icono real de objeto = gfxId)
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
  - Buscador en tarjetas: icono con marco del color de la rareza, gema de rareza,
    nivel, slot y los 4 stats más grandes del objeto con su icono del juego.
  - Comparador A/B rehecho **a dos columnas con la diferencia en el centro** (tipo
    Stratfu): columna A morada, columna B verde, columna central con la delta B − A
    ordenada por magnitud, en verde/rojo.
  - Iconos de estadística reales del juego en toda la interfaz (adiós emojis).
- Iconos — CHECKLIST DE LA SESIÓN ANTERIOR, RESULTADO REAL (todo verificado en vivo,
  nada asumido):
  1. **No se pudo** confirmar el campo `gfxId` contra el `items.json` real: este entorno
     tampoco tiene salida de red hacia `wakfu.cdn.ankama.com`. Sigue pendiente.
  2. Por lo mismo, `build_dataset.py` NO se ha tocado (además el usuario pidió
     explícitamente "solo visual, cero cambios de lógica" en esta sesión).
  3. La URL oficial
     `https://s.ankama.com/www/static.ankama.com/wakfu/portal/game/item/115/{gfxId}.png`
     se probó en el navegador y **no cargó**. No sirve como fuente ahora mismo.
  4. **Se usa wakassets como fuente**, vía GitHub Pages
     (`https://vertylo.github.io/wakassets/{carpeta}/{ID}.png`). Probado y **cargando
     correctamente**: `characteristics/*` (46 iconos de stats), `rarities/0..7.png`,
     `icons/shield.png`, `elements/chromatic.png` y `items/1010245.png`. Queda declarado
     en un comentario grande en la cabecera de `index.html` y en una sección propia del
     README ("Procedencia de los iconos").
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
- Qué falta (milestone 2/2 del rediseño):
  - Confirmar el nombre real del campo `gfxId` en el `items.json` de Ankama (hace falta
    una máquina con red hacia wakfu.cdn.ankama.com — la del usuario sirve).
  - Añadirlo a `build_dataset.py`, regenerar y subir `items_reduced.json`.
  - No hará falta tocar `index.html`: `itemIconUrl()` ya lee `it.gfx ?? it.gfxId ?? it.gfx_id`
    y, en cuanto exista, sustituye sola el placeholder (marco de rareza + inicial) por el
    icono real de `wakassets/items/{gfxId}.png`.
- Archivos tocados: `index.html` (reescrito visualmente), `README.md` (sección de
  procedencia de iconos).
- Último commit: pendiente de subir por el usuario (el entorno de diseño no tiene push
  al repo; los archivos se entregan para commitear con prefijo "WIP:").
- Duda pendiente de confirmar con el usuario: ninguna del rediseño. La única dependencia
  externa es el gfxId (punto de arriba).

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
