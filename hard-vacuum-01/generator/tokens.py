from hv import *
from maps_lib import *

def base(cv,ringcol,cx=128,cy=118,r=106):
    cv.fill_circle(cx,cy,r,(16,20,26,255))
    cv.ring(cx,cy,r,ringcol,9)
    cv.ring(cx,cy,r-9,(36,42,52,255),2)

def person(cv,cx,cy,suit,skin,weapon=None,helmet=False,glasses=False,trim=None):
    sh=[(cx-60,cy+80),(cx-38,cy-6),(cx+38,cy-6),(cx+60,cy+80)]
    cv.fill_polygon(sh,suit); cv.poly_outline(sh,(26,30,36),3)
    if trim: cv.fill_rect(cx-38,cy-2,76,8,trim)
    cv.fill_circle(cx,cy-44,28,skin); cv.ring(cx,cy-44,28,(26,30,36),3)
    if helmet:
        cv.fill_rect(cx-30,cy-64,60,20,suit)
        cv.fill_rect(cx-22,cy-56,44,9,(120,200,235,230))
    if glasses:
        cv.ring(cx-10,cy-48,7,(230,232,236),2); cv.ring(cx+10,cy-48,7,(230,232,236),2)
        cv.line(cx-3,cy-48,cx+3,cy-48,(230,232,236),2)
    if weapon in ('rifle','gauss'):
        cv.line(cx-74,cy+30,cx+66,cy+46,(58,56,52),9)
        cv.fill_rect(cx-76,cy+24,16,26,(46,44,40))
        cv.fill_rect(cx-8,cy+42,14,22,(46,44,40))
        if weapon=='gauss':
            for i in range(4): cv.ring(cx-40+i*22,cy+35,5,(150,190,230),2)
    elif weapon=='laser':
        cv.line(cx-74,cy+30,cx+62,cy+44,(70,68,64),8)
        cv.ring(cx+66,cy+45,7,(230,120,90),3)
        cv.fill_circle(cx+66,cy+45,4,(255,120,80,230))
    elif weapon=='smg':
        cv.line(cx-50,cy+34,cx+40,cy+44,(58,56,52),9)
        cv.fill_rect(cx-6,cy+42,12,20,(46,44,40))
    elif weapon=='cutlass':
        cv.line(cx-60,cy+72,cx+58,cy+32,(200,205,215),7)
        cv.line(cx-60,cy+72,cx-48,cy+52,(150,110,70),6)
    if weapon=='demo':
        for i in range(3): cv.fill_rect(cx-16+i*11,cy+40,8,22,(200,60,50))
        cv.fill_circle(cx-12,cy+62,4,(240,200,90,230))

def token(path,label,ringcol,drawfn):
    cv=Canvas(256,256,ss=2,bg=None)
    base(cv,ringcol)
    drawfn(cv,128,118)
    cv.text(128-textw(label,2)/2,238,label,C_TEXT,2)
    save_png(path,cv)
    print('ok',path)

def ship_token(path,label,kind):
    cv=Canvas(256,256,ss=2,bg=None)
    cv.glow(128,120,80,(120,160,230),55)
    ship_topdown(cv,128,40,180,140,kind)
    cv.text(128-textw(label,2)/2,240,label,C_TEXT,2)
    save_png(path,cv)
    print('ok',path)

R=(176,64,60); G=(224,176,88); M=(96,120,168)

token('token_pirate_chef.png','CHEF PIRATE',G,lambda cv,cx,cy: person(cv,cx,cy,(60,58,64),(206,170,140),weapon='cutlass',trim=G))
token('token_pirate_demo.png','DEMOLITIONNAIRE',R,lambda cv,cx,cy: person(cv,cx,cy,(66,54,48),(196,156,124),weapon='demo'))
token('token_pirate_3.png','PIRATE 3',R,lambda cv,cx,cy: person(cv,cx,cy,(70,56,50),(196,160,130),weapon='laser'))
token('token_pirate_4.png','PIRATE 4',R,lambda cv,cx,cy: person(cv,cx,cy,(64,60,54),(186,150,120),weapon='rifle'))
token('token_pirate_5.png','PIRATE 5',R,lambda cv,cx,cy: person(cv,cx,cy,(74,52,46),(200,164,134),weapon='smg'))
token('token_vuurst.png','VUURST',(96,160,140),lambda cv,cx,cy: person(cv,cx,cy,(150,152,158),(218,190,166),weapon=None,glasses=True))
token('token_merc_comdt.png','COMDT',G,lambda cv,cx,cy: person(cv,cx,cy,(70,78,92),(190,158,128),weapon='gauss',helmet=True,trim=G))
token('token_merc_1.png','MERC 1',M,lambda cv,cx,cy: person(cv,cx,cy,(70,78,92),(196,164,132),weapon='gauss',helmet=True))
token('token_merc_2.png','MERC 2',M,lambda cv,cx,cy: person(cv,cx,cy,(62,70,84),(186,154,124),weapon='rifle',helmet=True))

def robotfn(cv,cx,cy):
    cv.line(cx,cy-96,cx,cy-118,(150,158,168),3)
    cv.fill_circle(cx,cy-120,4,(230,120,70,255))
    cv.fill_rect(cx-34,cy-80,68,50,(120,128,138)); cv.rect(cx-34,cy-80,68,50,(36,42,50),3)
    cv.fill_circle(cx-13,cy-58,6,(230,150,80,255)); cv.fill_circle(cx+13,cy-58,6,(230,150,80,255))
    cv.fill_rect(cx-46,cy-24,92,76,(96,104,114)); cv.rect(cx-46,cy-24,92,76,(36,42,50),3)
    for i in range(3): cv.line(cx-38,cy-8+i*20,cx+38,cy-8+i*20,(60,66,74),3)
    cv.fill_rect(cx-58,cy+54,116,24,(58,64,72)); cv.rect(cx-58,cy+54,116,24,(30,34,40),2)
    for i in range(4): cv.fill_circle(cx-44+i*30,cy+66,6,(40,44,50))
token('token_robot.png','ROBOT',(150,158,170),robotfn)

ship_token('token_ship_hotcomet.png','HOT COMET','courier')
ship_token('token_ship_chiaroscuro.png','CHIAROSCURO','trader')
ship_token('token_ship_dragonclaw.png','DRAGON CLAW','raider')
print('tokens ok')
