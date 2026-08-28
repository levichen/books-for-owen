# -*- coding: utf-8 -*-
"""Book 21: Little Teacher! — 課堂內容太簡單時的自大反應（炫耀、覺得都會）
安裝「抓住炫耀 → 想起我只是先出發 → 當小老師幫忙」的重新框架腳本。
核心意象：跑道——大家跑同一條學習之路，Owen 只是先出發（head start）。"""
import math
from parts import *
from book_common import svg, svgtext, TXT, W, H

# soft page palettes
BG = {
    "cover": "#FFF8E8", "p1": "#E8F4FF", "p2": "#FFF3D6", "p3": "#FFE8E8",
    "p4": "#FFE8E8", "p5": "#3D2E5C", "p6": "#FFE9A8", "p7": "#E8F8D8",
    "p8": "#FFF0C9", "p9": "#FFE2EC", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

BRAG_BUBBLE_RED = "#E8574C"
HEAD_START_FLAG_GOLD = "#F0B429"
BADGE_GREEN = "#2D5016"

# ================== SHARED COMPONENTS ==================

def easy_bubble(cx, cy, s=1.0, zipped=False, mouth_ref_y=None):
    """SO EASY! 泡泡：ellipse rx=78 ry=36 白底＋#F0B4C8 描邊。
    文字 "SO EASY!" size=20 置中於 (cx, cy+7)。
    若 zipped=True，金色拉鍊疊在中線、此時無尾巴；否則小三角尾巴指向 mouth_ref_y。"""
    b = []
    # 泡泡本體（ellipse）
    b.append(f'<ellipse cx="0" cy="0" rx="78" ry="36" fill="#FFFFFF" stroke="#F0B4C8" stroke-width="2.5"/>')
    # 文字 "SO EASY!"
    b.append(svgtext(0, 7, "SO EASY!", size=20, fill=BRAG_BUBBLE_RED, weight="bold"))

    if not zipped and mouth_ref_y is not None:
        # 尾巴：小三角指向嘴
        tail_y = 36
        b.append(f'<polygon points="0,{tail_y} -12,{tail_y+16} 12,{tail_y+16}" '
                 f'fill="#FFFFFF" stroke="#F0B4C8" stroke-width="1.5"/>')
    elif zipped:
        # 金色拉鍊（貫穿泡泡中線 y=0）
        b.append(f'<rect x="-70" y="-3" width="140" height="6" rx="2" fill="{HEAD_START_FLAG_GOLD}" stroke="#8A5A2B" stroke-width="1.2"/>')
        # 上下交錯小齒
        for i in range(9):
            x = -65 + i * 16
            dy = 0 if i % 2 == 0 else 1
            b.append(f'<rect x="{x-1.5}" y="{-8+dy}" width="3" height="3" fill="{HEAD_START_FLAG_GOLD}" stroke="#8A5A2B" stroke-width="0.8"/>')
            b.append(f'<rect x="{x-1.5}" y="{5+dy}" width="3" height="3" fill="{HEAD_START_FLAG_GOLD}" stroke="#8A5A2B" stroke-width="0.8"/>')
        # 圓形拉頭
        b.append(f'<circle cx="70" cy="0" r="4.5" fill="{HEAD_START_FLAG_GOLD}" stroke="#8A5A2B" stroke-width="1.2"/>')

    return f'<g transform="translate({cx},{cy})">{"".join(b)}</g>'

def runway(x, y, w, line_color):
    """水平跑道帶：rect (x, y, w, 高 64, rx 12) + 上下邊線 + 虛線。
    紫底頁用 #FFE9A8 opacity .18；綠底頁用 #FFFFFF opacity .5。"""
    r = []
    opacity = 0.18 if line_color == "#FFE9A8" else 0.5
    # 跑道底色帶
    r.append(f'<rect x="{x}" y="{y}" width="{w}" height="64" rx="12" '
             f'fill="{line_color}" fill-opacity="{opacity}"/>')
    # 上邊線
    r.append(f'<line x1="{x}" y1="{y}" x2="{x+w}" y2="{y}" stroke="{line_color}" stroke-width="2"/>')
    # 下邊線
    r.append(f'<line x1="{x}" y1="{y+64}" x2="{x+w}" y2="{y+64}" stroke="{line_color}" stroke-width="2"/>')
    # 虛線中分線
    for seg in range(0, int(w), 24):
        r.append(f'<line x1="{x+seg}" y1="{y+32}" x2="{min(x+seg+14, x+w)}" y2="{y+32}" '
                 f'stroke="{line_color}" stroke-width="2" stroke-dasharray="14 10"/>')
    return "".join(r)

def runner(cx, cy, s, color, opacity):
    """奔跑剪影：圓頭(r=16) + 前傾軀幹 + 前後腿 + 兩臂擺動。腳底落在 cy+55*s。"""
    r = []
    # 頭（圓）
    r.append(f'<circle cx="0" cy="{-55*s}" r="{16*s}" fill="{color}" fill-opacity="{opacity}"/>')
    # 軀幹（前傾斜 path）
    r.append(f'<path d="M 0 {-38*s} L {12*s} {18*s}" stroke="{color}" stroke-width="{20*s}" '
             f'stroke-linecap="round" fill="none" fill-opacity="{opacity}"/>')
    # 前腿（前跨）
    r.append(f'<path d="M {8*s} {22*s} L {14*s} {55*s}" stroke="{color}" stroke-width="{10*s}" '
             f'stroke-linecap="round" fill="none" fill-opacity="{opacity}"/>')
    # 後腿（後勾）
    r.append(f'<path d="M {-4*s} {20*s} Q {-20*s} {8*s} {-16*s} {-8*s}" stroke="{color}" stroke-width="{10*s}" '
             f'stroke-linecap="round" fill="none" fill-opacity="{opacity}"/>')
    # 前臂（前擺）
    r.append(f'<path d="M {6*s} {-28*s} L {28*s} {-12*s}" stroke="{color}" stroke-width="{8*s}" '
             f'stroke-linecap="round" fill="none" fill-opacity="{opacity}"/>')
    # 後臂（後擺）
    r.append(f'<path d="M {-6*s} {-20*s} L {-22*s} {8*s}" stroke="{color}" stroke-width="{8*s}" '
             f'stroke-linecap="round" fill="none" fill-opacity="{opacity}"/>')
    return f'<g transform="translate({cx},{cy})">{"".join(r)}</g>'

def flag(x, ground_y):
    """旗桿垂直向上 56px (底端觸地 ground_y)，桿頂掛三角旗。"""
    f = []
    # 旗桿（從 ground_y 向上）
    f.append(f'<line x1="{x}" y1="{ground_y}" x2="{x}" y2="{ground_y-56}" '
             f'stroke="#8A5A2B" stroke-width="3" stroke-linecap="round"/>')
    # 三角旗（貼在桿頂）
    f.append(f'<polygon points="{x},{ground_y-56} {x+24},{ground_y-56} {x+18},{ground_y-36}" '
             f'fill="{HEAD_START_FLAG_GOLD}" stroke="#8A5A2B" stroke-width="2"/>')
    return "".join(f)

def teacher_badge(cx, cy, scale=1.0):
    """小老師徽章：發光黑板圖示（深綠圓角矩形+白色 "2+3" 內容）+ 雙層光暈。"""
    b = []
    # 外圈光暈（黃金色，兩層半透明圓）
    b.append(f'<circle cx="0" cy="0" r="{48*scale}" fill="{HEAD_START_FLAG_GOLD}" fill-opacity="0.35"/>')
    b.append(f'<circle cx="0" cy="0" r="{32*scale}" fill="{HEAD_START_FLAG_GOLD}" fill-opacity="0.55"/>')
    # 黑板本體（深綠圓角矩形）
    b.append(f'<rect x="{-20*scale}" y="{-22*scale}" width="{40*scale}" height="{44*scale}" '
             f'rx="{5*scale}" fill="{BADGE_GREEN}" stroke="#FFFFFF" stroke-width="{2*scale}"/>')
    # 木框（棕色邊框線）
    b.append(f'<rect x="{-22*scale}" y="{-24*scale}" width="{44*scale}" height="{48*scale}" '
             f'rx="{6*scale}" fill="none" stroke="#8A6A52" stroke-width="{2*scale}"/>')
    # 白色粉筆內容："2+3"
    b.append(svgtext(0, 4*scale, "2+3", size=int(20*scale), fill="#FFFFFF", weight="bold"))
    return f'<g transform="translate({cx},{cy})">{"".join(b)}</g>'

# ================== SCENES ==================

def scene_cover():
    """封面：Owen 白T 背書包出門上學，抱著珠算盤與英文書（手位），頭上小星星。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="620" fill="{BG["cover"]}"/>')

    # 地板
    e.append(f'<ellipse cx="594" cy="620" rx="560" ry="100" fill="#FFDD7E"/>')

    # Owen 走出門（walk pose）
    e.append(boy(pose="walk", expr="big", cx=350, cy=320, scale=1.2, backpack=True))

    # 珠算盤（左胸）
    e.append(f'<rect x="250" y="340" width="70" height="80" rx="4" fill="#8B6F47" stroke="#5A4A3A" stroke-width="2"/>')
    for row in range(3):
        for col in range(5):
            bx = 257 + col * 12
            by = 347 + row * 24
            e.append(f'<circle cx="{bx}" cy="{by}" r="4.5" fill="#E4574C" stroke="#8A5A2B" stroke-width="1"/>')

    # 英文書（右側，貼到手位：boy walk 右手底 ≈ (417, 514)→手圓位，書底 y→480 貼手圓）
    e.append(f'<rect x="385" y="450" width="60" height="80" rx="3" fill="#5CA8E8" stroke="#2E6AAA" stroke-width="2"/>')
    e.append(svgtext(415, 495, "ABC", size=20, fill="#FFFFFF", weight="bold"))

    # 頭上小星星
    e.append(star(200, 140, 18, fill=STAR_Y))
    e.append(star(900, 120, 20, fill=STAR_Y))

    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """p1：Owen 白T 背書包站立，抱著珠算盤與英文書（手位），頭上小星星。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p1"]}"/>')
    e.append(f'<ellipse cx="594" cy="560" rx="560" ry="80" fill="#D4E8FF"/>')

    # 雲朵裝飾
    e.append(cloud(150, 80, 0.9))
    e.append(cloud(950, 100, 1.1))

    # 星星與太陽
    e.append(sun(1000, 120, r=28))
    for (x, y, r) in [(200, 140, 18), (450, 100, 16)]:
        e.append(star(x, y, r, fill=STAR_Y))

    # Owen 開心站立，背書包（feet_y = 280+228*1.15 ≈ 542）
    e.append(boy(pose="stand", expr="big", cx=450, cy=280, scale=1.15, backpack=True))

    # 珠算盤（左胸前）
    e.append(f'<rect x="350" y="340" width="70" height="80" rx="4" fill="#8B6F47" stroke="#5A4A3A" stroke-width="2"/>')
    for row in range(3):
        for col in range(5):
            bx = 357 + col * 12
            by = 347 + row * 24
            e.append(f'<circle cx="{bx}" cy="{by}" r="4.5" fill="#E4574C" stroke="#8A5A2B" stroke-width="1"/>')

    # 英文書（右胸前，貼到手位：boy stand 右手約 (450+48*1.15, 280+166*1.15) ≈ (505, 471)→手圓位）
    e.append(f'<rect x="475" y="450" width="60" height="80" rx="3" fill="#5CA8E8" stroke="#2E6AAA" stroke-width="2"/>')
    e.append(svgtext(505, 495, "ABC", size=20, fill="#FFFFFF", weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p2():
    """p2：教室，Tr. Mina 在黑板前教 2+3=?，同學們認真看，Owen 課桌思考泡泡（珠算盤icon）。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p2"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#E8D2AC"/>')

    # 黑板
    e.append(f'<rect x="300" y="50" width="550" height="200" rx="10" fill="#C9A26B"/>')
    e.append(f'<rect x="320" y="70" width="510" height="160" rx="6" fill="#3E7C5B"/>')
    e.append(svgtext(595, 150, "2 + 3 = ?", size=80, fill="#FFFFFF", weight="bold"))

    # Tr. Mina 教書（右指）
    e.append(teacher(cx=200, cy=280, scale=1.0, point="right"))

    # Owen 課桌 + 半身
    e.append(desk(cx=550, cy=350, w=160, scale=0.85))
    e.append(boy_bust(expr="think", cx=550, cy=250, scale=0.8, arms="desk"))

    # 思考泡泡（頭上方左側）
    bubble_cx, bubble_cy = 650, 130
    e.append(f'<circle cx="{bubble_cx}" cy="{bubble_cy}" r="50" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="3"/>')
    # 尾巴指向頭
    e.append(f'<circle cx="610" cy="170" r="8" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2"/>')
    e.append(f'<circle cx="595" cy="200" r="5" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2"/>')
    # 泡泡內容：小珠算盤 icon
    e.append(f'<rect x="{bubble_cx-20}" y="{bubble_cy-20}" width="40" height="40" rx="3" fill="#8B6F47" stroke="#5A4A3A" stroke-width="1.5"/>')
    for row in range(2):
        for col in range(3):
            bx = bubble_cx - 15 + col * 8
            by = bubble_cy - 12 + row * 13
            e.append(f'<circle cx="{bx}" cy="{by}" r="2.5" fill="#E4574C"/>')

    # 同學 1（kid variant 0）
    e.append(desk(cx=800, cy=350, w=160, scale=0.85))
    e.append(kid(variant=0, cx=800, cy=270, scale=0.8, expr="think"))

    # 同學 2（kid variant 1）
    e.append(desk(cx=1000, cy=350, w=160, scale=0.85))
    e.append(kid(variant=1, cx=1000, cy=270, scale=0.8, expr="think"))

    return svg(W, H, "".join(e), bg=None)


def scene_p3():
    """p3：Owen 大頭特寫（star 表情），"SO EASY!" 泡泡在頭右側同高。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p3"]}"/>')

    # Owen 大頭特寫（star 表情的 boy_bust）
    e.append(boy_bust(expr="star", cx=400, cy=300, scale=1.4))

    # "SO EASY!" 泡泡（頭右側同高，mouth_ref_y=cy+300-10*1.4 ≈ 286，無尾巴）
    e.append(easy_bubble(650, 300, s=1.0, zipped=False, mouth_ref_y=286))

    # 星星裝飾
    e.append(star(150, 100, 16, fill=STAR_Y))
    e.append(star(1050, 120, 18, fill=STAR_Y))

    return svg(W, H, "".join(e), bg=None)


def scene_p4():
    """p4：【衝動頁】Owen 站起來驕傲（proud），"SO EASY!" 泡泡+頭上大「?」，
    兩位同學低頭（難過），Tr. Mina 溫和停頓。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p4"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#E8D2AC"/>')

    # Owen 站起來驕傲（feet_y=260+228*0.95 ≈ 477）
    e.append(boy(pose="stand", expr="proud", cx=300, cy=260, scale=0.95))

    # "SO EASY!" 泡泡（頭右上方，距頭≥20px）
    bubble_cx, bubble_cy = 450, 160
    mouth_y = 260 + 34*0.95  # ≈ 292
    e.append(easy_bubble(bubble_cx, bubble_cy, s=0.95, zipped=False, mouth_ref_y=mouth_y))

    # 頭頂大「?」（Owen 頭中心 = 260+4*0.95 ≈ 264，頭上≥24px）
    e.append(svgtext(300, 230, "?", size=44, fill=BRAG_BUBBLE_RED, weight="bold"))

    # 同學 1 低頭難過（坐課桌，think 表情）
    kid1_cx, kid1_cy = 650, 325
    e.append(desk(cx=kid1_cx, cy=kid1_cy, w=160, scale=0.85))
    e.append(kid(variant=0, cx=kid1_cx, cy=kid1_cy-80, scale=0.8, expr="think"))

    # 同學 2 低頭難過
    kid2_cx, kid2_cy = 900, 325
    e.append(desk(cx=kid2_cx, cy=kid2_cy, w=160, scale=0.85))
    e.append(kid(variant=2, cx=kid2_cx, cy=kid2_cy-80, scale=0.8, expr="think"))

    # Tr. Mina 溫和停頓（scale=1.0 > 0.8 kids✓）
    e.append(teacher(cx=1050, cy=280, scale=1.0, point="right"))

    return svg(W, H, "".join(e), bg=None)


def scene_p5():
    """p5：紫色星空，水平跑道帶（y≈380..444），Owen 站左前段，flag 右側插地，
    兩位 runner 右段面朝左（朝 Owen）。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p5"]}"/>')

    # 星空點綴
    for (x, y, r) in [(120, 100, 14), (1050, 120, 16), (200, 450, 12), (1000, 430, 14), (350, 80, 10), (850, 70, 12)]:
        e.append(star(x, y, r, fill="#E8D9FF"))
    for (sx, sy, sr) in [(320, 90, 12), (860, 80, 12), (90, 300, 10), (1100, 300, 10), (600, 50, 10)]:
        e.append(sparkle(sx, sy, sr, fill="#E8D9FF"))

    # 水平跑道帶（y=380 頂端，64 高 → 底 444）
    e.append(runway(150, 380, 888, "#FFE9A8"))

    # Owen 站跑道左前段（feet_y ≈ 444，press 表情看著）
    e.append(boy(pose="stand", expr="press", cx=280, cy=280, scale=0.95))

    # Flag 插在 Owen 右側約 60px 的跑道上（x≈340，ground_y=444）
    e.append(flag(340, 444))

    # 兩位 runner（白色半透明，s≈0.7）在跑道右段、面朝左（朝 Owen 方向跑）
    # 面朝左需要 scaleX(-1)
    runner_svg1 = runner(0, 0, 0.7, "#FFFFFF", 0.5)
    e.append(f'<g transform="translate(750, 410) scale(-1, 1)">{runner_svg1}</g>')
    runner_svg2 = runner(0, 0, 0.65, "#FFFFFF", 0.45)
    e.append(f'<g transform="translate(900, 420) scale(-1, 1)">{runner_svg2}</g>')

    return svg(W, H, "".join(e), bg=None)


def scene_p6():
    """p6：三步腳本三格：①Owen+拉鍊泡泡 ②縮小跑道+flag+runner ③Owen舉手+Tr.Mina（大於Owen）。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p6"]}"/>')

    # 三個圓形標誌與格子
    grid_positions = [(280, 280), (594, 280), (908, 280)]
    grid_w, grid_h = 240, 280

    for idx, (gx, gy) in enumerate(grid_positions):
        # 格子邊框
        e.append(f'<rect x="{gx-grid_w//2}" y="{gy-grid_h//2}" width="{grid_w}" height="{grid_h}" rx="12" fill="#FFFFFF" stroke="#FFB3D9" stroke-width="3"/>')
        # 圓形標誌
        e.append(f'<circle cx="{gx}" cy="{gy-130}" r="28" fill="{HEAD_START_FLAG_GOLD}" stroke="{HEAD_START_FLAG_GOLD}" stroke-width="3"/>')
        e.append(svgtext(gx, gy-120, str(idx+1), size=40, fill=BRAG_BUBBLE_RED, weight="bold"))

        if idx == 0:  # ①拉鍊泡泡
            # Owen 頭部特寫（半身）
            e.append(boy_bust(expr="press", cx=gx-55, cy=gy-40, scale=0.9, arms="desk"))
            # 拉鍊泡泡（頭右緣=gx-55+50=gx-5，泡泡左緣 gx+60-55=gx+5，不碰頭）
            e.append(easy_bubble(gx+60, gy-30, s=0.7, zipped=True))
            # 文字
            e.append(svgtext(gx, gy+100, "Catch!", size=22, fill=TXT, weight="bold"))

        elif idx == 1:  # ②跑道+旗+runner
            # 縮小跑道（格內寬 200）
            runway_y = gy + 40
            e.append(runway(gx-100, runway_y, 200, "#8A5A2B"))
            # Flag（底在 runway_y+64=gy+104）
            e.append(flag(gx-60, gy+104))
            # Runner（腳底在 runway_y+64）
            runner_svg = runner(0, 0, 0.5, "#2D2D2D", 0.6)
            e.append(f'<g transform="translate({gx+70}, {gy+40}) scale(-1, 1)">{runner_svg}</g>')
            # 文字
            e.append(svgtext(gx, gy+100, "I started early!", size=18, fill=TXT, weight="bold"))

        else:  # ③Owen舉手+Tr. Mina（Mina 要大於 Owen）
            # Owen 半身舉手（handup 手臂）
            e.append(boy_bust(expr="smile", cx=gx-70, cy=gy-30, scale=0.8, arms="handup"))
            # Tr. Mina 半身（scale=1.0 >> 0.8，cy 稍低以確保落地）
            e.append(teacher(cx=gx+60, cy=gy+20, scale=1.0, point="left"))
            # 對話泡泡 "Can I help?"
            bubble_x, bubble_y = gx-10, gy-70
            bubble_path = (f'<path d="M {bubble_x-30} {bubble_y} L {bubble_x-45} {bubble_y-25} L {bubble_x+30} {bubble_y-25} '
                           f'Q {bubble_x+40} {bubble_y-30} {bubble_x+40} {bubble_y-15} Q {bubble_x+40} {bubble_y} {bubble_x+30} {bubble_y} Z" '
                           f'fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2"/>')
            e.append(bubble_path)
            e.append(svgtext(bubble_x, bubble_y-10, "Can I help?", size=14, fill=TXT, weight="bold"))
            # 文字
            e.append(svgtext(gx, gy+100, "I ask first!", size=18, fill=TXT, weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p7():
    """p7：觀點頁 - 左格：kid坐課桌前+習題紙綠勾；右格：runway+Owen/runner同向跑+愛心。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p7"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#E8F8D8"/>')

    # 左格：kid 坐課桌+習題紙綠勾
    e.append(f'<rect x="80" y="100" width="360" height="300" rx="12" fill="#FFFFFF" stroke="#C4E8B4" stroke-width="3"/>')
    # 課桌
    e.append(desk(cx=260, cy=350, w=180, scale=0.85))
    # Kid smile（坐在課桌前）
    e.append(kid(variant=1, cx=260, cy=280, scale=0.85, expr="smile"))
    # 習題紙（桌上）
    e.append(f'<rect x="280" y="340" width="80" height="60" rx="3" fill="#FFFFFF" stroke="#D9B98C" stroke-width="2"/>')
    # 綠勾
    e.append(f'<path d="M 300 355 L 315 370 L 345 340" fill="none" stroke="#7FD93D" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>')

    # 右格：runway+Owen+runner 同向跑+愛心
    e.append(f'<rect x="748" y="100" width="360" height="300" rx="12" fill="#FFFFFF" stroke="#C4E8B4" stroke-width="3"/>')
    # 跑道下移到腳部高度（帶 300..364），人站帶上、頭遠離帶
    runway_y = 300
    e.append(runway(818, runway_y, 280, "#8A5A2B"))
    # Owen 奔跑（feet = 200+228*0.62 ≈ 341，落在帶內；頭底 ≈235 < 帶頂 300）
    e.append(boy(pose="run", expr="smile", cx=860, cy=200, scale=0.62))
    # Runner 奔跑（同向，腳 ≈353 帶內）
    e.append(runner(1000, 320, 0.6, "#9AA0A8", 0.55))
    # 愛心（兩人上方空中，不碰頭）
    for hx in [940, 980]:
        e.append(f'<path d="M {hx} 180 c 0 -5 -5 -10 -10 -10 c -5 0 -10 5 -10 10 c 0 10 10 15 10 15 s 10 -5 10 -15 Z" '
                 f'fill="#FF6B6B"/>')

    return svg(W, H, "".join(e), bg=None)


def scene_p8():
    """p8：Owen 與同學課桌邊坐，Owen 輕聲教，Tr. Mina 語音泡泡（移到她頭部左上方）。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p8"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#FFF0C9"/>')

    # 左側課桌 + Owen 半身
    owen_cx, owen_cy = 350, 350
    e.append(desk(cx=owen_cx, cy=owen_cy, w=160, scale=0.85))
    e.append(boy_bust(expr="smile", cx=owen_cx, cy=250, scale=0.8, arms="desk"))

    # 右側課桌 + 同學（kid variant 0, oh 表情表示驚訝/領悟）
    kid_cx, kid_cy = 650, 350
    e.append(desk(cx=kid_cx, cy=kid_cy, w=160, scale=0.85))
    e.append(kid(variant=0, cx=kid_cx, cy=270, scale=0.8, expr="oh"))

    # 習題紙（放在 Owen 課桌上）
    e.append(f'<rect x="320" y="340" width="60" height="40" rx="2" fill="#FFFFFF" stroke="#D9B98C" stroke-width="1.5" transform="rotate(-15 350 360)"/>')
    e.append(svgtext(350, 360, "✓", size=16, fill="#7FD93D", weight="bold"))

    # 輕聲泡泡（兩人之間）
    bubble_x, bubble_y = 500, 260
    e.append(f'<path d="M {bubble_x-25} {bubble_y} Q {bubble_x-25} {bubble_y-12} {bubble_x} {bubble_y-15} '
             f'Q {bubble_x+25} {bubble_y-12} {bubble_x+25} {bubble_y}" '
             f'fill="#FFFFFF" fill-opacity="0.85" stroke="#D9C9B8" stroke-width="1.5" stroke-dasharray="3 2"/>')
    e.append(svgtext(bubble_x, bubble_y-4, "psst...", size=12, fill=TXT))

    # Tr. Mina（右側）+ 語音泡泡（她頭部左上方，距離≤40px）
    mina_cx, mina_cy = 1050, 280
    e.append(teacher(cx=mina_cx, cy=mina_cy, scale=0.95, point="left"))
    # 語音泡泡：圓角矩形在她頭部左上方，尾巴貼泡泡底指向她的嘴（svgtext 不支援換行，單行放）
    e.append(f'<rect x="855" y="188" width="250" height="46" rx="14" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2.5"/>')
    e.append(f'<polygon points="1030,232 1052,232 1046,258" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2.5"/>')
    e.append(f'<rect x="1032" y="228" width="18" height="7" fill="#FFFFFF"/>')  # 蓋接縫
    e.append(svgtext(980, 217, "Super little teacher, Owen!", size=16, fill=TXT, weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p9():
    """p9：兩位同學舉著習題紙開心，Owen 中央挺胸微笑，頭上星星與愛心。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p9"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#FFE2EC"/>')

    # Owen 站立微笑、挺胸（proud 表情）
    e.append(boy(pose="stand", expr="proud", cx=450, cy=280, scale=1.0))

    # 左側同學（kid variant 0）舉著習題紙
    kid1_cx, kid1_cy = 280, 300
    e.append(kid(variant=0, cx=kid1_cx, cy=kid1_cy, scale=0.9, expr="smile"))
    # 上舉手臂：從肩（cy+70）伸到頭側上方（cy-55），紙底接臂端
    e.append(f'<path d="M {kid1_cx-30} {kid1_cy+70} Q {kid1_cx-52} {kid1_cy} {kid1_cx-44} {kid1_cy-55}" '
             f'stroke="{SKIN}" stroke-width="11" stroke-linecap="round" fill="none"/>')
    e.append(f'<rect x="{kid1_cx-80}" y="{kid1_cy-115}" width="70" height="60" rx="3" fill="#FFFFFF" stroke="#D9B98C" stroke-width="2" transform="rotate(-12 {kid1_cx-44} {kid1_cy-55})"/>')
    # 綠勾（紙面內）
    e.append(f'<path d="M {kid1_cx-68} {kid1_cy-88} L {kid1_cx-52} {kid1_cy-74} L {kid1_cx-26} {kid1_cy-102}" fill="none" stroke="#7FD93D" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" transform="rotate(-12 {kid1_cx-44} {kid1_cy-55})"/>')

    # 右側同學（kid variant 2）舉著習題紙
    kid2_cx, kid2_cy = 620, 300
    e.append(kid(variant=2, cx=kid2_cx, cy=kid2_cy, scale=0.9, expr="smile"))
    # 上舉手臂（鏡像）
    e.append(f'<path d="M {kid2_cx+30} {kid2_cy+70} Q {kid2_cx+52} {kid2_cy} {kid2_cx+44} {kid2_cy-55}" '
             f'stroke="{SKIN}" stroke-width="11" stroke-linecap="round" fill="none"/>')
    e.append(f'<rect x="{kid2_cx+10}" y="{kid2_cy-115}" width="70" height="60" rx="3" fill="#FFFFFF" stroke="#D9B98C" stroke-width="2" transform="rotate(12 {kid2_cx+44} {kid2_cy-55})"/>')
    # 綠勾（紙面內）
    e.append(f'<path d="M {kid2_cx+22} {kid2_cy-88} L {kid2_cx+38} {kid2_cy-74} L {kid2_cx+64} {kid2_cy-102}" fill="none" stroke="#7FD93D" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" transform="rotate(12 {kid2_cx+44} {kid2_cy-55})"/>')

    # 頭頂星星與愛心
    for (x, y, r) in [(350, 100, 14), (550, 80, 16), (750, 100, 14)]:
        e.append(star(x, y, r, fill=STAR_Y))

    # 愛心
    for (hx, hy) in [(300, 120), (600, 100), (900, 120)]:
        e.append(f'<path d="M {hx} {hy} c 0 -7 -7 -14 -14 -14 c -7 0 -14 7 -14 14 c 0 14 14 21 14 21 s 14 -7 14 -21 Z" fill="#FF6B6B"/>')

    return svg(W, H, "".join(e), bg=None)


def scene_p10():
    """p10：Owen 披紅披風叉腰（hips），手持小旗（from hips 手位外傾15°），身旁徽章，滿天星。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p10"]}"/>')

    # 滿天星星
    for (x, y, r) in [(160, 90, 18), (1020, 100, 22), (120, 380, 16), (1060, 380, 16), (330, 50, 14), (860, 60, 16), (420, 320, 12)]:
        e.append(star(x, y, r, fill=STAR_Y))
    for (sx, sy, sr) in [(260, 240, 12), (930, 240, 12), (600, 120, 10)]:
        e.append(sparkle(sx, sy, sr, fill=STAR_Y))

    # Owen 披紅披風叉腰（hips pose，scale=1.2）
    # hips 的右手位局部 (44, 150) → screen (cx+44*1.2, cy+150*1.2) ≈ (503, 460)
    e.append(boy(pose="hips", expr="proud", cx=450, cy=280, scale=1.2, cape=True))

    # 手持旗子：旗桿從右手位開始、向上 56px、外傾 15°
    flag_base_x, flag_base_y = 503, 460
    # 向上 56px 並外傾 15° (sin(15°)≈0.259, cos(15°)≈0.966)
    flag_top_x = flag_base_x + int(56 * 0.259)
    flag_top_y = flag_base_y - int(56 * 0.966)
    e.append(f'<line x1="{flag_base_x}" y1="{flag_base_y}" x2="{flag_top_x}" y2="{flag_top_y}" '
             f'stroke="#8A5A2B" stroke-width="3" stroke-linecap="round"/>')
    # 三角旗（貼在桿頂）
    e.append(f'<polygon points="{flag_top_x},{flag_top_y} {flag_top_x+24},{flag_top_y} {flag_top_x+18},{flag_top_y+20}" '
             f'fill="{HEAD_START_FLAG_GOLD}" stroke="#8A5A2B" stroke-width="2"/>')

    # 徽章（身旁，浮空低於下巴且不碰身體）
    e.append(teacher_badge(750, 320, scale=1.1))

    return svg(W, H, "".join(e), bg=None)


# ================== PAGES & METADATA ==================

PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I practiced a lot. I know a lot!'),
    ("p2", scene_p2, 'Tr. Mina teaches two plus three.<br/>I learned this long ago!'),
    ("p3", scene_p3, 'This is <b>easy</b> for me!<br/>The words want to jump out!'),
    ("p4", scene_p4, '&ldquo;So <b>easy</b>!&rdquo; jumps to my mouth!<br/>My nose points up, up, up.<br/>My friends look down. The room goes quiet.'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I just started early, that is all!'),
    ("p6", scene_p6, 'Catch my <b>brag</b>&mdash;zip!<br/>They are learning, like I did.<br/>I ask, &ldquo;Can I help?&rdquo;'),
    ("p7", scene_p7, 'Everyone runs the same road.<br/>My friends will get there too.<br/>Helping feels better than bragging!'),
    ("p8", scene_p8, 'Tr. Mina says yes. I help softly.<br/>My friend says, &ldquo;Oh! I get it!&rdquo;<br/>&ldquo;Super little teacher, <b>Owen</b>!&rdquo;'),
    ("p9", scene_p9, 'My friend gets it now!<br/>Teaching makes my smart shine.<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Catch my brag. I started early.<br/>Help like a teacher!<br/><b>Little teacher!</b> I practice every day!'),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3–4 次，重複讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "被反映上課喊無聊或炫耀的當天不讀不罵，平靜時再讀。"),
    ("歸因改造是地基", "在家把「你好聰明」換成「你練了很久所以會」。他嫌簡單時不否認，回「對，因為你先練過——那這題你能做得更快更漂亮嗎？」"),
    ("與 Tr. Mina 對暗號", "他喊 So easy 或坐不住時提醒「Little teacher?」——邀請進入幫手身份。規矩：老師同意＋同學願意才教。"),
    ("當他主動說 'So easy jumps to my mouth'", "覺察里程碑，大力稱讚——他察覺衝動訊號了。"),
    ("當他輕聲幫了同學一題", "稱讚點放在「你幫他學會了」而不是「你好棒」——持續把「被看見」餵給親社會成就。"),
]

BOOK = {
    "slug": "little-teacher",
    "order": 21,
    "title_pre": "", "title_hi": "Little Teacher", "title_post": "!",
    "title_zh": "小小老師",
    "subtitle": "Owen's helping story",
    "tagline_zh": "課堂內容太簡單時的自大反應→抓住炫耀→當小老師幫忙",
    "chips": ["Social Story", "Classroom", "12 pages"],
    "pdf_name": "Little_Teacher.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ["easy", "brag"],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。本書教的不是「不要炫耀」，"
                     "而是替 Owen 安裝一套<b>課堂內輕聲幫忙的正向替代腳本</b>："
                     "發現內容太簡單的衝動 → 抓住想炫耀的聲音 → 想起「我只是先出發」 → "
                     "轉身當小老師幫同學。目標是<b>不否認他的能力</b>（能力是真的、來自練習），"
                     "把「想被看見」的需求從炫耀改道到「小老師」的榮譽身份。"),
    "cue_html": ("口訣（全書通關密語）：<b>Catch my brag → Remember my head start → Help like a teacher!</b>&nbsp;"
                 "完整三部曲是「Catch my brag（抓住炫耀）→ Remember my head start（想起我先出發）→ Help like a teacher!（當小老師幫忙）」。"
                 "老師現場提醒時只說 <b>'Little teacher?'</b> 一個字，邀請他進入幫手身份，不是斥責。"),
    "cover": scene_cover,
}
