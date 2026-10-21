# -*- coding: utf-8 -*-
"""Empaqueta los mapas IPM de Barrio Obrero en un unico ZIP listo para compartir.

Copia los HTML de mapa_html/Barrio_obrero/ junto con un README (LEEME.txt) y
genera un ZIP con fecha en compartir_itt_mapas/.

Ejecutar en el entorno uv unico del proyecto:
  & "C:\\Users\\Jorge\\.venv\\Scripts\\python.exe" notebooks/98b_empaquetar_mapas_bo.py
"""
import os
import zipfile
from datetime import date

# Resolucion de rutas (local / Colab). Los mapas de BO viven en mapa_html/Barrio_obrero/.
PROC = None
for _base in [os.path.join("..", "mapa_html", "Barrio_obrero"),
              os.path.join("mapa_html", "Barrio_obrero"),
              "/content/mapa_html/Barrio_obrero"]:
    if os.path.isdir(_base):
        PROC = os.path.abspath(_base)
        break
if PROC is None:
    raise FileNotFoundError("No se encontro la carpeta mapa_html/Barrio_obrero/.")

RAIZ = os.path.dirname(os.path.dirname(PROC))  # .../mapa_Analitico_ciudad_Paraiso
OUT = os.path.join(RAIZ, "compartir_itt_mapas")
os.makedirs(OUT, exist_ok=True)

# Mapas IPM de Barrio Obrero a incluir.
INCLUIR = [
    "bo_mapa_ipm.html",
    "bo_mapa_ipm_original.html",
    "bo_mapa_ipm_dimensiones.html",
    "bo_mapa_ipm_dimensiones_v1.html",
    "mapa_comparacion_barrio_obrero.html",
]

LEEME = """MAPAS INTERACTIVOS - IPM BARRIO OBRERO (Cali)
=============================================

Que es esto
-----------
Mapas interactivos del Indice de Pobreza Multidimensional (IPM) a nivel de
manzana para la zona de estudio Barrio Obrero (Comuna 9), con dos limites:
el poligono V1 (16 manzanas) y el poligono oficial ampliado (45 manzanas).

Como abrir los mapas
--------------------
1. Descomprime este archivo ZIP en una carpeta (clic derecho > Extraer todo).
   IMPORTANTE: manten todos los archivos .html juntos en la misma carpeta.
2. Haz doble clic en cualquier  *.html  para abrirlo en el navegador.

Requisitos
----------
- Conexion a internet (los mapas cargan el fondo satelital/callejero y las
  graficas desde internet; sin conexion el mapa sale sin fondo).
- Navegador recomendado: Google Chrome o Microsoft Edge.

Que contiene
------------
- bo_mapa_ipm.html ...................... IPM por manzana - poligono V1 (16 mz).
- bo_mapa_ipm_original.html ............. IPM por manzana - poligono oficial (45 mz).
- bo_mapa_ipm_dimensiones.html .......... IPM por dimension DANE - poligono oficial;
                                          barras por manzana al dar clic.
- bo_mapa_ipm_dimensiones_v1.html ....... IPM por dimension DANE - poligono V1.
- mapa_comparacion_barrio_obrero.html ... Comparacion territorial: V1 vs oficial vs
                                          un 3er poligono que dibujas (circulo o
                                          poligono libre) para capturar manzanas
                                          aledanas y comparar su IPM en vivo.

Como usar cada mapa
-------------------
- Esquina superior derecha: control de capas (prende/apaga capas).
- Panel flotante: resumen, tabla comparativa y graficos (se puede colapsar).
- Clic en una manzana: muestra su IPM y nivel.
- En el mapa de comparacion: usa la herramienta de dibujo (arriba a la izquierda)
  para trazar un circulo o poligono sobre las manzanas aledanas; el panel calcula
  el IPM promedio y las dimensiones del area seleccionada al instante.

Notas tecnicas
--------------
- Unidad del IPM: % de personas. Vacios = 0. Escala de 4 niveles (cortes del
  proyecto 8 / 15 / 25). Paleta apta para daltonismo (azul -> naranja).
- Fuente del dato: Censo 2018 (DANE, CNPV).
- No se incluyen dimensiones del ITT (seguridad, movilidad): el dataset ITT real
  solo cubre Ciudad Paraiso (Comuna 3); Barrio Obrero (Comuna 9) aun no tiene esos
  datos cargados.

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
zip_nombre = "Mapas_IPM_Barrio_Obrero_" + fecha + ".zip"
zip_path = os.path.join(OUT, zip_nombre)
carpeta_zip = "Mapas_IPM_Barrio_Obrero"

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    z.writestr(carpeta_zip + "/LEEME.txt", LEEME.replace("__FECHA__", fecha))
    for f in presentes:
        z.write(os.path.join(PROC, f), carpeta_zip + "/" + f)

tam_mb = os.path.getsize(zip_path) / (1024 * 1024)
print("ZIP creado:", zip_path)
print("Archivos incluidos:", len(presentes), "HTML + LEEME.txt")
for f in presentes:
    print("  -", f)
print("Tamano del ZIP: %.1f MB" % tam_mb)
if tam_mb > 23:
    print("ADVERTENCIA: supera ~23 MB; algunos correos (25 MB) podrian rechazarlo.")
    print("Opcion: comparte por enlace (OneDrive/Drive/Teams) en vez de adjunto.")
else:
    print("Cabe en un correo estandar (limite ~25 MB en Gmail/Outlook).")
