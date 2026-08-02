## En curso: Página web de comparación
- Milestone actual: 1/2 hecho (con extras de pulido ya incluidos), 2/2 pendiente
- Qué está hecho:
  - `index.html` funcional: descarga el dataset desde GitHub, busca por nombre/slot/
    franja de nivel (1-20 y luego cada 15 niveles hasta 245), permite crear slots de
    candidatos con nombre libre (varios reliquia/épico en el mismo slot para comparar
    alternativas sin que se exijan a la vez), calcula combinaciones válidas (máx. 1
    reliquia/1 épico) y las muestra ordenables por estadística.
  - Al añadir un slot nuevo, la lista de resultados de búsqueda se refresca sola (antes
    se quedaba con el desplegable desactualizado). El desplegable de "añadir a qué
    slot" apunta por defecto al primer slot vacío.
  - Palabra "cubo" renombrada a "slot" en toda la interfaz.
  - Comparador entre 2 combinaciones: cada tarjeta de resultado tiene una casilla
    "Comparar"; al marcar 2, aparece un panel con las 2 combinaciones completas (estilo
    Stratfu, tarjeta A morada / tarjeta B verde) y debajo la diferencia neta (B − A) en
    chips compactos con icono, solo de los stats que cambian.
  - Todos los stats (en tarjetas normales y en el comparador) llevan un icono según el
    tipo (❤️ PdV, 🛡️ resistencia, ⚔️ dominio, etc.) para lectura rápida.
  - Layout ensanchado a 1600px con padding fluido (antes 1100px fijo, dejaba mucho
    espacio muerto a los lados en pantallas grandes).
  - `build_dataset.py`: arreglado el "Stat desconocida" del Dominio/Resistencia
    elemental. Confirmado con JSON crudo real (pegado por el usuario) que Ankama usa
    actionId 1068/1069 = "en N elementos" (nº en params[2], texto oficial roto) y
    actionId 80/120 = aplica siempre a los 4 elementos (sin nº). Ahora se nombran bien:
    "Dominio/Resistencia elemental (N elementos)" o "(todos)".
  - `index.html` calcula además un stat extra "Resistencia/Dominio elemental total"
    sumando específicas ×1 + "todos" ×4 + "N elementos" ×N — validado dando 234 vs 220
    en el caso de prueba real del usuario (ver PROJECT.md para el detalle).
  - **RESUELTO**: el usuario ya subió el `items_reduced.json` regenerado (commit
    7daff4d "Add files via upload"). Verificado: 7730 objetos, con 5716 stats de tipo
    "Dominio/Resistencia elemental (N elementos)" y 3059 de tipo "(todos)" ya presentes
    (antes salían todos como "Stat desconocida"). La web ya muestra los nombres
    correctos y el total elemental combinado sin pasos adicionales.
- Qué falta:
  - Milestone 2/2 real: guardar la última búsqueda en el propio navegador, instrucciones
    en el README de cómo publicarlo con GitHub Pages. (Quitar/editar candidatos ya está
    resuelto: se puede quitar uno a uno con el botón "x" y el flujo de añadir ya no usa
    popups confusos).
- Archivos tocados: `index.html`, `build_dataset.py`, `PROJECT.md`, `items_reduced.json`.
- Último commit: 7daff4d "Add files via upload" (dataset regenerado subido por el usuario)
- Duda pendiente de confirmar con el usuario: ninguna. Listo para seguir con el
  milestone 2/2 (guardar última búsqueda + instrucciones de GitHub Pages) cuando el
  usuario quiera continuar.

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
