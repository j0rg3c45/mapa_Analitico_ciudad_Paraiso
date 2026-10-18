# Contexto: Formato de lamina del deck ITT y export a output/deck_output

Analisis de la estructura del deck del PMU (`contexto/contexto_deck/Reporte diario PMU -
Ciudad Paraiso.pdf`) y como traducirlo a un formato de lamina coherente con los mapas HTML
del proyecto, exportable por print screen / captura a `output/deck_output/`.

---

## 1. Layout del deck (plantilla que se repite en cada lamina)

Cada lamina tematica (Seguridad/Homicidios, Dominio/Salud, etc.) usa el MISMO patron:

```
+-----------------------------------------------------------+
| Territorio - Seguridad            (seccion, arriba izq)   |
| Homicidios                        (titulo de la lamina)   |
+---------------------------+-------------------------------+
|  CIFRA GRANDE (4)         |                               |
|  "en 2026, ene-sep"       |        MAPA por manzana       |
|  delta: -56% vs 2025      |        (coropleta             |
|                           |         escala Menos -> Mas)  |
|  mini-serie 2023-2026     |                               |
+---------------------------+-------------------------------+
| Corte: [dia,hora] - Fuente: ... - Mapa ilustrativo (pie)  |
+-----------------------------------------------------------+
```

Posiciones constantes en todo el deck:
- **Encabezado (arriba izquierda):** seccion ("Territorio - Seguridad" / "Resultados por
  dominio") + titulo (Homicidios, Salud, ...).
- **Columna izquierda:** CIFRA GRANDE (ultimo dato), periodo ("en 2026, ene-sep"),
  DELTA porcentual vs mismo periodo del ano anterior, y una MINI-SERIE (trimestral o anual
  2023-2026).
- **Centro/derecha:** el MAPA por manzana (coropleta con leyenda "Menos -> Mas").
- **Pie:** "Corte: [dia, hora]", fuente institucional y "Mapa ilustrativo".

## 2. Datos/cifras que el deck pide, por lamina

Lectura del dia (3 mensajes). Avance de la operacion: % caracterizado (56,6% - 469/828),
manzanas (27), con padrino (23), cierre estimado, estado vs meta.

Resultados por dominio (cifra grande + indicador % + delta + mapa por manzana):
- Salud (base 257 personas), Vivienda (210 hogares), Bienestar (n personas),
  Menores (n menores), Negocios (238 caracterizados, 113 afectados por terremoto).

Territorio (cifra 2026 ene-sep + delta vs 2025 + serie trimestral 2023-2026 + mapa):
- Seguridad: Homicidios (4, -56%), Hurtos (89, -28%).
- Convivencia: Rinas (547, +78%), SPA (135, +96%).
- Movilidad: Siniestros viales (5, -69%; ene-jun).
- Desarrollo economico: Establecimientos activos (311; -4% vs 2025, +32% vs 2023; serie
  anual).

Territorio - Resumen (ITT): cifra 66,4, "Fase de transformacion", serie 2023-2026
(45,1 / 53,9 / 57,6 / 66,4), y las 6 dimensiones: Seguridad, Movilidad, Desarrollo social,
Entorno urbano, Vivienda, Desarrollo economico.

Caracterizacion x territorio ("Donde priorizar"): dispersion por manzana (x=delitos,
y=necesidad de hogares); cuadrante prioridad.

Anexo - otras variables (cifra grande = ultimo dato; series 2023-2026):
- Lesionados siniestros (4; 24/30/23/4), Muertes siniestros (1; 4/3/0/1),
  VIF (17; 11/17/15/17), Matricula (3.276; 3891/3529/3310/3276),
  Desercion (5,1%), Repitencia (9,7%), NDVI (0,099; 0.095/0.110/0.110/0.099),
  Deficit habitacional (46,1%), Empleo (885 de 1.158; 834/881/898/885).

## 3. Correspondencia con los mapas HTML del proyecto

Nuestros mapas ya replican el layout del deck:
- Panel flotante arriba-izquierda = la columna izquierda del deck (cifras + series).
- Mapa por manzana al centro/derecha = el mapa de la lamina.
- Encabezado de export (titulo + corte + fuente) = encabezado/pie del deck.
Por tanto, una captura/print screen de nuestro mapa (con el panel y el encabezado de
export) produce una lamina con la MISMA estructura del deck.

## 4. Export a output/deck_output

- Carpeta de salida de laminas para presentacion: `output/deck_output/`.
- Nombre sugerido: `deck_<dimension>_<AAAA-MM-DD>.jpg|pdf` (ej. deck_seguridad_...).
- El export JPG/PDF ya existe en los mapas (seccion 13.1): captura la vista actual con
  panel + encabezado + leyenda, sobre fondo claro (sin mapa base por CORS).
- Pendiente a definir con el usuario (ver seccion 5).

## 5. Pendiente de confirmar / proponer

Para que la lamina salga "tal como el deck" conviene estandarizar el panel izquierdo de
cada mapa en modo lamina: cifra grande + periodo + delta + mini-serie, y el mapa a la
derecha. Decidir:
1. Si el export debe guardar directamente en `output/deck_output/` (hoy el navegador
   descarga a la carpeta de descargas; para forzar `output/deck_output/` habria que generar
   las laminas desde Python/headless, no solo con el boton del navegador).
2. Si se quiere una lamina por dimension (varias) o solo las que el usuario capture.
3. Si el ITT por manzana (hoy uniforme 58.5 / scores vacios) debe calcularse para que la
   coropleta por manzana del deck tenga color real.
