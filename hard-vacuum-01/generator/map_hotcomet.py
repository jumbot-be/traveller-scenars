from hv import *
from maps_lib import *
from ship_common import *

cv=Canvas(1116,746,ss=2,bg=(20,24,32,255))
build(cv,24,90,1068,630,bow='right')

# corridor
corridor(cv,120,392,764,44,'COULOIR')
iris_at(cv,136,414,14)
iris_at(cv,868,414,14)

# cabins (individual doors on corridor)
for i in range(4):
    x0=170+i*144
    room(cv,x0,240,136,152,'CAB %d'%(i+1),doors=[('S',54,28)],maxsc=2)
    bunk(cv,x0+10,250,66,36)
    # private fresher
    cv.fill_rect(x0+80,246,48,64,C_FLOOR2); cv.rect(x0+80,246,48,64,(216,220,228),2)
    cv.fill_rect(x0+86,252,36,10,(96,168,232,200))
    cv.text(x0+84,284,'F',C_DIM,2)

# salon + sas at bow
room(cv,884,240,196,450,'SALON',doors=[('W',200,34)],maxsc=2)
table(cv,910,270,90,44); table(cv,1030,270,90,44)
table(cv,910,420,90,44); table(cv,1030,420,90,44)
room(cv,1002,560,72,120,'SAS',doors=[('W',20,28)],maxsc=1,t=4)
iris_at(cv,1038,620,12)
airlock_ext(cv,1088,620,17)

# machines / cargo / fuel
room(cv,120,436,300,264,'MACHINES',doors=[('N',120,34)])
for i in range(3): generator(cv,150+i*90,520,66,54)
fuel_tank(cv,180,640,26); fuel_tank(cv,240,640,26); fuel_tank(cv,300,640,26)
room(cv,424,436,376,264,'CALE 20 T',doors=[('N',170,40)],maxsc=2)
for i in range(4):
    for j in range(3):
        crate(cv,448+i*90,560+j*44,40)
hatch_door(cv,612,708,150)
cv.text(540,724,'PORTE CARGO',C_DIM,1)
room(cv,804,436,80,264,'CARBURANT',doors=[('N',24,26)],maxsc=1,minsc=1)
fuel_tank(cv,844,500,24); fuel_tank(cv,844,590,24)

# stern drives
nozzles(cv,30,470,24); nozzles(cv,30,640,24)
cv.text(28,724,'PROPULSEURS',C_DIM,2)

finish(cv,'HOT COMET - COURIER 100 T','VAISSEAU DES PERSONNAGES - CABINES INDIVIDUELLES - FRESHER PRIVE')
save_png('hotcomet_map.png',cv)
print('hotcomet ok')
