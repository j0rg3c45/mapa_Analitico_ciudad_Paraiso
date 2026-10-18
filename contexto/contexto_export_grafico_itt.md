# Contexto: Salida grafica del ITT (export PDF/JPG desde el HTML) para presentacion

Documento de referencia para una funcionalidad solicitada: generar, **desde dentro del
mapa HTML**, una salida grafica (PDF o JPG) con el estilo del deck del PMU, apta para
presentaciones. Basado en el material de `contexto/contexto_deck/` (Reporte diario PMU).

> Convenciones del proyecto: HTML autonomo (Folium + Leaflet), paleta Okabe-Ito accesible,
> datos agregados sin PII (conteos < 5 agrupados), entorno unico, codigo sin emojis.
> Ver `contexto_deck_reporte_pmu.md` (estructura del deck) y
> `contexto_mapa_y_generacion_html.md` (arquitectura de los mapas).

---

## 1. Objetivo

Que el usuario pueda, desde el visor HTML del ITT, **exportar una lamina/figura** (del
mapa y/o de las tarjetas analiticas) a **PDF o JPG** con un formato limpio tipo deck, para
pegar en una presentacion. La funcionalidad vive dentro del propio HTML (un boton), sin
depender de herramientas externas ni de reejecutar el notebook.

---

## 2. Que formato de salida se busca (del deck PMU)

El deck `contexto/contexto_deck/Reporte diario PMU - Ciudad Paraiso.pdf` define el estilo:

- Lamina por dominio con: titulo, cifra grande (indicador clave), delta vs periodo
  anterior, un mini-mapa coropletico por manzana ("Menos -> Mas") y el corte/fuente.
- Lamina resumen del **ITT**: cifra 0-100, fase, y serie 2023-2026
  (45,1 / 53,9 / 57,6 / 66,4).
- Lamina "Donde priorizar": dispersion por manzana (delitos vs necesidad).
- Rotulos de corte ("Corte: [dia, hora]") y fuente institucional en cada lamina.
- Paleta accesible, fondo claro, tipografia sobria.

La salida grafica debe acercarse a ese formato: encabezado con titulo + corte, el mapa o
grafico centrado, leyenda y pie con la fuente.

---

## 3. Enfoque tecnico propuesto (boton de export dentro del HTML)

Como los mapas son HTML autonomos con Leaflet, la via mas directa es capturar el DOM del
mapa a imagen en el navegador y ofrecer descarga. Opciones (todas por CDN, sin build):

### 3.1 JPG/PNG - captura de pantalla del mapa (recomendado para imagen)
- Librerias: **leaflet-easyPrint** (boton nativo de Leaflet que exporta el mapa visible a
  PNG) o **html2canvas** (captura cualquier div del DOM a canvas -> PNG/JPG).
- Flujo: boton "Exportar imagen" -> html2canvas sobre el contenedor del mapa (+ panel y
  leyenda) -> `canvas.toDataURL('image/jpeg', 0.95)` -> link de descarga automatico.
- Pros: simple, 100% en el navegador, respeta lo que se ve (capas activas, zoom).
- Contras: los tiles base externos (Google/Esri) pueden no capturarse por CORS; mitigacion:
  exportar solo las capas vectoriales/overlays, o usar un tile con CORS habilitado, o
  capturar sobre fondo claro sin tiles.

### 3.2 PDF - componer una lamina
- Librerias: **jsPDF** (+ la imagen de html2canvas). Se arma un PDF A4/16:9 con encabezado
  (titulo + corte + fuente), la imagen del mapa y la leyenda.
- Flujo: html2canvas -> imagen -> `jsPDF` agrega titulo, imagen y pie -> `doc.save()`.
- Permite varias laminas (una por dominio/capa activa) en un mismo PDF.

### 3.3 Alternativa de alta fidelidad (fuera del HTML)
- Si se requiere calidad de impresion (vectorial real), se puede generar el PDF/PNG desde
  Python en el notebook (matplotlib/geopandas plot con la paleta Okabe-Ito, o
  folium + selenium/playwright para captar el mapa). Esto NO cumple el requisito de "boton
  dentro del HTML", pero sirve como respaldo para el deck oficial.

Recomendacion: implementar 3.1 (JPG) + 3.2 (PDF) con html2canvas + jsPDF por CDN, como un
control flotante en el mapa. Mantener el respaldo 3.3 para laminas de alta calidad.

---

## 4. Diseno del control de export (dentro del mapa)

- Boton/control Leaflet flotante (esquina), z-index alto, que no tape la navegacion.
- Opciones: "Exportar JPG" y "Exportar PDF".
- Antes de capturar: incrustar un encabezado temporal con Titulo + "Corte: fecha/hora" +
  fuente, y la leyenda; luego capturar; luego restaurar la vista.
- Nombre de archivo sugerido: `ITT_<mapa>_<AAAA-MM-DD>.jpg|pdf`.
- Respetar accesibilidad (contraste) y marcar "Datos sinteticos (demo)" si aplica.

---

## 5. Datos del ITT para las laminas (fuente)

- Serie ITT por anio (del deck): 2023=45,1 / 2024=53,9 / 2025=57,6 / 2026=66,4
  (fase transformacion).
- Dimensiones: Seguridad, Movilidad, Desarrollo social, Entorno urbano, Vivienda,
  Desarrollo economico.
- Mapas y capas disponibles: ver `data/1_data_itt/` (seccion 10 del contexto de mapas) y
  los 4 mapas HTML del proyecto (seccion 9).
- Nota: el `itt` por manzana en `01_manzanas_itt_consolidado` esta uniforme (58.5) y los
  scores por dimension vacios; para laminas por manzana con color real falta calcular el
  ITT por manzana (pendiente de fondo).

---

## 6. Pendiente de confirmar con el usuario

1. Formato preferido: JPG, PDF, o ambos.
2. Alcance de la captura: solo el mapa, o mapa + panel analitico + leyenda (lamina
   completa estilo deck).
3. En que mapa(s) va el boton de export (seguridad, entorno urbano, un futuro mapa ITT
   resumen, o todos).
4. Si se desea multi-lamina (un PDF con varias dimensiones) o una sola figura por descarga.
