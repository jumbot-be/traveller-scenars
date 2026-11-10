from hv import *
from maps_lib import *
from ship_common import finish
from wb_common import *

cv=Canvas(1144,616,ss=2,bg=(20,24,32,255))

# COULOIR 2 (cases 4,6 -> 18,9 : x176..792, y264..396)
gcor(cv,4,6,14,3,'COULOIR 2')
wall_v(cv,176,264,396,[(308,44)])   # mur ouest + sortie vers coude
irisv(cv,191,330)

# CABINE TSYGANKOV (cases 13,3 -> 18,7 : x572..792, y132..264)
# a droite, collee a la salle de controle ; passage secret dans le dressing
groom(cv,13,3,5,4,None,doors=[('S',88,44),('E',66,22)])
bar(cv,592,150,88,22)
fresher(cv,720,146,44,44)
luxbed(cv,592,186,88,44)
closet(cv,696,196,88,44)
cv.fill_rect(784,198,6,22,C_GOLD)
cv.text(578,244,'TSYGANKOV',C_TEXT,1)

# 3 CABINES DOUBLES PERSONNEL (3x3 cases, porte 22px) - deplacees a gauche
for i in range(3):
    x0=(4+3*i)*CELL
    groom(cv,4+3*i,3,3,3,None,doors=[('S',66,22)])
    bunk(cv,x0+22,150,66,36)
    bunk(cv,x0+22,196,66,36)
    cv.text(x0+90,186,'CAB P%d'%(i+1),C_DIM,1)

# CUISINE (cases 4,9 -> 10,12 : x176..440, y396..528)
groom(cv,4,9,6,3,None,doors=[('N',110,44)])
cv.fill_rect(188,404,80,22,(70,76,84)); cv.fill_rect(352,404,76,22,(70,76,84))
for sx in (200,224,248): cv.fill_circle(sx,415,5,(230,120,70,220))
cv.text(308-textw('CUISINE',2)/2,442,'CUISINE',C_TEXT,2)
corpse(cv,250,486); corpse(cv,320,478); corpse(cv,390,490)

# SALON (cases 10,9 -> 18,12 : x440..792, y396..528)
groom(cv,10,9,8,3,None,doors=[('N',154,44)])
sofa(cv,460,420,120,36); sofa(cv,700,420,120,36)
table(cv,576,470,80,36)
cv.text(616-textw('SALON',2)/2,428,'SALON',C_TEXT,2)

# SALLE DE CONTROLE (cases 18,4 -> 24,11 : x792..1056, y176..484)
# passage secret depuis la cabine Tsygankov (mur ouest, gap 22px)
groom(cv,18,4,6,7,None,doors=[('W',132,44),('W',22,22),('E',308,44)])
cv.fill_rect(789,198,7,22,C_GOLD)
console(cv,806,188,100,26); console(cv,930,188,100,26)
console(cv,1010,250,26,90); console(cv,1010,360,26,90)
cv.fill_circle(924,300,40,(50,56,66)); cv.ring(924,300,40,C_CYAN,3); cv.ring(924,300,24,C_CYAN,2)
cv.glow(924,300,50,(110,190,200),50)
locker(cv,804,410,110,44)
cv.text(924-textw('SALLE DE CONTROLE',2)/2,466,'SALLE DE CONTROLE',C_TEXT,2)
irisv(cv,777,330)
airlock_ext(cv,1076,506,17)
cv.text(1000,534,'SAS VERS SURFACE',C_DIM,1)

# ingenieur mort dans le couloir (hors salle de controle verrouillee)
corpse(cv,740,330)

# notes
cv.text(176,556,'OUEST: VERS COUDE + SALLE DE PLAISIR (VANNE IRIS)',C_DIM,1)
cv.text(176,576,'PASSAGE SECRET DANS LE DRESSING DE TSYGANKOV VERS LA SALLE DE CONTROLE - PORTE BLINDEE, VERROU ELECTRONIQUE',C_DIM,1)

# grille + habillage
grid_overlay(cv,176,88,880,440)
finish(cv,'WHITE BEAR - COULOIR 2','DOMAINE TSYGANKOV - PERSONNEL A GAUCHE - CABINE TSYGANKOV COLLEE AU CONTROLE (PASSAGE SECRET) - 1 CASE = 1,5 M')
save_png('whitebear_deck2_map.png',cv)
print('deck2 ok')
