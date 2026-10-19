# Datos de referencia: serie IPM Cali, NDVI por zona e IPM comparativo

Datos de contexto aportados por el equipo (DANE / Estadisticas Distritales y calculo
propio de NDVI). Sirven como marco comparativo para interpretar los indices de Ciudad
Paraiso. Usar coma como separador decimal en textos; punto en codigo.

---

## 0. Como interpretar el IPM (guia de lectura)

La escala del IPM funciona igual que una **tasa de reprobados en un salon de clases**.
Va de 0% a 100% (o 0.0 a 1.0) y representa el **porcentaje de personas que viven en
hogares pobres multidimensionalmente**.

- **0%:** en esa zona nadie es pobre multidimensional (cero carencias criticas acumuladas).
- **100%:** en esa zona todos son pobres multidimensionales.
- **12,59% (media Cali urbano):** de cada 100 personas, ~13 viven en hogares que acumulan
  33% o mas de privaciones basicas.
- **26,52% (Ciudad Paraiso):** de cada 100 personas, casi 27 viven en hogares con
  privaciones criticas acumuladas (mas del doble que el promedio de la ciudad).
- **7,51% (Roosevelt):** de cada 100 personas, solo ~7-8 estan en esa condicion.

### Escala de referencia estandar para Colombia (area urbana)

Aunque tecnicamente llega a 100%, en ciudades colombianas los valores urbanos se
clasifican asi:

| Rango IPM (%) | Nivel | Significado practico | Ejemplo en el estudio |
| :--- | :--- | :--- | :--- |
| 0,0 - 8,0 | Muy bajo / Bajo | Zonas consolidadas (estratos 4-6). Cobertura casi total de servicios, empleo formal, buen nivel educativo. | Roosevelt (7,51%) |
| 8,1 - 15,0 | Medio / Tipico urbano | Promedio de una capital. Servicios basicos y vivienda aceptable, pero pesa la informalidad o adultos sin bachillerato. | Cali urbano (12,59%), Barrio Obrero (13,18%) |
| 15,1 - 25,0 | Alto | Sectores populares vulnerables. Alta desercion escolar, hacinamiento frecuente, empleo informal generalizado. | Comunas perifericas de ladera u oriente |
| > 25,0 | Critico / Severo | Zonas deprimidas, inquilinatos precarios o asentamientos informales. Se acumulan fallas de vivienda, saneamiento, educacion e ingresos. | Ciudad Paraiso (26,52%) |

### El "truco" de las dos etapas (no confundir dos porcentajes)

Hay DOS porcentajes distintos que suelen confundirse:

1. **El 33% (el examen del hogar):** regla fija para decidir si UN hogar es pobre. A cada
   hogar se le suman sus carencias (pisos de tierra, no cotizar pension, ninos sin
   estudiar, etc.). Si suma 33% o mas, ese hogar "reprobo" y se cataloga como pobre.
2. **El IPM final (el reporte de la zona):** el porcentaje de gente de la zona que vive en
   esos hogares que "reprobaron".

En resumen: el IPM de las tablas (7,51% · 13,18% · 26,52%) es el **porcentaje de
habitantes en situacion de pobreza multidimensional en cada poligono**. Entre mas alto el
numero, mas pobre y vulnerable es la zona.

> Nota de uso en los mapas: en las coropletas por manzana el valor `ipm` es el indice
> 0-100 de cada manzana (misma logica: mayor = mas pobreza). La paleta viridis refuerza
> la lectura (ver `contexto_ipm_ics.md`).

---

## 1. Serie anual de incidencia del IPM en Cali (medida estandar)

Medida estandar de referencia del IPM: **porcentaje de hogares en pobreza
multidimensional** (hogar pobre si `IPM >= 33.3%`). Fuente:
`Estadisticas_Distritales_IPM_periodica.xlsx`, serie anual de Cali.

| Año | Incidencia IPM (Cali) |
| :--- | ---: |
| 2019 | 8,92 % |
| 2020 | 9,39 % |
| 2021 | 13,27 % |
| 2022 | 13,29 % |
| 2023 | 11,17 % |
| 2024 | 20,04 % |
| 2025 | 22,43 % |

> Ojo: esta "incidencia" (% de hogares pobres) es distinta del **IPM promedio por
> manzana** usado en los mapas del proyecto (que es el valor del indice 0-100 por
> manzana). Son dos lecturas complementarias: la incidencia mide cuantos hogares superan
> el umbral; el IPM promedio mide el nivel medio de privacion.

---

## 2. IPM comparativo por zona de estudio

Valor del **IPM promedio por manzana** (indice 0-100) en las zonas de estudio del
proyecto.

| Zona | Manzanas con IPM | IPM Promedio |
| :--- | ---: | ---: |
| Cali (urbano) | 12.787 | 12,59 |
| Barrio Obrero | 11 | 13,18 |
| Roosevelt | 21 | 7,51 |
| Ciudad Paraiso | 33 | 26,52 |

- **Ciudad Paraiso es la zona con mayor privacion** (26,52), mas del doble del promedio
  urbano de Cali (12,59).
- Coherente con la guia `contexto_ipm_ics.md` (que tambien reporta Ciudad Paraiso 26,52,
  ICS promedio 23,07 y top privaciones: Informalidad 89,7%, Bajo logro educativo 59,7%).

---

## 3. NDVI (Indice de Vegetacion de Diferencia Normalizada)

### 3.1 Rango general en Cali
NDVI de Santiago de Cali entre **-0,20 y 0,85**, diferenciado entre casco urbano
consolidado y periferia rural/ecologica:

- **Zonas densamente urbanizadas e infraestructura (-0,10 a 0,25):** alta concentracion de
  asfalto, concreto y tejido residencial compacto (centro historico, comunas del
  oriente / Distrito de Aguablanca). Vegetacion casi nula.
- **Vegetacion urbana media y zonas mixtas (0,25 a 0,50):** espacios residenciales
  arbolados, separadores viales, parques barriales y dosel discontinuo (sur, oeste y
  franjas intermedias).

### 3.2 NDVI medio anual por zona de estudio
Calculado con el metodo del proyecto: media del raster descartando nodata y centinelas
(-9999).

| Zona | 2023 | 2024 | 2025 | 2026 | Tendencia 23->26 |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Ciudad Paraiso | 0,0948 | 0,1102 | 0,1100 | 0,0993 | +0,0045 |
| Barrio Obrero | 0,0687 | 0,0809 | 0,0804 | 0,0688 | +0,0001 |
| Corredor San Fernando / Yawa | 0,1787 | 0,2157 | 0,2122 | 0,2166 | +0,0379 |
| Pulmon de Oriente | 0,1808 | 0,1886 | 0,2043 | 0,2028 | +0,0220 |
| Roosevelt | 0,1282 | 0,1727 | 0,1704 | 0,1637 | +0,0355 |
| Avenida Ciudad de Cali (8 tramos)* | 0,2239 | 0,2299 | 0,2392 | 0,2309 | +0,0070 |

\* Avenida Ciudad de Cali medida en 8 tramos.

- **Ciudad Paraiso** tiene NDVI bajo (0,09-0,11; zona muy urbanizada, poca vegetacion),
  con leve mejora 2023->2026 (+0,0045). Coherente con el mapa de Entorno Urbano (nb 03),
  que usa el NDVI anual de la zona.
- Las zonas con mas vegetacion son el Corredor San Fernando/Yawa y el Pulmon de Oriente.

---

## 4. Relacion con los mapas del proyecto

- **IPM/ICS por manzana:** mapas `08_mapa_ipm` (viridis) y `10_mapa_ics` (cividis); capas
  de referencia en los mapas de dimension (02-07); laboratorio `09_lab_itt_ipm`.
- **NDVI anual:** mapa de Entorno Urbano `03_mapa_entorno_urbano` (rasters por anio
  2023-2026).
- Estas tablas son el marco COMPARATIVO entre zonas; los mapas muestran el detalle
  intra-zona (por manzana) de Ciudad Paraiso.
