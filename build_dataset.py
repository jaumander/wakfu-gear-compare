"""
build_dataset.py
-----------------
Descarga los datos oficiales de Wakfu (publicados por Ankama) y genera un
dataset reducido (items_reduced.json) con solo los objetos equipables de los
12 slots relevantes, incluyendo si son reliquia/épico y sus stats resueltas
a nombre legible.

Requiere conexión a internet hacia wakfu.cdn.ankama.com (solo librerías
estándar de Python, no hace falta instalar nada).

Uso:
    python build_dataset.py
"""

import json
import re
import urllib.request
from pathlib import Path

BASE_URL = "https://wakfu.cdn.ankama.com/gamedata"
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_PATH = Path(__file__).parent / "items_reduced.json"

# equipmentPositions oficiales -> etiqueta de slot en español
POSITION_LABELS = {
    "HEAD": "Casco",
    "NECK": "Amuleto",
    "CHEST": "Pechera",
    "BACK": "Capa",
    "SHOULDERS": "Hombreras",
    "BELT": "Cinturón",
    "LEGS": "Botas",
    "LEFT_HAND": "Anillo",
    "RIGHT_HAND": "Anillo",
    "FIRST_WEAPON": "Mano Derecha (arma)",
    "SECOND_WEAPON": "Mano Izquierda (arma/escudo)",
}

# El emblema y las herramientas comparten la posición ACCESSORY;
# distinguimos por itemTypeId.
EMBLEM_TYPE_ID = 646

RELIC_PROPERTY_ID = 8   # "solo 1 equipado a la vez" (reliquia)
EPIC_PROPERTY_ID = 12   # "solo 1 equipado a la vez" (épico)


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "wakfu-gear-compare/1.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_current_version():
    return fetch_json(f"{BASE_URL}/config.json")["version"]


def download_raw(version):
    DATA_DIR.mkdir(exist_ok=True)
    raw = {}
    for name in ["items", "itemTypes", "itemProperties", "actions"]:
        cache_path = DATA_DIR / f"{name}_{version}.json"
        if cache_path.exists():
            print(f"  {name}.json ya en caché, lo reutilizo")
            raw[name] = json.loads(cache_path.read_text(encoding="utf-8"))
            continue
        print(f"  Descargando {name}.json ...")
        data = fetch_json(f"{BASE_URL}/{version}/{name}.json")
        cache_path.write_text(json.dumps(data), encoding="utf-8")
        raw[name] = data
    return raw


def build_slot_map(item_types):
    """itemTypeId -> etiqueta de slot en español."""
    slot_map = {}
    for entry in item_types:
        d = entry["definition"]
        type_id = d["id"]
        if type_id == EMBLEM_TYPE_ID:
            slot_map[type_id] = "Emblema"
            continue
        positions = d.get("equipmentPositions", [])
        for pos in positions:
            if pos in POSITION_LABELS:
                slot_map[type_id] = POSITION_LABELS[pos]
                break
    return slot_map


def clean_stat_label(raw_label):
    """Limpia los placeholders tipo [#1], {...} de las descripciones oficiales."""
    label = re.sub(r"\[#?\d+\]", "", raw_label)
    label = re.sub(r"\[[a-zA-Z0-9]+\]", "", label)
    label = re.sub(r"\{.*?\}", "", label)
    label = label.strip(" :%-\u00a0")
    return label or "Stat desconocida"


def build_action_map(actions):
    """actionId -> nombre de stat legible (preferimos español, luego inglés)."""
    action_map = {}
    for entry in actions:
        action_id = entry["definition"]["id"]
        desc = entry.get("description", {})
        raw_label = desc.get("es") or desc.get("en") or entry["definition"].get("effect", "")
        action_map[action_id] = clean_stat_label(raw_label)
    return action_map


def build_reduced_items(items, slot_map, action_map):
    reduced = []
    for entry in items:
        item_def = entry["definition"]["item"]
        base = item_def["baseParameters"]
        type_id = base["itemTypeId"]

        slot_label = slot_map.get(type_id)
        if slot_label is None:
            continue  # no es uno de los 12 slots que nos interesan

        props = item_def.get("properties", [])
        is_relic = RELIC_PROPERTY_ID in props
        is_epic = EPIC_PROPERTY_ID in props

        stats = {}
        for eff in entry["definition"].get("equipEffects", []):
            definition = eff["effect"]["definition"]
            action_id = definition["actionId"]
            params = definition.get("params", [])
            if not params:
                continue
            value = params[0]
            if not isinstance(value, (int, float)):
                continue
            stat_name = action_map.get(action_id, f"accion_{action_id}")
            stats[stat_name] = stats.get(stat_name, 0) + value

        title = entry.get("title", {})
        name = title.get("es") or title.get("en") or f"item_{item_def['id']}"

        reduced.append({
            "id": item_def["id"],
            "nombre": name,
            "slot": slot_label,
            "nivel": item_def["level"],
            "rareza": base.get("rarity"),
            "set_id": base.get("itemSetId"),
            "es_reliquia": is_relic,
            "es_epico": is_epic,
            "stats": stats,
        })
    return reduced


def main():
    print("Consultando versión actual del juego...")
    version = get_current_version()
    print(f"Versión: {version}")

    print("Descargando datos oficiales (items.json puede tardar, pesa 20+MB)...")
    raw = download_raw(version)

    print("Construyendo mapeos de slot y de stats...")
    slot_map = build_slot_map(raw["itemTypes"])
    action_map = build_action_map(raw["actions"])

    print("Generando dataset reducido...")
    reduced = build_reduced_items(raw["items"], slot_map, action_map)

    OUTPUT_PATH.write_text(json.dumps(reduced, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Listo: {OUTPUT_PATH} ({len(reduced)} objetos equipables)")


if __name__ == "__main__":
    main()
