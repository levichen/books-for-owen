# -*- coding: utf-8 -*-
"""Book 17: Eyes, Not Hands! — 物權故事（便利商店場景）。"""
import math
from parts import *
from book_common import svg, svgtext, TXT, W, H

# soft page palettes
BG = {
    "cover": "#FFF8E8", "p1": "#E8F4FF", "p2": "#FFF3D6", "p3": "#F0E8FF",
    "p4": "#FFE8E8", "p5": "#E8D4FF", "p6": "#FFE8F8", "p7": "#E8F8D8",
    "p8": "#FFF0C9", "p9": "#E8F0FF", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

# ================== HELPER FUNCTIONS ==================

def shelf_unit(cx, cy, scale):
    """超商貨架單位：直立框架 + 3 層橫板 + 商品真的擺在架上（糖果罐、玩具車、餅乾盒、貼紙包）。"""
    s = []
    # frame outline
    s.append(f'<rect x="-80" y="-120" width="160" height="280" rx="8" fill="none" stroke="#A89968" stroke-width="5"/>')

    # 3 shelves (橫板)
    shelf_positions = [-40, 40, 120]
    for shelf_y in shelf_positions:
        s.append(f'<rect x="-70" y="{shelf_y-4}" width="140" height="8" rx="4" fill="#C4A272" stroke="#A89968" stroke-width="2"/>')

    # items on shelves - properly positioned on shelf surface
    # shelf 1 (top: y=-40): candy jar + toy car + sticker pack
    # candy jar: circle + colored cap
    s.append(f'<circle cx="-45" cy="-60" r="16" fill="#FFB3BA"/>')
    s.append(f'<rect x="-52" y="-72" width="14" height="12" rx="3" fill="#F77B8E"/>')
    s.append(f'<rect x="-45" y="-72" width="14" height="12" rx="3" fill="#FF69B4"/>')
    # toy car: body + two wheels
    s.append(f'<rect x="-10" y="-62" width="28" height="18" rx="4" fill="#FFD93D"/>')
    s.append(f'<circle cx="-15" cy="-45" r="6" fill="#5D3A1A"/>')
    s.append(f'<circle cx="5" cy="-45" r="6" fill="#5D3A1A"/>')
    # sticker pack: small square
    s.append(f'<rect x="35" y="-68" width="24" height="28" rx="3" fill="#A0C4FF" stroke="#7BA8FF" stroke-width="2"/>')

    # shelf 2 (middle: y=40): cookies + candy + toy
    # cookies box: striped rectangle
    s.append(f'<rect x="-48" y="20" width="26" height="20" rx="2" fill="#D2B48C" stroke="#8B7355" stroke-width="2"/>')
    s.append(f'<line x1="-42" y1="20" x2="-42" y2="40" stroke="#8B7355" stroke-width="1.5"/>')
    s.append(f'<line x1="-36" y1="20" x2="-36" y2="40" stroke="#8B7355" stroke-width="1.5"/>')
    # candy jar: round
    s.append(f'<circle cx="0" cy="30" r="14" fill="#F4A460"/>')
    s.append(f'<rect x="-10" y="12" width="20" height="8" rx="3" fill="#FFE8B6"/>')
    # toy: small blue box
    s.append(f'<rect x="28" y="18" width="26" height="24" rx="3" fill="#87CEEB" stroke="#4682B4" stroke-width="1.5"/>')
    s.append(f'<rect x="35" y="26" width="12" height="10" fill="#4682B4" opacity="0.6"/>')

    # shelf 3 (bottom: y=120): sticker pack + candy + toy
    # sticker pack
    s.append(f'<rect x="-48" y="100" width="24" height="30" rx="3" fill="#FFB6D9" stroke="#FF69B4" stroke-width="2"/>')
    # candy jar
    s.append(f'<circle cx="0" cy="115" r="13" fill="#F0A080"/>')
    s.append(f'<rect x="-8" y="98" width="16" height="8" rx="2" fill="#D9735C"/>')
    # toy car
    s.append(f'<rect x="30" y="102" width="24" height="16" rx="3" fill="#FF6B6B"/>')
    s.append(f'<circle cx="36" cy="122" r="5" fill="#4A4A4A"/>')
    s.append(f'<circle cx="48" cy="122" r="5" fill="#4A4A4A"/>')

    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(s)}</g>'


def phone_icon(cx, cy, scale):
    """通用手機 icon：深灰邊框 + 淺藍螢幕 + 圓 home 鍵。"""
    p = []
    p.append(f'<rect x="-18" y="-32" width="36" height="64" rx="6" fill="#4A4A4A" stroke="#2A2A2A" stroke-width="2"/>')
    p.append(f'<rect x="-14" y="-26" width="28" height="46" rx="4" fill="#ADD8E6"/>')
    p.append(f'<circle cx="0" cy="36" r="4" fill="#2A2A2A"/>')
    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(p)}</g>'


def glasses_icon(cx, cy, scale):
    """圓框眼鏡 icon：兩圓 + 鼻樑。"""
    g = []
    g.append(f'<circle cx="-12" cy="0" r="10" fill="#FFFFFF" stroke="#161616" stroke-width="2.5"/>')
    g.append(f'<circle cx="12" cy="0" r="10" fill="#FFFFFF" stroke="#161616" stroke-width="2.5"/>')
    g.append(f'<path d="M -2 -1 L 2 -1" stroke="#161616" stroke-width="2.5" stroke-linecap="round"/>')
    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(g)}</g>'


def book_icon(cx, cy, scale):
    """小書 icon：封面 + 書脊線。"""
    b = []
    b.append(f'<path d="M -12 -16 L -12 16 L 12 14 L 12 -16 Z" fill="#E8695C" stroke="#A84A41" stroke-width="1.5"/>')
    b.append(f'<path d="M -12 16 L 12 14" stroke="#A84A41" stroke-width="1.5"/>')
    b.append(f'<line x1="-8" y1="-10" x2="8" y2="-8" stroke="#A84A41" stroke-width="1" opacity="0.6"/>')
    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(b)}</g>'


def big_eye(cx, cy, scale, glow=False):
    """大眼睛圖示（本書核心符號）：杏仁形眼眶 + 圓瞳孔 + 高光點 + 睫毛 2-3 根。"""
    e = []
    if glow:
        e.append(f'<circle cx="0" cy="0" r="72" fill="{STAR_Y}" fill-opacity="0.18"/>')
        e.append(f'<circle cx="0" cy="0" r="48" fill="{STAR_Y}" fill-opacity="0.18"/>')
    # 杏仁形眼眶
    e.append(f'<ellipse cx="0" cy="0" rx="48" ry="42" fill="none" stroke="#2A2320" stroke-width="3.5"/>')
    # 圓瞳孔
    e.append(f'<circle cx="0" cy="4" r="28" fill="#1A1A1A"/>')
    # 高光點
    e.append(f'<circle cx="-8" cy="-12" r="10" fill="#FFFFFF" opacity="0.8"/>')
    e.append(f'<circle cx="-4" cy="-8" r="4" fill="#FFFFFF" opacity="0.6"/>')
    # 睫毛
    for i, (dx, dy) in enumerate([(-20, -48), (0, -52), (20, -48)]):
        e.append(f'<line x1="{dx}" y1="{dy}" x2="{dx}" y2="{dy-10}" stroke="#2A2320" stroke-width="2.5" stroke-linecap="round"/>')

    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(e)}</g>'


# ================== SCENES ================

def scene_cover():
    """封面：Owen 白 T 站在貨架前雙手背後用眼睛看 + big_eye 符號在上方 + 暖色星星。"""
    e = []
    # background
    e.append(f'<rect x="0" y="0" width="1188" height="620" fill="{BG["cover"]}"/>')
    # stars
    for (x, y, r) in [(120, 100, 16), (1050, 120, 18), (180, 500, 14), (1080, 480, 16), (400, 80, 12), (800, 520, 14)]:
        e.append(star(x, y, r, fill=STAR_Y))
    # ground
    e.append(f'<ellipse cx="594" cy="620" rx="560" ry="100" fill="#FFDD7E"/>')
    # shelves on both sides
    e.append(shelf_unit(250, 360, 0.75))
    e.append(shelf_unit(940, 360, 0.75))
    # Owen standing in center, hands behind back
    e.append(boy(pose="stand", expr="big", cx=594, cy=320, scale=1.35))
    # big eye above
    e.append(big_eye(594, 140, 1.15, glow=True))
    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """p1：Owen 白 T 開心走路，眼睛亮亮，四周飄著小星星與驚嘆號。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p1"]}"/>')
    # ground
    e.append(f'<ellipse cx="594" cy="560" rx="560" ry="80" fill="#D4E8FF"/>')
    # clouds
    e.append(cloud(150, 80, 0.9))
    e.append(cloud(900, 100, 1.1))
    # stars and sparkles
    e.append(star(200, 120, 18))
    e.append(star(950, 130, 20))
    e.append(sparkle(380, 100, 12))
    e.append(sparkle(820, 110, 14))
    # exclamation marks
    e.append(svgtext(480, 140, "!", size=60, fill="#FFC93C", weight="bold"))
    e.append(svgtext(780, 150, "!", size=56, fill="#FFC93C", weight="bold"))
    # Owen walking with bright eyes
    e.append(boy(pose="walk", expr="big", cx=450, cy=260, scale=1.15))
    return svg(W, H, "".join(e), bg=None)


def scene_p2():
    """p2：便利商店內整排貨架（糖果罐、玩具、餅乾），April 牽購物籃，Owen 眼睛發亮。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p2"]}"/>')
    # floor
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#E8D2AC"/>')
    # ceiling lights
    e.append(f'<ellipse cx="250" cy="30" rx="80" ry="12" fill="#F4E4A0" opacity="0.8"/>')
    e.append(f'<ellipse cx="594" cy="20" rx="100" ry="14" fill="#F4E4A0" opacity="0.8"/>')
    e.append(f'<ellipse cx="950" cy="30" rx="80" ry="12" fill="#F4E4A0" opacity="0.8"/>')
    # shelves
    e.append(shelf_unit(220, 280, 0.9))
    e.append(shelf_unit(594, 280, 0.9))
    e.append(shelf_unit(968, 280, 0.9))
    # April with shopping basket
    e.append(april(cx=150, cy=320, scale=1.1, pose="stand"))
    # basket
    e.append(f'<ellipse cx="140" cy="380" rx="28" ry="24" fill="#F0E8A8" stroke="#D4C456" stroke-width="3"/>')
    e.append(f'<path d="M 112 380 L 100 350 M 140 380 L 140 340 M 168 380 L 180 350" stroke="#D4C456" stroke-width="2.5" stroke-linecap="round"/>')
    # Owen with bright eyes and stars
    e.append(boy(pose="stand", expr="star", cx=780, cy=280, scale=1.15))
    e.append(sparkle(850, 180, 14))
    e.append(sparkle(720, 160, 12))
    return svg(W, H, "".join(e), bg=None)


def scene_p3():
    """p3：Owen 特寫（star 表情），視線虛線分別飄向糖果/玩具車/貼紙。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p3"]}"/>')
    # items to look at (top right)
    e.append(f'<g transform="translate(850,120)"><circle cx="0" cy="0" r="18" fill="#FFB3BA"/><rect x="-16" y="-16" width="32" height="10" rx="5" fill="#F77B8E"/></g>')  # candy jar
    e.append(f'<g transform="translate(950,160)"><rect x="-16" y="-12" width="32" height="24" rx="6" fill="#FFD93D"/><circle cx="-10" cy="-8" r="4" fill="#5D3A1A"/><circle cx="10" cy="-8" r="4" fill="#5D3A1A"/></g>')  # toy car
    e.append(f'<g transform="translate(1050,100)"><rect x="-14" y="-16" width="28" height="32" rx="4" fill="#A0C4FF" stroke="#7BA8FF" stroke-width="2"/></g>')  # sticker pack

    # sight lines (dashed) from Owen's eyes
    e.append(f'<path d="M 350 200 Q 550 180 850 120" stroke="#4A78A8" stroke-width="2" stroke-dasharray="5 8" fill="none" stroke-linecap="round"/>')
    e.append(f'<path d="M 350 200 Q 600 220 950 160" stroke="#4A78A8" stroke-width="2" stroke-dasharray="5 8" fill="none" stroke-linecap="round"/>')
    e.append(f'<path d="M 350 200 Q 650 140 1050 100" stroke="#4A78A8" stroke-width="2" stroke-dasharray="5 8" fill="none" stroke-linecap="round"/>')

    # Owen bust close-up
    e.append(boy_bust(expr="star", cx=280, cy=320, scale=1.4))

    return svg(W, H, "".join(e), bg=None)


def scene_p4():
    """p4：衝動頁 - Owen swing 伸手抓玩具，speed/shake lines，貨架在右，April oh 在左。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p4"]}"/>')
    # floor
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#E8D2AC"/>')

    # shelf on right side
    e.append(shelf_unit(800, 280, 0.95))

    # speed lines (at torso height, Owen center~380, scale 1.15)
    for i in range(3):
        y_pos = 270 + (i - 1) * 28
        e.append(f'<line x1="450" y1="{y_pos}" x2="580" y2="{y_pos}" stroke="#E8A20C" stroke-width="4" stroke-linecap="round"/>')

    # Owen (swing pose) - hands reach to shelf 2nd layer
    e.append(boy(pose="swing", expr="big", cx=380, cy=290, scale=1.15))

    # toy being grabbed - in front of Owen's hand (~hand x ≈ 380+102, hand y ≈ 290+58)
    # position at (600, 280) with slight rotation + shake lines
    e.append(f'<g transform="translate(600,275) rotate(-12)">')
    e.append(f'<rect x="-14" y="-10" width="28" height="20" rx="3" fill="#87CEEB"/>')
    e.append(f'<circle cx="-8" cy="8" r="5" fill="#4682B4"/>')
    e.append(f'<circle cx="8" cy="8" r="5" fill="#4682B4"/>')
    e.append('</g>')

    # shake lines near toy
    e.append(f'<path d="M 590 260 Q 595 255 600 260" stroke="#E8A20C" stroke-width="2.5" stroke-linecap="round" fill="none"/>')
    e.append(f'<path d="M 610 260 Q 615 255 620 260" stroke="#E8A20C" stroke-width="2.5" stroke-linecap="round" fill="none"/>')

    # April on left (stand pose, neutral face modified for surprise)
    e.append(april(cx=140, cy=310, scale=1.0, pose="stand"))

    # big question mark above Owen
    e.append(svgtext(440, 80, "?", size=88, fill="#FFB3BA", weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p5():
    """p5：紫星空 + boy_bust(arms='desk', expr='press') + big_eye(glow=True) 大大地發光。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p5"]}"/>')

    # stars scattered
    for (x, y, r) in [(120, 100, 14), (1050, 120, 16), (200, 450, 12), (1000, 430, 14), (350, 80, 10), (850, 70, 12)]:
        e.append(star(x, y, r, fill=STAR_Y))

    # sparkles
    e.append(sparkle(280, 100, 12))
    e.append(sparkle(950, 110, 14))

    # Owen bust (press expression, desk arms = resting hands on chest)
    e.append(boy_bust(expr="press", cx=350, cy=300, scale=1.3, arms="desk"))

    # big glowing eye in front
    e.append(big_eye(800, 280, 1.4, glow=True))

    return svg(W, H, "".join(e), bg=None)


def scene_p6():
    """p6：三步腳本三格 - ①思考泡泡「Is it mine?」＋搖頭 ②大眼睛發光＋商品 ③語音泡泡「Can I see it?」。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p6"]}"/>')

    # floor
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#D4E8F8"/>')

    # Three rounded boxes for three steps
    for i, (box_x, box_title) in enumerate([(210, "Is it mine?"), (594, ""), (978, "Can I see it?")]):
        # box frame
        e.append(f'<rect x="{box_x-140}" y="80" width="280" height="180" rx="16" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="4"/>')

        if i == 0:
            # Step 1: thought bubble with "Is it mine?" + red X
            e.append(f'<path d="M {box_x-30} 140 Q {box_x-80} 120 {box_x-50} 80" fill="none" stroke="#B9CFE8" stroke-width="3" stroke-linecap="round"/>')
            e.append(svgtext(box_x, 140, "Is it mine?", size=28, fill="#4A78A8", weight="bold"))
            # red X
            e.append(f'<line x1="{box_x-30}" y1="200" x2="{box_x+20}" y2="240" stroke="#E8574C" stroke-width="6" stroke-linecap="round"/>')
            e.append(f'<line x1="{box_x+20}" y1="200" x2="{box_x-30}" y2="240" stroke="#E8574C" stroke-width="6" stroke-linecap="round"/>')
        elif i == 1:
            # Step 2: big eye + products
            e.append(big_eye(box_x, 160, 0.7, glow=True))
            # mini products
            e.append(f'<circle cx="{box_x-50}" cy="240" r="12" fill="#FFB3BA"/>')
            e.append(f'<rect x="{box_x-20}" y="230" width="24" height="20" rx="4" fill="#FFD93D"/>')
            e.append(f'<rect x="{box_x+30}" y="225" width="20" height="28" rx="3" fill="#A0C4FF"/>')
        else:
            # Step 3: speech bubble "Can I see it?"
            e.append(f'<path d="M {box_x+50} 220 L {box_x+80} 250 L {box_x+40} 250 Z" fill="#B9CFE8" stroke="#7BA8D8" stroke-width="2"/>')
            e.append(svgtext(box_x, 150, "Can I see it?", size=26, fill="#4A78A8", weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p7():
    """p7：三格物主（用 icon + 標籤呈現，不畫人物） - ①phone + Daddy ②glasses + Anne ③book + Owen（各格小愛心）。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p7"]}"/>')

    # floor
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#E8F0DC"/>')

    # Three boxes
    for i, (box_x, icon_fn, label) in enumerate([(210, phone_icon, "Daddy"), (594, glasses_icon, "Anne"), (978, book_icon, "Owen")]):
        # box frame
        e.append(f'<rect x="{box_x-120}" y="100" width="240" height="240" rx="14" fill="#FFFFFF" stroke="#C4D8B4" stroke-width="4"/>')

        # icon in center
        e.append(icon_fn(box_x, 180, 1.2))

        # label
        e.append(svgtext(box_x, 280, label, size=32, fill="#4A6B3C", weight="bold"))

        # small heart in corner
        e.append(f'<path d="M {box_x+80} 110 c 0 -6 -6 -12 -12 -12 c -6 0 -12 6 -12 12 c 0 12 12 20 12 20 s 12 -8 12 -20 Z" fill="#FF6B6B"/>')

    return svg(W, H, "".join(e), bg=None)


def scene_p8():
    """p8：超商結帳區（櫃台矩形）+ Owen 雙手背後身體微前傾用眼睛欣賞玩具 + April 微笑比讚 + 語音泡泡「Good hands, Owen!」。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p8"]}"/>')

    # floor
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#FFF0C9"/>')

    # checkout counter
    e.append(f'<rect x="600" y="320" width="420" height="140" rx="12" fill="#D2B48C" stroke="#C4A272" stroke-width="3"/>')
    e.append(f'<rect x="620" y="300" width="60" height="40" rx="6" fill="#B0874D"/>')  # register

    # toy on shelf to look at
    e.append(f'<g transform="translate(750,280)"><circle cx="0" cy="0" r="16" fill="#87CEEB"/><rect x="-12" y="-8" width="24" height="16" rx="3" fill="#4682B4"/></g>')

    # Owen standing with hands behind back, leaning forward slightly
    e.append(boy(pose="stand", expr="big", cx=320, cy=320, scale=1.15))

    # April next to Owen giving thumbs up
    e.append(april(cx=150, cy=300, scale=1.0, pose="stand"))
    # modify to show thumbs up with speech
    e.append(f'<circle cx="80" cy="240" r="12" fill="#FFD34D"/>')  # thumb up circle

    # speech bubble "Good hands, Owen!"
    e.append(f'<path d="M 200 180 Q 200 140 260 140 L 380 140 Q 420 140 420 180 L 420 220 Q 420 240 400 240 L 320 240 L 300 270 L 320 240 L 280 240 Q 200 240 200 200 Z" fill="#FFFFFF" stroke="#D4C456" stroke-width="3"/>')
    e.append(svgtext(310, 190, "Good hands, Owen!", size=28, fill="#A86A3C", weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p9():
    """p9：轉移頁三小格 - ①phone_icon + big_eye ②glasses_icon + 語音泡泡 ③book_icon + big_eye；每格小綠勾。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p9"]}"/>')

    # floor
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#E8F0FF"/>')

    # Three small boxes
    for i, (box_x, icon_fn, has_speech) in enumerate([(210, phone_icon, False), (594, glasses_icon, True), (978, book_icon, False)]):
        # rounded box
        e.append(f'<rect x="{box_x-100}" y="120" width="200" height="200" rx="12" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')

        # icon
        e.append(icon_fn(box_x, 180, 1.0))

        # big eye or speech
        if has_speech:
            e.append(f'<path d="M {box_x-30} 260 Q {box_x-50} 280 {box_x-10} 290 Q {box_x+20} 280 {box_x} 260" fill="#FFFFFF" stroke="#5D9FE8" stroke-width="2"/>')
            e.append(svgtext(box_x, 275, "Can I see it?", size=18, fill="#4A78A8", weight="bold"))
        else:
            e.append(big_eye(box_x, 280, 0.6, glow=False))

        # green checkmark in corner
        e.append(f'<circle cx="{box_x+85}" cy="125" r="12" fill="#7BC47F"/>')
        e.append(f'<path d="M {box_x+80} 130 L {box_x+85} 135 L {box_x+92} 128" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>')

    return svg(W, H, "".join(e), bg=None)


def scene_p10():
    """p10：英雄頁 - boy(pose='hips', cape=True) + big_eye(glow=True) 徽章在胸口 + 雙手乖乖發光 + 滿天星。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p10"]}"/>')

    # ground
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="100" fill="#FFDD7E"/>')

    # stars scattered
    for (x, y, r) in [(140, 100, 18), (1040, 110, 20), (120, 380, 16), (1060, 390, 18), (310, 60, 12), (880, 70, 14), (450, 420, 10), (750, 430, 11)]:
        e.append(star(x, y, r))

    # sparkles on hands
    e.append(sparkle(420, 340, 14))
    e.append(sparkle(770, 340, 14))
    e.append(sparkle(500, 320, 10))
    e.append(sparkle(690, 310, 10))

    # Owen hero pose with cape
    e.append(boy(pose="hips", expr="proud", cx=594, cy=240, scale=1.3, cape=True))

    # big glowing eye badge on chest (diameter ~70px, centered at cy+105*scale)
    badge_cy = 240 + 105 * 1.3  # = 376.5
    e.append(big_eye(594, badge_cy, 0.73, glow=True))

    return svg(W, H, "".join(e), bg=None)


# ================== PAGE TEXTS ================

PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I see cool things everywhere!'),
    ("p2", scene_p2, 'We go to the <b>store</b>.<br/>So many shiny things!'),
    ("p3", scene_p3, 'Ooh, candy! Ooh, toys!<br/>I want to <b>touch</b> them all!'),
    ("p4", scene_p4, 'My fingers want to dance!<br/>My hands feel hot and jumpy.<br/>I grab a toy&mdash;it is not mine!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/><b>Eyes</b>, not hands!'),
    ("p6", scene_p6, 'Is it mine? No!<br/>Eyes, not hands.<br/>Or I ask, &ldquo;Can I see it?&rdquo;'),
    ("p7", scene_p7, 'Daddy\'s <b>phone</b> is Daddy\'s.<br/>Anne\'s glasses are Anne\'s.<br/>My things are mine, too!'),
    ("p8", scene_p8, 'I see a super toy.<br/>I look with my <b>eyes</b>.<br/>Mommy April smiles. &ldquo;Good hands, <b>Owen</b>!&rdquo;'),
    ("p9", scene_p9, 'Daddy\'s phone? Eyes, not hands!<br/>Anne\'s glasses? Ask first!<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Is it mine? Eyes, not hands!<br/>Or ask the owner.<br/><b>Eyes, not hands!</b> I practice every day!'),
]


# ================== PARENT TIPS ================

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("進店前先預告", "踏進便利商店前蹲下來說「今天用眼睛逛」——先啟動腳本再進場，比進場後糾正有效十倍。做到全程 eyes only 就在出店時給具體稱讚（可偶爾獎勵一樣小東西：「因為你今天用眼睛逛」）。"),
    ("家裡的手機規則同款", "想看爸媽手機＝先問「Can I see it?」——大人拿他東西時也示範先問（「爸爸可以看你的畫嗎？」），物權是雙向的，他的東西也被尊重，規則才可信。"),
    ("當他主動說出覺察時大力稱讚", "當他主動說「My fingers want to dance」或伸手前先問了「Whose is it?」= 覺察里程碑，大力稱讚；與 Ask first 是同一顆「先問」的肌肉，兩個口訣會互相加強。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]


# ================== BOOK DICT ================

BOOK = {
    "slug": "eyes-not-hands",
    "order": 17,
    "title_pre": "", "title_hi": "Eyes", "title_post": ", Not Hands!",
    "title_zh": "用眼睛看",
    "subtitle": "Owen's store story",
    "tagline_zh": "Owen 的物權故事",
    "chips": ["Social Story", "Manners", "13 pages"],
    "pdf_name": "Eyes_Not_Hands.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ["store", "phone", "touch"],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Is it mine? &rarr; Eyes, not hands &rarr; Or ask the owner</b>&nbsp;"
                 "（喊法：Eyes, not hands!）。當他哪天主動說出「My fingers want to dance」或在伸手前先問了「Whose is it?」，"
                 "就是最值得大力稱讚的里程碑。"),
    "cover": scene_cover,
}
