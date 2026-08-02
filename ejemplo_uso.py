"""
Ejemplo de uso real: comparar 2 amuletos y 2 pares de botas.

Edita los nombres de búsqueda (o usa IDs directamente con find_by_id) según
lo que tengas en items_reduced.json una vez ejecutes build_dataset.py.
"""

from compare import load_items, search_by_name, find_by_id, compare, print_results

items = load_items()

# --- Opción A: buscar por nombre y elegir el resultado que te interese ---
print("Resultados para 'amuleto':")
for it in search_by_name(items, "amuleto", slot="Amuleto"):
    print(f"  {it['id']}: {it['nombre']} (nivel {it['nivel']})")

# --- Opción B: si ya sabes el ID exacto (más rápido) ---
# amuleto_1 = find_by_id(items, 90001)
# amuleto_2 = find_by_id(items, 90002)
# botas_1 = find_by_id(items, 90003)
# botas_2 = find_by_id(items, 90004)

# candidatos = {
#     "Amuleto": [amuleto_1, amuleto_2],
#     "Botas": [botas_1, botas_2],
# }

# resultados = compare(candidatos, sort_by="Vitalidad")  # cambia el stat a priorizar
# print_results(resultados)
