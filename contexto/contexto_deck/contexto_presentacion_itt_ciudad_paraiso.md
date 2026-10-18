# Contexto — Presentación ITT / Reporte diario PMU · Ciudad Paraíso

Documento de contexto extraído del deck **"Reporte diario PMU · Ciudad Paraíso"**
(PMU · Recuperación Centro). Boceto para revisión del equipo, corte 16 de octubre de 2026.
17 láminas. Resume la estructura de la presentación y la data actual del ITT y sus variables.

---

## 1. Propósito y formato del deck

- **Qué es:** reporte diario del PMU (Puesto de Mando Unificado) de la Recuperación del Centro,
  zona Ciudad Paraíso. Combina avance operativo de caracterización + resultados por dominio
  social + indicadores de territorio (seguridad, convivencia, movilidad, desarrollo económico)
  + el ITT como resumen.
- **Estructura de láminas:**
  1. Portada (corte: día/hora).
  2. Lectura del día — "Hoy en tres mensajes" (qué avanzó, dónde intervenir, qué se decide).
  3. Avance de la operación — caracterización por manzana.
  4–8. Resultados por dominio: Salud, Vivienda, Bienestar, Menores, Negocios.
  9–14. Territorio: Homicidios, Hurtos, Riñas, SPA, Siniestros, Establecimientos.
  15. Resumen — Índice de Transformación Territorial (ITT).
  16. Caracterización × territorio — "Dónde priorizar".
  17. Anexo — otras variables del ITT.
- **Convenciones:** cifras con placeholders `[__]` por completar; "conteos menores de 5 agrupados"
  (protección de datos); mapas marcados como "ilustrativos"; comparaciones "frente al mismo
  periodo del año anterior".

---

## 2. Avance operativo (caracterización)

- **Caracterización por manzana: 56.6 %** — 469 de 828 personas.
- **27** manzanas con padrino · **23** [cierre estimado] · estado: *atrasada frente a la meta*.
- Fuente: Gob 24/7.

### Resultados por dominio (bases de caracterización)
| Dominio | Base |
|---|---|
| Salud | 257 personas con formulario de Salud |
| Vivienda | 210 hogares en la base |
| Bienestar | [por completar] |
| Menores | [por completar] |
| Negocios | 238 caracterizados · **113 afectados por el terremoto** |

---

## 3. Territorio — indicadores (2026, enero–septiembre salvo que se indique)

Cada indicador se muestra con cifra 2026, variación vs. mismo periodo 2025, y serie trimestral
desde la línea base 2023.

| Indicador | 2026 | Var. vs 2025 | Línea base 2023 | Fuente |
|---|---:|---:|---:|---|
| Homicidios | 4 | −56 % | 16 | Sec. Seguridad (T3 2026 prelim.) |
| Hurtos | 89 | −28 % | 260 | Sec. Seguridad (T3 2026 prelim.) |
| Riñas | 547 | +78 % | 327 | Sec. Seguridad (T3 2026 prelim.) |
| Casos por SPA | 135 | +96 % | 66 | Sec. Seguridad (T3 2026 prelim.) |
| Siniestros viales | 5 (ene–jun) | −69 % | 33 | Sec. Movilidad |
| Establecimientos activos | 311 | −4 % vs 2025 · +32 % vs 2023 | 236 | Cámara de Comercio |

> **Nota sobre riñas:** el deck usa 327 (2023) / 547 (2026), que corresponden al conteo amplio
> (incluye "DESACATO, IRRESPETO A LA AUTORIDAD"). El export de capas del proyecto usa el filtro
> estricto `== "RIÑAS"` (riñas reales: 29/61/114/49). Diferencia a tener presente al comparar deck vs capas.

---

## 4. Índice de Transformación Territorial (ITT) — lámina resumen del deck

- **ITT 2026 = 66.4** → **Fase de transformación** (escala 0–100).
- Serie del deck: **2023 = 45.1 · 2024 = 53.9 · 2025 = 57.6 · 2026 = 66.4**.
- Dimensiones que resume (deck, **6 dimensiones**): Seguridad · Movilidad · Desarrollo social ·
  Entorno urbano · **Vivienda** · Desarrollo económico.

> **Diferencia deck vs notebook (importante):** el notebook `08_itt_ciudad_paraiso_5dim.ipynb`
> calcula el ITT con **5 dimensiones** (Seguridad 27 %, Movilidad 22 %, DesSocial 19 %, EntornoU 17 %,
> DesEco 15 %) y da la serie **44.1 / 55.5 / 58.5 / 81.4** (2026 parcial, no comparable). El deck PMU
> presenta **6 dimensiones** (añade Vivienda como dimensión propia) y una serie distinta
> (45.1 / 53.9 / 57.6 / 66.4). Son dos consolidaciones diferentes del mismo índice; conviene unificar
> criterio (nº de dimensiones y tratamiento de 2026 parcial) antes de publicar.

---

## 5. Anexo — otras variables del ITT (series 2023 · 2024 · 2025 · 2026)

| Variable | Último dato (2026) | Serie 2023 · 2024 · 2025 · 2026 |
|---|---:|---|
| Lesionados en siniestros | 4 (ene–jun) | 24 · 30 · 23 · 4 |
| Muertes en siniestros | 1 (ene–jun) | 4 · 3 · 0 · 1 |
| Violencia intrafamiliar (VIF) | 17 (ene–sep) | 11 · 17 · 15 · 17 |
| Matrícula | 3.276 | 3.891 · 3.529 · 3.310 · 3.276 |
| Tasa de deserción | 5.1 % (2025) | 8.1 % · 6.2 % · 5.1 % |
| Tasa de repitencia | 9.7 % | 9.4 % · 10.4 % · 9.1 % · 9.7 % |
| Cobertura vegetal (NDVI) | 0.099 | 0.095 · 0.110 · 0.110 · 0.099 |
| Déficit habitacional | 46.1 % | de 1.158 hogares · Sisbén 2024 |
| Empleo | 885 | 834 · 881 · 898 · 885 |

---

## 6. Lámina de priorización (caracterización × territorio)

- Idea: cruzar delitos por manzana con necesidad de los hogares → "más delitos y más necesidad".
- Opciones de gráfico propuestas: correlación por manzana (scatter: → delitos, ↑ necesidad),
  proyección de cierre por dominio, alerta temprana de manzanas críticas.
- Se calcula con cifras agregadas por manzana (coherente con la regla de privacidad del proyecto).

---

## 7. Observaciones para preparar la presentación

- **Unificar el ITT:** decidir si el índice de la presentación es de 5 o 6 dimensiones (el deck añade
  Vivienda) y qué serie se publica; hoy deck y notebook no coinciden.
- **2026 es parcial** (DATIC hasta Q3, siniestros hasta Q2): marcarlo como preliminar/no comparable
  en cualquier lámina que lo compare contra años completos.
- **Riñas:** alinear el criterio (conteo amplio del deck vs filtro estricto de las capas).
- Mantener la **paleta Okabe-Ito** accesible para daltonismo en todas las gráficas del deck
  (ver `contexto_itt_ciudad_paraiso.md`).
- Las capas geoespaciales que alimentan los mapas por manzana ya están exportadas en
  `mapa_Analitico_ciudad_Paraiso/data/1_data_itt` (13 GeoJSON).

*Fuente: deck "Reporte diario PMU · Ciudad Paraíso", 17 láminas, corte 16/10/2026.*
*Contenido rephrased y estructurado para contexto del proyecto.*
