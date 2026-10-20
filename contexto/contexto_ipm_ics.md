# Contexto: IPM e ICS

Documento de referencia sobre los dos índices base del proyecto de pobreza
multidimensional y condición social de Santiago de Cali, a nivel de **manzana**.

---

## 1. Índice de Pobreza Multidimensional (IPM)

### Definición

Indicador **inverso** que mide el nivel de privaciones de los hogares.

- `0` = sin pobreza (óptimo)
- `100` = máxima pobreza (crítico)
- Un hogar se considera en **pobreza multidimensional** cuando `IPM >= 33.3%`.
- Las 15 variables desagregadas también son **inversas** (mayor valor = peor situación).

### Nota metodológica: severidad

Para análisis de **severidad** se promedian únicamente las manzanas con `IPM > 0` (donde
hay pobreza registrada), lo que mide la *profundidad* de la carencia en los hogares
afectados.

- Cali Urbana (severidad) = **15.28**
- Cali Rural (severidad) = **38.33**

### Fuente de datos

| Formato | Archivo | Clave de manzana |
| :--- | :--- | :--- |
| GeoJSON | `data/geojson_ipm/Mzn_ipm_variables.geojson` | `COD_MZN` (22 chars) |
| Excel | `IPM - Variables (incidencias).xlsx` | `cod_mzn` (24 chars) |

> **Merge Excel <-> ICS:** el `cod_mzn` del Excel tiene 24 chars; el `COD_MZN` del ICS
> tiene 22. Los 2 dígitos extra (posiciones 6-7) son el número de comuna. Transformación:
> `COD_MZN = cod_mzn[:6] + cod_mzn[8:]`. Match: 13.614 / 13.687 filas (99.5%).
>
> **Importante:** en los **GeoJSON** de IPM e ICS el `COD_MZN` ya viene homologado a 22
> chars, por lo que el cruce entre ellos es directo (`on='COD_MZN'`) y NO requiere la
> transformación anterior.

### Las 15 variables de incidencia (%)

| Código | Descripción | Obs. aprox. (manzanas) |
| :--- | :--- | :--- |
| `ANALF_` | Analfabetismo | ~9.512 |
| `BAJO_` | Bajo logro educativo | ~13.484 |
| `INFANCIA_` | Barreras servicios de cuidado primera infancia | ~6.487 |
| `INASIS_` | Inasistencia escolar | ~7.435 |
| `REZAGO_` | Rezago escolar | ~12.210 |
| `TRAB_INFAN` | Trabajo infantil | ~2.662 |
| `DEPEN_` | Dependencia económica | ~13.415 |
| `INFOR_` | Informalidad | ~13.686 |
| `SALUD_` | Barreras de acceso a servicios de salud | ~7.932 |
| `ASEGU_` | Sin aseguramiento en salud | ~13.187 |
| `HACI_` | Hacinamiento crítico | ~9.228 |
| `PARED_` | Material inadecuado de paredes exteriores | ~1.425 |
| `EXCRE_` | Eliminación inadecuada de excretas | ~2.008 |
| `PISOS_` | Material inadecuado de los pisos | ~1.065 |
| `AGUA_` | Sin acceso a fuentes de agua mejorada | ~1.511 |

### Agrupación por dimensiones

| Dimensión | Variables |
| :--- | :--- |
| Educación | `ANALF_`, `BAJO_`, `INFANCIA_`, `INASIS_`, `REZAGO_` |
| Trabajo | `TRAB_INFAN`, `DEPEN_`, `INFOR_` |
| Salud | `SALUD_`, `ASEGU_` |
| Vivienda | `HACI_`, `PARED_`, `PISOS_` |
| Servicios | `AGUA_`, `EXCRE_` |

- Variable más crítica a nivel ciudad: `INFOR_` (Informalidad, >82% promedio).
- Segunda más crítica: `BAJO_` (Bajo logro educativo, >37% promedio).

### Columnas del GeoJSON de IPM

```
COD_DPTO, COD_MPIO, COD_DANE, ipm, OID_, COD_MZN,
ANALF_, BAJO_, INFANCIA_, INASIS_, REZAGO_, TRAB_INFAN,
DEPEN_, INFOR_, SALUD_, ASEGU_, HACI_, PARED_, EXCRE_,
PISOS_, AGUA_, zona, zona2, geometry
```

> Nota del proyecto: el GeoJSON oficial en uso es
> `data/geojson/IPM_ciudad_Paraiso.geojson` (33 manzanas de Ciudad Paraiso, trae ademas
> la columna `ics`). Reemplaza a `Mzn_ipm_variables.geojson` como fuente para los mapas.

---

## 2. Índice de Condición Social (ICS)

### Definición

Indicador **directo** de bienestar y acceso.

- `0` = condición crítica
- `100` = condición óptima
- Se basa en clima educativo y hacinamiento.

### Fuente de datos

| Formato | Archivo | Clave de manzana |
| :--- | :--- | :--- |
| GeoJSON | `data/geojosn_ICS/ics_mzn.geojson` | `COD_MZN` (22 chars) |

### Columnas del GeoJSON de ICS

```
COD_MZN, CLASE, ZONA, cod_dane_a, ics, geometry
```

> Nota del proyecto: el GeoJSON oficial en uso es
> `data/geojson/ICS_ciudad_Paraiso.geojson` (33 manzanas de Ciudad Paraiso). El valor va
> en la columna `ics`.

---

## 3. Escala de clasificación (8 categorías)

El IPM y el ICS comparten los **mismos rangos numéricos** pero usan **paletas distintas**
(ambas accesibles para daltonismo):

- **IPM:** paleta `viridis` (indicador inverso, mayor = peor).
- **ICS:** paleta `cividis` (indicador directo, mayor = mejor).

> Usar coma como separador decimal en textos; punto en código.

| HEX | Rango | Categoría |
| :--- | :--- | :--- |
| `#00224e` | 0,4 - 20,0 | Bajo |
| `#213b6e` | 20,1 - 27,0 | Moderado-Bajo |
| `#4c556c` | 27,1 - 33,1 | Moderado |
| `#6c6e72` | 33,2 - 39,8 | Moderado-Alto |
| `#8e8978` | 39,9 - 48,6 | Alto |
| `#b1a570` | 48,7 - 60,6 | Muy Alto |
| `#d9c55c` | 60,7 - 80,0 | Extremo |
| `#fee838` | 80,1 - 335,1 | Extremo Máximo |

### Formato JSON (para código)

```json
{
  "leyenda": "IPM",
  "configuracion_escala": [
    {"rango_min": 0.4,  "rango_max": 20.0,  "hex": "#00224e", "categoria": "Bajo"},
    {"rango_min": 20.1, "rango_max": 27.0,  "hex": "#213b6e", "categoria": "Moderado-Bajo"},
    {"rango_min": 27.1, "rango_max": 33.1,  "hex": "#4c556c", "categoria": "Moderado"},
    {"rango_min": 33.2, "rango_max": 39.8,  "hex": "#6c6e72", "categoria": "Moderado-Alto"},
    {"rango_min": 39.9, "rango_max": 48.6,  "hex": "#8e8978", "categoria": "Alto"},
    {"rango_min": 48.7, "rango_max": 60.6,  "hex": "#b1a570", "categoria": "Muy Alto"},
    {"rango_min": 60.7, "rango_max": 80.0,  "hex": "#d9c55c", "categoria": "Extremo"},
    {"rango_min": 80.1, "rango_max": 335.1, "hex": "#fee838", "categoria": "Extremo Maximo"}
  ]
}
```

---

## 4. IPM Global comparativo por zona de estudio

| Zona | Manzanas con IPM | IPM Promedio | IPM Min | IPM Max |
| :--- | :--- | :--- | :--- | :--- |
| Cali (ciudad) | 11.026 | 16,60 | 0,20 | 100,00 |
| Barrio Obrero | 11 | 13,18 | 2,00 | 25,60 |
| Roosevelt | 21 | 7,51 | 2,50 | 25,00 |
| Ciudad Paraíso | 33 | 26,52 | - | - |

Severidad IPM (`IPM > 0`) por zona: Cali Urbana = 15,28 · Cali Rural = 38,33 · Barrio
Obrero = 13,18 · Roosevelt = 7,51.

### Hallazgos clave

- **Barrio Obrero:** severidad de Informalidad del 93,1% (supera el promedio urbano).
- **Roosevelt:** severidad de Sin Aseguramiento en Salud del 22,7%.
- **Ciudad Paraíso:** zona de estudio con mayor privación registrada. IPM global = 26,52
  (supera el promedio ciudad), ICS promedio = 23,07. Top privaciones: Informalidad 89,7%,
  Bajo logro educativo 59,7%, Hacinamiento crítico 22,9%, Sin aseguramiento 21,6%,
  Dependencia económica 20,9%.
- **Brecha rural:** severidad crítica en infraestructura básica (Eliminación de excretas
  41,9%, Agua mejorada 27,0%).

---

## 5. Lectura rápida para interpretar

| Si ves... | IPM | ICS |
| :--- | :--- | :--- |
| Dirección | Inverso (mayor = peor) | Directo (mayor = mejor) |
| Valor alto | Más pobreza / privación | Mejor condición social |
| Paleta | viridis | cividis |
| Umbral de referencia | Pobre si `>= 33,3%` | — |
| Clave de cruce | `COD_MZN` (22 chars en GeoJSON) | `COD_MZN` (22 chars) |

---

## 6. Estado de implementacion

1. **Mapa IPM (nb 08) - HECHO:** usa la fuente oficial `IPM_ciudad_Paraiso.geojson` con la
   escala oficial de 8 categorias en paleta **viridis** + leyenda de paleta en el mapa.
2. **Mapa ICS (nb 10) - HECHO:** `data/geojson/ICS_ciudad_Paraiso.geojson` (columna `ics`),
   escala de 8 categorias en paleta **cividis** (directo) + leyenda de paleta.
3. **Capas de referencia en los mapas 02-07 - HECHO:** cada mapa de dimension incluye
   `Ref IPM` (viridis) y `Ref ICS` (cividis), apagadas, desde la fuente oficial, via
   `_add_ipm_ics_ref(mapa)`. La leyenda de cada una aparece SOLO al activar la capa
   (`overlayadd`/`overlayremove`).
4. **Laboratorio (nb 09) - HECHO:** usa la fuente oficial (trae ipm, ics y las 15
   variables); panel legible con medidores IPM/ICS + privaciones por manzana al tocarla,
   y leyenda doble (viridis/cividis).
5. **Cruce IPM <-> ICS:** directo por `COD_MZN` (22 chars) en los GeoJSON; de hecho el
   GeoJSON oficial de IPM ya trae la columna `ics`, por lo que no requiere cruce de
   archivos. La transformacion 24->22 chars solo aplica al Excel.

### Pendiente / opcional
- Confirmar si el mapa dedicado de IPM debe mostrar tambien ICS como capa alterna (hoy el
  laboratorio ya ofrece ambas).


---

## 7. Replica IPM para Barrio Obrero (segunda zona de estudio)

Se replico el analisis de IPM (sin ITT ni capas transversales de Ciudad Paraiso) para la
zona **Barrio Obrero** (Comuna 9, Cali), 16 manzanas.

- **Datos:** `data/Barrio_Obrero_geojson/` -> `IPM_BARRIO_OBRERO_2_POLIGONOS/IPM_Barrio_Obrero_V1.geojson`
  (misma estructura que el IPM de Ciudad Paraiso: ipm, ics, 15 variables, COD_MZN) y
  `poligono_Barrio_Obrero_V1.geojson` (limite). IPM en zona: min 0, max 25,6, media 9,1.
- **Notebooks:** `BO_01_mapa_ipm.ipynb` (coropleta 4 niveles tipo calor),
  `BO_03_mapa_ipm_dimensiones.ipynb` (coropletas por dimension + barras por manzana al
  clic), `BO_04_analitica_ipm.ipynb` (barras comparativas Cali vs Comuna 9).
- **Salida HTML:** `mapa_html/Barrio_obrero/` (bo_mapa_ipm.html, bo_mapa_ipm_dimensiones.html).
- **Correcciones aplicadas (nacen corregidas):** paleta apta daltonismo azul->naranja (sin
  verde/rojo); vacios = 0 (REDATAM); unidad "% de personas"; leyenda aclara que los cortes
  8/15/25 son del proyecto (no el 33,3 del DANE); fuente rotulada Censo 2018 (DANE, CNPV);
  5 dimensiones DANE (Educacion, Ninez y juventud, Trabajo, Salud, Vivienda y servicios).
- Limite de Barrio Obrero en azul oscuro #1B4F8A.
