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

### 7.2 Heatmap (paleta INFERNO, apta daltonismo)

- Un `HeatMap` (folium.plugins) por categoria, conmutable. Hurtos activo por defecto.
- Gradiente **INFERNO** (perceptualmente uniforme, apto daltonismo, mejor contraste que
  cividis sobre el mapa): `{0.0:#000004, 0.25:#420a68, 0.5:#932667, 0.75:#dd513a,
  0.9:#fca50a, 1.0:#fcffa4}`.
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
