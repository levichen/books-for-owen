# -*- coding: utf-8 -*-
"""Book 3: One More Try! — 棒球比賽中遇到挫折時的衝動管理（草稿）。"""
from parts import *
from book_common import svg, svgtext, TXT, W, H
import math

# soft page palettes
BG = {
    "cover": "#FFF9E6", "p1": "#FFF9E6", "p2": "#FFE8D0", "p3": "#FFD6C0",
    "p4": "#FFE0D5", "p5": "#E8D8F5", "p6": "#E0E8FF", "p7": "#E8F0E0",
    "p8": "#FFF0D0", "p9": "#FFE6E0", "p10": "#FFF9E6", "p11": "#FBF4E8",
}

# ----------------SCENES ----------------
def scene_cover():
    """封面：Owen 白 T-shirt 拿著棒球手套與球棒站在家門口，星星點綴。"""
    e = []
    # 背景元素
    e.append(sun(1080, 100, 40))
    e.append(cloud(280, 80, 0.9))
    e.append(cloud(820, 90, 0.7))
    # 星星點綴
    for (x, y, r) in [(150, 200, 16), (380, 150, 14), (920, 220, 18), (1050, 380, 14)]:
        e.append(star(x, y, r))
    e.append(sparkle(550, 110, 12))
    e.append(sparkle(280, 380, 12))
    # 地面
    e.append(f'<ellipse cx="594" cy="640" rx="560" ry="120" fill="#E8D4A0"/>')
    # Owen stand white T 全身
    cx, cy, scale = 594, 300, 1.3
    e.append(boy(pose="stand", expr="smile", cx=cx, cy=cy, scale=scale, jersey=None))
    # 右手握球棒：stand 姿勢右手身體座標 (48,166) → 畫面 (cx+48s, cy+136s)
    bat_cx = cx + 48*scale
    bat_cy = cy + 136*scale
    e.append(bat(cx=bat_cx, cy=bat_cy, angle=-60, scale=0.95))
    # 手套：實心棕色手套（大圓 + 拇指小圓 + 縫線弧），放地上
    glove_cx, glove_cy = cx - 90, cy + 210
    e.append(f'<circle cx="{glove_cx}" cy="{glove_cy}" r="42" fill="#8B6B47" stroke="#5C4A31" stroke-width="3"/>')
    e.append(f'<circle cx="{glove_cx-52}" cy="{glove_cy-8}" r="15" fill="#8B6B47" stroke="#5C4A31" stroke-width="3"/>')  # 拇指
    e.append(f'<path d="M {glove_cx-22} {glove_cy-38} Q {glove_cx} {glove_cy-48} {glove_cx+22} {glove_cy-38}" fill="none" stroke="#5C4A31" stroke-width="3" stroke-linecap="round"/>')  # 縫線
    # baseball 放地上
    e.append(baseball(cx=cx+110, cy=cy+190, r=16))
    return svg(1188, 620, "".join(e), bg=None)

def scene_p1():
    """p1：Owen 白 T-shirt 拿著棒球手套與球棒站在家門口，頭上星星。"""
    e = []
    e.append(sun(1050, 90, 36))
    e.append(cloud(240, 90, 1.0))
    e.append(cloud(600, 70, 0.7))
    # ground
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#C8DDB8"/>')
    e.append(f'<path d="M 0 560 Q 594 400 1188 560 L 1188 560 L 0 560 Z" fill="#E8D4A0"/>')
    # home at bottom
    e.append(f'<polygon points="594,520 610,500 610,540 594,545 578,540 578,500" fill="#FFFFFF" stroke="#8B6B47" stroke-width="3"/>')
    # house in distance
    e.append(f'<rect x="880" y="270" width="230" height="160" rx="10" fill="#F2D8B8" stroke="#D4A880" stroke-width="4"/>')
    e.append(f'<polygon points="870,270 995,205 1120,270" fill="#C86450"/>')
    e.append(f'<circle cx="950" cy="240" r="8" fill="#FFD34D"/>')
    e.append(f'<rect x="910" y="300" width="44" height="36" rx="4" fill="#B8E3F2"/>')
    e.append(f'<rect x="1040" y="300" width="44" height="36" rx="4" fill="#B8E3F2"/>')
    # bushes
    e.append(f'<circle cx="80" cy="430" r="40" fill="#8FCB84"/><circle cx="130" cy="440" r="30" fill="#79BD6E"/>')
    # boy with glove and bat
    e.append(boy(pose="stand", expr="smile", cx=420, cy=210, scale=1.15))
    e.append(f'<ellipse cx="330" cy="330" rx="32" ry="40" fill="none" stroke="#8B6B47" stroke-width="4"/>')
    e.append(f'<circle cx="295" cy="328" r="8" fill="#8B6B47"/>')  # 拇指孔
    e.append(bat(cx=520, cy=270, angle=-30, scale=0.85))
    # 頭上星星
    e.append(star(560, 90, 18))
    e.append(sparkle(680, 140, 12))
    return svg(W, H, "".join(e))

def scene_p2():
    """p2：球場入口，Owen 100 號球衣背對觀眾走向球場，思考泡泡大「?」與哭臉獎盃。"""
    e = []
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#D4C8A8"/>')  # 場地
    # 遠景看台
    e.append(f'<polygon points="100,380 200,280 800,280 900,380 900,450 100,450" fill="#B8A89C"/>')
    e.append(f'<rect x="120" y="320" width="18" height="60" fill="#8B7B70"/>')
    e.append(f'<rect x="220" y="310" width="18" height="70" fill="#8B7B70"/>')
    e.append(f'<rect x="750" y="310" width="18" height="70" fill="#8B7B70"/>')
    # 思考泡泡：灰色大問號 + 哭臉獎盃
    e.append(f'<ellipse cx="700" cy="180" rx="120" ry="100" fill="#E8DDD8" stroke="#8B7B70" stroke-width="6"/>')
    e.append(f'<circle cx="720" cy="90" r="20" fill="#E8DDD8" stroke="#8B7B70" stroke-width="5"/>')
    e.append(f'<circle cx="650" cy="220" r="15" fill="#E8DDD8" stroke="#8B7B70" stroke-width="5"/>')
    # 大「?」
    e.append(svgtext(700, 210, "?", size=120, fill="#8B7B70", weight="bold"))
    # 哭臉獎盃：杯形 + 嘴哭 + 淚（更大更清楚）
    trophy_cx, trophy_cy = 750, 140
    e.append(f'<path d="M {trophy_cx-24} {trophy_cy} L {trophy_cx-32} {trophy_cy+35} L {trophy_cx+32} {trophy_cy+35} L {trophy_cx+24} {trophy_cy} Z" fill="#E8A20C" stroke="#C97E08" stroke-width="4"/>')
    e.append(f'<ellipse cx="{trophy_cx}" cy="{trophy_cy-10}" rx="26" ry="16" fill="#E8A20C" stroke="#C97E08" stroke-width="4"/>')
    e.append(f'<path d="M {trophy_cx-36} {trophy_cy+2} Q {trophy_cx-48} {trophy_cy+22} {trophy_cx-30} {trophy_cy+34}" fill="none" stroke="#C97E08" stroke-width="4" stroke-linecap="round"/>')
    e.append(f'<path d="M {trophy_cx+36} {trophy_cy+2} Q {trophy_cx+48} {trophy_cy+22} {trophy_cx+30} {trophy_cy+34}" fill="none" stroke="#C97E08" stroke-width="4" stroke-linecap="round"/>')
    # 獎盃上的悲傷表情（更大）
    e.append(f'<circle cx="{trophy_cx-8}" cy="{trophy_cy-4}" r="5" fill="#161616"/>')
    e.append(f'<circle cx="{trophy_cx+8}" cy="{trophy_cy-4}" r="5" fill="#161616"/>')
    e.append(f'<path d="M {trophy_cx-10} {trophy_cy+6} Q {trophy_cx} {trophy_cy-2} {trophy_cx+10} {trophy_cy+6}" fill="none" stroke="#161616" stroke-width="3" stroke-linecap="round"/>')
    # 淚水（更大）
    e.append(f'<path d="M {trophy_cx-6} {trophy_cy} Q {trophy_cx-12} {trophy_cy+22} {trophy_cx-2} {trophy_cy+38} Z" fill="#B8E3F2"/>')
    e.append(f'<path d="M {trophy_cx+6} {trophy_cy} Q {trophy_cx+12} {trophy_cy+22} {trophy_cx+2} {trophy_cy+38} Z" fill="#B8E3F2"/>')
    # Owen 背對走向球場（walk pose，從右往左走）
    e.append(boy(pose="walk", expr="think", cx=250, cy=210, scale=1.1, jersey=('100', '#4C7DD0', '#2E5AA8')))
    return svg(W, H, "".join(e))

def scene_p3():
    """p3：打擊區，Owen oh 表情低頭，三張 STRIKE 字卡。"""
    e = []
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#D4C8A8"/>')  # 土地
    # 棒球場線條
    e.append(f'<line x1="594" y1="450" x2="594" y2="80" stroke="#E8D4A0" stroke-width="4" stroke-dasharray="8 8"/>')
    # 三張 STRIKE 字卡（黑底白字，圓角矩形）
    for i, x in enumerate([300, 594, 888]):
        e.append(f'<rect x="{x-50}" y="100" width="100" height="80" rx="12" fill="#2A2320" stroke="#161616" stroke-width="3"/>')
        e.append(svgtext(x, 160, f"STRIKE {i+1}", size=32, fill="#FFFFFF", weight="bold"))
    # Owen 揮棒落空姿勢（swing，後往前）
    e.append(boy(pose="swing", expr="oh", cx=400, cy=210, scale=1.2, jersey=('100', '#4C7DD0', '#2E5AA8')))
    # 球在上方
    e.append(baseball(cx=520, cy=80, r=16))
    return svg(W, H, "".join(e))

def scene_p4():
    """p4 衝動頁：全身 stand，hold 表情，臉頰紅暈、肚子打結繩子、眼角淚、頭上烏雲。"""
    e = []
    # 頭上灰色烏雲
    e.append(cloud(600, 80, 1.2, fill="#AAAAAA", op=0.8))
    # 熱度波浪線（周圍）
    for (x, y) in [(280, 150), (920, 150), (250, 320), (950, 320)]:
        e.append(f'<path d="M {x} {y} q 12 -18 24 0 q 12 18 24 0" fill="none" stroke="#F26B5E" stroke-width="8" stroke-linecap="round"/>')
    # Owen 全身 stand：hold 表情，100 號球衣
    cx, cy, scale = 594, 240, 1.3
    e.append(boy(pose="stand", expr="hold", cx=cx, cy=cy, scale=scale, jersey=('100', '#4C7DD0', '#2E5AA8')))
    # 臉頰紅暈降到 0.25 以下
    e.append(f'<ellipse cx="{cx-60}" cy="{cy+50}" rx="32" ry="22" fill="#FF6B5B" fill-opacity="0.25"/>')
    e.append(f'<ellipse cx="{cx+60}" cy="{cy+50}" rx="32" ry="22" fill="#FF6B5B" fill-opacity="0.25"/>')
    # 肚子位置打結繩子：y ≈ cy+120s 高度（100 號下方）
    rope_y = cy + 120*scale
    e.append(f'<path d="M {cx-60} {rope_y} Q {cx} {rope_y+30} {cx+60} {rope_y}" fill="none" stroke="#8B6B47" stroke-width="12" stroke-linecap="round"/>')
    e.append(f'<path d="M {cx-55} {rope_y+20} Q {cx} {rope_y+5} {cx+55} {rope_y+20}" fill="none" stroke="#8B6B47" stroke-width="12" stroke-linecap="round"/>')
    e.append(f'<path d="M {cx-50} {rope_y+40} Q {cx} {rope_y+25} {cx+50} {rope_y+40}" fill="none" stroke="#8B6B47" stroke-width="12" stroke-linecap="round"/>')
    # 眼角淚
    e.append(f'<ellipse cx="{cx-40}" cy="{cy-20}" rx="5" ry="12" fill="#8FD3F2" stroke="#5AADE8" stroke-width="1"/>')
    e.append(f'<circle cx="{cx-42}" cy="{cy+15}" r="5" fill="#8FD3F2" stroke="#5AADE8" stroke-width="1"/>')
    return svg(W, H, "".join(e))

def scene_p5():
    """p5：紫色星空背景、press 表情深呼吸，胸口發光、字卡 "One more try!"。"""
    e = []
    # 紫色星空背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#6B4B9E"/>')
    # 星星點綴
    for (x, y, r) in [(120, 80, 14), (1050, 100, 18), (200, 420, 12), (1000, 450, 16), (600, 40, 10)]:
        e.append(star(x, y, r, fill="#E8D4A0"))
    e.append(sparkle(350, 150, 12))
    e.append(sparkle(880, 200, 12))
    # Owen 站立，press 表情（深呼吸）
    e.append(boy(pose="stand", expr="press", cx=400, cy=280, scale=1.2, jersey=('100', '#4C7DD0', '#2E5AA8')))
    # 胸口發光效果（多層半透明圓）
    e.append(f'<circle cx="400" cy="340" r="60" fill="#FFD34D" fill-opacity="0.2"/>')
    e.append(f'<circle cx="400" cy="340" r="45" fill="#FFD34D" fill-opacity="0.3"/>')
    e.append(f'<circle cx="400" cy="340" r="30" fill="#FFD34D" fill-opacity="0.4"/>')
    # 發光字卡 "One more try!"
    e.append(f'<rect x="680" y="200" width="420" height="120" rx="16" fill="#E8D4A0" stroke="#D4A880" stroke-width="5"/>')
    e.append(svgtext(900, 270, "One more try!", size=56, fill="#6B4B9E", weight="bold"))
    return svg(W, H, "".join(e))

def scene_p6():
    """p6：Owen 站在打擊準備區：①吸氣（肚子大圓箭頭）②語音泡泡喊口訣③準備揮棒。"""
    e = []
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#D4C8A8"/>')
    # home plate
    e.append(f'<polygon points="594,500 615,475 615,525 594,535 573,525 573,475" fill="#FFFFFF" stroke="#8B6B47" stroke-width="4"/>')
    # ① 吸氣大圓箭頭（肚子位置）
    e.append(f'<circle cx="280" cy="320" r="50" fill="none" stroke="#4C9AFF" stroke-width="6" stroke-dasharray="8 8"/>')
    e.append(f'<polygon points="280,260 270,290 290,290" fill="#4C9AFF"/>')  # 上箭頭
    e.append(svgtext(280, 330, "big breath", size=24, fill="#4C9AFF", weight="bold"))
    # Owen 站立姿勢，準備揮棒
    e.append(boy(pose="stand", expr="press", cx=594, cy=230, scale=1.25, jersey=('100', '#4C7DD0', '#2E5AA8')))
    # ② 語音泡泡喊口訣
    e.append(f'<ellipse cx="850" cy="120" rx="110" ry="70" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="4"/>')
    e.append(f'<polygon points="780,180 760,220 800,200" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')
    e.append(svgtext(850, 135, '"One more try!"', size=28, fill="#4C7DD0", weight="bold"))
    return svg(W, H, "".join(e))

def scene_p7():
    """p7：兩位不具名隊友（kid），一個揮棒落空、一個漏接滾地球，都在笑。"""
    e = []
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#D4C8A8"/>')
    # 兩隊友：kid variant 2（bob girl）
    e.append(kid(variant=2, cx=300, cy=280, scale=1.1, expr="smile"))
    e.append(kid(variant=2, cx=900, cy=280, scale=1.1, expr="smile"))
    # 左邊隊友揮棒姿勢（手臂線條表示揮動）
    e.append(f'<path d="M 250 220 L 150 140" stroke="#FFD9B6" stroke-width="18" stroke-linecap="round"/>')
    e.append(f'<circle cx="130" cy="120" r="11" fill="#FFD9B6"/>')
    # 球在空中，被揮棒落空
    e.append(baseball(cx=200, cy=100, r=14))
    # 右邊隊友漏接姿勢
    e.append(f'<path d="M 850 220 L 950 140" stroke="#FFD9B6" stroke-width="18" stroke-linecap="round"/>')
    e.append(f'<circle cx="970" cy="120" r="11" fill="#FFD9B6"/>')
    # 球滾過去
    e.append(baseball(cx=1000, cy="170", r=14))
    return svg(W, H, "".join(e))

def scene_p8():
    """p8 高潮：上半揮棒 + CRACK 星爆、球飛出；下半菱形跑壘圖 + Owen 沿線跑 + April cheer。"""
    e = []
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#D4C8A8"/>')
    # 上半：Owen swing + bat 對準手位置 + CRACK 星爆
    cx_swing, cy_swing, scale_swing = 200, 180, 1.1
    e.append(boy(pose="swing", expr="big", cx=cx_swing, cy=cy_swing, scale=scale_swing, jersey=('100', '#4C7DD0', '#2E5AA8')))
    # swing 手位置身體座標 (88,80) → 畫面 (cx+88s, cy+50s)；bat 握把對準 (cx+92s, cy+55s)
    bat_x = cx_swing + 92*scale_swing
    bat_y = cy_swing + 55*scale_swing
    e.append(bat(cx=bat_x, cy=bat_y, angle=-50, scale=0.95))
    # CRACK 字與星爆
    crack_x = 380
    e.append(f'<text x="{crack_x}" y="120" font-family="Huninn" font-size="50" font-weight="bold" fill="#E4574C" stroke="#C74338" stroke-width="2">CRACK!</text>')
    # 星爆效果（放射線）
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        x1, y1 = crack_x + 40*math.cos(rad), 90 + 40*math.sin(rad)
        x2, y2 = crack_x + 80*math.cos(rad), 90 + 80*math.sin(rad)
        e.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{STAR_DK}" stroke-width="5" stroke-linecap="round"/>')
    e.append(star(430, 70, 22))
    # 球飛出（baseball + 速度弧線）
    ball_x, ball_y = 530, 100
    e.append(baseball(cx=ball_x, cy=ball_y, r=16))
    e.append(f'<path d="M 450 140 Q 490 100 520 80" fill="none" stroke="#E8A20C" stroke-width="3" stroke-linecap="round"/>')
    e.append(f'<path d="M 460 155 Q 500 115 535 85" fill="none" stroke="#E8A20C" stroke-width="3" stroke-linecap="round"/>')

    # 下半：菱形跑壘圖（放大為主體）
    home_x, home_y = 594, 380
    first_x, first_y = 750, 380
    second_x, second_y = 672, 280
    third_x, third_y = 594, 380

    # 虛線箭頭：home → 一壘 → 二壘 → 三壘 → home
    e.append(f'<line x1="{home_x}" y1="{home_y}" x2="{first_x}" y2="{first_y}" stroke="#8B7B70" stroke-width="4" stroke-dasharray="8 6"/>')
    e.append(f'<polygon points="{first_x+12},{first_y} {first_x-2},{first_y-10} {first_x-2},{first_y+10}" fill="#8B7B70"/>')

    e.append(f'<line x1="{first_x}" y1="{first_y}" x2="{second_x}" y2="{second_y}" stroke="#8B7B70" stroke-width="4" stroke-dasharray="8 6"/>')
    e.append(f'<polygon points="{second_x+10},{second_y-12} {second_x-6},{second_y-2} {second_x+4},{second_y+10}" fill="#8B7B70"/>')

    e.append(f'<line x1="{second_x}" y1="{second_y}" x2="{third_x}" y2="{third_y}" stroke="#8B7B70" stroke-width="4" stroke-dasharray="8 6"/>')
    e.append(f'<polygon points="{third_x-12},{third_y} {third_x+2},{third_y-10} {third_x+2},{third_y+10}" fill="#8B7B70"/>')

    # 本壘板（五邊形）
    e.append(f'<polygon points="{home_x},{home_y-14} {home_x+14},{home_y-6} {home_x+14},{home_y+6} {home_x},{home_y+14} {home_x-14},{home_y+6} {home_x-14},{home_y-6}" fill="#FFFFFF" stroke="#8B6B47" stroke-width="3"/>')
    # 一二三壘（白色方塊）
    e.append(f'<rect x="{first_x-10}" y="{first_y-10}" width="20" height="20" fill="#FFFFFF" stroke="#8B6B47" stroke-width="3"/>')
    e.append(f'<rect x="{second_x-10}" y="{second_y-10}" width="20" height="20" fill="#FFFFFF" stroke="#8B6B47" stroke-width="3"/>')
    e.append(f'<rect x="{third_x-10}" y="{third_y-10}" width="20" height="20" fill="#FFFFFF" stroke="#8B6B47" stroke-width="3"/>')

    # 小 Owen run 在一壘與三壘之間路徑上
    e.append(boy(pose="run", expr="big", cx=700, cy=330, scale=0.65, jersey=('100', '#4C7DD0', '#2E5AA8')))

    # 場邊 April cheer
    e.append(april(cx=1070, cy=220, scale=1.0, pose="cheer"))
    # April 語音泡泡 "Run, Owen, run!"
    e.append(f'<ellipse cx="1070" cy="80" rx="95" ry="55" fill="#FFFFFF" stroke="#D9B3A0" stroke-width="5"/>')
    e.append(f'<polygon points="1020,122 1042,178 1068,128" fill="#FFFFFF" stroke="#D9B3A0" stroke-width="3"/>')
    e.append(f'<ellipse cx="1044" cy="126" rx="26" ry="10" fill="#FFFFFF"/>')  # 蓋掉尾巴與泡泡的接縫
    e.append(svgtext(1070, 100, '"Run, Owen, run!"', size=22, fill="#E4574C", weight="bold"))

    return svg(W, H, "".join(e))

def scene_p9():
    """p9：兩隊球員排隊擊掌（high-five），Owen 面帶微笑，記分板對方分數較高。"""
    e = []
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#D4C8A8"/>')
    # 記分板（上方）
    e.append(f'<rect x="300" y="50" width="600" height="100" rx="10" fill="#2A2320" stroke="#161616" stroke-width="4"/>')
    e.append(svgtext(450, 115, "HOME  3", size=48, fill="#FFFFFF", weight="bold"))
    e.append(svgtext(750, 115, "GUEST  5", size=48, fill="#FFFFFF", weight="bold"))
    # 兩排小孩擊掌
    # 上排（主隊）
    for i, x in enumerate([220, 400, 580]):
        e.append(kid(variant=i%3, cx=x, cy=240, scale=0.9, expr="smile"))
    # 下排（客隊）
    for i, x in enumerate([310, 490, 670]):
        e.append(kid(variant=(i+1)%3, cx=x, cy=340, scale=0.9, expr="smile"))
    # 擊掌手臂線（連接上下排）
    e.append(f'<line x1="220" y1="280" x2="310" y2="300" stroke="#FFD9B6" stroke-width="12" stroke-linecap="round"/>')
    e.append(f'<line x1="400" y1="280" x2="490" y2="300" stroke="#FFD9B6" stroke-width="12" stroke-linecap="round"/>')
    e.append(f'<line x1="580" y1="280" x2="670" y2="300" stroke="#FFD9B6" stroke-width="12" stroke-linecap="round"/>')
    # Owen 中央站立，smile 表情
    e.append(boy(pose="stand", expr="smile", cx=800, cy=240, scale=1.1, jersey=('100', '#4C7DD0', '#2E5AA8')))
    # Owen 跟右邊小孩高五
    e.append(f'<line x1="830" y1="310" x2="930" y2="310" stroke="#FFD9B6" stroke-width="14" stroke-linecap="round"/>')
    e.append(kid(variant=2, cx=970, cy=340, scale=0.9, expr="smile"))
    return svg(W, H, "".join(e))

def scene_p10():
    """p10 英雄頁：Owen 披紅披風站在本壘板上，handup 姿勢舉球棒指天，100 號，滿天星。"""
    e = []
    # 金色地面
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="110" fill="#FFDD7E"/>')
    # 星星點綴（多一些）
    for (x, y, r) in [(140, 100, 18), (1060, 120, 22), (100, 350, 14), (1080, 380, 16), (300, 60, 12), (880, 70, 14), (500, 480, 10), (700, 480, 10)]:
        e.append(star(x, y, r))
    e.append(sparkle(280, 260, 12))
    e.append(sparkle(950, 280, 12))

    # Owen 站在本壘板上，handup 姿勢 + cape + 100 號球衣
    cx, cy, scale = 594, 240, 1.35
    e.append(boy(pose="handup", expr="proud", cx=cx, cy=cy, scale=scale, cape=True, jersey=('100', '#4C7DD0', '#2E5AA8')))

    # 球棒：handup 舉起手身體座標 (74,-64) → 畫面 (cx+74s, cy-94s)
    bat_x = cx + 74*scale
    bat_y = cy - 94*scale
    e.append(bat(cx=bat_x, cy=bat_y, angle=-75, scale=1.0))

    # 五邊形本壘板
    home_x, home_y = cx, cy + 280
    e.append(f'<polygon points="{home_x},{home_y-20} {home_x+20},{home_y-8} {home_x+20},{home_y+8} {home_x},{home_y+20} {home_x-20},{home_y+8} {home_x-20},{home_y-8}" fill="#FFFFFF" stroke="#8B6B47" stroke-width="4"/>')

    return svg(W, H, "".join(e))

def scene_p11():
    """p11：家長頁（Parent Tips）。"""
    e = []
    # 柔和背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#FBF4E8"/>')
    return svg(W, H, "".join(e))

# ----------------PAGE TEXTS ----------------
PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I am number <b>100</b>. I love baseball!'),
    ("p2", scene_p2, 'Game day! My team plays today.<br/>What if we lose?'),
    ("p3", scene_p3, '<b>Strike</b> one! Strike two!<br/>Strike three&mdash;out.'),
    ("p4", scene_p4, 'My face feels hot.<br/>My tummy feels tight.<br/>I want to <b>quit</b> the game!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/><b>One more try!</b>'),
    ("p6", scene_p6, 'I take a big breath.<br/>I say, &ldquo;One more try!&rdquo;<br/>I keep playing.'),
    ("p7", scene_p7, 'My friends miss the ball too.<br/>Everyone misses sometimes.<br/>We still play. We still have fun!'),
    ("p8", scene_p8, '<b>CRACK!</b> Home run!<br/>I run and run&mdash;one, two, three&hellip; HOME!<br/>Mom April cheers, &ldquo;Run, <b>Owen</b>, run!&rdquo;'),
    ("p9", scene_p9, 'My team loses today. That is OK!<br/>We say, &ldquo;Good game!&rdquo;<br/>I still feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Big breath. Keep playing.<br/><b>One more try!</b><br/>I practice every day!'),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("賽前焦慮的標準答案", "他問「輸了會怎樣」，用 p9 的劇本回答：比賽結束、說 Good game、明天再玩。答案每次一致，焦慮才有地方放。"),
    ("不讀書練腳本", "賴皮當下不要拿出書。在賽前的中性時間預演 p5–p6：深呼吸 → 喊口訣 → 繼續玩。"),
    ("p9 是全書鑰匙", "Owen 打出 home run 但球隊輸球——刻意讓「我表現好」和「我們贏了」是兩件事。讀到這頁可以停下來問：Owen, was the game fun today?"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

BOOK = {
    "slug": "one-more-try",
    "order": 3,
    "title_pre": "One More ", "title_hi": "Try", "title_post": "!",
    "title_zh": "再試一次",
    "subtitle": "Owen's baseball story",
    "tagline_zh": "Owen 的棒球故事",
    "chips": ["Social Story", "Baseball", "12 pages"],
    "pdf_name": "One_More_Try.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ['strike', 'quit', 'home run'],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Big breath &rarr; Keep playing &rarr; One more try!</b>&nbsp;"
                 "當他提起比賽中的挫折、或賽前開始問「輸了會怎樣」時，就用這個口訣引導他。"),
    "cover": scene_cover,
}
