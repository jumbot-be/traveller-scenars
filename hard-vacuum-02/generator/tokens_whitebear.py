from hv import *
from maps_lib import *
import math

def base(cv,ringcol,cx=128,cy=118,r=106):
    cv.fill_circle(cx,cy,r,(16,20,26,255))
    cv.ring(cx,cy,r,ringcol,9)
    cv.ring(cx,cy,r-9,(36,42,52,255),2)

def person(cv,cx,cy,suit,skin,weapon=None,glasses=False,trim=None):
    sh=[(cx-60,cy+80),(cx-38,cy-6),(cx+38,cy-6),(cx+60,cy+80)]
    cv.fill_polygon(sh,suit); cv.poly_outline(sh,(26,30,36),3)
    if trim: cv.fill_rect(cx-38,cy-2,76,8,trim)
    cv.fill_circle(cx,cy-44,28,skin); cv.ring(cx,cy-44,28,(26,30,36),3)
    if glasses:
        cv.ring(cx-10,cy-48,7,(230,232,236),2); cv.ring(cx+10,cy-48,7,(230,232,236),2)
        cv.line(cx-3,cy-48,cx+3,cy-48,(230,232,236),2)
    if weapon=='rifle':
        cv.line(cx-74,cy+30,cx+66,cy+46,(58,56,52),9)
        cv.fill_rect(cx-76,cy+24,16,26,(46,44,40))
        cv.fill_rect(cx-8,cy+42,14,22,(46,44,40))
    elif weapon=='laser':
        cv.line(cx-74,cy+30,cx+62,cy+44,(70,68,64),8)
        cv.ring(cx+66,cy+45,7,(230,120,90),3)
        cv.fill_circle(cx+66,cy+45,4,(255,120,80,230))
    elif weapon=='pistol':
        cv.line(cx-30,cy+44,cx+18,cy+50,(70,68,64),7)
        cv.fill_rect(cx-32,cy+40,12,16,(46,44,40))
    elif weapon=='cutlass':
        cv.line(cx-60,cy+72,cx+58,cy+32,(200,205,215),7)
        cv.line(cx-60,cy+72,cx-48,cy+52,(150,110,70),6)

def token(path,label,ringcol,drawfn):
    cv=Canvas(256,256,ss=2,bg=None)
    base(cv,ringcol)
    drawfn(cv,128,118)
    cv.text(128-textw(label,2)/2,238,label,C_TEXT,2)
    save_png(path,cv)
    print('ok',path)

def servitor(cv,cx,cy):
    cv.line(cx,cy-96,cx,cy-118,(190,196,206),3)
    cv.fill_circle(cx,cy-120,5,(80,200,255,255))
    cv.fill_rect(cx-30,cy-82,60,46,(206,212,220)); cv.rect(cx-30,cy-82,60,46,(70,76,86),3)
    cv.fill_rect(cx-20,cy-72,40,10,(80,200,235,255))
    cv.line(cx-42,cy-10,cx-70,cy+30,(190,196,206),8)
    cv.line(cx+42,cy-10,cx+70,cy+30,(190,196,206),8)
    cv.fill_rect(cx+52,cy+30,40,6,(150,158,168))
    cv.fill_rect(cx+66,cy+14,10,16,(150,120,80))
    cv.fill_rect(cx-42,cy-28,84,70,(226,230,236)); cv.rect(cx-42,cy-28,84,70,(70,76,86),3)
    cv.fill_rect(cx-12,cy-16,24,46,(206,212,220))
    cv.fill_circle(cx,cy+2,8,(230,150,80,255))
    cv.fill_rect(cx-42,cy+54,84,18,(206,212,220)); cv.rect(cx-42,cy+54,84,18,(70,76,86),2)

def corpsfn(cv,cx,cy):
    cv.fill_circle(cx,cy+10,34,(70,28,26,120))
    cv.fill_rect(cx-40,cy-8,52,22,(138,136,130))
    cv.fill_circle(cx+28,cy+4,13,(158,150,138))
    cv.fill_circle(cx-44,cy-8,10,(158,150,138))
    cv.line(cx-30,cy+14,cx+10,cy+22,(120,118,112),5)

def yacht_topdown(cv,cx,top,L,Wd):
    hull=(168,174,186); dark=(40,46,54); glass=(150,205,240)
    pts=[(cx,top),(cx+Wd*0.16,top+L*0.14),(cx+Wd*0.16,top+L*0.78),(cx+Wd*0.34,top+L),(cx-Wd*0.34,top+L),(cx-Wd*0.16,top+L*0.78),(cx-Wd*0.16,top+L*0.14)]
    cv.fill_polygon(pts,hull); cv.poly_outline(pts,dark,3)
    for s in (1,-1):
        P=[(cx+s*Wd*0.16,top+L*0.6),(cx+s*Wd*0.5,top+L*0.9),(cx+s*Wd*0.16,top+L*0.82)]
        cv.fill_polygon(P,(120,128,140)); cv.poly_outline(P,dark,2)
    cv.fill_rect(cx-Wd*0.07,top+L*0.07,Wd*0.14,L*0.1,glass)
    cv.fill_rect(cx-Wd*0.1,top+L*0.92,Wd*0.2,L*0.05,(70,76,86))

def ship_token(path,label,kind):
    cv=Canvas(256,256,ss=2,bg=None)
    cv.glow(128,120,80,(120,160,230),55)
    if kind=='yacht': yacht_topdown(cv,128,60,140,110)
    else: ship_topdown(cv,128,50,150,120,kind)
    cv.text(128-textw(label,2)/2,240,label,C_TEXT,2)
    save_png(path,cv)
    print('ok',path)

G=(224,176,88); SIL=(150,158,170); M=(96,120,168)

for i in range(1,7):
    token('token_serviteur_%d.png'%i,'SERVITEUR %d'%i,SIL,servitor)

token('token_tsygankov.png','TSYGANKOV',G,lambda cv,cx,cy: person(cv,cx,cy,(94,70,112),(212,178,148),weapon='cutlass',trim=G))
token('token_mukhtar.png','MUKHTAR',M,lambda cv,cx,cy: person(cv,cx,cy,(58,62,72),(192,158,126),weapon='rifle'))
token('token_rolfo.png','ROLFO',(96,160,140),lambda cv,cx,cy: person(cv,cx,cy,(126,128,134),(206,180,158),weapon='pistol',glasses=True))
token('token_jairzinho.png','JAIRZINHO',(108,178,120),lambda cv,cx,cy: person(cv,cx,cy,(120,100,84),(180,142,108),weapon=None))
token('token_rio.png','RIO ZHALEO',(110,190,200),lambda cv,cx,cy: person(cv,cx,cy,(74,82,96),(198,166,136),weapon='laser'))
token('token_corps.png','CORPS',(110,110,118),corpsfn)

ship_token('token_ship_yacht.png','YACHT 100 T','yacht')
ship_token('token_ship_hotcomet.png','HOT COMET','courier')
print('tokens whitebear ok')
