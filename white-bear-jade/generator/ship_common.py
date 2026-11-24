from hv import *
from maps_lib import *

T=5

def build(cv,x0,y0,w,h,bow='right'):
    if bow=='flat':
        pts=[(x0+18,y0),(x0+w-18,y0),(x0+w,y0+18),(x0+w,y0+h-18),(x0+w-18,y0+h),(x0+18,y0+h),(x0,y0+h-18),(x0,y0+18)]
    else:
        pts=[(x0+6,y0+12),(x0+w*0.66,y0+6),(x0+w*0.86,y0+h*0.16),(x0+w-8,y0+h*0.5),
             (x0+w*0.86,y0+h*0.84),(x0+w*0.66,y0+h-6),(x0+6,y0+h-12),(x0,y0+h*0.5)]
    cv.fill_polygon(pts,(58,64,76))
    cv.poly_outline(pts,(28,32,40),4)
    cv.set_clip(x0+10,y0+10,w-20,h-20)
    for i in range(1,8):
        yy=y0+10+i*(h-20)/8
        cv.line(x0+10,yy,x0+w-10,yy,(50,56,66),1)
    gx=int(x0//44)*44
    while gx<x0+w:
        cv.line(gx,y0+8,gx,y0+h-8,(255,255,255,14),1)
        gx+=44
    gy=int(y0//44)*44
    while gy<y0+h:
        cv.line(x0+8,gy,x0+w-8,gy,(255,255,255,14),1)
        gy+=44
    cv.clear_clip()
    return pts

def _wh(cv,x,y,w,t,gaps,col):
    segs=[]; cur=x
    for pos,wd in sorted(gaps):
        gx=x+pos
        if gx>cur: segs.append((cur,gx-cur))
        cur=gx+wd
    if cur<x+w: segs.append((cur,x+w-cur))
    for sx,sw in segs:
        if sw>0: cv.fill_rect(sx,y,sw,t,col)
    for pos,wd in gaps:
        gx=x+pos
        cv.fill_rect(gx-2,y,3,t,C_ACC)
        cv.fill_rect(gx+wd-1,y,3,t,C_ACC)

def _wv(cv,x,y,h,t,gaps,col):
    segs=[]; cur=y
    for pos,wd in sorted(gaps):
        gy=y+pos
        if gy>cur: segs.append((cur,gy-cur))
        cur=gy+wd
    if cur<y+h: segs.append((cur,y+h-cur))
    for sy,sh in segs:
        if sh>0: cv.fill_rect(x,sy,t,sh,col)
    for pos,wd in gaps:
        gy=y+pos
        cv.fill_rect(x,gy-2,t,3,C_ACC)
        cv.fill_rect(x,gy+wd-1,t,3,C_ACC)

def room(cv,x,y,w,h,label,doors=(),col=C_FLOOR,lcol=C_TEXT,maxsc=2,minsc=1,t=T,wcol=(216,220,228)):
    cv.fill_rect(x,y,w,h,col)
    gN=[(p,d) for (s,p,d) in doors if s=='N']
    gS=[(p,d) for (s,p,d) in doors if s=='S']
    gW=[(p,d) for (s,p,d) in doors if s=='W']
    gE=[(p,d) for (s,p,d) in doors if s=='E']
    _wh(cv,x,y,w,t,gN,wcol)
    _wh(cv,x,y+h-t,w,t,gS,wcol)
    _wv(cv,x,y+t,h-2*t,t,gW,wcol)
    _wv(cv,x+w-t,y+t,h-2*t,t,gE,wcol)
    if label: station_label(cv,x+w/2,y+h/2,w-12,label,lcol,maxsc,minsc)

def corridor(cv,x,y,w,h,label='COULOIR'):
    cv.fill_rect(x,y,w,h,(64,70,82))
    xx=x+8
    while xx<x+w-14:
        cv.fill_rect(xx,y+h/2,10,1,(52,58,68))
        xx+=24
    station_label(cv,x+w/2,y+h/2,w-40,label,C_DIM,2,1)

def finish(cv,name,sub):
    cv.fill_rect(0,0,cv.W,58,(15,19,27))
    cv.rect(0,0,cv.W,58,(58,66,80),2)
    cv.text(18,10,name,C_TEXT,4)
    cv.text(18,40,sub,C_DIM,2)
    scale_bar(cv,cv.W-232,20)
    cv.text(cv.W-232,34,'1 CASE = 1,5 M',C_DIM,2)

def nozzles(cv,x,cy,r=26,flame=(150,200,255)):
    cv.fill_polygon([(x,cy-r*0.7),(x-r*0.9,cy-r*0.45),(x-r*0.9,cy+r*0.45),(x,cy+r*0.7)],(36,42,50))
    cv.fill_circle(x-r*1.2,cy,r*0.5,(flame[0],flame[1],flame[2],120))
