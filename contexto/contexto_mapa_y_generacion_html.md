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
- Los eventos de seguridad/ambiente son **sinteticos** hasta integrar los datos reales;
  los popups lo advierten ("Datos de evento SINTETICOS (demo)"). Los indicadores
  catastrales y el avance de caracterizacion SI son reales.

---

## 7. Dimension Seguridad: mapa de calor y serie de tiempo

Seccion 12 del notebook `02_mapa_geoanalitica_itt.ipynb`. Mapa de calor (heatmap)
interactivo de eventos de seguridad con panel colapsable de serie de tiempo.

### 7.1 Datos (reales, DATIC)

- Fuentes crudas en `data/1_Dimension_Seguridad/` (6 GeoJSON, ~11.8 MB): comparendos,
  homicidios y hurtos, cada uno en dos cortes (historico 2023-2026T1 + reciente 2026).
- Unificado en `data/geojson/seguridad_unificado.geojson` (3.34 MB, EPSG:4326):
  - **8.450 eventos** dentro de Ciudad Paraiso, rango **2023-01-01 a 2026-09-30**.
  - Por categoria: **comparendo 7.695, hurto 718, homicidio 37**.
  - Esquema: `fecha, anio, mes (YYYY-MM), categoria, subtipo, sitio, lat, lon, fuente, geometry`.
  - 83 duplicados eliminados; sin columnas PII (nombre/documento/direccion).
- Serie mensual agregada: `data_processed_geo/seguridad_serie_mensual.csv` (periodo,
  categoria, conteo).
- Salida: `data_processed_geo/mapa_seguridad_calor.html` (~11.2 MB; pesa por las capas de
  puntos, que arrancan apagadas).

### 7.2 Heatmap (gradiente por capa, rampas ColorBrewer aptas daltonismo)

- Un `HeatMap` (folium.plugins) por categoria, conmutable. Hurtos activo por defecto.
- Cada capa tiene su **propio gradiente secuencial** (varia en luminosidad dentro de un
  matiz, intenso = oscuro; distinguibles entre si y en escala de grises):
  - Hurtos -> **Blues**: `{0:#eff3ff, 0.4:#9ecae1, 0.7:#4292c6, 1:#08306b}`.
  - Comparendos -> **Greens**: `{0:#edf8e9, 0.4:#a1d99b, 0.7:#41ab5d, 1:#00441b}`.
  - Homicidios -> **Reds**: `{0:#fee5d9, 0.4:#fcae91, 0.7:#fb6a4a, 1:#67000d}`.
  - Coherente con la paleta Okabe-Ito por categoria (azul/verde/rojo).
- Parametros ajustados a la zona compacta (~26 ha): `radius=18`, `blur=14`,
  `min_opacity=0.35`. Solo puntos dentro del poligono.
- Capas de puntos (CircleMarker) por categoria, apagadas por defecto, popups SIN PII
  (homicidios con popup minimo: solo fecha).

### 7.3 Serie de tiempo (panel colapsable)

- Panel flotante HTML inyectado con `get_root().html.add_child(...)`, esquina superior
  izquierda, z-index 9999. Usa `<details>/<summary>` para colapsar.
- **Ancho del panel: `max-width:480px; width:min(480px,46vw)`.**
- Grafico con **Chart.js** (CDN jsdelivr), con degradacion a tabla HTML si no carga.
- Serie **ANUAL** (2023, 2024, 2025, 2026) por categoria.
- **Doble eje Y** por disparidad de magnitudes:
  - Eje izquierdo "Cantidad de casos (hurtos / homicidios)".
  - Eje derecho "Cantidad de comparendos".
  - Nota aclaratoria de doble escala sobre el grafico.
- Canvas en contenedor de altura fija (200px) con `maintainAspectRatio:false` +
  `responsive:true` para aprovechar el ancho sin distorsion.
- Colores de linea Okabe-Ito: hurto=OKI_AZUL, comparendo=OKI_VERDE, homicidio=OKI_BERMELL.
- Totales anuales reales: comparendos 1847/1920/1990/1938; hurtos 257/208/164/89;
  homicidios 16/6/11/4 (2026 parcial hasta septiembre).

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
| `mapa_seguridad_calor.html` | ~11.2 MB |

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
