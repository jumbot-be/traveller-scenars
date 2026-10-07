from hv import *
from maps_lib import *
from ship_common import build, finish, nozzles
from wb_common import *

# ============ CHIAROSCURO - FRONTIER TRADER 300 T - PONT 1 ============
cv=Canvas(1188,792,ss=2,bg=(20,24,32,255))
build(cv,20,88,1148,680,bow='flat')

gcor(cv,4,8,15,1,'COULOIR')
wall_h(cv,352,792,836)               # bout de couloir
wall_h(cv,396,176,352)
wall_v(cv,176,352,396); irisv(cv,191,374)

# 3 dortoirs, 4 couchettes, portes individuelles (y 176..352)
for i in range(3):
    gx=4+5*i; x0=gx*CELL
    groom(cv,gx,4,4,4,'DORTOIR %d'%(i+1),doors=[('S',66,22)],maxsc=2)
    bunk(cv,x0+22,198,66,36); bunk(cv,x0+88,198,66,36)
    bunk(cv,x0+22,260,66,36); bunk(cv,x0+88,260,66,36)

# pont a la proue (x 836..1056, y 176..528)
groom(cv,19,4,5,8,'PONT',doors=[('W',176,44)],maxsc=2)
for i in range(3): console(cv,860+i*66,190,58,22)
console(cv,940,300,110,26)
cv.text(890,244,'CAPITAINERIE',C_DIM,2)
irisv(cv,1041,440); airlock_ext(cv,1056,440,17)

# mess / cuisine (x 572..836, y 396..572)
groom(cv,13,9,6,4,'MESS / CUISINE',doors=[('N',44,44)],maxsc=1)
table(cv,600,412,70,44); table(cv,700,412,70,44)
table(cv,600,490,70,44); table(cv,700,490,70,44)

# salle des machines (x 352..572, y 396..572)
groom(cv,8,9,5,4,'MACHINES',doors=[('N',44,44)],maxsc=1)
generator(cv,380,420,66,54); generator(cv,470,420,66,54)
fuel_tank(cv,420,500,26)
irisv(cv,440,557)
cv.text(396,584,'VERS PONT 2',C_DIM,2)

nozzles(cv,30,430,24); nozzles(cv,30,600,24)

grid_overlay(cv,176,132,880,484)
finish(cv,'CHIAROSCURO - FRONTIER TRADER 300 T','PIRATES : HOUNDS OF THE CURSED MOON - PONT 1 - 1 CASE = 1,5 M')
save_png('chiaroscuro_deck1.png',cv)
print('chiaroscuro d1 ok')

# ============ CHIAROSCURO - PONT 2 ============
cv=Canvas(1188,792,ss=2,bg=(20,24,32,255))
build(cv,20,88,1148,680,bow='flat')

groom(cv,4,4,4,10,'MACHINES',doors=[('E',176,44)],maxsc=2)
for i in range(3): generator(cv,200,200+i*130,88,60)
fuel_tank(cv,240,560,26)

groom(cv,8,4,15,10,None,doors=[('W',176,44)])
station_label(cv,684,220,600,'CALE PRINCIPALE',C_TEXT,2,1)
for i in range(6):
    for j in range(2):
        crate(cv,396+i*88,264+j*88,40)
for i in range(4): crate(cv,480+i*88,480,44)
airraft(cv,682,528)
station_label(cv,682,586,200,'AIR/RAFT',C_DIM,2,1)
irisv(cv,528,191)
cv.text(552,210,'VERS PONT 1',C_DIM,2)
hatch_door(cv,528,616,160)
hatch_door(cv,836,616,160)
cv.text(700,636,'PORTE CARGO OUVERTE',C_DIM,2)

nozzles(cv,30,430,24); nozzles(cv,30,600,24)

grid_overlay(cv,176,132,880,484)
finish(cv,'CHIAROSCURO - PONT 2','CALE - PORTE CARGO OUVERTE - AIR/RAFT - 1 CASE = 1,5 M')
save_png('chiaroscuro_deck2.png',cv)
print('chiaroscuro d2 ok')
