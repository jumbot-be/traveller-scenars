from hv import *
from maps_lib import *
from wb_common import *
import math

def yacht_topdown(cv,cx,top,L,Wd):
    hull=(168,174,186); dark=(40,46,54); glass=(150,205,240)
    pts=[(cx,top),(cx+Wd*0.16,top+L*0.14),(cx+Wd*0.16,top+L*0.78),(cx+Wd*0.34,top+L),(cx-Wd*0.34,top+L),(cx-Wd*0.16,top+L*0.78),(cx-Wd*0.16,top+L*0.14)]
    cv.fill_polygon(pts,hull); cv.poly_outline(pts,dark,3)
    for s in (1,-1):
        P=[(cx+s*Wd*0.16,top+L*0.6),(cx+s*Wd*0.5,top+L*0.9),(cx+s*Wd*0.16,top+L*0.82)]
        cv.fill_polygon(P,(120,128,140)); cv.poly_outline(P,dark,2)
    cv.fill_rect(cx-Wd*0.07,top+L*0.07,Wd*0.14,L*0.1,glass)
    cv.fill_rect(cx-Wd*0.1,top+L*0.92,Wd*0.2,L*0.05,(70,76,86))

# WHITE BEAR - SURFACE - VUE EXTERIEURE
# Empreinte reelle du domaine (memes surfaces que les cartes interieures)
# mais aucun detail d'interieur : silhouette unie + panneaux exterieurs
cv=Canvas(1804,1760,ss=2,bg=(8,10,14,255))
stars(cv,7,160)

# ciel + sol lunaire
cv.fill_rect(0,88,1804,1672,(56,54,58))
cv.line(0,88,1804,88,(90,88,92),2)
for (cxx,cyy,r) in ((1450,120,36),(1720,150,28),(220,528,26),(200,1450,60),(600,1520,50),(1000,1440,44),(900,1560,40),(1200,1560,48),(250,1050,40),(150,1150,36)):
    cv.fill_circle(cxx,cyy,r,(48,46,50))
    cv.ring(cxx,cyy,r,(64,62,66),3)

# --- tubes vers les domes (exterieur, alignes) ---
for ty in (286,726):
    cv.fill_rect(396,ty,44,44,(70,76,88)); cv.rect(396,ty,44,44,(216,220,228),3)

# --- silhouette exterieure du domaine (empreinte reelle, aucun detail interieur) ---
BLDG=[(572,352),(1364,352),(1364,220),(1628,220),(1628,704),(1760,704),(1760,1320),
      (1672,1320),(1672,1628),(1408,1628),(1408,1320),(1320,1320),(1320,1100),
      (1364,1100),(1364,748),(572,748),(572,792),(440,792),(440,264),(572,264)]
cv.fill_polygon(BLDG,(74,80,92))
cv.poly_outline(BLDG,(40,46,54),4)
# panneaux de coque exterieurs (uniformes, ne revelent aucune piece)
greeble(cv,600,370,700,360,(86,92,104),(52,58,68),16,26)
greeble(cv,1380,240,230,440,(86,92,104),(52,58,68),9,26)
greeble(cv,1380,720,110,360,(86,92,104),(52,58,68),6,24)
greeble(cv,1510,720,110,580,(86,92,104),(52,58,68),8,24)
greeble(cv,1640,720,110,580,(86,92,104),(52,58,68),8,24)
greeble(cv,1420,1340,240,270,(86,92,104),(52,58,68),7,26)
# details exterieurs : sas surface + antenne
airlock_ext(cv,1688,1480,15)
cv.line(1700,1500,1700,1440,(150,158,168),4)
cv.fill_circle(1700,1434,6,(230,150,80,255))
# sas d'entree cote domes (face ouest du foyer)
airlock_ext(cv,426,308,13); airlock_ext(cv,426,748,13)

# --- domes (r = 4 cases) ---
for cyy in (308,748):
    cv.fill_circle(220,cyy,176,(64,70,82))
    cv.ring(220,cyy,176,(216,220,228),5)
    cv.ring(220,cyy,140,(110,118,130),2)
yacht_topdown(cv,220,178,260,150)
cv.text(220-textw('YACHT 100 T',1)/2,152,'YACHT 100 T',C_TEXT,1)
cv.fill_rect(208,438,24,46,(90,96,108)); cv.rect(208,438,24,46,(50,56,64),2)
corpse(cv,220,506)
cv.text(240,500,'PILOTE',C_DIM,1)
ship_topdown(cv,220,648,200,170,'courier')
cv.text(220-textw('HOT COMET',1)/2,588,'HOT COMET',C_TEXT,1)

# --- etiquettes ---
def lab(cx_,cy_,s,col=C_TEXT):
    cv.text(cx_-textw(s,1)/2,cy_,s,col,1)
lab(220,106,'DOME 1 - YACHT 100 T')
lab(220,936,'DOME 2 - HOT COMET (PAD LIBRE)')
station_label(cv,968,540,740,'DOMAINE TSYGANKOV',C_TEXT,3,2)
cv.text(620,1620,'PORTE DU DOME 1 VERROUILLEE DEPUIS LA SALLE DE CONTROLE',C_DIM,1)
cv.text(620,1640,'VUE EXTERIEURE - EMPREINTE REELLE (44 PX ALIGNEE), SANS DETAILS INTERIEURS',C_DIM,1)

grid_overlay(cv,0,88,1804,1540)
title(cv,'WHITE BEAR - PAD D\'ATTERRISSAGE - VUE EXTERIEURE','TG-14 - SURFACE - YACHT (DOME 1) - HOT COMET (DOME 2) - TUBES VERS DOMAINE - 1 CASE = 1,5 M')
save_png('whitebear_pad_map.png',cv)
print('pad ok')
