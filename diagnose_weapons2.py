"""
Diagnostico armas 2 manos - paso 1: buscar el campo real de itemTypes.json (o de
items.json) que distingue un arma de DOS manos (vara, arco, arco largo...) de una
de UNA mano (espada, daga, hacha de una mano...). No se asume nada: se imprime el
JSON crudo completo de un par de itemTypes conocidos para poder comparar a ojo.

Uso (desde la raiz del repo, con data/ ya poblado por build_dataset.py):
    python diagnose_weapons2.py
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def latest(name):
    candidates = sorted(DATA_DIR.glob(f"{name}_*.json"))
    if not candidates:
        raise SystemExit(f"No encuentro data/{name}_*.json — ejecuta build_dataset.py primero.")
    return json.loads(candidates[-1].read_text(encoding="utf-8"))


item_types = latest("itemTypes")

# Buscamos por nombre de tipo (nameId no ayuda, así que miramos el título/"denomination"
# si existe; si no aparece por nombre, imprimimos TODOS los tipos con equipmentPositions
# que incluyan FIRST_WEAPON o SECOND_WEAPON, para localizarlos a mano).
print("=== Todos los itemTypes con FIRST_WEAPON o SECOND_WEAPON en equipmentPositions ===")
for entry in item_types:
    d = entry["definition"]
    positions = d.get("equipmentPositions", [])
    if "FIRST_WEAPON" in positions or "SECOND_WEAPON" in positions:
        print(f"\n--- itemTypeId={d['id']} ---")
        print(json.dumps(entry, ensure_ascii=False, indent=2))
