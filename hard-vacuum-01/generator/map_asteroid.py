from hv import *
from maps_lib import *
from wb_common import *
import random, math

W,H=1960,1272
cv=Canvas(W,H,ss=2,bg=(8,10,20,255))

stars(cv,99,340)

# asteroide
rnd=random.Random(189)
pts=[]
for i in range(48):
    a=2*math.pi*i/48
    rr=1.0+rnd.uniform(-0.09,0.09)
    pts.append((W/2+math.cos(a)*W*0.47*rr, H/2+math.sin(a)*H*0.46*rr))
cv.fill_polygon(pts,(86,78,66))
cv.poly_outline(pts,(50,44,36),5)

for _ in range(90):
    cxr=rnd.uniform(150,W-150); cyr=rnd.uniform(160,H-160)
    r=rnd.uniform(20,110)
    cv.fill_circle(cxr,cyr,r,(70,62,52))
    cv.ring(cxr,cyr,r,(104,94,78),3)
    cv.ring(cxr,cyr,r*0.7,(78,70,58),2)
for _ in range(140):
    rx=rnd.uniform(60,W-60); ry=rnd.uniform(80,H-80)
    s_=rnd.uniform(6,18)
    cv.fill_polygon([(rx,ry-s_),(rx+s_,ry),(rx,ry+s_),(rx-s_,ry)],(112,102,84))
    cv.poly_outline([(rx,ry-s_),(rx+s_,ry),(rx,ry+s_),(rx-s_,ry)],(60,54,44),2)

# grille de bataille sur la surface
grid_overlay(cv,176,132,1628,924,(255,255,255,16))

# avant-poste (structure alignee : 7x4 cases)
cv.fill_rect(1232,528,308,176,(96,104,120)); cv.rect(1232,528,308,176,(50,56,66),5)
cv.fill_rect(1276,572,88,88,(64,70,82)); cv.rect(1276,572,88,88,(40,46,54),3)
cv.fill_rect(1388,572,88,88,(64,70,82)); cv.rect(1388,572,88,88,(40,46,54),3)
for i in range(4): crate(cv,1254+i*30,664,22)
station_label(cv,1386,500,320,'RODOLPHE 189 - AVANT-POSTE',C_TEXT,3,2)
irisv(cv,1232,638,16)

# tube 25 m (1 case de haut, aligne)
cv.fill_rect(792,616,440,44,(70,76,88)); cv.rect(792,616,440,44,(40,46,54),4)
for xx in range(836,1232,44): cv.line(xx,616,xx,660,(40,46,54),3)
station_label(cv,1012,594,300,'TUBE - 25 M',C_DIM,2,1)

# connecteur vaisseau -> tube
cv.fill_rect(616,616,176,44,(70,76,88)); cv.rect(616,616,176,44,(40,46,54),4)

# vaisseau des PJ (centre du vaisseau sur 12x14 cases)
cv.glow(528,616,150,(120,160,230),40)
ship_topdown(cv,528,440,340,210,'courier')
station_label(cv,528,806,300,'HOT COMET',C_TEXT,3,2)
airlock_ext(cv,653,638,15)

# pirates + robot
def marker(x,y,label,col):
    cv.fill_circle(x,y,40,(24,20,18,235))
    cv.ring(x,y,40,col,6)
    cv.text(x-textw(label,1)/2,y-6,label,(240,236,228),1)
    station_label(cv,x,y+58,160,label,(240,236,228),2,1)

marker(726,484,'P1',C_RED)
marker(858,528,'P2',C_RED)
marker(814,792,'P3',C_RED)
marker(968,792,'P4',C_RED)
marker(1100,968,'P5',C_RED)
marker(1188,836,'R',(150,158,170))

scale_bar(cv,60,H-60,4)
cv.text(60,H-80,'1 CASE = 1,5 M - GRILLE 44 PX',C_DIM,2)

cv.fill_rect(0,0,W,58,(15,19,27))
cv.rect(0,0,W,58,(58,66,80),2)
cv.text(18,10,'RODOLPHE 189 - SURFACE',C_TEXT,4)
cv.text(18,40,'ABORDAGE DES PIRATES - 5 PIRATES + ROBOT',C_DIM,2)

save_png('asteroid_map.png',cv)
print('asteroid ok')
