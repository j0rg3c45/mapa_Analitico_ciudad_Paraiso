# -*- coding: utf-8 -*-
"""Empaqueta los mapas HTML del ITT en un unico ZIP listo para enviar por correo.

Copia los HTML de data_processed_geo/ a una carpeta temporal junto con un
README (LEEME.txt), y genera un ZIP en output/ con fecha. El ZIP se abre
descomprimiendo y haciendo doble clic en index.html.

Ejecutar en el entorno uv unico del proyecto:
  & "C:\\Users\\Jorge\\.venv\\Scripts\\python.exe" notebooks/98_empaquetar_mapas.py
"""
import os
import shutil
import zipfile
import tempfile
from datetime import date

# Resolucion de rutas (local / Colab). Los mapas HTML viven en mapa_html/.
PROC = None
for _base in [os.path.join("..", "mapa_html"), "mapa_html", "/content/mapa_html"]:
    if os.path.isdir(_base):
        PROC = os.path.abspath(_base)
        break
if PROC is None:
    raise FileNotFoundError("No se encontro la carpeta mapa_html/.")

RAIZ = os.path.dirname(PROC)
OUT = os.path.join(RAIZ, "output")
os.makedirs(OUT, exist_ok=True)

# Archivos a incluir en el paquete (solo los del ITT; se omiten los de avance).
INCLUIR = [
    "index.html",
    "mapa_geoanalitica_itt.html",
    "mapa_seguridad_calor.html",
    "mapa_movilidad.html",
    "mapa_desarrollo_social.html",
    "mapa_entorno_urbano.html",
    "mapa_desarrollo_economico.html",
    "mapa_vivienda.html",
]

# README que viaja dentro del ZIP.
LEEME = """MAPAS INTERACTIVOS - ITT CIUDAD PARAISO
=======================================

Como abrir los mapas
--------------------
1. Descomprime este archivo ZIP en una carpeta (clic derecho > Extraer todo).
   IMPORTANTE: manten todos los archivos .html juntos en la misma carpeta.
2. Haz doble clic en  index.html  (la portada). Desde ahi puedes abrir cada mapa.
   Tambien puedes abrir cualquier mapa_*.html directamente.

Requisitos
----------
- Conexion a internet (los mapas cargan el fondo satelital/callejero y las
  graficas desde internet; sin conexion el mapa sale sin fondo).
- Navegador recomendado: Google Chrome o Microsoft Edge.
  (El boton "Exportar lamina (deck)" para generar un PDF funciona mejor en
   Chrome/Edge; en Firefox/Safari descarga el PDF directamente.)

Que contiene
------------
- index.html .......................... Portada con enlaces a todos los mapas.
- mapa_geoanalitica_itt.html .......... ITT - vista general.
- mapa_seguridad_calor.html ........... Seguridad (hurto, rinas, SPA, homicidio).
- mapa_movilidad.html ................. Movilidad (siniestros y red peatonal).
- mapa_desarrollo_social.html ......... Desarrollo social (VIF, rinas, SPA).
- mapa_entorno_urbano.html ............ Entorno urbano (NDVI, arbolado, deficit).
- mapa_desarrollo_economico.html ...... Desarrollo economico (negocios, educacion).
- mapa_vivienda.html .................. Vivienda (deficit habitacional por barrio).

Como usar cada mapa
-------------------
- Esquina superior derecha: control de capas (prende/apaga capas).
- Esquina superior izquierda: panel con resumen y serie de tiempo (se colapsa).
- Esquina inferior derecha: control de intensidad del calor (en los que aplica).
- Clic en un punto o poligono: muestra su informacion.

Nota de privacidad
------------------
Estos mapas contienen informacion territorial agregada. No los publiques en
sitios de acceso abierto; compartelos solo por canales internos autorizados.

Fuente: ITT Ciudad Paraiso - CDO Alcaldia de Santiago de Cali.
Generado: __FECHA__
"""

falta = [f for f in INCLUIR if not os.path.isfile(os.path.join(PROC, f))]
if falta:
    print("Aviso: no se encontraron estos HTML (se omiten):")
    for f in falta:
        print("  -", f)

presentes = [f for f in INCLUIR if os.path.isfile(os.path.join(PROC, f))]

fecha = date.today().isoformat()
zip_nombre = "Mapas_ITT_Ciudad_Paraiso_" + fecha + ".zip"
zip_path = os.path.join(OUT, zip_nombre)

# Nombre de carpeta raiz dentro del ZIP (para que al extraer quede ordenado).
carpeta_zip = "Mapas_ITT_Ciudad_Paraiso"

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    # README
    z.writestr(carpeta_zip + "/LEEME.txt", LEEME.replace("__FECHA__", fecha))
    # HTML
    for f in presentes:
        z.write(os.path.join(PROC, f), carpeta_zip + "/" + f)

tam_mb = os.path.getsize(zip_path) / (1024 * 1024)
print("ZIP creado:", zip_path)
print("Archivos incluidos:", len(presentes), "HTML + LEEME.txt")
print("Tamano del ZIP: %.1f MB" % tam_mb)
if tam_mb > 23:
    print("ADVERTENCIA: supera ~23 MB; algunos correos (25 MB) podrian rechazarlo.")
    print("Opcion: comparte por enlace (OneDrive/Drive/Teams) en vez de adjunto.")
else:
    print("Cabe en un correo estandar (limite ~25 MB en Gmail/Outlook).")
