# Índice de Transformación Territorial (ITT) — Ciudad Paraíso

Documento de contexto completo. Cifras verificadas contra
`outputs/itt_ciudad_paraiso/ITT_Ciudad_Paraiso_Consolidado.xlsx` y los GeoJSON exportados.

---

## 1. Zona de estudio

- **Zona:** Ciudad Paraíso — zona de renovación urbana, Comuna 3, Cali.
- **Barrios:** San Pascual, El Calvario, San Juan Bosco, Santa Rosa (y borde con Sucre).
- **Área del polígono:** 33.70 ha (337,039.2 m²).
- **Periodo:** 2023–2026. El 2026 es **parcial** (DATIC hasta Q3, siniestros hasta Q2); su ITT se
  calcula pero **no es comparable** con los años completos.
- **Método espacial:** verificación real point-in-polygon (`geopandas.sjoin "within"`) contra el
  polígono; no se confía en los campos `nom_barrio`/`comuna` de las fuentes (poco fiables en esta zona).
- **Notebook:** `notebooks/08_itt_ciudad_paraiso_5dim.ipynb`.

---

## 2. Metodología del ITT

### Pesos por dimensión (suma = 100 %)

| Dimensión | Peso |
|---|---:|
| Seguridad | 27 % |
| Movilidad | 22 % |
| Desarrollo Social (Cohesión + Educación) | 19 % |
| Entorno Urbano | 17 % |
| Desarrollo Económico | 15 % |
| **Total** | **100 %** |

Pesos idénticos a Barrio Obrero (metodología común del proyecto).

**Fórmula:**

`ITT = 0.27·Seguridad + 0.22·Movilidad + 0.19·DesSocial + 0.17·EntornoU + 0.15·DesEco`

- Normalización de cada indicador: min-max con umbrales fijos (`ref_min`/`ref_max`, `score_ref`),
  escala 0–100. Indicadores "inversos" (menos = mejor, p. ej. homicidios) se invierten.
- Donde no hay dato: `NaN` (no se puntúa como 0/100).

---

## 3. Resultado ITT (verificado — aritmética cierra exacto)

| Año | Seguridad | Movilidad | DesSocial | EntornoU | DesEco | **ITT** | Nivel |
|---|---:|---:|---:|---:|---:|---:|---|
| 2023 | 22.5 | 39.2 | 65.1 | 52.2 | 61.0 | **45.08** | Consolidación |
| 2024 | 58.1 | 35.7 | 53.5 | 61.6 | 65.0 | **53.94** | Consolidación |
| 2025 | 55.0 | 71.2 | 33.2 | 61.4 | 68.6 | **57.55** | Consolidación |
| 2026* | 88.1 | 94.4 | 12.7 | 55.0 | 67.3 | **66.42** | Transformación |

(*2026 parcial — cobertura: DATIC Q1-Q3, siniestros Q1-Q2, resto del año en curso.)

### Niveles de transformación (umbrales)

| Nivel | Rango ITT |
|---|---|
| Activación | ITT < 40 |
| Consolidación | 40 ≤ ITT < 60 |
| Transformación | 60 ≤ ITT < 80 |
| Escala | ITT ≥ 80 |

> **Advertencia 2026:** el salto a 66.4 ("Transformación") se debe en gran parte a que los conteos
> de seguridad y movilidad están incompletos (medio año) medidos contra umbrales anuales → los
> indicadores inversos dan score artificialmente alto (Seguridad 88, Movilidad 94). No leer como
> mejora real frente a 2023–2025.

---

## 4. Dimensiones en detalle

### 4.1 Seguridad (27 %) — homicidios + hurtos

| Año | Homicidios | Hurtos | score_homicidios | score_hurtos | **score_seguridad** |
|---|---:|---:|---:|---:|---:|
| 2023 | 16 | 260 | 20.0 | 25.0 | **22.5** |
| 2024 | 6 | 209 | 70.0 | 46.3 | **58.1** |
| 2025 | 11 | 164 | 45.0 | 65.0 | **55.0** |
| 2026* | 4 | 89 | 80.0 | 96.3 | **88.1** |

`score_seguridad = media(score_homicidios, score_hurtos)`.

### 4.2 Movilidad (22 %) — siniestralidad + lesionados + mortales

| Año | Siniestros | Lesionados | Mortales | **score_movilidad** |
|---|---:|---:|---:|---:|
| 2023 | 33 | 24 | 4 | **39.2** |
| 2024 | 35 | 30 | 3 | **35.7** |
| 2025 | 24 | 23 | 0 | **71.2** |
| 2026* | 5 | 4 | 1 | **94.4** |

`score_movilidad = media(score_siniestralidad, score_lesionados, score_mortales)`.
Cobertura siniestros 2026: hasta Q2.

### 4.3 Desarrollo Social / Cohesión (19 %) — VIF + riñas + SPA + educación

| Año | VIF | Riñas | SPA | score_matrícula | score_deserción | **score_DesSocial** |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 11 | 327 | 66 | 100.0 | 45.9 | **65.1** |
| 2024 | 17 | 357 | 28 | 41.1 | 58.6 | **53.5** |
| 2025 | 15 | 418 | 121 | 5.5 | 66.3 | **33.2** |
| 2026* | 17 | 547 | 135 | 0.0 | — | **12.7** |

> **Riñas — criterio del proyecto:** se usa el filtro amplio (`agrupado` contiene "RI"), que incluye
> `RIÑAS` + `DESACATO, IRRESPETO A LA AUTORIDAD`. Por eso las cifras son altas (327/357/418/547).
> Es el mismo criterio del Excel entregado (decisión adoptada). El filtro estricto (`== "RIÑAS"`) daría
> 29/61/114/49 (riñas reales), pero NO es el criterio publicado.

La caída de score (65→12.7) refleja el aumento sostenido de riñas y SPA.

### 4.4 Entorno Urbano (17 %) — NDVI + censo arbóreo + habitabilidad (vivienda)

| Año | NDVI | Árboles | score_ndvi | score_arbolado | score_habitabilidad | **score_entorno_u** |
|---|---:|---:|---:|---:|---:|---:|
| 2023 | 0.090 | 303 | 36.0 | 66.7 | 53.9 | **52.2** |
| 2024 | 0.110 | 303 | 64.1 | 66.7 | 53.9 | **61.6** |
| 2025 | 0.110 | 303 | 63.7 | 66.7 | 53.9 | **61.4** |
| 2026* | 0.099 | 303 | 44.2 | 66.7 | 53.9 | **55.0** |

- NDVI: media anual del raster satelital recortado al polígono (datos propios de la zona).
- Censo arbóreo: 303 árboles vivos/nuevos dentro del polígono (constante en la serie, corte único).
- Habitabilidad: `1 − déficit habitacional`, corte estructural único 2024 (constante).

### 4.5 Desarrollo Económico (15 %) — establecimientos + ingresos + activo + empleo

| Año | Establecimientos activos | Empleo (personas) | Ingresos operacionales | Activo total | **score_des_eco** |
|---|---:|---:|---:|---:|---:|
| 2023 | 236 | 834 | 374,307,227,177 | 527,574,501,397 | **61.0** |
| 2024 | 278 | 881 | 374,657,166,989 | 528,536,097,126 | **65.0** |
| 2025 | 325 | 898 | 374,690,467,989 | 529,034,175,386 | **68.6** |
| 2026* | 311 | 885 | 374,685,467,989 | 528,743,475,386 | **67.3** |

- Fuente: registro mercantil consolidado (Cámara de Comercio, filtrado al polígono). 328 negocios.
- Método: **stock activo por año** (matriculado ≤ año y no cancelado hasta ese año).
- 4 componentes: establecimientos, ingresos (log1p), activo total (log1p), empleo (PERSONAL_OCUPADO).

---

## 5. Variables de soporte (anexo)

### Vivienda (déficit habitacional SISBÉN 2024, corte único)

| Barrio | Hogares en zona | Déficit en zona | Tasa déficit |
|---|---:|---:|---:|
| San Pascual | 751 | 338 | 45.0 % |
| San Juan Bosco | 290 | 144 | 49.8 % |
| El Calvario | 59 | 27 | 46.0 % |
| Santa Rosa | 57 | 24 | 41.7 % |
| Sucre | 1 | 1 | 45.8 % |
| **TOTAL zona** | **1,158** | **534** | **46.1 %** |

- Habitabilidad = 53.9 (= 1 − 0.461, ×100). Subsidios de mejoramiento 2024-2026 en la zona: **0**
  (programa dirigido a comunas de ladera/periferia, no al centro).

### Educación (IE Antonio José Camacho + IE Santa Librada)

| Año | Matrícula | Desertores | Repitentes | Tasa deserción | Tasa repitencia |
|---|---:|---:|---:|---:|---:|
| 2023 | 3,891 | 316 | 365 | 8.12 % | 9.38 % |
| 2024 | 3,529 | 219 | 367 | 6.21 % | 10.40 % |
| 2025 | 3,310 | 167 | 302 | 5.05 % | 9.12 % |
| 2026* | 3,276 | — | 317 | — | 9.68 % |

### Indicadores trimestrales

Desglose Q1–Q4 2023–2026 disponible (hoja `Indicadores_Trimestrales`). En 2026: DATIC con dato hasta
Q3 (Q4 = sin dato); siniestros hasta Q2 (Q3–Q4 = sin dato).

---

## 6. Estructura del Excel entregado (10 hojas)

1. `ITT_Resumen` — scores por dimensión + ITT + nivel + cobertura 2026.
2. `Seguridad` — homicidios, hurtos y sus scores.
3. `Movilidad` — siniestralidad, lesionados, mortales y scores.
4. `DesSocial_Cohesion_Educ` — VIF, riñas, SPA + educación.
5. `Entorno_Urbano_NDVI_arb_viv` — NDVI, arbolado, habitabilidad.
6. `Vivienda_SecVivienda` — déficit por barrio prorrateado + subsidios.
7. `Educacion` — matrícula, deserción, repitencia por año.
8. `Desarrollo_Economico` — stock activo, ingresos, activo, empleo y scores.
9. `Indicadores_Trimestrales` — serie trimestral de todos los indicadores.
10. `Auditoria_Fuentes` — notas de método por fuente.

---

## 7. Capas GeoJSON exportadas (15) — carpeta `data/1_data_itt`

| # | Archivo | Registros | Geometría |
|---|---|---:|---|
| 00 | limite_ciudad_paraiso | 1 | MultiPolygon |
| 01 | manzanas_itt_consolidado | 28 | Polygon |
| 02 | seguridad_homicidios | 37 | Point |
| 03 | seguridad_hurtos | 722 | Point |
| 04 | convivencia_rinas | 1,649 | Point |
| 05 | convivencia_spa | 350 | Point |
| 06 | movilidad_siniestros | 97 | Point |
| 07 | movilidad_red_peatonal_osm | 400 | LineString |
| 08 | entorno_censo_arboreo | 312 | Point |
| 09 | seguridad_vif_calor_poligonal | 28 | Polygon |
| 10 | demoliciones_cristo_rey_predios | 100 | Polygon |
| 11 | estacion_fray_damian_manzana | 1 | Polygon |
| 12 | estacion_fray_damian_homicidios_300m | 17 | Point |
| 13 | desarrollo_economico_negocios | 328 | Point |
| 14 | educacion_sedes | 6 | Point |

- Todas en WGS84 (EPSG:4326), columnas snake_case, nulos → `None`, fechas ISO-8601.
- VIF solo como **agregación poligonal por manzana** (regla de privacidad: nunca puntos ni direcciones).
- Riñas con el criterio amplio del Excel (1,649 = 327+357+418+547).

---

## 8. Notas y advertencias clave

1. **2026 no es comparable**: conteos parciales inflan Seguridad (88) y Movilidad (94); el ITT 66.4
   es informativo, no una mejora real.
2. **Riñas con criterio amplio** (incluye desacatos), por decisión del proyecto para cuadrar con el
   Excel. Las riñas reales (`== "RIÑAS"`) serían ~1/10 de esa cifra.
3. **Deck PMU vs notebook**: el deck PMU presenta el ITT con 6 dimensiones (añade Vivienda aparte) y
   serie distinta (45.1/53.9/57.6/66.4). El notebook/Excel usa 5 dimensiones (Vivienda dentro de
   Entorno Urbano). Pendiente unificar si se publican juntos.
4. **Aritmética verificada**: `Σ(score × peso)` reproduce exacto el ITT de las 4 filas del Excel.
