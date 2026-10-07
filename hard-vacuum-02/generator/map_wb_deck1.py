from hv import *
from maps_lib import *
from ship_common import finish
from wb_common import *

cv=Canvas(1364,660,ss=2,bg=(20,24,32,255))

# FOYER / SAS CARGO  (cases 2,5 -> 5,10 : x88..220, y220..440)
groom(cv,2,5,3,5,'FOYER',doors=[('E',88,44),('W',44,44),('W',176,44)],maxsc=2)
irisv(cv,103,286); irisv(cv,103,418)
crate(cv,96,228,36); crate(cv,96,274,36)

# COULOIR 1 (cases 5,6 -> 23,9 : x220..1012, y264..396)
gcor(cv,5,6,18,3,'COULOIR 1')

# 6 CABINES INDIVIDUELLES DE LUXE (3x3 cases, porte 22px sur couloir)
for i in range(6):
    gx=5+3*i; x0=gx*CELL
    groom(cv,gx,3,3,3,None,doors=[('S',66,22)])
    cv.text(x0+22,140,'CAB %d'%(i+1),C_DIM,1)
    luxbed(cv,x0+22,152,88,44)
    desk(cv,x0+22,204)
    closet(cv,x0+22,240,44,22)
    fresher(cv,x0+88,208,44,44)

# EXPOSITION ARMURES (cases 5,9 -> 23,12 : x220..1012, y396..528)
groom(cv,5,9,18,3,None,doors=[('N',374,44)])
cv.text(616-textw('EXPOSITIONS ARMURES & ARMES ANTIQUES',1)/2,412,'EXPOSITIONS ARMURES & ARMES ANTIQUES',C_TEXT,1)
for i in range(8):
    display_ped(cv,242+i*88,462,'armor' if i%2==0 else 'sword')

# COUDE / SALLE DE PLAISIR (cases 23,2 -> 29,13 : x1012..1276, y88..572)
ex,ey=23*CELL,2*CELL
groom(cv,23,2,6,11,None,doors=[('W',220,44),('S',110,44)])
bar(cv,ex+22,ey+38,220,44)
table(cv,ex+44,ey+180,132,66)
table(cv,ex+44,ey+300,132,66)
screen(cv,ex+12,ey+120); screen(cv,ex+12,ey+330); screen(cv,ex+12,ey+380)
rack(cv,ex+206,ey+120,44,240)
for cx_,cy_ in ((ex+70,ey+230),(ex+150,ey+250),(ex+80,ey+340),(ex+160,ey+350),(ex+110,ey+430),(ex+190,ey+440)):
    corpse(cv,cx_,cy_)
cv.text(ex+132-textw('SALLE DE PLAISIR',2)/2,ey+92,'SALLE DE PLAISIR',C_TEXT,2)
cv.text(ex+132-textw('10 INVITES MORTS',1)/2,ey+470,'10 INVITES MORTS',C_RED,1)
irisv(cv,1027,330); irisv(cv,1144,557)

# notes
cv.text(88,452,'TUBES VERS DOMES',C_DIM,1)
cv.text(1080,584,'COULOIR 2 ->',C_DIM,1)

# grille + habillage
grid_overlay(cv,88,88,1276-88,616-88)
finish(cv,'WHITE BEAR - COULOIR 1','DOMAINE TSYGANKOV - 6 CABINES LUXE + EXPOSITIONS + SALLE DE PLAISIR - 1 CASE = 1,5 M')
save_png('whitebear_deck1_map.png',cv)
print('deck1 ok')
