## Rediseño visual de index.html (Claude Design) — TERMINADO (sesión 2026-08-02)

Rediseño **puramente visual**. La lógica de negocio NO se ha tocado: siguen intactos y
copiados tal cual `isValidCombo()`, `sumStats()`, `foldElementalStats()` (con sus
multiplicadores validados 234 vs 220), `cartesian()`, la carga del dataset desde
raw.githubusercontent.com, y el plegado de dominio/resistencia elemental con desglose.

### Cómo está montada la web ahora

Sigue siendo **un único `index.html` sin build step**. Tres zonas:

1. **Columna izquierda — ficha de personaje.** Stats de la combinación seleccionada,
   agrupadas en bloques plegables. Hay **dos modos** (conmutador arriba):
   - `Personaje`: Principales › Dominios › Combate › Secundario › **Resistencias**
   - `Aptitudes`: Mayor › Agilidad › Suerte › Fuerza › Inteligencia
   Los dos siguen el orden con el que el propio juego describe un objeto. El agrupador
   vive en `MODES` + `groupedStats()`; **lo usan también las tarjetas y el comparador**,
   así que una stat sale siempre en el mismo sitio en toda la interfaz. Cambiar de modo
   reordena las tres zonas a la vez. El bloque final "Otros" es el cajón de sastre para
   que nunca se pierda una stat que no encaje en ningún match.
2. **Ficha de los 12 slots** (Casco, Amuleto, Pechera, Capa, Hombreras, Cinturón, Botas,
   Anillo 1, Anillo 2, Mano dcha., Mano izq., Emblema). Híbrido: ficha real de personaje
   pero **cada slot admite N candidatos** para comparar alternativas. Slot vacío = silueta
   apagada de su tipo. Pulsar un slot lo activa, filtra el buscador a su tipo y muestra
   sus candidatos debajo.
3. **Buscador + resultados + comparador A/B** a dos columnas con la diferencia (B − A) en
   el centro, ordenada y agrupada igual que el resto. Botón "Invertir A/B".

### Iconos — CHECKLIST DEL HANDOFF ANTERIOR, COMPLETADO

Todo verificado contra datos reales o cargando en un navegador. Nada asumido.

1. **Campo del icono CONFIRMADO**: `definition.item.graphicParameters.gfxId`, contra el
   `items.json` real versión 1.92.1.59 (lo ejecutó el usuario en su máquina con
   `inspect_gfx.py`). **No coincide con el `id`** del objeto:
   id 2021 (Amuleto de jalató) → gfxId 1202021 · 2022 → 1032022 · 2023 → 1192023 ·
   2024 → 1322024 · 2025 → 1332025. Existe también `femaleGfxId`, que en los objetos
   comprobados vale lo mismo; no se guarda porque la web no distingue género.
2. **`build_dataset.py` ya lo guarda** como campo `gfx`, e imprime al terminar
   "objetos con gfx (icono): N / M". El usuario regeneró y subió el dataset: **7730/7730**.
3. **La URL oficial de Ankama NO SIRVE**. Probada en navegador con los 5 gfxId reales de
   arriba: `https://s.ankama.com/www/static.ankama.com/wakfu/portal/game/item/115/{gfxId}.png`
   → **fallan los 5**. La ruta documentada en el foro (2020) ya no existe. No volver a
   intentarla sin datos nuevos.
4. **Fuente usada: repo comunitario `Vertylo/wakassets`**, vía GitHub Pages
   (`https://vertylo.github.io/wakassets/{carpeta}/{ID}.png`). Verificado cargando:
   `items/{gfxId}.png` (64×64), `characteristics/*` (46 iconos de stats),
   `rarities/0..7.png`, `itemTypes/*`, `icons/shield.png`, `elements/chromatic.png`.
   Declarado en un comentario grande en la cabecera de `index.html` y en una sección
   propia del README ("Procedencia de los iconos"), como pidió el usuario.
5. **Tabla de equivalencia español → inglés** hecha a mano en `index.html`
   (`STAT_ICON_EXACT` + `STAT_ICON_FUZZY`: primero exacto, luego por fragmento). Los
   totales plegados usan `elements/chromatic.png` (dominio) y `icons/shield.png`
   (resistencia).
6. **Colores de rareza MEDIDOS pixel a pixel** sobre los propios `rarities/0..7.png`, no
   inventados: 0 `#939393` · 1 `#d1d1d1` · 2 `#04d376` · 3 `#f57a21` · 4 `#f1c13a` ·
   5 `#f659d4` · 6 `#77b7d8` · 7 `#e570a2`. Como **sigue sin confirmarse qué NOMBRE tiene
   cada número**, la interfaz no muestra ninguna etiqueta de rareza: solo la gema y el
   color del marco. No inventar nombres.
7. **El `itemTypeId` se deduce del propio `gfx`**, sin campo extra: verificado sobre los
   7730 objetos que el gfx es siempre "3 dígitos de itemTypeId" + el id del gráfico
   (1205368 → tipo 120 = amuleto). Ojo: ese id del gráfico **no** es el id del objeto,
   porque los objetos reskineados reusan el gráfico de otro (4669 de 7730 casos) — por eso
   se lee el prefijo, nunca se resta el id. `build_dataset.py` guarda además `tipo_id`
   explícito, pero la web ya no lo necesita.

### Decisiones de producto tomadas en esta sesión (no deshacer sin preguntar)

- **Tope de 250 combinaciones** (`MAX_COMBOS`). Por encima no se calcula nada y se avisa
  antes, porque el producto cartesiano cuelga la pestaña (7 slots × 3 candidatos = 2187 y
  el navegador se muere — pasó de verdad en esta sesión). Hay un contador en vivo junto al
  botón que se pone en rojo al pasarse. Solo se pintan las 40 mejores (`MAX_CARDS`).
  La herramienta está pensada para duelos cortos (1 único + 1 normal contra otra pareja),
  **no** para optimizar un build de 12 slots.
- **No hay etiqueta "Mejor"**. Se quitó a petición del usuario: era el máximo de un stat
  arbitrario, no una recomendación con criterio (y encima elegía combinaciones sin ningún
  objeto único). El desplegable de orden sigue, porque ahí lo elige el usuario.
- **Dominio elemental**: el total es el padre y **cada objeto va desglosado dentro**, con
  su multiplicador siempre visible (`147 ×3 → 441`), no solo en el tooltip. Se llegó aquí
  tras varias iteraciones; el usuario probó la versión inversa (objetos primero, total al
  final) y la descartó. Las **resistencias NO llevan reparto por objeto** — ahí el ×4
  siempre se aprovecha, así que se dejan con el desglose por línea de stat.
  El desglose muestra lo que **aporta** cada línea (valor × nº de elementos), no el valor
  en bruto: si no, los hijos no suman el padre y parece que el total cuente cosas de más.
- **Buscador con dos vistas** (como Stratfu): `Compacto` (por defecto; solo icono con marco
  de rareza, nombre y nivel — **ninguna stat**) y `Detallado` (todas las stats del objeto).
  En Detallado el **tooltip de hover está desactivado** a propósito: repetiría lo que ya se
  ve. En Compacto sí funciona.
- Búsqueda **sin acentos y por palabras sueltas**: "amuleto dragon" encuentra "Amuleto del
  dragón" (`norm()` + `it._n` precalculado al cargar).
- No se puede añadir el mismo objeto dos veces al mismo slot (el `+` pasa a `✓`).

### Qué falta / ideas que el usuario dejó abiertas

- **Selector de "elementos que usa mi build" (2/3/4)**: el usuario comentó que un objeto
  con `×4` infla un total que la mayoría de builds no aprovecha (casi todas las clases usan
  2-3 elementos). Se le propuso recalcular el total contando solo los elementos elegidos.
  **No implementado, pendiente de que él lo pida.** Zenith y Stratfu tienen algo así
  ("Nb éléments 1 2 3 4").
- **"Poids" de Stratfu**: al usuario le llamó la atención esa métrica pero no se sabe cómo
  la calculan y él mismo dudaba de su utilidad. No implementado, decisión aplazada.
- El milestone 2/2 original de la web (guardar la última búsqueda en localStorage) sigue
  **sin hacer, y el usuario dijo que no le importa**: quiere la herramienta como
  acompañante de un builder de verdad, no como builder.
- Sin confirmar todavía: qué nombre tiene cada número de rareza (ver punto 6 de arriba).

### Cosas del entorno que conviene saber

- **GitHub Pages ya está activado**: https://jaumander.github.io/wakfu-gear-compare/
  Sirve `index.html` de la raíz de `main`.
- `INSTRUCCIONES_PROYECTO.md` tiene el token en texto plano. **Se recomendó al usuario
  rotarlo** (aviso dado dos veces, no lo ha hecho).
- La CDN de Ankama (`wakfu.cdn.ankama.com`) **no se puede leer desde un navegador** (CORS).
  Cualquier cosa que necesite el JSON crudo de Ankama tiene que ejecutarla el usuario en su
  máquina con Python. Los datos que ya están en `items_reduced.json` sí se pueden leer.
- Los commits de esta sesión van todos con prefijo `WIP:`, uno por cambio.

## En cola (sin empezar): milestone 2/2 original de la web
- Guardar la última búsqueda en localStorage (el usuario dijo que no le interesa).
- Instrucciones en el README de cómo publicarlo con GitHub Pages (ya está publicado, falta
  documentarlo).

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
