"""
Diagnostico 4: el usuario regenero items_reduced.json y "Armadura dada" /
"Armadura recibida" / "Pasiva unica" salen 0 veces (deberian ser ~216 y ~570).
Esto traza EXACTAMENTE que rama del codigo de build_dataset.py se ejecuta para
el efecto actionId 39 de la Varita de mago gris (nivel 245), en vez de asumir
nada.

Uso (desde la raiz del repo, con data/ ya poblado):
    python diagnose_stats4.py
"""
import importlib.util
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def latest(name):
    candidates = sorted(DATA_DIR.glob(f"{name}_*.json"))
    if not candidates:
        raise SystemExit(f"No encuentro data/{name}_*.json — ejecuta build_dataset.py primero.")
    return json.loads(candidates[-1].read_text(encoding="utf-8"))


items = latest("items")

spec = importlib.util.spec_from_file_location("bd", Path(__file__).parent / "build_dataset.py")
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)

print("Confirmando que el modulo build_dataset.py cargado tiene el fix:")
print("  ARMOR_ACTION_IDS =", bd.ARMOR_ACTION_IDS)
print("  ARMOR_PARAM4_LABELS =", bd.ARMOR_PARAM4_LABELS)
print("  UNIQUE_PASSIVE_ACTION_IDS =", bd.UNIQUE_PASSIVE_ACTION_IDS)
print()

for entry in items:
    item_def = entry["definition"]["item"]
    title = entry.get("title", {})
    name = title.get("es") or title.get("en") or ""
    if "mago gris" in name.lower() and item_def.get("level") == 245:
        print(f"=== {name} (id={item_def['id']}, nivel {item_def['level']}) ===")
        for eff in entry["definition"].get("equipEffects", []):
            definition = eff["effect"]["definition"]
            action_id = definition["actionId"]
            params = definition.get("params", [])
            print(f"  actionId={action_id!r} (tipo {type(action_id).__name__})  params={params}")
            if action_id in bd.ARMOR_ACTION_IDS:
                ref = params[4] if len(params) > 4 and isinstance(params[4], (int, float)) else None
                print(f"    -> SI esta en ARMOR_ACTION_IDS. ref={ref!r} (tipo {type(ref).__name__ if ref is not None else None})")
                if ref is not None:
                    print(f"    -> int(ref)={int(ref)}  ARMOR_PARAM4_LABELS.get(int(ref))={bd.ARMOR_PARAM4_LABELS.get(int(ref))!r}")
            else:
                print(f"    -> NO esta en ARMOR_ACTION_IDS={bd.ARMOR_ACTION_IDS!r}")
