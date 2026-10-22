# -*- coding: utf-8 -*-
"""Empaqueta los mapas ITT de Barrio Obrero (ambas zonas) en un unico ZIP para
compartir. Dentro del ZIP, los mapas quedan organizados en dos subcarpetas:
  01_poligono_completo/  (45 manzanas)
  02_poligono_v1/        (16 manzanas)
mas un LEEME.txt. Salida en compartir_itt_mapas/.

Ejecutar en el entorno uv unico del proyecto:
  & "C:\\Users\\Jorge\\.venv\\Scripts\\python.exe" notebooks/98c_empaquetar_itt_bo.py
"""
import os
import zipfile
from datetime import date

# Resolucion de rutas (local / Colab).
BASE = None
for _b in [os.path.join("..", "mapa_html", "Barrio_obrero"),
           os.path.join("mapa_html", "Barrio_obrero"),
           "/content/mapa_html/Barrio_obrero"]:
    if os.path.isdir(_b):
        BASE = os.path.abspath(_b)
        break
if BASE is None:
    raise FileNotFoundError("No se encontro mapa_html/Barrio_obrero/.")

RAIZ = os.path.dirname(os.path.dirname(BASE))  # .../mapa_Analitico_ciudad_Paraiso
OUT = os.path.join(RAIZ, "compartir_itt_mapas")
os.makedirs(OUT, exist_ok=True)

ZONAS = [
    ("Barrio_obrero_actual", "01_poligono_completo", "Poligono oficial (45 manzanas)"),
    ("Barrio_obrero_v1", "02_poligono_v1", "Poligono V1 (16 manzanas)"),
]

LEEME = """MAPAS INTERACTIVOS - ITT BARRIO OBRERO (Cali)
=============================================

Que es esto
-----------
Suite de mapas del Indice de Transformacion Territorial (ITT) de la zona de
estudio Barrio Obrero (Comuna 9), por dimension, para los DOS poligonos:

  01_poligono_completo/  -> poligono oficial, 45 manzanas (37.7 ha).
  02_poligono_v1/        -> poligono V1, 16 manzanas (13.6 ha).

Cada carpeta trae 6 mapas (uno por dimension del ITT):
  01 Seguridad .............. homicidios y hurtos (puntos + calor).
  02 Movilidad .............. siniestros por severidad + red peatonal.
  03 Convivencia / Social ... VIF (solo calor), rinas y SPA.
  04 Entorno Urbano ......... censo arboreo por estado + NDVI (4 anios) + CAI.
  05 Desarrollo Economico ... negocios por tipo + sedes educativas.
  06 Deficit de Vivienda .... deficit habitacional por sector (SISBEN).

Como abrir los mapas
--------------------
1. Descomprime este archivo ZIP en una carpeta (clic derecho > Extraer todo).
   IMPORTANTE: manten las subcarpetas y sus archivos .html juntos.
2. Haz doble clic en cualquier  *.html  para abrirlo en el navegador.

Requisitos
----------
- Conexion a internet (el fondo del mapa y las graficas cargan desde internet).
- Navegador recomendado: Google Chrome o Microsoft Edge.

Como usar cada mapa
-------------------
- 4 capas base conmutables (OpenStreetMap activa, Esri Satelite, Google Streets,
  Google Satelite).
- Control de capas (arriba a la derecha): todas inician apagadas salvo el limite.
  Prende las capas de puntos y de calor que quieras ver.
- Control de intensidad del calor (abajo a la derecha).
- Panel flotante (abajo a la izquierda): resumen de la zona y serie de tiempo
  2023-2026 con el score oficial del ITT por dimension.

Notas tecnicas
--------------
- Scores del ITT: fuente oficial CDO Alcaldia de Santiago de Cali (consolidado
  2023-2026). El corte 2026 es parcial (no comparable, anio no cerrado).
- Paleta apta para daltonismo (Okabe-Ito) y mapas de calor en escala cividis.
- VIF se muestra SOLO como densidad/calor (nunca puntos), por privacidad de las
  victimas.

Nota de privacidad
------------------
Informacion territorial agregada. No publicar en sitios de acceso abierto;
compartir solo por canales internos autorizados.

Fuente: ITT Barrio Obrero - CDO Alcaldia de Santiago de Cali.
Generado: __FECHA__
"""

fecha = date.today().isoformat()
zip_nombre = "Mapas_ITT_Barrio_Obrero_" + fecha + ".zip"
zip_path = os.path.join(OUT, zip_nombre)
carpeta_zip = "Mapas_ITT_Barrio_Obrero"

total = 0
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.writestr(carpeta_zip + "/LEEME.txt", LEEME.replace("__FECHA__", fecha))
    for sub_src, sub_zip, _desc in ZONAS:
        d = os.path.join(BASE, sub_src)
        if not os.path.isdir(d):
            print("Aviso: no existe", d)
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".html"):
                z.write(os.path.join(d, f), carpeta_zip + "/" + sub_zip + "/" + f)
                total += 1

tam_mb = os.path.getsize(zip_path) / (1024 * 1024)
print("ZIP creado:", zip_path)
print("Mapas incluidos:", total, "(+ LEEME.txt)")
print("Tamano del ZIP: %.1f MB" % tam_mb)
if tam_mb > 23:
    print("ADVERTENCIA: supera ~23 MB; comparte por enlace (OneDrive/Drive/Teams).")
else:
    print("Cabe en un correo estandar (limite ~25 MB).")
