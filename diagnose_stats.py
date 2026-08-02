"""
Diagnostico: por que "armadura dada" (y similares) caen en el cajon "Stat
desconocida" en vez de mostrarse con su propio nombre.

Uso (desde la raiz del repo, con data/ ya poblado por build_dataset.py):
    python diagnose_stats.py
"""
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def clean_stat_label(raw_label):
    label = re.sub(r"\[#?\d+\]", "", raw_label)
    label = re.sub(r"\[[a-zA-Z0-9]+\]", "", label)
    label = re.sub(r"\{.*?\}", "", label)
    label = label.strip(" :%-\u00a0")
    return label or "Stat desconocida"


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

# --- Caso concreto: Varita de mago gris (nivel 245) ---
print("=== Varita de mago gris (nivel 245) ===")
for entry in items:
    item_def = entry["definition"]["item"]
    title = entry.get("title", {})
    name = title.get("es") or title.get("en") or ""
    if "mago gris" in name.lower() and item_def.get("level") == 245:
        print(f"id={item_def['id']}  nombre={name}")
        for eff in entry["definition"].get("equipEffects", []):
            definition = eff["effect"]["definition"]
            action_id = definition["actionId"]
            params = definition.get("params", [])
            raw = action_map_raw.get(action_id, "<sin descripcion>")
            cleaned = clean_stat_label(raw) if raw != "<sin descripcion>" else "Stat desconocida"
            print(f"  actionId={action_id}  params={params}  raw_desc={raw!r}  -> limpio: {cleaned!r}")

# --- Barrido general: que actionIds usados de verdad en items caen en "Stat desconocida" ---
print()
print("=== Barrido general: actionIds cuya descripcion limpia queda vacia/generica ===")
used_action_ids = set()
for entry in items:
    for eff in entry["definition"].get("equipEffects", []):
        used_action_ids.add(eff["effect"]["definition"]["actionId"])

problematic = {}
for action_id in used_action_ids:
    raw = action_map_raw.get(action_id)
    if raw is None:
        problematic[action_id] = "<actionId sin entrada en actions.json>"
        continue
    cleaned = clean_stat_label(raw)
    if cleaned == "Stat desconocida" or cleaned.strip() == "":
        problematic[action_id] = raw

print(f"Total actionIds problematicos: {len(problematic)}")
for action_id, raw in sorted(problematic.items()):
    print(f"  actionId={action_id}  raw_desc={raw!r}")
