from hv import *
from maps_lib import *
from ship_common import *

cv=Canvas(1076,380,ss=2,bg=(20,24,32,255))
build(cv,24,64,1028,294,bow='flat')

# --- top row ---
room(cv,40,70,180,140,'STOCKAGE',doors=[('S',70,30)])
for i in range(3):
    crate(cv,58+i*54,76,42); crate(cv,58+i*54,164,42)
room(cv,224,70,200,140,'ATELIER',doors=[('S',85,30)])
table(cv,252,80,90,44); table(cv,252,150,90,44)
crate(cv,360,80,42); crate(cv,360,160,42)
room(cv,428,70,200,140,'REFECTOIRE',doors=[('S',85,30)])
for i in range(2):
    table(cv,450+i*90,80,70,44); table(cv,450+i*90,156,70,44)
room(cv,632,70,170,140,'QRTS OFFICIERS',doors=[('S',70,30)],maxsc=1)
cv.fill_rect(713,75,4,127,(216,220,228))
bunk(cv,644,100,58,34); bunk(cv,726,100,58,34)
room(cv,806,70,230,140,'GENERATRICES',doors=[('S',100,30)])
for i in range(3): generator(cv,836+i*66,96,54,44)
cv.text(870,166,'ALIM',C_DIM,1)

# --- corridor ---
corridor(cv,40,214,996,44,'COULOIR')

# --- bottom row ---
room(cv,40,262,280,94,'QUAI',doors=[('N',60,40)])
crate(cv,70,300,40); crate(cv,120,270,40); crate(cv,176,300,40); crate(cv,232,272,40)
for i in range(4):
    x0=324+i*100
    room(cv,x0,262,96,94,'CAB %d'%(i+1),doors=[('N',34,28)],maxsc=1)
    bunk(cv,x0+12,268,64,30)
room(cv,728,262,78,94,'F',doors=[('N',24,28)],maxsc=1)
room(cv,810,262,92,94,'SAS',doors=[('N',30,30)])
iris_at(cv,856,306,13)
room(cv,906,262,130,94,'CONTROLE',doors=[('N',46,30)],maxsc=1)
console(cv,922,284,98,22); console(cv,922,316,98,22)
airlock_ext(cv,856,366,17)

finish(cv,'RODOLPHE 189 - AVANT-POSTE MINIER','NIVEAU UNIQUE - CABINES INDIVIDUELLES SUR COULOIR')
save_png('outpost_map.png',cv)
print('outpost ok')
