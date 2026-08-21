# -*- coding: utf-8 -*-
"""Book 19: Ears On! — 上課想講話想玩的衝動（跟鄰座聊天→被制止改玩文具→自言自語）
導致漏聽老師講的內容、練習考卷寫不出教過的部分。
安裝「嘴拉上→手休息→耳朵開機」的正向替代腳本。
核心意象：話語星星——Tr. Mina 講課時話語化作小星星飄出，耳朵開機就接住；分心時星星掉地上消失。"""
import math
from parts import *
from book_common import svg, svgtext, TXT, W, H

# soft page palettes (教室+專心主題)
BG = {
    "cover": "#FFF8E8", "p1": "#E8F4FF", "p2": "#FFF3D6", "p3": "#FFE8E8",
    "p4": "#FFE8D6", "p5": "#D7C8FF", "p6": "#FFE9A8", "p7": "#E8F8D8",
    "p8": "#FFF0C9", "p9": "#FFE2EC", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

# 話語星星色彩
STAR_WORD_GOLD = "#F0B429"
STAR_WORD_LIGHT = "#FFD93D"

# ================== 【規格 A】耳朵光暈 ==================
def ear_glow_spec_a(cx, cy, s=1.0):
    """【規格 A】耳朵光暈，疊在角色「原生耳朵」的位置上。
    座標換算：head/head_with_zipper 的耳朵在 (cx±56*s, cy+6*s)；
    boy_bust 的耳朵在 (cx±56*s, cy-4*s)；boy 的耳朵在 (cx±56*s, cy+13*s)。"""
    return (f'<circle cx="{cx}" cy="{cy}" r="{20*s}" fill="#FFE9A8" fill-opacity="0.45"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{12*s}" fill="#FFE9A8" fill-opacity="0.7"/>')


def zipper_badge(cx, cy, s=1.0):
    """【規格 B】嘴巴拉鍊（獨立元件，疊在嘴的位置上）。
    boy() 的嘴中心在 (cx, cy+34*s)；head 系的嘴中心在 (cx, cy+30*s)。"""
    z = []
    z.append(f'<ellipse cx="0" cy="0" rx="36" ry="12" fill="{STAR_WORD_GOLD}" fill-opacity="0.2"/>')
    z.append(f'<rect x="-30" y="-3" width="60" height="6" rx="3" fill="{STAR_WORD_GOLD}" stroke="#8A5A2B" stroke-width="1.5"/>')
    for i in range(8):
        x = -26 + i * 7.5
        dy = 0 if i % 2 == 0 else 1
        z.append(f'<rect x="{x-1.5}" y="{-7+dy}" width="3" height="3" fill="{STAR_WORD_GOLD}" stroke="#8A5A2B" stroke-width="0.8"/>')
        z.append(f'<rect x="{x-1.5}" y="{4+dy}" width="3" height="3" fill="{STAR_WORD_GOLD}" stroke="#8A5A2B" stroke-width="0.8"/>')
    z.append(f'<circle cx="33" cy="0" r="4.5" fill="{STAR_WORD_GOLD}" stroke="#8A5A2B" stroke-width="1.5"/>')
    return f'<g transform="translate({cx},{cy}) scale({s})">{"".join(z)}</g>'

# ================== 【規格 B】嘴巴拉鍊（內置 head() 調用） ==================
def head_with_zipper(expr="smile", scale=1.0, cx=0, cy=0, use_zipper=False):
    """改造版 head()，支持 use_zipper=True 時用拉鍊替代嘴。
    位置：嘴部 y≈10..18（head 局部座標），寬約臉寬 55%（≈61px）。
    返回含拉鍊的頭部 SVG。"""
    e = []
    # ears
    e.append(f'<circle cx="-56" cy="6" r="12" fill="{SKIN}"/>')
    e.append(f'<circle cx="56" cy="6" r="12" fill="{SKIN}"/>')
    # face
    e.append(f'<ellipse cx="0" cy="0" rx="56" ry="52" fill="{SKIN}"/>')
    # hair dome + straight bangs
    e.append(f'<path d="M -56 6 C -60 -62 60 -62 56 6 L 56 -6 '
             f'Q 44 -22 34 -14 Q 24 -24 12 -16 Q 0 -26 -12 -16 Q -24 -24 -34 -14 Q -44 -22 -56 -6 Z" fill="{HAIR}"/>')
    # side hair
    e.append(f'<path d="M -56 -4 Q -60 10 -54 18 L -48 6 Z" fill="{HAIR}"/>')
    e.append(f'<path d="M 56 -4 Q 60 10 54 18 L 48 6 Z" fill="{HAIR}"/>')
    # glasses
    e.append(f'<line x1="-50" y1="-2" x2="-56" y2="2" stroke="#E8944A" stroke-width="6" stroke-linecap="round"/>')
    e.append(f'<line x1="50" y1="-2" x2="56" y2="2" stroke="#E8944A" stroke-width="6" stroke-linecap="round"/>')
    e.append(f'<circle cx="-27" cy="0" r="22" fill="#FFFFFF" fill-opacity="0.25" stroke="#161616" stroke-width="7"/>')
    e.append(f'<circle cx="27" cy="0" r="22" fill="#FFFFFF" fill-opacity="0.25" stroke="#161616" stroke-width="7"/>')
    e.append(f'<path d="M -6 -2 Q 0 -7 6 -2" fill="none" stroke="#161616" stroke-width="6" stroke-linecap="round"/>')

    # brows / eyes per expression
    if expr in ("smile", "proud"):
        e.append(f'<path d="M -36 -26 Q -27 -31 -18 -26" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 18 -26 Q 27 -31 36 -26" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M -34 2 Q -27 -7 -20 2" fill="none" stroke="{LINE}" stroke-width="5.5" stroke-linecap="round"/>')
        e.append(f'<path d="M 20 2 Q 27 -7 34 2" fill="none" stroke="{LINE}" stroke-width="5.5" stroke-linecap="round"/>')
    elif expr == "press":
        e.append(f'<path d="M -36 -30 Q -27 -26 -18 -28" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 18 -28 Q 27 -26 36 -30" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<circle cx="-27" cy="0" r="5.5" fill="{LINE}"/><circle cx="27" cy="0" r="5.5" fill="{LINE}"/>')

    # nose
    e.append(f'<path d="M -3 14 Q 0 18 3 14" fill="none" stroke="{SKIN_DK}" stroke-width="4" stroke-linecap="round"/>')

    # blush
    e.append(f'<ellipse cx="-40" cy="18" rx="9" ry="6" fill="{BLUSH}" fill-opacity="0.75"/>')
    e.append(f'<ellipse cx="40" cy="18" rx="9" ry="6" fill="{BLUSH}" fill-opacity="0.75"/>')

    # mouth: zipper or normal
    if use_zipper:
        # 【規格 B】拉鍊代替嘴——畫在嘴的位置（local y≈30，非鼻子高度）
        e.append(zipper_badge(0, 30, 1.0))
    else:
        # 原本的嘴（smile 表情）
        if expr in ("smile", "proud"):
            e.append(f'<path d="M -18 26 Q 0 42 18 26 Q 0 34 -18 26 Z" fill="#8C4A3C"/>')
            e.append(f'<path d="M -14 27 Q 0 33 14 27 L 12 30 Q 0 35 -12 30 Z" fill="#FFFFFF"/>')
        elif expr == "press":
            e.append(f'<path d="M -16 29 Q 0 24 16 29" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>')
            e.append(f'<path d="M -6 40 Q 0 43 6 40" fill="none" stroke="{SKIN_DK}" stroke-width="4" stroke-linecap="round"/>')

    inner = "".join(e)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'

# ================== HELPER FUNCTIONS ==================

def speech_star(cx, cy, scale=1.0, opacity=1.0):
    """話語星星（金黃色，帶外圍光暈）。"""
    s = []
    s.append(f'<circle cx="0" cy="0" r="14" fill="{STAR_WORD_LIGHT}" fill-opacity="{opacity*0.3}"/>')
    s.append(f'<polygon points="{star_pts(0, 0, 10)}" fill="{STAR_WORD_LIGHT}" stroke="{STAR_WORD_GOLD}" stroke-width="2"/>')
    return f'<g transform="translate({cx},{cy}) scale({scale})" opacity="{opacity}">{"".join(s)}</g>'

def star_trail(x1, y1, x2, y2, opacity=1.0):
    """虛線軌跡（星星飄行路徑）。"""
    return f'<path d="M {x1} {y1} Q {(x1+x2)//2} {(y1+y2)//2-30} {x2} {y2}" fill="none" stroke="{STAR_WORD_GOLD}" stroke-width="2" stroke-dasharray="4 6" opacity="{opacity}"/>'

def test_paper(cx, cy, w=120, h=160, scale=1.0):
    """練習考卷（白紙+灰色橫線題目+紅色小數字）。"""
    p = []
    p.append(f'<rect x="{-w//2}" y="{-h//2}" width="{w}" height="{h}" rx="4" fill="#FFFFFF" stroke="#D4B8A0" stroke-width="2"/>')
    for i in range(5):
        y = -h//2 + 20 + i * 28
        p.append(f'<line x1="{-w//2+8}" y1="{y}" x2="{w//2-8}" y2="{y}" stroke="#CCCCCC" stroke-width="1.5"/>')
        p.append(f'<text x="{-w//2+4}" y="{y+4}" font-family="Huninn" font-size="14" fill="#E8574C" font-weight="bold">{i+1}</text>')
    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(p)}</g>'

def desk(cx, cy, w=220, scale=1.0):
    """課桌（棕色長方形+腿）。"""
    d = []
    d.append(f'<rect x="{-w//2}" y="-15" width="{w}" height="30" rx="8" fill="#D9B98C" stroke="#B08A56" stroke-width="3"/>')
    d.append(f'<line x1="{-w//2+30}" y1="15" x2="{-w//2+30}" y2="50" stroke="#8B6F47" stroke-width="6" stroke-linecap="round"/>')
    d.append(f'<line x1="{w//2-30}" y1="15" x2="{w//2-30}" y2="50" stroke="#8B6F47" stroke-width="6" stroke-linecap="round"/>')
    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(d)}</g>'

# ================== SCENES ==================

def scene_cover():
    """【修正】封面：Owen 白T 走進教室，頭上一個大思考泡泡（內含 icon），刪掉懸空木板與文字。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="620" fill="{BG["cover"]}"/>')

    # 牆面色帶（交代依附）
    e.append(f'<rect x="0" y="0" width="1188" height="450" fill="#F5E8D8"/>')  # 牆面
    e.append(f'<ellipse cx="594" cy="620" rx="560" ry="120" fill="#E8D2AC"/>')  # 地板

    # 黑板框（有牆帶依附）
    e.append(f'<rect x="80" y="60" width="200" height="140" rx="10" fill="#C9A26B"/>')
    e.append(f'<rect x="100" y="80" width="160" height="100" rx="6" fill="#3E7C5B"/>')

    # Owen 走進（規格 C：腳落在 y=470）
    e.append(boy(pose="walk", expr="big", cx=350, cy=300, scale=1.2))

    # 一個大思考泡泡（聚在 Owen 頭上）
    bubble_cx, bubble_cy = 500, 100
    e.append(f'<circle cx="{bubble_cx}" cy="{bubble_cy}" r="75" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="4"/>')
    # 兩顆小圓點尾巴接向頭
    e.append(f'<circle cx="440" cy="160" r="12" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="3"/>')
    e.append(f'<circle cx="420" cy="190" r="8" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2"/>')
    # 泡泡內容：三個 icon（不放文字）
    e.append(f'<polygon points="{star_pts(bubble_cx-25, bubble_cy-10, 14)}" fill="#FFD93D" stroke="#F0B429" stroke-width="2"/>')  # 星星
    e.append(f'<circle cx="{bubble_cx}" cy="{bubble_cy-10}" r="16" fill="#7BC47F" fill-opacity="0.7"/>')  # 恐龍圓
    e.append(svgtext(bubble_cx, bubble_cy, "🦕", size=18))
    e.append(f'<circle cx="{bubble_cx+25}" cy="{bubble_cy-10}" r="16" fill="#FF6B6B" fill-opacity="0.7"/>')  # 球圓
    e.append(svgtext(bubble_cx+25, bubble_cy, "⚽", size=18))

    # 星星裝飾
    e.append(star(200, 300, 16, fill=STAR_Y))
    e.append(star(1000, 350, 18, fill=STAR_Y))

    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """【修正】p1：Owen 開心站立（規格 C），黑板加牆帶。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p1"]}"/>')
    e.append(f'<rect x="0" y="0" width="1188" height="430" fill="#F5E8D8"/>')  # 牆面
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D9B98C"/>')  # 地板（規格 C：y=430..560）

    # 黑板（有牆帶依附）
    e.append(f'<rect x="80" y="80" width="200" height="120" rx="8" fill="#C9A26B"/>')
    e.append(f'<rect x="98" y="100" width="164" height="80" rx="4" fill="#3E7C5B"/>')

    # Owen 開心站立（腳落 y=470）
    e.append(boy(pose="stand", expr="big", cx=350, cy=280, scale=1.15))

    # 頭上大思考泡泡（同封面風格）
    bubble_cx, bubble_cy = 480, 120
    e.append(f'<circle cx="{bubble_cx}" cy="{bubble_cy}" r="70" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="4"/>')
    e.append(f'<circle cx="420" cy="180" r="10" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2"/>')
    e.append(f'<circle cx="400" cy="210" r="7" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2"/>')
    # 內容
    e.append(f'<polygon points="{star_pts(bubble_cx-20, bubble_cy-10, 12)}" fill="#FFD93D" stroke="#F0B429" stroke-width="2"/>')
    e.append(f'<circle cx="{bubble_cx}" cy="{bubble_cy}" r="14" fill="#7BC47F" fill-opacity="0.7"/>')
    e.append(svgtext(bubble_cx, bubble_cy, "🦕", size=16))
    e.append(f'<circle cx="{bubble_cx+20}" cy="{bubble_cy-10}" r="14" fill="#FF6B6B" fill-opacity="0.7"/>')
    e.append(svgtext(bubble_cx+20, bubble_cy, "⚽", size=16))

    # 星星裝飾
    e.append(star(180, 100, 18, fill=STAR_Y))
    e.append(star(1000, 150, 16, fill=STAR_Y))

    return svg(W, H, "".join(e))


def scene_p2():
    """【修正】p2：Tr. Mina 講課（星星起點在嘴邊），Owen+Ethan 各自課桌（身高相當），Owen 耳暈規格 A。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p2"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D9B98C"/>')  # 地板（規格 C）

    # 黑板
    e.append(f'<rect x="340" y="60" width="510" height="280" rx="12" fill="#C9A26B"/>')
    e.append(f'<rect x="358" y="80" width="474" height="240" rx="8" fill="#3E7C5B"/>')
    e.append(svgtext(595, 200, "Let's learn!", size=70, fill="#FFF7E0", weight="bold"))

    # Tr. Mina 講課，指著黑板
    e.append(teacher(cx=180, cy=280, scale=1.0, point="right"))

    # 話語星星群（起點在 Tr. Mina 嘴邊）
    star_positions = [(240, 200, 500, 120), (270, 180, 650, 80), (300, 200, 800, 120)]
    for sx, sy, ex, ey in star_positions:
        e.append(star_trail(sx, sy, ex, ey, opacity=0.6))
        e.append(speech_star(ex, ey, scale=0.85))

    # Owen 課桌 + 半身
    owen_desk_cx, owen_desk_cy = 800, 350
    e.append(desk(cx=owen_desk_cx, cy=owen_desk_cy, w=180, scale=0.9))
    e.append(boy_bust(expr="star", cx=owen_desk_cx, cy=250, scale=0.8, arms="desk"))
    # Owen 耳暈（規格 A，bust 耳位 cx±56*0.8, cy-4*0.8）
    e.append(ear_glow_spec_a(owen_desk_cx-45, 247, s=0.8))
    e.append(ear_glow_spec_a(owen_desk_cx+45, 247, s=0.8))

    # Ethan 課桌 + 半身（身高相當，cx 偏右）
    ethan_desk_cx, ethan_desk_cy = 1020, 350
    e.append(desk(cx=ethan_desk_cx, cy=ethan_desk_cy, w=180, scale=0.9))
    e.append(ethan(cx=ethan_desk_cx, cy=270, scale=0.8, expr="think"))

    return svg(W, H, "".join(e))


def scene_p3():
    """【修正】p3：思考泡泡尾巴連向 Owen 的頭，Ethan 有自己的課桌。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p3"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D9B98C"/>')  # 地板

    # Owen 課桌 + 半身
    owen_desk_cx, owen_desk_cy = 320, 350
    e.append(desk(cx=owen_desk_cx, cy=owen_desk_cy, w=180, scale=0.85))
    e.append(boy_bust(expr="star", cx=owen_desk_cx, cy=250, scale=0.8, arms="desk"))

    # Ethan 課桌 + 半身
    ethan_desk_cx, ethan_desk_cy = 700, 350
    e.append(desk(cx=ethan_desk_cx, cy=ethan_desk_cy, w=180, scale=0.85))
    e.append(ethan(cx=ethan_desk_cx, cy=270, scale=0.8, expr="smile"))

    # 思考泡泡（連向 Owen 頭）
    bubble_cx, bubble_cy = 450, 140
    e.append(f'<circle cx="{bubble_cx}" cy="{bubble_cy}" r="65" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="4"/>')
    # 尾巴指向 Owen 頭
    e.append(f'<path d="M 400 190 Q 380 230 360 280" fill="none" stroke="#D9B6E8" stroke-width="3" stroke-linecap="round"/>')
    # 內容
    e.append(f'<polygon points="{star_pts(bubble_cx-18, bubble_cy-10, 11)}" fill="#FFD93D" stroke="#F0B429" stroke-width="2"/>')
    e.append(f'<circle cx="{bubble_cx}" cy="{bubble_cy}" r="13" fill="#7BC47F" fill-opacity="0.7"/>')
    e.append(svgtext(bubble_cx, bubble_cy, "🦕", size=14))
    e.append(f'<circle cx="{bubble_cx+18}" cy="{bubble_cy-10}" r="13" fill="#FF6B6B" fill-opacity="0.7"/>')
    e.append(svgtext(bubble_cx+18, bubble_cy, "⚽", size=14))

    # 星星裝飾
    e.append(star(150, 100, 16, fill=STAR_Y))
    e.append(star(1000, 120, 14, fill=STAR_Y))

    return svg(W, H, "".join(e))


def scene_p4():
    """【修正】p4：三格放大，人物大半身、腳落格內地面線。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p4"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D9B98C"/>')  # 地板

    # 三個格子（放大）
    grid_positions = [(280, 280), (594, 280), (908, 280)]
    grid_w, grid_h = 240, 260

    for idx, (gx, gy) in enumerate(grid_positions):
        # 格子邊框
        e.append(f'<rect x="{gx-grid_w//2}" y="{gy-grid_h//2}" width="{grid_w}" height="{grid_h}" rx="14" fill="none" stroke="#D4B8A0" stroke-width="4"/>')

        if idx == 0:  # ①Chat
            e.append(f'<text x="{gx}" y="{gy-140}" font-family="Huninn" font-size="20" font-weight="bold" fill="#4A4A4A" text-anchor="middle">① Chat</text>')
            desk_x = gx - 50
            desk_y = gy + 60
            e.append(desk(cx=desk_x, cy=desk_y, w=160, scale=0.8))
            e.append(boy_bust(expr="big", cx=desk_x, cy=gy-30, scale=0.75, arms="desk"))
            ethan_x = gx + 60
            e.append(ethan(cx=ethan_x, cy=gy-10, scale=0.75, expr="think"))
            # 對話泡泡（兩人頭上方空隙）
            bubble_x, bubble_y = gx + 10, gy - 90
            e.append(f'<path d="M {bubble_x-40} {bubble_y} L {bubble_x-60} {bubble_y-30} L {bubble_x+60} {bubble_y-30} Q {bubble_x+75} {bubble_y-30} {bubble_x+75} {bubble_y-15} Q {bubble_x+75} {bubble_y} {bubble_x+55} {bubble_y} Q {bubble_x} {bubble_y+35} {bubble_x-40} {bubble_y} Z" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2.5"/>')
            e.append(svgtext(bubble_x, bubble_y-15, "blah blah", size=16, fill="#8B7355", weight="bold"))
            # 掉地上的星星
            e.append(speech_star(gx-40, gy+100, scale=0.55, opacity=0.35))
            e.append(speech_star(gx+30, gy+110, scale=0.5, opacity=0.35))

        elif idx == 1:  # ②Play
            e.append(f'<text x="{gx}" y="{gy-140}" font-family="Huninn" font-size="20" font-weight="bold" fill="#4A4A4A" text-anchor="middle">② Play</text>')
            desk_x = gx
            desk_y = gy + 60
            e.append(desk(cx=desk_x, cy=desk_y, w=160, scale=0.8))
            e.append(boy_bust(expr="smile", cx=desk_x, cy=gy-30, scale=0.75, arms="desk"))
            # 文具在桌面上彈跳（不飄在頭旁）：鉛筆＋橡皮擦＋小弧線
            table_top = desk_y - 14
            e.append(f'<line x1="{desk_x-52}" y1="{table_top-8}" x2="{desk_x-20}" y2="{table_top-16}" stroke="#D4A574" stroke-width="5" stroke-linecap="round"/>')
            e.append(f'<polygon points="{desk_x-56},{table_top-6} {desk_x-52},{table_top-12} {desk_x-49},{table_top-5}" fill="#4A4A4A"/>')
            e.append(f'<rect x="{desk_x+30}" y="{table_top-16}" width="18" height="11" rx="3" fill="#FFB6A0" stroke="#E8917A" stroke-width="1.5"/>')
            # 搖動小弧線（在文具上方、遠低於頭部）
            e.append(f'<path d="M {desk_x-46} {table_top-26} q 8 -6 16 0" stroke="#F26B5E" stroke-width="2" fill="none" opacity="0.7"/>')
            e.append(f'<path d="M {desk_x+32} {table_top-24} q 7 -5 14 0" stroke="#F26B5E" stroke-width="2" fill="none" opacity="0.7"/>')
            # 掉地上的星星
            e.append(speech_star(gx-30, gy+105, scale=0.52, opacity=0.35))

        else:  # ③Blah
            e.append(f'<text x="{gx}" y="{gy-140}" font-family="Huninn" font-size="20" font-weight="bold" fill="#4A4A4A" text-anchor="middle">③ Blah</text>')
            desk_x = gx
            desk_y = gy + 60
            e.append(desk(cx=desk_x, cy=desk_y, w=160, scale=0.8))
            e.append(boy_bust(expr="think", cx=desk_x, cy=gy-30, scale=0.75, arms="desk"))
            # 小 blah 泡泡（在嘴邊，不壓頭）
            bubble_x, bubble_y = desk_x + 50, gy - 10
            e.append(f'<path d="M {bubble_x-20} {bubble_y-10} Q {bubble_x+10} {bubble_y-25} {bubble_x+30} {bubble_y-10} Q {bubble_x+20} {bubble_y+10} {bubble_x} {bubble_y+10} Z" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2" opacity="0.85"/>')
            e.append(svgtext(bubble_x+5, bubble_y, "blah...", size=12, fill="#8B7355"))
            # 掉地上的星星
            e.append(speech_star(gx+40, gy+100, scale=0.5, opacity=0.35))

    return svg(W, H, "".join(e))


def scene_p5():
    """【修正】p5：星空背景，Owen press 表情，拉鍊嘴（規格 B）在嘴位置，耳朵光暈（規格 A）。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#4A3A5C"/>')

    # 星星散佈（星空）
    for (x, y, r) in [(150, 80, 16), (1030, 100, 20), (200, 440, 14), (1000, 420, 16), (450, 150, 12), (950, 340, 14)]:
        e.append(star(x, y, r, fill="#E8D9FF"))
    for (sx, sy, sr) in [(320, 90, 12), (860, 80, 12), (90, 300, 10), (1100, 300, 10), (600, 50, 10)]:
        e.append(sparkle(sx, sy, sr, fill="#E8D9FF"))

    # Owen 大頭特寫（超能力頁聚焦「拉鍊嘴＋耳朵開機」）——不畫身體，避免拼裝解體
    e.append(head_with_zipper(expr="press", scale=1.6, cx=594, cy=260, use_zipper=True))
    # 雙耳光暈（規格 A，疊在原生耳朵位置：cx±56*1.6, cy+6*1.6）
    e.append(ear_glow_spec_a(594 - 90, 270, s=1.4))
    e.append(ear_glow_spec_a(594 + 90, 270, s=1.4))

    # 身旁環繞的小星星（被接住）
    surrounding_stars = [(400, 180), (500, 120), (690, 120), (790, 180), (370, 340), (480, 430), (710, 430), (820, 340)]
    for sx, sy in surrounding_stars:
        e.append(speech_star(sx, sy, scale=0.7, opacity=0.9))

    return svg(W, H, "".join(e))


def scene_p6():
    """【修正】p6：三步腳本重畫。①parts.head 完整頭+拉鍊+zzzip ②課桌+交疊雙手 ③parts.head 完整頭+耳暈+星星飛進。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p6"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D9B98C"/>')  # 地板

    # 三個圓形標誌（頂部）
    for i, label in enumerate(["①", "②", "③"]):
        cx = 280 + i * 320
        e.append(f'<circle cx="{cx}" cy="50" r="30" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="3"/>')
        e.append(svgtext(cx, 62, label, size=36, fill="#D9B6E8", weight="bold"))

    # ① 拉鍊嘴特寫：parts.head() 完整頭 + 拉鍊 + zzzip 字效
    mouth_cx, mouth_cy = 280, 200
    e.append(head_with_zipper(expr="press", scale=1.15, cx=mouth_cx, cy=mouth_cy, use_zipper=True))
    e.append(svgtext(mouth_cx, 310, "zzzip!", size=32, fill=STAR_WORD_GOLD, weight="bold"))

    # ② 課桌面特寫 + 交疊雙手（手臂從下方伸上來，手掌交疊在桌面上）
    hands_cx, hands_cy = 594, 200
    desk_top = hands_cy + 55  # 桌面頂 y
    e.append(desk(cx=hands_cx, cy=hands_cy+70, w=200, scale=1.0))
    # 兩截白袖手臂（有依附，不是懸空的蛋）
    e.append(f'<path d="M {hands_cx-70} {desk_top+60} Q {hands_cx-52} {desk_top+20} {hands_cx-20} {desk_top-2}" stroke="#FFFFFF" stroke-width="20" stroke-linecap="round" fill="none"/>')
    e.append(f'<path d="M {hands_cx+70} {desk_top+60} Q {hands_cx+52} {desk_top+20} {hands_cx+20} {desk_top-2}" stroke="#FFFFFF" stroke-width="20" stroke-linecap="round" fill="none"/>')
    # 交疊的手掌（下掌＋上掌斜疊＋指縫線）
    e.append(f'<ellipse cx="{hands_cx-8}" cy="{desk_top-4}" rx="24" ry="15" fill="{SKIN}" transform="rotate(-12 {hands_cx-8} {desk_top-4})"/>')
    e.append(f'<ellipse cx="{hands_cx+10}" cy="{desk_top-8}" rx="24" ry="15" fill="{SKIN}" stroke="#E8B48C" stroke-width="1.5" transform="rotate(12 {hands_cx+10} {desk_top-8})"/>')
    for fx in (-2, 8, 18):
        e.append(f'<path d="M {hands_cx+fx} {desk_top-16} q 3 6 1 11" stroke="#E8B48C" stroke-width="1.5" fill="none"/>')
    # 小光點
    e.append(f'<circle cx="{hands_cx-26}" cy="{desk_top-24}" r="5" fill="#F0B429" opacity="0.8"/>')
    e.append(f'<circle cx="{hands_cx+30}" cy="{desk_top-26}" r="5" fill="#F0B429" opacity="0.8"/>')

    # ③ 耳朵特寫發光：parts.head() 完整頭 + 耳暈 + 星星飛進
    ear_cx, ear_cy = 908, 200
    e.append(head_with_zipper(expr="smile", scale=1.15, cx=ear_cx, cy=ear_cy, use_zipper=False))
    # 耳暈（規格 A，疊在原生耳朵位置 cx±56*1.15, cy+6*1.15）
    e.append(ear_glow_spec_a(ear_cx-64, ear_cy+7, s=1.1))
    e.append(ear_glow_spec_a(ear_cx+64, ear_cy+7, s=1.1))
    # 星星飛進耳朵（虛線軌跡終點對耳位）
    e.append(star_trail(ear_cx-150, ear_cy-40, ear_cx-78, ear_cy+2, opacity=0.8))
    e.append(speech_star(ear_cx-120, ear_cy-32, scale=0.7, opacity=0.9))
    e.append(star_trail(ear_cx+150, ear_cy-40, ear_cx+78, ear_cy+2, opacity=0.8))
    e.append(speech_star(ear_cx+120, ear_cy-32, scale=0.7, opacity=0.9))

    return svg(W, H, "".join(e))


def scene_p7():
    """【修正】p7：左格真頭+耳暈+星星排排，右格真頭+課卷放桌上（不懸空）。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p7"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D9B98C"/>')  # 地板

    # 左格：Owen 頭部特寫 + 耳暈 + 星星排排
    left_cx = 350
    e.append(f'<rect x="{left_cx-140}" y="80" width="280" height="320" rx="12" fill="none" stroke="#D4B8A0" stroke-width="3"/>')
    # 真頭
    e.append(head_with_zipper(expr="smile", scale=1.0, cx=left_cx, cy=150, use_zipper=False))
    # 耳暈（規格 A，耳位 cy+6）
    e.append(ear_glow_spec_a(left_cx-56, 156))
    e.append(ear_glow_spec_a(left_cx+56, 156))
    # 耳朵旁排排的小星星（收集完成）
    star_lineup = [(left_cx-75, 100), (left_cx-75, 145), (left_cx-75, 190),
                   (left_cx+75, 100), (left_cx+75, 145), (left_cx+75, 190)]
    for sx, sy in star_lineup:
        e.append(speech_star(sx, sy, scale=0.6, opacity=0.85))

    # 右格：Owen 坐著 + 課卷放桌上（加寬桌面）
    right_cx = 850
    e.append(f'<rect x="{right_cx-140}" y="80" width="280" height="320" rx="12" fill="none" stroke="#D4B8A0" stroke-width="3"/>')
    # 課桌面特寫（寬桌）
    desk_w = 240
    e.append(desk(cx=right_cx, cy=280, w=desk_w, scale=0.95))
    # 考卷平放在桌面上（微傾）
    e.append(test_paper(cx=right_cx, cy=280, w=130, h=150, scale=0.95))
    # 星星虛線從左格頭部飛向右格考卷
    star_paths = [
        ((left_cx-75, 100), (right_cx-50, 240)),
        ((left_cx, 100), (right_cx, 220)),
        ((left_cx+75, 100), (right_cx+50, 240)),
    ]
    for (sx, sy), (ex, ey) in star_paths:
        e.append(star_trail(sx, sy, ex, ey, opacity=0.7))
        e.append(speech_star(ex, ey, scale=0.68, opacity=0.9))
    # 綠色小勾（考卷上）
    e.append(svgtext(right_cx-35, 260, "✓", size=24, fill="#7BC47F", weight="bold"))
    e.append(svgtext(right_cx+20, 300, "✓", size=24, fill="#7BC47F", weight="bold"))

    # Tr. Mina 在左邊微笑
    e.append(teacher(cx=150, cy=320, scale=0.8, point="right"))

    return svg(W, H, "".join(e))


def scene_p8():
    """【修正】p8：語音泡泡移到 Tr. Mina 頭右側、尾巴指向她的嘴，Ethan 課桌，Owen 耳暈。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p8"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D9B98C"/>')  # 地板

    # 黑板
    e.append(f'<rect x="80" y="60" width="280" height="180" rx="10" fill="#C9A26B"/>')
    e.append(f'<rect x="104" y="84" width="232" height="132" rx="6" fill="#3E7C5B"/>')
    e.append(svgtext(220, 160, "Great!", size=60, fill="#FFF7E0", weight="bold"))

    # Tr. Mina 講課，指著黑板
    mina_cx, mina_cy = 180, 280
    e.append(teacher(cx=mina_cx, cy=mina_cy, scale=1.0, point="right"))

    # 語音泡泡（移到 Tr. Mina 頭右側）
    bubble_x, bubble_y = 450, 120
    e.append(f'<path d="M 380 140 Q 420 100 520 100 L 600 100 Q 640 100 640 140 Q 640 180 600 180 L 480 220 L 520 180 L 440 180 Q 380 180 380 140 Z" fill="#FFFFFF" stroke="#E3C98F" stroke-width="4"/>')
    # 尾巴指向 Tr. Mina 的嘴（約 200, 250）
    e.append(f'<line x1="380" y1="140" x2="220" y2="240" stroke="#E3C98F" stroke-width="3" stroke-linecap="round"/>')
    e.append(svgtext(510, 145, "Super ears, Owen!", size=28, fill="#D97706", weight="bold"))

    # 話語星星群（起點在 Tr. Mina 嘴邊）
    star_positions = [(240, 210, 500, 100), (270, 190, 650, 80), (300, 210, 800, 120)]
    for sx, sy, ex, ey in star_positions:
        e.append(star_trail(sx, sy, ex, ey, opacity=0.6))
        e.append(speech_star(ex, ey, scale=0.8))

    # Owen 課桌 + 半身
    owen_desk_cx, owen_desk_cy = 930, 350
    e.append(desk(cx=owen_desk_cx, cy=owen_desk_cy, w=200, scale=1.0))
    e.append(boy_bust(expr="smile", cx=owen_desk_cx, cy=250, scale=0.85, arms="desk"))
    # Owen 耳暈（規格 A，bust 耳位）
    e.append(ear_glow_spec_a(owen_desk_cx-48, 247, s=0.85))
    e.append(ear_glow_spec_a(owen_desk_cx+48, 247, s=0.85))

    # Ethan 課桌 + 半身
    ethan_desk_cx, ethan_desk_cy = 1100, 350
    e.append(desk(cx=ethan_desk_cx, cy=ethan_desk_cy, w=180, scale=0.9))
    e.append(ethan(cx=ethan_desk_cx, cy=270, scale=0.8, expr="think"))

    return svg(W, H, "".join(e))


def scene_p9():
    """【修正】p9：考卷放課桌桌面上（加寬、平放微傾），耳暈規格 A。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p9"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D9B98C"/>')  # 地板

    # 彩帶裝飾（頂部）
    import random
    random.seed(9)
    cols = ["#F6C445", "#7BC47F", "#6FA8DC", "#F49AB5", "#E4574C"]
    for i in range(20):
        x, y = random.randint(50, 1138), random.randint(20, 180)
        c = cols[i % 5]
        e.append(f'<rect x="{x}" y="{y}" width="8" height="12" rx="2" fill="{c}" transform="rotate({random.randint(-40,40)} {x} {y})"/>')

    # Owen 挺胸開心（坐著）
    desk_cx, desk_cy = 420, 350
    e.append(desk(cx=desk_cx, cy=desk_cy, w=240, scale=1.0))  # 加寬桌面
    owen_cx = desk_cx - 65  # 人靠桌左端，避免右側考卷壓到頭
    e.append(boy_bust(expr="proud", cx=owen_cx, cy=250, scale=0.95))
    # 耳暈（規格 A，bust 耳位 cx±56*0.95, cy-4*0.95）
    e.append(ear_glow_spec_a(owen_cx-53, 246, s=0.95))
    e.append(ear_glow_spec_a(owen_cx+53, 246, s=0.95))

    # 考卷立在桌面右端（底邊貼桌面頂 y≈335，不懸空）
    test_cx = desk_cx + 105
    e.append(test_paper(cx=test_cx, cy=270, w=130, h=140, scale=0.95))

    # 星星從耳邊跳出，落在考卷上（虛線軌跡＋星星）
    surrounding_paths = [
        ((owen_cx+53, 240), (test_cx-25, 230)),
        ((owen_cx+53, 246), (test_cx+20, 260)),
        ((owen_cx+53, 252), (test_cx-10, 300)),
    ]
    for (sx, sy), (ex, ey) in surrounding_paths:
        e.append(star_trail(sx, sy, ex, ey, opacity=0.7))
        e.append(speech_star(ex, ey, scale=0.6, opacity=0.9))

    # 綠色勾勾（考卷題目行右側）
    e.append(svgtext(test_cx+35, 240, "✓", size=22, fill="#7BC47F", weight="bold"))
    e.append(svgtext(test_cx+35, 292, "✓", size=22, fill="#7BC47F", weight="bold"))
    e.append(svgtext(test_cx+35, 318, "✓", size=22, fill="#7BC47F", weight="bold"))

    return svg(W, H, "".join(e))


def scene_p10():
    """【修正】p10：拉鍊照規格 B 畫在嘴位置，補上雙耳光暈。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p10"]}"/>')
    e.append(f'<ellipse cx="594" cy="560" rx="540" ry="110" fill="#FFDD7E"/>')  # 金色地板

    # 滿天星
    for (x, y, r) in [(160, 90, 18), (1020, 100, 22), (120, 380, 16), (1060, 380, 16), (330, 50, 14), (860, 60, 16), (420, 320, 12)]:
        e.append(star(x, y, r, fill=STAR_Y))
    for (sx, sy, sr) in [(260, 240, 12), (930, 240, 12), (600, 120, 10)]:
        e.append(sparkle(sx, sy, sr, fill=STAR_Y))

    # Owen 披紅披風叉腰（press 抿嘴，讓拉鍊直接蓋在嘴位不殘留笑嘴）
    e.append(boy(pose="hips", expr="press", cx=594, cy=200, scale=1.3, cape=True))

    # 拉鍊徽章疊在嘴位（boy 嘴中心 = cy+34*s）＋雙耳光暈（boy 耳位 = cx±56*s, cy+13*s）
    e.append(zipper_badge(594, 200 + int(34*1.3), s=1.1))
    e.append(ear_glow_spec_a(594 - int(56*1.3), 200 + int(13*1.3), s=1.2))
    e.append(ear_glow_spec_a(594 + int(56*1.3), 200 + int(13*1.3), s=1.2))

    return svg(W, H, "".join(e))


# ================== PAGES DATA ==================

PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I have SO much to say!'),
    ("p2", scene_p2, 'Tr. Mina talks. Star words fly!<br/>My ears catch them, one by one.'),
    ("p3", scene_p3, 'Ethan sits by me.<br/>I want to tell him ALL my things!'),
    ("p4", scene_p4, 'My mouth feels full of words!<br/>I <b>chat</b>. I play. I blah-blah.<br/>The star words fall down&mdash;gone!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I <b>zip</b> and turn my ears ON!'),
    ("p6", scene_p6, '<b>Zip</b> my lips&mdash;zzzip!<br/>Quiet hands on my desk.<br/>Ears ON! Catch the stars!'),
    ("p7", scene_p7, 'Star words live in my ears.<br/>On my <b>test</b>, they jump out to help!<br/>Tr. Mina smiles at my quiet hands.'),
    ("p8", scene_p8, 'Tr. Mina talks. I zip and listen.<br/>My ears catch every star.<br/>&ldquo;Super ears, <b>Owen</b>!&rdquo;'),
    ("p9", scene_p9, '<b>Test</b> day! My stars jump out.<br/>I know this! Teacher said it!<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Zip my lips. Quiet hands. Ears ON!<br/><b>Ears on!</b><br/>I practice every day!'),
]

# ================== PARENT TIPS ==================

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3–4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("跟 Tr. Mina 對暗號", "上課時只說 'Ears on!'（不點名批評、不說「不要講話」）——聊天/玩文具/自言自語是同一顆衝動的三個變形，提醒要指向「開耳朵」這個正向動作。"),
    ("在家玩「接星星」遊戲", "大人一次講三件事（例：紅色、恐龍、星期五），Owen 複述接住幾顆算幾分——練「聽到→留住」的肌肉。"),
    ("當他主動說 'My mouth feels full of words'", "覺察里程碑，大力稱讚。"),
    ("考卷寫對教過的題目時", "回連因果：「這題就是你上課耳朵接到的星星！」——讓「上課聽」與「考卷會寫」在他腦中焊起來。"),
]

# ================== BOOK DICT ==================

BOOK = {
    "slug": "ears-on",
    "order": 19,
    "title_pre": "", "title_hi": "Ears", "title_post": " On!",
    "title_zh": "耳朵開機",
    "subtitle": "Owen's listening story",
    "tagline_zh": "上課專心聽講、把話語星星接住的故事",
    "chips": ["Social Story", "Classroom", "12 pages"],
    "pdf_name": "Ears_On.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ['zip', 'chat', 'test'],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。本書教的不是「乖乖不要亂講話」，"
                     "而是替 Owen 安裝一套<b>上課時用得出來的正向替代腳本</b>："
                     "發現想聊天/玩的衝動 → 嘴拉上、手休息 → 耳朵開機接星星 → "
                     "靠這些星星在考卷上寫出正確答案。目標是幫他看到「安靜聽講」的<b>真正好處</b>——"
                     "不是被罵而停止，而是因為有效而自主選擇。"),
    "cue_html": ("口訣（全書通關密語）：<b>Zip my lips → Quiet hands → Ears on!</b>&nbsp;"
                 "完整三部曲是「Zip my lips（嘴拉上）→ Quiet hands（手休息）→ Ears on!（耳朵開機）」。"
                 "老師現場提醒時只說 <b>'Ears on!'</b> 兩個字，不用長篇講解。"),
    "cover": scene_cover,
}
