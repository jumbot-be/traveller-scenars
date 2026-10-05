from hv import *
from maps_lib import *
import math, random, sys

def lerp(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def backdrop(cv,seed,hue='blue'):
    W,H=cv.W,cv.H
    rnd=random.Random(seed)
    if hue=='blue':
        top,mid,bot=(8,10,26),(14,18,40),(6,14,24); neb1,neb2=(60,40,120),(20,70,110); pl=(70,110,160)
    elif hue=='orange':
        top,mid,bot=(22,12,20),(38,20,26),(10,10,18); neb1,neb2=(140,60,60),(170,110,50); pl=(190,120,70)
    else:
        top,mid,bot=(14,8,18),(30,14,30),(8,10,16); neb1,neb2=(120,30,90),(60,30,120); pl=(150,70,90)
    for y in range(H):
        f=y/H
        if f<0.6: c=lerp(top,mid,f/0.6)
        else: c=lerp(mid,bot,(f-0.6)/0.4)
        cv.span(y,0,W,c)
    for _ in range(5):
        bx,by=rnd.uniform(0,W),rnd.uniform(0,H*0.7); r=rnd.uniform(120,300)
        col=neb1 if rnd.random()<0.5 else neb2
        for i in range(6,0,-1):
            a=int(80*(7-i)/6)
            cv.fill_circle(bx,by,r*i/6,(col[0],col[1],col[2],a))
    for _ in range(240):
        x,y=rnd.uniform(0,W),rnd.uniform(0,H); b=int(rnd.uniform(90,255))
        cv.fill_rect(x,y,1.5,1.5,(b,b,min(255,b+30),255))
    px,py=W*0.84,H*0.86
    r=270
    cv.fill_circle(px,py,r,pl)
    cv.fill_circle(px+r*0.22,py,r,(0,0,0,120))
    cv.ring(px,py,r,(200,210,225,90),3)
    for i in range(3):
        yy=py-r+90+i*110+rnd.uniform(-20,20)
        cv.line(px-r*0.9,yy,px+r*0.9,yy,(0,0,0,50),6)

def hotcomet_exterior():
    W,H=1500,950
    cv=Canvas(W,H,ss=2,bg=None)
    backdrop(cv,42,'blue')
    cx,cy=W*0.47,H*0.5
    L,Hh=1150,150
    hull,dark=(138,146,158),(34,40,50)
    hot=(210,120,70)
    pts=[(cx-L/2,cy-Hh*0.5),(cx-L*0.25,cy-Hh*0.7),(cx+L*0.25,cy-Hh*0.9),(cx+L*0.9,cy-Hh*0.32),
         (cx+L/2,cy-Hh*0.28),(cx+L/2,cy+Hh*0.32),(cx+L*0.2,cy+Hh*0.9),(cx-L*0.3,cy+Hh*0.7),(cx-L/2,cy+Hh*0.5)]
    cv.fill_polygon(pts,hull); cv.poly_outline(pts,dark,4)
    fin=[(cx-L*0.05,cy-Hh*0.5),(cx+L*0.16,cy-Hh*0.88),(cx+L*0.30,cy-Hh*0.88),(cx+L*0.34,cy-Hh*0.5)]
    cv.fill_polygon(fin,(120,128,140)); cv.poly_outline(fin,dark,3)
    for i in range(1,10):
        xx=cx-L/2+i*L/10
        cv.line(xx,cy-Hh*0.55,xx,cy+Hh*0.55,dark,2)
    for yy in (cy-Hh*0.18,cy+Hh*0.22):
        cv.line(cx-L*0.46,yy,cx+L*0.38,yy,dark,2)
    cv.fill_polygon([(cx+L*0.52,cy-Hh*0.24),(cx+L*0.62,cy-Hh*0.14),(cx+L*0.62,cy+Hh*0.14),(cx+L*0.52,cy+Hh*0.24)],(150,205,240))
    cv.poly_outline([(cx+L*0.52,cy-Hh*0.24),(cx+L*0.62,cy-Hh*0.14),(cx+L*0.62,cy+Hh*0.14),(cx+L*0.52,cy+Hh*0.24)],dark,3)
    windows(cv,[(cx-L*0.30,cy-Hh*0.35),(cx-L*0.26,cy-Hh*0.35),(cx-L*0.22,cy-Hh*0.35),
                (cx-L*0.30,cy+Hh*0.3),(cx-L*0.26,cy+Hh*0.3)])
    cv.fill_rect(cx-L*0.05,cy-Hh*0.9,90,26,hot); cv.rect(cx-L*0.05,cy-Hh*0.9,90,26,dark,2)
    turret(cv,cx-L*0.05+45,cy-Hh*0.9-6,14,hot)
    engine(cv,cx+L/2-10,cy-40,58,(180,205,255),dark)
    engine(cv,cx+L/2-10,cy+46,44,(150,180,255),dark)
    for i in range(12,0,-1):
        cv.fill_polygon([(cx+L/2-6,cy-70),(cx+L/2+i*70,cy-40+(70*i/12)*0.9),
                         (cx+L/2+i*70,cy-40-(70*i/12)*0.9)],(170,200,255,int(24*i/12)))
    title(cv,"HOT COMET","COURIER 100 T - VAISSEAU DES PERSONNAGES - VUE EXTERIEURE")
    save_png('ext_hotcomet.png',cv)

def chiaroscuro_exterior():
    W,H=1500,950
    cv=Canvas(W,H,ss=2,bg=None)
    backdrop(cv,77,'orange')
    cx,cy=W*0.5,H*0.54
    L,Hh=1050,170
    hull,dark=(128,112,88),(58,50,38)
    rust=(150,120,80)
    pts=[(cx-L/2,cy-Hh*0.55),(cx-L*0.34,cy-Hh*0.85),(cx+L*0.20,cy-Hh),
         (cx+L*0.46,cy-Hh*0.85),(cx+L/2,cy-Hh*0.4),
         (cx+L/2,cy+Hh*0.6),(cx+L*0.42,cy+Hh),(cx-L*0.30,cy+Hh*0.95),
         (cx-L/2,cy+Hh*0.4)]
    cv.fill_polygon(pts,hull); cv.poly_outline(pts,dark,3)
    for i in range(3):
        cv.line(cx-L*0.44+i*26,cy-Hh*0.5,cx-L*0.38+i*26,cy+Hh*0.5,dark,2)
    for (ry,rh,col_) in (((cy-Hh*0.55,Hh*0.5,(150,90,60)),
                          (cy-Hh*0.05,Hh*0.5,(120,110,70)),
                          (cy+Hh*0.45,Hh*0.55,(100,90,120)))):
        x0=cx-L*0.30; w_=L*0.66
        cv.fill_rect(x0,ry,w_,rh,col_); cv.rect(x0,ry,w_,rh,dark,2)
        n=9
        for i in range(n):
            cv.line(x0+i*w_/n,ry,x0+i*w_/n,ry+rh,dark,2)
    bpx,bpy=cx+L*0.30,cy-Hh-92
    for sxx in (-40,40):
        cv.fill_rect(bpx+sxx-7,cy-Hh,14,92,dark)
    bp=[(bpx-95,bpy+18),(bpx-70,bpy-38),(bpx+70,bpy-38),(bpx+95,bpy+18),(bpx+80,bpy+52),(bpx-80,bpy+52)]
    cv.fill_polygon(bp,(150,130,100)); cv.poly_outline(bp,dark,3)
    windows(cv,[(bpx-50,bpy+6),(bpx-30,bpy+6),(bpx-10,bpy+6),(bpx+10,bpy+6),(bpx+30,bpy+6)])
    cv.ring(bpx-70,bpy-40,20,(200,190,160),3); cv.line(bpx-70,bpy-40,bpx-70,bpy-60,dark,3)
    cv.ring(bpx+40,bpy-42,14,(200,190,160),3)
    for i in range(3):
        px_=cx-L*0.18+i*L*0.2
        cv.fill_rect(px_-70,cy+Hh-4,140,74,(90,96,110)); cv.rect(px_-70,cy+Hh-4,140,74,dark,2)
    greeble(cv,cx-L*0.28,cy-Hh*0.3,L*0.6,Hh*0.6,rust,dark,12,20)
    for i in range(5):
        py_=cy+Hh*0.15+i*12
        cv.line(cx-L*0.24,py_,cx+L*0.1,py_,dark,3)
    turret(cv,cx-L*0.36,cy-Hh*0.75,16,(210,120,70))
    turret(cv,cx+L*0.14,cy-Hh-6,14,(210,120,70))
    engine(cv,cx+L/2-8,cy-Hh*0.42,62,(255,180,90),dark)
    engine(cv,cx+L/2-8,cy+Hh*0.42,62,(255,160,80),dark)
    for i in range(12,0,-1):
        cv.fill_polygon([(cx+L/2-4,cy-Hh*0.85),(cx+L/2+i*80,cy-Hh*0.42+(Hh*0.42*i/12)),
                         (cx+L/2+i*80,cy-Hh*0.42-(Hh*0.42*i/12))],(255,180,90,int(22*i/12)))
    title(cv,"CHIAROSCURO","FRONTIER TRADER 300 T - PIRATES HOUNDS OF THE CURSED MOON - VUE EXTERIEURE")
    save_png('ext_chiaroscuro.png',cv)

def dragonclaw_exterior():
    W,H=1500,950
    cv=Canvas(W,H,ss=2,bg=None)
    backdrop(cv,55,'red')
    cx,cy=W*0.5,H*0.5
    L,Hh=1100,120
    hull,dark=(118,128,132),(46,52,56)
    gun=(95,105,110); red=(190,55,50)
    pts=[(cx-L*0.30,cy-Hh*0.35),(cx-L*0.10,cy-Hh*0.55),(cx+L*0.26,cy-Hh*0.8),
         (cx+L*0.44,cy-Hh*0.6),(cx+L/2,cy-Hh*0.25),
         (cx+L/2,cy+Hh*0.55),(cx+L*0.36,cy+Hh),(cx-L*0.16,cy+Hh*0.9),
         (cx-L*0.34,cy+Hh*0.45)]
    cv.fill_polygon(pts,hull); cv.poly_outline(pts,dark,3)
    p1=[(cx+L/2,cy-Hh*0.22),(cx+L*0.60,cy-Hh*0.75),(cx+L*0.65,cy-Hh*0.12),(cx+L*0.58,cy+Hh*0.1)]
    p2=[(cx+L/2,cy+Hh*0.35),(cx+L*0.58,cy+Hh*0.72),(cx+L*0.62,cy+Hh*0.25),(cx+L*0.56,cy+Hh*0.05)]
    cv.fill_polygon(p1,hull); cv.poly_outline(p1,dark,3)
    cv.fill_polygon(p2,hull); cv.poly_outline(p2,dark,3)
    for i in range(3):
        bx=cx-L*0.24+i*L*0.17
        cv.fill_polygon([(bx,cy-Hh*0.7),(bx+26,cy-Hh*0.72),(bx+26,cy+Hh*0.85),(bx,cy+Hh*0.85)],red)
    cv.fill_rect(cx-L*0.12,cy-Hh*1.25,220,20,gun); cv.rect(cx-L*0.12,cy-Hh*1.25,220,20,dark,3)
    cv.fill_rect(cx+L*0.10,cy-Hh*1.5,26,40,gun); cv.rect(cx+L*0.10,cy-Hh*1.5,26,40,dark,3)
    greeble(cv,cx-L*0.30,cy-Hh*0.3,L*0.5,Hh*0.6,gun,dark,14,26)
    for i in range(1,9):
        xx=cx-L*0.30+i*L*0.09
        cv.line(xx,cy-Hh*0.5,xx,cy+Hh*0.5,dark,2)
    cv.fill_rect(cx+L*0.30,cy-Hh*0.35,70,14,(150,205,240))
    cv.rect(cx+L*0.30,cy-Hh*0.35,70,14,dark,2)
    for i,ey in enumerate((cy-Hh*0.5,cy,cy+Hh*0.5)):
        engine(cv,cx-L/2-10,ey,40,(120,255,170),dark)
    for i in range(12,0,-1):
        cv.fill_polygon([(cx-L/2-6,cy-Hh*0.9),(cx-L/2-i*70,cy-Hh*0.5+(Hh*0.5*i/12)*1.8),
                         (cx-L/2-i*70,cy-Hh*0.5-(Hh*0.5*i/12)*1.8)],(120,255,170,int(22*i/12)))
    title(cv,"MERC DRAGON CLAW","RAIDER - MERCENAIRES - VUE EXTERIEURE")
    save_png('ext_dragonclaw.png',cv)

which=sys.argv[1] if len(sys.argv)>1 else 'all'
if which in ('all','hotcomet'): hotcomet_exterior(); print('hotcomet ok')
if which in ('all','chiaroscuro'): chiaroscuro_exterior(); print('chiaroscuro ok')
if which in ('all','dragonclaw'): dragonclaw_exterior(); print('dragonclaw ok')
