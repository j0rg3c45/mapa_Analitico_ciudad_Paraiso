# Contexto: Deck / Reporte Diario del PMU - Ciudad Paraiso

Documento de referencia del material en `contexto/contexto_deck/`. Describe la plantilla
del **Reporte Diario del PMU** (Puesto de Mando Unificado · Recuperacion Centro, Ciudad
Paraiso) que servira de guia para un proceso que el usuario solicitara mas adelante
(probablemente generar/alimentar este deck con los datos reales del proyecto).

> Convenciones del proyecto aplicables: entorno unico `uv`, codigo sin emojis, paleta
> Okabe-Ito accesible, datos agregados sin PII (conteos menores de 5 agrupados), y
> versionado automatico. Ver `contexto_rol_analitica_geoespacial.md`.

---

## 1. Que es

Archivo: `contexto/contexto_deck/Reporte diario PMU - Ciudad Paraiso.pdf` (~3.06 MB).

Es un **deck ejecutivo** (plantilla / boceto para revision del equipo, fechado 16 de
octubre de 2026) con placeholders tipo `[__]`, `[dia, hora]`, `[indicador clave]`. Resume
en formato de presentacion el avance diario de la operacion de recuperacion del centro de
Cali en el poligono Ciudad Paraiso. Esta pensado como salida de comunicacion, alimentada
por las mismas cifras del ITT y la caracterizacion que ya maneja el proyecto.

---

## 2. Estructura del deck (laminas)

1. **Portada:** "PMU · Recuperacion Centro · Ciudad Paraiso · Reporte diario". Corte por
   dia y hora.
2. **Lectura del dia - "Hoy en tres mensajes":** 1) que avanzo, 2) donde intervenir,
   3) que se decide hoy.
3. **Avance de la operacion - Caracterizacion por manzana:** barra de avance global
   (ej. 56,6 % · 469 de 828 personas), delta desde el ultimo reporte, nº de manzanas,
   manzanas con padrino, cierre estimado, estado frente a la meta. Mapa ilustrativo por
   manzana. Fuente: Gob 24/7.
4. **Resultados por dominio** (una lamina por dominio, con base poblacional, indicador
   clave, delta y mapa coropletico por manzana "Menos -> Mas"):
   - Salud (base 257 personas con formulario de Salud).
   - Vivienda (base 210 hogares).
   - Bienestar (base [n] personas en programas).
5. **Territorio - series por dominio** (serie trimestral/anual desde linea base 2023,
   con mapa ilustrativo):
   - Convivencia · Rinas (desde 327 casos linea base 2023).
   - Convivencia · Sustancias psicoactivas (SPA): 135 en 2026 ene-sep, +96 % vs 2025.
   - Movilidad · Siniestros viales: 5 en 2026 ene-jun, -69 % vs 2025 (linea base 33).
   - Desarrollo economico · Establecimientos activos: 311 empresas con matricula vigente
     en 2026, -4 % vs 2025, +32 % vs 2023 (linea base 236).
6. **Territorio - Resumen · Indice de Transformacion Territorial (ITT):** cifra 0-100 y
   fase. Serie: **2023=45,1 · 2024=53,9 · 2025=57,6 · 2026=66,4** (fase de
   transformacion). Dimensiones que resume: Seguridad, Movilidad, Desarrollo social,
   Entorno urbano, Vivienda, Desarrollo economico.
7. **Caracterizacion x territorio - "Donde priorizar":** dispersion donde cada punto es
   una manzana (eje -> delitos, eje ^ necesidad de los hogares). Cuadrante de prioridad
   (mas delitos + mas necesidad). Opciones de lamina: correlacion por manzana, proyeccion
   de cierre por dominio, alerta temprana de manzanas criticas.
8. **Anexo - Otras variables del ITT** (cifra grande = ultimo dato; series 2023-2026):
   - Lesionados en siniestros viales: 4 (serie 24·30·23·4 ene-jun).
   - Muertes en siniestros viales: 1 (serie 4·3·0·1 ene-jun).
   - Violencia intrafamiliar (VIF): 17 (serie 11·17·15·17 ene-sep).
   - Matricula: 3.276 (serie 3.891·3.529·3.310·3.276).
   - Tasa de desercion: 5,1 % · Tasa de repitencia: 9,7 %.
   - Cobertura vegetal (NDVI): 0,099 (serie 0,095·0,110·0,110·0,099).
   - Deficit habitacional: 46,1 %.
   - Empleo: 885 de 1.158 hogares (Sisben 2024; serie 834·881·898·885).

---

## 3. Convenciones de contenido observadas en el deck

- **Cortes temporales** siempre rotulados: "Corte: [dia, hora]" y la fuente institucional
  (Gob 24/7, Secretaria de Seguridad, Movilidad, Camara de Comercio, Sisben, etc.).
- **Proteccion de datos:** "Conteos menores de 5 agrupados" (coherente con la regla
  MIN_N del proyecto).
- **Series desde linea base 2023** con comparacion interanual y variacion porcentual.
- **Mapas por manzana** descritos como "ilustrativos", escala "Menos -> Mas".
- Dominios del ITT: Seguridad, Movilidad, Desarrollo social, Entorno urbano, Vivienda,
  Desarrollo economico.

---

## 4. Relacion con los datos del proyecto

El deck consume cifras que YA se trabajan o estan disponibles en el repo:

- **Caracterizacion por manzana / dominios** (Salud, Vivienda, Bienestar): ver el mapa de
  avance de caracterizacion (`notebooks/02_mapa_geoanalitica_itt.ipynb`, seccion 11).
- **Seguridad** (hurto, rina, SPA, homicidio): fuente oficial `data/1_data_itt/` (capas
  02-05); mapa en `notebooks/02_mapa_geoanalitica_itt.ipynb` seccion 12.
- **Entorno urbano** (NDVI 2023-2026, censo arboreo, deficit habitacional): datos en
  `data/5_Dimension_Entorno_Urbano/` (pendiente de integrar en su mapa dedicado).
- **ITT** (indice y niveles): seccion 5 del notebook.

Nota: el deck trae valores de ejemplo/preliminares (ej. ITT 66,4; avance 56,6 %) que
pueden diferir de los calculos actuales del notebook (p. ej. el avance real por manzana
geolocalizado dio ~39,4 % global). Al generar el reporte real habra que alinear las
cifras con la fuente definitiva de cada dominio.

---

## 5. Proceso probable a solicitar (hipotesis, a confirmar con el usuario)

Generar/alimentar este deck con datos reales del proyecto. Posibles enfoques:
- Un script que calcule las cifras por dominio y las exporte (JSON/Excel) para llenar los
  placeholders del deck.
- O una version HTML del reporte (coherente con la arquitectura de mapas actual) con las
  laminas, series y mini-mapas por manzana.

Pendiente: confirmar con el usuario el formato de salida (PDF/PowerPoint vs HTML), la
periodicidad (diaria) y la fuente oficial de cada cifra.
