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

cv=Canvas(1760,1232,ss=2,bg=(8,10,14,255))
stars(cv,7,160)

# sol lunaire + horizon
cv.fill_rect(0,176,1760,1056,(56,54,58))
cv.line(0,176,1760,176,(90,88,92),2)
for (cxx,cyy,r) in ((170,980,64),(1420,320,50),(1560,760,76),(900,1090,42),(220,320,36),(1300,1060,48),(1620,980,40),(120,760,30)):
    cv.fill_circle(cxx,cyy,r,(48,46,50))
    cv.ring(cxx,cyy,r,(64,62,66),3)

# DOMES (r=4 cases)
for cyy,lbl in ((616,'DOME 1'),(924,'DOME 2')):
    cv.fill_circle(440,cyy,176,(64,70,82))
    cv.ring(440,cyy,176,(216,220,228),5)
    cv.ring(440,cyy,140,(110,118,130),2)

# TUBES VERS FOYER
for ty in (594,902):
    cv.fill_rect(616,ty,88,44,(70,76,88)); cv.rect(616,ty,88,44,(216,220,228),3)

# FOYER (cases 16,12 -> 19,24)
groom(cv,16,12,3,12,'FOYER',doors=[('W',66,44),('W',374,44),('E',110,44)],maxsc=2)
irisv(cv,720,616); irisv(cv,720,924)

# COULOIR 1 (esquisse, vers le domaine)
groom(cv,19,14,5,3,'COULOIR 1',doors=[('W',22,44)],col=(64,70,82),maxsc=1)
cv.text(1064,672,'VERS COUDE + DOMAINE',C_DIM,1)

# YACHT + RAMPE + PILOTE (dome 1)
yacht_topdown(cv,440,470,260,150)
cv.text(440-textw('YACHT 100 T',1)/2,452,'YACHT 100 T',C_TEXT,1)
cv.fill_rect(428,730,24,62,(90,96,108)); cv.rect(428,730,24,62,(50,56,64),2)
corpse(cv,440,812)
cv.text(456,806,'PILOTE',C_DIM,1)

# HOT COMET (dome 2)
ship_topdown(cv,440,824,200,170,'courier')
cv.text(440-textw('HOT COMET',1)/2,806,'HOT COMET',C_TEXT,1)

cv.text(700,1122,'PORTE DU DOME 1 VERROUILLEE DEPUIS LA SALLE DE CONTROLE',C_DIM,1)

grid_overlay(cv,0,176,1760,1056)
title(cv,'WHITE BEAR - PAD D\'ATTERRISSAGE','TG-14 - SURFACE - YACHT (DOME 1) - HOT COMET (DOME 2) - TUBES VERS FOYER - 1 CASE = 1,5 M')
save_png('whitebear_pad_map.png',cv)
print('pad ok')
