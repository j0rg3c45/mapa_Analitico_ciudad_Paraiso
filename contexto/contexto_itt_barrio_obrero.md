# Índice de Transformación Territorial (ITT) e IPM — Barrio Obrero

Documento de contexto del trabajo de geoanalítica para **Barrio Obrero** (Comuna 9, Cali).
Cifras verificadas contra `C:\Users\Jorge\Desktop\Itt_repos_cali\outputs\itt_barrio_obrero\ITT_Barrio_Obrero_Consolidado.xlsx`
(el **Excel maestro**, fuente oficial de los scores) y contra los GeoJSON de la zona.

> Replica el estándar metodológico, cartográfico y visual de Ciudad Paraíso.
> Los mapas **consumen** los scores del Excel maestro (no los recalculan); el
> extracto vive en `data/Barrio_Obrero_geojson/itt_maestro_barrio_obrero.json`.

---

## 1. Zonas de estudio (dos polígonos)

| Zona | Polígono | Manzanas | Área | Datos (carpeta) | Salida mapas |
|---|---|---:|---:|---|---|
| **Oficial / completo** | `Geojson_Barrio_Obrero.geojson` | 45 | 37.7 ha | `data/Barrio_Obrero_geojson/barrio_obrero_completo/` | `mapa_html/Barrio_obrero/Barrio_obrero_actual/` |
| **V1** | `poligono_Barrio_Obrero_V1.geojson` | 16 | 13.6 ha | `data/Barrio_Obrero_geojson/v1_barrio_obrero/` | `mapa_html/Barrio_obrero/Barrio_obrero_v1/` |

- CRS de los polígonos: MAGNA-SIRGAS CMT12 (ESRI:103599) → reproyectar a 4326 (web) / 9377 (área).
- Periodo: 2023–2026. El **2026 es parcial (no comparable)** — año no cerrado.
- Método espacial: cruce real point-in-polygon (`gpd.sjoin "within"`). Las cifras de los
  geojson cuadran 100 % con el Excel (hurtos 737, homicidios 33, VIF 93, riñas 187, SPA 268,
  siniestros 83 en el polígono completo, suma 2023–2026).

---

## 2. Metodología del ITT (común con Ciudad Paraíso)

### Pesos por dimensión (suma = 100 %)

| Dimensión | Peso | Variables |
|---|---:|---|
| Seguridad | 27 % | homicidios + hurtos |
| Movilidad | 22 % | siniestralidad + lesionados + mortales |
| Desarrollo Social (Cohesión) | 19 % | VIF + riñas + SPA |
| Entorno Urbano | 17 % | NDVI + % verde + área verde + densidad arbórea |
| Desarrollo Económico | 15 % | establecimientos + ingresos + activo total + empleo |

`ITT = 0.27·Seg + 0.22·Mov + 0.19·DesSocial + 0.17·EntornoU + 0.15·DesEco`

- Filtro estricto de riñas: `agrupado.strip().upper() == "RIÑAS"` (evita falsos positivos de
  "desacato a la autoridad"). SPA: `agrupado == "SUSTANCIAS PSICOACTIVAS"`.
- VIF **siempre** como densidad/calor, nunca puntos individuales (privacidad de víctimas).
- Niveles: Activación 0–40 (#D55E00), Consolidación 40–60 (#E69F00),
  Transformación 60–80 (#009E73), Escala 80–100 (#0072B2).

---

## 3. Resultado ITT (verificado contra Excel maestro, oct 2026)

| Año | Seguridad | Movilidad | DesSocial | EntornoU | DesEco | **ITT** | Nivel |
|---|---:|---:|---:|---:|---:|---:|---|
| 2023 | 66.1 | 24.0 | 48.6 | 30.6 | 60.2 | **46.59** | Consolidación |
| 2024 | 36.9 | 58.0 | 52.5 | 32.7 | 93.7 | **52.31** | Consolidación |
| 2025 | 33.2 | 80.6 | 45.0 | 32.4 | 72.7 | **51.65** | Consolidación |
| 2026* | 66.8 | 84.4 | 84.9 | 31.7 | 71.3 | **68.81** | Parcial (no comparable) |

(*2026 parcial — año no cerrado.)

> **Nota histórica:** el Entorno Urbano se recalculó al incorporar el NDVI de cobertura completa
> (grilla 100×56 que cubre todo el polígono, vs el anterior 35×31 que cubría ~la mitad). Eso bajó
> el score de Entorno (2023 de 60.7 → 30.6) y el ITT consolidado ~5 pts/año respecto a la primera
> versión. Las cifras de esta tabla son las vigentes.

---

## 4. Suite de mapas (6 por zona, estándar Ciudad Paraíso)

Notebooks `BO_1x` (completo) y `BO_V1_0x` (V1). Salidas HTML normalizadas:

| # | Dimensión | Completo | V1 |
|---|---|---|---|
| 01 | Seguridad | `mapa_itt_barrio_obrero_01_seguridad.html` | `..._v1_01_seguridad.html` |
| 02 | Movilidad | `..._02_movilidad.html` | `..._v1_02_movilidad.html` |
| 03 | Convivencia / Social | `..._03_convivencia_social.html` | `..._v1_03_convivencia_social.html` |
| 04 | Entorno Urbano | `..._04_entorno_urbano.html` | `..._v1_04_entorno_urbano.html` |
| 05 | Desarrollo Económico | `..._05_desarrollo_economico.html` | `..._v1_05_desarrollo_economico.html` |
| 06 | Déficit de Vivienda | `..._06_deficit_vivienda.html` | `..._v1_06_deficit_vivienda.html` |

### Estándar visual común
- **4 capas base conmutables**: OpenStreetMap (activa), Esri Satélite, Google Streets, Google Satélite.
- Máscara oscura fuera de la zona; **límite azul `#1B4F8A` weight 2.5**, única capa activa al inicio.
- Mapas de calor con gradiente **cividis** (apto daltonismo), puntos con paleta Okabe-Ito.
- Panel flotante colapsable (abajo-izq) con serie temporal 2023–2026 del ITT maestro (eje Y "Cantidad").
- Slider de intensidad del calor (abajo-der). **Sin botón de exportación** (interfaz despejada).
- `LayerControl(collapsed=True, position="topright")`.

### Detalles por dimensión
- **Movilidad**: siniestros clasificados por `clasificacion_severidad` (solo_danos naranja,
  lesionados azul claro #56B4E9, mortal bermellón #D55E00) + red peatonal OSM (#2A9C8A).
- **Entorno**: censo arbóreo por estado (verde vivo/nuevo, gris muerto/eliminado) + NDVI 4 años
  (ImageOverlay rampa Greens, conmutable) + CAI Obrero. En **V1 el NDVI se recorta (mask) al
  polígono V1** y el panel muestra la media NDVI propia de V1.
- **Déficit vivienda**: coropleta SISBEN (`DEF_HAB_SISBEN.shp`, campo `F_HOG_DE_1`) + panel con
  el dato oficial por barrio del Excel `BD_DEFICIT_HABITACIONAL_BARRIOS_2024.xlsx`
  (Barrio Obrero: 2.140 hogares, 881 en déficit = 41.2 %; cuantitativo 125, cualitativo 756).

---

## 5. Mapas de IPM (separados del ITT — NO se tocan)

Además del ITT, Barrio Obrero tiene su suite de IPM (Índice de Pobreza Multidimensional) por
manzana, previa e independiente, en `mapa_html/Barrio_obrero/`:
`bo_mapa_ipm.html`, `bo_mapa_ipm_original.html`, `bo_mapa_ipm_dimensiones.html`,
`bo_mapa_ipm_dimensiones_v1.html`, `mapa_comparacion_barrio_obrero.html`.
Fuente IPM: Censo 2018 (DANE, CNPV), unidad "% de personas", vacíos = 0, 4 niveles daltónicos.

---

## 6. Datos, insumos y privacidad

- **NDVI** (completo, cobertura total): `barrio_obrero_completo/5_Entorno_Urbano/NDVI_Barrio_Obrero/barrio_obrero_nuevo_ndvi_{2023..2026}.tif` (grilla 100×56, WGS84).
- **Déficit habitacional SISBEN**: `data/5_Dimension_Entorno_Urbano/sec_vivienda/DEF_HAB_SISBEN.shp` + Excel por barrio.
- **CAI Obrero**: `.../5_Entorno_Urbano/CAI_MECAL_CALI_OBRERO.geojson`.
- **PII:** las capas de homicidios (sexo/edad/dirección/ocupación), VIF, riñas y hurtos traen
  campos personales. Por habeas data, las carpetas de datos crudos de BO **no se versionan** en
  el remoto (igual que `data/1_data_itt/` de Ciudad Paraíso). Solo se versiona el JSON maestro
  (agregado, sin PII) y los notebooks.

---

## 7. Empaquetado para compartir

- `notebooks/98c_empaquetar_itt_bo.py` → `compartir_itt_mapas/Mapas_ITT_Barrio_Obrero_<fecha>.zip`
  con los 12 mapas (6 por zona) en subcarpetas `01_poligono_completo/` y `02_poligono_v1/` + LEEME.
- El ZIP no se versiona (regenerable, carpeta `compartir_itt_mapas/` ignorada).

---

## 8. Reglas de trabajo (recordatorio)

- Entorno Python único: `C:\Users\Jorge\.venv\Scripts\python.exe` (uv, NO crear entornos).
- Editar `.ipynb` con `json.dump` utf-8 **sin BOM**, `outputs=[]`, `execution_count=null`.
- Ejecutar: `python -m jupyter nbconvert --to notebook --execute ...` (exit 1 por warnings de
  nbformat/zmq es normal; revisar `output_type=='error'`).
- Si el **Excel maestro cambia**, re-extraer el JSON y reejecutar los mapas.
