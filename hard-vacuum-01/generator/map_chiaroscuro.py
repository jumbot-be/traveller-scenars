from hv import *
from maps_lib import *
from ship_common import *

# ============ DECK 1 ============
cv=Canvas(1200,800,ss=2,bg=(20,24,32,255))
build(cv,24,90,1152,680,bow='right')

corridor(cv,140,378,900,44,'COULOIR')
iris_at(cv,156,400,14)

# 3 dorms, 4 bunks each, individual doors on corridor
for i in range(3):
    x0=180+i*244
    room(cv,x0,150,240,228,'DORTOIR %d'%(i+1),doors=[('S',104,32)],maxsc=2)
    bunk(cv,x0+16,162,84,38); bunk(cv,x0+140,162,84,38)
    bunk(cv,x0+16,300,84,38); bunk(cv,x0+140,300,84,38)

room(cv,908,422,246,318,'PONT',doors=[('N',60,34)],maxsc=2)
for i in range(3): console(cv,930+i*70,440,58,22)
console(cv,1010,600,110,26)
cv.text(930,560,'CAPITAINERIE',C_DIM,2)
iris_at(cv,1120,690,14)
airlock_ext(cv,1150,690,17)

room(cv,500,422,404,318,'MESS / CUISINE',doors=[('N',40,32)],maxsc=2)
for i in range(3):
    table(cv,530+i*110,480,80,44)
for i in range(2):
    table(cv,560+i*110,600,80,44)
crate(cv,840,660,40)

room(cv,180,422,316,318,'SALLE DES MACHINES',doors=[('N',40,32)],maxsc=1)
for i in range(2): generator(cv,210+i*100,520,70,54)
iris_at(cv,338,680,14)
cv.text(300,700,'VERS PONT 2',C_DIM,2)
fuel_tank(cv,230,600,26)

nozzles(cv,30,430,24); nozzles(cv,30,600,24)

finish(cv,'CHIAROSCURO - FRONTIER TRADER 300 T','PIRATES : HOUNDS OF THE CURSED MOON - PONT 1 - DORTOIRS A PORTE INDIVIDUELLE')
save_png('chiaroscuro_deck1.png',cv)
print('chiaroscuro d1 ok')

# ============ DECK 2 ============
cv=Canvas(1200,800,ss=2,bg=(20,24,32,255))
build(cv,24,90,1152,680,bow='right')

room(cv,180,150,860,600,'',maxsc=2)
station_label(cv,610,200,500,'CALE PRINCIPALE - PORTE CARGO OUVERTE',C_TEXT,2,1)
for i in range(6):
    for j in range(2):
        crate(cv,230+i*90,320+j*46,40)
for i in range(4):
    crate(cv,300+i*100,470,44)
airraft(cv,600,640)
station_label(cv,600,700,300,'AIR/RAFT',C_DIM,2,1)
iris_at(cv,560,240,14)
cv.text(500,260,'VERS PONT 1',C_DIM,2)
for i in range(2): generator(cv,210+i*90,560,60,48)
hatch_door(cv,420,748,170)
hatch_door(cv,800,748,170)
cv.text(350,766,'PORTE CARGO OUVERTE',C_DIM,2)

nozzles(cv,30,430,24); nozzles(cv,30,600,24)

finish(cv,'CHIAROSCURO - PONT 2','CALE - PORTE CARGO OUVERTE - AIR/RAFT')
save_png('chiaroscuro_deck2.png',cv)
print('chiaroscuro d2 ok')
