# Wakfu Gear Compare — Estado del proyecto

## Qué hace
Descarga los datos oficiales de Wakfu (publicados por Ankama) y compara combinaciones de
equipo, descartando automáticamente las que violan la regla de "máx. 1 reliquia y máx. 1
épico equipados a la vez".

## Hecho
- `build_dataset.py`: descarga items.json / itemTypes.json / itemProperties.json /
  actions.json de la versión actual del juego y genera `items_reduced.json` con los
  objetos equipables de los 12 slots (casco, amuleto, pechera, anillos, botas, capa,
  hombreras, cinturón, mano izq/der, emblema), cada uno con nombre, slot, nivel, rareza
  (número, ver pendientes), flags es_reliquia/es_epico, y stats resueltas a nombre legible.
- `compare.py`: búsqueda de items por nombre/ID + motor de combinatoria (`compare()`) que
  genera el producto cartesiano de candidatos por slot y descarta las combinaciones
  inválidas.
- Validado con un dataset sintético de 4 items (2 amuletos, 2 pares de botas, con 1
  reliquia en cada slot) que reproduce el caso real del usuario: de 4 combinaciones
  posibles, detecta y descarta correctamente la única inválida (2 reliquias a la vez).

## HECHO: Página web de comparación (sustituye el flujo de terminal)

**Motivación:** el usuario quiere usarlo junto a Zenith/Wakforge en el navegador. Stratfu ya
hace algo parecido pero solo compara 2 objetos a la vez y está en francés; esta herramienta
compara N candidatos por slot (2, 4, o más) a la vez, respetando la regla de reliquia/épico,
y en español.

**Alcance — qué toca:**
- Un único archivo `index.html` (HTML+CSS+JS, sin frameworks, sin paso de build) que:
  - Descarga `items_reduced.json` directamente desde GitHub (raw.githubusercontent.com) al
    abrirse, así siempre usa el dataset más reciente sin tener que tocar el archivo.
  - Permite buscar objetos por nombre (y filtrar por slot).
  - Permite añadir 2+ candidatos a "cubos" (el usuario los nombra, ej. "Amuleto",
    "Anillo 1", "Anillo 2"...).
  - Calcula todas las combinaciones válidas (máx. 1 reliquia, máx. 1 épico) y las muestra
    ordenadas por la estadística que el usuario elija.
  - Funciona abriendo el archivo directamente con doble clic (sin instalar nada); también
    se puede publicar con GitHub Pages para usarlo desde el móvil con una URL.

**Qué NO toca (para no romper nada existente):**
- No modifica `build_dataset.py` ni `compare.py` (siguen funcionando igual para quien
  prefiera la terminal).
- No añade backend ni build step (Node, npm, etc.) — todo vive en un solo archivo HTML.
- No implementa aún la optimización de las 12 piezas a la vez (eso sigue siendo v2,
  sin tocar en esta feature).

**Milestones:**
1/2 — Página funcional: búsqueda, cubos de candidatos, cálculo de combinaciones válidas,
      tabla de resultados ordenable. Validado comparando su resultado con `compare.py`
      sobre los mismos IDs.
2/2 — Pulido de uso real: quitar/editar candidatos ya añadidos (HECHO), guardar la última
      búsqueda en el navegador (el usuario dijo que NO le interesa: quiere la herramienta
      como acompañante de un builder, no como builder), instrucciones en el README de cómo
      publicarlo con GitHub Pages (ya está publicado en
      https://jaumander.github.io/wakfu-gear-compare/ , falta documentarlo).

## Hecho (sesión 2026-08-02)
- `items_reduced.json` ya tiene el dataset REAL del juego (versión 1.92.1.59, 7730 objetos
  equipables), generado por el usuario en su máquina con `build_dataset.py`. Ya no es el
  dataset sintético de 4 items.
- Arreglado bug en `clean_stat_label()` (build_dataset.py): los placeholders de Ankama tipo
  `[#charac AP]` no se quitaban porque la regex antigua solo esperaba dígitos entre
  corchetes, no letras. Ahora se quita cualquier contenido entre corchetes. Se validó
  reprocesando el dataset real: bajó de 58 nombres de estadística "sucios" a 37 limpios
  (ej. antes "[#charac AP]  PA" y "[#charac AP] - PA máx." salían como texto crudo, ahora
  "PA" y "PA máx.").
- Arreglado el "Stat desconocida" del Dominio/Resistencia elemental: Ankama tiene 2 sabores
  de estos stats (confirmado con JSON crudo real pegado por el usuario, actionId 1068/1069
  = "en N elementos" con el nº en `params[2]`, y actionId 80/120 = aplica siempre a los 4
  elementos, sin nº) pero el texto oficial para 1068/1069 viene roto, así que ahora se
  fijan a mano en `build_dataset.py` como "Dominio/Resistencia elemental (N elementos)" o
  "(todos)". La web (`index.html`) además calcula un "Resistencia/Dominio elemental total"
  combinando específicas (×1) + "todos" (×4) + "N elementos" (×N) — validado dando 234 vs
  220 en el caso de prueba real del usuario.
- `items_reduced.json` regenerado y subido por el usuario con este arreglo ya aplicado
  (commit 7daff4d). Verificado: 5716 stats "(N elementos)" y 3059 "(todos)" presentes en
  el dataset publicado — la web ya muestra los nombres correctos sin pasos adicionales.

## Hecho (sesión 2026-08-02, rediseño visual con Claude Design)
Rediseño **puramente visual** de `index.html`; la lógica de negocio no se tocó. Resumen —
el detalle completo, con los datos verificados y las decisiones tomadas, está en HANDOFF.md.
- Interfaz tipo "ficha de personaje" inspirada en Zenith/Wakfuli/Stratfu: columna de stats
  a la izquierda en bloques plegables, ficha de los 12 slots a la derecha (cada slot admite
  N candidatos), y comparador A/B a dos columnas con la diferencia en el centro.
- Iconos reales del juego (stats, rareza, tipo de slot y objeto). **Confirmado** que el
  identificador del icono es `definition.item.graphicParameters.gfxId` (no coincide con el
  `id`); `build_dataset.py` ya lo guarda como `gfx` y el dataset publicado lo trae en
  7730/7730 objetos.
- **La URL oficial de iconos de Ankama ya no funciona** (probada con 5 gfxId reales, fallan
  los 5). Se usa el repo comunitario `Vertylo/wakassets`, declarado en el código y en el
  README por transparencia.
- Las stats se agrupan y ordenan como en el propio juego, con dos modos (Personaje /
  Aptitudes), y el mismo orden se aplica a la ficha, a las tarjetas y al comparador.
- Tope de 250 combinaciones: por encima el navegador se cuelga (comprobado). La herramienta
  es para duelos cortos, no para optimizar un build entero.
- GitHub Pages activado: https://jaumander.github.io/wakfu-gear-compare/

## HECHO: Dominio elemental limitado por nº de elementos de la build

**Motivación:** un objeto que da dominio a los 4 elementos infla el total si la build solo
usa 2 o 3 (la mayoría de clases usan 2-3 elementos), como el "Nb éléments" de Stratfu.

**Alcance — qué toca:**
- Selector en la ficha (2 / 3 / 4 elementos) junto al conmutador Personaje/Aptitudes.
- El cálculo de "Dominio elemental total": por objeto, `multiplicador_usado =
  min(elementos_del_objeto, elementos_de_la_build)`. Si el objeto da a más elementos de
  los que la build usa, se cala el multiplicador y se muestra un aviso (icono + tooltip)
  explicando por qué.

**Qué NO toca:**
- Resistencia elemental sigue igual (siempre ×4 aprovechado, sin tope, según ya se decidió).
- No cambia el motor de combinatoria (`compare()`/`isValidCombo` en compare.py) ni nada de
  terminal — solo el cálculo/visual del dominio en `index.html`.

**Milestones:**
1/2 — HECHO: selector 2/3/4 en la ficha (junto al conmutador de modo) + estado
      `buildElementCount` guardado.
2/2 — HECHO: `foldElementalStats()` y `dominioPorItem()` capan el multiplicador del
      DOMINIO (no la resistencia) con `min(elementos_del_objeto, buildElementCount)`, y
      muestran un icono de aviso (⚠, con tooltip) cuando un objeto se cala. Validado con
      el caso real de la Varita de mago gris (520 en 3 elementos): build=4 y build=3 dan
      1560 (igual que antes), build=2 cala a 1040 y marca el aviso — igual que describió
      el usuario. Al cambiar el selector con resultados ya calculados, se recalcula el
      dominio sin rehacer el cartesiano (`refoldResults()`).

- Arreglado el "Stat desconocida" que quedaba en `build_dataset.py`: actionId 39/40
  (plantilla rota en `actions.json`) resultaban ser "Armadura dada"/"Armadura recibida",
  confirmado con capturas reales del propio juego (no por texto de Ankama, que ahí no
  sirve). ActionId 304 resultó ser el efecto de **pasivas únicas** de texto libre (objetos
  épicos/reliquia con habilidad especial), así que en vez de mostrar un número sin sentido
  se marca como "Pasiva única (ver descripción del objeto)". Dataset real regenerado y
  verificado: 126 objetos con Armadura dada, 89 con Armadura recibida, 80 con Pasiva
  única, **0 objetos con "Stat desconocida" o "accion_XXX" sin resolver** en los 7730
  objetos del dataset.

## HECHO: Armas de 2 manos bloquean la mano izquierda

**Motivación:** algunas armas (Hacha, Pala, Martillo, Arco, Espada/Bastón "Dos manos")
ocupan las dos manos en el juego real; la web dejaba añadir un candidato a "Mano izq."
aunque "Mano derecha" tuviera una de éstas, generando combinaciones imposibles.

**Campo real confirmado** (con JSON pegado por el usuario, salida de
`diagnose_weapons2.py`): una arma de mano derecha es de 2 manos si su
`equipmentDisabledPositions` incluye `"SECOND_WEAPON"`.

**Decisión de UX** (confirmada con el usuario): en vez de bloquear al añadir o vaciar el
otro slot, se quería poder comparar en la misma tabla "arma de 2 manos sola" vs "1 mano +
objeto en la izquierda".

**Implementación:**
- `build_dataset.py`: `build_two_handed_set()` + campo `"es_dos_manos"` en cada objeto.
- `index.html`: Mano derecha/Mano izq. se emparejan en el motor — si el candidato de la
  derecha es de 2 manos, se genera 1 sola combinación con la izquierda "libre" (objeto
  placeholder `MANO_LIBRE`, `es_hueco: true`, excluido del contador de piezas y del rango
  de nivel) en vez de multiplicar por cada candidato de esa mano.
- Validado: test unitario de `build_two_handed_set()` contra las 11 armas reales pegadas
  por el usuario (6 de 2 manos detectadas bien); test del motor en Node (2 candidatos por
  mano → 3 combinaciones crudas en vez de 4, todas válidas); dataset real regenerado por
  el usuario y verificado: **509 armas de 2 manos** de 7730 objetos.

## Hecho: Filtros rápidos en el buscador (los 3 milestones completos)

**Motivación:** el usuario quiere filtrar más rápido sin desplegables: un slider de nivel
de 2 puntos (en vez del dropdown de franjas), iconos de rareza que se pueden apagar/encender
para ocultar rarezas, e iconos de tipo de equipo (a modo de espejo de la selección del grid
de Equipo) justo encima del buscador.

**Alcance — qué toca:**
- Solo `index.html` (HTML + CSS + JS del buscador). No toca `build_dataset.py`, `compare.py`
  ni el motor de combinaciones (`compare()`/cartesian) — los filtros solo afectan a qué
  aparece en la lista de resultados de búsqueda, no a las combinaciones ya calculadas.
- Sustituye el `<select id="level-filter">` por un slider de 2 puntos (min/max) sobre las
  mismas franjas ya definidas en `levelRanges()`.
- Añade una fila de iconos de rareza (0-7, usando `RARITY_COLOR`/`rarityGem`) que actúan
  como "ocultar esta rareza" al pulsarlos (toggle on/off, todas activas por defecto).
- Añade una fila de iconos de tipo de equipo (los 12 `GEAR_SLOTS`) que hacen de atajo para
  `selectSlot()` — mismo comportamiento que pulsar un slot en el grid de Equipo de arriba,
  para no duplicar lógica.

**Qué NO toca:**
- No cambia `doSearch()` en su lógica de tokens/nombre, solo añade condiciones de filtro
  adicionales (rango de nivel del slider, rarezas no ocultas).
- No cambia el motor de combinaciones ni el modal de comparación.
- No es responsive para móvil en esta pasada (se revisa después si hace falta).

**Milestones:**
1/3 — Slider de nivel de 2 puntos sustituyendo el dropdown de franjas. Mismo rango de
      valores exacto (1-245) que ya usa `levelRanges()`, sin franjas fijas: nivel exacto
      arrastrable. Validado contra el filtrado que ya hacía el dropdown.
2/3 — Iconos de rareza (0-7) para ocultar/mostrar por rareza.
3/3 — Iconos de tipo de equipo como atajo de `selectSlot()`, con el icono activo resaltado
      igual que en el grid de Equipo.

**Estado: completo.** Los 3 milestones están implementados y pusheados:
- 1/3 slider de nivel de 2 puntos (sustituye el dropdown de franjas fijas).
- 2/3 iconos de rareza (0-7) para ocultar/mostrar en el buscador, apagados/encendidos
  independientes entre sí.
- 3/3 iconos de tipo de equipo como atajo de `selectSlot()`, resaltado el activo igual
  que en el grid de Equipo (mismo estado `activeSlot`, sin duplicar lógica).
Validado con `node --check` sobre el JS extraído del archivo tras cada milestone (sin
errores de sintaxis); no se ha podido probar en un navegador real dentro de este entorno,
así que conviene que el usuario lo abra una vez y confirme que el slider y los iconos
responden bien al tacto/ratón antes de darlo por cerrado del todo.

**Nota sobre la sesión anterior (2026-08-02):** hubo un intento previo de este mismo
milestone 1/3 que nunca llegó a commitearse (la sesión se cortó a medias sin dejar nada en
git), así que se reimplementó desde cero en esta sesión siguiendo este alcance.

## Pendiente / decisiones abiertas
- **"Poids" de Stratfu**: métrica de valor global de un objeto. No se sabe cómo la calculan
  y el propio usuario duda de su utilidad. Aplazado.
- Tabla de `rareza` con nombres ya en la web (`RARITY_NAMES` en index.html): 0 Común,
  1 Poco Común, 2 Raro, 3 Mítico, 4 Legendario, 5 Reliquia, 6 Recuerdo, 7 Épico.
  **5 y 7 están confirmados** contra el dataset real (coinciden al 100% con los flags
  es_reliquia/es_epico). El resto (0,1,2,3,4,6) sigue el orden oficial de la wiki de
  Wakfu + el conteo real de objetos por valor, pero no está verificado objeto a objeto
  contra el juego — si el usuario ve algún color/nombre que no cuadra, avisar para
  corregirlo.
- Nombres de estadística sin unificar del todo: "PdV" y "Punto de vida" son la misma stat
  (Vida) pero Ankama los describe con dos textos distintos en su JSON; de momento quedan
  como dos claves separadas. No bloquea el uso normal de la herramienta.
- v2 (nice-to-have, sin comprometer ahora): optimización global de las 12 piezas a la vez,
  UI web, soporte de sublimaciones épicas/de reliquia, auto-detección de nueva versión del
  juego.

## Decisiones de diseño
- Fuente de datos: JSON oficial de Ankama (`wakfu.cdn.ankama.com/gamedata`), NO scraping de
  terceros (stratfu/zenith/wakforge/gearfu) — confirmado accesible y con los flags de
  reliquia/épico ya incluidos de fábrica (`properties: [8]` = reliquia, `[12]` = épico).
- Búsqueda de candidatos por nombre (preferido) con soporte también por ID.
- El motor de comparación (`compare()`) es agnóstico a qué llamas cada slot — para anillos,
  usa dos claves distintas (ej. "Anillo 1" / "Anillo 2").
