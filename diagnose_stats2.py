"""
Diagnostico 2: el actionId 39 (y su gemelo 40) usan una plantilla generica
"[#1]{...%} [#3]" donde el hueco [#3] no es texto fijo sino que se rellena
con OTRO stat, probablemente referenciado por uno de los parametros
numericos (params[4]=120.0 en el caso de la Varita de mago gris). Este
script comprueba esa hipotesis contra datos reales antes de tocar el
parser:

1. Muestra la descripcion cruda del actionId 120 (para ver si tiene algo
   que ver con "armadura").
2. Recopila, para TODOS los items que usan actionId 39 o 40, el valor de
   cada posicion de params, para ver si params[4] es siempre un actionId
   valido (y cual).

Uso (desde la raiz del repo, con data/ ya poblado por build_dataset.py):
    python diagnose_stats2.py
"""
import json
from collections import Counter
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def latest(name):
    candidates = sorted(DATA_DIR.glob(f"{name}_*.json"))
    if not candidates:
        raise SystemExit(f"No encuentro data/{name}_*.json — ejecuta build_dataset.py primero.")
    return json.loads(candidates[-1].read_text(encoding="utf-8"))


items = latest("items")
actions = latest("actions")

action_map_raw = {}
for entry in actions:
    action_id = entry["definition"]["id"]
    desc = entry.get("description", {})
    raw_label = desc.get("es") or desc.get("en") or entry["definition"].get("effect", "")
    action_map_raw[action_id] = raw_label

print("=== Descripcion cruda de actionId 120 (referenciado por la Varita de mago gris) ===")
print(f"  {action_map_raw.get(120, '<no existe>')!r}")
print()

print("=== Todos los items que usan actionId 39 o 40, con sus params completos ===")
count = 0
param4_values = Counter()
for entry in items:
    item_def = entry["definition"]["item"]
    title = entry.get("title", {})
    name = title.get("es") or title.get("en") or f"item_{item_def['id']}"
    for eff in entry["definition"].get("equipEffects", []):
        definition = eff["effect"]["definition"]
        action_id = definition["actionId"]
        if action_id in (39, 40):
            params = definition.get("params", [])
            print(f"  actionId={action_id}  nombre={name}  nivel={item_def.get('level')}  params={params}")
            count += 1
            if len(params) > 4:
                ref = params[4]
                param4_values[ref] += 1
                ref_desc = action_map_raw.get(int(ref)) if isinstance(ref, (int, float)) else None
                if ref_desc is not None:
                    print(f"      -> params[4]={ref} coincide con actionId {int(ref)}, cuya descripcion cruda es: {ref_desc!r}")

print()
print(f"Total apariciones de actionId 39/40: {count}")
print(f"Valores distintos vistos en params[4]: {dict(param4_values)}")
