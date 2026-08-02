## En curso: Página web de comparación
- Milestone actual: 1/2 hecho, 2/2 pendiente
- Qué está hecho: `index.html` funcional — descarga el dataset desde GitHub, busca por
  nombre/slot/franja de nivel (1-20 y luego cada 15 niveles hasta 245), permite crear
  cubos de candidatos con nombre libre (varios reliquia/épico en el mismo cubo para
  comparar alternativas sin que se exijan a la vez), calcula combinaciones válidas
  (máx. 1 reliquia/1 épico) y las muestra ordenables por estadística. Validado
  comparando la lógica JS contra `compare.py` con Node (mismos resultados). Se
  corrigió el flujo de "añadir candidato": el popup de texto (prompt) se sustituyó
  por un desplegable con los cubos existentes, para evitar que candidatos que debían
  ir juntos (ej. 2 épicos alternativos) acabaran sin querer en cubos separados.
- Qué falta (milestone 2/2): quitar/editar candidatos ya añadidos con más comodidad
  (ahora se puede quitar uno a uno, falta pulir UX), guardar la última búsqueda en el
  propio navegador, instrucciones en el README de cómo publicarlo con GitHub Pages.
- Archivos tocados: `index.html`.
- Último commit: 709cf7d "WIP: filtro por franja de nivel + arreglar UX de añadir candidatos (desplegable en vez de prompt)"
- Sin dudas pendientes de confirmar con el usuario en este milestone.

<!--
Plantilla para cuando quede trabajo a medias:

## En curso: <nombre de la feature/milestone>
- Milestone actual: X/Y
- Qué está hecho: ...
- Qué falta: ...
- Archivos tocados en este milestone: ...
- Último commit: <hash o mensaje>
- Cualquier decisión o duda pendiente de confirmar con el usuario: ...
-->
