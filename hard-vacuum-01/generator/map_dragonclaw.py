from hv import *
from maps_lib import *
from ship_common import build, finish, nozzles
from wb_common import *

# ============ MERC DRAGON CLAW - RAIDER - PONT 1 ============
cv=Canvas(1188,792,ss=2,bg=(20,24,32,255))
build(cv,20,88,1148,680,bow='flat')

gcor(cv,4,8,20,1,'COULOIR')
wall_h(cv,352,792,836)               # bout de couloir
wall_v(cv,176,352,396); irisv(cv,191,374)

# 3 cabines officiers, portes individuelles (y 176..352)
for i in range(3):
    gx=4+5*i; x0=gx*CELL
    groom(cv,gx,4,4,4,'CAB OFF %d'%(i+1),doors=[('S',66,22)],maxsc=1)
    bunk(cv,x0+22,198,80,36)
    table(cv,x0+110,200,60,40)

# armurerie (x 836..1056, y 176..352)
groom(cv,19,4,5,4,'ARMURERIE',doors=[('S',726,44)],maxsc=2)
for i in range(5):
    cv.fill_rect(860+i*36,210,4,60,(140,120,70))
    cv.fill_rect(852+i*36,202,20,6,(216,220,228))

# quartiers troupes (x 176..484, y 396..616)
groom(cv,4,9,7,5,'QUARTIERS TROUPES',doors=[('N',88,44)],maxsc=1)
for i in range(3):
    bunk(cv,196+i*88,410,84,36)
    bunk(cv,196+i*88,460,84,36)
bunk(cv,250,540,84,36); bunk(cv,390,540,84,36)

# brig : acces couloir uniquement (x 484..660)
groom(cv,11,9,4,5,'BRIG',doors=[('N',352,44)],maxsc=2)
cv.fill_rect(510,440,70,36,(52,58,70)); cv.rect(510,440,70,36,(30,34,42),2)
station_label(cv,572,560,170,'ACCES COULOIR UNIQUEMENT',C_DIM,1,1)

# medbay (x 660..792)
groom(cv,15,9,3,5,'MEDBAY',doors=[('N',506,44)],maxsc=2)
bunk(cv,680,410,50,30); bunk(cv,740,410,50,30)
bunk(cv,700,480,70,34)

# pont (x 792..1056, y 396..616)
groom(cv,18,9,6,5,'PONT',doors=[('N',726,44)],maxsc=2)
for i in range(3): console(cv,812+i*66,410,58,22)
console(cv,900,540,120,26)
irisv(cv,1041,500); airlock_ext(cv,1056,500,17)

nozzles(cv,30,430,24); nozzles(cv,30,600,24)

grid_overlay(cv,176,132,880,484)
finish(cv,'MERC DRAGON CLAW - RAIDER','PONT 1 - BRIG : ACCES COULOIR UNIQUEMENT - 1 CASE = 1,5 M')
save_png('dragonclaw_deck1.png',cv)
print('dragonclaw d1 ok')

# ============ MERC DRAGON CLAW - PONT 2 ============
cv=Canvas(1188,792,ss=2,bg=(20,24,32,255))
build(cv,20,88,1148,680,bow='flat')

groom(cv,4,4,4,10,'MACHINES',doors=[('E',176,44)],maxsc=2)
for i in range(3): generator(cv,200,200+i*130,88,60)
fuel_tank(cv,240,560,26)

groom(cv,8,4,15,10,None,doors=[('W',176,44)])
station_label(cv,660,220,600,'HANGAR - 3 CHASSEURS',C_TEXT,2,1)
for i in range(3):
    ship_topdown(cv,440+i*220,250,190,150,'fighter')
irisv(cv,528,191)
cv.text(552,210,'VERS PONT 1',C_DIM,2)
for i in range(4): crate(cv,400+i*88,528,42)
hatch_door(cv,1012,420,200,horizontal=False)
station_label(cv,1000,640,150,'PORTE DE LANCEMENT',C_DIM,1,1)

nozzles(cv,30,430,24); nozzles(cv,30,600,24)

grid_overlay(cv,176,132,880,484)
finish(cv,'MERC DRAGON CLAW - PONT 2','HANGAR - 3 CHASSEURS - PORTE DE LANCEMENT - 1 CASE = 1,5 M')
save_png('dragonclaw_deck2.png',cv)
print('dragonclaw d2 ok')
