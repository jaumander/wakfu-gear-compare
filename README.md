# Wakfu Gear Compare

Herramienta para comparar combinaciones de equipo de Wakfu respetando la
restricción de "máximo 1 reliquia y máximo 1 épico equipados a la vez".

Usa los datos oficiales que publica Ankama (no scraping de terceros):
`https://wakfu.cdn.ankama.com/gamedata/{version}/{type}.json`

## 1. Generar el dataset (una vez, y cada vez que quieras actualizarlo)

```bash
python build_dataset.py
```

Esto descarga `items.json`, `itemTypes.json`, `itemProperties.json` y
`actions.json` de la versión actual del juego, y genera `items_reduced.json`
con solo los objetos equipables de los 12 slots (casco, amuleto, pechera,
anillos, botas, capa, hombreras, cinturón, mano izq/der, emblema), cada uno
con: nombre, slot, nivel, rareza, si es reliquia/épico, sus stats y el `gfx`
(identificador del icono del objeto).

> Nota: `items.json` pesa 20+MB, la primera descarga puede tardar unos
> segundos. Los archivos se cachean en `data/` para no re-descargarlos si
> vuelves a correr el script con la misma versión del juego.

**Importante:** este script necesita acceso a internet hacia
`wakfu.cdn.ankama.com`. Si lo corres en un entorno con restricciones de red,
ejecútalo desde tu propia máquina.

## 2. Buscar items

```bash
python compare.py --search "amuleto"
python compare.py --search "bota" --slot Botas
```

## 3. Comparar combinaciones

Ver `ejemplo_uso.py`. La idea:

```python
from compare import load_items, find_by_id, compare, print_results

items = load_items()

candidatos = {
    "Amuleto": [find_by_id(items, ID_1), find_by_id(items, ID_2)],
    "Botas":   [find_by_id(items, ID_3), find_by_id(items, ID_4)],
}

resultados = compare(candidatos, sort_by="Vitalidad")  # o el stat que prefieras
print_results(resultados)
```

`compare()` genera todas las combinaciones cruzadas y descarta automáticamente
las que tengan más de 1 reliquia o más de 1 épico. Puedes pasar tantos slots
como quieras (2, 4, hasta los 12), y para los anillos simplemente usa dos
claves distintas (ej. `"Anillo 1"` y `"Anillo 2"`).

## 4. La web (`index.html`)

Un único archivo HTML+CSS+JS, sin paso de build: se abre con doble clic o se
publica con GitHub Pages. Descarga `items_reduced.json` de este mismo repo al
abrirse, así siempre usa el dataset más reciente.

Interfaz tipo "ficha de personaje": columna de estadísticas a la izquierda (en
bloques plegables), ficha de los 12 slots del personaje a la derecha —cada slot
admite N candidatos para comparar—, buscador de objetos, lista de combinaciones
válidas y comparador A/B a dos columnas con la diferencia en el centro.

## Procedencia de los iconos (importante)

Los **iconos de estadística** (PA, PdV, Esquiva, Dominio, Resistencia…), las
**gemas de rareza** y —cuando el dataset traiga el `gfxId`— los **iconos de
objeto** NO vienen de una fuente oficial de Ankama. Se cargan del repositorio
comunitario **[Vertylo/wakassets](https://github.com/Vertylo/wakassets)**,
servido por GitHub Pages:

```
https://vertylo.github.io/wakassets/{carpeta}/{ID}.png
```

Ese repo declara explícitamente que todas sus imágenes son **© Ankama** y que se
publican **solo para proyectos comunitarios sin ánimo de lucro relacionados con
Wakfu**, que es exactamente el caso de esta herramienta.

Se intentó primero la ruta oficial documentada en el foro de desarrollo de Wakfu
(`https://s.ankama.com/www/static.ankama.com/wakfu/portal/game/item/115/{gfxId}.png`):
se probó con 5 `gfxId` reales del dataset (1202021, 1032022, 1192023, 1322024,
1332025) y **fallaron los 5** — esa ruta de 2020 ya no sirve. Los mismos 5 `gfxId`
cargan correctamente en wakassets (64×64, icono correcto), así que esa es la fuente.

El campo `gfxId` está confirmado contra el `items.json` real (versión 1.92.1.59):
vive en `definition.item.graphicParameters.gfxId` y **no** coincide con el `id` del
objeto (ej. id 2021 → gfxId 1202021). `build_dataset.py` lo guarda como `gfx` en
`items_reduced.json`. Si un objeto no lo trae, la web dibuja un marco con el color de
su rareza y la inicial del objeto.

Los **colores de rareza** de la interfaz no están inventados: se han medido pixel
a pixel sobre los propios PNG `rarities/0..7.png` de wakassets. El **nombre** de
cada número de rareza sigue sin confirmarse (pendiente abierto en PROJECT.md), así
que la interfaz nunca muestra una etiqueta de rareza, solo la gema y el color.

## Pendiente de confirmar

- Tabla completa de valores de `rareza` (se ven 1-4 en items de nivel bajo;
  falta confirmar qué número corresponde a legendario/mítico/recuerdo/etc.
  para poder filtrar por rareza además de por reliquia/épico).
- Ampliar a las 12 piezas simultáneas con optimización global (nice-to-have
  v2, discutido en la conversación).
