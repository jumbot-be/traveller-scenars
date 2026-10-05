from hv import *
from maps_lib import *
from ship_common import *

# ============ DECK 1 ============
cv=Canvas(1200,800,ss=2,bg=(20,24,32,255))
build(cv,24,90,1152,680,bow='right')

corridor(cv,140,378,910,44,'COULOIR')
iris_at(cv,156,400,14)

# 3 officer cabins, individual doors on corridor
for i in range(3):
    x0=180+i*244
    room(cv,x0,230,240,148,'CAB OFF %d'%(i+1),doors=[('S',104,30)],maxsc=2)
    bunk(cv,x0+14,240,80,36)
    table(cv,x0+150,244,70,40)

room(cv,912,230,240,148,'ARMURERIE',doors=[('S',100,30)],maxsc=2)
for i in range(5):
    cv.fill_rect(936+i*40,258,4,60,(140,120,70))
    cv.fill_rect(930,250,52,6,(216,220,228))

room(cv,180,422,320,318,'QUARTIERS TROUPES',doors=[('N',40,34)],maxsc=2)
for i in range(3):
    bunk(cv,200+i*100,440,84,36)
    bunk(cv,200+i*100,500,84,36)
bunk(cv,220,640,84,36); bunk(cv,360,640,84,36)

# brig: corridor access only
room(cv,506,422,184,198,'BRIG',doors=[('N',72,26)],maxsc=2)
cv.fill_rect(560,560,70,36,(52,58,70)); cv.rect(560,560,70,36,(30,34,42),2)
station_label(cv,598,620,170,'ACCES COULOIR UNIQUEMENT',C_DIM,1,1)

room(cv,698,422,152,318,'MEDBAY',doors=[('N',30,28)],maxsc=2)
for i in range(2): bunk(cv,716+i*60,450,50,30)
bunk(cv,740,600,70,34)

room(cv,858,422,296,318,'PONT',doors=[('N',60,34)],maxsc=2)
for i in range(3): console(cv,880+i*70,440,58,22)
console(cv,950,620,120,26)
iris_at(cv,1110,690,14)
airlock_ext(cv,1140,690,17)

nozzles(cv,30,430,24); nozzles(cv,30,600,24)

finish(cv,'MERC DRAGON CLAW - RAIDER','PONT 1 - CABINES OFFICIERS INDIVIDUELLES - BRIG : ACCES COULOIR UNIQUEMENT')
save_png('dragonclaw_deck1.png',cv)
print('dragonclaw d1 ok')

# ============ DECK 2 ============
cv=Canvas(1200,800,ss=2,bg=(20,24,32,255))
build(cv,24,90,1152,680,bow='right')

room(cv,180,150,146,600,'MACHINES',doors=[('E',100,30)],maxsc=2)
for i in range(3): generator(cv,205,200+i*120,96,64)
fuel_tank(cv,240,560,26)

room(cv,330,150,650,600,'',maxsc=2)
station_label(cv,655,180,400,'HANGAR - 3 CHASSEURS',C_TEXT,2,1)
for i in range(3):
    ship_topdown(cv,420+i*230,250,190,150,'fighter')
iris_at(cv,560,720,14)
cv.text(500,600,'VERS PONT 1',C_DIM,2)
for i in range(4): crate(cv,370+i*70,650,42)

# launch door on bow edge
hatch_door(cv,1020,450,200,horizontal=False)
station_label(cv,1040,600,150,'PORTE DE LANCEMENT',C_DIM,1,1)

nozzles(cv,30,430,24); nozzles(cv,30,600,24)

finish(cv,'MERC DRAGON CLAW - PONT 2','HANGAR - 3 CHASSEURS - PORTE DE LANCEMENT')
save_png('dragonclaw_deck2.png',cv)
print('dragonclaw d2 ok')
