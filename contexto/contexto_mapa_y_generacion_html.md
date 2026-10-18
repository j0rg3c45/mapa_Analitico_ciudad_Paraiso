# Contexto del Mapa de Geoanalitica ITT y Generacion del HTML

Documento de referencia del notebook `notebooks/02_mapa_geoanalitica_itt.ipynb`:
que produce, con que datos, y COMO se genera el HTML interactivo paso a paso.

> Convenciones del proyecto: entorno unico `uv` (`C:\Users\Jorge\.venv`), codigo sin
> emojis, paleta Okabe-Ito accesible, CRS metrico EPSG:9377 y capa web EPSG:4326,
> notebooks sin outputs, salidas regenerables en `data_processed_geo/` (ignorada por git).

---

## 1. Que produce el notebook

Dos mapas HTML interactivos y autonomos, mas sus datos intermedios, en `data_processed_geo/`:

| Archivo | Que es |
|---|---|
| `mapa_geoanalitica_itt.html` | Mapa ITT: niveles, densidad de delitos, VIF (heatmap) |
| `mapa_avance_caracterizacion.html` | Avance de caracterizacion por manzana y por eje tematico |
| `manzanas_itt.geojson` / `.parquet` | Manzanas con indicadores ITT (WGS84) |
| `avance_caracterizacion_manzana.geojson` / `.parquet` | Agregados de avance por manzana (sin PII) |

La unidad espacial de analisis es la **manzana catastral** (`data/catastral/MANZANAS_U_2024.shp`,
28 manzanas, clave `IDMANZANA`).

---

## 2. Fuentes de datos

- **Catastrales (reales):** `data/catastral/` -> MANZANAS, TERRENOS (857 predios),
  CONSTRUCCION (1346). CRS EPSG:6249. `IDMANZANA` = COMUNA(2)+BARRIO(2)+MANZANA(4)
  (en CONSTRUCCION se deriva porque no la trae).
- **Poligono de zona (real):** `data/geojson/poligono_ciudad_Paraiso.geojson`
  (MAGNA-SIRGAS CMT12, se reproyecta a WGS84).
- **Encuesta (real, PII):** 5 Excel en `data/*.xlsx` (padron, hogares, caracterizacion,
  programas Hogares/Salud/Empresas). Solo entran al mapa como agregados por manzana.
- **Eventos ITT (SINTETICOS, demo):** hurtos, homicidios, rinas, lesionados, siniestros,
  SPA, VIF, arbolado, NDVI. Aislados en una sola celda (`DATOS_SINTETICOS = True`).

---

## 3. Estructura del notebook (35 celdas)

| Seccion | Contenido |
|---|---|
| 1 | Entorno e imports + paleta Okabe-Ito (constantes de color, `NIVEL_COLORS`, `EVENTO_COLORS`) |
| 2 | Resolucion de rutas (local + Colab) y carga de capas catastrales |
| 3 | Indicadores reales por manzana (predios, construcciones, pisos, area, densidad) |
| 4 | Eventos ITT PLACEHOLDER (sinteticos) |
| 5 | Indice ITT (5 dimensiones) y clasificacion en 4 niveles |
| 6 | Exporta `manzanas_itt.geojson` / `.parquet` |
| 7 | Funciones de popup enriquecido (HTML/CSS + mini-graficas SVG) |
| 8 | Construccion del mapa ITT con Folium |
| 9 | Leyenda, LayerControl y `m.save(...)` del HTML ITT |
| 10 | Resumen analitico ITT |
| 11a-11f | Avance de caracterizacion por manzana: carga, geolocalizacion, agregacion por eje, exportacion, mapa `m_av.save(...)` y resumen |

---

## 4. Como se genera el HTML, en detalle

El HTML se construye con **Folium** (que envuelve Leaflet.js). Folium arma un documento
HTML autonomo con el JS/CSS de Leaflet embebido y los datos (GeoJSON) inline, de modo que
el `.html` resultante abre en cualquier navegador sin servidor ni dependencias externas
(salvo los tiles de los mapas base, que se cargan por internet).

### Paso 1 - Reproyectar a WGS84 (EPSG:4326)

Leaflet trabaja en lat/lon WGS84. Todo lo que se dibuja se reproyecta antes:

```python
mz_web = mz.to_crs(CRS_WEB)          # manzanas con indicadores, 4326
POLIGONO_ZONA = gpd.read_file(ruta).to_crs(CRS_WEB)
```

### Paso 2 - Crear el mapa SIN tiles por defecto

Se crea el `folium.Map` con `tiles=None` para controlar manualmente las capas base y que
el mapa arranque limpio:

```python
centro = [mz_web.geometry.union_all().centroid.y, mz_web.geometry.union_all().centroid.x]
m = folium.Map(location=centro, zoom_start=16, tiles=None, control_scale=True)
```

### Paso 3 - Agregar las capas base conmutables

Tres capas base (OpenStreetMap fue retirado porque no cargaba). Google Streets queda
activa por defecto (`show=True`); las demas apagadas:

```python
folium.TileLayer(tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                 attr="Google", name="Google Streets", show=True).add_to(m)
folium.TileLayer("https://server.arcgisonline.com/.../World_Imagery/MapServer/tile/{z}/{y}/{x}",
                 attr="Esri", name="Esri Satelite", show=False).add_to(m)
folium.TileLayer(tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
                 attr="Google", name="Google Satelite", show=False).add_to(m)
```

### Paso 4 - Agregar capas de datos como FeatureGroup

Cada capa tematica es un `folium.FeatureGroup` (para que aparezca conmutable en el
control). Solo el contorno y el poligono arrancan visibles; el resto `show=False`:

- **Poligono Ciudad Paraiso:** `folium.GeoJson` con borde oscuro grueso punteado
  (`color="#8A6D1A", weight=5, dashArray="10 6", fill=False`).
- **Contorno territorial:** bordes de las manzanas sin relleno.
- **Coropleta ITT (nivel):** una `folium.GeoJson` por manzana, rellena con el color
  pastel del nivel y borde del color saturado; popup enriquecido y tooltip.
- **Hurtos (densidad por manzana):** coropleta en gradiente azul segun el conteo; popup
  con diagrama de torta (composicion de delitos) + tabla T0/porcentaje/variacion.
- **VIF (mapa de calor):** `folium.plugins.HeatMap` con pesos por manzana. Nunca puntos
  individuales (privacidad / no re-identificacion).

Patron de una coropleta por manzana:

```python
fg = folium.FeatureGroup(name="Coropleta ITT (nivel)", show=False)
for _, r in mz_web.iterrows():
    folium.GeoJson(
        r["geometry"].__geo_interface__,
        style_function=lambda f, c=color_pastel, b=color_borde: {
            "fillColor": c, "color": b, "weight": 1.5, "fillOpacity": 0.7},
        popup=folium.Popup(popup_html(r), max_width=280),
        tooltip=f'Manzana {r["MANZANA"]} - {r["nivel"]}',
    ).add_to(fg)
fg.add_to(m)
```

### Paso 5 - Popups enriquecidos (HTML/CSS + SVG inline)

Los popups son cadenas HTML construidas en Python. Las mini-graficas (barras y torta) se
dibujan como **SVG inline** (sin JS ni librerias de grafico en el popup):

- `svg_barras(valores, colores, ...)` -> barras comparativas por eje/evento.
- `svg_torta(valores, colores, ...)` -> torta de composicion de delitos (usa `math`
  para los angulos; por eso el notebook importa `math`).
- `pct_var(t0, t1)` -> variacion porcentual T0 vs T-1.

El HTML del popup usa la paleta Okabe-Ito y fondo `#F4F6F9`, con tabla de datos.

### Paso 6 - Leyenda flotante

La leyenda es un bloque HTML fijo que se inyecta en la raiz del documento:

```python
m.get_root().html.add_child(folium.Element(legend_html))
```

Explica los colores de nivel ITT y las convenciones (ej. borde punteado = ubicacion
mayoritariamente aproximada en el mapa de avance).

### Paso 7 - Control de capas y guardado

Al final se agrega el `LayerControl` (permite prender/apagar bases y capas tematicas) y
se escribe el archivo HTML:

```python
folium.LayerControl(collapsed=False, position="topright").add_to(m)
html_path = os.path.join(OUT_DIR, "mapa_geoanalitica_itt.html")
m.save(html_path)      # escribe el HTML autonomo
m                       # en Jupyter/Colab, muestra el mapa inline
```

El mapa de avance (`m_av`) sigue el mismo patron y termina en
`m_av.save("mapa_avance_caracterizacion.html")`.

---

## 5. Como ejecutar y regenerar los HTML

Con el entorno unico (no crear entornos nuevos):

```powershell
# Abrir el notebook en JupyterLab
& "C:\Users\Jorge\.venv\Scripts\python.exe" -m jupyterlab

# O regenerar los HTML sin abrir Jupyter (ejecuta todas las celdas)
cd notebooks
& "C:\Users\Jorge\.venv\Scripts\python.exe" -m jupyter nbconvert `
    --to notebook --execute --output _tmp.ipynb 02_mapa_geoanalitica_itt.ipynb
Remove-Item _tmp.ipynb
```

Dependencias (ya instaladas en el entorno unico): geopandas, folium, pyarrow, pandas,
numpy, openpyxl, nbconvert.

En Colab: montar Drive o subir los shapefiles; definir `CATASTRAL_DIR` / `POLIGONO_ZONA`
si hace falta. La celda 2 resuelve ambas rutas (local y Colab).

Los HTML quedan en `data_processed_geo/` (NO versionada: son salidas regenerables y
pueden derivarse de datos con PII).

---

## 6. Notas de privacidad y datos

- En el mapa solo hay **agregados por manzana**, nunca puntos de personas.
- VIF se representa como superficie (HeatMap), nunca como punto individual.
- La dimension Seguridad usa **datos reales** de `data/1_data_itt/` (ver seccion 7). Los
  popups de homicidios no exponen PII (solo fecha). Los indicadores catastrales y el avance
  de caracterizacion tambien son reales.

---

## 7. Dimension Seguridad: mapa de calor y serie de tiempo

Seccion 12 del notebook `02_mapa_geoanalitica_itt.ipynb`. Mapa de calor (heatmap)
interactivo de eventos de seguridad con panel colapsable de serie de tiempo.

### 7.1 Datos (reales, dataset oficial `data/1_data_itt/`)

- **Fuente oficial (vigente):** las 4 capas tematicas de `data/1_data_itt/` (reemplaza al
  antiguo `seguridad_unificado.geojson` y a los eventos sinteticos). Campo de fecha:
  `fecha_evento`. `data/1_data_itt/` NO se versiona (gitignore) por PII en homicidios.
  - `03_seguridad_hurtos.geojson` -> **hurto: 722** eventos.
  - `04_convivencia_rinas.geojson` -> **rina: 253** eventos.
  - `05_convivencia_spa.geojson` -> **spa: 350** eventos.
  - `02_seguridad_homicidios.geojson` -> **homicidio: 37** eventos.
- Rango temporal **2023-2026** (2026 parcial hasta septiembre).
- Salida: `data_processed_geo/mapa_seguridad_calor.html` (~1.27 MB; ignorada por git).

### 7.2 Capas por categoria (puntos + heatmap propio, aptas daltonismo)

- **4 categorias**, cada una con su capa de **puntos** ("Puntos: <cat>") y su capa de
  **calor** ("Calor: <cat>") conmutables de forma independiente en el LayerControl.
- Cada categoria tiene su **propio gradiente secuencial** (ColorBrewer, intenso = oscuro;
  distinguibles entre si y en escala de grises), coherente con Okabe-Ito:
  - Hurto -> **Blues** (`#0072B2`).
  - Rina -> **Greens** (`#009E73`).
  - Spa -> **YlOrBr** (`#F0E442`).
  - Homicidio -> **Reds** (`#D55E00`).
- **Puntos (CircleMarker):** filtrados a **`fecha_evento >= 2025-09-01`** (foto reciente).
  Conteos filtrados: hurto **136**, rina **68**, spa **200**, homicidio **6**. Popups SIN
  PII (homicidios: solo fecha).
- **Heatmap:** usa TODOS los eventos (sin filtro de fecha). Solo puntos dentro del
  poligono. Slider de intensidad del calor en el panel.

### 7.3 Serie de tiempo (panel colapsable)

- Panel flotante HTML inyectado con `get_root().html.add_child(...)`, esquina superior
  izquierda, z-index 9999. Usa `<details>/<summary>` para colapsar.
- **Ancho del panel: `max-width:480px; width:min(480px,46vw)`.**
- Grafico con **Chart.js** (CDN jsdelivr), con degradacion a tabla HTML si no carga.
- Serie **ANUAL** (2023, 2024, 2025, 2026) por categoria, usando TODOS los eventos.
- **Doble eje Y** por disparidad de magnitudes (hurto domina ~16x):
  - Eje izquierdo "Cantidad de casos (hurto)".
  - Eje derecho "Cantidad de casos (rina / spa / homicidio)".
  - Nota aclaratoria de doble escala sobre el grafico.
- Canvas en contenedor de altura fija (200px) con `maintainAspectRatio:false` +
  `responsive:true` para aprovechar el ancho sin distorsion.
- Colores de linea Okabe-Ito por categoria (azul/verde/amarillo/bermellon).
- Totales anuales reales (2026 parcial hasta septiembre):
  - hurto: **260 / 209 / 164 / 89**.
  - rina: **29 / 61 / 114 / 49**.
  - spa: **66 / 28 / 121 / 135**.
  - homicidio: **16 / 6 / 11 / 4**.

### 7.4 Parametros comunes de los 3 mapas (ITT, avance, seguridad)

- Capas base: Google Streets (activa), Esri Satelite, Google Satelite. **Sin OpenStreetMap**
  (no cargaba de forma fiable).
- **Zoom:** `zoom_start=16`, `zoom_snap=0.25`, `zoom_delta=0.5` (zoom fraccional, pasos
  finos). Tiles con `max_zoom=22`, `max_native_zoom=20` (los tiles se escalan mas alla de
  su resolucion nativa; el zoom ya no se bloquea en nivel 18).
- Poligono de Ciudad Paraiso: borde `#8A6D1A`, weight 5, dashArray "10 6", sin relleno.
- Mapa de seguridad a pantalla completa (CSS: contenedor 100% de la ventana) + mascara
  oscura (fillOpacity 0.25) fuera de la zona para enfocar.

### 7.5 Tamanios de los HTML generados (data_processed_geo/, ignorada por git)

| Archivo | Tamano |
|---|---|
| `mapa_geoanalitica_itt.html` | ~1.79 MB |
| `mapa_avance_caracterizacion.html` | ~2.61 MB |
| `mapa_avance_caracterizacion_ejecutivo.html` | ~2.59 MB |
| `mapa_seguridad_calor.html` | ~1.27 MB |

---

## 8. Dimension Entorno Urbano: mapa dedicado (NDVI, deficit, arboles)

Notebook propio `notebooks/03_mapa_entorno_urbano.ipynb` (mapa separado, no se integra al
ITT por naturaleza visual distinta de las capas y para no sobrecargar un solo HTML).
Requiere `rasterio` (instalado en el entorno unico con `uv pip install --python
C:\Users\Jorge\.venv\Scripts\python.exe rasterio`).

### 8.1 Datos (reales, en `data/5_Dimension_Entorno_Urbano/`)

- **NDVI**: 4 rasters anuales `ciudad_Paraiso_ndvi/ciudad_Paraiso_ndvi_YYYY.tif`
  (2023-2026, 74x61 px, WGS84). NDVI promedio: 2023=0.095, 2024=0.110, 2025=0.110,
  2026=0.099 (bajo, zona urbana densa). Cobertura espacial reducida (nucleo de la zona).
- **Censo arboreo**: `CENSO_ARBOREO_ciudad_Paraiso.geojson` (312 puntos, comuna 3).
  Estados: Nuevo 170, Vivo 133, Muerto 7, Eliminado 2.
- **Deficit habitacional**: `sec_vivienda/DEF_HAB_SISBEN.shp` (386 poligonos SISBEN,
  EPSG:6249). Campo mapeado `F_HOG_DE_1` = deficit habitacional total (cuantitativo +
  cualitativo). % deficit: min 0, promedio 44.5, max 100. 6 poligonos con T_HOG=0.
- **PII - NO versionar**: `sec_vivienda/*SUBSIDIOS*.xlsx` contiene nombre, cedula y
  direccion de beneficiarios. Excluido en `.gitignore`.

### 8.2 Capas del mapa (colores accesibles daltonismo)

- **NDVI por anio** como `folium.raster_layers.ImageOverlay` (PNG RGBA generados en
  `data_processed_geo/ndvi_YYYY.png`), conmutable, 2026 activo. Rampa secuencial VERDE
  ColorBrewer Greens `{0:#edf8e9, 0.4:#a1d99b, 0.7:#41ab5d, 1:#00441b}`, normalizada a
  rango fijo NDVI 0..0.6, nodata transparente.
- **Deficit habitacional** como coropleta de los 386 poligonos. Rampa secuencial MORADA
  ColorBrewer Purples `{0:#f2f0f7, 0.5:#9e9ac8, 1:#54278f}`. Regla **MIN_N=5**:
  poligonos con T_HOG<5 (o =0) en gris, popup solo con conteo.
- **Censo arboreo**: `CircleMarker` por estado (verde Okabe-Ito #009E73 vivos/nuevos,
  gris #333333 muertos/eliminados) + capa `HeatMap` de densidad (gradiente Greens).
- Panel colapsable (max-width 480px, Chart.js) con serie anual del NDVI promedio y
  resumen de arboles por estado.
- Mismos estandares comunes (ver 7.4): capas base sin OSM, zoom fraccional, max_zoom=22,
  poligono dorado, mascara de foco, pantalla completa.

### 8.3 Tamanios (data_processed_geo/, ignorada por git)

| Archivo | Tamano |
|---|---|
| `mapa_entorno_urbano.html` | ~7.31 MB |
| `ndvi_2023.png` .. `ndvi_2026.png` | ~0.01 MB c/u |

---

## 9. Estado de los mapas del proyecto (resumen)

Cuatro mapas por proposito, misma arquitectura Folium + estandares comunes:

| Mapa | Notebook | Datos | HTML |
|---|---|---|---|
| Geoanalitica ITT | `02_...itt.ipynb` sec. 5-10 | catastral real + eventos sinteticos | `mapa_geoanalitica_itt.html` ~1.8 MB |
| Avance caracterizacion | `02_...itt.ipynb` sec. 11 | encuesta real (501 ciudadanos) | `mapa_avance_caracterizacion[_ejecutivo].html` ~2.6 MB |
| Seguridad (calor) | `02_...itt.ipynb` sec. 12 | DATIC real (8450 eventos) | `mapa_seguridad_calor.html` ~11 MB |
| Entorno Urbano | `03_mapa_entorno_urbano.ipynb` | NDVI + arboles + deficit reales | `mapa_entorno_urbano.html` ~7.3 MB |

Pendiente: proceso del deck PMU (ver `contexto_deck_reporte_pmu.md`); otras dimensiones
del ITT (movilidad, desarrollo economico, desarrollo social) si llegan sus datos.

---

## 10. Dataset ITT consolidado (`data/1_data_itt/`)

Dataset definitivo y consolidado del ITT, 13 capas GeoJSON numeradas por dimension, TODAS
en **EPSG:4326**. Es la fuente de verdad mas completa y organizada del proyecto; sustituye
a los insumos dispersos usados antes. Prefijo numerico = orden/dimension.

| Archivo | n | Geometria | Contenido |
|---|---|---|---|
| `00_limite_ciudad_paraiso.geojson` | 1 | MultiPolygon | Limite/poligono de la zona |
| `01_manzanas_itt_consolidado.geojson` | 28 | Polygon | Manzanas con ITT, nivel y scores por dimension |
| `02_seguridad_homicidios.geojson` | 37 | Point | Homicidios (trae PII: direccion, sexo, edad, ocupacion) |
| `03_seguridad_hurtos.geojson` | 722 | Point | Hurtos (dinamica, modalidad, titulo) |
| `04_convivencia_rinas.geojson` | 253 | Point | Comparendos por rinas |
| `05_convivencia_spa.geojson` | 350 | Point | Comparendos por sustancias psicoactivas |
| `06_movilidad_siniestros.geojson` | 97 | Point | Siniestros viales (clase, placas, vehiculos) |
| `07_movilidad_red_peatonal_osm.geojson` | 400 | LineString | Red peatonal (OSM: name, highway, length) |
| `08_entorno_censo_arboreo.geojson` | 312 | Point | Censo arboreo (estado, especie) |
| `09_seguridad_vif_calor_poligonal.geojson` | 28 | Polygon | VIF agregada por manzana (vif_casos, vif_densidad_ha, nota_privacidad) - sin puntos |
| `10_demoliciones_cristo_rey_predios.geojson` | 100 | Polygon | Predios en plan de demolicion (NPN, fecha, estado, cronograma) |
| `11_estacion_fray_damian_manzana.geojson` | 1 | Polygon | Manzana de la estacion de policia Fray Damian |
| `12_estacion_fray_damian_homicidios_300m.geojson` | 17 | Point | Homicidios a <=300 m de la estacion (dist_a_estacion_m) |

### 10.1 Capa clave: `01_manzanas_itt_consolidado`

Columnas analiticas: `idmanzana`, `comuna`, `barrio`, `manzana`,
`manzana_plan_cristorey`, `anio_referencia`, `itt`, `nivel`, y scores por dimension:
`score_seguridad`, `score_movilidad`, `score_des_social`, `score_entorno_u`,
`score_des_eco`, `nota`.

**Estado actual (importante):** el `itt` viene en **58.5 para las 28 manzanas** (valor
unico de zona, nivel "Consolidacion") y los `score_*` por dimension estan **vacios
(None)**. Es decir, la estructura esta lista pero el ITT por manzana y los scores por
dimension estan PENDIENTES de calcular/poblar.

### 10.2 Dimensiones del ITT representadas

Seguridad (homicidios, hurtos, VIF), Convivencia (rinas, SPA), Movilidad (siniestros, red
peatonal), Entorno urbano (censo arboreo). Mas capas de contexto operativo: demoliciones
Cristo Rey y estacion de policia Fray Damian (con homicidios en radio de 300 m).

### 10.3 Nota de privacidad (PII)

- `02_seguridad_homicidios` y `12_..._homicidios_300m` traen atributos personales
  (direccion, sexo, edad, ocupacion). En cualquier mapa publicable, los homicidios deben
  ir SIN esos campos en popups (solo fecha/tipo), o agregados.
- VIF ya viene agregada por manzana (`09_...vif_calor_poligonal`), nunca como punto.
- Evaluar que capas de `data/1_data_itt/` se versionan vs se ignoran segun contengan PII.

### 10.4 Estructura de la carpeta (arbol)

```
data/1_data_itt/
├── 00_limite_ciudad_paraiso.geojson                 0.9 KB  · 1 MultiPolygon  · limite de la zona
├── 01_manzanas_itt_consolidado.geojson              161 KB  · 28 Polygon      · ITT + scores por dimension
├── 02_seguridad_homicidios.geojson                  117 KB  · 37 Point        · homicidios (con PII)
├── 03_seguridad_hurtos.geojson                     1009 KB  · 722 Point       · hurtos
├── 04_convivencia_rinas.geojson                     464 KB  · 253 Point       · comparendos rinas
├── 05_convivencia_spa.geojson                       718 KB  · 350 Point       · comparendos SPA
├── 06_movilidad_siniestros.geojson                   95 KB  · 97 Point        · siniestros viales
├── 07_movilidad_red_peatonal_osm.geojson            116 KB  · 400 LineString  · red peatonal (OSM)
├── 08_entorno_censo_arboreo.geojson                 167 KB  · 312 Point       · censo arboreo
├── 09_seguridad_vif_calor_poligonal.geojson         152 KB  · 28 Polygon      · VIF agregada por manzana
├── 10_demoliciones_cristo_rey_predios.geojson       146 KB  · 100 Polygon     · predios en demolicion
├── 11_estacion_fray_damian_manzana.geojson          2.9 KB  · 1 Polygon       · manzana estacion de policia
└── 12_estacion_fray_damian_homicidios_300m.geojson   50 KB  · 17 Point        · homicidios a <=300m de la estacion
```

### 10.5 Organizacion por dimension

- **Base / territorio:** `00` limite de la zona, `01` manzanas con ITT consolidado.
- **Seguridad:** `02` homicidios, `03` hurtos, `09` VIF (agregada por manzana).
- **Convivencia:** `04` rinas, `05` SPA.
- **Movilidad:** `06` siniestros viales, `07` red peatonal (OSM).
- **Entorno urbano:** `08` censo arboreo.
- **Contexto operativo (no son dimensiones del ITT, son capas de apoyo):**
  `10` demoliciones Cristo Rey, `11` manzana de la estacion Fray Damian,
  `12` homicidios en radio de 300 m de la estacion.

---

## 11. Capas del dataset ITT en los mapas y ajustes de simbologia

A los 2 mapas activos (seguridad `notebooks/02` celda del mapa de seguridad, y entorno
urbano `notebooks/03`) se agregaron capas del dataset `data/1_data_itt/`, conmutables y
apagadas al inicio, resolviendo ruta local y Colab.

> Nota: `data/1_data_itt/` NO se versiona por ahora (ver `.gitignore`): es la data
> original en uso local y contiene PII de homicidios. Se cargara al repo depurada mas
> adelante. Primero se organizan mapas y contexto.

### 11.1 Capas agregadas y su simbologia

- **Limite Ciudad Paraiso** (`00`): UNICO limite oficial. Estilo homologado del poligono
  anterior (dorado #8A6D1A, weight 5, dashArray "10 6", sin relleno). Se elimino la capa
  duplicada "Poligono Ciudad Paraiso" (antes existia doble contorno).
- **ITT: manzanas (consolidado)** (`01`): coropleta neutra azul claro. Tooltip y popup con
  4 atributos: ID Manzana, Barrio, Manzana y Area. El area se recalcula en EPSG:9377 y se
  formatea entera con separador de miles en punto (ej. "6.090 m2"). `GeoJsonTooltip` con
  alias y `localize=True`.
- **ITT: demoliciones Cristo Rey** (`10`): clasificada por la columna `demolicion` con
  colores Okabe-Ito, fillOpacity 0.65, borde #333333 weight 0.8, estado en tooltip y
  popup. Categorias: Demolido=#D55E00, Programado=#E69F00, En proceso=#F0E442,
  Sin demolicion programada=#009E73.
- **ITT: estacion Fray Damian** (`11`): solo contorno (fill=False), weight 3.5, azul
  #0072B2.
- **ITT: homicidios <=300m estacion** (`12`): puntos con popup SIN PII (solo fecha,
  distancia, tipo de arma, movil).

### 11.2 Notas tecnicas

- Las capas con columnas de fecha (Timestamp) se convierten a texto antes de
  `to_json()`/popup (folium no serializa Timestamp).
- Estado del ITT en `01`: valor 58.5 uniforme y scores por dimension vacios (None); la
  coropleta es neutra hasta calcular el ITT real por manzana (pendiente de fondo).
- Metodologia del ITT documentada aparte en `contexto/contexto_itt_ciudad_paraiso.md`
  (zona, pesos por dimension, verificacion espacial point-in-polygon).

---

## 12. Orden de capas en el LayerControl (ambos mapas)

Las capas del control se ordenan segun el orden en que se hace `.add_to(mapa)` (Folium las
lista en ese mismo orden). Para controlarlo, las funciones que crean capas (`_add_geojson_itt`,
`_add_manzanas_itt`, `_add_demoliciones`) RETORNAN su FeatureGroup y al final se agregan en
una lista ordenada. Solo el limite queda activo (`show=True`); el resto `show=False`.

Orden definido (de primera a ultima en el panel):

**Mapa seguridad (`m_seg`):**
1. Limite Ciudad Paraiso (activo)
2. ITT: manzanas (consolidado)
3. ITT: estacion Fray Damian (CAI de policia)
4-7. Puntos: hurto, rina, spa, homicidio (+ homicidios <=300m estacion)
8-11. Calor: hurto, rina, spa, homicidio
12. ITT: demoliciones Cristo Rey (poligono de fondo)

**Mapa entorno urbano (`m_eu`):**
1. Limite Ciudad Paraiso (activo)
2. ITT: manzanas (consolidado)
3. ITT: estacion Fray Damian
4-6. Arboles (censo), Arboles (densidad/calor), homicidios <=300m estacion
7-10. NDVI 2023, 2024, 2025, 2026
11-12. Deficit habitacional, ITT: demoliciones Cristo Rey

Regla general del orden: limite > manzanas > CAI > puntos/eventos > NDVI > deficit/fondo.
Las capas base (TileLayer) y la mascara oscura van antes y no son overlays conmutables.

---

## 13. Interactividad, export y simbologia (estado consolidado de los mapas)

Resumen de los ajustes de visualizacion aplicados a los mapas (principalmente seguridad
`m_seg` y entorno urbano `m_eu`; los de ITT/avance comparten la base comun).

### 13.1 Exportacion de laminas (boton unico "Exportar lamina (deck)")
- Funcion reutilizable `agregar_export(mapa, titulo, slug)` en ambos notebooks. **Un solo
  boton "Exportar lamina (deck)"** (esquina superior derecha) que genera un PDF con dialogo
  "Guardar como" (`showSaveFilePicker` + fallback a descarga en Firefox/Safari). Librerias
  html2canvas@1.4.1 y jsPDF@2.5.1 por CDN. Una lamina por dimension. Nombre sugerido:
  `ITT_<slug>_<AAAA-MM-DD>`.
- El grafico de tendencia se captura como imagen real del canvas (`toDataURL('image/png')`
  + `replaceChild`), porque clonar el canvas lo copia vacio.
- Alineacion de capas en la lamina: `fitBounds(ZONA_BOUNDS, {padding:[10,10], maxZoom:17,
  animate:false})` + `once('moveend')` + `invalidateSize()` + delay 350ms (evita el
  desplazamiento de overlays al imprimir).
- **Captura la VISTA ACTUAL** del usuario: NO re-centra con fitBounds (se elimino la
  llamada a `ajustarZona`). El encuadre/zoom/capas que el usuario deja en pantalla es lo
  que se descarga.
- Durante la captura: se ocultan los botones de export, el selector de capas
  (`.leaflet-control-layers`) y los tiles base; se pinta fondo claro #F4F6F9; se inserta un
  encabezado temporal (titulo + "Corte: fecha" + "Fuente: ITT Ciudad Paraiso - CDO
  Alcaldia de Santiago de Cali"); se restaura todo despues.
- El panel de graficas de tendencia SI sale en la lamina (no se oculta).
- Limitacion (decision B): el mapa base (Google/Esri) NO sale en la lamina por CORS; la
  captura va sobre fondo claro con overlays + panel + leyenda. Para mapa base real haria
  falta OSM-con-CORS o render desde Python.

### 13.2 Zoom
- `zoom_start=16`, `zoom_snap=0.25`, `zoom_delta=0.1` (pasos finos para escalas
  intermedias 60/70/80/90 m), `max_zoom=22`, tiles `max_native_zoom=20`.
- Los mapas inician con `fit_bounds` al poligono de Ciudad Paraiso
  `[[3.442445,-76.53259],[3.44791,-76.526004]]` con padding (30,30).

### 13.3 Simbologia estandar
- **Limite Ciudad Paraiso**: unico, borde #8A6D1A, weight 5, dashArray "10 6", sin
  relleno; unica capa activa al inicio.
- **ITT: manzanas (consolidado)**: SIN relleno (`fill: False`), solo contorno gris
  weight 1.0 (se quito el relleno azul pastel).
- **Estacion Fray Damian**: sin relleno, borde azul #0072B2 continuo weight 2.75.
- **Demoliciones Cristo Rey**: clasificadas por `demolicion` (Demolido=#D55E00,
  Programado=#E69F00, En proceso=#F0E442, Sin programar=#009E73), fillOpacity 0.65.

### 13.4 Slider de intensidad del heatmap
- Control deslizante "Intensidad del calor" (esquina inferior derecha) en los mapas con
  HeatMap (seguridad y entorno urbano). Ajusta en runtime el radius/blur de las capas de
  calor via `setOptions`, SIN cambiar la definicion base (seguridad radius=18/blur=14;
  entorno radius=22/blur=16) ni los gradientes. Valor inicial del slider: 18 (seguridad),
  22 (entorno). Afecta todas las heat layers a la vez; no afecta coropletas ni graficas.

### 13.5 Filtro temporal de la capa de PUNTOS (solo seguridad)
- Las capas "Puntos: hurto/rina/spa/homicidio" muestran SOLO eventos con `fecha_evento`
  >= 2025-09-01 (2026 + desde septiembre 2025): hurto 136, rina 68, spa 200, homicidio 6.
- Los **mapas de calor** (HeatMap) y las **graficas de tendencia** NO se filtran: siguen
  usando todos los eventos (hurto 722, rina 253, spa 350, homicidio 37; 2023-2026).

### 13.6 Panel de graficas
- Posicion top:20px left:20px, fondo claro, redondeado, colapsable (`<details>`).
  Seguridad: #seg-panel ("Seguridad - resumen", series anual doble eje con Chart.js).
  Entorno urbano: #eu-panel (serie NDVI anual).
  Movilidad: #mov-panel (serie anual de siniestros por severidad, eje unico).
  Desarrollo social: #ds-panel (serie anual de rinas y spa, eje unico).
- El helper de export (`agregar_export`) oculta/clona el panel por id; cada notebook amplia
  el selector para incluir su panel (`#seg-panel, #eu-panel, #mov-panel, #ds-panel`).

---

## 14. Dimension Movilidad (notebook 04)

Notebook `notebooks/04_mapa_movilidad.ipynb`. Mapa de la dimension Movilidad del ITT
(peso 22%) con datos reales de `data/1_data_itt/`. Salida:
`data_processed_geo/mapa_movilidad.html` (~0.9 MB, ignorada por git).

### 14.1 Datos
- `06_movilidad_siniestros.geojson` (97 puntos): siniestros viales con campo
  `clasificacion_severidad` (lesionados 81, mortal 8, solo_danos 8), `clase_acci` y
  `fecha_evento` (2023-2026).
- `07_movilidad_red_peatonal_osm.geojson` (400 lineas, OSM): red peatonal con `highway` y
  `length`; longitud total en zona ~21.6 km.

### 14.2 Capas
- **Puntos de siniestros por severidad** (CircleMarker): mortales (bermellon, radio 6,
  ACTIVA al inicio), lesionados (naranja), solo danos (azul claro). Popup SIN PII (fecha +
  clase). Filtrados a `fecha_evento >= 2025-09-01`.
- **Calor: siniestros** (HeatMap, rampa Oranges): usa TODOS los siniestros en zona.
- **Red peatonal (OSM)**: lineas coloreadas por tipo de via (footway/pedestrian/
  residential/service/tertiary/secondary/primary), Okabe-Ito.
- **Capas transversales ITT** (apagadas, salvo el limite): Limite Ciudad Paraiso (activo),
  ITT manzanas (consolidado), ITT estacion Fray Damian, ITT demoliciones Cristo Rey.
- Comparte: capas base Google, mascara oscura, panel #mov-panel (serie anual
  por severidad, eje unico), slider de calor, boton "Exportar lamina (deck)".

## 15. Dimension Desarrollo Social / Convivencia (notebook 05)

Notebook `notebooks/05_mapa_desarrollo_social.ipynb`. UN solo mapa que integra las tres
variables de la dimension (peso 19%: VIF + rinas + SPA). Salida:
`data_processed_geo/mapa_desarrollo_social.html` (~0.6 MB, ignorada por git).

### 15.1 Datos
- `09_seguridad_vif_calor_poligonal.geojson` (28 manzanas): VIF agregado por manzana
  (`vif_casos`, `vif_densidad_ha`). 34 casos en 18 manzanas. NUNCA puntos (regla de
  privacidad VIF del proyecto).
- `04_convivencia_rinas.geojson` (253) y `05_convivencia_spa.geojson` (350): puntos con
  `fecha_evento`.

### 15.2 Capas
- **VIF: densidad por manzana** (coropleta, rampa Purples por densidad de casos/ha, borde
  morado). ACTIVA al inicio. Popup con casos, densidad y nota de privacidad.
- **Puntos: rina / spa** (CircleMarker, verde / amarillo) filtrados a
  `fecha_evento >= 2025-09-01`. Popup SIN PII (fecha + sitio del hecho).
- **Calor: rina / spa** (HeatMap, rampas Greens / YlOrBr): usan TODOS los eventos en zona.
- **Capas transversales ITT** (apagadas, salvo el limite): Limite Ciudad Paraiso (activo),
  ITT manzanas (consolidado), ITT estacion Fray Damian, ITT demoliciones Cristo Rey.
- Comparte: capas base Google, mascara oscura, panel #ds-panel (serie anual
  de rinas y spa, eje unico), slider de calor, boton "Exportar lamina (deck)".

> Nota: rinas y SPA tambien aparecen en el mapa de seguridad (notebook 02) como foto de
> convivencia; aqui se agrupan con VIF segun la composicion metodologica del ITT
> (Desarrollo Social = VIF + rinas + SPA).
