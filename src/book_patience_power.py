# -*- coding: utf-8 -*-
"""Book 14: Patience Power! — 快輸或一直錯的當下失去耐心（遊戲/珠心算）——安裝「深呼吸 → I can wait → 繼續輪流」的情緒調節腳本。"""
from parts import *
from book_common import svg, svgtext, TXT, W, H
import math

# soft page palettes
BG = {
    "cover": "#FFF9E6", "p1": "#F5EDD8", "p2": "#FFF3D6", "p3": "#FFE3C2",
    "p4": "#FFD9CF", "p5": "#6B5BA8", "p6": "#D7E9F8", "p7": "#F0E8DC",
    "p8": "#FFF0C9", "p9": "#FFE2EC", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

# ================ Helper Functions ================

def tile(cx, cy, scale, kind="mahjong", label="", color="#FFFFFF"):
    """小長方磚牌：圓角矩形、白面＋淺陰影側邊。
    kind: "mahjong"（圓點/條紋）| "lami"（彩色數字）
    label: 麻將簡單圖樣標籤或拉密數字
    """
    t = []
    w, h = 32 * scale, 48 * scale
    # 陰影側邊（右下）
    t.append(f'<path d="M {cx-w/2+2} {cy+h/2-2} L {cx+w/2-2} {cy+h/2-2} L {cx+w/2-2} {cy-h/2+2}" '
             f'fill="none" stroke="#D9D3C8" stroke-width="{max(1, 2*scale)}" stroke-linecap="round"/>')
    # 白色牌面
    t.append(f'<rect x="{cx-w/2}" y="{cy-h/2}" width="{w}" height="{h}" rx="{3*scale}" '
             f'fill="{color}" stroke="#C4B5A0" stroke-width="{max(1, 2*scale)}"/>')

    if kind == "mahjong":
        # 簡單圖樣：圓點或條紋
        if label == "dot":
            t.append(f'<circle cx="{cx}" cy="{cy-6*scale}" r="{3*scale}" fill="#E4574C"/>')
            t.append(f'<circle cx="{cx}" cy="{cy+6*scale}" r="{3*scale}" fill="#E4574C"/>')
        elif label == "stripe":
            t.append(f'<line x1="{cx-8*scale}" y1="{cy}" x2="{cx+8*scale}" y2="{cy}" '
                     f'stroke="#3E5C41" stroke-width="{2*scale}" stroke-linecap="round"/>')
    elif kind == "lami":
        # 拉密數字牌
        if label:
            fs = max(12, 20 * scale)
            t.append(f'<text x="{cx}" y="{cy+fs*0.35}" font-family="Huninn" font-size="{fs}" '
                     f'font-weight="bold" fill="#E8A20C" text-anchor="middle">{label}</text>')

    return "".join(t)


def volcano(cx, cy, scale, mood="bubble"):
    """胸口小火山：棕色梯形山身＋山口。
    mood: "bubble"（紅橙泡泡＋紅光暈）| "cloud"（藍色小雲蓋住）| "calm"（綠色山+藍雲，安靜）
    """
    v = []
    # 根據 mood 決定山身顏色
    mountain_fill = "#7A6A50" if mood in ("bubble", "cloud") else "#5A8A4A"

    # 梯形山身（底寬、頂尖）
    w_base = 50 * scale
    h = 50 * scale
    v.append(f'<path d="M {cx-w_base/2} {cy+h/2} L {cx+w_base/2} {cy+h/2} L {cx+10*scale} {cy-h/2} L {cx-10*scale} {cy-h/2} Z" '
             f'fill="{mountain_fill}" stroke="#4A3A2A" stroke-width="{max(1, 2*scale)}"/>')

    if mood == "bubble":
        # 紅光暈（多層半透明圓）
        v.append(f'<circle cx="{cx}" cy="{cy-25*scale}" r="{25*scale}" fill="#FF6B5B" fill-opacity="0.12"/>')
        v.append(f'<circle cx="{cx}" cy="{cy-25*scale}" r="{16*scale}" fill="#FF6B5B" fill-opacity="0.16"/>')
        # 紅橙泡泡（三顆）
        bubble_y_top = cy - 30 * scale
        bubble_r = 6 * scale
        v.append(f'<circle cx="{cx-12*scale}" cy="{bubble_y_top-8*scale}" r="{bubble_r}" '
                 f'fill="#FF7B3B" stroke="#D95C1B" stroke-width="{max(1, scale)}"/>')
        v.append(f'<circle cx="{cx}" cy="{bubble_y_top-16*scale}" r="{bubble_r+2*scale}" '
                 f'fill="#FF6B5B" stroke="#D94C3B" stroke-width="{max(1, scale)}"/>')
        v.append(f'<circle cx="{cx+12*scale}" cy="{bubble_y_top-6*scale}" r="{bubble_r+1*scale}" '
                 f'fill="#FF7B3B" stroke="#D95C1B" stroke-width="{max(1, scale)}"/>')

    elif mood == "cloud":
        # 藍色小雲蓋在山口（泡泡變小或消失）
        cloud_y = cy - 30 * scale
        # 簡化雲形：橢圓+小圓
        v.append(f'<ellipse cx="{cx}" cy="{cloud_y}" rx="{20*scale}" ry="{12*scale}" '
                 f'fill="#7EAFDB" stroke="#5A8AC8" stroke-width="{max(1, 2*scale)}"/>')
        v.append(f'<circle cx="{cx-12*scale}" cy="{cloud_y-6*scale}" r="{8*scale}" '
                 f'fill="#7EAFDB" stroke="#5A8AC8" stroke-width="{max(1, 2*scale)}"/>')
        v.append(f'<circle cx="{cx+12*scale}" cy="{cloud_y-6*scale}" r="{8*scale}" '
                 f'fill="#7EAFDB" stroke="#5A8AC8" stroke-width="{max(1, 2*scale)}"/>')

    elif mood == "calm":
        # 綠色安靜山身＋藍色小雲（已由 mountain_fill 決定）
        cloud_y = cy - 28 * scale
        v.append(f'<ellipse cx="{cx}" cy="{cloud_y}" rx="{18*scale}" ry="{10*scale}" '
                 f'fill="#7EAFDB" stroke="#5A8AC8" stroke-width="{max(1, 2*scale)}"/>')
        v.append(f'<circle cx="{cx-10*scale}" cy="{cloud_y-5*scale}" r="{7*scale}" '
                 f'fill="#7EAFDB" stroke="#5A8AC8" stroke-width="{max(1, 2*scale)}"/>')

    return "".join(v)


def tile_rack(cx, cy, scale, count=5, scrambled=False, daddy=False):
    """牌架：排列 count 張牌。scrambled=True 時亂七八糟（各種角度）；daddy=True 時半透明＋快齊。"""
    r = []
    tile_w = 32 * scale
    spacing = 38 * scale

    if daddy:
        # Daddy 牌架：半透明、快齊整（垂直排列）
        r.append(f'<g fill-opacity="0.5">')
        for i in range(count):
            tx = cx - (count-1)*spacing/2 + i*spacing
            ty = cy
            angle = -2 + i * 0.5  # 微微歪斜
            r.append(f'<g transform="translate({tx},{ty}) rotate({angle})">')
            r.append(tile(0, 0, scale, kind="mahjong", label=["dot", "stripe"][i % 2]))
            r.append(f'</g>')
        r.append(f'</g>')
    else:
        # Owen 牌架：亂序、各角度
        for i in range(count):
            tx = cx - (count-1)*spacing/2 + i*spacing
            if scrambled:
                ty = cy + ((-1)**(i) * 8 * scale)
                angle = -15 + i * 10
            else:
                ty = cy
                angle = -5 + i * 2
            r.append(f'<g transform="translate({tx},{ty}) rotate({angle})">')
            r.append(tile(0, 0, scale, kind="mahjong", label=["dot", "stripe"][i % 2]))
            r.append(f'</g>')

    return "".join(r)


# ================ SCENES ================

def scene_cover():
    """封面：遊戲桌暖光 + Owen 拿牌微笑 + tile 點綴。"""
    e = []
    e.append(sun(1080, 100, 40))
    e.append(cloud(280, 80, 0.9))
    e.append(cloud(820, 90, 0.7))
    # 星星點綴
    for (x, y, r) in [(150, 200, 16), (380, 150, 14), (920, 220, 18), (1050, 380, 14)]:
        e.append(star(x, y, r))
    e.append(sparkle(550, 110, 12))
    e.append(sparkle(280, 380, 12))

    # 吊燈光暈（暖色亮黃）
    e.append(f'<circle cx="594" cy="80" r="100" fill="#FFE9A8" fill-opacity="0.25"/>')
    e.append(f'<circle cx="594" cy="80" r="70" fill="#FFE9A8" fill-opacity="0.2"/>')

    # 圓桌（大橢圓）
    table_cx, table_cy = 594, 420
    e.append(f'<ellipse cx="{table_cx}" cy="{table_cy}" rx="280" ry="120" fill="#C9B48A" stroke="#8B6B47" stroke-width="5"/>')

    # 桌上牌（散開排列）
    for i in range(4):
        tx = 400 + i * 100
        ty = 410
        angle = -10 + i * 8
        e.append(f'<g transform="translate({tx},{ty}) rotate({angle})">')
        e.append(tile(0, 0, 0.7, kind="mahjong", label=["dot", "stripe"][i % 2]))
        e.append(f'</g>')

    # 地面
    e.append(f'<ellipse cx="594" cy="610" rx="560" ry="60" fill="#E8D4A0"/>')

    # Owen stand white T 全身
    e.append(boy(pose="stand", expr="smile", cx=450, cy=240, scale=1.3))

    # Owen 手邊牌架（右邊）
    e.append(tile_rack(740, 300, 0.8, count=5))

    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """遊戲夜：暖燈客廳圓桌，桌上麻將牌與拉密數字牌排開，Owen、April、Daddy 圍坐。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#F5EDD8"/>')

    # 吊燈光暈
    e.append(f'<circle cx="594" cy="100" r="100" fill="#FFE9A8" fill-opacity="0.3"/>')
    e.append(f'<circle cx="594" cy="100" r="70" fill="#FFE9A8" fill-opacity="0.2"/>')

    # 圓桌（大橢圓桌面）
    table_cx, table_cy = 594, 360
    e.append(f'<ellipse cx="{table_cx}" cy="{table_cy}" rx="280" ry="140" fill="#C9B48A" stroke="#8B6B47" stroke-width="5"/>')
    e.append(f'<ellipse cx="{table_cx}" cy="{table_cy-8}" rx="280" ry="140" fill="#D9C49A" stroke="#8B6B47" stroke-width="3"/>')

    # 桌上牌（散開排列）
    # 麻將牌
    for i in range(3):
        tx = 300 + i * 120
        ty = 340
        angle = -10 + i * 8
        e.append(f'<g transform="translate({tx},{ty}) rotate({angle})">')
        e.append(tile(0, 0, 0.8, kind="mahjong", label=["dot", "stripe"][i % 2]))
        e.append(f'</g>')

    # 拉密牌
    for i in range(2):
        tx = 850 + i * 100
        ty = 340
        angle = -5 + i * 6
        e.append(f'<g transform="translate({tx},{ty}) rotate({angle})">')
        e.append(tile(0, 0, 0.8, kind="lami", label=str(i+3)))
        e.append(f'</g>')

    # Owen 在桌後 bust 姿勢
    e.append(boy_bust(expr="smile", cx=594, cy=240, scale=1.1, arms="desk"))

    # April 在桌左邊（stand 姿勢遠離桌）
    e.append(april(cx=320, cy=280, scale=1.0, pose="stand"))

    # Daddy 在桌右邊（bust 姿勢在桌後）
    cx_daddy = 868
    cy_daddy = 260
    e.append(daddy(cx=cx_daddy, cy=cy_daddy, scale=1.0, pose="stand"))

    return svg(W, H, "".join(e), bg=BG["p1"])


def scene_p2():
    """Owen 拿牌微笑，眼睛發亮盯著牌河，頭上獎盃思考泡泡。"""
    e = []
    # 牌架特寫（Owen 的牌：亂七八糟）
    e.append(tile_rack(594, 280, 1.0, count=6, scrambled=True))

    # 眼睛發亮（星星眼）
    e.append(boy_bust(expr="big", cx=594, cy=180, scale=1.3))
    e.append(star(550, 120, 20))
    e.append(sparkle(650, 130, 14))

    # 思考泡泡：獎盃
    bubble_cx, bubble_cy = 850, 150
    e.append(f'<ellipse cx="{bubble_cx}" cy="{bubble_cy}" rx="120" ry="100" fill="#FFFFFF" stroke="#D4A880" stroke-width="6"/>')
    e.append(f'<circle cx="{bubble_cx+30}" cy="{bubble_cy-110}" r="22" fill="#FFFFFF" stroke="#D4A880" stroke-width="5"/>')
    e.append(f'<circle cx="{bubble_cx-50}" cy="{bubble_cy+60}" r="18" fill="#FFFFFF" stroke="#D4A880" stroke-width="5"/>')
    # 獎盃
    trophy_cx, trophy_cy = 850, 160
    e.append(f'<path d="M {trophy_cx-24} {trophy_cy} L {trophy_cx-32} {trophy_cy+35} L {trophy_cx+32} {trophy_cy+35} L {trophy_cx+24} {trophy_cy} Z" '
             f'fill="#E8A20C" stroke="#C97E08" stroke-width="4"/>')
    e.append(f'<ellipse cx="{trophy_cx}" cy="{trophy_cy-10}" rx="26" ry="16" fill="#E8A20C" stroke="#C97E08" stroke-width="4"/>')
    e.append(f'<path d="M {trophy_cx-36} {trophy_cy+2} Q {trophy_cx-48} {trophy_cy+22} {trophy_cx-30} {trophy_cy+34}" '
             f'fill="none" stroke="#C97E08" stroke-width="4" stroke-linecap="round"/>')
    e.append(f'<path d="M {trophy_cx+36} {trophy_cy+2} Q {trophy_cx+48} {trophy_cy+22} {trophy_cx+30} {trophy_cy+34}" '
             f'fill="none" stroke="#C97E08" stroke-width="4" stroke-linecap="round"/>')

    return svg(W, H, "".join(e), bg=BG["p2"])


def scene_p3():
    """Owen 的牌架特寫（牌面亂七八糟湊不成組），Daddy 那側牌快齊了（半透明示意），Owen oh 表情。"""
    e = []
    # Owen 牌架（大特寫）
    e.append(tile_rack(300, 280, 1.2, count=6, scrambled=True))

    # Daddy 牌架（遠景半透明、整齊）
    e.append(tile_rack(950, 300, 0.9, count=5, daddy=True))

    # Owen oh 表情
    e.append(boy_bust(expr="oh", cx=250, cy=140, scale=1.2))

    return svg(W, H, "".join(e), bg=BG["p3"])


def scene_p4():
    """衝動頁：Owen bust 在桌後，胸口火山冒紅泡泡，雙手伸向桌面的牌（速度線），April/Daddy oh 表情。"""
    e = []

    # 圓桌（大橢圓）
    table_cx, table_cy = 594, 380
    e.append(f'<ellipse cx="{table_cx}" cy="{table_cy}" rx="280" ry="120" fill="#C9B48A" stroke="#8B6B47" stroke-width="5"/>')

    # 桌上牌（5-6 張散開）
    for i in range(6):
        tx = 350 + i * 80
        ty = 370
        angle = -10 + i * 6
        e.append(f'<g transform="translate({tx},{ty}) rotate({angle})">')
        e.append(tile(0, 0, 0.75, kind="mahjong", label=["dot", "stripe"][i % 2]))
        e.append(f'</g>')

    # Owen bust hold 表情，在桌後
    cx_owen, cy_owen, scale_owen = 594, 240, 1.2
    e.append(boy_bust(expr="hold", cx=cx_owen, cy=cy_owen, scale=scale_owen))

    # 火山：胸口位置 (cx, cy+80*s)，寬 ≤50*s
    volcano_cx = cx_owen
    volcano_cy = cy_owen + 80 * scale_owen
    e.append(volcano(volcano_cx, volcano_cy, 0.8, mood="bubble"))

    # 雙手伸向牌（速度線）——從 bust 的手部出發（(±56,150) 身體座標），沿桌面高度，不經過臉
    hand_y = cy_owen + 132  # (150-40)*1.2 + cy
    e.append(f'<line x1="{cx_owen-70}" y1="{hand_y}" x2="{cx_owen-160}" y2="{hand_y+8}" '
             f'stroke="#F26B5E" stroke-width="6" stroke-linecap="round" stroke-dasharray="4 6"/>')
    e.append(f'<line x1="{cx_owen+70}" y1="{hand_y}" x2="{cx_owen+160}" y2="{hand_y+8}" '
             f'stroke="#F26B5E" stroke-width="6" stroke-linecap="round" stroke-dasharray="4 6"/>')

    # 熱氣線（只在人物外側空白處）
    for (x, y) in [(200, 120), (1000, 120), (150, 200), (1050, 200)]:
        e.append(f'<path d="M {x} {y} q 12 -18 24 0 q 12 18 24 0" fill="none" stroke="#F26B5E" stroke-width="8" stroke-linecap="round"/>')

    # April 和 Daddy oh 表情（在桌後）
    e.append(april(cx=280, cy=280, scale=0.9, pose="stand"))
    e.append(daddy(cx=920, cy=280, scale=0.9, pose="stand"))

    return svg(W, H, "".join(e), bg=BG["p4"])


def scene_p5():
    """紫色星空背景：Owen（press 表情）手放胸口，胸前小火山上方藍雲輕蓋山口，柔光。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#6B5BA8"/>')

    # 星星點綴（淡金色）
    for (x, y, r) in [(120, 80, 14), (1050, 100, 18), (200, 420, 12), (1000, 450, 16), (600, 40, 10)]:
        e.append(star(x, y, r, fill="#E8D4A0"))
    e.append(sparkle(350, 150, 12))
    e.append(sparkle(880, 200, 12))

    # Owen 站立，press 表情（深呼吸）
    cx_owen, cy_owen, scale_owen = 400, 280, 1.2
    e.append(boy(pose="stand", expr="press", cx=cx_owen, cy=cy_owen, scale=scale_owen))

    # 胸口火山 cloud 模式（火山棕山身可見、藍雲蓋住山口）
    volcano_cx = cx_owen
    volcano_cy = cy_owen + 80 * scale_owen
    e.append(volcano(volcano_cx, volcano_cy, 0.85, mood="cloud"))

    # 柔光效果（多層半透明圓）
    e.append(f'<circle cx="{cx_owen}" cy="{cy_owen+70}" r="60" fill="#FFD34D" fill-opacity="0.15"/>')
    e.append(f'<circle cx="{cx_owen}" cy="{cy_owen+70}" r="40" fill="#FFD34D" fill-opacity="0.2"/>')

    # "Patience power!" 文字卡
    e.append(f'<rect x="680" y="200" width="420" height="120" rx="16" fill="#E8D4A0" stroke="#D4A880" stroke-width="5"/>')
    e.append(svgtext(900, 270, "Patience power!", size=56, fill="#6B5BA8", weight="bold"))

    return svg(W, H, "".join(e), bg=BG["p5"])


def scene_p6():
    """三步腳本三格：①深呼吸（肚子大圓箭頭）②語音泡泡 "I can wait."③手輕輕放一張牌到桌面。"""
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#C5D9EC"/>')

    # 三格背景（圓角矩形框）
    grid_y = 80
    grid_h = 320
    for i, x in enumerate([200, 594, 988]):
        e.append(f'<rect x="{x-130}" y="{grid_y}" width="260" height="{grid_h}" rx="12" '
                 f'fill="#FFFFFF" stroke="#B9CFE8" stroke-width="4"/>')

    # ① 深呼吸（肚子大圓箭頭）
    e.append(f'<circle cx="200" cy="240" r="50" fill="none" stroke="#4C9AFF" stroke-width="6" stroke-dasharray="8 8"/>')
    e.append(f'<polygon points="200,170 185,210 215,210" fill="#4C9AFF"/>')  # 上箭頭
    e.append(svgtext(200, 320, "big breath", size=20, fill="#4C9AFF", weight="bold"))

    # ② 語音泡泡 "I can wait."
    e.append(f'<ellipse cx="594" cy="160" rx="100" ry="65" fill="#B8DFF2" stroke="#7EAFDB" stroke-width="4"/>')
    e.append(f'<polygon points="530,220 510,260 550,240" fill="#B8DFF2" stroke="#7EAFDB" stroke-width="3"/>')
    e.append(svgtext(594, 175, '"I can wait."', size=28, fill="#2A5A8A", weight="bold"))

    # ③ 手輕放牌（簡化表示）
    e.append(f'<ellipse cx="988" cy="200" rx="40" ry="35" fill="#D9C9B8" stroke="#8B6B47" stroke-width="3"/>')
    e.append(f'<polygon points="988,210 970,240 1010,240" fill="#8B6B47"/>')  # 下垂手指
    e.append(tile(988, 280, 0.8, kind="mahjong", label="dot"))

    # Owen stand 表情 press（全貌）
    e.append(boy(pose="stand", expr="press", cx=594, cy=120, scale=1.0))

    return svg(W, H, "".join(e), bg=BG["p6"])


def scene_p7():
    """Daddy 攤手笑（cheer 姿勢），April 笑，Daddy 牌架歪斜掉一張，波浪虛線表遊戲起伏。"""
    e = []

    # 圓桌（大橢圓）
    table_cx, table_cy = 594, 380
    e.append(f'<ellipse cx="{table_cx}" cy="{table_cy}" rx="280" ry="120" fill="#C9B48A" stroke="#8B6B47" stroke-width="5"/>')

    # 桌面波浪虛線（遊戲有高有低）
    for i in range(3):
        x_start = 200 + i * 350
        e.append(f'<path d="M {x_start} 380 Q {x_start+60} 350 {x_start+120} 380 Q {x_start+180} 410 {x_start+240} 380" '
                 f'fill="none" stroke="#8B7B70" stroke-width="5" stroke-linecap="round" stroke-dasharray="8 6"/>')

    # April 笑（左邊，在桌後）
    e.append(april(cx=280, cy=280, scale=1.0, pose="wave"))

    # Daddy 攤手笑（cheer 姿勢，右邊，在桌後）
    e.append(daddy(cx=920, cy=280, scale=1.0, pose="cheer"))

    # Daddy 牌架（長條歪斜放在桌上）
    for i in range(5):
        tx = 800 + i * 50
        ty = 360 + (i % 2) * 12  # 歪斜
        angle = -15 + i * 8
        e.append(f'<g transform="translate({tx},{ty}) rotate({angle})">')
        e.append(tile(0, 0, 0.7, kind="mahjong", label=["dot", "stripe"][i % 2]))
        e.append(f'</g>')

    # 掉落的牌（滑落到桌面下方）
    e.append(f'<g transform="translate(980,440) rotate(35)">')
    e.append(tile(0, 0, 0.7, kind="mahjong", label="stripe"))
    e.append(f'</g>')

    return svg(W, H, "".join(e), bg=BG["p7"])


def scene_p8():
    """Owen 摸到好牌（發光的牌），眼睛一亮（star 表情），April 微笑語音泡泡 "So patient, Owen!"。"""
    e = []

    # 遠景桌面
    e.append(f'<ellipse cx="594" cy="400" rx="280" ry="100" fill="#C9B48A" stroke="#8B6B47" stroke-width="4"/>')

    # Owen star 表情（特寫上半身）
    cx_owen, cy_owen = 300, 200
    e.append(boy_bust(expr="star", cx=cx_owen, cy=cy_owen, scale=1.2))

    # 發光的牌（金色光暈）
    tile_cx, tile_cy = 420, 160
    e.append(f'<circle cx="{tile_cx}" cy="{tile_cy}" r="40" fill="{STAR_Y}" fill-opacity="0.25"/>')
    e.append(f'<circle cx="{tile_cx}" cy="{tile_cy}" r="28" fill="{STAR_Y}" fill-opacity="0.3"/>')
    e.append(tile(tile_cx, tile_cy, 1.0, kind="lami", label="9", color="#F2E8C8"))

    # April 語音泡泡（右邊）
    e.append(april(cx=850, cy=300, scale=1.0, pose="wave"))
    bubble_cx, bubble_cy = 880, 140
    e.append(f'<ellipse cx="{bubble_cx}" cy="{bubble_cy}" rx="130" ry="75" fill="#FFFFFF" stroke="#D9705C" stroke-width="5"/>')
    e.append(f'<polygon points="{bubble_cx-60},{bubble_cy+75} {bubble_cx-90},{bubble_cy+120} {bubble_cx-50},{bubble_cy+80}" '
             f'fill="#FFFFFF" stroke="#D9705C" stroke-width="3"/>')
    e.append(svgtext(880, 155, '"So patient, Owen!"', size=28, fill="#C9705C", weight="bold"))

    return svg(W, H, "".join(e), bg=BG["p8"])


def scene_p9():
    """兩小格轉移：左格珠心算習題紙紅 ✗＋Owen 深呼吸（小火山安靜）；右格牌桌＋Owen 微笑；每格角落小藍雲 icon。"""
    e = []

    # 框架背景
    frame_y = 60
    frame_h = 420
    frame_w = 480

    # 左格
    e.append(f'<rect x="80" y="{frame_y}" width="{frame_w}" height="{frame_h}" rx="14" '
             f'fill="#FFF5F0" stroke="#F2A9A0" stroke-width="5"/>')

    # 右格
    e.append(f'<rect x="{1188-80-frame_w}" y="{frame_y}" width="{frame_w}" height="{frame_h}" rx="14" '
             f'fill="#FFF5F0" stroke="#F2A9A0" stroke-width="5"/>')

    # 左格：習題紙 + 紅叉 + 火山安靜 + 深呼吸
    e.append(f'<rect x="120" y="100" width="200" height="150" fill="#FFFBF8" stroke="#D4A880" stroke-width="3"/>')
    # 紅叉
    e.append(f'<line x1="140" y1="120" x2="300" y2="240" stroke="#E4574C" stroke-width="8" stroke-linecap="round"/>')
    e.append(f'<line x1="300" y1="120" x2="140" y2="240" stroke="#E4574C" stroke-width="8" stroke-linecap="round"/>')

    # Owen 在左格（小尺寸）
    e.append(boy_bust(expr="press", cx=290, cy=280, scale=0.8))
    # 火山 calm 模式
    e.append(volcano(290, 340, 0.8, mood="calm"))
    # 深呼吸圓箭頭（小）
    e.append(f'<circle cx="160" cy="340" r="35" fill="none" stroke="#4C9AFF" stroke-width="4" stroke-dasharray="6 6"/>')
    e.append(f'<polygon points="160,300 150,330 170,330" fill="#4C9AFF"/>')

    # 左格角落藍雲 icon
    e.append(cloud(120, 80, 0.6, fill="#7EAFDB", op=0.8))

    # 右格：牌桌 + Owen 微笑
    e.append(f'<ellipse cx="{800}" cy="320" rx="160" ry="80" fill="#C9B48A" stroke="#8B6B47" stroke-width="3"/>')
    e.append(boy_bust(expr="smile", cx=800, cy=240, scale=0.9, arms="desk"))

    # 右格角落藍雲 icon
    e.append(cloud(628-120, 80, 0.6, fill="#7EAFDB", op=0.8))

    return svg(W, H, "".join(e), bg=BG["p9"])


def scene_p10():
    """英雄收尾：Owen 披紅披風叉腰，胸口的火山變成安靜的綠色小山（山頂一朵藍色小雲），滿天星。"""
    e = []

    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="110" fill="#FFDD7E"/>')

    # 滿天星
    for (x, y, r) in [(160, 120, 20), (1020, 120, 24), (120, 380, 16), (1060, 380, 16), (330, 70, 12), (860, 70, 14),
                       (450, 200, 14), (750, 200, 14)]:
        e.append(star(x, y, r))
    e.append(sparkle(260, 260, 12))
    e.append(sparkle(930, 260, 12))

    # 英雄 Owen（hips 姿勢 + cape）
    cx_owen, cy_owen, scale_owen = 594, 180, 1.25
    e.append(boy(pose="hips", expr="proud", cx=cx_owen, cy=cy_owen, scale=scale_owen, cape=True))

    # 胸口火山 calm 模式
    volcano_cx = cx_owen
    volcano_cy = cy_owen + 100 * scale_owen
    e.append(volcano(volcano_cx, volcano_cy, scale_owen, mood="calm"))

    return svg(W, H, "".join(e), bg=BG["p10"])


# ================ PAGE TEXTS ================

PAGES = [
    ("p1", scene_p1, "This is me, <b>Owen</b>!<br/>Game night! We play <b>tiles</b>."),
    ("p2", scene_p2, "We take turns.<br/>I pick a tile.<br/>I want to <b>WIN</b>!"),
    ("p3", scene_p3, "But my tiles are bad.<br/>Daddy is winning.<br/>Losing, losing, again!"),
    ("p4", scene_p4, "My <b>volcano</b> starts to bubble!<br/>Hot, hot, hot inside.<br/>I want to push the tiles!"),
    ("p5", scene_p5, "<b>STOP!</b> I use my superpower&hellip;<br/><b>Patience</b> power!"),
    ("p6", scene_p6, "One big breath.<br/>I say, &ldquo;I can wait.&rdquo;<br/>I play my turn."),
    ("p7", scene_p7, "Games go up and down.<br/>Daddy loses sometimes too.<br/>We laugh and play again!"),
    ("p8", scene_p8, "My turn comes back.<br/>Good tile!<br/>Mommy April smiles. &ldquo;So patient, <b>Owen</b>!&rdquo;"),
    ("p9", scene_p9, "Math page hard? Patience!<br/>Game going bad? Patience!<br/>I feel <b>GREAT</b>!"),
    ("p10", scene_p10, "Big breath. I can wait.<br/><b>Patience power!</b><br/>I practice every day!"),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("與 One more try 的分工", "輸完了、失敗了 → 用 &ldquo;One more try!&rdquo;（重新出發）；還在遊戲中快輸、快炸 → 用 &ldquo;Patience power!&rdquo;（撐住這一輪）。當下只指口訣，不講道理。"),
    ("大人示範輸牌", "玩遊戲時故意旁白自己的耐心（「爸爸的牌好爛，我的火山在冒泡……深呼吸，I can wait」）——他看過大人用，才會相信這招有用。"),
    ("當他主動說 My volcano bubbles", "或自己深呼吸 = 情緒覺察里程碑，大力稱讚；遊戲結束後再跟他數「今天火山冒泡幾次、蓋住幾次」。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

BOOK = {
    "slug": "patience-power",
    "order": 14,
    "title_pre": "", "title_hi": "Patience", "title_post": " Power!",
    "title_zh": "耐心超能力",
    "subtitle": "Owen's game night story",
    "tagline_zh": "Owen 的遊戲夜故事",
    "chips": ["Social Story", "English", "11 pages"],
    "pdf_name": "Patience_Power.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ['patience', 'volcano', 'tiles'],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Big breath → \"I can wait\" → Patience power!</b>&nbsp;"
                 "當他哪天主動說出 &ldquo;My volcano bubbles&rdquo;（我察覺到快炸了），"
                 "就是最值得大力稱讚的時刻。"),
    "cover": scene_cover,
}
