from hv import *
from maps_lib import *
import random, math

W,H=1960,1272
cv=Canvas(W,H,ss=2,bg=(8,10,20,255))

# stars in space corners
stars(cv,99,340)

# asteroid surface
rnd=random.Random(189)
pts=[]
for i in range(48):
    a=2*math.pi*i/48
    rr=1.0+rnd.uniform(-0.09,0.09)
    pts.append((W/2+math.cos(a)*W*0.47*rr, H/2+math.sin(a)*H*0.46*rr))
cv.fill_polygon(pts,(86,78,66))
cv.poly_outline(pts,(50,44,36),5)

# craters
for _ in range(90):
    cxr=rnd.uniform(150,W-150); cyr=rnd.uniform(160,H-160)
    r=rnd.uniform(20,110)
    cv.fill_circle(cxr,cyr,r,(70,62,52))
    cv.ring(cxr,cyr,r,(104,94,78),3)
    cv.ring(cxr,cyr,r*0.7,(78,70,58),2)
# rocks
for _ in range(140):
    rx=rnd.uniform(60,W-60); ry=rnd.uniform(80,H-80)
    s_=rnd.uniform(6,18)
    cv.fill_polygon([(rx,ry-s_),(rx+s_,ry),(rx,ry+s_),(rx-s_,ry)],(112,102,84))
    cv.poly_outline([(rx,ry-s_),(rx+s_,ry),(rx,ry+s_),(rx-s_,ry)],(60,54,44),2)

# --- outpost (right side) ---
cv.fill_rect(1230,560,300,190,(96,104,120)); cv.rect(1230,560,300,190,(50,56,66),5)
cv.fill_rect(1250,600,120,120,(64,70,82)); cv.rect(1250,600,120,120,(40,46,54),3)
cv.fill_rect(1390,600,120,120,(64,70,82)); cv.rect(1390,600,120,120,(40,46,54),3)
for i in range(4): crate(cv,1400+i*26,740-40,22)
station_label(cv,1380,530,320,'RODOLPHE 189 - AVANT-POSTE',C_TEXT,3,2)
iris_at(cv,1226,655,16)

# --- tube 25 m ---
cv.fill_rect(760,632,470,46,(70,76,88)); cv.rect(760,632,470,46,(40,46,54),4)
for xx in range(790,1210,60): cv.line(xx,632,xx,678,(40,46,54),3)
station_label(cv,995,590,300,'TUBE - 25 M',C_DIM,2,1)

# --- player ship (courier) ---
cv.glow(560,600,150,(120,160,230),40)
ship_topdown(cv,560,430,340,210,'courier')
station_label(cv,560,810,300,'HOT COMET',C_TEXT,3,2)
airlock_ext(cv,660,650,15)

# --- pirates + robot ---
def marker(x,y,label,col):
    cv.fill_circle(x,y,40,(24,20,18,235))
    cv.ring(x,y,40,col,6)
    cv.text(x-textw(label,1)/2,y-6,label,(240,236,228),1)
    station_label(cv,x,y+58,160,label,(240,236,228),2,1)

marker(760,470,'P1',C_RED)
marker(880,530,'P2',C_RED)
marker(830,760,'P3',C_RED)
marker(980,780,'P4',C_RED)
marker(1120,900,'P5',C_RED)
marker(1200,960,'R',(150,158,170))

# scale + note
scale_bar(cv,60,H-60,4)
cv.text(60,H-80,'1 CASE = 1,5 M - GRILLE 44 PX',C_DIM,2)

cv.fill_rect(0,0,W,58,(15,19,27))
cv.rect(0,0,W,58,(58,66,80),2)
cv.text(18,10,'RODOLPHE 189 - SURFACE',C_TEXT,4)
cv.text(18,40,'ABORDAGE DES PIRATES - 5 PIRATES + ROBOT',C_DIM,2)

save_png('asteroid_map.png',cv)
print('asteroid ok')
