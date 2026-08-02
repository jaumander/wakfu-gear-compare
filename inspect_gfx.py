"""
inspect_gfx.py
--------------
Script de un solo uso: mira el items.json REAL de Ankama y busca dónde está el
identificador gráfico de cada objeto (el "gfxId", que es lo que hace falta para
poder mostrar el icono de cada objeto en la web).

No modifica nada. Solo imprime.

Uso:
    python inspect_gfx.py

Reutiliza los archivos ya descargados en data/ si existen; si no, se los baja.
"""

import glob
import json
import os
import urllib.request

BASE_URL = "https://wakfu.cdn.ankama.com/gamedata"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "wakfu-gear-compare/1.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def load_items():
    cached = sorted(glob.glob(os.path.join("data", "items_*.json")))
    if cached:
        print(f"Usando el archivo ya descargado: {cached[-1]}")
        with open(cached[-1], encoding="utf-8") as fh:
            return json.load(fh)
    print("No hay items.json en data/. Descargando de Ankama (20+MB, tarda un poco)...")
    version = fetch_json(f"{BASE_URL}/config.json")["version"]
    print(f"Version del juego: {version}")
    items = fetch_json(f"{BASE_URL}/{version}/items.json")
    os.makedirs("data", exist_ok=True)
    with open(os.path.join("data", f"items_{version}.json"), "w", encoding="utf-8") as fh:
        json.dump(items, fh)
    return items


def find_gfx_paths(node, path=""):
    """Busca recursivamente cualquier clave que suene a identificador grafico."""
    found = []
    if isinstance(node, dict):
        for key, value in node.items():
            here = f"{path}.{key}" if path else key
            if "gfx" in key.lower() or "graphic" in key.lower():
                found.append((here, value if not isinstance(value, (dict, list)) else type(value).__name__))
            found.extend(find_gfx_paths(value, here))
    elif isinstance(node, list):
        for i, value in enumerate(node[:3]):
            found.extend(find_gfx_paths(value, f"{path}[{i}]"))
    return found


def main():
    items = load_items()
    print(f"\n{len(items)} objetos en total.\n")

    print("=" * 70)
    print("1) UN OBJETO COMPLETO (los primeros 2500 caracteres)")
    print("=" * 70)
    sample = items[0]
    print(json.dumps(sample, ensure_ascii=False, indent=2)[:2500])

    print("\n" + "=" * 70)
    print("2) CLAVES QUE SUENAN A IDENTIFICADOR GRAFICO, en 5 objetos")
    print("=" * 70)
    for entry in items[:5]:
        item_id = entry["definition"]["item"]["id"]
        name = (entry.get("title") or {}).get("es") or (entry.get("title") or {}).get("en") or "?"
        hits = find_gfx_paths(entry)
        print(f"\nid={item_id}  {name}")
        if hits:
            for path, value in hits:
                print(f"    {path} = {value}")
        else:
            print("    (ninguna clave con 'gfx' ni 'graphic')")

    print("\n" + "=" * 70)
    print("3) TODAS LAS CLAVES DE definition.item (para ver que hay disponible)")
    print("=" * 70)
    print(sorted(sample["definition"]["item"].keys()))
    print("\nbaseParameters:")
    print(sorted(sample["definition"]["item"]["baseParameters"].keys()))
    print("\nclaves de primer nivel de definition:")
    print(sorted(sample["definition"].keys()))
    print("\nclaves de primer nivel del objeto entero:")
    print(sorted(sample.keys()))


if __name__ == "__main__":
    main()
