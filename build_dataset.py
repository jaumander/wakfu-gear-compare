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

# actionId confirmados manualmente contra el JSON crudo de Ankama (ver HANDOFF/PROJECT
# para el detalle): la descripción oficial de estos 2 viene rota ("[#charac X] }"), así
# que el nombre se fija a mano en vez de fiarse del texto de actions.json.
#   1068 = Dominio elemental "en N elementos" (params[0]=valor, params[2]=nº elementos)
#   1069 = Resistencia elemental "en N elementos" (mismo formato que 1068)
#   80   = Resistencia elemental que aplica SIEMPRE a los 4 elementos (sin nº)
#   120  = Dominio elemental que aplica SIEMPRE a los 4 elementos (sin nº)
ELEMENTAL_N_ACTION_IDS = {1068: "Dominio elemental", 1069: "Resistencia elemental"}
ELEMENTAL_ALL_ACTION_IDS = {80: "Resistencia elemental (todos)", 120: "Dominio elemental (todos)"}

# actionId 39/40: plantilla generica "[#1]{...%} [#3]" cuyo texto en actions.json NO
# sirve para saber el nombre (a diferencia de arriba, aqui el numero en params[4] NO
# es un actionId real, es un codigo de caracteristica en una tabla aparte que no
# tenemos). Confirmado contra capturas del propio juego (2026-08): actionId 39 con
# params[4]=120.0 en "Varita de mago gris" = "5% de armadura dada" (5.0 = params[0]),
# y con params[4]=121.0 en "Botas rompehielos" = "5% de armadura recibida". Solo se
# han visto estos 2 valores en los 216 objetos reales que usan 39/40 (ver
# diagnose_stats2.py). actionId 40 es la version en negativo (el texto crudo empieza
# por "-"), asi que se le resta el valor en vez de sumarlo.
ARMOR_ACTION_IDS = (39, 40)
ARMOR_PARAM4_LABELS = {120: "Armadura dada", 121: "Armadura recibida"}

# actionId 304: NO es un stat normal, es el efecto de una PASIVA ÚNICA de texto libre
# (confirmado por el usuario viendo los objetos reales que lo usan: son objetos con
# habilidades especiales redactadas a mano, no una característica sumable). El número
# de params[0] no representa un valor de stat comparable, así que en vez de intentar
# nombrarlo como stat se marca aparte para no confundir con "Stat desconocida".
UNIQUE_PASSIVE_ACTION_IDS = {304: "Pasiva única (ver descripción del objeto)"}


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


def build_two_handed_set(item_types):
    """itemTypeId de armas que ocupan las 2 manos (Hacha, Pala, Martillo, Arco,
    Espada/Baston de 2 manos...). Confirmado con datos reales: cuando una arma de
    FIRST_WEAPON trae "SECOND_WEAPON" en equipmentDisabledPositions, el juego no
    deja poner nada en la mano izquierda a la vez (ver diagnose_weapons2.py)."""
    two_handed = set()
    for entry in item_types:
        d = entry["definition"]
        if "SECOND_WEAPON" in d.get("equipmentDisabledPositions", []):
            two_handed.add(d["id"])
    return two_handed


def clean_stat_label(raw_label):
    """Limpia los placeholders de las descripciones oficiales de Ankama.

    Los placeholders reales no son solo tipo [#1]: incluyen letras y espacios,
    ej. "[#charac AP]  PA" o "[#charac BLOCK] -% de anticipación". Por eso se
    quita CUALQUIER contenido entre corchetes, sin asumir que solo hay dígitos.
    """
    label = re.sub(r"\[.*?\]", "", raw_label)
    label = re.sub(r"\{.*?\}", "", label)
    label = label.strip()
    label = re.sub(r"^[-%\s]+", "", label)       # restos de "-% " al principio
    label = re.sub(r"^de\s+", "", label, flags=re.IGNORECASE)  # "de golpe crítico" -> "golpe crítico"
    label = label.strip(" :%-\u00a0}")
    if not label:
        return "Stat desconocida"
    return label[0].upper() + label[1:]


def build_action_map(actions):
    """actionId -> nombre de stat legible (preferimos español, luego inglés)."""
    action_map = {}
    for entry in actions:
        action_id = entry["definition"]["id"]
        desc = entry.get("description", {})
        raw_label = desc.get("es") or desc.get("en") or entry["definition"].get("effect", "")
        action_map[action_id] = clean_stat_label(raw_label)
    return action_map


def build_reduced_items(items, slot_map, action_map, two_handed_ids):
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

        # Identificador GRAFICO del objeto. Confirmado contra el items.json real
        # (version 1.92.1.59) el 2026-08-02: vive en
        # definition.item.graphicParameters.gfxId, y NO coincide con el `id` del
        # objeto (ej. id 2021 -> gfxId 1202021). Hay tambien un femaleGfxId, que
        # en los objetos comprobados vale lo mismo; no lo guardamos porque la web
        # no distingue genero.
        # Es lo que necesita la web para pintar el icono real de cada objeto.
        gfx_id = item_def.get("graphicParameters", {}).get("gfxId")

        # itemTypeId: lo usa la web para pintar el icono del TIPO de objeto
        # (casco, amuleto, botas...) en el tooltip. wakassets lo sirve en
        # itemTypes/{itemTypeId}.png y coincide con el mapeo que ya usamos aqui
        # para asignar el slot (build_slot_map).
        type_icon_id = type_id

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
            if action_id in ELEMENTAL_N_ACTION_IDS:
                count = params[2] if len(params) > 2 and isinstance(params[2], (int, float)) else None
                base_label = ELEMENTAL_N_ACTION_IDS[action_id]
                stat_name = f"{base_label} ({int(count)} elementos)" if count else base_label
            elif action_id in ELEMENTAL_ALL_ACTION_IDS:
                stat_name = ELEMENTAL_ALL_ACTION_IDS[action_id]
            elif action_id in ARMOR_ACTION_IDS:
                ref = params[4] if len(params) > 4 and isinstance(params[4], (int, float)) else None
                stat_name = ARMOR_PARAM4_LABELS.get(int(ref)) if ref is not None else None
                if stat_name is None:
                    stat_name = f"accion_{action_id}"
                if action_id == 40:
                    value = -value
            elif action_id in UNIQUE_PASSIVE_ACTION_IDS:
                stat_name = UNIQUE_PASSIVE_ACTION_IDS[action_id]
                value = 1  # solo marca "tiene una pasiva única"; el número crudo no es un stat sumable
            else:
                stat_name = action_map.get(action_id, f"accion_{action_id}")
            stats[stat_name] = stats.get(stat_name, 0) + value

        title = entry.get("title", {})
        name = title.get("es") or title.get("en") or f"item_{item_def['id']}"

        reduced.append({
            "id": item_def["id"],
            "gfx": gfx_id,
            "tipo_id": type_icon_id,
            "nombre": name,
            "slot": slot_label,
            "nivel": item_def["level"],
            "rareza": base.get("rarity"),
            "set_id": base.get("itemSetId"),
            "es_reliquia": is_relic,
            "es_epico": is_epic,
            "es_dos_manos": type_id in two_handed_ids,
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
    two_handed_ids = build_two_handed_set(raw["itemTypes"])
    action_map = build_action_map(raw["actions"])

    print("Generando dataset reducido...")
    reduced = build_reduced_items(raw["items"], slot_map, action_map, two_handed_ids)

    con_gfx = sum(1 for it in reduced if it.get("gfx"))
    print(f"  objetos con gfx (icono): {con_gfx} / {len(reduced)}")
    con_tipo = sum(1 for it in reduced if it.get("tipo_id"))
    print(f"  objetos con tipo_id (icono de tipo): {con_tipo} / {len(reduced)}")
    if con_gfx < len(reduced):
        print("  aviso: algunos objetos no traen graphicParameters.gfxId;")
        print("         la web les pondra un marco de rareza con la inicial.")

    OUTPUT_PATH.write_text(json.dumps(reduced, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Listo: {OUTPUT_PATH} ({len(reduced)} objetos equipables)")


if __name__ == "__main__":
    main()
