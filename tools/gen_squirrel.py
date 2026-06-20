# -*- coding: utf-8 -*-
# 8비트 픽셀 다람쥐 스프라이트 생성 (손으로 찍은 픽셀맵)
from PIL import Image

# 색 팔레트
P = {
    '.': None,                 # 투명
    'o': (60, 38, 22, 255),    # 진한 외곽선
    'B': (176, 110, 54, 255),  # 몸통 갈색
    'b': (146, 88, 40, 255),   # 몸통 그림자
    'L': (232, 196, 150, 255), # 배(밝은색)
    'T': (150, 92, 46, 255),   # 꼬리
    't': (124, 74, 36, 255),   # 꼬리 그림자
    'W': (255, 255, 255, 255), # 눈 흰자
    'E': (30, 22, 16, 255),    # 눈동자
    'N': (40, 28, 20, 255),    # 코
    'A': (158, 102, 50, 255),  # 도토리 알
    'C': (96, 62, 30, 255),    # 도토리 모자
    'p': (224, 150, 120, 255), # 볼 홍조
}

# 24x22 픽셀 다람쥐 (오른쪽을 보고 앉아 큰 꼬리를 세운 모습)
GRID = [
    "........................",
    "..............oo........",
    ".............oBBo..oo....",
    "....TTT......oBBBoooBo...",  # 귀 + 머리
    "...TttTT....oBBBBBBBBo...",
    "..TttttT...oBBBBBBBBBBo..",
    "..TttttT..oBBBWWoBBNBo...",  # 눈/코 줄
    "..TttttT..oBBBWEoBBBo....",
    "..TttttT..oBBBBBBBpBo....",
    "..TttttT..oBBBBBBBBo.....",
    "...TttT...oBBBBBBBBo.....",
    "...TttT..oBLLLLLBBBo.....",  # 배 시작
    "...TttT..oBLLLLLLBBo..AA.",
    "...TttT.oBLLLLLLLBBo.ACCA",  # 손에 도토리
    "...TttT.oBLLLLLLLBBooAAAA",
    "...TtT..oBLLLLLLLBBBo.AA.",
    "...ooo..oBBLLLLLBBBo.....",
    "........oBBBBBBBBBBo.....",
    ".........oBBoooBBo.......",  # 발
    ".........oBBo.oBBo.......",
    "........oooo..oooo.......",
    "........................",
]

def render(grid, scale, outfile):
    h=len(grid); w=max(len(r) for r in grid)
    img=Image.new("RGBA",(w,h),(0,0,0,0))
    px=img.load()
    for y,row in enumerate(grid):
        for x,ch in enumerate(row):
            c=P.get(ch)
            if c: px[x,y]=c
    big=img.resize((w*scale,h*scale),Image.NEAREST)
    big.save(outfile)
    return big

render(GRID, 14, "/tmp/squirrel_8bit.png")

# 미리보기 보드: 배경 위에 다람쥐 + 도토리 + 라벨
from PIL import ImageDraw, ImageFont
KRB="/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/NanumGothicBold.ttf"
def f(s): return ImageFont.truetype(KRB,s)

sq=render(GRID,12,"/tmp/sq_tmp.png")
board=Image.new("RGB",(720,420),(233,247,255))
d=ImageDraw.Draw(board)
# 잔디 바닥
d.rectangle((0,330,720,420),fill=(124,192,90))
# 그림자
d.ellipse((250,338,470,360),fill=(108,170,80))
board.paste(sq,(int(360-sq.width/2),int(330-sq.height+18)),sq)
d.text((360,28),"8비트 픽셀 다람쥐 — 미리보기",font=f(26),fill=(25,31,40),anchor="mm")
d.text((360,62),"이모지 → 픽셀 일러스트로 변경한 시안이에요",font=f(15),fill=(90,100,110),anchor="mm")
board.save("/home/user/news/squirrel_8bit_preview.png")
print("done", sq.size)
