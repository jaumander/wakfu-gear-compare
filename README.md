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
con: nombre, slot, nivel, rareza, si es reliquia/épico, y sus stats.

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

## Pendiente de confirmar

- Tabla completa de valores de `rareza` (se ven 1-4 en items de nivel bajo;
  falta confirmar qué número corresponde a legendario/mítico/recuerdo/etc.
  para poder filtrar por rareza además de por reliquia/épico).
- Ampliar a las 12 piezas simultáneas con optimización global (nice-to-have
  v2, discutido en la conversación).
