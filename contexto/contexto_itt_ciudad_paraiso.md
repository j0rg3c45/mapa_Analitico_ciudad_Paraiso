# Contexto ITT — Ciudad Paraíso (Comuna 3, Cali)

Índice de Transformación Territorial (ITT) de la zona de renovación urbana Ciudad Paraíso.

## Zona de estudio

- Barrios: San Pascual, El Calvario, San Juan Bosco, Santa Rosa (Comuna 3).
- Área del polígono: **33.70 ha** (337,039.2 m²).
- Periodo analizado: **2023–2026** (2026 parcial: DATIC hasta Q3, siniestros hasta Q2; Q4 2026 sin dato).
- Verificación espacial: point-in-polygon real (`geopandas.sjoin "within"`) contra el polígono; no se
  confía en los campos `nom_barrio`/`comuna` de las fuentes.

## Pesos del ITT por dimensión (suma = 100 %)

| Dimensión | Peso |
|---|---:|
| Seguridad | 27 % |
| Movilidad | 22 % |
| Desarrollo Social (Cohesión) | 19 % |
| Entorno Urbano | 17 % |
| Desarrollo Económico | 15 % |
| **Total** | **100 %** |

Pesos idénticos a Barrio Obrero (metodología común del proyecto).

**Fórmula:**
`ITT = 0.27·Seguridad + 0.22·Movilidad + 0.19·DesSocial + 0.17·EntornoU + 0.15·DesEco`

### Composición de cada dimensión

- **Seguridad (27 %):** homicidios + hurtos.
- **Movilidad (22 %):** siniestralidad + lesionados + mortales.
- **Desarrollo Social / Cohesión (19 %):** VIF + riñas + SPA.
- **Entorno Urbano (17 %):** NDVI anual + censo arbóreo (datos propios de la zona).
- **Desarrollo Económico (15 %):** establecimientos activos + ingresos + activo total + empleo
  (stock activo por año, fuente Cámara de Comercio consolidada).

## Resultado ITT (0–100)

| Año | ITT | Nivel |
|---|---:|---|
| 2023 | 44.1 | Consolidación |
| 2024 | 55.5 | Consolidación |
| 2025 | 58.5 | Consolidación |
| 2026 | 81.4 | Parcial — no comparable (cobertura incompleta) |

> El ITT 2026 (81.4) sale "Escala" por el cálculo, pero está marcado como **parcial/no comparable**
> porque la cobertura de 2026 está incompleta (faltan trimestres). No debe leerse como una mejora real
> frente a los años completos.

### Niveles de transformación (umbrales)

| Nivel | Rango ITT |
|---|---|
| Activación | ITT < 40 |
| Consolidación | 40 ≤ ITT < 60 |
| Transformación | 60 ≤ ITT < 80 |
| Escala | ITT ≥ 80 |

---

# Paleta de colores accesible para daltonismo — Okabe-Ito

Diseñada para ser distinguible en las tres formas de daltonismo (protanopia, deuteranopia, tritanopia)
y también en escala de grises. Es la paleta estándar del proyecto, definida una sola vez y reutilizada
en todas las gráficas y mapas.

## Constantes (hex)

| Constante | Hex | Color |
|---|---|---|
| OKI_AZUL | `#0072B2` | azul fuerte |
| OKI_NARANJA | `#E69F00` | naranja |
| OKI_VERDE | `#009E73` | verde |
| OKI_AMARILLO | `#F0E442` | amarillo |
| OKI_AZUL_C | `#56B4E9` | azul cielo |
| OKI_BERMELL | `#D55E00` | bermellón / rojo-naranja |
| OKI_MORADO | `#CC79A7` | rosa / morado |
| OKI_GRIS | `#333333` | gris oscuro (ejes y referencias) |
| BG | `#F4F6F9` | fondo de figuras |

## Niveles ITT (color fijo por nivel)

| Nivel | Color |
|---|---|
| Activación | `#D55E00` bermellón |
| Consolidación | `#E69F00` naranja |
| Transformación | `#009E73` verde |
| Escala | `#0072B2` azul |

## Capa de predios por estado de demolición (Plan Cristo Rey)

Colores elegidos para **máxima distinguibilidad bajo daltonismo** (los 4 tonos más separados):

| Estado | Color |
|---|---|
| Demolido | `#D55E00` bermellón |
| Programado para demolición | `#0072B2` azul |
| En proceso (hacia demolición) | `#F0E442` amarillo |
| Sin demolición programada | `#009E73` verde |

> "Programado" se cambió de naranja a azul: bermellón y naranja se confunden en daltonismo rojo-verde.

## Homicidios estación Fray Damián (color por año)

| Año | Color |
|---|---|
| 2023 | `#0072B2` azul |
| 2024 | `#009E73` verde |
| 2025 | `#E69F00` naranja |
| 2026 | `#D55E00` bermellón |

## Mapas de calor (heatmaps indicador × trimestre)

Colormap **`cividis`** (perceptualmente uniforme y apto para daltonismo).

## Reglas de uso

- Cada indicador tiene color fijo (p. ej. VIF siempre morado, homicidios siempre bermellón), para
  asociar color↔indicador en todas las gráficas.
- Para magnitud/continuo: colormaps uniformes (`cividis`), nunca jet/rainbow.
- **EVITAR juntar bermellón (`#D55E00`) y naranja (`#E69F00`):** se confunden en daltonismo rojo-verde.
  Para pares/cuartetos usar azul + verde + amarillo + bermellón bien repartidos.
- Fondo claro uniforme (`#F4F6F9`), ejes sin spines superior/derecho, grid alpha 0.3, fuente DejaVu Sans.
