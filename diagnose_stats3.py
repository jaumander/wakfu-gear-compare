"""
Diagnostico 3: barrido completo de actionIds reales para ver si queda alguno
mas (aparte de 39/40, que ya se arreglo) cuyo nombre no se resuelve bien.

Reutiliza las funciones y las tablas de casos especiales YA CONFIRMADAS de
build_dataset.py (en vez de duplicar la logica), para no dar falsos positivos
sobre estadisticas que ya sabemos que estan bien.

Uso (desde la raiz del repo, con data/ ya poblado por build_dataset.py):
    python diagnose_stats3.py
"""
import importlib.util
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

spec = importlib.util.spec_from_file_location("bd", Path(__file__).parent / "build_dataset.py")
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)

action_map = bd.build_action_map(actions)
raw_by_id = {e["definition"]["id"]: e.get("description", {}) for e in actions}

# actionIds que YA tienen un caso especial resuelto en build_dataset.py; los
# saltamos aqui porque sabemos que su nombre final no depende de action_map.
ALREADY_FIXED = set(bd.ELEMENTAL_N_ACTION_IDS) | set(bd.ELEMENTAL_ALL_ACTION_IDS) | set(bd.ARMOR_ACTION_IDS)

problematic = Counter()
examples = {}
for entry in items:
    item_def = entry["definition"]["item"]
    title = entry.get("title", {})
    name = title.get("es") or title.get("en") or f"item_{item_def['id']}"
    for eff in entry["definition"].get("equipEffects", []):
        definition = eff["effect"]["definition"]
        action_id = definition["actionId"]
        params = definition.get("params", [])
        if not params or action_id in ALREADY_FIXED:
            continue
        label = action_map.get(action_id, f"accion_{action_id}")
        if label == "Stat desconocida" or label.startswith("accion_"):
            problematic[action_id] += 1
            examples.setdefault(action_id, (name, params))

print(f"Total actionIds problematicos SIN resolver todavia: {len(problematic)}")
for action_id, count in sorted(problematic.items(), key=lambda kv: -kv[1]):
    name, params = examples[action_id]
    print(f"  actionId={action_id}  apariciones={count}  ejemplo={name!r}  params={params}  raw={raw_by_id.get(action_id)!r}")
