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

## Pendiente / decisiones abiertas
- Confirmar la tabla completa de valores de `rareza` (se han visto 1-4 en items de nivel
  bajo; falta mapear qué número corresponde a legendario/mítico/recuerdo, para poder
  filtrar por rareza además de por reliquia/épico).
- Nombres de estadística sin unificar del todo: "PdV" y "Punto de vida" son la misma stat
  (Vida) pero Ankama los describe con dos textos distintos en su JSON; de momento quedan
  como dos claves separadas. También queda un cajón "Stat desconocida" (descripciones rotas
  en el propio JSON de Ankama, no arreglable desde aquí) y una etiqueta suelta en francés.
  Ninguno de los dos bloquea el uso normal de la herramienta.
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
