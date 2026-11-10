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

# WHITE BEAR - SURFACE - EMPREINTE EXACTE DU DOMAINE
cv=Canvas(1804,1760,ss=2,bg=(8,10,14,255))
stars(cv,7,160)

# ciel + sol lunaire
cv.fill_rect(0,88,1804,1672,(56,54,58))
cv.line(0,88,1804,88,(90,88,92),2)
for (cxx,cyy,r) in ((1450,120,36),(1720,150,28),(220,528,26),(200,1450,60),(600,1520,50),(1000,1440,44),(900,1560,40),(1200,1560,48),(250,1050,40),(150,1150,36)):
    cv.fill_circle(cxx,cyy,r,(48,46,50))
    cv.ring(cxx,cyy,r,(64,62,66),3)

# --- empreinte du domaine (toits, memes surfaces que l'interieur) ---
SLAB=(74,80,92); SLABD=(40,46,54)
def slab(gx,gy,gw,gh):
    x,y,w,h=gx*CELL,gy*CELL,gw*CELL,gh*CELL
    cv.fill_rect(x,y,w,h,SLAB); cv.rect(x,y,w,h,SLABD,3)
slab(10,6,3,12)      # foyer
slab(13,11,18,3)     # couloir 1
for i in range(6): slab(13+3*i,8,3,3)   # cabines
slab(13,14,18,3)     # expositions
slab(31,5,6,11)      # coude
slab(34,16,3,14)     # couloir 2
slab(30,25,4,5)      # Tsygankov
for j in range(3): slab(31,16+3*j,3,3) # personnel
slab(37,16,3,6)      # cuisine
slab(37,22,3,8)      # salon
slab(32,30,6,7)      # controle
for ty in (286,726):  # tubes
    cv.fill_rect(396,ty,44,44,(70,76,88)); cv.rect(396,ty,44,44,(216,220,228),3)

# --- domes (r = 4 cases) avec vaisseaux ---
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
irisv(cv,455,308); irisv(cv,455,748)

# --- etiquettes ---
def lab(cx_,cy_,s,col=C_TEXT):
    cv.text(cx_-textw(s,1)/2,cy_,s,col,1)
lab(220,106,'DOME 1 - YACHT 100 T')
lab(220,936,'DOME 2 - HOT COMET (PAD LIBRE)')
lab(506,522,'FOYER')
lab(968,534,'COULOIR 1')
lab(968,404,'6 CABINES')
lab(968,668,'EXPOSITIONS')
lab(1496,452,'COUDE')
lab(1562,990,'COULOIR 2')
lab(1416,1207,'TSYGANKOV')
lab(1430,747,'CAB P1'); lab(1430,879,'CAB P2'); lab(1430,1011,'CAB P3')
lab(1694,826,'CUISINE')
lab(1694,1134,'SALON')
lab(1540,1460,'CONTROLE')
cv.text(620,1620,'PORTE DU DOME 1 VERROUILLEE DEPUIS LA SALLE DE CONTROLE',C_DIM,1)

grid_overlay(cv,0,88,1804,1540)
title(cv,'WHITE BEAR - SURFACE - DOMES + DOMAINE','TG-14 - EMPREINTE EXACTE DU DOMAINE (MEMES SURFACES QUE LES CARTES INTERIEURES) - 1 CASE = 1,5 M')
save_png('whitebear_pad_map.png',cv)
print('pad ok')
