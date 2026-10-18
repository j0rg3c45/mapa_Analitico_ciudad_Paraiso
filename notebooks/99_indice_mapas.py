# -*- coding: utf-8 -*-
"""Genera una portada HTML (indice) que enlaza todos los mapas por dimension del
ITT Ciudad Paraiso. Detecta que HTML existen en data_processed_geo/ y arma las
tarjetas con el estilo del proyecto (paleta Okabe-Ito). La portada se escribe en
data_processed_geo/index.html (misma carpeta que los mapas, para que los enlaces
relativos funcionen al abrir el archivo directamente).

Ejecutar en el entorno uv unico del proyecto:
  & "C:\\Users\\Jorge\\.venv\\Scripts\\python.exe" notebooks/99_indice_mapas.py
"""
import os
from datetime import date

# Carpeta de salida (donde viven los HTML). Resolucion local + Colab.
OUT_DIR = None
for _base in [os.path.join("..", "data_processed_geo"), "data_processed_geo",
              "/content/data_processed_geo"]:
    if os.path.isdir(_base):
        OUT_DIR = os.path.abspath(_base)
        break
if OUT_DIR is None:
    raise FileNotFoundError("No se encontro la carpeta data_processed_geo/.")

# Paleta Okabe-Ito.
OKI_AZUL, OKI_NARANJA, OKI_VERDE = "#0072B2", "#E69F00", "#009E73"
OKI_MORADO, OKI_BERMELL, OKI_GRIS = "#CC79A7", "#D55E00", "#333333"
DORADO, BG = "#8A6D1A", "#F4F6F9"

# Catalogo de mapas: (archivo, dimension, peso, descripcion, color).
CATALOGO = [
    ("mapa_geoanalitica_itt.html", "ITT - vista general", None,
     "Indice de Transformacion Territorial consolidado por manzana.", OKI_GRIS),
    ("mapa_seguridad_calor.html", "Seguridad", "27%",
     "Hurto, rinas, SPA y homicidio: puntos y mapas de calor por categoria.", OKI_AZUL),
    ("mapa_movilidad.html", "Movilidad", "22%",
     "Siniestros viales por severidad (calor) y red peatonal (OSM).", OKI_NARANJA),
    ("mapa_desarrollo_social.html", "Desarrollo social / convivencia", "19%",
     "VIF (densidad por manzana), rinas y SPA (puntos y calor).", OKI_MORADO),
    ("mapa_entorno_urbano.html", "Entorno urbano", "17%",
     "NDVI anual, censo arboreo y deficit habitacional.", OKI_VERDE),
    ("mapa_desarrollo_economico.html", "Desarrollo economico", "15%",
     "Negocios por estado (puntos y densidad) y sedes educativas.", OKI_AZUL),
    ("mapa_vivienda.html", "Vivienda", None,
     "Deficit habitacional por barrio (SISBEN), coropleta.", OKI_BERMELL),
]

# Dimensiones sin datos todavia (se muestran deshabilitadas).
PENDIENTES = []

def _tarjeta(archivo, titulo, peso, desc, color):
    disponible = os.path.isfile(os.path.join(OUT_DIR, archivo))
    peso_badge = ('<span class="peso">%s</span>' % peso) if peso else ""
    if disponible:
        return (
            '<a class="card" href="%s" style="border-left:6px solid %s">'
            '<div class="card-head"><span class="dot" style="background:%s"></span>'
            '<span class="titulo">%s</span>%s</div>'
            '<div class="desc">%s</div>'
            '<div class="abrir">Abrir mapa &rarr;</div></a>'
            % (archivo, color, color, titulo, peso_badge, desc)
        )
    return (
        '<div class="card card-off" style="border-left:6px solid #bbb">'
        '<div class="card-head"><span class="dot" style="background:#bbb"></span>'
        '<span class="titulo">%s</span>%s</div>'
        '<div class="desc">%s</div>'
        '<div class="abrir off">No disponible (regenerar notebook)</div></div>'
        % (titulo, peso_badge, desc)
    )

def _tarjeta_pendiente(titulo, peso, desc):
    peso_badge = ('<span class="peso">%s</span>' % peso) if peso else ""
    return (
        '<div class="card card-off" style="border-left:6px solid #ddd">'
        '<div class="card-head"><span class="dot" style="background:#ddd"></span>'
        '<span class="titulo">%s</span>%s</div>'
        '<div class="desc">%s</div>'
        '<div class="abrir off">Pendiente de datos</div></div>'
        % (titulo, peso_badge, desc)
    )

cards = "\n".join(_tarjeta(*c) for c in CATALOGO)
cards_pend = "\n".join(_tarjeta_pendiente(*c) for c in PENDIENTES)
n_disp = sum(1 for c in CATALOGO if os.path.isfile(os.path.join(OUT_DIR, c[0])))

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ITT Ciudad Paraiso - Mapas por dimension</title>
<style>
  *{box-sizing:border-box}
  body{margin:0;font-family:system-ui,Segoe UI,sans-serif;color:__GRIS__;background:__BG__}
  header{background:#fff;border-bottom:4px solid __DORADO__;padding:22px 28px}
  header h1{margin:0;font-size:22px;color:#222}
  header .sub{margin-top:4px;font-size:13px;color:#777}
  .wrap{max-width:1100px;margin:0 auto;padding:22px 28px 40px 28px}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px}
  .card{display:block;background:#fff;border-radius:10px;padding:16px 18px;text-decoration:none;
        color:inherit;box-shadow:0 2px 8px rgba(0,0,0,.08);transition:transform .12s,box-shadow .12s}
  .card:hover{transform:translateY(-2px);box-shadow:0 4px 14px rgba(0,0,0,.14)}
  .card-off{opacity:.6;cursor:default}
  .card-off:hover{transform:none;box-shadow:0 2px 8px rgba(0,0,0,.08)}
  .card-head{display:flex;align-items:center;gap:8px;margin-bottom:6px}
  .dot{width:12px;height:12px;border-radius:50%;display:inline-block;flex:0 0 auto}
  .titulo{font-weight:700;font-size:15px}
  .peso{margin-left:auto;background:#eef1f5;color:#555;font-size:11px;font-weight:700;
        padding:2px 8px;border-radius:20px}
  .desc{font-size:12.5px;color:#666;line-height:1.4;margin-bottom:10px}
  .abrir{font-size:12px;font-weight:700;color:__AZUL__}
  .abrir.off{color:#999;font-weight:600}
  h2.sec{font-size:14px;color:#555;margin:26px 0 10px 0;text-transform:uppercase;letter-spacing:.5px}
  footer{max-width:1100px;margin:0 auto;padding:0 28px 30px 28px;font-size:11px;color:#999}
</style>
</head>
<body>
<header>
  <h1>ITT Ciudad Paraiso - Mapas por dimension</h1>
  <div class="sub">Indice de Transformacion Territorial - CDO Alcaldia de Santiago de Cali
    &nbsp;|&nbsp; __N__ mapas disponibles &nbsp;|&nbsp; Actualizado: __FECHA__</div>
</header>
<div class="wrap">
  <div class="grid">
__CARDS__
  </div>
__PEND_SECTION__
</div>
<footer>
  Los mapas se abren en el navegador. Se regeneran ejecutando sus notebooks
  (notebooks/02-07) en el entorno uv del proyecto. Esta portada no se versiona
  (carpeta data_processed_geo/ ignorada por git).
</footer>
</body>
</html>
"""

# Seccion de pendientes solo si hay items.
if cards_pend.strip():
    pend_section = ('  <h2 class="sec">Dimensiones pendientes</h2>\n'
                    '  <div class="grid">\n' + cards_pend + '\n  </div>')
else:
    pend_section = ""

HTML = (HTML.replace("__GRIS__", OKI_GRIS).replace("__BG__", BG)
            .replace("__DORADO__", DORADO).replace("__AZUL__", OKI_AZUL)
            .replace("__N__", str(n_disp)).replace("__FECHA__", date.today().isoformat())
            .replace("__CARDS__", cards).replace("__PEND_SECTION__", pend_section))

out = os.path.join(OUT_DIR, "index.html")
with open(out, "w", encoding="utf-8") as fh:
    fh.write(HTML)
print("Portada escrita:", out)
print("Mapas disponibles:", n_disp, "de", len(CATALOGO))
