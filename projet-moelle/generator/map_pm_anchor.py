# PROJET MOELLE - 01 - Station orbitale ANCRE-HAUTE : vue d'ensemble schematique
from hv import *
from maps_lib import stars, station_label, title, ship_topdown, engine
import math

cv = Canvas(1600, 1040, ss=2, bg=(10,12,18,255))
stars(cv, 77, 300)

# --- Planete COLCHIDE (en bas a gauche) ---
PX, PY, PR = 330, 790, 300
cv.glow(PX, PY, PR+30, (150,180,215), 60)
cv.fill_circle(PX, PY, PR, (172,190,208))          # glace
cv.fill_circle(PX, PY-40, PR-16, (186,202,218))    # calotte polaire claire
cv.ring(PX, PY+70, PR*0.55, (148,168,188), 14)     # bande equatoriale
cv.ring(PX, PY+60, PR*0.72, (158,176,194), 8)
cv.ring(PX, PY+95, PR*0.34, (140,160,182), 10)
cv.ring(PX, PY, PR+6, (110,140,180,120), 3)        # atmosphere
station_label(cv, PX, PY+PR+42, 420, "COLCHIDE (OLF-13) - CALOTTE GLACIAIRE -80 C", C_CYAN, 2, 1)

# --- Station ANCRE-HAUTE (au centre-droite) ---
SX, SY = 1060, 420
# radiateurs
for rx, rw in ((SX-160, 150), (SX+40, 150)):
    cv.fill_rect(rx, SY-6, rw, 12, (120,86,60))
    cv.line(rx, SY, rx+rw, SY, (224,140,70), 2)
# rayons / spokes
for i in range(4):
    a = math.pi/4 + i*math.pi/2
    cv.line(SX, SY, SX+math.cos(a)*280, SY+math.sin(a)*280, (110,120,136), 6)
# anneaux
cv.ring(SX, SY, 130, (110,120,136), 8)   # anneau A
cv.ring(SX, SY, 210, (110,120,136), 8)   # anneau B
cv.ring(SX, SY, 280, (96,104,120), 10)   # anneau C - quai
# hub central
cv.glow(SX, SY, 66, (96,168,232), 70)
cv.fill_circle(SX, SY, 50, (96,104,120))
cv.fill_circle(SX, SY, 34, (74,80,94))
cv.ring(SX, SY, 14, C_GOLD, 6)
# pods d'amarrage sur l'anneau C
for a_deg in (20, 110, 200, 340):
    a = math.radians(a_deg)
    px, py = SX+math.cos(a)*280, SY+math.sin(a)*280
    cv.fill_circle(px, py, 16, (124,134,150))
    cv.ring(px, py, 16, (36,42,50), 3)
# navire fantome amare a l'anneau C (vers le bas-droite)
a = math.radians(20)
GX, GY = SX+math.cos(a)*280, SY+math.sin(a)*280
cv.line(GX, GY, GX+60, GY+40, (110,120,136), 5)
ship_topdown(cv, GX+120, GY+20, 150, 90, 'trader')
station_label(cv, GX+120, GY+190, 380, "NRC PALAMEDE - NAVIRE FANTOME (AMARE, AUCUN REPONSE)", C_RED, 2, 1)

# labels station
station_label(cv, SX, SY-74, 300, "HUB - OPS / CONTROLE", C_TEXT, 2, 1)
station_label(cv, SX-100, SY-190, 420, "ANNEAU A - MARCHE / QUARTIERS", C_TEXT, 2, 1)
station_label(cv, SX+140, SY-268, 420, "ANNEAU B - RAFFINERIE / STOCKAGE", C_DIM, 2, 1)
station_label(cv, SX-200, SY-368, 420, "ANNEAU C - QUAI D'AMARRAGE", C_TEXT, 2, 1)
station_label(cv, SX+420, SY-140, 320, "RADIATEURS", C_DIM, 2, 1)

# --- navette : trajectoire pointillee vers Colchide ---
def dashes(x0, y0, x1, y1, n=14, t=5):
    for i in range(n):
        f1 = i/n; f2 = f1 + 0.36/n
        cv.line(x0+(x1-x0)*f1, y0+(y1-y0)*f1, x0+(x1-x0)*f2, y0+(y1-y0)*f2, (96,168,232), t)

dashes(SX-80, SY+120, PX+230, PY-190)
# glyph navette
MX, MY = (SX-80+PX+230)/2, (SY+120+PY-190)/2
cv.fill_polygon([(MX, MY-26), (MX+34, MY+14), (MX-34, MY+14)], (150,170,190))
cv.fill_polygon([(MX-12, MY+14), (MX+12, MY+14), (MX+6, MY+30), (MX-6, MY+30)], (96,168,232))
station_label(cv, MX+10, MY+62, 360, "NAVETTE - DESCENTE VERS COLCHIDE (40 MIN)", C_CYAN, 2, 1)

title(cv, "PROJET MOELLE - ANCRE-HAUTE", "STATION ORBITALE AU-DESSUS DE COLCHIDE (OLF-13) - SCHEMA D'ENSEMBLE, CARTES DETAILLEES SEPAREES")
save_png("pm_anchor_overview.png", cv)
print("OK pm_anchor_overview.png")
