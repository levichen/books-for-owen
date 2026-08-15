# -*- coding: utf-8 -*-
"""Book 18: Hold and Wait! — 防走失故事（人多牽手 → 沒看到爸媽待在裡面 → 原地等大人來）。"""
import math
from parts import *
from book_common import svg, svgtext, TXT, W, H

# soft page palettes
BG = {
    "cover": "#FFF8E8", "p1": "#E8F4FF", "p2": "#FFF3D6", "p3": "#F0E8FF",
    "p4": "#FFE8E8", "p5": "#D4B4FF", "p6": "#FFE8F8", "p7": "#E8F8D8",
    "p8": "#FFF0C9", "p9": "#FFE9A8", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

# ================== SHARED FUNCTIONS ==================

def hand_in_hand(cx, cy, scale):
    """大手牽小手共用圖示（local 座標，外層 translate+scale）。用於 p5、p6①、p10 徽章。"""
    h = []
    # 光暈三層
    h.append(f'<circle cx="0" cy="0" r="90" fill="#FFE9A8" fill-opacity="0.25"/>')
    h.append(f'<circle cx="0" cy="0" r="68" fill="#FFE9A8" fill-opacity="0.4"/>')
    h.append(f'<circle cx="0" cy="0" r="48" fill="#FFE9A8" fill-opacity="0.6"/>')

    # 粉袖口（April，左側）
    h.append(f'<rect x="-84" y="-20" width="30" height="40" rx="10" fill="#F48FB1"/>')

    # 大手掌（從左伸入）
    h.append(f'<ellipse cx="-30" cy="0" rx="36" ry="27" fill="#F6C99F"/>')

    # 白袖口（Owen，右側）
    h.append(f'<rect x="52" y="-16" width="26" height="32" rx="9" fill="#FFFFFF" stroke="#E0D6CC" stroke-width="1.5"/>')

    # 小手掌（從右伸入）
    h.append(f'<ellipse cx="26" cy="0" rx="22" ry="17" fill="#FFDFC2"/>')

    # 大手四根手指
    h.append(f'<rect x="0" y="-18" width="34" height="9" rx="4.5" fill="#F6C99F"/>')
    h.append(f'<rect x="2" y="-6" width="38" height="9" rx="4.5" fill="#F6C99F"/>')
    h.append(f'<rect x="0" y="6" width="32" height="9" rx="4.5" fill="#F6C99F"/>')

    # 大拇指
    h.append(f'<ellipse cx="8" cy="17" rx="15" ry="8" fill="#F6C99F"/>')

    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(h)}</g>'


def crowd_silhouettes(cx, cy, scale):
    """人群剪影（背景用）。"""
    c = []
    silhouettes = [
        (-200, 0, 1.0, 0.5), (-100, 20, 0.9, 0.45), (-30, 10, 0.8, 0.4),
        (80, 0, 1.05, 0.55), (180, 25, 0.75, 0.38), (280, 5, 0.95, 0.5), (360, 30, 0.7, 0.35),
    ]
    for sx, sy, h_scale, w_scale in silhouettes:
        head_r = 20 * h_scale
        body_h = 80 * h_scale
        body_w = 35 * w_scale
        c.append(f'<circle cx="{sx}" cy="{sy - body_h/2 - head_r}" r="{head_r}" fill="#2A2320" fill-opacity="0.3"/>')
        c.append(f'<rect x="{sx - body_w}" y="{sy - body_h/2}" width="{body_w*2}" height="{body_h}" fill="#2A2320" fill-opacity="0.25" rx="{body_w*0.3}"/>')
    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(c)}</g>'


def elevator_door_open(cx, cy, scale):
    """電梯門開啟（左右各滑開一半）。"""
    e = []
    e.append(f'<rect x="-90" y="-140" width="180" height="260" rx="8" fill="#E8E8E8" stroke="#A8A8A8" stroke-width="3"/>')
    e.append(f'<rect x="-90" y="-130" width="80" height="230" rx="4" fill="#D4D4D4" stroke="#888888" stroke-width="2"/>')
    e.append(f'<circle cx="-45" cy="0" r="4" fill="#888888"/>')
    e.append(f'<rect x="10" y="-130" width="80" height="230" rx="4" fill="#D4D4D4" stroke="#888888" stroke-width="2"/>')
    e.append(f'<circle cx="55" cy="0" r="4" fill="#888888"/>')
    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(e)}</g>'


def waiting_spot_glow(cx, cy, scale):
    """等候點發光橢圓。"""
    w = []
    w.append(f'<ellipse cx="0" cy="0" rx="85" ry="18" fill="#FFE9A8" fill-opacity="0.3"/>')
    w.append(f'<ellipse cx="0" cy="0" rx="65" ry="14" fill="#FFE9A8" fill-opacity="0.45"/>')
    w.append(f'<ellipse cx="0" cy="0" rx="45" ry="10" fill="#FFE9A8" fill-opacity="0.6"/>')
    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(w)}</g>'


# ================== SCENES ================

def scene_cover():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="620" fill="{BG["cover"]}"/>')
    e.append(f'<ellipse cx="594" cy="620" rx="560" ry="100" fill="#FFDD7E"/>')
    e.append(crowd_silhouettes(594, 380, 1.0))
    for (x, y, r) in [(120, 100, 16), (1050, 120, 18), (180, 500, 14), (1080, 480, 16), (400, 80, 12), (800, 520, 14)]:
        e.append(star(x, y, r, fill=STAR_Y))
    e.append(boy(pose="run", expr="big", cx=594, cy=340, scale=1.3))
    for i in range(3):
        y_pos = 375 + (i - 1) * 23  # 軀幹高度（比照 p1 驗證過的偏移），不碰頭
        e.append(f'<line x1="440" y1="{y_pos}" x2="515" y2="{y_pos}" stroke="#FFC93C" stroke-width="3" stroke-linecap="round"/>')
    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p1"]}"/>')
    e.append(f'<ellipse cx="594" cy="560" rx="560" ry="80" fill="#D4E8FF"/>')
    e.append(cloud(150, 80, 0.9))
    e.append(cloud(900, 100, 1.1))
    for (x, y, r) in [(200, 120, 18), (950, 130, 20)]:
        e.append(star(x, y, r))
    e.append(sparkle(380, 100, 12))
    e.append(sparkle(820, 110, 14))
    e.append(boy(pose="run", expr="big", cx=450, cy=270, scale=1.15))
    for i in range(3):
        y_pos = 310 + (i - 1) * 20
        e.append(f'<line x1="310" y1="{y_pos}" x2="380" y2="{y_pos}" stroke="#FFC93C" stroke-width="3" stroke-linecap="round"/>')
    return svg(W, H, "".join(e), bg=None)


def scene_p2():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p2"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#E8D2AC"/>')
    for cx in [300, 594, 900]:
        e.append(f'<rect x="{cx-80}" y="30" width="160" height="20" fill="#E8D2AC" opacity="0.6"/>')
    for cx in [250, 594, 950]:
        e.append(f'<ellipse cx="{cx}" cy="50" rx="70" ry="15" fill="#F4E4A0" opacity="0.7"/>')
        e.append(f'<circle cx="{cx}" cy="55" r="8" fill="#FFD700" opacity="0.6"/>')
    for stall_x in [200, 594, 950]:
        e.append(f'<rect x="{stall_x-60}" y="260" width="120" height="160" rx="6" fill="#E8D2AC" stroke="#C4A272" stroke-width="2"/>')
    e.append(crowd_silhouettes(350, 300, 0.9))
    e.append(crowd_silhouettes(850, 310, 0.85))
    e.append(daddy(cx=200, cy=260, scale=1.3, pose="stand"))
    e.append(april(cx=470, cy=253, scale=1.25, pose="stand"))  # 鞋底 518 與 Owen 對齊，大人明顯較高
    e.append(boy(pose="stand", expr="big", cx=540, cy=290, scale=1.0))
    e.append(f'<path d="M 505 345 L 540 345" stroke="{SKIN}" stroke-width="10" stroke-linecap="round" fill="none"/>')
    return svg(W, H, "".join(e), bg=None)


def scene_p3():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p3"]}"/>')
    e.append(f'<g transform="translate(900,120)"><rect x="-45" y="-22" width="90" height="44" rx="8" fill="#FFB3BA" stroke="#FF6B6B" stroke-width="2.5"/><text x="0" y="10" font-family="Huninn" font-size="18" fill="#2A2320" text-anchor="middle" font-weight="bold">玩具</text><g transform="translate(-50, 40)"><rect x="-14" y="-10" width="28" height="20" rx="3" fill="#FFD93D"/><circle cx="-8" cy="8" r="5" fill="#5D3A1A"/><circle cx="8" cy="8" r="5" fill="#5D3A1A"/></g></g>')
    for i, (ox, oc) in enumerate([(-20, "#FFD700"), (0, "#FF6B9D"), (20, "#7BA8E8"), (40, "#FFD700")]):
        e.append(f'<circle cx="{1000+ox}" cy="280" r="14" fill="{oc}" stroke="{oc}" stroke-width="1"/>')
    e.append(f'<path d="M 980 280 L 1040 280" stroke="#CCCCCC" stroke-width="2" stroke-dasharray="3 2"/>')
    e.append(f'<g transform="translate(920, 420)"><polygon points="0,-15 -20,15 20,15" fill="#FF8866"/><rect x="-15" y="15" width="30" height="20" rx="4" fill="#E8D2AC" stroke="#C4A272" stroke-width="1"/><circle cx="-8" cy="25" r="8" fill="#FFB3BA"/><circle cx="8" cy="25" r="8" fill="#FFB3BA"/></g>')
    e.append(f'<path d="M 350 200 Q 600 160 900 120" stroke="#4A78A8" stroke-width="2" stroke-dasharray="5 8" fill="none"/>')
    e.append(f'<path d="M 350 200 Q 650 240 1000 280" stroke="#4A78A8" stroke-width="2" stroke-dasharray="5 8" fill="none"/>')
    e.append(f'<path d="M 350 200 Q 600 300 920 420" stroke="#4A78A8" stroke-width="2" stroke-dasharray="5 8" fill="none"/>')
    e.append(boy_bust(expr="star", cx=280, cy=320, scale=1.4))
    return svg(W, H, "".join(e), bg=None)


def scene_p4():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p4"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#E8D2AC"/>')
    e.append(f'<rect x="50" y="140" width="280" height="240" rx="14" fill="#FFFFFF" stroke="#FFB3D9" stroke-width="3"/>')
    e.append(april(cx=140, cy=258, scale=1.18, pose="stand"))  # 鞋底 508 與 Owen 對齊，大人較高
    e.append(f'<rect x="280" y="260" width="120" height="140" rx="6" fill="#FFE8E8" stroke="#FFB3BA" stroke-width="2"/>')
    e.append(boy(pose="run", expr="big", cx=320, cy=280, scale=1.0))
    for i in range(3):
        y_pos = 380 + (i - 1) * 20  # 軀幹高度、拖在身後，不碰臉
        e.append(f'<line x1="215" y1="{y_pos}" x2="256" y2="{y_pos}" stroke="#FFC93C" stroke-width="3" stroke-linecap="round"/>')
    e.append(f'<rect x="858" y="140" width="280" height="240" rx="14" fill="#FFFFFF" stroke="#FFB3D9" stroke-width="3"/>')
    e.append(crowd_silhouettes(998, 320, 0.95))
    e.append(boy(pose="stand", expr="oh", cx=880, cy=280, scale=1.0))
    e.append(svgtext(880, 180, "?", size=72, fill="#FFB3BA", weight="bold"))
    heart_cx = 850
    heart_cy = 390  # 白T中段（chin≈315，boom 波紋不得碰頭）
    e.append(f'<path d="M {heart_cx} {heart_cy} c 0 -6 -6 -12 -12 -12 c -6 0 -12 6 -12 12 c 0 12 12 18 12 18 s 12 -6 12 -18 Z" fill="#E57373"/>')
    e.append(f'<ellipse cx="{heart_cx}" cy="{heart_cy}" rx="24" ry="20" fill="none" stroke="#E57373" stroke-width="3" opacity="0.7"/>')
    e.append(f'<ellipse cx="{heart_cx}" cy="{heart_cy}" rx="34" ry="28" fill="none" stroke="#E57373" stroke-width="3" opacity="0.45"/>')
    return svg(W, H, "".join(e), bg=None)


def scene_p5():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p5"]}"/>')
    for (x, y, r) in [(120, 100, 14), (1050, 120, 16), (200, 450, 12), (1000, 430, 14), (350, 80, 10), (850, 70, 12)]:
        e.append(star(x, y, r, fill=STAR_Y))
    e.append(sparkle(280, 100, 12))
    e.append(sparkle(950, 110, 14))
    e.append(boy_bust(expr="press", cx=320, cy=300, scale=1.3, arms="desk"))
    e.append(hand_in_hand(830, 190, 1.0))
    return svg(W, H, "".join(e), bg=None)


def scene_p6():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p6"]}"/>')
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#FFE8F0"/>')
    for i, box_x in enumerate([210, 594, 978]):
        e.append(f'<rect x="{box_x-150}" y="60" width="300" height="320" rx="16" fill="#FFFFFF" stroke="#FFB3D9" stroke-width="4"/>')
        e.append(f'<line x1="{box_x-145}" y1="340" x2="{box_x+145}" y2="340" stroke="#FFD4E8" stroke-width="2"/>')
        if i == 0:
            e.append(hand_in_hand(box_x, 220, 0.75))
        elif i == 1:
            e.append(f'<rect x="{box_x+50}" y="80" width="90" height="220" rx="6" fill="#D4B8A0" stroke="#A89968" stroke-width="2"/>')
            e.append(f'<rect x="{box_x+52}" y="82" width="86" height="60" fill="#AAAAAA" opacity="0.3"/>')
            e.append(f'<line x1="{box_x+60}" y1="110" x2="{box_x+130}" y2="110" stroke="#888888" stroke-width="1" opacity="0.5"/>')
            e.append(boy(pose="stand", expr="hold", cx=box_x-30, cy=220, scale=0.95))
            e.append(f'<line x1="{box_x+60}" y1="95" x2="{box_x+130}" y2="125" stroke="#E8574C" stroke-width="5" stroke-linecap="round"/>')
            e.append(f'<line x1="{box_x+130}" y1="95" x2="{box_x+60}" y2="125" stroke="#E8574C" stroke-width="5" stroke-linecap="round"/>')
        else:
            e.append(boy(pose="stand", expr="proud", cx=box_x-50, cy=240, scale=0.95))
            e.append(april(cx=box_x+50, cy=220, scale=1.05, pose="wave"))
            e.append(f'<path d="M {box_x} 140 c 0 -5 -5 -10 -10 -10 c -5 0 -10 5 -10 10 c 0 10 10 16 10 16 s 10 -6 10 -16 Z" fill="#FF6B6B"/>')
    return svg(W, H, "".join(e), bg=None)


def scene_p7():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p7"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#E8F8D8"/>')
    e.append(f'<rect x="60" y="100" width="280" height="280" rx="14" fill="#FFFFFF" stroke="#C4E8B4" stroke-width="3"/>')
    e.append(f'<line x1="70" y1="330" x2="330" y2="330" stroke="#E8F8D8" stroke-width="2"/>')
    e.append(april(cx=140, cy=240, scale=1.0, pose="stand"))
    e.append(boy(pose="stand", expr="smile", cx=220, cy=265, scale=0.95))
    e.append(f'<path d="M 190 290 L 210 290" stroke="{SKIN}" stroke-width="10" stroke-linecap="round" fill="none"/>')
    e.append(f'<path d="M 140 130 c 0 -6 -6 -12 -12 -12 c -6 0 -12 6 -12 12 c 0 12 12 20 12 20 s 12 -8 12 -20 Z" fill="#FF6B6B"/>')
    e.append(f'<rect x="848" y="100" width="280" height="280" rx="14" fill="#FFFFFF" stroke="#C4E8B4" stroke-width="3"/>')
    e.append(f'<line x1="858" y1="330" x2="1118" y2="330" stroke="#E8F8D8" stroke-width="2"/>')
    e.append(boy(pose="stand", expr="proud", cx=920, cy=270, scale=0.95))
    e.append(daddy(cx=1010, cy=240, scale=1.15, pose="point"))
    e.append(f'<path d="M 960 250 Q 980 250 1000 250" stroke="#FFC93C" stroke-width="3" stroke-dasharray="6 10" fill="none" opacity="0.8"/>')
    e.append(f'<path d="M 920 130 c 0 -6 -6 -12 -12 -12 c -6 0 -12 6 -12 12 c 0 12 12 20 12 20 s 12 -8 12 -20 Z" fill="#FF6B6B"/>')
    e.append(f'<path d="M 200 340 Q 594 380 988 340" stroke="#FFE9A8" stroke-width="8" fill="none" opacity="0.6"/>')
    e.append(f'<path d="M 200 340 Q 594 380 988 340" stroke="#FFDD7E" stroke-width="3" fill="none"/>')
    return svg(W, H, "".join(e), bg=None)


def scene_p8():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p8"]}"/>' )
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#FFF0C9"/>' )
    # LEFT: elevator well on main ground
    e.append(f'<rect x="95" y="110" width="150" height="360" fill="#8A8F98"/>' )
    e.append(f'<rect x="125" y="150" width="90" height="320" fill="#D8DCE2"/>' )
    e.append(boy(pose="stand", expr="smile", cx=170, cy=374, scale=0.55))
    e.append(f'<rect x="95" y="150" width="30" height="320" fill="#B8BDC6"/>' )
    e.append(f'<rect x="215" y="150" width="30" height="320" fill="#B8BDC6"/>' )
    e.append(f'<rect x="115" y="112" width="110" height="32" fill="#333333"/>' )
    e.append(svgtext(170, 127, "3 · 2 · 1", size=20, fill="#FFFFFF", weight="bold"))
    # RIGHT: ground floor
    e.append(f'<rect x="858" y="100" width="280" height="280" rx="14" fill="#FFFFFF" stroke="#FFD9A8" stroke-width="3"/>' )
    e.append(f'<line x1="868" y1="320" x2="1128" y2="320" stroke="#FFE8D8" stroke-width="2"/>' )
    e.append(f'<line x1="1090" y1="430" x2="1090" y2="560" stroke="#A89968" stroke-width="8"/>' )
    e.append(f'<line x1="1120" y1="430" x2="1120" y2="560" stroke="#A89968" stroke-width="8"/>' )
    e.append(waiting_spot_glow(780, 475, 1.0))
    e.append(boy(pose="stand", expr="smile", cx=780, cy=242, scale=1.0))
    e.append(april(cx=990, cy=226, scale=1.15, pose="cheer"))
    e.append(f'<path d="M 1010 160 Q 1010 135 1070 135 L 1100 135 Q 1120 135 1120 155 L 1120 180 Q 1120 195 1100 195 L 1070 195 L 1060 215 L 1070 195 L 1040 195 Q 1010 195 1010 175 Z" fill="#FFFFFF" stroke="#FFD9A8" stroke-width="2"/>' )
    e.append(svgtext(1060, 155, "Super waiting,", size=13, fill="#8B6D47", weight="bold"))
    e.append(svgtext(1060, 175, "Owen!", size=13, fill="#8B6D47", weight="bold"))
    return svg(W, H, "".join(e), bg=None)


def scene_p9():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p9"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#FFE9A8"/>')
    for cx in [250, 594, 950]:
        e.append(f'<ellipse cx="{cx}" cy="40" rx="70" ry="15" fill="#F4E4A0" opacity="0.7"/>')
    e.append(crowd_silhouettes(280, 300, 0.95))
    e.append(crowd_silhouettes(920, 310, 0.9))
    e.append(april(cx=430, cy=237, scale=1.1, pose="stand"))
    e.append(boy(pose="stand", expr="proud", cx=594, cy=242, scale=1.0))
    e.append(daddy(cx=760, cy=200, scale=1.25, pose="stand"))
    owen_left_x = 594 - 48
    owen_right_x = 594 + 48
    hand_y = 242 + 136
    april_hand_x = 430 - 48
    april_hand_y = 237 + 136*1.1
    daddy_hand_x = 760 + 48
    daddy_hand_y = 270 + 136*1.2
    e.append(f'<path d="M {owen_left_x} {hand_y} Q {(owen_left_x + april_hand_x)/2} {min(hand_y, april_hand_y) - 30} {april_hand_x} {april_hand_y}" stroke="#F6C99F" stroke-width="10" stroke-linecap="round" fill="none"/>')
    e.append(f'<path d="M 642 378 Q 671 373 700 370" stroke="#F6C99F" stroke-width="10" stroke-linecap="round" fill="none"/>' )
    for (x, y, r) in [(150, 100, 12), (1020, 120, 14), (300, 430, 10), (950, 430, 12)]:
        e.append(star(x, y, r, fill=STAR_Y))
    return svg(W, H, "".join(e), bg=None)


def scene_p10():
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p10"]}"/>')
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="100" fill="#FFE9A8"/>')
    for (x, y, r) in [(140, 100, 18), (1040, 110, 20), (120, 380, 16), (1060, 390, 18), (310, 60, 12), (880, 70, 14), (450, 420, 10), (750, 430, 11)]:
        e.append(star(x, y, r))
    e.append(sparkle(420, 320, 14))
    e.append(sparkle(770, 320, 14))
    e.append(sparkle(500, 300, 10))
    e.append(sparkle(690, 290, 10))
    e.append(boy(pose="hips", expr="proud", cx=594, cy=240, scale=1.3, cape=True))
    hand_x = 651   # hips 手位 (44,150) → 594+44*1.3
    hand_y = 396   # 240+(150-30)*1.3
    e.append(f'<circle cx="{hand_x}" cy="{hand_y}" r="26" fill="#FFE9A8" fill-opacity="0.35"/>')
    e.append(f'<circle cx="{hand_x}" cy="{hand_y}" r="16" fill="#FFE9A8" fill-opacity="0.6"/>')
    e.append(hand_in_hand(800, 375, 0.5))  # 肩下身側，徽章頂端(≈330)低於下巴(≈310)以下留距
    return svg(W, H, "".join(e), bg=None)


# ================== PAGE TEXTS ================

PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>My legs love to go, go, go!'),
    ("p2", scene_p2, 'We go out with Mommy and Daddy.<br/>So many people everywhere!'),
    ("p3", scene_p3, 'Lights! Toys! Yummy food!<br/>I want to see it ALL!'),
    ("p4", scene_p4, 'My feet <b>fly</b> first!<br/>My hand slips away.<br/>Where is Mommy? My heart goes boom!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I hold and I wait!'),
    ("p6", scene_p6, 'So many people? Hold a hand!<br/>No Mommy? Stay <b>inside</b>.<br/>I wait. Mommy comes to me!'),
    ("p7", scene_p7, 'Mommy holds my hand. She feels happy.<br/>When I wait, Daddy finds me fast.<br/>Hold and wait keeps me safe!'),
    ("p8", scene_p8, 'School is done! <b>Elevator</b> down—three, two, one!<br/>No Mommy yet? I stay and wait.<br/>Mommy April comes. &ldquo;Super waiting, <b>Owen</b>!&rdquo;'),
    ("p9", scene_p9, 'We go out again.<br/>I hold. I wait. I stay close.<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Hold a hand. Stay inside. Wait!<br/><b>Hold and wait!</b><br/>I practice every day!'),
]


# ================== PARENT TIPS ================

PARENT_TIPS = [
    ("等候點固定化", "跟他約好放學的固定等候點（一樓電梯口），每天同一位置；大人遲到也<b>永遠先去那個點</b>找他。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材或事後檢討工具，這本書就報廢了。"),
    ("把牽手變好玩", "出門前預告「今天是 hold and wait 日」；牽手時玩捏手遊戲（媽媽捏三下＝我愛你，Owen 捏回來）。"),
    ("教他識別家長", "指著 April 和 Daddy 確認「這是你媽媽」「這是你爸爸」，特別是走失情境下能靠聲音輪廓識人。"),
    ("當他主動說出覺察時大力稱讚", "當他主動說 \"My feet fly first\"、或在一樓自己站到等候點 = 覺察里程碑。"),
    ("不用「會被壞人抓走」恐嚇", "講「這樣媽媽一下就找到你」，恐懼會讓腳本失效（嚇到亂跑）。"),
]


# ================== BOOK DICT ================

BOOK = {
    "slug": "hold-and-wait",
    "order": 18,
    "title_pre": "", "title_hi": "Hold", "title_post": " and Wait!",
    "title_zh": "牽好，等好",
    "subtitle": "Owen's safety story",
    "tagline_zh": "Owen 的防走失故事",
    "chips": ["Social Story", "Safety", "11 pages"],
    "pdf_name": "Hold_and_Wait.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ["elevator", "inside", "fly"],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標是替 Owen 安裝一套<b>當人多或看不到大人時用得出來的「原地等」腳本</b>"
                     "——不靠恐懼，靠成就感。"),
    "cue_html": ("口訣（全書通關密語）：<b>Hold a hand → Stay inside → Wait, Mommy comes</b>&nbsp;"
                 "（喊法：Hold and wait!）。當他主動牽手、在一樓自己站到等候點、或走散時沒有尖叫亂跑反而靜靜等著，就是里程碑。"),
    "cover": scene_cover,
}
