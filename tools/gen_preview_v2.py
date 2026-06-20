# -*- coding: utf-8 -*-
"""mockup_v2.html 의 '포근·귀여운 토스풍' 디자인을 그대로 그린 미리보기 PNG."""
from PIL import Image, ImageDraw, ImageFont

KR  = "/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/NanumGothic.ttf"
KRB = "/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/NanumGothicBold.ttf"
KRXB= "/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/NanumGothicExtraBold.ttf"
EMO = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

def f(size, bold=0):
    return ImageFont.truetype(KRXB if bold==2 else KRB if bold==1 else KR, size)

_ec={}
def emoji(ch, size):
    key=(ch,size)
    if key in _ec: return _ec[key]
    big=Image.new("RGBA",(140,140),(0,0,0,0))
    ImageDraw.Draw(big).text((4,4),ch,font=ImageFont.truetype(EMO,109),embedded_color=True)
    bb=big.getbbox()
    im=big.crop(bb).resize((size,size),Image.LANCZOS) if bb else None
    _ec[key]=im; return im

def pe(c, ch, cx, cy, size):
    im=emoji(ch,size)
    if im: c.paste(im,(int(cx-size/2),int(cy-size/2)),im)

def tw(d, text, font):
    return d.textbbox((0,0),text,font=font)[2]

def etc(img, d, cx, cy, ch, text, font, fill, esize):
    """이모지+텍스트를 중앙(cx,cy) 기준으로 가로 배치."""
    gap=4
    w=esize+gap+tw(d,text,font)
    x=cx-w/2
    pe(img,ch,x+esize/2,cy,esize)
    d.text((x+esize+gap,cy),text,font=font,fill=fill,anchor="lm")

def etl(img, d, x, cy, ch, text, font, fill, esize):
    """이모지+텍스트를 왼쪽 x 기준으로 가로 배치."""
    gap=5
    pe(img,ch,x+esize/2,cy,esize)
    d.text((x+esize+gap,cy),text,font=font,fill=fill,anchor="lm")

# 색상 (CSS 변수와 동일)
TOSS="#3182f6"; TOSSD="#1b64da"; BG="#f4f6f8"; CARD="#ffffff"
TEXT="#191f28"; SUB="#8b95a1"; LINE="#eef1f4"; ACORN="#c47a2c"; ACBG="#fff5e9"
PEACH="#ffeede"; STREAK="#ff7a45"; CREAM="#fff8f0"

def rr(d,xy,r,fill=None,outline=None,width=1):
    d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)

def vgrad(w,h,top,bot):
    """세로 그라데이션 이미지."""
    base=Image.new("RGB",(1,h))
    t=tuple(int(top[i:i+2],16) for i in (1,3,5))
    b=tuple(int(bot[i:i+2],16) for i in (1,3,5))
    for y in range(h):
        k=y/(h-1)
        base.putpixel((0,y),tuple(int(t[i]+(b[i]-t[i])*k) for i in range(3)))
    return base.resize((w,h))

def shadow(canvas, xy, r, blur=18, alpha=40):
    from PIL import ImageFilter
    x0,y0,x1,y1=xy
    pad=blur*2
    sh=Image.new("RGBA",(int(x1-x0+pad*2),int(y1-y0+pad*2)),(0,0,0,0))
    sd=ImageDraw.Draw(sh)
    sd.rounded_rectangle([pad,pad+6,x1-x0+pad,y1-y0+pad+6],radius=r,fill=(17,24,39,alpha))
    sh=sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.paste(sh,(int(x0-pad),int(y0-pad)),sh)

def phone(title_screen):
    """폰 한 대 렌더 -> RGBA 이미지 반환."""
    W,H=384,724  # 바깥 프레임
    img=Image.new("RGBA",(W,H),(0,0,0,0))
    d=ImageDraw.Draw(img)
    # 프레임
    rr(d,[0,0,W,H],40,fill="#ffffff")
    rr(d,[11,11,W-11,H-11],30,fill=BG)
    iw=W-22; ix=11; iy=11; ih=H-22
    # 상단바
    pe(img,"🐿️",ix+28,iy+30,22)
    d.text((ix+46,iy+30),"다람쥐 뽀모도로",font=f(15,2),fill=TEXT,anchor="lm")
    # pills
    rr(d,[ix+iw-148,iy+16,ix+iw-84,iy+44],14,fill="#fff0ea")
    etc(img,d,ix+iw-116,iy+31,"🔥","3일",f(12,1),STREAK,14)
    rr(d,[ix+iw-78,iy+16,ix+iw-14,iy+44],14,fill=ACBG)
    etc(img,d,ix+iw-46,iy+31,"🌰","28",f(12,1),ACORN,14)
    # 무대
    st_y=iy+58; st_h=200
    sky=vgrad(iw, st_h, "#d6efff", "#fef6ec")
    mask=Image.new("L",(iw,st_h),0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,iw,st_h],radius=0,fill=255)
    img.paste(sky,(ix,st_y))
    # 바닥 (둥근 언덕)
    floor=vgrad(iw,70,"#a7dd86","#8ccb64")
    fmask=Image.new("L",(iw,70),0)
    ImageDraw.Draw(fmask).ellipse([-40,-40,iw+40,90],fill=255)
    img.paste(floor,(ix,st_y+st_h-58),fmask)
    # 소나무들
    for i in range(6):
        pe(img,"🌲",ix+30+i*((iw-60)//5),st_y+st_h-66,20)
    pe(img,"🌳",ix+52,st_y+st_h-78,78)      # 나무
    pe(img,"🐿️",ix+iw-86,st_y+st_h-74,66)  # 다람쥐
    pe(img,"🌰",ix+iw-110,st_y+st_h-50,16)

    panel_y=st_y+st_h+8
    if title_screen=="timer":
        d.text((ix+iw/2,panel_y+10),"집중할 시간을 정하고 시작해요.",font=f(12),fill=SUB,anchor="mm")
        d.text((ix+iw/2,panel_y+30),"집중하는 동안 다람쥐가 도토리를 모아요.",font=f(12),fill=SUB,anchor="mm")
        # 큰 시간
        d.text((ix+iw/2-10,panel_y+72),"25",font=f(46,2),fill=TEXT,anchor="mm")
        d.text((ix+iw/2+36,panel_y+80),"분",font=f(16,1),fill=SUB,anchor="mm")
        # 슬라이더
        sy=panel_y+118
        d.line([ix+24,sy,ix+iw-24,sy],fill=LINE,width=6)
        d.line([ix+24,sy,ix+iw/2,sy],fill=TOSS,width=6)
        d.ellipse([ix+iw/2-10,sy-10,ix+iw/2+10,sy+10],fill="#ffffff",outline=TOSS,width=3)
        d.text((ix+24,sy+14),"5분",font=f(11),fill=SUB)
        d.text((ix+iw-48,sy+14),"60분",font=f(11),fill=SUB)
        # streak bar
        etc(img,d,ix+iw/2,sy+44,"🔥","연속 3일 · 다음 보너스까지 4일",f(12),SUB,14)
        # 버튼
        by=sy+64
        rr(d,[ix+18,by,ix+iw-18,by+50],16,fill=TOSS)
        etc(img,d,ix+iw/2,by+25,"🌰","집중 시작",f(16,2),"#ffffff",18)
        rr(d,[ix+18,by+60,ix+iw-18,by+104],16,fill=PEACH)
        etc(img,d,ix+iw/2,by+82,"📺","광고 보고 도토리 +3 (오늘 5회 남음)",f(12,1),ACORN,15)
    else:  # shop
        etl(img,d,ix+18,panel_y+16,"🛍️","꾸미기 상점",f(18,2),TEXT,20)
        d.text((ix+18,panel_y+40),"도토리로 아이템을 사고, 눌러서 장착해요.",font=f(12),fill=SUB)
        rows=[("🌰","도토리 모자","10","buy"),("🍁","단풍잎 모자","","equip"),
              ("🧣","빨간 목도리","","on"),("⭐","별 반지","25","buy"),
              ("☀️","맑은 하늘","25","buy")]
        ry=panel_y+58
        for em,name,price,kind in rows:
            rr(d,[ix+16,ry,ix+iw-16,ry+50],16,fill=CARD)
            pe(img,em,ix+40,ry+25,24)
            d.text((ix+62,ry+11),name,font=f(14,1),fill=TEXT,anchor="lm")
            if kind=="buy": etl(img,d,ix+62,ry+33,"🌰",price,f(11,1),ACORN,13)
            else: d.text((ix+62,ry+33),"보유중",font=f(11,1),fill=SUB,anchor="lm")
            bx0=ix+iw-92; bx1=ix+iw-24
            col={"buy":ACBG,"equip":"#eaf2ff","on":TOSS}[kind]
            rr(d,[bx0,ry+11,bx1,ry+39],11,fill=col)
            tcol={"buy":ACORN,"equip":TOSS,"on":"#ffffff"}[kind]
            if kind=="buy": etc(img,d,(bx0+bx1)/2,ry+25,"🌰",price,f(11,1),tcol,13)
            else: d.text(((bx0+bx1)/2,ry+25),"장착중" if kind=="on" else "장착",font=f(11,1),fill=tcol,anchor="mm")
            ry+=58
    # 탭바
    tb=iy+ih-46
    d.line([ix,tb,ix+iw,tb],fill=LINE,width=1)
    tabs=[("⏱️","집중","timer"),("🛍️","상점","shop"),("📖","도감","f"),("🏆","랭킹","r")]
    for i,(em,lab,key) in enumerate(tabs):
        cx=ix+iw*(i+0.5)/4
        active=(key==title_screen)
        etc(img,d,cx,tb+22,em,lab,f(12,1 if active else 0),TOSS if active else SUB,15)
    return img

# 캔버스
CW,CH=900,860
canvas=Image.new("RGB",(CW,CH),BG)
d=ImageDraw.Draw(canvas)
etl(canvas,d,40,40,"🐿️","다람쥐 뽀모도로 — 새 디자인 미리보기 (포근·귀여운 토스풍)",f(22,2),TEXT,24)
d.text((40,64),"mockup_v2.html 의 실제 스타일을 그대로 그린 이미지예요. (둥근 카드 · 토스 블루 · 파스텔 풍경)",font=f(14),fill=SUB)

p1=phone("timer"); p2=phone("shop")
shadow(canvas,[60,100,60+384,100+724],40)
shadow(canvas,[470,100,470+384,100+724],40)
canvas.paste(p1,(60,100),p1)
canvas.paste(p2,(470,100),p2)
canvas.save("/home/user/news/preview_v2.png")
print("saved preview_v2.png")
