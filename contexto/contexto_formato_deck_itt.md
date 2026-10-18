# Contexto: Formato de lamina del deck ITT y export a output/deck_output

Analisis de la estructura del deck del PMU (`contexto/contexto_deck/Reporte diario PMU -
Ciudad Paraiso.pdf`) y como traducirlo a un formato de lamina coherente con los mapas HTML
del proyecto, exportable por print screen / captura a `output/deck_output/`.

---

## 1. Layout del deck (plantilla que se repite en cada lamina)

Cada lamina tematica (Seguridad/Homicidios, Dominio/Salud, etc.) usa el MISMO patron:

```
+-----------------------------------------------------------+
| Territorio - Seguridad            (seccion, arriba izq)   |
| Homicidios                        (titulo de la lamina)   |
+---------------------------+-------------------------------+
|  CIFRA GRANDE (4)         |                               |
|  "en 2026, ene-sep"       |        MAPA por manzana       |
|  delta: -56% vs 2025      |        (coropleta             |
|                           |         escala Menos -> Mas)  |
|  mini-serie 2023-2026     |                               |
+---------------------------+-------------------------------+
| Corte: [dia,hora] - Fuente: ... - Mapa ilustrativo (pie)  |
+-----------------------------------------------------------+
```

Posiciones constantes en todo el deck:
- **Encabezado (arriba izquierda):** seccion ("Territorio - Seguridad" / "Resultados por
  dominio") + titulo (Homicidios, Salud, ...).
- **Columna izquierda:** CIFRA GRANDE (ultimo dato), periodo ("en 2026, ene-sep"),
  DELTA porcentual vs mismo periodo del ano anterior, y una MINI-SERIE (trimestral o anual
  2023-2026).
- **Centro/derecha:** el MAPA por manzana (coropleta con leyenda "Menos -> Mas").
- **Pie:** "Corte: [dia, hora]", fuente institucional y "Mapa ilustrativo".

## 2. Datos/cifras que el deck pide, por lamina

Lectura del dia (3 mensajes). Avance de la operacion: % caracterizado (56,6% - 469/828),
manzanas (27), con padrino (23), cierre estimado, estado vs meta.

Resultados por dominio (cifra grande + indicador % + delta + mapa por manzana):
- Salud (base 257 personas), Vivienda (210 hogares), Bienestar (n personas),
  Menores (n menores), Negocios (238 caracterizados, 113 afectados por terremoto).

Territorio (cifra 2026 ene-sep + delta vs 2025 + serie trimestral 2023-2026 + mapa):
- Seguridad: Homicidios (4, -56%), Hurtos (89, -28%).
- Convivencia: Rinas (547, +78%), SPA (135, +96%).
- Movilidad: Siniestros viales (5, -69%; ene-jun).
- Desarrollo economico: Establecimientos activos (311; -4% vs 2025, +32% vs 2023; serie
  anual).

Territorio - Resumen (ITT): cifra 66,4, "Fase de transformacion", serie 2023-2026
(45,1 / 53,9 / 57,6 / 66,4), y las 6 dimensiones: Seguridad, Movilidad, Desarrollo social,
Entorno urbano, Vivienda, Desarrollo economico.

Caracterizacion x territorio ("Donde priorizar"): dispersion por manzana (x=delitos,
y=necesidad de hogares); cuadrante prioridad.

Anexo - otras variables (cifra grande = ultimo dato; series 2023-2026):
- Lesionados siniestros (4; 24/30/23/4), Muertes siniestros (1; 4/3/0/1),
  VIF (17; 11/17/15/17), Matricula (3.276; 3891/3529/3310/3276),
  Desercion (5,1%), Repitencia (9,7%), NDVI (0,099; 0.095/0.110/0.110/0.099),
  Deficit habitacional (46,1%), Empleo (885 de 1.158; 834/881/898/885).

## 3. Correspondencia con los mapas HTML del proyecto

Nuestros mapas ya replican el layout del deck:
- Panel flotante arriba-izquierda = la columna izquierda del deck (cifras + series).
- Mapa por manzana al centro/derecha = el mapa de la lamina.
- Encabezado de export (titulo + corte + fuente) = encabezado/pie del deck.
Por tanto, una captura/print screen de nuestro mapa (con el panel y el encabezado de
export) produce una lamina con la MISMA estructura del deck.

## 4. Export a output/deck_output

- Carpeta de salida de laminas para presentacion: `output/deck_output/`.
- Nombre sugerido: `deck_<dimension>_<AAAA-MM-DD>.jpg|pdf` (ej. deck_seguridad_...).
- El export JPG/PDF ya existe en los mapas (seccion 13.1): captura la vista actual con
  panel + encabezado + leyenda, sobre fondo claro (sin mapa base por CORS).
- Pendiente a definir con el usuario (ver seccion 5).

## 5. Decisiones tomadas (confirmadas por el usuario)

1. **Export con dialogo "Guardar como":** al dar export, el navegador debe preguntar
   DONDE guardar el archivo (no descarga automatica a Descargas). Se implementa con la
   File System Access API (`showSaveFilePicker`) en Chrome/Edge, con nombre sugerido
   `deck_<dimension>_<AAAA-MM-DD>.jpg|pdf`; el usuario elige la carpeta (p. ej.
   `output/deck_output/`). Fallback automatico a descarga normal donde la API no exista
   (Firefox/Safari).
2. **Una lamina por dimension.** Cada mapa (seguridad, entorno urbano, avance, ITT)
   produce su propia lamina.
3. **ITT por manzana: NO por ahora (no viable).** La coropleta de manzanas queda sin color
   por dimension; el `itt` sigue uniforme (58.5) y los scores por dimension vacios. No se
   calcula el ITT por manzana en este momento. Las laminas usan las capas y cifras ya
   disponibles.

---

## 6. Estado actual del export y PENDIENTE (lamina estructurada tipo deck)

### 6.1 Lo que ya funciona
- Botones "Exportar JPG" / "Exportar PDF" en los 5 mapas (seccion 13.1 del contexto de
  mapas).
- Dialogo "Guardar como" (`showSaveFilePicker`, Chrome/Edge) con nombre sugerido
  `deck_<dimension>_<AAAA-MM-DD>`; fallback a descarga normal en Firefox/Safari.
- Captura la vista actual del usuario (no re-centra), con el panel de graficas + leyenda +
  encabezado temporal (titulo + corte + fuente), sobre fondo claro (sin mapa base por CORS).

### 6.2 PENDIENTE confirmado por el usuario
La captura actual NO sale con la ESTRUCTURA del deck. Hoy el export toma el div del mapa
con el panel flotante SUPERPUESTO encima (mapa a pantalla completa + tarjeta arriba-izq),
mientras el deck pide una composicion en columnas:

```
+-----------------------------------------------------------+
| Seccion - Titulo                                          |
+---------------------------+-------------------------------+
| CIFRA GRANDE              |                               |
| periodo / delta %         |        MAPA (coropleta)       |
| mini-serie 2023-2026      |                               |
+---------------------------+-------------------------------+
| Corte - Fuente - Mapa ilustrativo                         |
+-----------------------------------------------------------+
```

### 6.3 Plan propuesto para resolverlo (a implementar)
Para que la lamina salga en la estructura del deck, el export NO debe capturar el mapa
directo, sino construir y capturar una LAMINA HTML dedicada (un contenedor con grid de 2
columnas):
- Al pulsar "Exportar lamina (deck)": generar un div-lamina temporal (fuera de pantalla o
  modal) con: encabezado (seccion + titulo), columna izquierda (cifra grande + periodo +
  delta + mini-serie reutilizando el Chart.js o un SVG), columna derecha = imagen del mapa
  (captura previa del contenedor del mapa con html2canvas), y pie (corte + fuente).
- Capturar ese div-lamina con html2canvas y exportar JPG/PDF (con el dialogo Guardar como
  ya implementado) a `output/deck_output/`.
- Una lamina por dimension; cifras tomadas de los datos de cada mapa (las que ya se
  muestran en el panel). ITT por manzana NO se calcula (decision vigente): la coropleta va
  con la simbologia disponible.

Esto es un cambio de fondo del modo de export (de "captura del mapa" a "lamina compuesta").

---

## 7. PASO A implementado (boton unico "Exportar lamina (deck)")

Estado: HECHO. Se reemplazaron los dos botones (JPG/PDF) por UN solo boton
**"Exportar lamina (deck)"** en los 5 mapas (m, m_full, m_ejec, m_seg, m_eu).

Comportamiento al pulsar (funcion `agregar_export(mapa, titulo, slug)`, identica en ambos
notebooks):
1. Captura solo el div del mapa con html2canvas, ocultando antes: los botones de export,
   `.leaflet-control-layers`, los tiles base (`.leaflet-tile-pane`, fondo claro #F4F6F9 por
   CORS), el panel flotante (#seg-panel/#eu-panel) y el slider de calor
   (#heat-intensity-ctrl); restaura todo despues. Esa imagen es "el mapa".
2. Construye un div temporal `id="deck-lamina"` (1200px, fondo blanco) con la estructura
   del deck:
   - Encabezado: titulo (20px bold) + linea de seccion, borde inferior dorado #8A6D1A.
   - Cuerpo en grid 2 columnas (35% / 65%): izquierda = CLON del panel del mapa
     (#seg-panel/#eu-panel) con sus cifras y serie (se le fuerza `open` en el `<details>` y
     se le quita el position:fixed); derecha = la imagen del mapa.
   - Pie: "Corte: " + fecha/hora + " | Fuente: ITT Ciudad Paraiso - CDO Alcaldia de
     Santiago de Cali | Mapa ilustrativo".
3. Captura `#deck-lamina` con html2canvas (scale 2) -> jsPDF landscape -> guardar con
   showSaveFilePicker (dialogo "Guardar como"; fallback a descarga). Nombre
   `deck_<slug>_<AAAA-MM-DD>.pdf`.
4. Elimina el div-lamina temporal al terminar o ante error.

Notas:
- Las cifras de la columna izquierda salen del panel existente de cada mapa (no se
  recalculan). Si un mapa no tuviera panel, muestra titulo + "Resumen no disponible"
  (en la practica los mapas con panel son seguridad y entorno urbano).
- CORS: la imagen del mapa no incluye el mapa base (tiles); va sobre fondo claro con
  overlays/contorno/manzanas. Decision B vigente.

## 8. Plan por partes (acordado con el usuario)

- **A (HECHO):** boton unico "Exportar lamina (deck)".
- **B (pendiente):** crear el mapa de la dimension que falta -> MOVILIDAD, con
  `06_movilidad_siniestros` (97 puntos) y `07_movilidad_red_peatonal_osm` (400 lineas).
- **C (HECHO para seguridad):** el mapa de seguridad ya consume los datos reales de
  `data/1_data_itt/` (hurto 03, rina 04, spa 05, homicidio 02) como fuente oficial, con
  puntos + heatmap propio por categoria. Reemplazo de `seguridad_unificado.geojson`
  completado. Pendiente: resto de dimensiones conforme existan datos.
- ITT por manzana: NO se calcula por ahora (decision vigente).

## 9. Correccion de la lamina (post-validacion del usuario)

Tras generar el primer PDF (`deck_seguridad_...`), el usuario detecto 2 problemas, ambos
corregidos:
1. **Grafico de tendencia no aparecia** (canvas de Chart.js se clonaba vacio) -> se captura
   el canvas real con `toDataURL` y se inserta como imagen. HECHO y validado por el usuario.
2. **Capas desfasadas y mapa no centrado al imprimir** -> html2canvas renderiza mal las
   capas de Leaflet en zoom fraccional / panes sin asentar. Corregido: `fitBounds` con
   zoom ENTERO (maxZoom 17, animate false), esperar evento `moveend` (fallback 1200ms),
   `invalidateSize()` + margen 350ms antes de capturar. HECHO (pendiente de validacion
   visual final del usuario abriendo el HTML y generando un nuevo PDF).

## 10. Que falta (estado al corte)

- **Paso B (pendiente):** crear el mapa de MOVILIDAD (`06_movilidad_siniestros` 97 puntos +
  `07_movilidad_red_peatonal_osm` 400 lineas) como notebook propio `04_mapa_movilidad.ipynb`,
  replicando estandares (capas base, zoom, mascara, poligono, panel colapsable con serie,
  boton lamina deck, slider de calor, colores Okabe-Ito).
- **Paso C (HECHO para seguridad):** seguridad/convivencia migradas a `data/1_data_itt/`
  (02-05) como fuente oficial, con 4 categorias (hurto, rina, spa, homicidio), cada una con
  puntos (filtrados >=2025-09-01) y heatmap propio (todos los anios) + serie anual.
- **ITT por manzana:** no se calcula por ahora (decision del usuario).
- **Deck PMU completo:** 17 laminas (ver `contexto_deck/contexto_presentacion_itt_ciudad_paraiso.md`).
  Hoy solo se exportan laminas por dimension desde cada mapa; el deck completo multi-lamina
  no esta automatizado.
