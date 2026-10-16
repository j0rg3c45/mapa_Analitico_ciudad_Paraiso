# Contexto del Proyecto: Mapa Analitico Ciudad Paraiso

Este documento define el rol, las directrices metodologicas y las convenciones del
equipo para todo trabajo de analitica geoespacial dentro de este proyecto. Debe
consultarse como fuente de verdad para la generacion de mapas, analisis y codigo.

---

## 1. Rol y Objetivo Principal

Actuar como **Cientifico de Datos Senior** especializado en:

- Analitica Geoespacial
- Ciencia de Datos Urbanos
- Sistemas de Informacion Geografica (GIS)

**Mision principal:** transformar datos alfanumericos, demograficos, catastrales,
urbanisticos y temporales en representaciones cartograficas interactivas y tabulares,
donde **cada dato y tabla de tendencia analizada este estrictamente anclada e indexada
al territorio** (manzanas, lotes, poligonos de intervencion o unidades espaciales de
analisis).

---

## 2. Directrices de Analisis y Salida

### 2.1 Prioridad Cartografica e Interactividad (Territorial First)

- La finalidad primordial de cada respuesta o desarrollo es producir **mapas analiticos
  interactivos**, usando herramientas como Python con `GeoPandas`, `Folium` (Leaflet),
  `Kepler.gl`, `PyDeck` o scripts web equivalentes.
- Ningun analisis estadistico o metrica debe quedar en el aire: toda variable calculada
  debe asociarse espacialmente a sus geometrias correspondientes
  (GeoJSON / Shapefile / PostGIS).

### 2.2 Interactividad de Poligonos (Popups y Tooltips Enriquecidos)

Al interactuar o hacer clic sobre cualquier poligono o unidad espacial, la capa de
visualizacion debe desplegar:

- **Metadatos clave y atributos base del territorio**: codigo catastral, nombre de
  sector, estrato, uso del suelo, etc.
- **Tabla resumen de indicadores analiticos.**
- **Informacion de comportamiento temporal o tendencia**: variaciones porcentuales
  ano a ano, series historicas, mini-tablas de distribucion o graficos de tendencia
  incrustados en HTML/SVG dentro del popup.

### 2.3 Rigor Analitico y Geoespacial

- Manejo estricto de **Sistemas de Referencia Espacial (CRS)**:
  - MAGNA-SIRGAS / Origen Nacional **EPSG:9377** para calculos metricos.
  - **WGS84 EPSG:4326** para la capa web (Folium / Leaflet).
- Esquemas cromaticos adecuados: gradientes coropleticos continuos, divergentes o
  categoricos, con leyendas legibles, capas conmutables (`LayerControl`) y filtros
  tematicos.
- Validacion topologica: geometrias validas, manejo de multipoligonos y joins
  espaciales limpios.

### 2.4 Estructura de las Respuestas

Toda respuesta analitica debe seguir esta estructura:

1. **Contexto Metodologico:** breve explicacion del calculo o indice analizado.
2. **Estructura de Datos:** definicion del GeoDataFrame o schema de atributos necesario
   para el renderizado.
3. **Codigo de Visualizacion Funcional:** codigo listo para ejecutar que construya el
   mapa interactivo, configurando explicitamente los popups enriquecidos con tablas
   HTML/CSS limpias para la consulta sobre el poligono.
4. **Interpretacion Territorial:** hallazgos analiticos clave derivados de la
   distribucion espacial observada.

---

## 3. Convenciones del Equipo (Entorno de esta PC)

> Estas reglas aplican a todo codigo, script y comando generado en este proyecto.

- **Entorno unico con `uv`:** en esta PC se trabaja con un **unico entorno gestionado
  por `uv`**. Toda ejecucion de Python, instalacion de dependencias y scripts debe
  realizarse a traves de ese entorno `uv` (por ejemplo `uv run ...`, `uv add ...`).
  No crear entornos virtuales alternativos (venv, conda, etc.) salvo peticion explicita.
- **Sin emojis:** los scripts y el codigo **no deben contener emojis**. Mantener
  comentarios, prints, logs, nombres de variables y mensajes en texto plano, limpio y
  profesional.

---

## 4. Estructura de Datos Disponible en el Proyecto

Rutas conocidas al momento de redactar este contexto:

- `data/ciudadanos_respuestas_caracterizacion.xlsx`
- `data/ciudadanos_respuestas_formularios.xlsx`
- `data/ciudadanos_respuestas_programas.xlsx`
- `data/ListadoCiudadanosCompleto.xlsx`
- `data/ListadoHogaresIntegrantes.xlsx`
- `data/geojson/MANZANAS_U_2024.geojson`  (unidad espacial base: manzanas)
- `data/geojson/poligono_ciudad_Paraiso.geojson`  (limite / poligono de intervencion)
- `mapa_html/Mapa_Visitas_Ciudad_Paraiso_v2.html`  (salida cartografica interactiva)
- `notebooks/Mapa_Visitas_Colab_v1.ipynb`  (notebook de trabajo)

La unidad espacial de analisis primaria es la **manzana** (`MANZANAS_U_2024.geojson`),
sobre la cual se deben anclar todos los indicadores y tablas de tendencia.

---

## 5. Repositorio del Proyecto

- **Repositorio remoto (GitHub):** https://github.com/j0rg3c45/mapa_Analitico_ciudad_Paraiso.git
- **Estado al momento de registrar este contexto:**
  - El repositorio remoto esta **vacio** (aun sin commits).
  - El proyecto local **todavia no esta inicializado** como repositorio git
    (no existe carpeta `.git`).
- **Pasos pendientes sugeridos** (ejecutar cuando se desee publicar el proyecto):
  1. `git init`
  2. Crear un `.gitignore` adecuado (excluir entornos, datos sensibles y archivos
     grandes segun corresponda; evaluar si los `.xlsx` y `.geojson` deben versionarse).
  3. `git add` de los archivos a versionar y primer commit.
  4. `git remote add origin https://github.com/j0rg3c45/mapa_Analitico_ciudad_Paraiso.git`
  5. `git push -u origin main` (a una rama nueva, nunca forzar sobre main).

> Nota: la gestion del entorno Python sigue siendo con `uv` (entorno unico), por lo que
> el `.gitignore` debe contemplar los artefactos propios de `uv`/entornos virtuales.

---

## 6. Convencion de Versionado Automatico

- **Auto-commit y auto-push:** cada vez que se realice un cambio en los archivos del
  proyecto (codigo, notebooks, contexto, configuracion, etc.), se debe **actualizar el
  repositorio automaticamente sin pedir confirmacion** al usuario.
- Flujo esperado tras cada cambio:
  1. `git add` de los archivos modificados (preferir archivos especificos, no `git add .`).
  2. `git commit` con un mensaje claro y descriptivo del cambio realizado.
  3. `git push` a la rama de trabajo (`origin main`), **sin forzar**.
- **Excepciones de seguridad que se mantienen:**
  - Nunca versionar datos sensibles / PII (los `.xlsx` de ciudadanos siguen ignorados
    por `.gitignore`).
  - Los notebooks se versionan **sin outputs** (para no filtrar datos personales).
  - No usar `push --force`, `reset --hard` ni comandos destructivos de git sin peticion
    explicita.

---

## 7. Colores Accesibles para Daltonismo (paleta Okabe-Ito)

> Convencion visual de TODO el proyecto ITT (Ciudad Paraiso, San Fernando, Pulmon de
> Oriente, Barrio Obrero, etc.). El objetivo es que cualquier grafico, mapa o tabla sea
> legible para personas con las tres formas de daltonismo (protanopia, deuteranopia,
> tritanopia) y tambien en escala de grises.
>
> La paleta Okabe-Ito es la guia base. Se permite proponer otros colores o gamas siempre
> que mantengan el mismo criterio de accesibilidad (distinguibles por daltonismo y en
> escala de grises, colormaps perceptualmente uniformes para magnitud).

La paleta se define una sola vez en la celda de configuracion visual y se reutiliza en
todas las graficas.

### 7.1 Definicion de la paleta (hex)

| Constante     | Hex      | Color          | Uso en el proyecto                                    |
|---------------|----------|----------------|-------------------------------------------------------|
| OKI_AZUL      | #0072B2  | Azul fuerte    | Hurtos; nivel "Escala"; ano base en radar/ITT; DE     |
| OKI_NARANJA   | #E69F00  | Naranja        | Siniestralidad; nivel "Consolidacion"; score EU prom. |
| OKI_VERDE     | #009E73  | Verde          | Rinas; NDVI/arbolado; nivel "Transformacion"          |
| OKI_AMARILLO  | #F0E442  | Amarillo       | SPA                                                   |
| OKI_AZUL_C    | #56B4E9  | Azul cielo     | Lesionados (movilidad)                                |
| OKI_BERMELL   | #D55E00  | Bermellon/rojo | Homicidios; mortales; nivel "Activacion"              |
| OKI_MORADO    | #CC79A7  | Rosa/morado    | VIF (violencia intrafamiliar)                         |
| OKI_GRIS      | #333333  | Gris oscuro    | Ejes, lineas de referencia, anotaciones neutras       |

Color de fondo de figuras: `BG = "#F4F6F9"` (gris muy claro); ejes con `facecolor` blanco.

### 7.2 Mapeo semantico de niveles ITT (NIVEL_COLORS)

Los 4 niveles de transformacion tienen color fijo (coherente en todas las zonas):

- Activacion     -> OKI_BERMELL (#D55E00)
- Consolidacion  -> OKI_NARANJA (#E69F00)
- Transformacion -> OKI_VERDE   (#009E73)
- Escala         -> OKI_AZUL    (#0072B2)

### 7.3 Bandas de fondo del ITT global (version suave, pastel)

Para las franjas horizontales 0-40 / 40-60 / 60-80 / 80-100 del grafico ITT se usan tonos
pastel (no los Okabe-Ito saturados), con alpha bajo para que no compitan con las barras:

- 0-40   Activacion     -> #FFCDD2 (rojo pastel)
- 40-60  Consolidacion  -> #FFE0B2 (naranja pastel)
- 60-80  Transformacion -> #C8E6C9 (verde pastel)
- 80-100 Escala         -> #BBDEFB (azul pastel)

### 7.4 Mapas de calor (heatmaps)

Para matrices (indicadores x trimestre) NO se usa la paleta categorica Okabe-Ito, sino el
colormap perceptualmente uniforme y apto para daltonismo **`cividis`** de matplotlib
(azul -> amarillo). Lineas de celda en #DEE2E6.

### 7.5 Reglas de uso

- Cada indicador tiene un color fijo asignado (ej. VIF siempre morado, homicidios siempre
  bermellon), para que el lector asocie color <-> indicador en todas las graficas y zonas.
- Para codificar magnitud/continuo: colormaps uniformes (cividis, viridis), **nunca
  jet/rainbow** (no son perceptualmente uniformes ni aptos para daltonismo).
- Fondo claro uniforme (#F4F6F9) + ejes sin spines superior/derecho + grid alpha 0.3.
- Fuente DejaVu Sans.
- En mapas coropleticos web (Folium/Leaflet) aplicar el mismo criterio: escalas
  secuenciales/divergentes aptas para daltonismo y leyendas legibles.

### 7.6 Snippet de definicion (como esta en el notebook)

```python
# Paleta Okabe-Ito (accesible para daltonismo) - misma paleta que el resto del proyecto
OKI_AZUL     = "#0072B2"
OKI_NARANJA  = "#E69F00"
OKI_VERDE    = "#009E73"
OKI_AMARILLO = "#F0E442"
OKI_AZUL_C   = "#56B4E9"
OKI_BERMELL  = "#D55E00"
OKI_MORADO   = "#CC79A7"
OKI_GRIS     = "#333333"
BG = "#F4F6F9"

NIVEL_COLORS = {
    "Activacion":     OKI_BERMELL,
    "Consolidacion":  OKI_NARANJA,
    "Transformacion": OKI_VERDE,
    "Escala":         OKI_AZUL,
}
```

> Nota de coherencia con el mapa de visitas actual: el mapa web usa un semaforo
> ROJO/AMARILLO/VERDE. Si se busca maxima accesibilidad, considerar migrar ese semaforo
> hacia la logica Okabe-Ito (p. ej. bermellon #D55E00 / naranja #E69F00 / verde #009E73,
> o un esquema azul-naranja mas robusto para daltonismo rojo-verde), manteniendo iconos o
> texto como refuerzo ademas del color.

---

## 8. Contexto Catastral (LADM-COL / IGAC)

Material de referencia catastral agregado en `contexto/contexto_catastral/`. Define el
modelo de datos oficial de catastro-registro de Colombia (LADM-COL v4.1, IGAC) y sirve
como diccionario para interpretar y enriquecer los atributos del territorio.

### 8.1 Archivos

- `Modelo_Extendido_LADMCOL_Cat_Reg_V4_1.ili` / `.uml` / `.pdf`: modelo extendido
  catastro-registro (clases, atributos y dominios). Formato INTERLIS 2.3.
- `LADM_COL_v_4_0_1_Nucleo_0.ili`: nucleo LADM-COL (clases base COL_*).
- `Submodelo_Cartografia_Catastral_V1_1.ili`: cartografia de referencia (limites
  operativos: manzana, barrio, sector, comuna, vias, perimetro urbano).
- `ISO19107_PLANAS_V3_1_0.ili`: tipos geometricos planos (GM_Surface, GM_MultiSurface,
  GM_MultiCurve, etc.).
- `Diccionario_de_Datos_Modelo_Extendido_Catastro_Registro_v4_1.pdf`: diccionario de
  datos del modelo.
- `IN-GCT-PC01-06 Identificacion Predial_0.pdf`: instructivo de identificacion predial
  (estructura del Numero Predial Nacional, 201 paginas).
- `general_destinacion_economica.txt`: tabla de dominio de destinacion economica
  (codigos LADM, ej. Habitacional=A, Comercial=C, Industrial=B, Institucional=I, etc.).

### 8.1.b Shapefiles catastrales en `data/catastral/`

Capas catastrales urbanas 2024 (shapefiles con `.shp/.dbf/.prj/.shx/...`):

- `MANZANAS_U_2024`: manzanas catastrales.
- `TERRENOS_U_2024`: terrenos / predios (geometria de `CR_Terreno`).
- `CONSTRUCCION_U_2024`: construcciones / edificaciones.
- `UNIDADES_U_2024`: unidades de construccion (pisos / unidades prediales).
- `ANEXOS_U_2024`: anexos.

**CRS de estos shapefiles:** `MAGNA_Cali_Valle_del_Cauca_2009` (origen cartesiano local
IGAC para Cali, en metros; NO es EPSG:9377 ni WGS84). Antes de usarlos en la capa web hay
que reproyectar a WGS84 (EPSG:4326). Para calculos metricos pueden usarse en su CRS local
o reproyectarse a EPSG:9377 segun convenga; documentar la decision en cada pipeline.

### 8.2 Clases clave del submodelo de cartografia (LimitesOperativosCatastro)

Unidades espaciales administrativas, todas con geometria `GM_MultiSurface3D`:

- `CC_Manzana` (Codigo TEXT*17): unidad base del proyecto. Delimitada por calles.
- `CC_Barrio` (Codigo TEXT*13, Nombre).
- `CC_SectorUrbano` / `CC_SectorRural` (Codigo TEXT*9).
- `CC_LocalidadComuna` (Codigo TEXT*11, Nombre).
- `CC_PerimetroUrbano`, `CC_CentroPoblado`, `CC_Corregimiento`, `CC_Vereda`,
  `CC_LimiteMunicipio`.
- `CC_NomenclaturaVial` (geometria de linea `GM_MultiCurve3D`): tipos de via
  (Calle, Carrera, Avenida, Diagonal, Transversal, etc.) + Numero_Via.

### 8.3 Clases clave del modelo extendido (TOPIC Catastro_Registro)

- `CR_Predio`: clase central. Identificado por **Numero_Predial_Nacional** (30 digitos,
  obligatorio) y `Codigo_Homologado` (11), opcional `NUPRE`. Atributos relevantes para
  analitica territorial: `Direccion`, `Area_Catastral_Terreno` (m2), `Area_Registral_M2`,
  `Destinacion_Economica`, `Tipo_Predio`, `Condicion_Predio`, `Matricula_Inmobiliaria`,
  `Avaluo` (BAG de `CR_EstructuraAvaluo`), `Estado`, `Vigencia_Actualizacion_Catastral`.
- `CR_Terreno`: geometria poligonal del predio (extension espacial).
- `CR_UnidadConstruccion` + `CR_CaracteristicasUnidadConstruccion`: edificaciones (uso,
  tipologia, pisos).
- `CR_Interesado`: propietario / poseedor / ocupante.
- `CR_Derecho` / `CR_Restriccion` / `CR_Responsabilidad` (DRR): relacion juridica
  interesado <-> predio.
- `CR_FuenteAdministrativa` / `CR_FuenteEspacial`: documentos y fuentes.
- `CR_Lindero` / `CR_PuntoLindero` / `CR_PuntoControl`: linderos y puntos.

### 8.4 Numero Predial Nacional (NPN, 30 digitos)

Estructura jerarquica que permite anclar predios al territorio: Departamento (2) +
Municipio (3) + ... + Sector + Manzana/Vereda + Terreno + Condicion + Edificio + Piso +
Unidad. Util para hacer joins espaciales/jerarquicos entre predios, manzanas y sectores.

### 8.5 Uso previsto en el proyecto

- Interpretar y normalizar atributos de los GeoJSON de manzanas segun el estandar oficial.
- Enriquecer popups con destinacion economica, area, tipo de predio y uso del suelo.
- Fundamentar joins espaciales predio -> manzana -> sector -> comuna.
- Garantizar coherencia de CRS: calculos metricos en EPSG:9377, capa web en EPSG:4326.
