from hv import *
import math, random

def crate(cv,x,y,s=34,col=(128,104,70)):
    cv.fill_rect(x,y,s,s,col); cv.rect(x,y,s,s,(40,34,26),3)
    cv.line(x,y,x+s,y+s,(40,34,26),2)

def bunk(cv,x,y,w=76,h=38):
    cv.fill_rect(x,y,w,h,(52,58,70)); cv.rect(x,y,w,h,(30,34,42),2)
    cv.fill_rect(x+3,y+3,22,h-6,(116,124,138))

def iris(cv,x,y,r=15,col=C_ACC):
    cv.fill_circle(x,y,r,(26,30,38))
    cv.ring(x,y,r,col,3); cv.ring(x,y,r*0.6,col,2)
    for i in range(6):
        a=math.pi*i/3
        cv.line(x+math.cos(a)*r*0.6,y+math.sin(a)*r*0.6,x+math.cos(a)*r,y+math.sin(a)*r,col,2)
def iris_at(cv,x,y,r=15): iris(cv,x,y,r)

def airlock_ext(cv,x,y,r=22):
    cv.ring(x,y,r,C_ACC,4); cv.ring(x,y,r-7,(120,150,190),2)
    for i in range(4):
        a=math.pi/2*i+math.pi/4
        cv.line(x+math.cos(a)*(r+4),y+math.sin(a)*(r+4),x+math.cos(a)*(r+13),y+math.sin(a)*(r+13),C_ACC,3)

def hatch_door(cv,cx,cy,w=140,horizontal=True):
    if horizontal:
        cv.rect(cx-w/2,cy-16,w,32,C_TEXT,3)
        cv.line(cx,cy-16,cx,cy+16,C_TEXT,3)
        for dx in (-w*0.3,w*0.3):
            cv.fill_polygon([(cx+dx,cy+27),(cx+dx-8,cy+13),(cx+dx+8,cy+13)],C_TEXT)
            cv.fill_polygon([(cx+dx,cy-27),(cx+dx-8,cy-13),(cx+dx+8,cy-13)],C_TEXT)
    else:
        cv.rect(cx-16,cy-w/2,32,w,C_TEXT,3)
        cv.line(cx-16,cy,cx+16,cy,C_TEXT,3)
        for dy in (-w*0.3,w*0.3):
            cv.fill_polygon([(cx+27,cy+dy),(cx+13,cy+dy-8),(cx+13,cy+dy+8)],C_TEXT)
            cv.fill_polygon([(cx-27,cy+dy),(cx-13,cy+dy-8),(cx-13,cy+dy+8)],C_TEXT)

def turret(cv,x,y,r,col=(210,120,70)):
    cv.fill_circle(x,y,r,col); cv.ring(x,y,r,(40,34,28),3)
    cv.line(x,y,x+r*1.7,y-r*0.5,(40,34,28),6); cv.fill_circle(x,y,r*0.4,(60,50,40))

def docking_collar(cv,x,y,r=18):
    cv.ring(x,y,r,C_ACC,3); cv.ring(x,y,r*0.55,(120,150,190),2)
    for i in range(8):
        a=math.pi*i/4; cv.fill_circle(x+math.cos(a)*r*0.8,y+math.sin(a)*r*0.8,2,C_DIM)

def fuel_tank(cv,x,y,r=24):
    cv.fill_circle(x,y,r,(104,112,122)); cv.ring(x,y,r,(40,44,50),3)
    cv.line(x,y-r,x,y+r,(40,44,50),3); cv.line(x-r,y,x+r,y,(40,44,50),3)

def generator(cv,x,y,w=70,h=50):
    cv.fill_rect(x,y,w,h,(92,88,96)); cv.rect(x,y,w,h,(40,38,44),3)
    for i in range(3): cv.line(x+6+i*(w-12)/2,y+6,x+6+i*(w-12)/2,y+h-6,(60,56,64),4)
    cv.fill_circle(x+w/2,y+h/2,7,(230,150,80,230))

def console(cv,x,y,w=90,h=26):
    cv.fill_rect(x,y,w,h,(40,44,52)); cv.rect(x,y,w,h,(24,28,34),2)
    cv.fill_rect(x+4,y+4,w-8,8,(96,168,232,220))

def table(cv,x,y,w=90,h=40):
    cv.fill_rect(x,y,w,h,(96,86,62)); cv.rect(x,y,w,h,(44,38,26),3)

def airraft(cv,x,y):
    pts=[(x-62,y-26),(x+26,y-26),(x+58,y-4),(x+58,y+4),(x+26,y+26),(x-62,y+26),(x-72,y)]
    cv.fill_polygon(pts,(150,158,168)); cv.poly_outline(pts,(50,56,64),3)
    cv.fill_rect(x+18,y-10,26,14,(130,190,225,230))
    cv.line(x-56,y+30,x+50,y+30,(70,76,84),4)

def station_label(cv,cx,cy,maxw,s,col=C_TEXT,maxsc=2,minsc=1):
    s=norm(s); words=s.split()
    sc=maxsc; lines=[s]
    while sc>=minsc:
        lines=[]; cur=''; ok=True
        for wd in words:
            t=(cur+' '+wd).strip()
            if textw(t,sc)<=maxw: cur=t
            else:
                if not cur: ok=False; break
                lines.append(cur)
                if textw(wd,sc)>maxw: ok=False; break
                cur=wd
        if not ok: sc-=1; continue
        lines.append(cur); break
    if sc<minsc: sc=minsc; lines=[s]
    lh=9*sc
    y=cy-(len(lines)-1)*lh/2 - 3.5*sc
    for ln in lines:
        cv.text(cx-textw(ln,sc)/2, y, ln, col, sc)
        y+=lh

def panel_lines(cv,x,y,w,h,col,n=6,t=1):
    for i in range(1,n):
        yy=y+i*h/n
        cv.line(x,yy,x+w,yy,col,t)

def scale_bar(cv,x,y,n=4,cell=44,col=C_TEXT):
    for i in range(n):
        c=col if i%2==0 else (60,66,78)
        cv.fill_rect(x+i*cell,y,cell,8,c)
    cv.rect(x,y,n*cell,8,(30,34,42),1)

def stars(cv,seed,n=260):
    rnd=random.Random(seed)
    for _ in range(n):
        x=rnd.uniform(0,cv.W); y=rnd.uniform(0,cv.H); b=int(rnd.uniform(90,255))
        cv.fill_rect(x,y,1.5,1.5,(b,b,min(255,b+30),255))

def windows(cv,pts):
    for (x,y) in pts:
        cv.fill_rect(x-7,y-3,14,6,(190,222,250,235))
        cv.rect(x-8,y-4,16,8,(30,34,40),2)

def greeble(cv,x,y,w,h,col,dark,n=14,sz=22):
    rnd=random.Random(int(x*13+y*7))
    for _ in range(n):
        gw=rnd.uniform(sz*0.4,sz); gh=rnd.uniform(sz*0.3,sz*0.7)
        gx=x+rnd.uniform(0,max(1,w-gw)); gy=y+rnd.uniform(0,max(1,h-gh))
        cv.fill_rect(gx,gy,gw,gh,col); cv.rect(gx,gy,gw,gh,dark,2)

def engine(cv,x,y,r,flame,dark):
    cv.fill_polygon([(x,y-r*0.62),(x+r,y-r*0.38),(x+r,y+r*0.38),(x,y+r*0.62)],dark)
    cv.fill_polygon([(x,y-r*0.4),(x+r*0.9,y-r*0.2),(x+r*0.9,y+r*0.2),(x,y+r*0.4)],flame)
    cv.fill_circle(x+r*1.3,y,r*0.55,(flame[0],flame[1],flame[2],90))

def title(cv,name,sub):
    cv.fill_rect(0,cv.H-96,cv.W,96,(0,0,0,110))
    cv.text(34,cv.H-82,name,C_TEXT,5)
    cv.text(34,cv.H-38,sub,C_DIM,2)

def ship_topdown(cv,cx,top,L,Wd,kind='courier'):
    hull=(124,134,150); dark=(36,42,50); glass=(150,205,240)
    def P(pts,fill=None):
        cv.fill_polygon(pts,fill or hull); cv.poly_outline(pts,dark,3)
    if kind=='courier':
        P([(cx,top),(cx+Wd*0.10,top+L*0.22),(cx+Wd*0.13,top+L*0.6),(cx+Wd*0.10,top+L*0.9),(cx,top+L),(cx-Wd*0.10,top+L*0.9),(cx-Wd*0.13,top+L*0.6),(cx-Wd*0.10,top+L*0.22)])
        P([(cx+Wd*0.13,top+L*0.30),(cx+Wd*0.5,top+L*0.72),(cx+Wd*0.5,top+L*0.88),(cx+Wd*0.13,top+L*0.66)])
        P([(cx-Wd*0.13,top+L*0.30),(cx-Wd*0.5,top+L*0.72),(cx-Wd*0.5,top+L*0.88),(cx-Wd*0.13,top+L*0.66)])
        cv.fill_rect(cx-Wd*0.05,top+L*0.08,Wd*0.10,L*0.09,glass)
        cv.fill_rect(cx-Wd*0.09,top+L*0.88,Wd*0.07,L*0.06,(70,76,86))
        cv.fill_rect(cx+Wd*0.02,top+L*0.88,Wd*0.07,L*0.06,(70,76,86))
        cv.fill_circle(cx-Wd*0.055,top+L*1.0,9,(150,200,255,170))
        cv.fill_circle(cx+Wd*0.055,top+L*1.0,9,(150,200,255,170))
    elif kind=='trader':
        P([(cx-Wd*0.30,top+L*0.12),(cx+Wd*0.02,top+L*0.04),(cx+Wd*0.28,top+L*0.2),(cx+Wd*0.28,top+L*0.8),(cx+Wd*0.02,top+L*0.96),(cx-Wd*0.30,top+L*0.88)])
        for f in (0.22,0.58):
            P([(cx-Wd*0.48,top+L*f),(cx-Wd*0.30,top+L*(f+0.06)),(cx-Wd*0.30,top+L*(f+0.2)),(cx-Wd*0.48,top+L*(f+0.14))],(108,98,84))
        P([(cx+Wd*0.28,top+L*0.38),(cx+Wd*0.44,top+L*0.42),(cx+Wd*0.44,top+L*0.56),(cx+Wd*0.28,top+L*0.60)])
        cv.fill_rect(cx-Wd*0.06,top+L*0.14,Wd*0.12,L*0.08,glass)
        for i in range(3): cv.fill_rect(cx-Wd*0.12+i*Wd*0.12,top+L*0.9,Wd*0.08,L*0.06,(70,76,86))
    elif kind=='raider':
        P([(cx-Wd*0.09,top+L*0.30),(cx-Wd*0.16,top+L*0.75),(cx-Wd*0.09,top+L),(cx+Wd*0.09,top+L),(cx+Wd*0.16,top+L*0.75),(cx+Wd*0.09,top+L*0.30)])
        P([(cx-Wd*0.28,top),(cx-Wd*0.09,top+L*0.24),(cx-Wd*0.05,top+L*0.36),(cx-Wd*0.26,top+L*0.16)])
        P([(cx+Wd*0.28,top),(cx+Wd*0.09,top+L*0.24),(cx+Wd*0.05,top+L*0.36),(cx+Wd*0.26,top+L*0.16)])
        cv.fill_rect(cx-Wd*0.14,top+L*0.52,Wd*0.28,L*0.05,(190,55,50))
        cv.fill_rect(cx-Wd*0.13,top+L*0.68,Wd*0.26,L*0.04,(190,55,50))
        P([(cx-Wd*0.30,top+L*0.55),(cx-Wd*0.09,top+L*0.6),(cx-Wd*0.09,top+L*0.75),(cx-Wd*0.30,top+L*0.8)],(104,112,118))
        P([(cx+Wd*0.30,top+L*0.55),(cx+Wd*0.09,top+L*0.6),(cx+Wd*0.09,top+L*0.75),(cx+Wd*0.30,top+L*0.8)],(104,112,118))
        cv.fill_rect(cx-Wd*0.05,top+L*0.9,Wd*0.1,L*0.05,(70,76,86))
        cv.fill_circle(cx,top+L*1.02,10,(120,255,170,160))
    elif kind=='fighter':
        P([(cx,top),(cx+Wd*0.34,top+L*0.45),(cx+Wd*0.34,top+L*0.7),(cx+Wd*0.12,top+L),(cx-Wd*0.12,top+L),(cx-Wd*0.34,top+L*0.7),(cx-Wd*0.34,top+L*0.45)])
        cv.fill_rect(cx-Wd*0.06,top+L*0.1,Wd*0.12,L*0.08,glass)
        cv.fill_rect(cx-Wd*0.16,top+L*0.86,Wd*0.32,L*0.07,(70,76,86))
        cv.fill_circle(cx,top+L*1.02,8,(150,200,255,170))
