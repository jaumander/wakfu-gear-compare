"""
Diagnóstico rápido: ¿qué valores de equipmentPositions existen en itemTypes.json
que NO estemos mapeando en build_dataset.py? Sirve para encontrar por qué las
armas a dos manos no aparecen.

Uso: ejecútalo desde la raíz del repo, con data/ ya poblado por build_dataset.py
(no descarga nada nuevo).

    python diagnose_weapons.py
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

# Copiado de build_dataset.py para comparar
POSITION_LABELS = {
    "HEAD": "Casco", "NECK": "Amuleto", "CHEST": "Pechera", "BACK": "Capa",
    "SHOULDERS": "Hombreras", "BELT": "Cinturón", "LEGS": "Botas",
    "LEFT_HAND": "Anillo", "RIGHT_HAND": "Anillo",
    "FIRST_WEAPON": "Mano Derecha (arma)", "SECOND_WEAPON": "Mano Izquierda (arma/escudo)",
}

candidates = sorted(DATA_DIR.glob("itemTypes_*.json"))
if not candidates:
    raise SystemExit("No encuentro data/itemTypes_*.json — ejecuta build_dataset.py primero.")

item_types = json.loads(candidates[-1].read_text(encoding="utf-8"))

all_positions = set()
unmapped_types = []

for entry in item_types:
    d = entry["definition"]
    positions = d.get("equipmentPositions", [])
    all_positions.update(positions)
    if positions and not any(p in POSITION_LABELS for p in positions):
        name = d.get("name") or entry.get("title", {}).get("es") or f"type_{d['id']}"
        unmapped_types.append((d["id"], name, positions))

print("Todos los valores de equipmentPositions encontrados en el JSON real:")
for p in sorted(all_positions):
    print(" -", p)

print()
print(f"itemTypeId cuyas posiciones NO están mapeadas en absoluto ({len(unmapped_types)}):")
for type_id, name, positions in unmapped_types[:20]:
    print(f"  id={type_id}  nombre={name}  positions={positions}")
