# Guia de estilo y capas por dimension (mapa de referencia)

Mapa patron: `mapa_html/mapa_seguridad_calor.html` (notebook
`notebooks/02_mapa_geoanalitica_itt.ipynb`, seccion 12). Este documento es la
**plantilla oficial**: cada nueva dimension (movilidad, desarrollo social, entorno
urbano, desarrollo economico, etc.) debe replicar esta configuracion de capas,
controles y estilo. Los mapas de movilidad (`04`) y desarrollo social (`05`) ya
siguen esta guia.

> Regla general: si una dimension nueva no define algo, se toma lo que hace el mapa
> de seguridad. No inventar estilos nuevos salvo el color/semantica propios de la
> dimension.

---

## 1. Objeto base del mapa (Folium)

```python
m = folium.Map(location=centro, zoom_start=16, tiles=None, control_scale=True,
               zoom_snap=0.25, zoom_delta=0.1, max_zoom=22)
m.get_root().width = "100%"
m.get_root().height = "100%"
```

- `tiles=None`: las capas base se agregan manualmente (ver seccion 2).
- `zoom_snap=0.25`, `zoom_delta=0.1`: zoom fraccional de pasos finos (escalas 60/70/80 m).
- `max_zoom=22` en el mapa; los TileLayer usan `max_native_zoom=20` (los tiles se
  escalan mas alla de su resolucion nativa, el zoom no se bloquea en 18).
- **Pantalla completa** (CSS inyectado en el header):

```python
_css_full = ("<style>html,body{height:100%;margin:0;padding:0}"
             ".folium-map{position:absolute;top:0;bottom:0;left:0;right:0;"
             "width:100%;height:100%}</style>")
m.get_root().header.add_child(folium.Element(_css_full))
```

- **Centro:** centroide del poligono de la zona si existe; si no, media de los puntos.
- **Encuadre inicial:** `m.fit_bounds([[3.442445,-76.53259],[3.44791,-76.526004]], padding=(30,30))`.

---

## 2. Capas base (3, conmutables). SIN OpenStreetMap

Orden y estado exactos del mapa de referencia:

| Nombre | tiles | show |
|---|---|---|
| Google Streets | `https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}` | True |
| Esri Satelite | `https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}` | False |
| Google Satelite | `https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}` | False |

Todas con `attr`, `max_zoom=22`, `max_native_zoom=20`. **No usar OpenStreetMap** (no
cargaba de forma fiable).

---

## 3. Mascara oscura (foco en la zona)

Poligono mundial con agujero = la zona de estudio, relleno negro `fillOpacity 0.25`,
`control=False` (no aparece en el LayerControl). Enfoca visualmente dentro de Ciudad
Paraiso y atenua el resto. Codigo identico al de seguridad (celda 39).

---

## 4. Limite oficial de la zona

- Capa `Limite Ciudad Paraiso`, UNICA y ACTIVA al inicio (`show=True`).
- Estilo: `{"color": "#8A6D1A", "weight": 5, "dashArray": "10 6", "fill": False}`
  (borde dorado punteado, sin relleno).
- Fuente: `00_limite_ciudad_paraiso.geojson`.

---

## 5. Capas tematicas: patron PUNTOS + CALOR por categoria

Cada categoria/variable de la dimension genera DOS capas conmutables e
independientes, apagadas al inicio (salvo que la dimension defina una activa):

- **`Puntos: <cat> (<n>)`** - `CircleMarker`, radio 3-4, popup SIN PII.
  - Filtro temporal: solo eventos con `fecha_evento >= 2025-09-01` (foto reciente).
- **`Calor: <cat> (<n>)`** - `HeatMap` (folium.plugins), `radius=18, blur=14,
  min_opacity=0.35`. Usa TODOS los eventos en zona (sin filtro de fecha).

El conteo real `(<n>)` va en el nombre de la capa (puntos = filtrado; calor = total).

### 5.1 Gradiente de calor por categoria (rampas secuenciales, aptas daltonismo)

Cada capa varia en luminosidad dentro de UN matiz (intenso = oscuro), distinguible en
escala de grises. Rampas ColorBrewer usadas en seguridad:

| Categoria | Rampa | Stops |
|---|---|---|
| hurto | Blues | `{0:#eff3ff, 0.4:#9ecae1, 0.7:#4292c6, 1:#08306b}` |
| rina | Greens | `{0:#edf8e9, 0.4:#a1d99b, 0.7:#41ab5d, 1:#00441b}` |
| spa | YlOrBr | `{0:#ffffd4, 0.4:#fed98e, 0.7:#fe9929, 1:#993404}` |
| homicidio | Reds | `{0:#fee5d9, 0.4:#fcae91, 0.7:#fb6a4a, 1:#67000d}` |

Para una dimension nueva: elegir una rampa secuencial coherente con el color
Okabe-Ito de esa variable (ej. movilidad siniestros = Oranges; VIF = Purples).

### 5.2 Color de punto (Okabe-Ito) y contraste de borde

```python
OKI_AZUL="#0072B2"; OKI_NARANJA="#E69F00"; OKI_VERDE="#009E73"
OKI_AMARILLO="#F0E442"; OKI_AZUL_C="#56B4E9"; OKI_BERMELL="#D55E00"
OKI_MORADO="#CC79A7"; OKI_GRIS="#333333"
```

- Relleno = color Okabe-Ito de la categoria, `fill_opacity 0.75`.
- Borde = mismo color, EXCEPTO amarillo (spa) que usa borde gris `#555555` por contraste.

### 5.3 Popups SIN PII

- Fondo `#F4F6F9`, fuente system-ui 12px, bordes redondeados.
- Contenido permitido: categoria, fecha, sitio del hecho (tipo de lugar, NO personal).
- **Homicidios: popup minimo (solo fecha).** Nunca nombre, documento, direccion, sexo,
  edad, placa ni numero de comparendo.

---

## 6. Capas de poligono/superficie (coropleta)

Cuando la variable es agregada por manzana (ej. VIF, deficit, densidad):
- `GeoJson` por manzana con `style_function` que asigna color por valor (rampa
  secuencial), `weight` fino y `fillOpacity ~0.6`.
- Tooltip corto + popup con tabla (valor, densidad, nota de privacidad si aplica).
- **VIF y datos sensibles SIEMPRE como superficie por manzana, nunca puntos.**
- Las manzanas catastrales base (`01_manzanas_itt_consolidado`) van SIN relleno
  (`fill: False`), solo contorno gris `weight 1.0`.

---

## 7. Orden de overlays en el LayerControl

El `LayerControl(collapsed=False, position="topright")` lista los overlays en el
MISMO orden en que se hace `add_to(m)`. Patron del mapa de seguridad (de primero a
ultimo):

1. `Limite Ciudad Paraiso` (activo)
2. `ITT: manzanas (consolidado)`
3. `ITT: estacion Fray Damian` (contorno azul `#0072B2` weight 2.75, sin relleno)
4. `Puntos: <cat>` (una por categoria)
5. `ITT: homicidios <=300m estacion` (si aplica)
6. `Calor: <cat>` (una por categoria)
7. `ITT: demoliciones Cristo Rey` (poligono de fondo, al final)

Regla general: **limite > manzanas > CAI > puntos/eventos > calor > fondo**. Las capas
base (TileLayer) y la mascara van antes y no son overlays conmutables.

### 7.1 Capas transversales del ITT (OBLIGATORIAS en TODAS las dimensiones)

Independiente de la dimension, TODO mapa debe incluir estas 4 capas de contexto del
dataset `data/1_data_itt/`, con el MISMO nombre, estilo y estado que en el mapa de
seguridad (`mapa_seguridad_calor.html`). Son las "capas base del proyecto":

| # | Capa | Fuente | Estilo | show inicial |
|---|---|---|---|---|
| 1 | `Limite Ciudad Paraiso` | `00_limite_ciudad_paraiso.geojson` | borde dorado `#8A6D1A`, weight 5, dashArray "10 6", sin relleno | **True** |
| 2 | `ITT: manzanas (consolidado)` | `01_manzanas_itt_consolidado.geojson` | SIN relleno (`fill:False`), contorno gris `#333333` weight 1.0; tooltip/popup con ID, barrio, manzana y area formateada | False |
| 3 | `ITT: estacion Fray Damian` | `11_estacion_fray_damian_manzana.geojson` | sin relleno, borde azul `#0072B2` weight 2.75 | False |
| 4 | `ITT: demoliciones Cristo Rey` | `10_demoliciones_cristo_rey_predios.geojson` | poligonos clasificados por `demolicion` (Demolido `#D55E00`, Programado `#E69F00`, En proceso `#F0E442`, Sin programar `#009E73`), fillOpacity 0.65; va al FINAL del orden (fondo) | False |

Opcional segun dimension: `ITT: homicidios <=300m estacion`
(`12_estacion_fray_damian_homicidios_300m.geojson`, puntos popup SIN PII) cuando el
tema lo amerite (seguridad).

Capa de referencia adicional (TAMBIEN en todos los mapas, apagada):
`Ref IPM: pobreza por manzana` -> coropleta del IPM recortado a la zona
(`data/geojson/Mzn_ipm_variables.geojson`, 33 manzanas), rampa RdPu, `fillOpacity 0.55`.
Sirve como contexto socioeconomico comun. Codigo: funcion `_add_ipm_ref()` que resuelve
la ruta (local y Colab), recorta a la zona y arma la capa apagada; se agrega al orden
justo despues de `_fg_manzanas`. El mapa dedicado de IPM es `notebooks/08_mapa_ipm.ipynb`.

El codigo de estas capas (funciones `_add_geojson_itt`, `_add_manzanas_itt`,
`_add_demoliciones` y los popups) se reutiliza TAL CUAL del notebook 02 (celda 39);
copiarlo en cada notebook de dimension y agregarlas en el orden de la seccion 7.

> **Estado al corte (HECHO):** `mapa_movilidad.html` (nb 04) y
> `mapa_desarrollo_social.html` (nb 05) ya incluyen las 4 capas transversales (limite,
> manzanas consolidado, estacion Fray Damian, demoliciones Cristo Rey), igualadas al
> mapa de seguridad reutilizando el codigo del notebook 02.

---

## 8. Panel colapsable (resumen + serie de tiempo)

- `<div id="<dim>-panel">` fijo, `top:20px; left:20px`, `z-index:9999`, fondo
  `#F4F6F9`, `max-width:480px; width:min(480px,46vw)`, redondeado, sombra.
- Primera linea: titulo "<Dimension> - resumen" + items con cuadro de color por
  categoria y su total.
- `<details>/<summary>` para colapsar la serie.
- Grafico **Chart.js** (CDN jsdelivr) con **fallback a tabla HTML** si no carga.
- Serie **ANUAL** (2023-2026). Doble eje Y solo si hay disparidad fuerte de magnitudes
  (seguridad: hurto domina ~16x -> hurto al eje derecho, resto al izquierdo). Si las
  magnitudes son comparables, eje unico (movilidad, desarrollo social).
- Canvas en contenedor de altura fija (200px), `maintainAspectRatio:false`,
  `responsive:true`.
- Id del panel por dimension: `#seg-panel`, `#eu-panel`, `#mov-panel`, `#ds-panel`.

---

## 9. Slider de intensidad del calor

- `<div id="heat-intensity-ctrl">` fijo, `bottom:24px; right:24px`, `z-index:9999`.
- `input type=range` min 8, max 40, valor inicial 18. Ajusta en runtime `radius` y
  `blur` (= radius*0.8) de TODAS las heat layers via `setOptions` + `redraw`, sin
  cambiar la definicion base ni los gradientes. No afecta coropletas ni graficas.

---

## 10. Boton unico de exportacion de lamina (deck)

- Funcion `agregar_export(mapa, titulo, slug)` (helper identico en todos los
  notebooks). Debe llamarse ANTES de `mapa.save(...)`.
- Inyecta UN boton `Exportar lamina (deck)` (`id=btndeck_<mapid>`, esquina superior
  derecha). Genera un PDF de una pagina con dialogo "Guardar como"
  (`showSaveFilePicker` + fallback a descarga en Firefox/Safari). Nombre:
  `deck_<slug>_<AAAA-MM-DD>.pdf`.
- Libs por CDN: `html2canvas@1.4.1`, `jspdf@2.5.1`, `chart.js`.
- Al capturar: oculta botones, selector de capas, tiles base (CORS -> fondo claro
  `#F4F6F9`), panel y slider; captura el grafico real del canvas con
  `toDataURL('image/png')` e inserta como `<img>` (clonar el canvas lo copia vacio).
- Alineacion: `fitBounds(ZONA_BOUNDS, {padding:[10,10], maxZoom:17, animate:false})` +
  `once('moveend')` + `invalidateSize()` + delay 350ms (evita el desfase de capas al
  imprimir).
- **Importante:** cada notebook amplia el selector de panel del helper para incluir su
  id (`#seg-panel, #eu-panel, #mov-panel, #ds-panel`).

---

## 11. Checklist para una dimension nueva

1. Entorno uv unico + paleta Okabe-Ito (seccion 5.2).
2. Resolucion de rutas robusta (local + Colab) y poligono de zona.
3. Carga de datos reales desde `data/1_data_itt/` (campo de fecha: `fecha_evento`).
4. Mapa base: 3 TileLayer (seccion 2) + mascara + limite dorado activo.
5. Capas tematicas: puntos (filtrados >=2025-09-01) + calor (todos) por categoria, o
   coropleta por manzana si el dato es agregado/sensible.
6. Capas ITT transversales OBLIGATORIAS (seccion 7.1): Limite (activo), manzanas
   consolidado, estacion Fray Damian y demoliciones Cristo Rey, apagadas salvo el
   limite. Reutilizar el codigo del notebook 02 (celda 39) tal cual.
7. Orden de overlays (seccion 7) y `LayerControl(collapsed=False, position="topright")`.
8. Panel `#<dim>-panel` con resumen + serie anual (Chart.js + fallback).
9. Slider `#heat-intensity-ctrl`.
10. `agregar_export(...)` (ampliar selector de panel) y `m.save(...)` a
    `mapa_html/mapa_<dimension>.html` (variable `MAPAS_DIR`). Los artefactos de datos
    (.geojson/.parquet/.png) van a `data_processed_geo/` (variable `OUT_DIR`).
11. Verificar: ejecutar el notebook con nbconvert (0 celdas con error) y confirmar en
    el HTML que existen las capas, el panel, el slider y el boton de export.
12. Limpiar outputs del notebook (json utf-8 sin BOM, `execution_count=null`) y
    versionar. Agregar la dimension a `notebooks/99_indice_mapas.py`.
