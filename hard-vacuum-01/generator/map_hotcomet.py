from hv import *
from maps_lib import *
from ship_common import build, finish, nozzles
from wb_common import *

# HOT COMET - COURIER 100 T - VAISSEAU DES PERSONNAGES
cv=Canvas(1232,572,ss=2,bg=(20,24,32,255))
build(cv,20,88,1200,440,bow='flat')

# couloir (1 case de haut, y 308..352)
gcor(cv,6,7,16,1,'COULOIR')
wall_v(cv,264,308,352)      # mur arcade
irisv(cv,279,330)

# 4 cabines individuelles avec fresher (y 176..308)
for i in range(4):
    gx=6+4*i; x0=gx*CELL
    groom(cv,gx,4,4,3,'CAB %d'%(i+1),doors=[('S',66,22)],maxsc=1)
    bunk(cv,x0+22,190,66,36)
    desk(cv,x0+22,252)
    fresher(cv,x0+110,190,44,44)

# salon a la proue + sas (x 968..1188, y 176..484)
groom(cv,22,4,5,7,'SALON',doors=[('W',132,44)],maxsc=2)
table(cv,990,220,88,44); table(cv,1090,220,88,44)
table(cv,990,300,88,44); table(cv,1090,300,88,44)
irisv(cv,1173,440)
airlock_ext(cv,1188,440,17)
cv.text(1120,432,'SAS',C_DIM,1)

# rangee bas (y 352..528)
groom(cv,6,8,7,4,'MACHINES',doors=[('N',132,44)])
for i in range(3): generator(cv,300+i*88,380,66,54)
fuel_tank(cv,320,470,26); fuel_tank(cv,400,470,26); fuel_tank(cv,480,470,26)
groom(cv,13,8,7,4,'CALE 20 T',doors=[('N',44,44)],maxsc=1)
for i in range(3):
    for j in range(2):
        crate(cv,600+i*88,380+j*66,40)
hatch_door(cv,726,528,150)
cv.text(690,540,'PORTE CARGO',C_DIM,1)
groom(cv,20,8,2,4,'CARBURANT',doors=[('N',22,44)],maxsc=1,minsc=1)
fuel_tank(cv,912,390,24); fuel_tank(cv,912,468,24)

nozzles(cv,30,392,24); nozzles(cv,30,480,24)

grid_overlay(cv,264,132,924,352)
finish(cv,'HOT COMET - COURIER 100 T','VAISSEAU DES PERSONNAGES - CABINES INDIVIDUELLES - 1 CASE = 1,5 M')
save_png('hotcomet_map.png',cv)
print('hotcomet ok')
