# -*- coding: utf-8 -*-
# 포켓몬 골드(GBC) 느낌 다람쥐 + 인터랙티브 목업 GIF
from PIL import Image, ImageDraw, ImageFont
import math

# --- GBC풍 팔레트 (검은 외곽선 + 제한된 색 + 디더) ---
OUT=(40,32,28)
DK=(120,74,40)      # 어두운 갈색
MD=(176,116,62)     # 중간 갈색
LT=(232,202,156)    # 크림(배)
TAIL=(150,98,52)
TAILH=(198,146,86)
CHK=(228,150,150)   # 볼

def disc(d,cx,cy,r,c): d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=c)

def dither(d, box, c, step=2):
    x0,y0,x1,y1=box
    for y in range(int(y0),int(y1)):
        for x in range(int(x0),int(x1)):
            if (x+y)%step==0:
                d.point((x,y),fill=c)

def make_squirrel(scale=6, hat=None):
    W,H=46,44
    img=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(img)
    # 말린 꼬리 (스파이럴)
    cx0,cy0=16,25; pts=[]
    for i in range(0,28):
        ang=math.radians(120+i*10); rad=10-i*0.18
        pts.append((cx0+math.cos(ang)*rad, cy0-math.sin(ang)*rad))
    for x,y in pts: disc(d,int(x),int(y),6,OUT)
    for x,y in pts: disc(d,int(x),int(y),5,TAIL)
    for x,y in pts: disc(d,int(x),int(y),2,TAILH)
    # 몸통(검은 외곽선 + 셀 셰이딩)
    d.ellipse((20,14,40,40),fill=OUT)
    d.ellipse((21,15,39,39),fill=MD)
    d.ellipse((25,21,37,38),fill=LT)         # 배
    dither(d,(22,30,30,38),DK)               # 그림자 디더
    # 머리
    d.ellipse((24,2,44,21),fill=OUT)
    d.ellipse((25,3,43,20),fill=MD)
    dither(d,(25,15,33,20),DK)
    # 귀
    for ex in (29,40):
        d.ellipse((ex-3,0,ex+3,6),fill=OUT); d.ellipse((ex-2,1,ex+2,5),fill=MD)
        d.ellipse((ex-1,2,ex+1,4),fill=DK)
    # 눈 (크고 또렷한 GBC 눈)
    for ex in (31,38):
        d.ellipse((ex-2,8,ex+2,13),fill=OUT)
        d.ellipse((ex-2,8,ex+2,12),fill=(20,16,14))
        d.point((ex-1,9),fill=(255,255,255))
    # 코/입
    d.ellipse((33,13,37,16),fill=OUT)
    d.line((35,16,35,18),fill=OUT)
    # 볼
    disc(d,29,14,1,CHK); disc(d,40,14,1,CHK)
    # 앞발 + 작은 도토리
    d.ellipse((30,33,36,39),fill=OUT); d.ellipse((31,34,35,38),fill=DK)
    d.ellipse((35,32,40,37),fill=OUT)
    d.ellipse((36,34,39,37),fill=(170,112,58))   # 도토리알
    d.rectangle((36,32,39,34),fill=(96,62,30))   # 모자
    # 머리 장식(상점용)
    if hat=="acorn":
        d.ellipse((31,-1,40,4),fill=(96,62,30)); d.ellipse((33,-3,38,1),fill=(96,62,30))
    elif hat=="maple":
        d.polygon([(35,-3),(31,2),(34,1),(33,4),(35,2),(37,4),(36,1),(39,2)],fill=(206,86,46))
    return img.resize((W*scale,H*scale),Image.NEAREST)

# --- GBC풍 숲 배경 ---
def forest(W,H):
    bg=Image.new("RGB",(W,H),(196,224,200))
    d=ImageDraw.Draw(bg)
    for y in range(0,int(H*0.6)):
        t=y/(H*0.6); d.line((0,y,W,y),fill=(int(168+24*t),int(208+14*t),int(176+18*t)))
    import random; random.seed(5)
    for x in range(-10,W,40):
        h=random.randint(54,88); ty=int(H*0.6)-h
        d.rectangle((x+13,ty+h-18,x+19,ty+h),fill=(104,72,44))
        d.polygon([(x,ty+h-8),(x+30,ty+h-8),(x+15,ty)],fill=(86,148,84))
        d.polygon([(x+3,ty+h-20),(x+27,ty+h-20),(x+15,ty+12)],fill=(100,164,96))
    gy=int(H*0.6)
    d.rectangle((0,gy,W,H),fill=(120,186,92))
    d.rectangle((0,gy,W,gy+5),fill=(146,204,108))
    for ax,ay in [(40,gy+30),(150,gy+60),(300,gy+44),(250,gy+90)]:
        d.ellipse((ax,ay+3,ax+7,ay+10),fill=(170,112,58)); d.rectangle((ax,ay,ax+7,ay+4),fill=(96,62,30))
    return bg

KRB="/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/NanumGothicBold.ttf"
KRX="/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/NanumGothicExtraBold.ttf"
def f(s,x=0): return ImageFont.truetype(KRX if x else KRB,s)

PW,PH=340,600
BLUE=(49,130,246); SUB=(120,130,140); TEXT=(30,36,44); ACORN=(181,101,29)

def frame(stage_text, time_txt, prog, sess, balance, mode, hat=None, drop_y=None, toast=None):
    img=Image.new("RGB",(PW,PH),(242,244,246)); d=ImageDraw.Draw(img)
    # 상단 balance
    d.text((16,16),"다람쥐 뽀모도로",font=f(15,1),fill=TEXT)
    d.rounded_rectangle((PW-86,12,PW-14,40),14,fill=(255,247,236))
    d.ellipse((PW-78,20,PW-70,28),fill=(170,112,58)); d.rectangle((PW-78,18,PW-70,22),fill=(96,62,30))
    d.text((PW-64,17),str(balance),font=f(15,1),fill=ACORN)
    # 무대
    st=forest(PW,210); img.paste(st,(0,48))
    # 바닥에 쌓이는 도토리(진행도)
    for i in range(min(sess,5)):
        ax=28+i*15; d.ellipse((ax,236,ax+9,245),fill=(170,112,58)); d.rectangle((ax,233,ax+9,237),fill=(96,62,30))
    # 떨어지는 도토리
    if drop_y is not None:
        dy=48+60+drop_y
        d.ellipse((150,dy,160,dy+10),fill=(170,112,58)); d.rectangle((150,dy-3,160,dy+1),fill=(96,62,30))
    # 다람쥐
    sq=make_squirrel(5,hat=hat)
    img.paste(sq,(int(PW/2-sq.width/2)+40,int(258-sq.height+8)),sq)
    # 패널
    if mode=="setup":
        d.text((PW/2,300),stage_text,font=f(12),fill=SUB,anchor="mm")
        d.text((PW/2,344),"25",font=f(46,1),fill=TEXT,anchor="mm"); d.text((PW/2+52,356),"분",font=f(16),fill=SUB,anchor="lm")
        d.line((30,396,PW-30,396),fill=(225,228,232),width=6); d.line((30,396,150,396),fill=BLUE,width=6)
        d.ellipse((140,388,158,404),fill=BLUE)
        d.rounded_rectangle((24,430,PW-24,474),14,fill=BLUE)
        d.text((PW/2,452),"집중 시작",font=f(17,1),fill=(255,255,255),anchor="mm")
    elif mode=="focus":
        d.text((PW/2,298),stage_text,font=f(12),fill=SUB,anchor="mm")
        d.text((PW/2,344),time_txt,font=f(42,1),fill=BLUE,anchor="mm")
        d.rounded_rectangle((30,386,PW-30,395),4,fill=(225,228,232))
        d.rounded_rectangle((30,386,30+int((PW-60)*prog),395),4,fill=BLUE)
        d.text((PW/2,420),f"이번 집중 도토리: {sess}개",font=f(13),fill=SUB,anchor="mm")
        d.rounded_rectangle((24,448,PW-24,488),14,fill=(238,240,243))
        d.text((PW/2,468),"포기하기 (절반만 획득)",font=f(13),fill=SUB,anchor="mm")
    elif mode=="shop":
        d.text((PW/2,300),stage_text,font=f(12),fill=SUB,anchor="mm")
        d.rounded_rectangle((20,330,PW-20,378),12,fill=(255,255,255))
        d.ellipse((34,346,52,364),fill=(96,62,30)); d.ellipse((38,342,48,350),fill=(96,62,30))
        d.text((64,340),"도토리 모자",font=f(14,1),fill=TEXT); d.text((64,358),"방금 장착!",font=f(12),fill=SUB)
        d.rounded_rectangle((PW-86,344,PW-26,366),10,fill=BLUE); d.text((PW-56,355),"장착중",font=f(12),fill=(255,255,255),anchor="mm")
    # 토스트
    if toast:
        tw=int(f(14).getlength(toast))+36
        d.rounded_rectangle((PW/2-tw/2,250,PW/2+tw/2,284),12,fill=(28,34,40))
        d.text((PW/2,267),toast,font=f(14,1),fill=(255,255,255),anchor="mm")
    # 탭바
    d.rectangle((0,PH-46,PW,PH),fill=(255,255,255)); d.line((0,PH-46,PW,PH-46),fill=(229,232,235))
    for i,(name,act) in enumerate([("집중",mode in("setup","focus")),("상점",mode=="shop"),("도감",False)]):
        cx=int(PW/3*i+PW/6); d.text((cx,PH-26),name,font=f(12,1),fill=BLUE if act else SUB,anchor="mm")
    return img

# ---- GIF 프레임 시퀀스 ----
frames=[]; durs=[]
def add(im,ms): frames.append(im.convert("P",palette=Image.ADAPTIVE)); durs.append(ms)

# 1) 시작 화면
for _ in range(2): add(frame("집중할 시간을 정하고 시작해요","",0,0,12,"setup"),900)
# 2) 집중 진행 (5분 단위로 도토리 적립 + 낙하 연출)
seq=[("20:00",0.2,1),("15:00",0.4,2),("10:00",0.6,3),("05:00",0.8,4),("00:02",0.98,5)]
for t,p,s in seq:
    add(frame("집중 중이에요. 화면을 벗어나면 포기!",t,p,s-1,12,"focus",drop_y=10),250)
    add(frame("집중 중이에요. 화면을 벗어나면 포기!",t,p,s-1,12,"focus",drop_y=70),250)
    add(frame("집중 중이에요. 화면을 벗어나면 포기!",t,p,s,12,"focus"),300)
# 3) 성공
add(frame("","",1,5,17,"focus",toast="집중 성공! 🌰 5개 획득"),1500)
# 4) 상점에서 모자 장착
add(frame("도토리로 다람쥐를 꾸며요",":",0,5,12,"shop",hat="acorn"),1600)
add(frame("도토리로 다람쥐를 꾸며요",":",0,5,12,"shop",hat="acorn",toast="도토리 모자를 장착했어요!"),1600)

frames[0].save("/home/user/news/mockup_demo.gif",save_all=True,append_images=frames[1:],
               duration=durs,loop=0,disposal=2,optimize=True)

# 정적 미리보기: GBC 다람쥐 보드 (한 마리만, 전체 보이게)
board=forest(420,360); d=ImageDraw.Draw(board)
sq=make_squirrel(5)
gy=int(360*0.6)
board.paste(sq,(int(210-sq.width/2),gy-sq.height+30),sq)
d.rounded_rectangle((40,308,380,346),16,fill=(255,255,255))
d.text((210,327),"포켓몬 골드 느낌 8비트 다람쥐",font=f(17,1),fill=(40,50,60),anchor="mm")
board.save("/home/user/news/squirrel_gbc.png")

# GIF 프레임 점검용 몽타주
mont=Image.new("RGB",(PW*4+30,PH),(255,255,255))
picks=[2,8,14,18]
for i,fi in enumerate(picks):
    mont.paste(frames[fi].convert("RGB"),(i*(PW+8),0))
mont.save("/tmp/montage.png")
print("frames:",len(frames))
