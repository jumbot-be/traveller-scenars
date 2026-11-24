from hv import *
from maps_lib import *
from ship_common import finish
from wb_common import *

# WHITE BEAR - COULOIR 1 - MEME GEOMETRIE QUE LE PLAN D'ENSEMBLE
cv=Canvas(1716,880,ss=2,bg=(20,24,32,255))

# tubes vers les domes (esquisses a l'ouest)
for ty in (286,726):
    cv.fill_rect(352,ty,88,44,(70,76,88)); cv.rect(352,ty,88,44,(216,220,228),3)
cv.text(286,272,'TUBE DOME 1',C_DIM,1)
cv.text(286,712,'TUBE DOME 2',C_DIM,1)

# FOYER / SAS CARGO (3 x 12 cases : x440..572, y264..792)
groom(cv,10,6,3,12,'FOYER',doors=[('W',22,44),('W',462,44),('E',264,44)],maxsc=2)
irisv(cv,455,308); irisv(cv,455,748); irisv(cv,557,550)
crate(cv,460,300,36); crate(cv,460,346,36); crate(cv,460,660,36)

# COULOIR 1 (18 x 3 cases : x572..1364, y484..616)
gcor(cv,13,11,18,3,'COULOIR 1')

# 6 CABINES INDIVIDUELLES DE LUXE (3x3 cases, porte 22px sur couloir)
for i in range(6):
    gx=13+3*i; x0=gx*CELL
    groom(cv,gx,8,3,3,None,doors=[('S',66,22)])
    cv.text(x0+22,358,'CAB %d'%(i+1),C_DIM,1)
    luxbed(cv,x0+22,370,88,44)
    desk(cv,x0+22,422)
    closet(cv,x0+22,458,44,22)
    fresher(cv,x0+88,428,44,44)

# EXPOSITION ARMURES (18 x 3 cases : x572..1364, y616..748)
groom(cv,13,14,18,3,None,doors=[('N',374,44)])
cv.text(968-textw('EXPOSITIONS ARMURES & ARMES ANTIQUES',1)/2,628,'EXPOSITIONS ARMURES & ARMES ANTIQUES',C_TEXT,1)
for i in range(8):
    display_ped(cv,638+i*88,682,'armor' if i%2==0 else 'sword')

# COUDE / SALLE DE PLAISER (6 x 11 cases : x1364..1628, y220..704)
ex,ey=31*CELL,5*CELL
groom(cv,31,5,6,11,None,doors=[('W',308,44),('S',176,44)])
bar(cv,ex+22,ey+38,220,44)
table(cv,ex+44,ey+180,132,66)
table(cv,ex+44,ey+300,132,66)
screen(cv,ex+12,ey+120); screen(cv,ex+12,ey+360)
rack(cv,ex+220,ey+120,44,200)
for cx_,cy_ in ((ex+70,ey+230),(ex+150,ey+250),(ex+80,ey+340),(ex+160,ey+350),(ex+110,ey+430),(ex+190,ey+440)):
    corpse(cv,cx_,cy_)
cv.text(ex+132-textw('SALLE DE PLAISIR',2)/2,ey+92,'SALLE DE PLAISIR',C_TEXT,2)
cv.text(ex+132-textw('10 INVITES MORTS',1)/2,ey+456,'10 INVITES MORTS',C_RED,1)
irisv(cv,1379,550); irisv(cv,1562,689)

# note sortie sud
cv.text(1500,716,'COULOIR 2 ->',C_DIM,1)

grid_overlay(cv,352,132,1276,660)
finish(cv,'WHITE BEAR - COULOIR 1','DOMAINE TSYGANKOV - FOYER + 6 CABINES LUXE + EXPOSITIONS + SALLE DE PLAISIR - 1 CASE = 1,5 M')
save_png('whitebear_deck1_map.png',cv)
print('deck1 ok')
