from hv import *
from maps_lib import *
from ship_common import finish
from wb_common import *

cv=Canvas(1496,1320,ss=2,bg=(20,24,32,255))

# DOMES D'ATTERRISSAGE (r=2 cases, centres alignes)
for cy,l1,l2 in ((264,'DOME 1','YACHT 100 T'),(616,'DOME 2','PAD LIBRE')):
    cv.fill_circle(220,cy,88,(64,70,82))
    cv.ring(220,cy,88,(216,220,228),4)
    cv.ring(220,cy,72,(110,118,130),2)
    cv.text(220-textw(l1,2)/2,cy-26,l1,C_TEXT,2)
    cv.text(220-textw(l2,1)/2,cy+2,l2,C_DIM,1)
# TUBES (1 case de large)
for ty in (220,572):
    cv.fill_rect(308,ty,88,44,(70,76,88)); cv.rect(308,ty,88,44,(216,220,228),3)

# FOYER (cases 9,4 -> 12,15)
groom(cv,9,4,3,11,'FOYER',doors=[('W',44,44),('W',396,44),('E',176,44)],maxsc=2)

# COULOIR 1 (cases 12,7 -> 26,10)
gcor(cv,12,7,14,3,'COULOIR 1')
wall_h(cv,308,528,1144)          # mur nord couloir 1
wall_h(cv,440,528,1144)          # mur sud couloir 1
cv.text(540,452,'EXPOSITIONS ARMURES SUR LES MURS',C_DIM,1)

# COUDE / SALLE DE PLAISIR (cases 26,5 -> 30,12)
groom(cv,26,5,4,7,None,doors=[('W',132,44),('S',88,44)],maxsc=1)
station_label(cv,1232,378,162,'COUDE - SALLE DE PLAISIR',C_TEXT,1,1)
irisv(cv,1159,374); irisv(cv,1254,557)

# COULOIR 2 (cases 27,12 -> 30,24)
gcor(cv,27,12,3,12,'COULOIR 2')
wall_v(cv,1188,528,1056,[(748,44)])          # mur ouest couloir 2 (porte Tsygankov)
wall_v(cv,1320,528,1056,[(704,44),(880,44)]) # mur est couloir 2 (personnel, cuisine/salon)

# SALLE DE CONTROLE (cases 26,24 -> 30,28)
groom(cv,26,24,4,4,'CONTROLE',doors=[('N',88,44)],maxsc=2)

# CABINE TSYGANKOV (cases 25,16 -> 27,19)
groom(cv,25,16,2,3,'TSYGANKOV',doors=[('E',44,44)],maxsc=1)

# CABINES PERSONNEL (cases 30,15 -> 32,18)
groom(cv,30,15,2,3,'PERSONNEL',doors=[('W',44,44)],maxsc=1)

# CUISINE + SALON (cases 30,19 -> 32,22)
groom(cv,30,19,2,3,'CUISINE SALON',doors=[('W',44,44)],maxsc=1,minsc=1)

# notes
cv.text(88,1250,'SCHEMA D\'ENSEMBLE - CARTES DETAILLEES: COULOIR 1, COULOIR 2, PAD D\'ATTERRISSAGE',C_DIM,1)
cv.text(88,1274,'VANNES IRIS AUX DEUX EXTREMITES DU COUDE - SALLE DE PLAISIR SCELLABLE',C_DIM,1)

grid_overlay(cv,0,0,1496,1320)
finish(cv,'WHITE BEAR - DOMAINE TSYGANKOV','TG-14 "CHICHARITO" - VUE D\'ENSEMBLE EN L - 2 DOMES + COULOIRS - 1 CASE = 1,5 M')
save_png('whitebear_estate_map.png',cv)
print('estate ok')
