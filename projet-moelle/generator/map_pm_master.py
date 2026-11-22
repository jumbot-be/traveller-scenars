# PROJET MOELLE - 02 - COLCHIDE : reseau souterrain (carte maitresse)
from hv import *
from maps_lib import station_label, title
from wb_common import grid_overlay
import math, random

cv = Canvas(1700, 1300, ss=2, bg=(186,200,212,255))

# --- champ de glace ---
rnd = random.Random(55)
for _ in range(16):  # longues fissures
    x, y = rnd.uniform(0, 1700), rnd.uniform(0, 1300)
    pts = [(x, y)]
    for _s in range(5):
        x += rnd.uniform(-160, 160); y += rnd.uniform(-90, 90)
        pts.append((x, y))
    cv.poly_outline(pts, (150,164,178), 2)
for _ in range(9):  # crateres
    x, y = rnd.uniform(0, 1600), rnd.uniform(60, 1240)
    r = rnd.uniform(18, 46)
    cv.ring(x, y, r, (166,182,196), 3)
    cv.fill_circle(x, y, r, (196,208,218,120))

CX, CY = 850, 650   # centre de la boucle
R  = 452            # rayon des gares

# --- grille locale (pour l'echelle de combat, pas la geographie) ---
grid_overlay(cv, 0, 0, 1700, 1300, (60,84,116,26))

# --- tunnel en boucle, deux voies ---
cv.ring(CX, CY, R+34, (56,70,84), 8)   # voie externe
cv.ring(CX, CY, R-34, (56,70,84), 8)   # voie interne
cv.ring(CX, CY, R, (28,36,46,140), 22)  # gabarit central (roche profonde)

# fleches de sens
def arrow(ax, ay, ang, col):
    a = math.radians(ang)
    dx, dy = math.cos(a), math.sin(a)
    px, py = -dy, dx
    pts = [(ax+dx*20, ay+dy*20), (ax-dx*8+px*9, ay-dy*8+py*9), (ax-dx*8-px*9, ay-dy*8-py*9)]
    cv.fill_polygon(pts, col)

for i in range(12):  # voie externe : horaire
    a = 90 + i*30
    arrow(CX+math.cos(math.radians(a))*(R+34), CY-math.sin(math.radians(a))*(R+34), a-90, C_ACC)
for i in range(12):  # voie interne : anti-horaire
    a = 270 + i*30
    arrow(CX+math.cos(math.radians(a))*(R-34), CY+math.sin(math.radians(a))*(R-34), -a+90, C_GOLD)

# --- glyphes des deux trains ---
def train(cx, cy, col, lab):
    cv.fill_rect(cx-26, cy-13, 44, 26, (44,54,66))
    cv.fill_polygon([(cx+18, cy-13), (cx+38, cy), (cx+18, cy+13)], (44,54,66))
    cv.fill_rect(cx-18, cy-5, 12, 20, (200,215,228))
    cv.fill_circle(cx-20, cy-4, 4, col); cv.fill_circle(cx-20, cy+5, 4, col)
    cv.fill_circle(cx+8, cy-4, 4, col); cv.fill_circle(cx+8, cy+5, 4, col)
    station_label(cv, cx, cy+34, 240, lab, col, 2, 1)

train(CX, CY-(R+80), C_ACC, "BORÉAL (SENS HORAIRE)")
train(CX, CY+(R+80), C_GOLD, "AUSTRAL (SENS INVERSE)")

# --- les 6 gares ---
stations = [
    (90,  "PUITS D'ODESSA", "SEUL ACCÈS SURFACE - TRIAGE"),
    (30,  "MINE BORÉE", "MÉTAUX - PERCÉES VHURR"),
    (330, "USINE 12", "FONDERIE - RÉACTEUR PRINCIPAL"),
    (270, "CITÉ-BASSIN", "2000 HAB. (MOITIÉ VIDE)"),
    (210, "LABO CENTRAL", "CENTRE XÉNOARCHÉOLOGIQUE"),
    (150, "TERMIN PROFOND", "CHAMBRE - VANNE BLINDÉE -4 KM"),
]
for ang, name, sub in stations:
    a = math.radians(ang)
    sx, sy = CX+math.cos(a)*R, CY-math.sin(a)*R
    cv.fill_rect(sx-26, sy-26, 52, 52, (74,84,98))
    cv.rect(sx-26, sy-26, 52, 52, (28,36,46), 4)
    cv.fill_rect(sx-12, sy-12, 24, 24, (110,124,140))
    lx = CX+math.cos(a)*(R+120) + (130 if math.cos(a) > 0.4 else -130 if math.cos(a) < -0.4 else 0)
    ly = CY-math.sin(a)*(R+96) if abs(math.cos(a)) <= 0.4 else CY-math.sin(a)*(R+60)
    cv.line(sx + (26 if math.cos(a)>=0 else -26), sy, lx, ly, (60,72,88), 3)
    station_label(cv, lx, ly-26, 300, name, C_TEXT, 2, 2)
    station_label(cv, lx, ly+22, 300, sub, C_RED if "VHURR" in sub or "CHAMBRE" in sub else C_DIM, 1, 1)

# --- percées vhurr (galeries qui remontent vers la boucle) ---
for (vx, vy) in ((CX+math.cos(math.radians(30))*R-60, CY-math.sin(math.radians(30))*R+92),
                 (CX-math.cos(math.radians(30))*R+56, CY-math.sin(math.radians(30))*R+92)):
    cv.ring(vx, vy, 30, C_RED, 8)
    cv.line(vx-22, vy-22, vx+18, vy+18, C_RED, 5)
    cv.line(vx+18, vy-22, vx-22, vy+18, C_RED, 5)

# --- zone d'atterrissage au-dessus du Puits d'Odessa ---
cv.ring(CX, 150, 70, (60,72,88), 6)
cv.text(CX-96, 148, "GLACE PLATE - ATTERISSAGE", C_TEXT, 2)
d = 0
while d < 1:  # puits de descente (pointille)
    y0 = 180 + d*290
    cv.line(CX, y0, CX, min(y0+44, 180+290), (60,72,88), 5)
    d += 0.18
cv.text(CX-160, 320, "PUITS + ASCENSEUR", C_DIM, 2)

# --- legende (haut-gauche) ---
legend = [
    ("RÉSEAU SOUTERRAIN DE COLCHIDE", C_TEXT, 2),
    ("TUNNEL EN BOUCLE : 190 KM, 2 VOIES", C_TEXT, 1),
    ("TRAINS AUTOMATIQUES : BORÉAL / AUSTRAL", C_TEXT, 1),
    ("SURFACE : CALOTTE GLACIAIRE, -80 C, RIEN", C_DIM, 1),
    ("TOUT LE COMPLEXE EST SOUTERRAIN", C_DIM, 1),
    ("MARQUES ROUGES : PERCÉES VHURR", C_RED, 1),
    ("GRILLE : 1 CASE = 1,5 M (COMBAT LOCAL)", C_DIM, 1),
]
ly = 96
for txt, col, sc in legend:
    cv.text(44, ly, txt, col, sc); ly += 14*sc + 8

# --- cadre de carte ---
cv.rect(0, 0, 1700, 1300, (28,36,46), 8)
title(cv, "PROJET MOELLE - COLCHIDE", "RÉSEAU SOUTERRAIN - CARTE MAÎTRESSE - BOUCLE DE 190 KM, DEUX TRAINS, SIX GARES")
save_png("pm_colchide_master.png", cv)
print("OK pm_colchide_master.png")
