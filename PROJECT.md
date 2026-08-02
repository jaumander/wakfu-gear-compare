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

## EN CURSO: Página web de comparación (sustituye el flujo de terminal)

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
2/2 — Pulido de uso real: quitar/editar candidatos ya añadidos, guardar la última búsqueda
      en el propio navegador, instrucciones de uso en el README (incluye cómo publicarlo
      con GitHub Pages para el móvil).

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

## Pendiente / decisiones abiertas
- Confirmar la tabla completa de valores de `rareza` (se han visto 1-4 en items de nivel
  bajo; falta mapear qué número corresponde a legendario/mítico/recuerdo, para poder
  filtrar por rareza además de por reliquia/épico).
- Nombres de estadística sin unificar del todo: "PdV" y "Punto de vida" son la misma stat
  (Vida) pero Ankama los describe con dos textos distintos en su JSON; de momento quedan
  como dos claves separadas. También queda un cajón "Stat desconocida" (otras descripciones
  rotas en el propio JSON de Ankama distintas a las ya arregladas, no arreglable desde aquí
  sin más ejemplos reales) y una etiqueta suelta en francés. Ninguno de los dos bloquea el
  uso normal de la herramienta.
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
