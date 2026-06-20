# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont

KR   = "/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/NanumGothic.ttf"
KRB  = "/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/NanumGothicBold.ttf"
KRXB = "/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/NanumGothicExtraBold.ttf"
EMO  = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

def f(size, bold=0):
    return ImageFont.truetype(KRXB if bold==2 else KRB if bold==1 else KR, size)

_emoji_cache={}
def emoji_img(ch, size):
    key=(ch,size)
    if key in _emoji_cache: return _emoji_cache[key]
    big=Image.new("RGBA",(140,140),(0,0,0,0))
    ImageDraw.Draw(big).text((4,4),ch,font=ImageFont.truetype(EMO,109),embedded_color=True)
    bb=big.getbbox()
    if not bb:
        _emoji_cache[key]=None; return None
    im=big.crop(bb).resize((size,size),Image.LANCZOS)
    _emoji_cache[key]=im; return im

def paste_emoji(canvas, ch, cx, cy, size, anchor="mm"):
    im=emoji_img(ch,size)
    if im is None: return
    x=cx-size//2 if "m" in anchor else cx
    y=cy-size//2 if "m" in anchor[1:] else cy
    if anchor=="lm": x=cx; y=cy-size//2
    canvas.paste(im,(int(x),int(y)),im)

def vgrad(w,h,top,bot):
    base=Image.new("RGB",(w,h),top)
    tr,tg,tb=top; br,bg,bb=bot
    px=base.load()
    for y in range(h):
        t=y/max(h-1,1)
        c=(int(tr+(br-tr)*t),int(tg+(bg-tg)*t),int(tb+(bb-tb)*t))
        for x in range(w): px[x,y]=c
    return base

def rrect(d,xy,r,fill=None,outline=None,width=1):
    d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)

W,H=400,760
BLUE=(49,130,246); BLUED=(27,100,218); SUB=(139,149,161); TEXT=(25,31,40)
LINE=(229,232,235); BG=(242,244,246); ACORN=(181,101,29)

def new_phone():
    img=Image.new("RGB",(W,H),BG)
    return img, ImageDraw.Draw(img)

def topbar(d,img,acorns):
    paste_emoji(img,"🐿️",30,31,22)
    d.text((46,22),"다람쥐 뽀모도로",font=f(17,2),fill=TEXT)
    # acorn pill
    label=f"{acorns}"
    pill_w=70
    rrect(d,(W-18-pill_w,16,W-18,46),15,fill=(255,247,236))
    paste_emoji(img,"🌰",W-18-pill_w+18,31,18)
    d.text((W-18-pill_w+32,22),label,font=f(15,2),fill=ACORN)

def stage(d,img,working=False,acorns_on_tree=0,hat="🌰"):
    sky=vgrad(W,150,(191,231,255),(233,247,255))
    img.paste(sky,(0,60))
    floor=vgrad(W,46,(155,209,122),(124,192,90))
    img.paste(floor,(0,164))
    # tree
    paste_emoji(img,"🌳",60,150,96)
    if acorns_on_tree:
        for i in range(min(acorns_on_tree,5)):
            paste_emoji(img,"🌰",36+i*20,198,14)
    # squirrel + hat
    paste_emoji(img,"🐿️",300,150,72)
    if hat: paste_emoji(img,"🌰" if hat=="🌰" else hat,300,108,26)
    # scarf
    paste_emoji(img,"🧣",300,178,22)
    if working:
        for i,(x,y) in enumerate([(150,120),(190,140),(230,115)]):
            paste_emoji(img,"🌰",x,y,18)

def tabbar(d,img,active=0):
    y=H-54
    d.rectangle((0,y,W,H),fill=(255,255,255))
    d.line((0,y,W,y),fill=LINE,width=1)
    tabs=[("⏱️","집중"),("🛍️","상점"),("📖","도감")]
    tw=W/3
    for i,(em,name) in enumerate(tabs):
        cx=int(tw*i+tw/2)
        col=BLUE if i==active else SUB
        paste_emoji(img,em,cx-28,y+26,18)
        d.text((cx+2,y+18),name,font=f(13,1),fill=col,anchor="lm")

def hint(d,lines,y):
    for i,ln in enumerate(lines):
        d.text((W/2,y+i*18),ln,font=f(12),fill=SUB,anchor="mm")

def btn(d,xy,fill,text,tcol,fnt):
    rrect(d,xy,14,fill=fill)
    cx=(xy[0]+xy[2])//2; cy=(xy[1]+xy[3])//2
    d.text((cx,cy),text,font=fnt,fill=tcol,anchor="mm")

# ---------- Screen A: 타이머 설정 ----------
def screen_setup():
    img,d=new_phone(); topbar(d,img,12); stage(d,img)
    hint(d,["집중할 시간을 정하고 시작해요.","집중하는 동안 다람쥐가 도토리를 모아요."],235)
    d.text((W/2,300),"25",font=f(52,2),fill=TEXT,anchor="mm")
    d.text((W/2+58,312),"분",font=f(18),fill=SUB,anchor="lm")
    # slider
    sy=355
    d.line((30,sy,W-30,sy),fill=LINE,width=6)
    d.line((30,sy,int(30+(W-60)*(20/55)),sy),fill=BLUE,width=6)
    d.ellipse((int(30+(W-60)*(20/55))-10,sy-10,int(30+(W-60)*(20/55))+10,sy+10),fill=BLUE)
    d.text((30,sy+18),"5분",font=f(11),fill=SUB)
    d.text((W-30,sy+18),"60분",font=f(11),fill=SUB,anchor="ra")
    btn(d,(24,400,W-24,448),BLUE,"집중 시작",( 255,255,255),f(17,2))
    paste_emoji(img,"🌰",W-90,424,20)
    tabbar(d,img,0)
    return img

# ---------- Screen B: 집중 진행 ----------
def screen_focus():
    img,d=new_phone(); topbar(d,img,12); stage(d,img,working=True,acorns_on_tree=3)
    hint(d,["집중 중이에요.","화면을 벗어나면 포기로 처리돼요!"],232)
    d.text((W/2,295),"18:42",font=f(46,2),fill=BLUE,anchor="mm")
    # progress
    py=340
    rrect(d,(30,py,W-30,py+9),5,fill=LINE)
    rrect(d,(30,py,30+int((W-60)*0.25),py+9),5,fill=BLUE)
    d.text((W/2,375),"이번 집중 도토리: 1 🌰",font=f(13),fill=SUB,anchor="mm")
    paste_emoji(img,"🌰",W/2+58,375,16)
    btn(d,(24,400,W-24,442),BG,"포기하기 (절반만 획득)",SUB,f(14,1))
    tabbar(d,img,0)
    return img

# ---------- Screen C: 상점 ----------
def screen_shop():
    img,d=new_phone(); topbar(d,img,40)
    paste_emoji(img,"🛍️",28,80,22); d.text((46,70),"꾸미기 상점",font=f(19,2),fill=TEXT)
    d.text((18,102),"도토리로 아이템을 사고, 눌러서 장착/해제해요.",font=f(12),fill=SUB)
    # (이모지, 이름, 보유여부, 가격숫자, 버튼텍스트, 버튼색)
    rows=[("h","모자",None),
          ("🌰","도토리 모자",True,None,"장착중",BLUE),
          ("🍁","단풍잎 모자",False,"15","구매",None),
          ("h","목도리",None),("🧣","빨간 목도리",False,"12","구매",None),
          ("h","반지",None),("💍","도토리 반지",False,"15","구매",None)]
    y=130
    for r in rows:
        if r[0]=="h":
            d.text((18,y),r[1],font=f(13,1),fill=SUB); y+=24; continue
        em,name,owned,price,bt,bc=r
        rrect(d,(16,y,W-16,y+52),14,fill=(255,255,255))
        paste_emoji(img,em,42,y+26,26)
        d.text((66,y+12),name,font=f(14,2),fill=TEXT)
        if owned:
            d.text((66,y+31),"보유중",font=f(12,1),fill=SUB)
        else:
            paste_emoji(img,"🌰",66,y+37,14)
            d.text((84,y+31),price,font=f(12,1),fill=ACORN)
        bw=64
        fillc=BLUE if bc==BLUE else (255,247,236) if bt=="구매" else (234,242,255)
        tcol=(255,255,255) if bc==BLUE else ACORN if bt=="구매" else BLUE
        rrect(d,(W-16-bw,y+12,W-22,y+40),10,fill=fillc)
        d.text((W-16-bw/2-3,y+26),bt,font=f(12,1),fill=tcol,anchor="mm")
        y+=60
    tabbar(d,img,1)
    return img

# ---------- Screen D: 친구 도감 ----------
def screen_friends():
    img,d=new_phone(); topbar(d,img,120)
    paste_emoji(img,"📖",28,80,22); d.text((46,70),"다람쥐 친구 도감",font=f(19,2),fill=TEXT)
    d.text((18,102),"도토리를 모아 친구를 데려오세요. (수집 전용!)",font=f(12),fill=SUB)
    cards=[("기본 다람쥐","done",False,None),
           ("아기 다람쥐","50",False,"데려오기"),
           ("???","100",True,"데려오기"),
           ("???","200",True,"데려오기")]
    gx,gy=16,130; cw=(W-16-16-10)//2; ch=150
    for i,(name,status,locked,bt) in enumerate(cards):
        cxp=gx+(i%2)*(cw+10); cyp=gy+(i//2)*(ch+10)
        rrect(d,(cxp,cyp,cxp+cw,cyp+ch),16,fill=(255,255,255))
        im=emoji_img("🐿️",54)
        if im:
            if locked:
                im=im.convert("LA").convert("RGBA")
                im.putalpha(im.getchannel("A").point(lambda a:int(a*0.4)))
            img.paste(im,(cxp+cw//2-27,cyp+18),im)
        d.text((cxp+cw//2,cyp+86),name,font=f(13,2),fill=TEXT,anchor="mm")
        if status=="done":
            d.text((cxp+cw//2,cyp+108),"수집 완료",font=f(12,1),fill=(25,195,125),anchor="mm")
            paste_emoji(img,"✅",cxp+cw//2+34,cyp+108,14)
        else:
            paste_emoji(img,"🌰",cxp+cw//2-20,cyp+108,14)
            d.text((cxp+cw//2-2,cyp+108),status,font=f(12,1),fill=ACORN,anchor="lm")
        if bt:
            bw=80
            rrect(d,(cxp+cw//2-bw//2,cyp+120,cxp+cw//2+bw//2,cyp+142),10,fill=(255,247,236))
            d.text((cxp+cw//2,cyp+131),bt,font=f(11,1),fill=ACORN,anchor="mm")
    tabbar(d,img,2)
    return img

# ---------- 합치기 ----------
screens=[("① 메인 · 집중 시작",screen_setup()),
         ("② 집중 중 (도토리 모으기)",screen_focus()),
         ("③ 꾸미기 상점",screen_shop()),
         ("④ 다람쥐 친구 도감",screen_friends())]
gap=24; lab_h=44; pad=30
total_w=pad*2+W*4+gap*3
total_h=pad+lab_h+H+pad
canvas=Image.new("RGB",(total_w,total_h),(255,255,255))
cd=ImageDraw.Draw(canvas)
paste_emoji(canvas,"🐿️",pad+12,30,26)
cd.text((pad+32,18),"다람쥐 뽀모도로 — 화면 미리보기",font=f(22,2),fill=TEXT)
for i,(title,sc) in enumerate(screens):
    x=pad+i*(W+gap); y=pad+lab_h
    # phone frame
    cd.rounded_rectangle((x-6,y-6,x+W+6,y+H+6),radius=30,outline=(17,17,17),width=8)
    canvas.paste(sc,(x,y))
    cd.text((x+W/2,y-22),title,font=f(15,1),fill=TEXT,anchor="mm")
canvas.save("/home/user/news/preview_screens.png")
print("saved preview_screens.png", canvas.size)
PY = None
