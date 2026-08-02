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

## PRÓXIMO (en cola, sin empezar): Rediseño visual con Claude Design
- Motivación: el usuario va a dar acceso al repo a Claude Design para rehacer el diseño
  visual de `index.html`, inspirándose en 3 herramientas ya existentes (capturas
  compartidas por el usuario en la conversación, no en el repo): Wakfuli
  (wakfuli.com/builder), Zenith (zenithwakfu.com/builder) y Stratfu (stratfu.fr/builder).
  Lo que más le gustó: los iconitos de objetos con marco de rareza, y sobre todo los
  iconos de ESTADÍSTICAS (PA, PdV, Esquiva, Dominio, Resistencia...) que son iguales que
  en el propio juego.
- Investigación de iconos ya hecha (sesión 2026-08-02), para no repetirla:
  1. **Oficial de Ankama** (preferible cuando se pueda): un hilo del foro oficial de
     desarrollo de Wakfu ("[JSON] Utilisation des icônes d'objets",
     wakfu.com/fr/forum/467-developpement/416777) confirma que los iconos de OBJETOS
     (con marco de rareza) se sirven en:
     `https://s.ankama.com/www/static.ankama.com/wakfu/portal/game/item/115/{gfxId}.png`
     `{gfxId}` es el campo `graphicParameters.gfxId` de cada item en el `items.json` real
     de Ankama — NO es el mismo `id` que ya guardamos (dos items reskineados/recoloreados
     pueden compartir el mismo gfxId). **Bloqueante**: `build_dataset.py` no guarda ese
     campo todavía, y esta sesión no tenía acceso de red a wakfu.cdn.ankama.com para
     confirmar el nombre exacto del campo contra el JSON real (el nombre podría haber
     cambiado desde 2020, que es cuando se documentó en el foro). Nunca asumir el campo
     sin comprobarlo primero, según las instrucciones del proyecto.
  2. **Repo comunitario `github.com/Vertylo/wakassets`** (no oficial, pero el propio repo
     dice explícitamente: "todas las imágenes y datos son © Ankama, provistas solo para
     proyectos comunitarios no comerciales sobre Wakfu" — encaja con nuestro caso). Se
     usa así: `https://raw.githubusercontent.com/Vertylo/wakassets/main/{carpeta}/{ID}.png`
     (o el mismo patrón vía GitHub Pages en `vertylo.github.io/wakassets/...`). Carpetas
     verificadas relevantes:
     - `characteristics/` → **esto es justo lo que más le gustó al usuario**: 46 iconos
       de estadísticas del juego, nombrados en inglés (`AP.png`, `HP.png`, `DODGE.png`,
       `CRITICAL_BONUS.png`, `BACKSTAB_BONUS.png`, etc). No hay una tabla de equivalencia
       automática entre estos nombres en inglés y los nombres en español que usamos en
       `items_reduced.json` (vienen de traducir las descripciones de Ankama) — hay que
       mapearlos a mano.
     - `rarities/` → iconos `0.png` a `7.png`. Coinciden en cantidad con los valores de
       `rareza` vistos en el dataset (pendiente de confirmar en PROJECT.md) — buena pista
       visual para terminar de resolver ese pendiente comparando contra objetos de rareza
       conocida.
     - `itemTypes/` → un icono por `itemTypeId`, coincide con el mapeo que ya usa
       `build_dataset.py` (`POSITION_LABELS`) para asignar el slot de cada objeto.
     - `items/` → iconos de objetos por ID, pero probados varios IDs reales de nuestro
       `items_reduced.json` (2021, 2022, 2023) y dan 404. Los nombres de archivo que sí
       existen ahí tienen 7-8 dígitos, un rango que no coincide con nuestros IDs — con
       toda probabilidad también usan el `gfxId` de Ankama del punto 1, no el `id` del
       item. Mismo bloqueante: falta el gfxId real para confirmarlo.
- **Checklist para quien continúe (verificar todo contra datos reales, nunca asumir):**
  1. Con acceso de red a `wakfu.cdn.ankama.com`, imprimir 1-2 items completos del
     `items.json` real para confirmar el nombre exacto del campo `gfxId` (puede que el
     esquema haya cambiado desde 2020).
  2. Añadir ese campo a `items_reduced.json` en `build_dataset.py` (regenerar el dataset
     y volver a subirlo, igual que se hizo con el fix de dominio/resistencia elemental).
  3. Probar la URL oficial del punto 1 con 3-4 gfxId reales y confirmar que carga (puede
     que el "115" del path o el dominio hayan cambiado desde que se documentó).
  4. Si la URL oficial no funciona, usar wakassets como alternativa/respaldo, dejando
     claro en el propio código o en un comentario que la fuente es comunitaria y por qué.
  5. Construir a mano la tabla de equivalencia entre nuestros nombres de stat en español
     y los nombres en inglés de `characteristics/` en wakassets (ej. "PA"→"AP",
     "PdV"→"HP", "Esquiva"→"DODGE"...). Los stats elementales plegados ("Dominio/
     Resistencia elemental total") no tienen un icono 1:1 obvio en esa carpeta — decidir
     si se usa un icono genérico de dominio/resistencia o se combina visualmente.
  6. Opcional: usar `rarities/0.png`...`7.png` para terminar de confirmar la tabla de
     rareza pendiente en PROJECT.md, comparando contra objetos de rareza conocida.

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
