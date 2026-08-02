"""
compare.py
----------
Busca objetos por nombre (o ID) en items_reduced.json y compara combinaciones
de candidatos respetando la restricción de "máx. 1 reliquia y máx. 1 épico
equipados a la vez".

Uso como CLI (buscar):
    python compare.py --search "amuleto"
    python compare.py --search "bota" --slot Botas

Uso como librería (comparar combinaciones) — ver ejemplo_uso.py
"""

import argparse
import json
from itertools import product
from pathlib import Path

DATA_PATH = Path(__file__).parent / "items_reduced.json"


def load_items(path=DATA_PATH):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def search_by_name(items, query, slot=None):
    query = query.lower()
    return [
        it for it in items
        if query in it["nombre"].lower() and (slot is None or it["slot"] == slot)
    ]


def find_by_id(items, item_id):
    for it in items:
        if it["id"] == item_id:
            return it
    return None


def is_valid_combo(combo):
    relics = sum(1 for it in combo if it["es_reliquia"])
    epics = sum(1 for it in combo if it["es_epico"])
    return relics <= 1 and epics <= 1


def sum_stats(combo):
    total = {}
    for it in combo:
        for stat, value in it["stats"].items():
            total[stat] = total.get(stat, 0) + value
    return total


def compare(candidates_by_slot, sort_by=None):
    """
    candidates_by_slot: dict {etiqueta_de_slot: [item_dict, item_dict, ...]}
        La etiqueta puede ser cualquier string que tú elijas (ej. "amuleto",
        "botas", "anillo_1", "anillo_2"...), no tiene que coincidir con el
        campo "slot" del dataset.

    Devuelve la lista de combinaciones VÁLIDAS (sin violar la exclusividad
    de reliquia/épico), cada una con sus items y stats totales sumadas.
    """
    slot_labels = list(candidates_by_slot.keys())
    option_lists = [candidates_by_slot[s] for s in slot_labels]

    results = []
    for combo in product(*option_lists):
        if not is_valid_combo(combo):
            continue
        results.append({
            "combinacion": {
                slot_labels[i]: combo[i]["nombre"] + (
                    " [RELIQUIA]" if combo[i]["es_reliquia"] else
                    " [ÉPICO]" if combo[i]["es_epico"] else ""
                )
                for i in range(len(combo))
            },
            "stats": sum_stats(combo),
        })

    if sort_by:
        results.sort(key=lambda r: r["stats"].get(sort_by, 0), reverse=True)

    return results


def print_results(results, top=None):
    to_show = results[:top] if top else results
    for i, r in enumerate(to_show, 1):
        print(f"\n--- Combinación {i} ---")
        for slot, name in r["combinacion"].items():
            print(f"  {slot}: {name}")
        print("  Stats totales:")
        for stat, value in sorted(r["stats"].items(), key=lambda kv: -kv[1]):
            print(f"    {stat}: {value}")


def main():
    parser = argparse.ArgumentParser(description="Busca items de Wakfu por nombre")
    parser.add_argument("--search", help="Texto a buscar en el nombre")
    parser.add_argument("--slot", help="Filtrar por slot (ej: Botas, Amuleto)")
    args = parser.parse_args()

    items = load_items()

    if args.search:
        results = search_by_name(items, args.search, args.slot)
        if not results:
            print("Sin resultados.")
            return
        for it in results:
            flag = " [RELIQUIA]" if it["es_reliquia"] else " [ÉPICO]" if it["es_epico"] else ""
            print(f"{it['id']:>6}  {it['nombre']}{flag}  (nivel {it['nivel']}, {it['slot']})")
        return

    print("Usa --search 'nombre' para buscar. Para comparar combinaciones, usa este")
    print("módulo como librería (ver ejemplo_uso.py).")


if __name__ == "__main__":
    main()
