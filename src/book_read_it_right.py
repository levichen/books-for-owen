# -*- coding: utf-8 -*-
"""Book 16: Read It Right! — 珠心算計時比賽練習（草稿）。
核心：貓頭鷹吉祥物（大眼睛象徵看清楚）＋計時器＋習題紙，安裝「看清一次寫對」的比賽腳本。
口訣：Owl eyes on → Read it right → Write it once!"""
import math
from parts import *
from book_common import svg, svgtext, TXT, W, H

# soft page palettes
BG = {
    "cover": "#FFE9A8", "p1": "#FFFBF0", "p2": "#FFF5E6", "p3": "#FFFCF4",
    "p4": "#FFE8D0", "p5": "#E6DEFF", "p6": "#F5F0FF", "p7": "#E8F5E0",
    "p8": "#FFF0D6", "p9": "#FFF8E6", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

# ============= OWL MASCOT =============

def owl(cx=0, cy=0, scale=1.0, mood="watch", cape=False):
    """貓頭鷹吉祥物：棕色圓身＋淺色肚皮＋兩顆大圓眼（黑框白底大瞳孔）＋小三角嘴＋頭頂耳羽＋短翅。
    mood: watch（靜停）| nod（頭部微前傾）| cheer（翅膀上舉）| fly（展翅 + 身體微傾）
    cape: True 時披迷你紅披風"""
    OWL_BODY = "#8B6B47"
    OWL_DK = "#5C4A31"
    OWL_BELLY = "#E8D5B8"
    OWL_EYE_W = "#FFFFFF"
    OWL_PUPIL = "#1A1A1A"

    o = []

    # 身體：棕色橢圓（中心原點）
    o.append(f'<ellipse cx="0" cy="0" rx="34" ry="42" fill="{OWL_BODY}" stroke="{OWL_DK}" stroke-width="2.5"/>')

    # 肚皮：淺色橢圓
    o.append(f'<ellipse cx="0" cy="10" rx="20" ry="26" fill="{OWL_BELLY}" fill-opacity="0.95"/>')

    # 肚皮羽紋（V 形線）
    o.append(f'<path d="M -10 0 L 0 8 L 10 0" fill="none" stroke="{OWL_DK}" stroke-width="1.5" stroke-linecap="round"/>')
    o.append(f'<path d="M -8 12 L 0 18 L 8 12" fill="none" stroke="{OWL_DK}" stroke-width="1.5" stroke-linecap="round"/>')

    # 兩顆大圓眼（白圓 + 黑框 + 大瞳孔）
    # 左眼
    o.append(f'<circle cx="-13" cy="-18" r="13" fill="{OWL_EYE_W}" stroke="{OWL_DK}" stroke-width="3"/>')
    o.append(f'<circle cx="-13" cy="-18" r="6" fill="{OWL_PUPIL}"/>')
    o.append(f'<circle cx="-11" cy="-20" r="1.5" fill="#FFFFFF"/>')  # 眼睛反光

    # 右眼
    o.append(f'<circle cx="13" cy="-18" r="13" fill="{OWL_EYE_W}" stroke="{OWL_DK}" stroke-width="3"/>')
    o.append(f'<circle cx="13" cy="-18" r="6" fill="{OWL_PUPIL}"/>')
    o.append(f'<circle cx="15" cy="-20" r="1.5" fill="#FFFFFF"/>')  # 眼睛反光

    # 小三角嘴（向下）
    o.append(f'<polygon points="0,-6 -3,-2 3,-2" fill="{OWL_DK}"/>')

    # 頭頂耳羽（兩個小三角）
    o.append(f'<polygon points="-16,-40 -22,-52 -10,-44" fill="{OWL_BODY}" stroke="{OWL_DK}" stroke-width="1.5"/>')
    o.append(f'<polygon points="16,-40 22,-52 10,-44" fill="{OWL_BODY}" stroke="{OWL_DK}" stroke-width="1.5"/>')

    # 短翅（兩側小橢圓，mood 決定位置和角度）
    if mood == "fly":
        # 展翅飛行：翅膀橫向展開
        o.append(f'<ellipse cx="-38" cy="-8" rx="12" ry="24" fill="{OWL_BODY}" stroke="{OWL_DK}" stroke-width="2" transform="rotate(-35 -38 -8)"/>')
        o.append(f'<ellipse cx="38" cy="-8" rx="12" ry="24" fill="{OWL_BODY}" stroke="{OWL_DK}" stroke-width="2" transform="rotate(35 38 -8)"/>')
    elif mood == "cheer":
        # 翅膀上舉（開心）
        o.append(f'<ellipse cx="-32" cy="-30" rx="10" ry="20" fill="{OWL_BODY}" stroke="{OWL_DK}" stroke-width="2"/>')
        o.append(f'<ellipse cx="32" cy="-30" rx="10" ry="20" fill="{OWL_BODY}" stroke="{OWL_DK}" stroke-width="2"/>')
    else:
        # watch 和 nod：翅膀放在身體兩側
        o.append(f'<ellipse cx="-34" cy="2" rx="10" ry="18" fill="{OWL_BODY}" stroke="{OWL_DK}" stroke-width="2"/>')
        o.append(f'<ellipse cx="34" cy="2" rx="10" ry="18" fill="{OWL_BODY}" stroke="{OWL_DK}" stroke-width="2"/>')

    # 短腳（兩條短線＋爪）
    o.append(f'<line x1="-10" y1="42" x2="-10" y2="52" stroke="{OWL_DK}" stroke-width="2" stroke-linecap="round"/>')
    o.append(f'<line x1="10" y1="42" x2="10" y2="52" stroke="{OWL_DK}" stroke-width="2" stroke-linecap="round"/>')

    # 爪（小叉線）
    o.append(f'<path d="M -12 52 L -10 56 L -8 52" fill="none" stroke="{OWL_DK}" stroke-width="1.5" stroke-linecap="round"/>')
    o.append(f'<path d="M 8 52 L 10 56 L 12 52" fill="none" stroke="{OWL_DK}" stroke-width="1.5" stroke-linecap="round"/>')

    # 披風（若 cape=True）
    if cape:
        o.append(f'<path d="M -22 -8 Q -40 15 -26 48 L 26 48 Q 40 15 22 -8 Z" fill="#E4574C" stroke="#C74338" stroke-width="1.5"/>')

    # mood 為 nod 時，整體微前傾
    transform = f'rotate(8)'  if mood == "nod" else ""
    inner = "".join(o)
    if transform:
        return f'<g transform="translate({cx},{cy}) scale({scale}) {transform}">{inner}</g>'
    else:
        return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


# ============= TIMER AND WORKSHEET HELPERS =============

def timer_stopwatch(cx=0, cy=0, scale=1.0, time_text="2:00", glow=False):
    """圓形碼表：圓面＋中心鈕＋指針。time_text 為顯示的時間。"""
    t = []

    # 發光光暈（若 glow=True）
    if glow:
        t.append(f'<circle cx="0" cy="0" r="80" fill="{STAR_Y}" fill-opacity="0.2"/>')
        t.append(f'<circle cx="0" cy="0" r="60" fill="{STAR_Y}" fill-opacity="0.15"/>')

    # 碼表外殼（淺灰圓形）
    t.append(f'<circle cx="0" cy="0" r="56" fill="#E8E0D4" stroke="#B8A89C" stroke-width="3"/>')

    # 刻度標記（12, 3, 6, 9 點）
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        x1 = 50 * math.cos(rad)
        y1 = 50 * math.sin(rad)
        x2 = 44 * math.cos(rad)
        y2 = 44 * math.sin(rad)
        t.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#4A3B32" stroke-width="3"/>')

    # 中心小點
    t.append(f'<circle cx="0" cy="0" r="4" fill="#4A3B32"/>')

    # 時間顯示（在碟面中央）
    t.append(svgtext(0, 8, time_text, size=22, fill="#E4574C", weight="bold", anchor="middle"))

    # 頂部鈕
    t.append(f'<rect x="-8" y="-64" width="16" height="10" rx="5" fill="#B8A89C" stroke="#8B7B6F" stroke-width="1.5"/>')

    inner = "".join(t)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def worksheet_contest(cx=0, cy=0, scale=1.0, marks="none"):
    """比賽習題紙：白紙＋密集格線＋數字題＋marks: "none"（空白）| "x"（紅✗ 多個）| "check"（綠勾）"""
    w = []

    # 白紙（稍大，表示比賽版）
    w.append(f'<rect x="-85" y="-100" width="170" height="200" rx="6" fill="#FFFFFF" stroke="#E0D4C4" stroke-width="2"/>')

    # 密集格線（兩欄，更多題）
    # 左欄
    for i in range(6):
        y = -85 + i * 30
        w.append(f'<line x1="-78" y1="{y}" x2="-8" y2="{y}" stroke="#E8DCC9" stroke-width="0.8"/>')

    # 右欄
    for i in range(6):
        y = -85 + i * 30
        w.append(f'<line x1="-2" y1="{y}" x2="68" y2="{y}" stroke="#E8DCC9" stroke-width="0.8"/>')

    # 中間分欄線
    w.append(f'<line x1="-4" y1="-90" x2="-4" y2="90" stroke="#D0C0B0" stroke-width="1"/>')

    # 數字題（小字，兩欄）
    left_probs = ["12", "34", "56", "78", "90", "45"]
    right_probs = ["23", "45", "67", "89", "12", "34"]

    for i, (lp, rp) in enumerate(zip(left_probs, right_probs)):
        y = -78 + i * 30
        w.append(svgtext(-43, y, lp, size=13, fill=TXT, weight="normal"))
        w.append(svgtext(31, y, rp, size=13, fill=TXT, weight="normal"))

    # 標記
    if marks == "x":
        # 多個紅 ✗（表示寫錯）
        for i in range(3):
            y = -60 + i * 35
            mx, my = -43, y
            w.append(f'<path d="M {mx-5} {my-5} L {mx+5} {my+5}" stroke="#E4574C" stroke-width="3" stroke-linecap="round"/>')
            w.append(f'<path d="M {mx+5} {my-5} L {mx-5} {my+5}" stroke="#E4574C" stroke-width="3" stroke-linecap="round"/>')
    elif marks == "check":
        # 綠勾一排（表示全對）
        for i in range(6):
            y = -78 + i * 30
            mx, my = 31, y
            w.append(f'<path d="M {mx-4} {my+1} L {mx-1} {my+4} L {mx+4} {my-3}" fill="none" stroke="#5BA85C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')

    inner = "".join(w)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


# ============= SCENES =============

def scene_cover():
    """封面：Owen bust + desk + 計時器 + owl 停桌角 + 獎狀背景"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="620" fill="{BG["cover"]}"/>')

    # 牆壁背景（下方，暖奶油色）
    e.append(f'<rect x="0" y="350" width="1188" height="270" fill="#E8D2AC"/>')

    # 書桌
    e.append(desk(cx=594, cy=500, w=380, scale=1.15))

    # 桌上物品：習題紙、計時器、鉛筆
    e.append(f'<rect x="450" y="380" width="90" height="70" rx="5" fill="#FFFFFF" stroke="#DDD3C2" stroke-width="1.5"/>')
    for i in range(3):
        y = 395 + i * 22
        e.append(f'<line x1="465" y1="{y}" x2="525" y2="{y}" stroke="#DDD3C2" stroke-width="0.8"/>')

    # 計時器（在習題紙右方）
    e.append(timer_stopwatch(cx=650, cy=350, scale=0.85, time_text="2:00"))

    # 鉛筆（斜放）
    e.append(f'<g transform="translate(750, 310) rotate(-25) scale(1.2)">'
             f'<rect x="-3" y="-55" width="6" height="90" rx="3" fill="#F2D146"/>'
             f'<rect x="-4" y="-65" width="8" height="10" rx="3" fill="#F2A9A0"/>'
             f'<polygon points="-2,-2 2,-2 0,-10" fill="#8B6F47"/></g>')

    # 獎狀背景（牆上）
    e.append(f'<rect x="200" y="80" width="160" height="140" rx="8" fill="#F2E4C0" stroke="#D9C49A" stroke-width="3"/>')
    e.append(f'<path d="M 220 130 Q 280 110 340 130" fill="none" stroke="#E4574C" stroke-width="2" stroke-dasharray="2 3"/>')
    e.append(svgtext(280, 160, "CONTEST!", size=24, fill="#E4574C", weight="bold"))

    # Owen bust（微笑，坐在桌前）
    e.append(boy_bust(expr="smile", cx=350, cy=360, scale=1.2))

    # 貓頭鷹停在桌角（爪子貼桌，mood='watch'）
    e.append(owl(cx=830, cy=495, scale=0.95, mood="watch"))

    # 暖色星星點綴
    e.append(star(120, 120, 16))
    e.append(star(1060, 140, 14))
    e.append(sparkle(240, 280, 11))

    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """p1：Owen 坐書桌，桌上習題紙 + 計時器，挺胸微笑"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p1"]}"/>')

    # 牆壁（下方）
    e.append(f'<rect x="0" y="380" width="{W}" height="180" fill="#E8D2AC"/>')

    # 書桌
    e.append(desk(cx=594, cy=440, w=380, scale=1.15))

    # 桌上物品
    e.append(f'<rect x="440" y="320" width="100" height="80" rx="4" fill="#FFFFFF" stroke="#DDD3C2" stroke-width="1.5"/>')
    for i in range(4):
        y = 335 + i * 18
        e.append(f'<line x1="455" y1="{y}" x2="535" y2="{y}" stroke="#DDD3C2" stroke-width="0.8"/>')

    # 計時器（在習題紙右方）
    e.append(timer_stopwatch(cx=680, cy=310, scale=0.8, time_text="2:00"))

    # 鉛筆
    e.append(f'<g transform="translate(620, 270) rotate(-15) scale(1.0)">'
             f'<rect x="-3" y="-50" width="6" height="80" rx="3" fill="#F2D146"/>'
             f'<rect x="-4" y="-60" width="8" height="10" rx="3" fill="#F2A9A0"/>'
             f'<polygon points="-2,0 2,0 0,-8" fill="#8B6F47"/></g>')

    # Owen bust（微笑，坐桌前）
    e.append(boy_bust(expr="smile", cx=400, cy=310, scale=1.15))

    # 星星點綴
    e.append(star(180, 100, 14))
    e.append(star(1000, 120, 12))
    e.append(sparkle(300, 180, 10))

    return svg(W, H, "".join(e))


def scene_p2():
    """p2：計時器特寫（2:00）+ April 手按計時器頂鈕"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p2"]}"/>')

    # 地板
    e.append(f'<rect x="0" y="420" width="{W}" height="140" fill="#D9B98C"/>')

    # 大計時器（中央，發光）
    e.append(timer_stopwatch(cx=594, cy=200, scale=1.5, time_text="2:00", glow=True))

    # April（在右側，手指向計時器頂鈕）
    e.append(april(cx=900, cy=280, scale=1.1, pose="wave"))

    # 手指指向計時器頂鈕的視線
    e.append(f'<line x1="850" y1="100" x2="580" y2="130" stroke="#F2A9A0" stroke-width="2" stroke-dasharray="2 4" stroke-opacity="0.6"/>')

    # 星星點綴
    e.append(star(150, 100, 16))
    e.append(star(1050, 130, 14))

    return svg(W, H, "".join(e))


def scene_p3():
    """p3：Owen bust（star 表情）盯著計時器，頭上思考泡泡（獲勝想像）"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p3"]}"/>')
    e.append(f'<rect x="0" y="420" width="{W}" height="140" fill="#E8D2AC"/>')

    # 計時器（左側，中等大小）
    e.append(timer_stopwatch(cx=250, cy=240, scale=1.0, time_text="2:00"))

    # Owen bust（star 表情，中央看著計時器）
    e.append(boy_bust(expr="star", cx=594, cy=310, scale=1.35))

    # 思考泡泡（頭上）
    bubble = f'<ellipse cx="750" cy="130" rx="100" ry="70" fill="#FFFFFF" stroke="#D7C7AD" stroke-width="4"/>'
    e.append(bubble)
    e.append(f'<path d="M 700 190 L 680 260 L 720 240 Z" fill="#FFFFFF" stroke="#D7C7AD" stroke-width="2"/>')

    # 泡泡內獎盃圖示（簡單金杯形）
    e.append(f'<path d="M 710 110 Q 740 100 760 130 Q 750 160 730 150 Q 730 170 750 180 L 750 190 L 710 190 L 710 180 Q 730 170 730 150 Q 710 160 710 130 Z" fill="#F2D146" stroke="#E8A20C" stroke-width="2"/>')

    # 星星點綴
    e.append(star(200, 80, 18))
    e.append(star(1050, 100, 16))
    e.append(sparkle(350, 150, 12))

    return svg(W, H, "".join(e))


def scene_p4():
    """p4：衝動頁 - Owen bust（hold 表情）狂寫 + 鉛筆殘影 + 眼睛亂飄虛線 + 習題紙紅✗ + 計時器滴答線 + 心跳"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p4"]}"/>')
    e.append(f'<rect x="0" y="420" width="{W}" height="140" fill="#E8D2AC"/>')

    # 背景衝動線
    for (x, y) in [(250, 100), (950, 120), (200, 300), (1000, 280)]:
        e.append(f'<path d="M {x} {y} q 12 -18 24 0 q 12 18 24 0" fill="none" stroke="#F26B5E" stroke-width="6" stroke-linecap="round"/>')

    # 習題紙（左側，有紅 ✗）
    e.append(f'<rect x="140" y="280" width="120" height="100" rx="5" fill="#FFFFFF" stroke="#DDD3C2" stroke-width="1.5"/>')
    for i in range(4):
        y = 300 + i * 20
        e.append(f'<line x1="155" y1="{y}" x2="245" y2="{y}" stroke="#DDD3C2" stroke-width="0.8"/>')

    # 習題紙上的紅 ✗✗✗
    for (mx, my) in [(180, 310), (200, 335), (190, 360), (210, 380)]:
        e.append(f'<path d="M {mx-6} {my-6} L {mx+6} {my+6}" stroke="#E4574C" stroke-width="3" stroke-linecap="round"/>')
        e.append(f'<path d="M {mx+6} {my-6} L {mx-6} {my+6}" stroke="#E4574C" stroke-width="3" stroke-linecap="round"/>')

    # Owen bust（hold 表情，中央狂寫）
    e.append(boy_bust(expr="hold", cx=594, cy=310, scale=1.45))

    # 鉛筆殘影（平行虛影線，表示筆高速）
    for offset in [120, 160, 200]:  # 頭右緣 x≈675，殘影線從 714 起跑不碰頭
        e.append(f'<path d="M {594+offset} 200 L {594+offset+25} 380" fill="none" stroke="#F2D146" stroke-width="3" stroke-dasharray="4 8" stroke-opacity="0.5"/>')

    # 眼睛亂飄虛線（從眼睛出發向外，不穿過臉，2-3 條）
    # 假設眼睛中心在 (594, 280) 附近
    e.append(f'<path d="M 560 280 L 500 240 L 480 260" fill="none" stroke="#E4574C" stroke-width="2" stroke-dasharray="3 5" stroke-linecap="round"/>')
    e.append(f'<path d="M 628 280 L 680 250 L 700 270" fill="none" stroke="#E4574C" stroke-width="2" stroke-dasharray="3 5" stroke-linecap="round"/>')
    # （第三條垂直視線會穿過頭頂，移除——兩條外飄視線已足夠）

    # 計時器滴答動態線（右上方）
    e.append(timer_stopwatch(cx=950, cy=150, scale=0.75, time_text="2:00"))
    for angle in [30, 90, 150]:
        rad = math.radians(angle)
        x1 = 950 + 65 * math.cos(rad)
        y1 = 150 + 65 * math.sin(rad)
        x2 = 950 + 85 * math.cos(rad)
        y2 = 150 + 85 * math.sin(rad)
        e.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#E4574C" stroke-width="2" stroke-linecap="round"/>')

    # 心臟符號（表示緊張，左上方）
    e.append(f'<path d="M 300 150 c 0 -12 16 -12 16 0 c 0 -12 16 -12 16 0 c 0 12 -16 20 -16 28 c 0 -8 -16 -16 -16 -28 Z" fill="#F2665A" stroke="#D14A3F" stroke-width="2"/>')

    return svg(W, H, "".join(e))


def scene_p5():
    """p5：紫星空 + owl 發光登場停桌角 + Owen bust（press 表情）"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p5"]}"/>')

    # 星星點綴
    for (x, y, r) in [(120, 100, 18), (1050, 130, 20), (180, 400, 14), (980, 380, 16), (300, 60, 12), (900, 80, 14)]:
        e.append(star(x, y, r, fill="#FFE8B6"))
    e.append(sparkle(250, 150, 12))
    e.append(sparkle(950, 200, 12))

    # 書桌（背景）
    e.append(desk(cx=594, cy=440, w=360, scale=1.1))

    # Owl 發光登場（多層光暈）
    e.append(f'<circle cx="850" cy="420" r="120" fill="{STAR_Y}" fill-opacity="0.15"/>')
    e.append(f'<circle cx="850" cy="420" r="85" fill="{STAR_Y}" fill-opacity="0.2"/>')

    # 貓頭鷹停在桌角（爪子貼桌面，mood='watch'）
    e.append(owl(cx=850, cy=415, scale=1.0, mood="watch"))

    # Owen bust（press 表情，看著 owl）
    e.append(boy_bust(expr="press", cx=350, cy=310, scale=1.2))

    # 地面陰影
    e.append(f'<ellipse cx="594" cy="520" rx="500" ry="80" fill="#D9C4B8" fill-opacity="0.3"/>')

    return svg(W, H, "".join(e))


def scene_p6():
    """p6：三格（圓角矩形框）- ①大眼睛圖示 ②題目放大發光 ③答案+綠勾"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p6"]}"/>')
    e.append(f'<rect x="0" y="430" width="{W}" height="130" fill="#D0DEFF"/>')

    frame_w = 300
    frame_h = 260
    frame_y = 100

    # ===== 第一格：大眼睛圖示 =====
    x1 = 150
    e.append(f'<rect x="{x1-frame_w//2}" y="{frame_y}" width="{frame_w}" height="{frame_h}" rx="12" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')

    # 貓頭鷹式大圓眼（簡化版，只畫眼睛和視線）
    e.append(f'<circle cx="{x1-25}" cy="200" r="20" fill="#FFFFFF" stroke="#1A1A1A" stroke-width="4"/>')
    e.append(f'<circle cx="{x1-25}" cy="200" r="10" fill="#1A1A1A"/>')
    e.append(f'<circle cx="{x1+25}" cy="200" r="20" fill="#FFFFFF" stroke="#1A1A1A" stroke-width="4"/>')
    e.append(f'<circle cx="{x1+25}" cy="200" r="10" fill="#1A1A1A"/>')

    # 視線實線鎖定題目（從眼睛向下指向）
    e.append(f'<path d="M {x1-25} 220 L {x1-25} 280" fill="none" stroke="#E4574C" stroke-width="2.5" stroke-linecap="round"/>')
    e.append(f'<path d="M {x1+25} 220 L {x1+25} 280" fill="none" stroke="#E4574C" stroke-width="2.5" stroke-linecap="round"/>')

    e.append(svgtext(x1, 320, "Owl eyes on", size=16, fill=STAR_DK, weight="bold"))

    # ===== 第二格：題目數字放大發光 =====
    x2 = 594
    e.append(f'<rect x="{x2-frame_w//2}" y="{frame_y}" width="{frame_w}" height="{frame_h}" rx="12" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')

    # 題目框發光
    e.append(f'<circle cx="{x2}" cy="200" r="70" fill="{STAR_Y}" fill-opacity="0.2"/>')
    e.append(f'<rect x="{x2-60}" y="170" width="120" height="60" rx="8" fill="{STAR_Y}" fill-opacity="0.15" stroke="{STAR_DK}" stroke-width="2"/>')

    # 大字題目
    e.append(svgtext(x2, 205, "12+34", size=32, fill="#E4574C", weight="bold"))

    e.append(svgtext(x2, 320, "Read it right", size=16, fill=STAR_DK, weight="bold"))

    # ===== 第三格：答案+綠勾 =====
    x3 = 1038
    e.append(f'<rect x="{x3-frame_w//2}" y="{frame_y}" width="{frame_w}" height="{frame_h}" rx="12" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')

    # 答案區
    e.append(f'<rect x="{x3-50}" y="170" width="100" height="50" rx="6" fill="#FFFFFF" stroke="#DDD3C2" stroke-width="1.5"/>')
    e.append(svgtext(x3, 200, "46", size=24, fill=TXT, weight="bold"))

    # 綠勾（大）
    e.append(f'<path d="M {x3-30} 260 L {x3-15} 275 L {x3+20} 230" fill="none" stroke="#5BA85C" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')

    e.append(svgtext(x3, 320, "Write it once", size=16, fill=STAR_DK, weight="bold"))

    return svg(W, H, "".join(e))


def scene_p7():
    """p7：左右對比格 - 左格紅✗+橡皮+時鐘圈；右格綠勾+時鐘一格+owl nod 比讚"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p7"]}"/>')
    e.append(f'<rect x="0" y="420" width="{W}" height="140" fill="#BFD9EE"/>')

    # ===== 左格：寫錯的耗時 =====
    e.append(f'<rect x="80" y="100" width="420" height="280" rx="12" fill="#FFFFFF" stroke="#E8A8A8" stroke-width="3"/>')

    # 習題紙（左上）
    e.append(f'<rect x="140" y="130" width="80" height="70" rx="4" fill="#FFFEF5" stroke="#DDD3C2" stroke-width="1.5"/>')
    for i in range(3):
        y = 145 + i * 18
        e.append(f'<line x1="155" y1="{y}" x2="205" y2="{y}" stroke="#DDD3C2" stroke-width="0.8"/>')

    # 紅 ✗（在習題紙上）
    e.append(f'<path d="M 155 150 L 190 185" stroke="#E4574C" stroke-width="4" stroke-linecap="round"/>')
    e.append(f'<path d="M 190 150 L 155 185" stroke="#E4574C" stroke-width="4" stroke-linecap="round"/>')

    # 橡皮擦（粉紅方塊）
    e.append(f'<rect x="240" y="140" width="30" height="40" rx="4" fill="#F2A9A0" stroke="#E89490" stroke-width="2"/>')
    e.append(f'<rect x="240" y="135" width="30" height="4" fill="#C9BFA8"/>')  # 金屬套

    # 時鐘（多圈箭頭，表示重做）
    for i, r in enumerate([55, 65, 75]):
        angle = 90
        rad = math.radians(angle)
        x, y = 330 + r * math.cos(rad), 190 + r * math.sin(rad)
        e.append(f'<circle cx="330" cy="190" r="{r}" fill="none" stroke="#E4574C" stroke-width="2" stroke-dasharray="3 4" stroke-opacity="0.6"/>')

    e.append(svgtext(330, 190, "❌", size=28, fill="#E4574C"))

    # 左格標籤
    e.append(svgtext(290, 310, "Wrong costs time!", size=14, fill="#E4574C", weight="bold"))

    # ===== 右格：寫對的速度 =====
    e.append(f'<rect x="688" y="100" width="420" height="280" rx="12" fill="#FFFFFF" stroke="#A8E8A8" stroke-width="3"/>')

    # 綠勾（大）
    e.append(f'<path d="M 770 200 L 800 230 L 880 140" fill="none" stroke="#5BA85C" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')

    # 時鐘（一格，表示快速）
    e.append(f'<circle cx="950" cy="190" r="50" fill="none" stroke="#5BA85C" stroke-width="2"/>')
    e.append(f'<line x1="950" y1="190" x2="950" y2="130" stroke="#5BA85C" stroke-width="2" stroke-linecap="round"/>')  # 時針指向 12
    e.append(f'<line x1="950" y1="190" x2="980" y2="190" stroke="#5BA85C" stroke-width="2" stroke-linecap="round"/>')  # 分針指向 3

    # 貓頭鷹 nod 比讚（右上方）
    e.append(owl(cx=1040, cy=160, scale=0.9, mood="nod"))

    # 右格標籤
    e.append(svgtext(898, 310, "Speed from accuracy!", size=14, fill="#5BA85C", weight="bold"))

    return svg(W, H, "".join(e))


def scene_p8():
    """p8：計時器響 Ding! + April 拿習題紙對答案 + 語音泡泡 + Owen bust 挺胸 + owl 開心"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p8"]}"/>')
    e.append(f'<rect x="0" y="420" width="{W}" height="140" fill="#D9B98C"/>')

    # 計時器（上方左側，帶 Ding! 符號）
    e.append(timer_stopwatch(cx=200, cy=120, scale=0.9, time_text="0:00", glow=True))

    # Ding! 文字＋星星（在計時器上方）
    e.append(svgtext(200, 80, "Ding!", size=28, fill="#E4574C", weight="bold"))
    for angle in [45, 135, 225, 315]:
        rad = math.radians(angle)
        x = 200 + 65 * math.cos(rad)
        y = 80 + 65 * math.sin(rad)
        e.append(star(int(x), int(y), 12, fill=STAR_Y))

    # 習題紙（April 拿著，有綠勾一排）
    e.append(worksheet_contest(cx=380, cy=280, scale=1.2, marks="check"))

    # April（右側，拿習題紙）
    e.append(april(cx=750, cy=280, scale=1.0, pose="stand"))

    # 語音泡泡（指向 April 嘴邊）
    bubble = f'<ellipse cx="550" cy="140" rx="130" ry="75" fill="#FFFFFF" stroke="#D7C7AD" stroke-width="4"/>'
    e.append(bubble)
    e.append(f'<path d="M 480 190 L 450 240 L 500 200 Z" fill="#FFFFFF" stroke="#D7C7AD" stroke-width="2"/>')

    # 泡泡內文字
    e.append(svgtext(550, 125, "Owl eyes,", size=18, fill="#D97706", weight="bold"))
    e.append(svgtext(550, 155, "<b>Owen</b>!", size=18, fill="#D97706", weight="bold"))

    # Owen bust（挺胸 proud 表情）
    e.append(boy_bust(expr="proud", cx=350, cy=320, scale=1.15))

    # 貓頭鷹（在右下方開心，mood='cheer'）
    e.append(owl(cx=900, cy=380, scale=0.85, mood="cheer"))

    return svg(W, H, "".join(e))


def scene_p9():
    """p9：習題紙特寫綠勾滿排 + 大星星 + Owen jump 歡呼 + owl fly"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p9"]}"/>')
    e.append(f'<rect x="0" y="420" width="{W}" height="140" fill="#E8D2AC"/>')

    # 習題紙特寫（中央偏左，滿排綠勾）
    e.append(f'<rect x="200" y="160" width="160" height="200" rx="6" fill="#FFFFFF" stroke="#DDD3C2" stroke-width="2"/>')
    for i in range(8):
        y = 185 + i * 22
        e.append(f'<path d="M 240 {y} L 255 {y+8} L 280 {y-6}" fill="none" stroke="#5BA85C" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')

    # 大星星點綴（習題紙周圍）
    e.append(star(150, 120, 26, fill=STAR_Y))
    e.append(star(400, 300, 24, fill=STAR_Y))
    e.append(star(280, 400, 20, fill=STAR_Y))

    # Owen jump 歡呼（右側）
    e.append(boy(pose="jump", expr="big", cx=850, cy=200, scale=1.25))

    # 貓頭鷹 fly（展翅飛，左上方）
    e.append(owl(cx=400, cy=120, scale=1.0, mood="fly"))

    # 背景五彩紙屑
    import random
    random.seed(9)
    cols = ["#F6C445", "#7BC47F", "#6FA8DC", "#F49AB5", "#E4574C"]
    for i in range(15):
        x, y = random.randint(100, 1000), random.randint(50, 350)
        c = cols[i % 5]
        e.append(f'<rect x="{x}" y="{y}" width="10" height="14" rx="2" fill="{c}" transform="rotate({random.randint(-45,45)} {x} {y})"/>')

    return svg(W, H, "".join(e))


def scene_p10():
    """p10：英雄頁 - Owen hips+cape + owl(cape=True) 在肩膀 + 桌上發光習題紙 + 計時器 + 滿天星"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p10"]}"/>')

    # 背景地面
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="100" fill="#FFDD7E"/>')

    # 滿天星
    for (x, y, r) in [(140, 100, 20), (1050, 120, 22), (180, 400, 14), (1000, 380, 16), (320, 60, 12), (870, 70, 14)]:
        e.append(star(x, y, r))
    e.append(sparkle(260, 240, 12))
    e.append(sparkle(930, 240, 12))

    # 發光的習題紙（桌上）
    e.append(f'<circle cx="700" cy="340" r="100" fill="{STAR_Y}" fill-opacity="0.15"/>')
    e.append(f'<circle cx="700" cy="340" r="70" fill="{STAR_Y}" fill-opacity="0.2"/>')
    e.append(worksheet_contest(cx=700, cy=340, scale=1.3, marks="check"))

    # 計時器（右下方）
    e.append(timer_stopwatch(cx=950, cy=380, scale=0.9, time_text="2:00"))

    # Owen（hips 英雄姿勢 + cape）
    e.append(boy(pose="hips", expr="proud", cx=350, cy=160, scale=1.3, cape=True))

    # 貓頭鷹（披披風）站在 Owen 右側地面歡呼——原本放肩膀會與頭部區域（x≤423）重疊擋臉
    # Owen feet_y = 160+228*1.3 ≈ 456；owl 爪子貼同一地面 → cy = 456-40
    e.append(owl(cx=530, cy=416, scale=0.95, mood="cheer", cape=True))

    return svg(W, H, "".join(e))


# ============= PAGE TEXTS ================

PAGES = [
    ("p1", scene_p1, "This is me, <b>Owen</b>!<br/>I practice for my math <b>contest</b>!"),
    ("p2", scene_p2, "Two minutes, fifty problems!<br/>The <b>timer</b> goes tick, tick, tick."),
    ("p3", scene_p3, "I want to beat the clock!<br/>Fast, fast, fast!"),
    ("p4", scene_p4, "My eyes skip the numbers!<br/>My heart ticks fast like the timer.<br/>X, X, X&mdash;so many wrong!"),
    ("p5", scene_p5, "<b>STOP!</b> I use my superpower&hellip;<br/>I get my <b>owl</b> eyes!"),
    ("p6", scene_p6, "<b>Owl</b> eyes ON.<br/>Read it right.<br/>Write it once!"),
    ("p7", scene_p7, "Wrong ones cost time.<br/>My owl nods: read first, win!<br/>Read it right <b>is</b> fast!"),
    ("p8", scene_p8, "Ding! Time is up!<br/>Mommy April counts my page.<br/>&ldquo;Owl eyes, <b>Owen</b>!&rdquo;"),
    ("p9", scene_p9, "Fifty problems, so many right!<br/>My owl eyes win.<br/>I feel <b>GREAT</b>!"),
    ("p10", scene_p10, "Owl eyes on. Read it right.<br/>Write it once!<br/><b>Read it right!</b> I practice every day!"),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3～4 次，重複是關鍵。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("與 Slow and check 的分工", "平日無時限練習用『Slow and check!』（慢＋逐題檢查）；計時/比賽模式用『Read it right!』（看清一次寫對）。開始計時前先問他「今天是哪一種？」讓他自己說出口訣。"),
    ("計分改『對題數』不改『完成數』", "計時練習後只數「對幾題」，寫 50 題錯 20 不如寫 35 題全對——讓他體感「對才是分數」。連續進步就給貓頭鷹貼紙。"),
    ("當他主動說『My eyes skip』", "或寫前先指著題目讀一次 = 覺察里程碑，大力稱讚。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

BOOK = {
    "slug": "read-it-right",
    "order": 16,
    "title_pre": "", "title_hi": "Read", "title_post": " It Right!",
    "title_zh": "看清楚，寫對",
    "subtitle": "Owen's contest story",
    "tagline_zh": "Owen 的比賽練習故事",
    "chips": ["Social Story", "Math", "13 pages"],
    "pdf_name": "Read_It_Right.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ['owl', 'timer', 'contest'],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Owl eyes on &rarr; Read it right &rarr; Write it once!</b>&nbsp;"
                 "當他主動說出『My eyes skip』或寫前先指著題目讀一次時，就是最值得大力稱讚的覺察時刻。"),
    "cover": scene_cover,
}
