from hv import *
from maps_lib import *
import math

CELL=44   # 1 case = 44 px = 1,5 m
T=5       # epaisseur mur, centre sur ligne de grille

def grid_overlay(cv,x,y,w,h,col=(255,255,255,22)):
    for gx in range(int(x),int(x+w)+1,CELL):
        cv.line(gx,y,gx,y+h,col,1)
    for gy in range(int(y),int(y+h)+1,CELL):
        cv.line(x,gy,x+w,gy,col,1)

def _wh(cv,y,x0,x1,gaps,col):
    segs=[];cur=x0
    for s,wd in sorted(gaps):
        if s>cur: segs.append((cur,s-cur))
        cur=s+wd
    if cur<x1: segs.append((cur,x1-cur))
    for sx,sw in segs:
        if sw>0: cv.fill_rect(sx,y-T/2,sw,T,col)
    for s,wd in gaps:
        cv.fill_rect(s-3,y-T/2,3,T,C_ACC)
        cv.fill_rect(s+wd,y-T/2,3,T,C_ACC)

def _wv(cv,x,y0,y1,gaps,col):
    segs=[];cur=y0
    for s,wd in sorted(gaps):
        if s>cur: segs.append((cur,s-cur))
        cur=s+wd
    if cur<y1: segs.append((cur,y1-cur))
    for sy,sh in segs:
        if sh>0: cv.fill_rect(x,sy-T/2,T,sh,col)
    for s,wd in gaps:
        cv.fill_rect(x-T/2,s-3,T,3,C_ACC)
        cv.fill_rect(x-T/2,s+wd,T,3,C_ACC)

def groom(cv,gx,gy,gw,gh,label=None,doors=(),col=C_FLOOR,lcol=C_TEXT,maxsc=2,minsc=1,wcol=(216,220,228)):
    """Piece alignee grille: (gx,gy,gw,gh) en cases de 44px.
    doors: (cote, offset_px, largeur_px) - offsets multiples de 22."""
    x,y,w,h=gx*CELL,gy*CELL,gw*CELL,gh*CELL
    cv.fill_rect(x,y,w,h,col)
    dN=[(x+p,wd) for s,p,wd in doors if s=='N']
    dS=[(x+p,wd) for s,p,wd in doors if s=='S']
    dW=[(y+p,wd) for s,p,wd in doors if s=='W']
    dE=[(y+p,wd) for s,p,wd in doors if s=='E']
    _wh(cv,y,x,x+w,dN,wcol)
    _wh(cv,y+h,x,x+w,dS,wcol)
    _wv(cv,x,y,y+h,dW,wcol)
    _wv(cv,x+w,y,y+h,dE,wcol)
    if label: station_label(cv,x+w/2,y+h/2,w-14,label,lcol,maxsc,minsc)
    return (x,y,w,h)

def gcor(cv,gx,gy,gw,gh,label='COULOIR'):
    x,y,w,h=gx*CELL,gy*CELL,gw*CELL,gh*CELL
    cv.fill_rect(x,y,w,h,(64,70,82))
    xx=x+10
    while xx<x+w-16:
        cv.fill_rect(xx,y+h-16,10,2,(52,58,68))
        xx+=26
    if label: station_label(cv,x+w/2,y+h/2-8,w-40,label,C_DIM,2,1)

def wall_h(cv,ypx,x0,x1,gaps=(),col=(216,220,228)):
    _wh(cv,ypx,x0,x1,list(gaps),col)
def wall_v(cv,xpx,y0,y1,gaps=(),col=(216,220,228)):
    _wv(cv,xpx,y0,y1,list(gaps),col)

# --- mobilier aligne (multiples de 22) ---

def luxbed(cv,x,y,w=88,h=44):
    cv.fill_rect(x,y,w,h,(120,44,52)); cv.rect(x,y,w,h,(50,24,28),3)
    cv.fill_rect(x+4,y+4,w*0.28,h-8,(210,214,222))
def desk(cv,x,y):
    cv.fill_rect(x,y,44,30,(96,86,62)); cv.rect(x,y,44,30,(44,38,26),2)
    cv.fill_circle(x+22,y+40,8,(90,98,112))
def fresher(cv,x,y,w=44,h=44):
    cv.fill_rect(x,y,w,h,C_FLOOR2); cv.rect(x,y,w,h,(216,220,228),2)
    cv.fill_rect(x+4,y+4,w-8,10,(96,168,232,200))
    cv.text(x+w/2-textw('F',1)/2,y+h-20,'F',C_DIM,1)
def closet(cv,x,y,w=44,h=44):
    cv.fill_rect(x,y,w,h,(92,72,50)); cv.rect(x,y,w,h,(44,38,26),2)
    cv.line(x+w/2,y+4,x+w/2,y+h-4,(44,38,26),2)
def bar(cv,x,y,w=176,h=44):
    cv.fill_rect(x,y,w,h,(74,50,36)); cv.rect(x,y,w,h,(36,26,18),3)
    for i in range(int((w-20)/22)):
        cv.fill_rect(x+12+i*22,y-14,8,14,(120+i%3*40,60+((i*7)%3)*50,70))
def sofa(cv,x,y,w=120,h=36):
    cv.fill_rect(x,y,w,h,(70,84,110)); cv.rect(x,y,w,h,(32,38,50),2)
    cv.fill_rect(x+4,y+4,w-8,10,(96,112,140))
def display_ped(cv,x,y,kind='armor'):
    cv.fill_rect(x,y,44,44,(58,62,72)); cv.rect(x,y,44,44,(30,34,42),2)
    if kind=='armor':
        cv.fill_polygon([(x+12,y+38),(x+12,y+16),(x+22,y+8),(x+32,y+16),(x+32,y+38)],(170,176,188))
        cv.line(x+22,y+8,x+22,y+38,(80,86,96),2)
    else:
        cv.line(x+10,y+36,x+34,y+12,(210,216,226),3)
        cv.line(x+10,y+28,x+18,y+36,(150,110,70),3)
        cv.line(x+10,y+36,x+16,y+30,(210,216,226),2)
def rack(cv,x,y,w=44,h=220):
    cv.fill_rect(x,y,w,h,(64,50,36)); cv.rect(x,y,w,h,(32,24,16),2)
    for i in range(3):
        yy=y+14+i*(h-28)/2
        cv.line(x+8,yy+18,x+w-8,yy-6,(210,216,226),3)
        cv.line(x+8,yy+18,x+14,yy+12,(150,110,70),3)
def corpse(cv,x,y):
    cv.fill_circle(x,y,17,(80,30,28,110))
    cv.fill_rect(x-16,y-6,24,12,(138,136,130))
    cv.fill_circle(x+15,y,8,(158,150,138))
    cv.fill_circle(x-18,y-6,5,(158,150,138))
def screen(cv,x,y,w=20,h=70):
    cv.fill_rect(x,y,w,h,(40,44,52)); cv.rect(x,y,w,h,(24,28,34),2)
    cv.fill_rect(x+3,y+4,w-6,h*0.4,(96,168,232,200))
def locker(cv,x,y,w=110,h=44,label='CASIER D\'ARMES'):
    cv.fill_rect(x,y,w,h,(70,74,86)); cv.rect(x,y,w,h,(36,40,48),3)
    cv.line(x+18,y+6,x+18,y+h-6,(210,180,120),4)
    cv.line(x+40,y+8,x+40,y+h-8,(210,216,226),4)
    cv.text(x+w/2-textw(label,1)/2,y+h+6,label,C_DIM,1)
def irisv(cv,x,y,r=13):
    iris(cv,x,y,r)
