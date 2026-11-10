from hv import *
from maps_lib import *
from ship_common import finish
from wb_common import *

# WHITE BEAR - PLAN D'ENSEMBLE AUX VRAIES DIMENSIONS
# Memes surfaces que les cartes detaillees (couloir 1, couloir 2, pad)
cv=Canvas(1804,1672,ss=2,bg=(20,24,32,255))

# --- domes d'atterrissage (r = 4 cases) ---
for cyy,l1,l2 in ((308,'DOME 1','YACHT 100 T'),(748,'DOME 2','PAD LIBRE')):
    cv.fill_circle(220,cyy,176,(64,70,82))
    cv.ring(220,cyy,176,(216,220,228),5)
    cv.ring(220,cyy,140,(110,118,130),2)
    cv.text(220-textw(l1,3)/2,cyy-40,l1,C_TEXT,3)
    cv.text(220-textw(l2,1)/2,cyy+20,l2,C_DIM,1)

# --- tubes vers le foyer (1 case de large) ---
for ty in (286,726):
    cv.fill_rect(396,ty,44,44,(70,76,88)); cv.rect(396,ty,44,44,(216,220,228),3)

# --- foyer / sas cargo (3 x 12 cases) ---
groom(cv,10,6,3,12,'FOYER',doors=[('W',22,44),('W',462,44),('E',264,44)],maxsc=2)
irisv(cv,455,308); irisv(cv,455,748); irisv(cv,557,550)

# --- couloir 1 (18 x 3 cases) ---
gcor(cv,13,11,18,3,'COULOIR 1')

# --- 6 cabines individuelles de luxe (3x3 cases) ---
for i in range(6):
    groom(cv,13+3*i,8,3,3,'CAB %d'%(i+1),doors=[('S',66,22)],maxsc=1)

# --- expositions armures (18 x 3 cases) ---
groom(cv,13,14,18,3,'EXPOSITIONS',doors=[('N',374,44)],maxsc=1)

# --- coude / salle de plaisir (6 x 11 cases) ---
groom(cv,31,5,6,11,'COUDE - SALLE DE PLAISIR',doors=[('W',308,44),('S',176,44)],maxsc=1)
irisv(cv,1379,550); irisv(cv,1562,689)

# --- couloir 2 (3 x 14 cases) ---
gcor(cv,34,16,3,14,'COULOIR 2')

# --- cabine Tsygankov (4 x 5 cases) ---
groom(cv,30,16,4,5,'TSYGANKOV',doors=[('E',88,44)],maxsc=1)

# --- 3 cabines du personnel (3x3 cases empilees) ---
for j in range(3):
    groom(cv,31,21+3*j,3,3,'CAB P%d'%(j+1),doors=[('E',66,22)],maxsc=1)

# --- cuisine (3 x 6 cases) ---
groom(cv,37,16,3,6,'CUISINE',doors=[('W',110,44)],maxsc=1)

# --- salon (3 x 8 cases) ---
groom(cv,37,22,3,8,'SALON',doors=[('W',154,44)],maxsc=1)

# --- salle de controle (6 x 7 cases) ---
groom(cv,32,30,6,7,'CONTROLE',doors=[('N',132,44)],maxsc=2)
irisv(cv,1562,1335)

# notes
cv.text(88,1644,'MEMES SURFACES QUE LES CARTES DETAILLEES (COULOIR 1, COULOIR 2) ET LA VUE DE SURFACE - 1 CASE = 1,5 M',C_DIM,1)

grid_overlay(cv,44,132,1716,1496)
finish(cv,'WHITE BEAR - DOMAINE TSYGANKOV - PLAN D\'ENSEMBLE','TG-14 "CHICHARITO" - ANCIEN AVANT-POSTE TL11 EN L - 2 DOMES + TUBES + COULOIRS')
save_png('whitebear_estate_map.png',cv)
print('estate ok')
