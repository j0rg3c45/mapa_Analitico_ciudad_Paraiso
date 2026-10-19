# -*- coding: utf-8 -*-
"""Genera una version PUBLICA (sin PII) de las capas de data/1_data_itt/ y la
empaqueta en UN unico ZIP versionable en el repo:  data_publico/data_itt_publico.zip

Enfoque de seguridad: WHITELIST por capa (solo se conservan las columnas
explicitamente listadas, que son las que usan los mapas). Cualquier columna no
listada (direccion, sexo, edad, identificacion, placas, razon social, etc.) se
ELIMINA. Para homicidios (02 y 12) se deja practicamente solo geometria + fecha.

Este ZIP es seguro para GitHub. El notebook en Colab lo descomprime a
data/1_data_itt/ y reproduce los mapas sin exponer datos personales.

Ejecutar en el entorno uv unico del proyecto:
  & "C:\\Users\\Jorge\\.venv\\Scripts\\python.exe" notebooks/97_publicar_datos_sin_pii.py
"""
import os
import zipfile
import geopandas as gpd

# Resolucion de rutas (local / Colab).
def _dir_itt():
    for b in [os.path.join("..", "data", "1_data_itt"), os.path.join("data", "1_data_itt"),
              "/content/data/1_data_itt"]:
        if os.path.isdir(b):
            return os.path.abspath(b)
    raise FileNotFoundError("No se encontro data/1_data_itt/.")

DIR_ITT = _dir_itt()
RAIZ = os.path.dirname(os.path.dirname(DIR_ITT))        # .../mapa_Analitico_ciudad_Paraiso
OUT_DIR = os.path.join(RAIZ, "data_publico")
os.makedirs(OUT_DIR, exist_ok=True)
TMP = os.path.join(OUT_DIR, "_tmp_itt")
os.makedirs(TMP, exist_ok=True)

# WHITELIST de columnas por capa (solo campos SIN PII que usan los mapas).
# El resto se descarta. La geometria SIEMPRE se conserva.
WHITELIST = {
    "00_limite_ciudad_paraiso.geojson": ["id", "area"],
    "01_manzanas_itt_consolidado.geojson": [
        "idmanzana", "comuna", "barrio", "manzana", "itt", "nivel",
        "score_seguridad", "score_movilidad", "score_des_social",
        "score_entorno_u", "score_des_eco", "shape_area"],
    # Homicidios: SOLO fecha + categoria. Nada de persona/lugar.
    "02_seguridad_homicidios.geojson": ["fecha_evento", "anio", "trimestre"],
    "03_seguridad_hurtos.geojson": ["fecha_evento", "anio", "trimestre", "sitio"],
    "04_convivencia_rinas.geojson": ["fecha_evento", "anio", "trimestre", "sitio_hech", "agrupado"],
    "05_convivencia_spa.geojson": ["fecha_evento", "anio", "trimestre", "sitio_hech", "agrupado"],
    # Siniestros: fecha, clase y severidad (sin direccion/placas/sexo/edad/nombre).
    "06_movilidad_siniestros.geojson": ["fecha_evento", "anio", "trimestre",
                                        "clase_acci", "clasificacion_severidad"],
    "07_movilidad_red_peatonal_osm.geojson": ["name", "highway", "length"],
    "08_entorno_censo_arboreo.geojson": ["estado_arb", "comuna"],
    "09_seguridad_vif_calor_poligonal.geojson": [
        "idmanzana", "barrio", "vif_casos", "area_ha", "vif_densidad_ha", "nota_privacidad"],
    "10_demoliciones_cristo_rey_predios.geojson": [
        "idmanzana_catastral", "barrio", "area_terreno_m2", "fecha_demolicion",
        "estado", "demolicion", "anio", "entidad_responsable", "notas"],
    # Estacion: "nombre" es el nombre del CAI (equipamiento), no de persona.
    "11_estacion_fray_damian_manzana.geojson": [
        "nombre", "barrio", "comuna", "ubicacion", "criterio", "area_m2"],
    # Homicidios <=300m: SOLO fecha + distancia. Nada de persona/direccion.
    "12_estacion_fray_damian_homicidios_300m.geojson": ["fecha", "anio", "dist_a_estacion_m"],
    # Economico: se ELIMINA razonsocial y nombre_establecimiento (pueden identificar
    # a persona natural comerciante). Se deja estado, fechas, cifras agregadas y CIIU.
    "13_desarrollo_economico_negocios.geojson": [
        "estado", "fecharenovacion", "fechamatricula", "fechacancelacion",
        "ingresosordinarios", "activototal", "utilidadoperacional", "codigo_ciiu",
        # Atributos ampliados (sin PII): empleo, actividad y clasificacion.
        "empleo_personal_ocupado", "descripcion_ciiu", "sector_economico",
        "categoria", "tamano_empresa"],
    # Educacion: nombres de sedes (equipamiento publico), sin PII personal.
    "14_educacion_sedes.geojson": ["eenomsede", "eenomcorto", "eeclasede",
                                   "eeestado", "eecomcor", "eebarver", "dist_poligono_m"],
}

CRS_WEB = 4326

# IPM: la fuente (data/geojson/Mzn_ipm_variables.geojson) son 15.658 manzanas de Cali
# (~31 MB), demasiado para el repo. Se RECORTA a la zona (unas 33 manzanas) y la version
# liviana se incluye en el ZIP publico, dentro de geojson/. No tiene PII (datos censales
# agregados por manzana).
def _recorte_ipm(tmp_dir):
    def _p(nombre, carpeta):
        for b in [os.path.join("..", "data", carpeta, nombre),
                  os.path.join("data", carpeta, nombre),
                  os.path.join("/content", "data", carpeta, nombre)]:
            if os.path.isfile(b):
                return os.path.abspath(b)
        return None
    rp_ipm = _p("Mzn_ipm_variables.geojson", "geojson")
    rp_pol = _p("poligono_ciudad_Paraiso.geojson", "geojson")
    if rp_ipm is None or rp_pol is None:
        print("Aviso: no se pudo recortar IPM (falta fuente o poligono); se omite.")
        return None
    g = gpd.read_file(rp_ipm)
    g = g.set_crs(epsg=CRS_WEB) if g.crs is None else g.to_crs(CRS_WEB)
    pol = gpd.read_file(rp_pol).to_crs(CRS_WEB)
    zona = pol.geometry.union_all()
    z = g[g.geometry.within(zona) | g.geometry.intersects(zona)].copy()
    sub = os.path.join(tmp_dir, "geojson")
    os.makedirs(sub, exist_ok=True)
    dest = os.path.join(sub, "Mzn_ipm_variables.geojson")
    z.to_file(dest, driver="GeoJSON")
    print("Recorte IPM: %d de %d manzanas (en zona) -> geojson/Mzn_ipm_variables.geojson" % (len(z), len(g)))
    return dest

resumen = []
for arch, cols_ok in WHITELIST.items():
    rp = os.path.join(DIR_ITT, arch)
    if not os.path.isfile(rp):
        print("Aviso: no existe", arch, "- se omite")
        continue
    g = gpd.read_file(rp)
    if g.crs is None:
        g = g.set_crs(epsg=CRS_WEB)
    else:
        g = g.to_crs(CRS_WEB)
    # Conservar solo columnas de la whitelist que existan + geometria.
    keep = [c for c in cols_ok if c in g.columns]
    out = g[keep + ["geometry"]].copy()
    # Guardar saneado.
    dest = os.path.join(TMP, arch)
    out.to_file(dest, driver="GeoJSON")
    descartadas = [c for c in g.columns if c not in keep and c != "geometry"]
    resumen.append((arch, len(out), len(keep), len(descartadas)))
    print("Saneada %-45s feats=%-5d conserva=%-2d descarta=%d" % (arch, len(out), len(keep), len(descartadas)))

# Recorte del IPM a la zona (version liviana para el repo/Colab).
ipm_recorte = _recorte_ipm(TMP)

# Empaquetar en un unico ZIP.
zip_path = os.path.join(OUT_DIR, "data_itt_publico.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for arch, _, _, _ in resumen:
        z.write(os.path.join(TMP, arch), "1_data_itt/" + arch)
    # IPM recortado dentro de geojson/.
    if ipm_recorte and os.path.isfile(ipm_recorte):
        z.write(ipm_recorte, "geojson/Mzn_ipm_variables.geojson")
    # README dentro del ZIP.
    z.writestr("1_data_itt/LEEME_DATOS.txt",
               "Datos PUBLICOS del ITT Ciudad Paraiso (version SIN datos personales).\n"
               "Columnas con PII (direccion, sexo, edad, identificacion, placas, razon\n"
               "social, nombres de comerciantes) fueron ELIMINADAS. Homicidios: solo\n"
               "fecha y geometria. Uso: descomprimir a data/1_data_itt/ y correr los\n"
               "notebooks. Fuente: CDO Alcaldia de Santiago de Cali.\n")

# Limpiar temporales saneados (ya estan en el ZIP).
for arch, _, _, _ in resumen:
    try:
        os.remove(os.path.join(TMP, arch))
    except OSError:
        pass
import shutil as _sh
_sh.rmtree(os.path.join(TMP, "geojson"), ignore_errors=True)
try:
    os.rmdir(TMP)
except OSError:
    pass

tam = os.path.getsize(zip_path) / (1024 * 1024)
print("\nZIP publico creado:", zip_path)
print("Capas incluidas:", len(resumen), "| tamano: %.1f MB" % tam)
print("Este ZIP es SEGURO para versionar en GitHub (sin PII).")
