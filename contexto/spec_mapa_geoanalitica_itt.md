# Especificacion: Mapa Interactivo de Geoanalitica Territorial (ITT)

Guia de implementacion para el mapa interactivo de geoanalitica territorial del proyecto
(Ciudad Paraiso / Pulmon de Oriente / Cali). Este documento es la referencia de disenio;
la ejecucion depende de contar con los datos de origen (ver seccion "Datos requeridos").

> Convenciones del proyecto aplicables: entorno unico `uv`, codigo sin emojis, versionado
> automatico tras cada cambio, y paleta Okabe-Ito accesible (ver
> `contexto_rol_analitica_geoespacial.md`).

---

## 1. Rol y objetivo

Cientifico de Datos Senior / Especialista GIS. Desarrollar un mapa interactivo de
geoanalitica territorial a partir de datos y scripts del notebook
`notebooks/04_itt_pulmon_oriente_5dim.ipynb` (pendiente de incorporar al repo).

El ITT (Indice de Transformacion Territorial) resume 5 dimensiones por unidad espacial y
clasifica cada poligono en uno de 4 niveles.

---

## 2. Gestion de datos y entorno de archivos

- Carpeta dedicada para datos procesados: `data_processed_geo/` (o `exports_mapa/`).
- Procesar, limpiar, cruzar espacialmente e indexar indicadores a nivel de
  poligono/manzana ANTES de visualizar.
- Exportar artefactos intermedios listos para render: `.geojson`, `.gpkg` o `.parquet`.
- CRS estricto: calculo metrico en EPSG:9377 (MAGNA-SIRGAS Origen Nacional); capa web
  reproyectada a WGS84 EPSG:4326.

---

## 3. Sistema cromatico y accesibilidad (OBLIGATORIO: Okabe-Ito)

Aplicar estrictamente la paleta accesible para daltonismo y la semantica ITT en todos los
marcadores, coropletas y graficos incrustados.

| Constante     | Hex      | Semantica                                                        |
|---------------|----------|------------------------------------------------------------------|
| OKI_AZUL      | #0072B2  | Hurtos / Nivel "Escala" / DE                                     |
| OKI_NARANJA   | #E69F00  | Siniestralidad vial / Nivel "Consolidacion"                      |
| OKI_VERDE     | #009E73  | Rinas (filtro exacto) / Censo arboreo y NDVI / "Transformacion"  |
| OKI_AMARILLO  | #F0E442  | Comparendos SPA (con borde de contraste gris #333333)            |
| OKI_AZUL_C    | #56B4E9  | Lesionados movilidad / Red peatonal                              |
| OKI_BERMELL   | #D55E00  | Homicidios / Siniestros mortales / Nivel "Activacion"            |
| OKI_MORADO    | #CC79A7  | Violencia Intrafamiliar (VIF)                                    |
| OKI_GRIS      | #333333  | Contornos, ejes, textos y referencias neutras                    |

Colores pastel de nivel (bandas / fondo de coropleta suave):

- Activacion     -> #FFCDD2
- Consolidacion  -> #FFE0B2
- Transformacion -> #C8E6C9
- Escala         -> #BBDEFB

Fondo de interfaz / popups: `#F4F6F9`.
Degradados continuos o matrices: colormap `cividis` exclusivamente. Nunca jet/rainbow.

---

## 4. Interactividad cartografica y graficas sobre el mapa

### 4.1 El poligono como unidad central de consulta

Al hacer clic sobre cualquier poligono (zona, sector o manzana) desplegar un
**Popup / ficha enriquecida en HTML/CSS**:

- Nombre, comuna, area y clasificacion.
- Badge del nivel ITT con su color correspondiente.
- Mini-graficas / diagramas incrustados (barras de distribucion de incidentes,
  distribucion de arbolado, barras comparativas de tendencia T-1 vs T0), con los colores
  de la paleta. Preferir SVG inline (sin dependencias JS pesadas en el popup).
- Tabla sintesis con variaciones porcentuales.

### 4.2 Tipologias cartograficas

- Coropletas: pintar poligonos segun nivel ITT o densidad de criticidad con los tonos
  semanticos.
- Simbolos proporcionales (eventos puntuales): escalar el radio del marcador segun la
  frecuencia de eventos en intersecciones/puntos, con el color tematico asignado.

---

## 5. Capas base, eventos y reglas de privacidad

### 5.1 Arranque del mapa

- `tiles=None` de base. Agregar manualmente 4 capas conmutables:
  - OpenStreetMap (activa por defecto).
  - Esri Satelite.
  - Google Streets.
  - Google Satelite.
- Mapa limpio al inicio: solo el contorno territorial activo (`show=True`); el resto de
  capas apagadas (`show=False`) en el `LayerControl`.

### 5.2 Privacidad estricta en VIF

- La Violencia Intrafamiliar NUNCA se representa como punto individual. Se genera como
  superficie continua / mapa de calor (`HeatMap`) para evitar re-identificacion de
  victimas.

### 5.3 Consistencia de filtros

- Rinas: filtro exacto `agrupado.strip().upper() == "RINAS"`.
- SPA: comparendos filtrados exactamente como sustancias psicoactivas.
- Red peatonal: extraccion con `osmnx` tolerante a fallos (`try/except`).
- Censo arboreo: capa visible en verde Okabe-Ito (#009E73).

---

## 6. Entregables requeridos

1. Pipeline de procesamiento que guarde la data en la carpeta procesada
   (`data_processed_geo/`).
2. Codigo completo y documentado para generar y exportar el mapa `.html` interactivo y
   autonomo.
3. Resumen analitico de los hallazgos territoriales de la zona.

---

## 7. Datos requeridos (BLOQUEANTE para ejecutar)

Al momento de redactar esta spec, el workspace NO contiene:

- El notebook `notebooks/04_itt_pulmon_oriente_5dim.ipynb`.
- Capas/tablas de eventos de seguridad: hurtos, homicidios, rinas, lesionados,
  siniestralidad vial, comparendos SPA, VIF.
- Censo arboreo / NDVI de la zona.
- Poligonos de las unidades de analisis del Pulmon de Oriente (si difieren de las manzanas
  de Ciudad Paraiso ya disponibles en `data/geojson/`).

Para ejecutar el pipeline se necesita incorporar esos insumos al proyecto (o indicar su
ruta). Mientras tanto, esta spec queda como guia de implementacion.
