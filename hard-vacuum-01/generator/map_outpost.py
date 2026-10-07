from hv import *
from maps_lib import *
from ship_common import build, finish, nozzles
from wb_common import *

# RODOLPHE 189 - AVANT-POSTE MINIER - NIVEAU UNIQUE
# Toutes les pieces en cases de 44 px, murs sur les lignes de grille
cv=Canvas(1320,528,ss=2,bg=(20,24,32,255))
build(cv,20,40,1280,448,bow='flat')

# --- rangee haut (3 cases de haut, y 88..220) ---
groom(cv,2,2,5,3,'STOCKAGE',doors=[('S',88,44)])
for i in range(3):
    crate(cv,110+i*66,100,40); crate(cv,110+i*66,176,40)
groom(cv,7,2,5,3,'ATELIER',doors=[('S',88,44)])
table(cv,330,96,88,44); table(cv,330,168,88,44)
crate(cv,470,96,40); crate(cv,470,168,40)
groom(cv,12,2,5,3,'REFECTOIRE',doors=[('S',88,44)])
for i in range(2):
    table(cv,550+i*88,96,70,44); table(cv,550+i*88,168,70,44)
groom(cv,17,2,5,3,'QRTS OFFICIERS',doors=[('S',88,44)],maxsc=1)
cv.fill_rect(856,90,4,130,(216,220,228))
bunk(cv,766,120,60,34); bunk(cv,896,120,60,34)
groom(cv,22,2,6,3,'GENERATRICES',doors=[('S',110,44)],maxsc=1)
for i in range(3): generator(cv,988+i*80,120,66,54)
cv.text(1000,190,'ALIM',C_DIM,1)

# --- couloir (1 case de haut, y 220..264) ---
gcor(cv,2,5,26,1,'COULOIR')

# --- rangee bas (2 cases de haut, y 264..352) ---
groom(cv,2,6,7,2,'QUAI',doors=[('N',132,44)])
crate(cv,110,300,40); crate(cv,180,280,40); crate(cv,260,300,40); crate(cv,330,280,40)
for i in range(4):
    x0=(9+3*i)*CELL
    groom(cv,9+3*i,6,3,2,'CAB %d'%(i+1),doors=[('N',44,44)],maxsc=1)
    bunk(cv,x0+22,272,66,30)
groom(cv,21,6,2,2,'F',doors=[('N',22,44)],maxsc=1)
groom(cv,23,6,2,2,'SAS',doors=[('N',22,44)],maxsc=1)
irisv(cv,1056,308)
groom(cv,25,6,3,2,'CONTROLE',doors=[('N',44,44)],maxsc=1)
console(cv,1120,280,88,22); console(cv,1120,312,88,22)
airlock_ext(cv,1056,374,17)

grid_overlay(cv,88,88,1144,264)
finish(cv,'RODOLPHE 189 - AVANT-POSTE MINIER','NIVEAU UNIQUE - CABINES INDIVIDUELLES SUR COULOIR - 1 CASE = 1,5 M')
save_png('outpost_map.png',cv)
print('outpost ok')
