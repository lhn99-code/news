# -*- coding: utf-8 -*-
# 8비트 다람쥐 v2 - 동그랗게 말린 꼬리 + 작은 도토리 + 숲 배경
from PIL import Image, ImageDraw, ImageFont
import math

OUT=(58,36,20)      # 외곽선
BODY=(176,110,54)
BODYS=(150,90,42)
BELLY=(235,200,155)
TAIL=(158,98,48)
TAILH=(196,140,82)  # 꼬리 밝은 결
ACORN=(170,112,58)
ACAP=(96,62,30)

def disc(d, cx, cy, r, color):
    d.ellipse((cx-r,cy-r,cx+r,cy+r), fill=color)

def outlined_disc(d, cx, cy, r, color, ow=1):
    d.ellipse((cx-r-ow,cy-r-ow,cx+r+ow,cy+r+ow), fill=OUT)
    d.ellipse((cx-r,cy-r,cx+r,cy+r), fill=color)

def make_squirrel(scale):
    W,Hh=46,44
    img=Image.new("RGBA",(W,Hh),(0,0,0,0))
    d=ImageDraw.Draw(img)

    # ----- 꼬리: 말린 스파이럴 (몸 뒤에서 위로 동그랗게) -----
    # 스파이럴 경로를 따라 원을 찍어 두툼한 말린 꼬리 형성
    cx0,cy0=17,24      # 꼬리 중심
    pts=[]
    for i in range(0,28):
        ang=math.radians(120 + i*10)     # 120°~390° 회전
        rad=10 - i*0.18                   # 안쪽으로 말림
        x=cx0+math.cos(ang)*rad
        y=cy0-math.sin(ang)*rad
        pts.append((x,y))
    # 외곽선 패스
    for (x,y) in pts: disc(d,int(x),int(y),6,OUT)
    for (x,y) in pts: disc(d,int(x),int(y),5,TAIL)
    # 밝은 결
    for (x,y) in pts: disc(d,int(x),int(y),2,TAILH)

    # ----- 뒷발 -----
    outlined_disc(d,27,37,4,BODYS)

    # ----- 몸통 -----
    d.ellipse((20,14,40,40), fill=OUT)
    d.ellipse((21,15,39,39), fill=BODY)
    # 배(밝은색)
    d.ellipse((25,21,37,38), fill=BELLY)

    # ----- 머리 -----
    d.ellipse((25,2,43,20), fill=OUT)
    d.ellipse((26,3,42,19), fill=BODY)
    # 귀
    outlined_disc(d,30,3,3,BODY)
    outlined_disc(d,39,3,3,BODY)
    d.ellipse((29,2,32,5), fill=BELLY)

    # ----- 앞발 + 작은 도토리 -----
    outlined_disc(d,34,33,3,BODYS)   # 앞발
    # 작은 도토리 (몸 앞, 작게)
    d.ellipse((36,31,41,36), fill=OUT)
    d.ellipse((37,33,40,36), fill=ACORN)   # 알
    d.rectangle((37,31,40,33), fill=ACAP)  # 모자
    d.point((38,30), fill=ACAP)

    # ----- 얼굴 -----
    # 눈
    d.ellipse((34,8,38,13), fill=(255,255,255))
    d.ellipse((35,9,37,12), fill=(28,20,14))
    d.point((36,10), fill=(255,255,255))
    # 코
    d.ellipse((40,11,43,14), fill=(50,32,22))
    # 볼 홍조
    disc(d,33,14,2,(232,160,150))

    return img.resize((W*scale,Hh*scale),Image.NEAREST)

# 숲 배경 (픽셀 톤)
def make_forest(W,H):
    bg=Image.new("RGB",(W,H),(206,236,214))
    d=ImageDraw.Draw(bg)
    # 하늘 그라데이션
    for y in range(0,int(H*0.62)):
        t=y/(H*0.62)
        c=(int(180+30*t),int(225+15*t),int(245-10*t))
        d.line((0,y,W,y),fill=c)
    # 먼 나무 실루엣
    import random
    random.seed(7)
    for x in range(0,W,46):
        h=random.randint(70,120); tw=34
        ty=int(H*0.62)-h
        d.rectangle((x+14,ty+h-24,x+22,ty+h),fill=(120,86,52))      # 기둥
        d.polygon([(x,ty+h-10),(x+tw,ty+h-10),(x+tw//2,ty)],fill=(96,160,92))   # 잎(삼각)
        d.polygon([(x+3,ty+h-26),(x+tw-3,ty+h-26),(x+tw//2,ty+14)],fill=(112,176,104))
    # 잔디 바닥
    gy=int(H*0.62)
    d.rectangle((0,gy,W,H),fill=(126,194,96))
    d.rectangle((0,gy,W,gy+6),fill=(150,210,110))
    # 바닥에 흩뿌린 작은 도토리들
    for (ax,ay) in [(80,gy+40),(180,gy+70),(540,gy+50),(620,gy+30)]:
        d.ellipse((ax,ay+3,ax+8,ay+11),fill=(170,112,58))
        d.rectangle((ax,ay,ax+8,ay+4),fill=(96,62,30))
    return bg

KRB="/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/NanumGothicBold.ttf"
def f(s): return ImageFont.truetype(KRB,s)

# 시안 보드
W,H=720,430
board=make_forest(W,H)
d=ImageDraw.Draw(board)
sq=make_squirrel(7)
board.paste(sq,(int(W/2-sq.width/2),int(H*0.62-sq.height+30)),sq)
# 제목 칩
d.rounded_rectangle((W/2-220,16,W/2+220,54),18,fill=(255,255,255))
d.text((W/2,35),"8비트 다람쥐 v2 — 말린 꼬리 · 작은 도토리 · 숲",font=f(17),fill=(40,50,60),anchor="mm")
board.save("/home/user/news/squirrel_8bit_v2.png")
# 스프라이트 단독(투명)도 저장
make_squirrel(10).save("/home/user/news/squirrel_sprite.png")
print("done", sq.size)
