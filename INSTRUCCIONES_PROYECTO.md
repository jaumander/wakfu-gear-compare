Este proyecto es una herramienta de comparación de equipo de Wakfu (wakfu-gear-compare)
que descarga los datos oficiales de Ankama (items.json, itemTypes.json, itemProperties.json,
actions.json) y calcula combinaciones válidas de equipo respetando la restricción de
"máx. 1 reliquia y máx. 1 épico equipados a la vez".

Este proyecto no tiene archivos subidos en la sección de archivos del proyecto — todo vive
en GitHub (https://github.com/jaumander/wakfu-gear-compare, rama main).

Al empezar cualquier conversación donde haya que tocar el código o el PROJECT.md:
1. Clona el repo con git usando el token de abajo.
2. Lee HANDOFF.md en la raíz: si dice "Nada en curso", trabaja normal desde PROJECT.md;
   si no, hay trabajo a medias de otra sesión — continúa desde ahí, no reimplementes.

token_for_claude: <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>

Antes de tocar código o asumir un campo/formato del JSON de Ankama (mapeo de itemTypeId a
slot, valores de "rareza", qué actionId corresponde a qué stat, etc.), verifica el dato real
descargándolo y comprobándolo (python/node) — nunca asumas el formato por documentación
externa, por lo que "suena lógico" en otros juegos tipo Dofus, ni de memoria de sesiones
pasadas. Ankama puede cambiar el esquema entre versiones del juego sin avisar. Si el entorno
no tiene acceso a wakfu.cdn.ankama.com y hace falta verificar un dato, pídele al usuario que
lo confirme o pegue el JSON relevante en la conversación antes de escribir o tocar el parser.

Antes de actuar, piensa la forma de gastar pocos tokens/uso.

Da siempre un breve contexto en lenguaje no técnico de lo que se ha hecho, ya que quien usa
este proyecto no es programador y quiere entender el porqué, no solo el qué.

Todo cambio en build_dataset.py o compare.py debe validarse ejecutándolo (contra datos reales
si hay red disponible, o contra el dataset de prueba items_reduced.json si no la hay) antes
de entregarlo — nunca entregar sin probar.

El PROJECT.md del conocimiento del proyecto es la fuente de verdad del estado actual;
consúltalo antes de reimplementar algo que ya esté documentado como hecho.

Todo cambio se sube en commits pequeños con prefijo "WIP:" a medida que avanzas, no un único
commit al final. Antes de que acabe la sesión (por falta de tokens o al terminar), actualiza
HANDOFF.md (déjalo en "Nada en curso" si terminaste, o rellena la plantilla si queda algo a
medias) y haz commit+push de ese archivo en el mismo commit final.

## Metodología para features grandes (varias partes de la app o riesgo de romper algo)
Para cambios pequeños y aislados, sigue el flujo normal (un commit, una prueba). Para
features que pueden tocar varias partes de la app o tienen riesgo de romper algo existente
(ej. pasar de comparar 2-4 slots a optimizar las 12 piezas del build):
1. Antes de implementar, decide y escribe el ALCANCE en PROJECT.md: qué va a tocar la
   feature y, explícitamente, qué NO va a tocar / qué límites tiene para no poder romper
   otras partes de la app.
2. Trocea en milestones pequeños y numerados (ej. "1/4", "2/4"...). Cada milestone debe
   dejar la app en un estado que funcione, aunque la feature no esté completa — usa stubs
   defensivos si un milestone necesita algo que añadirá otro milestone posterior.
3. Cada milestone es su propio commit WIP:, validado antes de commitear, y pusheado.
4. Actualiza HANDOFF.md al final de CADA milestone (esto sustituye a "actualízalo al final
   de la sesión" para este tipo de features) — nunca lo dejes desactualizado más de un
   commit. Vacíalo a "Nada en curso" solo cuando la feature esté 100% completa y documentada
   en PROJECT.md.
