import zlib, struct, math, unicodedata

C_BG=(20,24,32); C_HULL=(96,104,120); C_DARK=(30,34,42); C_FLOOR=(74,80,94); C_FLOOR2=(60,66,78)
C_WALL=(214,218,226); C_TEXT=(235,237,242); C_DIM=(150,158,170); C_ACC=(96,168,232)
C_RED=(196,84,72); C_GOLD=(224,176,88); C_GREEN=(108,178,120); C_ORANGE=(224,140,70)
C_CYAN=(110,190,200); C_GRID=(44,50,62)

FONT = {
 'A':[14,17,17,31,17,17,17],'B':[30,17,17,30,17,17,30],'C':[14,17,16,16,16,17,14],
 'D':[30,17,17,17,17,17,30],'E':[31,16,16,30,16,16,31],'F':[31,16,16,30,16,16,16],
 'G':[14,17,16,23,17,17,14],'H':[17,17,17,31,17,17,17],'I':[14,4,4,4,4,4,14],
 'J':[7,2,2,2,2,18,12],'K':[17,18,20,24,20,18,17],'L':[16,16,16,16,16,16,31],
 'M':[17,27,21,21,17,17,17],'N':[17,25,21,19,17,17,17],'O':[14,17,17,17,17,17,14],
 'P':[30,17,17,30,16,16,16],'Q':[14,17,17,17,21,18,13],'R':[30,17,17,30,20,18,17],
 'S':[15,16,16,14,1,1,30],'T':[31,4,4,4,4,4,4],'U':[17,17,17,17,17,17,14],
 'V':[17,17,17,17,17,10,4],'W':[17,17,17,21,21,27,17],'X':[17,17,10,4,10,17,17],
 'Y':[17,17,10,4,4,4,4],'Z':[31,1,2,4,8,16,31],
 '0':[14,17,19,21,25,17,14],'1':[4,12,4,4,4,4,14],'2':[14,17,1,6,8,16,31],
 '3':[31,2,4,6,1,17,14],'4':[2,6,10,18,31,2,2],'5':[31,16,30,1,1,17,14],
 '6':[6,8,16,30,17,17,14],'7':[31,1,2,4,8,8,8],'8':[14,17,17,14,17,17,14],
 '9':[14,17,17,15,1,2,12],
 ' ':[0,0,0,0,0,0,0],'-':[0,0,0,14,0,0,0],'_':[0,0,0,0,0,0,31],
 '.':[0,0,0,0,0,12,12],',':[0,0,0,0,6,6,12],':':[0,12,12,0,12,12,0],
 '/':[1,2,2,4,8,8,16],"'":[4,4,8,0,0,0,0],'(':[2,4,8,8,8,4,2],')':[8,4,2,2,2,4,8],
 '!':[4,4,4,4,4,0,4],'?':[14,17,1,6,4,0,4],'+':[0,4,4,31,4,4,0],
 '=':[0,0,31,0,31,0,0],'*':[0,21,14,31,14,21,0],'%':[25,26,2,4,8,11,19],
}

def _norm(s):
    s = unicodedata.normalize('NFD', str(s))
    return ''.join(c for c in s if not unicodedata.combining(c)).upper()

def norm(s):
    return _norm(s)

def textw(s, sc=1):
    s = _norm(s)
    return max(1, len(s))*6*sc - sc

class Canvas:
    def __init__(self, W, H, ss=1, bg=(20,24,32,255)):
        self.W=W; self.H=H; self.ss=float(ss)
        self.Ws=max(1,int(round(W*ss))); self.Hs=max(1,int(round(H*ss)))
        self.buf=[bytearray(self.Ws*4) for _ in range(self.Hs)]
        self._clipb=None
        if bg is not None:
            r,g,b,a=bg
            row=bytes((r,g,b,a))*self.Ws
            for yy in range(self.Hs): self.buf[yy][:]=row

    def set_clip(self,x,y,w,h):
        s=self.ss
        self._clipb=(int(round(x*s)),int(round(y*s)),int(round(w*s)),int(round(h*s)))
    def clear_clip(self): self._clipb=None

    def _spanb(self,ys,xs,xe,col):
        if ys<0 or ys>=self.Hs: return
        c=self._clipb
        if c is not None:
            if ys<c[1] or ys>=c[1]+c[3]: return
            if xs<c[0]: xs=c[0]
            if xe>c[0]+c[2]: xe=c[0]+c[2]
        if xs<0: xs=0
        if xe>self.Ws: xe=self.Ws
        if xe<=xs: return
        row=self.buf[ys]
        if len(col)>=4 and col[3]<255:
            r,g,b,a=col[0],col[1],col[2],col[3]; inv=255-a
            for x in range(xs,xe):
                i=x*4
                row[i]  =min(255,(r*a+row[i]*inv)//255)
                row[i+1]=min(255,(g*a+row[i+1]*inv)//255)
                row[i+2]=min(255,(b*a+row[i+2]*inv)//255)
                if row[i+3]<a: row[i+3]=a
        else:
            pat=bytes((col[0],col[1],col[2],255))
            row[xs*4:xe*4]=pat*(xe-xs)

    def span(self,y,x0,x1,col):
        s=self.ss
        self._spanb(int(round(y*s)),int(round(x0*s)),int(round(x1*s)),col)

    def fill_rect(self,x,y,w,h,col):
        if w<=0 or h<=0: return
        s=self.ss
        x0=int(round(x*s)); x1=int(round((x+w)*s))
        y0=int(round(y*s)); y1=int(round((y+h)*s))
        for ys in range(y0,y1):
            self._spanb(ys,x0,x1,col)

    def rect(self,x,y,w,h,col,t=1):
        self.fill_rect(x,y,w,t,col)
        self.fill_rect(x,y+h-t,w,t,col)
        self.fill_rect(x,y,t,h,col)
        self.fill_rect(x+w-t,y,t,h,col)

    def fill_circle(self,x,y,r,col):
        s=self.ss
        R=float(r)*s; X=float(x)*s; Y=float(y)*s
        y0=int(round(Y-R)); y1=int(round(Y+R))
        for ys in range(y0,y1+1):
            dy=ys+0.5-Y
            if abs(dy)>R: continue
            w=math.sqrt(max(0.0,R*R-dy*dy))
            self._spanb(ys,int(round(X-w)),int(round(X+w))+1,col)

    def ring(self,x,y,r,col,t=2):
        n=max(18,int((r*self.ss)*7))
        for i in range(n):
            a=2*math.pi*i/n
            self.fill_rect(x+math.cos(a)*r-t/2, y+math.sin(a)*r-t/2, t, t, col)

    def line(self,x0,y0,x1,y1,col,t=1):
        dx,dy=x1-x0,y1-y0
        n=int(max(abs(dx),abs(dy))*self.ss*2)+2
        for i in range(n+1):
            f=i/n
            self.fill_rect(x0+dx*f-t/2, y0+dy*f-t/2, t, t, col)

    def fill_polygon(self,pts,col):
        s=self.ss
        P=[(p[0]*s,p[1]*s) for p in pts]
        ys=[p[1] for p in P]
        ya=int(math.ceil(min(ys))); yb=int(max(ys))
        n=len(P)
        for y in range(ya,yb+1):
            xs=[]
            for i in range(n):
                a=P[i]; b=P[(i+1)%n]
                if (a[1]<=y<b[1]) or (b[1]<=y<a[1]):
                    xs.append(a[0]+(b[0]-a[0])*(y-a[1])/(b[1]-a[1]))
            xs.sort()
            for i in range(0,len(xs)-1,2):
                self._spanb(y,int(math.ceil(xs[i])),int(xs[i+1])+1,col)

    def poly_outline(self,pts,col,t=2):
        for i in range(len(pts)):
            a=pts[i]; b=pts[(i+1)%len(pts)]
            self.line(a[0],a[1],b[0],b[1],col,t)

    def hatch(self,x,y,w,h,col,step=12,t=1):
        self.set_clip(x,y,w,h)
        for d in range(-int(h),int(w)+int(h),step):
            self.line(x+d,y,x+d+h,y+h,col,t)
        self.clear_clip()

    def glow(self,x,y,r,col,strength=110):
        s=self.ss
        X=float(x)*s; Y=float(y)*s; R=max(1.0,float(r)*s)
        for dy in range(-int(R),int(R)+1):
            w=int(math.sqrt(max(0.0,R*R-dy*dy)))
            a=int(strength*(1.0-abs(dy)/R))
            if a>0:
                self._spanb(int(round(Y))+dy,int(round(X))-w,int(round(X))+w+1,(col[0],col[1],col[2],a))

    def text(self,x,y,s,col,sc=1):
        s=_norm(s)
        cx=float(x)
        for ch in s:
            g=FONT.get(ch, FONT.get(ch.upper(), FONT['?']))
            for j,row in enumerate(g):
                for i in range(5):
                    if row & (1<<(4-i)):
                        self.fill_rect(cx+i*sc, y+j*sc, sc, sc, col)
            cx+=6*sc

def save_png(path,cv):
    W,H=cv.Ws,cv.Hs
    raw=bytearray()
    for row in cv.buf:
        raw.append(0); raw+=row
    comp=zlib.compress(bytes(raw),9)
    def chunk(t,d):
        return struct.pack('>I',len(d))+t+d+struct.pack('>I', zlib.crc32(t+d)&0xffffffff)
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,6,0,0,0))
    png+=chunk(b'IDAT',comp)+chunk(b'IEND',b'')
    with open(path,'wb') as f: f.write(png)
