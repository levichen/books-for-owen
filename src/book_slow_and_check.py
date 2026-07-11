# -*- coding: utf-8 -*-
"""Book 10: Slow and Check! — 珠心算加速度練習（草稿）。
核心：烏龜吉祥物＋珠算盤＋習題紙＋鉛筆，安裝「一題一題、指著檢查、慢慢寫」的腳本。"""
import math
from parts import *
from book_common import svg, svgtext, TXT, W, H

# soft page palettes
BG = {
    "cover": "#FFE9B8", "p1": "#FFF8E6", "p2": "#FFF3E0", "p3": "#FFFAED",
    "p4": "#FFF5E6", "p5": "#E6DEFF", "p6": "#F0F5FF", "p7": "#E8F2E0",
    "p8": "#FFE9D6", "p9": "#FFF7E0", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

# ============= HELPER FUNCTIONS: TURTLE, ABACUS, WORKSHEET, PENCIL =============

def turtle(cx=0, cy=0, scale=1.0, mood="smile", cape=False):
    """烏龜吉祥物（側面視角，面朝左）：
    殼 rx=60 ry=40 + 殼上 3 個淺色圓斑 + 左側頭（粗頸線連接）+ 瞇瞇眼微笑 + 四隻短腳 + 小尾巴
    mood: smile（微笑）| cheer（左前腳向上舉）| walk（前後腳前後錯開）
    cape: True 時披紅色小披風"""
    SHELL = "#7BC47F"
    SHELL_DK = "#4E9A55"
    SHELL_LIGHT = "#A8D4A0"  # 殼上斑點
    SKIN = "#FFD9B6"
    LINE = "#33291F"

    t = []

    # 殼（橢圓，中心原點）
    t.append(f'<ellipse cx="0" cy="0" rx="60" ry="40" fill="{SHELL}" stroke="{SHELL_DK}" stroke-width="2.5"/>')

    # 殼上 3 個淺色圓斑（三角排列）
    t.append(f'<circle cx="-20" cy="-16" r="10" fill="{SHELL_LIGHT}" fill-opacity="0.8"/>')
    t.append(f'<circle cx="20" cy="-16" r="10" fill="{SHELL_LIGHT}" fill-opacity="0.8"/>')
    t.append(f'<circle cx="0" cy="14" r="10" fill="{SHELL_LIGHT}" fill-opacity="0.75"/>')

    # 頭（圓，r=18，在左側 (-72, -4)）
    t.append(f'<circle cx="-72" cy="-4" r="18" fill="{SKIN}" stroke="{LINE}" stroke-width="1.5"/>')

    # 粗頸線（連接頭和殼）
    t.append(f'<line x1="-54" y1="-6" x2="-60" y2="-2" stroke="{SKIN}" stroke-width="14" stroke-linecap="round"/>')

    # 頭上的臉：瞇瞇眼（兩條下彎小弧）
    t.append(f'<path d="M -78 -8 Q -76 -4 -74 -8" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>')
    t.append(f'<path d="M -70 -8 Q -68 -4 -66 -8" fill="none" stroke="{LINE}" stroke-width="2" stroke-linecap="round"/>')

    # 微笑嘴巴（小弧線）
    t.append(f'<path d="M -78 2 Q -72 6 -66 2" fill="none" stroke="{LINE}" stroke-width="1.5" stroke-linecap="round"/>')

    # 尾巴（小三角在殼右緣 (62, 8)）
    t.append(f'<polygon points="62,8 72,2 72,14" fill="{SHELL_DK}"/>')

    # 四隻腳：短圓角矩形（寬 14 高 18）
    if mood == "cheer":
        # 左前腳（位置 -40）向上舉成圓角矩形
        t.append(f'<rect x="-47" y="0" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')
        # 左後腳
        t.append(f'<rect x="-22" y="28" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')
        # 右前腳
        t.append(f'<rect x="8" y="28" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')
        # 右後腳
        t.append(f'<rect x="33" y="28" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')
    elif mood == "walk":
        # 爬行：前後腳前後錯開
        t.append(f'<rect x="-47" y="26" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')  # 左前腳稍前
        t.append(f'<rect x="-22" y="30" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')  # 左後腳
        t.append(f'<rect x="8" y="30" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')    # 右前腳
        t.append(f'<rect x="33" y="28" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')   # 右後腳稍後
    else:  # smile（正常站立）
        t.append(f'<rect x="-47" y="28" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')  # 左前腳
        t.append(f'<rect x="-22" y="28" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')  # 左後腳
        t.append(f'<rect x="8" y="28" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')   # 右前腳
        t.append(f'<rect x="33" y="28" width="14" height="18" rx="7" fill="{SKIN}" stroke="{LINE}" stroke-width="1"/>')  # 右後腳

    # 披風（若 cape=True）：紅色小披風披在殼上
    if cape:
        # 從殼頂右上方弧形披下來
        t.append(f'<path d="M 20 -30 Q 50 -20 60 10 L 50 15 Q 30 0 15 -25 Z" fill="#E4574C" stroke="#C74338" stroke-width="1.5"/>')

    inner = "".join(t)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def abacus(cx=0, cy=0, scale=1.0):
    """珠算盤：木框＋橫樑＋直桿 5 根＋上珠 1 顆/下珠 4 顆（圓珠兩色）。"""
    FRAME = "#C9A26B"
    FRAME_DK = "#A87D3A"
    ROD = "#8B6F47"
    BEAD_UP = "#F2A9A0"
    BEAD_DOWN = "#6FA8DC"

    a = []

    # 框（木色矩形）
    a.append(f'<rect x="-80" y="-56" width="160" height="112" rx="8" fill="{FRAME}" stroke="{FRAME_DK}" stroke-width="3"/>')

    # 橫樑分隔線
    a.append(f'<line x1="-76" y1="0" x2="76" y2="0" stroke="{FRAME_DK}" stroke-width="3"/>')

    # 5 根直桿（縱向）
    for i, x in enumerate([-48, -24, 0, 24, 48]):
        a.append(f'<line x1="{x}" y1="-50" x2="{x}" y2="46" stroke="{ROD}" stroke-width="2.5"/>')

        # 上珠 1 顆（靠近上邊框）
        a.append(f'<circle cx="{x}" cy="-36" r="8" fill="{BEAD_UP}" stroke="{FRAME_DK}" stroke-width="1.5"/>')

        # 下珠 4 顆（靠近下邊框）
        for j in range(4):
            a.append(f'<circle cx="{x}" cy="{20 + j*10}" r="7" fill="{BEAD_DOWN}" stroke="{FRAME_DK}" stroke-width="1.5"/>')

    inner = "".join(a)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def worksheet(cx=0, cy=0, scale=1.0, marks="x"):
    """習題紙：白紙＋格線＋數字題＋marks: "x"（紅 ✗ 三個）| "o"（紅 ⭕ 一排）| "100"（大大的紅色 100 與圓圈）"""
    PAPER = "#FFFFFF"
    PAPER_LINE = "#E0D7C9"
    TEXT_COLOR = "#4A3B32"
    MARK_RED = "#E4574C"

    w = []

    # 白紙
    w.append(f'<rect x="-70" y="-90" width="140" height="180" rx="6" fill="{PAPER}" stroke="{PAPER_LINE}" stroke-width="2"/>')

    # 格線（4 行＋列）
    for i in range(5):
        y = -80 + i * 40
        w.append(f'<line x1="-62" y1="{y}" x2="62" y2="{y}" stroke="{PAPER_LINE}" stroke-width="1"/>')
    for j in range(3):
        x = -50 + j * 50
        w.append(f'<line x1="{x}" y1="-80" x2="{x}" y2="80" stroke="{PAPER_LINE}" stroke-width="1"/>')

    # 數字題（小字體）
    problems = [
        (-45, -60, "12"),
        (-45, -20, "34"),
        (-45, 20, "56"),
        (5, -60, "78"),
        (5, -20, "90"),
        (5, 20, "45"),
    ]
    for px, py, prob in problems:
        w.append(svgtext(px, py, prob, size=16, fill=TEXT_COLOR, weight="normal"))

    # marks 記號
    if marks == "x":
        # 紅色 ✗ 三個（p4 衝動頁：多個 ✗ 表示寫錯）
        for i, (mx, my) in enumerate([(-45, -60), (-45, -20), (-45, 20)]):
            # 畫 ✗
            w.append(f'<path d="M {mx-8} {my-8} L {mx+8} {my+8}" stroke="{MARK_RED}" stroke-width="3" stroke-linecap="round"/>')
            w.append(f'<path d="M {mx+8} {my-8} L {mx-8} {my+8}" stroke="{MARK_RED}" stroke-width="3" stroke-linecap="round"/>')
    elif marks == "o":
        # 紅色 ⭕ 一排（p8：正確的圓圈）
        for mx, my in [(-45, -60), (-45, -20), (-45, 20)]:
            w.append(f'<circle cx="{mx}" cy="{my}" r="10" fill="none" stroke="{MARK_RED}" stroke-width="2.5"/>')
    elif marks == "100":
        # 大大的紅色 100 與圓圈（p9 的 100 分特寫）
        w.append(f'<text x="0" y="20" font-family="Huninn" font-size="48" font-weight="bold" fill="{MARK_RED}" text-anchor="middle">100</text>')
        w.append(f'<circle cx="0" cy="55" r="28" fill="none" stroke="{MARK_RED}" stroke-width="3"/>')

    inner = "".join(w)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def pencil(cx=0, cy=0, angle=0, scale=1.0):
    """鉛筆：黃桿＋粉紅擦頭＋筆尖（簡單三段）。angle 為旋轉角（度）。"""
    BARREL = "#F2D146"
    ERASER = "#F2A9A0"
    TIP = "#8B6F47"

    p = []
    # 黃桿（長矩形）
    p.append(f'<rect x="-3" y="-60" width="6" height="96" rx="3" fill="{BARREL}"/>')
    # 粉紅擦頭（右上端）
    p.append(f'<rect x="-4" y="-68" width="8" height="10" rx="3" fill="{ERASER}"/>')
    # 筆尖（左下端，小三角）
    p.append(f'<polygon points="-2,-4 2,-4 0,-14" fill="{TIP}"/>')
    # 金屬套筒（介於擦頭和筆尖）
    p.append(f'<rect x="-3.5" y="-6" width="7" height="4" fill="#C9BFA8"/>')

    inner = "".join(p)
    return f'<g transform="translate({cx},{cy}) rotate({angle}) scale({scale})">{inner}</g>'


# ============= SCENES =============

def scene_cover():
    """封面：Owen 坐書桌（bust＋desk）＋烏龜在桌上（趴著、頭朝 Owen）＋算盤＋暖晨光＋有框窗戶"""
    e = []

    # 背景色
    e.append(f'<rect x="0" y="0" width="1188" height="620" fill="{BG['cover']}"/>')

    # 窗戶（右上，有框）
    e.append(f'<rect x="850" y="30" width="300" height="220" rx="14" fill="#B8E5F8" stroke="#8FC4E6" stroke-width="4"/>')
    e.append(f'<line x1="1000" y1="30" x2="1000" y2="250" stroke="#8FC4E6" stroke-width="2"/>')
    e.append(f'<line x1="850" y1="130" x2="1150" y2="130" stroke="#8FC4E6" stroke-width="2"/>')

    # 晨光斜帶（半透明黃色）
    e.append(f'<polygon points="1188,0 1188,160 820,620 1188,620" fill="#FFF8DC" fill-opacity="0.25"/>')

    # 牆壁背景（下方）
    e.append(f'<rect x="0" y="300" width="1188" height="320" fill="#E8D2AC"/>')

    # 書桌（desk API）
    e.append(desk(cx=594, cy=490, w=380, scale=1.15))

    # 桌上的習題紙（背景）
    e.append(f'<rect x="480" y="380" width="90" height="75" rx="5" fill="#FFFFFF" stroke="#DDD3C2" stroke-width="1.5"/>')
    for i in range(3):
        y = 395 + i * 25
        e.append(f'<line x1="495" y1="{y}" x2="555" y2="{y}" stroke="#DDD3C2" stroke-width="0.8"/>')

    # 珠算盤（在習題紙右方）
    e.append(abacus(cx=680, cy=390, scale=0.9))

    # 鉛筆（斜放在桌上）
    e.append(pencil(cx=750, cy=340, angle=-30, scale=1.3))

    # Owen（bust 坐在桌前左側，smile 表情）
    e.append(boy_bust(expr="smile", cx=320, cy=350, scale=1.25))

    # 烏龜在桌上（趴著，頭朝 Owen 左邊）
    # 為了讓烏龜看起來趴著，我們用 scale 稍微壓平它，並調整 y 位置
    e.append(turtle(cx=500, cy=430, scale=1.0, mood="smile"))

    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """早晨書房：Owen 坐書桌（bust＋desk），桌上習題紙、鉛筆、珠算盤，窗外晨光"""
    e = []

    # 背景色
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG['p1']}"/>')

    # 窗戶（右上，晨光進來）
    e.append(f'<rect x="900" y="40" width="240" height="200" rx="12" fill="#B8E5F8" stroke="#8FC4E6" stroke-width="3"/>')
    e.append(f'<line x1="1020" y1="40" x2="1020" y2="240" stroke="#8FC4E6" stroke-width="2"/>')
    e.append(f'<line x1="900" y1="120" x2="1140" y2="120" stroke="#8FC4E6" stroke-width="2"/>')

    # 晨光斜線（半透明黃矩形表示光線）
    e.append(f'<polygon points="1188,0 1188,140 850,560 1188,560" fill="#FFF8DC" fill-opacity="0.25"/>')

    # 牆壁（暖奶油色）
    e.append(f'<rect x="0" y="240" width="1188" height="320" fill="#E8D2AC"/>')

    # 書桌
    e.append(desk(cx=594, cy=440, w=380, scale=1.15))

    # 桌上物品：習題紙、珠算盤、鉛筆
    e.append(f'<rect x="450" y="340" width="100" height="80" rx="4" fill="#FFFFFF" stroke="#DDD3C2" stroke-width="1.5"/>')
    for i in range(4):
        y = 350 + i * 20
        e.append(f'<line x1="460" y1="{y}" x2="540" y2="{y}" stroke="#DDD3C2" stroke-width="0.8"/>')

    # 珠算盤
    e.append(abacus(cx=700, cy=360, scale=0.85))

    # 鉛筆（斜放在習題紙上）
    e.append(pencil(cx=620, cy=300, angle=-20, scale=1.0))

    # Owen（bust 微笑坐在桌前）
    e.append(boy_bust(expr="smile", cx=420, cy=320, scale=1.15))

    # 小星星點綴
    e.append(star(200, 80, 14))
    e.append(star(1000, 100, 12))
    e.append(sparkle(300, 150, 10))

    return svg(W, H, "".join(e))


def scene_p2():
    """珠算盤特寫（珠子撥動的小弧線）＋Owen 微笑寫字"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG['p2']}"/>')

    # 背景地板
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D9B98C"/>')

    # 珠算盤特寫（大一點，中間）
    e.append(abacus(cx=594, cy=200, scale=1.4))

    # 珠子撥動的弧線（表示動作）
    for i in range(3):
        y = 120 + i * 40
        e.append(f'<path d="M 480 {y} Q 550 {y-15} 620 {y}" fill="none" stroke="#F2D146" stroke-width="3" stroke-dasharray="3 5" stroke-linecap="round"/>')

    # Owen 坐在右側（bust，寫字姿勢）
    e.append(boy_bust(expr="smile", cx=900, cy=310, scale=1.1, arms="desk"))
    e.append(desk(cx=900, cy=420, w=240, scale=0.95))

    # 小星星
    e.append(star(150, 100, 16))
    e.append(star(1050, 150, 14))

    return svg(W, H, "".join(e))


def scene_p3():
    """Owen 特寫（star 表情），盯著習題紙最後一題，頭上思考泡泡：畫著「FINISH」旗子"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG['p3']}"/>')
    e.append(f'<rect x="0" y="420" width="1188" height="140" fill="#E8D2AC"/>')

    # 習題紙特寫（左側）
    e.append(f'<rect x="120" y="240" width="140" height="160" rx="6" fill="#FFFFFF" stroke="#DDD3C2" stroke-width="2"/>')
    for i in range(5):
        y = 260 + i * 30
        e.append(f'<line x1="135" y1="{y}" x2="245" y2="{y}" stroke="#DDD3C2" stroke-width="1"/>')

    # 習題（小字）
    for i, (py, prob) in enumerate([(260, "12"), (290, "34"), (320, "56"), (350, "78"), (380, "90")]):
        e.append(svgtext(160, py, prob, size=12, fill=TXT))

    # Owen bust（中央，star 表情，興奮地看著習題紙）
    e.append(boy_bust(expr="star", cx=594, cy=310, scale=1.35))

    # 思考泡泡（頭上方）
    bubble = f'<ellipse cx="750" cy="140" rx="110" ry="70" fill="#FFFFFF" stroke="#D7C7AD" stroke-width="4"/>'
    e.append(bubble)

    # 泡泡尾巴（指向 Owen 的頭）
    e.append(f'<path d="M 700 200 L 680 260 L 720 240 Z" fill="#FFFFFF" stroke="#D7C7AD" stroke-width="2"/>')

    # FINISH 旗子（在泡泡內）
    e.append(f'<rect x="710" y="110" width="3" height="50" fill="#4A3B32"/>')  # 旗桿
    e.append(f'<polygon points="713,110 713,130 760,120" fill="#E4574C"/>')  # 旗子
    e.append(svgtext(800, 155, "FINISH!", size=28, fill="#D97706", weight="bold"))

    # 背景點綴
    e.append(star(200, 80, 18))
    e.append(star(1050, 100, 16))
    e.append(sparkle(350, 120, 12))

    return svg(W, H, "".join(e))


def scene_p4():
    """衝動頁：Owen 的手和鉛筆畫殘影與煙線（狂寫），習題紙上紅色 ✗✗✗ 越來越多，一顆汗滴"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG['p4']}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#E8D2AC"/>')

    # 背景：熱線（衝動感）
    for (x, y) in [(250, 100), (950, 120), (200, 300), (1000, 280)]:
        e.append(f'<path d="M {x} {y} q 12 -18 24 0 q 12 18 24 0" fill="none" stroke="#F26B5E" stroke-width="6" stroke-linecap="round"/>')

    # 習題紙（左側，有多個 ✗ 記號）
    e.append(f'<rect x="140" y="300" width="120" height="100" rx="5" fill="#FFFFFF" stroke="#DDD3C2" stroke-width="1.5"/>')
    for i in range(4):
        y = 315 + i * 20
        e.append(f'<line x1="155" y1="{y}" x2="245" y2="{y}" stroke="#DDD3C2" stroke-width="0.8"/>')

    # 習題紙上的 ✗✗✗ 記號（紅色，越來越多 = 狂寫）
    for i, (mx, my) in enumerate([(180, 320), (200, 340), (190, 360), (210, 380)]):
        e.append(f'<path d="M {mx-6} {my-6} L {mx+6} {my+6}" stroke="#E4574C" stroke-width="3" stroke-linecap="round"/>')
        e.append(f'<path d="M {mx+6} {my-6} L {mx-6} {my+6}" stroke="#E4574C" stroke-width="3" stroke-linecap="round"/>')

    # Owen bust（中央，hold 表情 = 憋著衝動）
    e.append(boy_bust(expr="hold", cx=594, cy=310, scale=1.45))

    # 鉛筆殘影（3 條平行虛影線，表示筆的高速）
    for offset in [60, 100, 140]:
        e.append(f'<path d="M {594+offset} 200 L {594+offset+30} 380" fill="none" stroke="#F2D146" stroke-width="3" stroke-dasharray="4 8" stroke-opacity="0.5"/>')

    # 手部速度線
    for dx, dy in [(-40, 100), (-20, 120), (10, 140)]:
        e.append(f'<line x1="{594+dx*0.8:.0f}" y1="{320+dy*0.5:.0f}" x2="{594+dx}" y2="{320+dy}" stroke="#F26B5E" stroke-width="4" stroke-linecap="round"/>')

    # 汗滴（在頭旁）
    e.append(f'<path d="M 700 160 q 10 20 0 26 q -10 -6 0 -26 Z" fill="#8FD3F2"/>')

    # 心臟（衝動的表現）
    e.append(f'<path d="M 950 280 c 0 -24 34 -24 34 -2 c 0 -22 34 -22 34 2 c 0 24 -34 36 -34 48 c 0 -12 -34 -24 -34 -48 Z" fill="#E4574C" stroke="#C74338" stroke-width="3"/>')

    return svg(W, H, "".join(e))


def scene_p5():
    """紫色星空背景：Owen（press 表情）＋綠色烏龜吉祥物發光登場（微笑、慢慢爬），Owen 手放胸口"""
    e = []

    # 紫色星空背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#E6DEFF"/>')

    # 星星點綴（各種大小）
    for (x, y, r) in [(120, 100, 18), (1050, 130, 20), (180, 400, 14), (980, 380, 16), (300, 60, 12), (900, 80, 14)]:
        e.append(star(x, y, r, fill="#FFE8B6"))
    e.append(sparkle(250, 150, 12))
    e.append(sparkle(950, 200, 12))

    # 烏龜發光登場（多層半透明綠/金圓）
    e.append(f'<circle cx="800" cy="280" r="120" fill="#7BC47F" fill-opacity="0.12"/>')
    e.append(f'<circle cx="800" cy="280" r="90" fill="#FFE8B6" fill-opacity="0.15"/>')
    e.append(f'<circle cx="800" cy="280" r="60" fill="#7BC47F" fill-opacity="0.18"/>')

    # 烏龜本體（發光登場）
    e.append(turtle(cx=800, cy=280, scale=1.1, mood="smile"))

    # Owen（press 表情，手放胸口）
    e.append(boy(pose="stand", expr="press", cx=350, cy=240, scale=1.2))

    # 背景地面
    e.append(f'<ellipse cx="594" cy="520" rx="500" ry="80" fill="#D9C4B8" fill-opacity="0.4"/>')

    return svg(W, H, "".join(e))


def scene_p6():
    """三步腳本三格（有分格框）：①習題紙圈一題②手指點題③烏龜 cheer，三格內容填滿框"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG['p6']}"/>')
    e.append(f'<rect x="0" y="450" width="1188" height="110" fill="#B8D4F0"/>')

    # 三格佈局（並排）：每格寬約 320px
    frame_width = 320
    frame_height = 280
    frame_y = 80

    # ===== 第一格：習題紙圈一題 =====
    x1 = 120
    frame_x1 = x1 - frame_width//2

    # 分格框（圓角矩形）
    e.append(f'<rect x="{frame_x1}" y="{frame_y}" width="{frame_width}" height="{frame_height}" rx="12" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')

    # 習題紙在格內（放大）
    e.append(f'<rect x="{x1-55}" y="110" width="110" height="140" rx="4" fill="#FFFEF5" stroke="#DDD3C2" stroke-width="1.5"/>')
    # 5 題（其中第 2 題被圈住）
    for i in range(5):
        y_pos = 128 + i * 24
        fill_op = "0.3" if i != 1 else "1.0"
        e.append(f'<text x="{x1}" y="{y_pos}" font-family="Huninn" font-size="18" fill="{TXT}" text-anchor="middle" fill-opacity="{fill_op}">12+34</text>')

    # 圓圈圈住第 2 題（黃色）
    e.append(f'<circle cx="{x1}" cy="152" r="22" fill="none" stroke="#F2D146" stroke-width="3"/>')

    # 格底標籤
    e.append(svgtext(x1, 300, "One at a time", size=18, fill=STAR_DK, weight="bold"))

    # ===== 第二格：手指點題 =====
    x2 = 594
    frame_x2 = x2 - frame_width//2

    # 分格框
    e.append(f'<rect x="{frame_x2}" y="{frame_y}" width="{frame_width}" height="{frame_height}" rx="12" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')

    # 習題紙在格內
    e.append(f'<rect x="{x2-60}" y="110" width="120" height="150" rx="4" fill="#FFFEF5" stroke="#DDD3C2" stroke-width="1.5"/>')
    # 3 題
    problems = ["12+34", "56+78", "90+45"]
    for i, prob in enumerate(problems):
        y_pos = 135 + i * 45
        e.append(svgtext(x2, y_pos, prob, size=20, fill=TXT, weight="normal"))

    # 手指點著題目（簡單圖示）
    e.append(f'<circle cx="{x2-45}" cy="135" r="6" fill="#FFD9B6"/>')  # 指節
    e.append(f'<circle cx="{x2-50}" cy="128" r="3" fill="#FFE8B6"/>')  # 指尖光點

    # 格底標籤
    e.append(svgtext(x2, 300, "Point and check", size=18, fill=STAR_DK, weight="bold"))

    # ===== 第三格：烏龜 cheer =====
    x3 = 1068
    frame_x3 = x3 - frame_width//2

    # 分格框
    e.append(f'<rect x="{frame_x3}" y="{frame_y}" width="{frame_width}" height="{frame_height}" rx="12" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')

    # 烏龜在格內中央（放大）
    e.append(turtle(cx=x3, cy=190, scale=1.2, mood="cheer"))

    # 格底標籤
    e.append(svgtext(x3, 300, "Slow hands win!", size=18, fill=STAR_DK, weight="bold"))

    return svg(W, H, "".join(e))


def scene_p7():
    """觀點頁：烏龜一步一步爬向終點旗（每一步留下一個打勾腳印），April 在終點微笑拍手"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG['p7']}"/>')
    e.append(f'<rect x="0" y="420" width="1188" height="140" fill="#BFD9EE"/>')

    # 烏龜爬行路徑（S 形曲線）
    path_points = [(200, 350), (350, 320), (500, 340), (650, 310), (800, 330), (950, 300)]

    # 烏龜的腳印（綠色打勾 ✓）
    for i, (px, py) in enumerate(path_points[:-1]):
        # 打勾腳印（小 ✓）
        e.append(f'<path d="M {px-4} {py} Q {px} {py+4} {px+6} {py-2}" fill="none" stroke="#7BC47F" stroke-width="2.5" stroke-linecap="round"/>')

    # 終點旗子
    last_x, last_y = path_points[-1]
    e.append(f'<line x1="{last_x}" y1="{last_y-30}" x2="{last_x}" y2="{last_y+20}" stroke="#4A3B32" stroke-width="3"/>')
    e.append(f'<polygon points="{last_x},{last_y-30} {last_x},{last_y-10} {last_x+30},{last_y-20}" fill="#E4574C"/>')

    # 烏龜（walk 姿勢，爬到終點旁；水平鏡像讓頭朝右、面向終點與 April）
    tx, ty = last_x-70, last_y+30
    e.append(f'<g transform="translate({2*tx},0) scale(-1,1)">{turtle(cx=tx, cy=ty, scale=1.05, mood="walk")}</g>')

    # April（在終點拍手，wave 姿勢 = 揮手）
    e.append(april(cx=last_x+80, cy=280, scale=1.0, pose="cheer"))

    return svg(W, H, "".join(e))


def scene_p8():
    """April 拿著習題紙檢查，紙上一排紅色 ⭕⭕⭕，語音泡泡 "Wow, Owen! Super slow hands!"，Owen 挺胸"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG['p8']}"/>')
    e.append(f'<rect x="0" y="420" width="1188" height="140" fill="#D9B98C"/>')

    # 習題紙（April 拿著，有 ⭕ 記號）
    e.append(worksheet(cx=280, cy=240, scale=1.1, marks="o"))

    # April（右側，拿著習題紙）
    e.append(april(cx=750, cy=280, scale=1.0, pose="stand"))

    # 語音泡泡
    bubble = f'<ellipse cx="550" cy="100" rx="140" ry="80" fill="#FFFFFF" stroke="#D7C7AD" stroke-width="4"/>'
    e.append(bubble)
    e.append(f'<path d="M 480 160 L 450 220 L 500 180 Z" fill="#FFFFFF" stroke="#D7C7AD" stroke-width="2"/>')

    # 泡泡內文字
    e.append(svgtext(550, 80, "Wow, Owen!", size=22, fill="#D97706", weight="bold"))
    e.append(svgtext(550, 110, "Super slow hands!", size=18, fill="#D97706"))

    # Owen（左側，bust 挺胸）
    e.append(boy_bust(expr="proud", cx=350, cy=320, scale=1.15))

    return svg(W, H, "".join(e))


def scene_p9():
    """習題紙特寫：大大的紅色 100 分＋圈圈，Owen 舉起雙手歡呼，烏龜在桌上跟著開心"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG['p9']}"/>')
    e.append(f'<rect x="0" y="420" width="1188" height="140" fill="#E8D2AC"/>')

    # 習題紙特寫（中央偏左）
    e.append(worksheet(cx=350, cy=240, scale=1.6, marks="100"))

    # Owen（jump 歡呼，右側）
    e.append(boy(pose="jump", expr="big", cx=850, cy=200, scale=1.25))

    # 烏龜開心（cheer 姿勢，在習題紙旁）
    e.append(turtle(cx=550, cy=380, scale=1.1, mood="cheer"))

    # 背景點綴（五彩紙屑）
    import random
    random.seed(8)
    cols = ["#F6C445", "#7BC47F", "#6FA8DC", "#F49AB5", "#E4574C"]
    for i in range(20):
        x, y = random.randint(100, 1000), random.randint(50, 350)
        c = cols[i % 5]
        e.append(f'<rect x="{x}" y="{y}" width="10" height="16" rx="3" fill="{c}" transform="rotate({random.randint(-45,45)} {x} {y})"/>')

    return svg(W, H, "".join(e))


def scene_p10():
    """英雄收尾：Owen 披紅披風叉腰，烏龜披迷你披風在旁，桌上發光的 100 分習題紙，滿天星"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG['p10']}"/>')

    # 背景地面
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="100" fill="#FFDD7E"/>')

    # 滿天星
    for (x, y, r) in [(140, 100, 20), (1050, 120, 22), (180, 400, 14), (1000, 380, 16), (320, 60, 12), (870, 70, 14)]:
        e.append(star(x, y, r))
    e.append(sparkle(260, 240, 12))
    e.append(sparkle(930, 240, 12))

    # 發光的 100 分習題紙（書桌上，中央背景）
    e.append(f'<circle cx="594" cy="280" r="100" fill="{STAR_Y}" fill-opacity="0.15"/>')
    e.append(f'<circle cx="594" cy="280" r="70" fill="{STAR_Y}" fill-opacity="0.2"/>')
    e.append(worksheet(cx=594, cy=280, scale=1.3, marks="100"))

    # Owen（hips 英雄姿勢 + cape）
    e.append(boy(pose="hips", expr="proud", cx=380, cy=180, scale=1.3, cape=True))

    # 烏龜（英雄姿勢，也披迷你披風）
    e.append(turtle(cx=780, cy=240, scale=1.15, mood="cheer", cape=True))

    return svg(W, H, "".join(e))


# ============= PAGE TEXTS ================

PAGES = [
    # 封面不屬於 PAGES——渲染器會用 BOOK["cover"] 另行處理；塞進來會多出一頁
    ("p1", scene_p1, "This is me, <b>Owen</b>!<br/>Every morning, I do math."),
    ("p2", scene_p2, "Math time! Click, click!<br/>I write my numbers."),
    ("p3", scene_p3, "I want to finish <b>FAST</b>!<br/>Fast feels like winning!"),
    ("p4", scene_p4, "My pencil <b>zooms</b>!<br/>My heart goes fast, fast!<br/>Oops&mdash;wrong, wrong, wrong!"),
    ("p5", scene_p5, "<b>STOP!</b> I use my superpower&hellip;<br/>I am a <b>turtle</b>!"),
    ("p6", scene_p6, "One at a time.<br/>Point and <b>check</b>.<br/>Slow hands win!"),
    ("p7", scene_p7, "My turtle checks each step.<br/>Careful work makes Mommy smile.<br/>Slow and right feels good!"),
    ("p8", scene_p8, "Mommy April checks my page.<br/>So many right marks!<br/>&ldquo;Wow, <b>Owen</b>! Super slow hands!&rdquo;"),
    ("p9", scene_p9, "All right! One hundred!<br/>I feel <b>GREAT</b>!"),
    ("p10", scene_p10, "One at a time. Point and check.<br/><b>Slow and check!</b><br/>I practice every day!"),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("稱讚慢不稱讚快", "檢查作業時把稱讚點從「寫完了」移到「這題你有慢慢寫」「這題你有用手指檢查」——強化過程不強化速度。"),
    ("正確率可視化", "和他一起數今天的 ⭕ 數量並記在小表上，跟「昨天的自己」比，不跟別人比；p9 的 100 分是願景不是每日標準。"),
    ("當他主動說『My pencil zooms』", "或自己放慢重寫 = 察覺訊號，大力稱讚。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

BOOK = {
    "slug": "slow-and-check",
    "order": 10,
    "title_pre": "", "title_hi": "Slow", "title_post": " and Check!",
    "title_zh": "慢慢寫，檢查看",
    "subtitle": "Owen's math story",
    "tagline_zh": "Owen 的珠心算故事",
    "chips": ["Social Story", "Math", "12 pages"],
    "pdf_name": "Slow_And_Check.pdf",
    "bg": BG,
    "pages": PAGES,
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>One at a time &rarr; Point and check &rarr; Slow and check!</b>&nbsp;"
                 "當他主動說出 &ldquo;My pencil zooms&rdquo;（我的筆狂飆了）或自己放慢重寫時，"
                 "就是最值得大力稱讚的察覺時刻。"),
    "cover": scene_cover,
}
