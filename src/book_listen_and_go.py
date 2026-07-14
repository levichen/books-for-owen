# -*- coding: utf-8 -*-
"""Book 13: Listen and Go! — 第一次叫就出發（媽媽 April 的一次口訣故事）"""
import math
from parts import *
from book_common import svg, svgtext, TXT, W, H, COVER_W, COVER_H

# soft page palettes
BG = {
    "cover": "#FFF0E0", "p1": "#FFF8E8", "p2": "#FFF3D6", "p3": "#FFF0C2",
    "p4": "#FFE8C9", "p5": "#4A3A6B", "p6": "#FFF5E0", "p7": "#FFF0D9",
    "p8": "#FFE8C0", "p9": "#FFF8E8", "p10": "#4A3A6B", "p11": "#FBF4E8",
}

# ---- Helper functions for toys ----
def toy_block(cx, cy, scale, color, face=True, arms="none"):
    """小方塊積木＋小臉＋小手臂。
    arms: "none" | "pull" (雙手向前拉) | "wave" (揮手) | "cheer" (雙手上舉)"""
    b = []
    # 圓角矩形方塊
    b.append(f'<rect x="{cx-24*scale:.0f}" y="{cy-24*scale:.0f}" width="{48*scale:.0f}" height="{48*scale:.0f}" '
             f'rx="{6*scale:.0f}" fill="{color}" stroke="#C9BFA8" stroke-width="{2*scale:.1f}"/>')

    if face:
        # 小眼睛
        b.append(f'<circle cx="{cx-10*scale:.0f}" cy="{cy-6*scale:.0f}" r="{2*scale:.1f}" fill="#33291F"/>')
        b.append(f'<circle cx="{cx+10*scale:.0f}" cy="{cy-6*scale:.0f}" r="{2*scale:.1f}" fill="#33291F"/>')
        # 微笑嘴
        b.append(f'<path d="M {cx-8*scale:.0f} {cy+4*scale:.0f} Q {cx:.0f} {cy+10*scale:.0f} {cx+8*scale:.0f} {cy+4*scale:.0f}" '
                 f'fill="none" stroke="#33291F" stroke-width="{1.5*scale:.1f}" stroke-linecap="round"/>')

    # 小手臂（加粗增大）
    if arms == "pull":
        # 雙手向前伸（拉人）
        b.append(f'<line x1="{cx-16*scale:.0f}" y1="{cy-10*scale:.0f}" x2="{cx-40*scale:.0f}" y2="{cy-28*scale:.0f}" '
                 f'stroke="#C9BFA8" stroke-width="{4*scale:.1f}" stroke-linecap="round"/>')
        b.append(f'<line x1="{cx+16*scale:.0f}" y1="{cy-10*scale:.0f}" x2="{cx+40*scale:.0f}" y2="{cy-28*scale:.0f}" '
                 f'stroke="#C9BFA8" stroke-width="{4*scale:.1f}" stroke-linecap="round"/>')
        # 小手掌（加大）
        b.append(f'<circle cx="{cx-40*scale:.0f}" cy="{cy-28*scale:.0f}" r="{4*scale:.1f}" fill="#C9BFA8"/>')
        b.append(f'<circle cx="{cx+40*scale:.0f}" cy="{cy-28*scale:.0f}" r="{4*scale:.1f}" fill="#C9BFA8"/>')
    elif arms == "wave":
        # 揮手（加大弧度）
        b.append(f'<path d="M {cx+16*scale:.0f} {cy-10*scale:.0f} Q {cx+48*scale:.0f} {cy-40*scale:.0f} {cx+40*scale:.0f} {cy-60*scale:.0f}" '
                 f'fill="none" stroke="#C9BFA8" stroke-width="{4*scale:.1f}" stroke-linecap="round"/>')
        b.append(f'<circle cx="{cx+40*scale:.0f}" cy="{cy-60*scale:.0f}" r="{4*scale:.1f}" fill="#C9BFA8"/>')
    elif arms == "cheer":
        # 雙手上舉（加高加大）
        b.append(f'<path d="M {cx-16*scale:.0f} {cy-10*scale:.0f} L {cx-28*scale:.0f} {cy-56*scale:.0f}" '
                 f'stroke="#C9BFA8" stroke-width="{4*scale:.1f}" stroke-linecap="round"/>')
        b.append(f'<path d="M {cx+16*scale:.0f} {cy-10*scale:.0f} L {cx+28*scale:.0f} {cy-56*scale:.0f}" '
                 f'stroke="#C9BFA8" stroke-width="{4*scale:.1f}" stroke-linecap="round"/>')
        b.append(f'<circle cx="{cx-28*scale:.0f}" cy="{cy-56*scale:.0f}" r="{4*scale:.1f}" fill="#C9BFA8"/>')
        b.append(f'<circle cx="{cx+28*scale:.0f}" cy="{cy-56*scale:.0f}" r="{4*scale:.1f}" fill="#C9BFA8"/>')

    return "".join(b)

def toy_car(cx, cy, scale, face=True):
    """小車＋小臉。車身 ≈ 48px 寬，兩輪"""
    c = []
    # 車身
    c.append(f'<rect x="{cx-24*scale:.0f}" y="{cy-16*scale:.0f}" width="{48*scale:.0f}" height="{20*scale:.0f}" '
             f'rx="{4*scale:.0f}" fill="#E74C3C" stroke="#C0392B" stroke-width="{2*scale:.1f}"/>')
    # 車頭小臉
    if face:
        c.append(f'<circle cx="{cx-20*scale:.0f}" cy="{cy-8*scale:.0f}" r="{6*scale:.0f}" fill="#FFD9B6"/>')
        c.append(f'<circle cx="{cx-24*scale:.0f}" cy="{cy-10*scale:.0f}" r="{2*scale:.1f}" fill="#33291F"/>')
        c.append(f'<circle cx="{cx-16*scale:.0f}" cy="{cy-10*scale:.0f}" r="{2*scale:.1f}" fill="#33291F"/>')
        c.append(f'<path d="M {cx-22*scale:.0f} {cy-4*scale:.0f} Q {cx-20*scale:.0f} {cy-2*scale:.0f} {cx-18*scale:.0f} {cy-4*scale:.0f}" '
                 f'fill="none" stroke="#33291F" stroke-width="{1*scale:.1f}" stroke-linecap="round"/>')
    # 兩輪
    c.append(f'<circle cx="{cx-12*scale:.0f}" cy="{cy+8*scale:.0f}" r="{6*scale:.0f}" fill="#333333" stroke="#111111" stroke-width="{1*scale:.1f}"/>')
    c.append(f'<circle cx="{cx+12*scale:.0f}" cy="{cy+8*scale:.0f}" r="{6*scale:.0f}" fill="#333333" stroke="#111111" stroke-width="{1*scale:.1f}"/>')

    return "".join(c)

def wash_pot(cx, cy, scale):
    """洗鼻壺：藍色茶壺形"""
    p = []
    # 壺身
    p.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{18*scale:.0f}" ry="{20*scale:.0f}" fill="#5CA8E8" stroke="#2E7AB6" stroke-width="{2*scale:.1f}"/>')
    # 把手
    p.append(f'<path d="M {cx+16*scale:.0f} {cy-8*scale:.0f} Q {cx+32*scale:.0f} {cy-4*scale:.0f} {cx+28*scale:.0f} {cy+12*scale:.0f}" '
             f'fill="none" stroke="#5CA8E8" stroke-width="{5*scale:.1f}" stroke-linecap="round"/>')
    # 嘴
    p.append(f'<path d="M {cx-12*scale:.0f} {cy-16*scale:.0f} L {cx-20*scale:.0f} {cy-24*scale:.0f}" '
             f'stroke="#5CA8E8" stroke-width="{4*scale:.1f}" stroke-linecap="round"/>')
    return "".join(p)

def hair_dryer(cx, cy, scale):
    """吹風機：簡化版（圓形出風口＋握把）"""
    d = []
    # 出風口
    d.append(f'<circle cx="{cx:.0f}" cy="{cy-16*scale:.0f}" r="{10*scale:.0f}" fill="#F4A460" stroke="#D9793D" stroke-width="{2*scale:.1f}"/>')
    # 握把
    d.append(f'<rect x="{cx-8*scale:.0f}" y="{cy-4*scale:.0f}" width="{16*scale:.0f}" height="{28*scale:.0f}" '
             f'rx="{4*scale:.0f}" fill="#A9A9A9" stroke="#888888" stroke-width="{2*scale:.1f}"/>')
    return "".join(d)

def bathtub(cx, cy, scale):
    """浴缸：橢圓形盤子＋小泡泡"""
    t = []
    # 缸身
    t.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{22*scale:.0f}" ry="{14*scale:.0f}" fill="#E8F4F8" stroke="#9BC8DC" stroke-width="{2*scale:.1f}"/>')
    # 邊緣
    t.append(f'<path d="M {cx-20*scale:.0f} {cy-12*scale:.0f} Q {cx:.0f} {cy-16*scale:.0f} {cx+20*scale:.0f} {cy-12*scale:.0f}" '
             f'fill="none" stroke="#9BC8DC" stroke-width="{2*scale:.1f}" stroke-linecap="round"/>')
    # 小泡泡
    for i in range(3):
        bx = cx - 12*scale + i*12*scale
        by = cy - 4*scale
        b_r = (3-i)*1.5*scale
        t.append(f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{b_r:.1f}" fill="#B8E6F0" fill-opacity="0.6"/>')
    return "".join(t)

def glue_mark(cx, cy, scale):
    """膠水黏地標記：金色水漬橢圓＋兩滴（明顯版）"""
    g = []
    # 主要水漬（大橢圓）
    g.append(f'<ellipse cx="{cx:.0f}" cy="{cy:.0f}" rx="{28*scale:.0f}" ry="{18*scale:.0f}" fill="#FFD700" fill-opacity="0.7" stroke="#DAA520" stroke-width="{1.5*scale:.1f}"/>')
    # 上方小滴
    g.append(f'<ellipse cx="{cx-18*scale:.0f}" cy="{cy-28*scale:.0f}" rx="{8*scale:.0f}" ry="{12*scale:.0f}" fill="#FFD700" stroke="#DAA520" stroke-width="{1.5*scale:.1f}"/>')
    # 右下小滴
    g.append(f'<ellipse cx="{cx+22*scale:.0f}" cy="{cy+16*scale:.0f}" rx="{7*scale:.0f}" ry="{11*scale:.0f}" fill="#FFD700" stroke="#DAA520" stroke-width="{1.5*scale:.1f}"/>')
    return "".join(g)

def speech_bubble(cx, cy, text, size=40, w=200, h=100):
    """語音泡泡（圓角矩形＋三角形指針）"""
    b = []
    # 泡泡框
    b.append(f'<rect x="{cx-w/2:.0f}" y="{cy-h/2:.0f}" width="{w:.0f}" height="{h:.0f}" '
             f'rx="12" fill="#FFFFFF" stroke="#D4A574" stroke-width="3"/>')
    # 指針（向下）
    b.append(f'<polygon points="{cx:.0f},{cy+h/2+12:.0f} {cx-12:.0f},{cy+h/2:.0f} {cx+12:.0f},{cy+h/2:.0f}" '
             f'fill="#FFFFFF" stroke="#D4A574" stroke-width="2"/>')
    # 文字
    b.append(svgtext(cx, cy+10, text, size=size, fill=TXT, weight="bold"))
    return "".join(b)

def startline(cx, cy, scale):
    """起跑線：白色橫線＋小旗標"""
    s = []
    s.append(f'<line x1="{cx-40*scale:.0f}" y1="{cy:.0f}" x2="{cx+40*scale:.0f}" y2="{cy:.0f}" '
             f'stroke="#FFFFFF" stroke-width="{6*scale:.1f}" stroke-linecap="round"/>')
    # 小旗標
    for i in [-1, 1]:
        fx = cx + i*40*scale
        s.append(f'<rect x="{fx-4*scale:.0f}" y="{cy-20*scale:.0f}" width="{8*scale:.0f}" height="{20*scale:.0f}" fill="#C9BFA8"/>')
        s.append(f'<polygon points="{fx:.0f},{cy-20*scale:.0f} {fx+12*scale:.0f},{cy-14*scale:.0f} {fx:.0f},{cy-8*scale:.0f}" '
                 f'fill="#FFD700"/>')
    return "".join(s)

def sound_wave(cx, cy, scale, num_arcs=3):
    """聲波弧：從 cx 向外開口，num_arcs 層"""
    w = []
    for i in range(1, num_arcs+1):
        r = 12*scale*i
        w.append(f'<path d="M {cx-r:.0f} {cy:.0f} A {r:.0f} {r:.0f} 0 0 1 {cx+r:.0f} {cy:.0f}" '
                 f'fill="none" stroke="#FFD700" stroke-width="{3*scale:.1f}" stroke-linecap="round"/>')
    return "".join(w)

# ---- SCENE FUNCTIONS ----
def scene_cover():
    """封面：Owen 開心玩玩具＋玩具小臉們＋暖色"""
    e = []
    # 背景色已由 BG["cover"] 提供
    # 地墊（暖棕）
    e.append(f'<rect x="100" y="380" width="988" height="150" rx="20" fill="#F4E4D0"/>')

    # 玩具散佈：都在地墊上（y ≥ 380）
    e.append(toy_block(280, 440, 1.0, "#F4A460", face=True, arms="wave"))  # 橙色積木移到地墊上
    e.append(toy_block(880, 450, 1.0, "#F2A04D", face=True, arms="cheer"))  # 金色積木移到地墊上
    e.append(toy_block(550, 470, 1.0, "#87CEEB", face=True, arms="none"))  # 藍色積木
    e.append(toy_car(420, 490, 0.9, face=True))  # 紅色小車
    e.append(toy_car(750, 495, 0.95, face=True))  # 另一台小車

    # Owen 開心玩：stand 姿勢，big 表情
    e.append(boy(pose="stand", expr="big", cx=550, cy=220, scale=1.2))

    # 裝飾星星
    for (x, y, r) in [(200, 120, 16), (950, 140, 18), (380, 100, 12), (820, 90, 14)]:
        e.append(star(x, y, r))
    e.append(sparkle(680, 80, 14))

    return svg(COVER_W, COVER_H, "".join(e), bg="#FFF0E0")

def scene_p1():
    """p1: Owen 開心玩積木＋小車，玩具都有微笑小臉"""
    e = []
    # 客廳背景
    bg_color = BG["p1"]
    e.append(f'<rect x="0" y="0" width="1188" height="380" fill="{bg_color}"/>')  # 牆面
    e.append(f'<rect x="0" y="380" width="1188" height="180" fill="#E8D2AC"/>')  # 地板

    # 地墊（圓角矩形）
    e.append(f'<rect x="120" y="340" width="900" height="180" rx="20" fill="#E6D4C0" stroke="#D4A574" stroke-width="3"/>')

    # 玩具（地墊上）：積木和小車
    e.append(toy_block(280, 380, 1.0, "#F4A460", face=True, arms="none"))
    e.append(toy_block(420, 350, 0.9, "#87CEEB", face=True, arms="wave"))
    e.append(toy_block(750, 380, 0.95, "#FFB6C1", face=True, arms="none"))
    e.append(toy_car(600, 430, 0.85, face=True))
    e.append(toy_car(880, 400, 0.9, face=True))

    # Owen 站在地墊上，開心玩
    e.append(boy(pose="stand", expr="big", cx=350, cy=240, scale=1.15))

    # 裝飾星星和亮晶晶
    e.append(star(950, 100, 18))
    e.append(sparkle(200, 150, 12))
    e.append(sparkle(1050, 180, 10))

    return svg(W, H, "".join(e), bg=None)

def scene_p2():
    """p2: April 在浴室門框拿洗鼻壺呼喚，Owen 背對在玩具區"""
    e = []
    # 背景：客廳＋浴室門框
    bg_color = BG["p2"]
    e.append(f'<rect x="0" y="0" width="1188" height="380" fill="{bg_color}"/>')
    e.append(f'<rect x="0" y="380" width="1188" height="180" fill="#E8D2AC"/>')  # 地板

    # 浴室門框（右側）
    e.append(f'<rect x="850" y="80" width="220" height="340" rx="10" fill="#E8C5A8" stroke="#D4A574" stroke-width="4"/>')
    e.append(f'<line x1="960" y1="80" x2="960" y2="420" stroke="#D4A574" stroke-width="3"/>')  # 門中線

    # 地墊
    e.append(f'<rect x="120" y="340" width="700" height="160" rx="20" fill="#E6D4C0" stroke="#D4A574" stroke-width="3"/>')

    # Owen 背對，玩玩具
    e.append(boy(pose="stand", expr="smile", cx=300, cy=240, scale=1.1))

    # 玩具在地墊上
    e.append(toy_block(450, 370, 0.9, "#F4A460", face=True, arms="none"))
    e.append(toy_car(600, 390, 0.85, face=True))

    # April 在浴室門框，拿洗鼻壺，呼喚表情
    e.append(april(cx=960, cy=250, scale=1.0, pose="stand"))
    e.append(wash_pot(920, 180, 0.8))

    # April 的語音泡泡："Owen! Nose wash time!"
    e.append(speech_bubble(700, 150, "Owen! Nose wash\ntime!", size=38, w=220, h=100))

    return svg(W, H, "".join(e), bg=None)

def scene_p3():
    """p3: Owen 特寫（star 表情）緊抱積木塔，玩具圍著他"""
    e = []
    bg_color = BG["p3"]
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{bg_color}"/>')

    # 積木塔（Owen 身後）
    for i in range(3):
        e.append(f'<rect x="{594-40+i*20:.0f}" y="{280-i*50:.0f}" width="{80:.0f}" height="{50:.0f}" '
                 f'rx="6" fill="#F4A460" stroke="#D4A574" stroke-width="2"/>')

    # Owen 特寫，star 表情，抱著積木
    e.append(boy(pose="stand", expr="star", cx=400, cy=240, scale=1.2))

    # 玩具圍著他
    e.append(toy_block(600, 200, 1.0, "#87CEEB", face=True, arms="none"))
    e.append(toy_block(650, 320, 0.95, "#FFB6C1", face=True, arms="none"))
    e.append(toy_car(750, 280, 0.9, face=True))

    # 裝飾星星
    e.append(star(200, 100, 20))
    e.append(star(1000, 350, 22))
    e.append(sparkle(280, 400, 12))
    e.append(sparkle(950, 450, 10))

    return svg(W, H, "".join(e), bg=None)

def scene_p4():
    """p4: 衝動頁——玩具拉住 Owen，背景 April 疲累呼喚"""
    e = []
    bg_color = BG["p4"]
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{bg_color}"/>')

    # 背景：April 疲累呼喚（左上角）
    e.append(april(cx=150, cy=120, scale=0.8, pose="stand"))
    # April 頭上疲累線
    e.append(f'<line x1="100" y1="50" x2="120" y2="40" stroke="#E4574C" stroke-width="3" stroke-linecap="round"/>')
    e.append(f'<line x1="150" y1="40" x2="170" y2="45" stroke="#E4574C" stroke-width="3" stroke-linecap="round"/>')
    e.append(f'<line x1="200" y1="50" x2="210" y2="30" stroke="#E4574C" stroke-width="3" stroke-linecap="round"/>')

    # April 的疊層呼喚泡泡："Owen! Owen! Owen!"（逐層遞增）
    e.append(f'<ellipse cx="280" cy="100" rx="50" ry="35" fill="#FFFFFF" stroke="#D4A574" stroke-width="2"/>')
    e.append(svgtext(280, 112, "Owen!", size=28, fill=TXT, weight="bold"))

    e.append(f'<ellipse cx="330" cy="80" rx="65" ry="42" fill="#FFFFFF" stroke="#D4A574" stroke-width="2"/>')
    e.append(svgtext(330, 95, "Owen!", size=32, fill=TXT, weight="bold"))

    e.append(f'<ellipse cx="390" cy="60" rx="80" ry="50" fill="#FFFFFF" stroke="#D4A574" stroke-width="2"/>')
    e.append(svgtext(390, 80, "Owen!", size=36, fill=TXT, weight="bold"))

    # 地墊
    e.append(f'<rect x="120" y="340" width="900" height="180" rx="20" fill="#E6D4C0" stroke="#D4A574" stroke-width="3"/>')

    # Owen 被玩具拉住
    e.append(boy(pose="stand", expr="press", cx=550, cy=200, scale=1.15))

    # 膠水黏地標記（Owen 腳下）
    e.append(glue_mark(550, 460, 0.8))

    # 玩具拉住 Owen（移到身體側面：手臂/衣角高度 cy+60~120）
    # 左邊積木：在 Owen 左手臂邊（約 cx-120, cy+80）
    e.append(toy_block(430, 280, 1.0, "#F4A460", face=True, arms="pull"))
    # 右邊積木：在 Owen 右手臂邊（約 cx+120, cy+80）
    e.append(toy_block(670, 270, 0.95, "#87CEEB", face=True, arms="pull"))

    # Owen 的語音泡泡（SVG <text> 不支援 \n——單行呈現，避免字被黏在一起）
    e.append(speech_bubble(770, 255, "One more minute…", size=30, w=270, h=64))

    # 玩具的語音泡泡："Stay! Stay!"（指向玩具，加尾巴）
    e.append(f'<ellipse cx="380" cy="310" rx="80" ry="45" fill="#FFFFFF" stroke="#D4A574" stroke-width="3"/>')
    e.append(svgtext(380, 330, "Stay! Stay!", size=40, fill=TXT, weight="bold"))
    # 泡泡尾巴指向玩具
    e.append(f'<polygon points="420,355 440,380 430,360" fill="#FFFFFF" stroke="#D4A574" stroke-width="2"/>')

    return svg(W, H, "".join(e), bg=None)

def scene_p5():
    """p5: 紫色星空，Owen 啟動 superpower，聲波＋起跑線"""
    e = []
    # 紫色星空背景
    bg_color = BG["p5"]
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{bg_color}"/>')

    # 滿天星
    for (x, y, r) in [(150, 100, 14), (250, 200, 12), (900, 120, 16), (1000, 280, 14),
                       (300, 450, 13), (950, 400, 15), (100, 350, 11), (1080, 500, 12)]:
        e.append(star(x, y, r, fill="#FFE9A8", stroke=STAR_DK))
    e.append(sparkle(500, 80, 14))
    e.append(sparkle(700, 480, 12))

    # 起跑線
    e.append(startline(550, 450, 0.8))

    # Owen press 表情，身體前傾
    e.append(boy(pose="stand", expr="press", cx=550, cy=180, scale=1.2))

    # 聲波（耳朵旁發光）
    e.append(sound_wave(520, 140, 0.7, num_arcs=3))

    # 聲波弧旁邊亮光
    for i in range(2):
        e.append(f'<circle cx="{500+i*60:.0f}" cy="{100+i*40:.0f}" r="{8-i*2:.0f}" fill="#FFE9A8" fill-opacity="{0.5-i*0.15:.1f}"/>')

    return svg(W, H, "".join(e), bg=None)

def scene_p6():
    """p6: 三格腳本——①"OK, Mommy!" ②玩具揮手bye ③Owen run 衝向門"""
    e = []
    bg_color = BG["p6"]
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{bg_color}"/>')

    # 背景地板
    e.append(f'<rect x="0" y="400" width="1188" height="160" fill="#E8D2AC"/>')

    # 三個圓角框格子
    boxes = [
        {"x": 80, "y": 80, "w": 340, "h": 300, "text": "OK,\nMommy!"},
        {"x": 440, "y": 80, "w": 320, "h": 300, "text": ""},
        {"x": 780, "y": 80, "w": 320, "h": 300, "text": ""},
    ]

    for box in boxes:
        bx, by, bw, bh = box["x"], box["y"], box["w"], box["h"]
        e.append(f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw:.0f}" height="{bh:.0f}" '
                 f'rx="12" fill="#FFFFFF" stroke="#D4A574" stroke-width="3"/>')

    # Frame 1: "OK, Mommy!" 大語音泡泡＋Owen bust（說話的人要在場）
    e.append(f'<ellipse cx="220" cy="120" rx="110" ry="70" fill="#FFE9A8" stroke="#DAA520" stroke-width="3"/>')
    e.append(svgtext(220, 140, "OK, Mommy!", size=42, fill=TXT, weight="bold"))
    e.append(boy_bust(expr="big", cx=250, cy=260, scale=0.8))

    # Frame 2: 玩具們坐地墊揮手 bye
    e.append(f'<rect x="460" y="340" width="280" height="100" rx="15" fill="#E6D4C0" stroke="#D4A574" stroke-width="2"/>')
    e.append(toy_block(520, 360, 0.8, "#F4A460", face=True, arms="wave"))
    e.append(toy_block(600, 370, 0.75, "#87CEEB", face=True, arms="wave"))
    e.append(toy_car(700, 380, 0.7, face=True))

    # Frame 3: Owen run 衝向右邊門框＋速度線在身後
    e.append(boy(pose="run", expr="big", cx=880, cy=240, scale=1.0))
    # 速度線（只在身後軀幹高度，y ≥ cy+40*s）
    for i in range(3):
        e.append(f'<line x1="{800-i*25:.0f}" y1="{300:.0f}" x2="{750-i*25:.0f}" y2="{300:.0f}" '
                 f'stroke="#F4A460" stroke-width="4" stroke-linecap="round" stroke-dasharray="4 8"/>')
    # 右邊門框（兩豎一橫）
    e.append(f'<rect x="945" y="120" width="40" height="200" fill="none" stroke="#D4A574" stroke-width="3"/>')  # 左豎
    e.append(f'<rect x="1005" y="120" width="40" height="200" fill="none" stroke="#D4A574" stroke-width="3"/>')  # 右豎
    e.append(f'<line x1="945" y1="220" x2="1045" y2="220" stroke="#D4A574" stroke-width="3"/>')  # 橫

    return svg(W, H, "".join(e), bg=None)

def scene_p7():
    """p7: 左小格玩具等待，右大格 April 抱 Owen＋時鐘"""
    e = []
    bg_color = BG["p7"]
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{bg_color}"/>')

    # 背景地板
    e.append(f'<rect x="0" y="380" width="1188" height="180" fill="#E8D2AC"/>')

    # 左小格：玩具等待
    e.append(f'<rect x="80" y="80" width="340" height="320" rx="12" fill="#FFFFFF" stroke="#D4A574" stroke-width="3"/>')
    e.append(f'<rect x="100" y="350" width="300" height="100" rx="15" fill="#E6D4C0" stroke="#D4A574" stroke-width="2"/>')
    e.append(toy_block(180, 370, 0.8, "#F4A460", face=True, arms="wave"))
    e.append(toy_block(260, 375, 0.75, "#87CEEB", face=True, arms="wave"))
    e.append(toy_car(370, 385, 0.7, face=True))

    # 右大格：April 抱 Owen（更親密的位置）
    e.append(f'<rect x="440" y="80" width="660" height="320" rx="12" fill="#FFFFFF" stroke="#D4A574" stroke-width="3"/>')
    e.append(april(cx=920, cy=220, scale=1.0, pose="cheer"))
    e.append(boy(pose="stand", expr="big", cx=880, cy=250, scale=0.9))

    # 時鐘（右上角，只走一小格）
    e.append(f'<circle cx="1050" cy="140" r="35" fill="#FFE9A8" stroke="#DAA520" stroke-width="3"/>')
    e.append(f'<line x1="1050" y1="140" x2="1050" y2="110" stroke="#333333" stroke-width="3" stroke-linecap="round"/>')  # 時針
    e.append(f'<line x1="1050" y1="140" x2="1070" y2="140" stroke="#333333" stroke-width="2" stroke-linecap="round"/>')  # 分針
    e.append(f'<circle cx="1050" cy="140" r="4" fill="#333333"/>')

    return svg(W, H, "".join(e), bg=None)

def scene_p8():
    """p8: 三小格 icon（洗鼻壺/吹風機/浴缸＋綠勾），下方 April 抱 Owen"""
    e = []
    bg_color = BG["p8"]
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{bg_color}"/>')

    # 背景地板
    e.append(f'<rect x="0" y="380" width="1188" height="180" fill="#E8D2AC"/>')

    # 三小格 icon
    icons = [
        {"x": 180, "y": 100, "item": "wash_pot"},
        {"x": 594, "y": 100, "item": "hair_dryer"},
        {"x": 1008, "y": 100, "item": "bathtub"},
    ]

    for icon in icons:
        ix, iy = icon["x"], icon["y"]
        e.append(f'<rect x="{ix-70:.0f}" y="{iy:.0f}" width="140" height="140" '
                 f'rx="10" fill="#F5F5F5" stroke="#D4A574" stroke-width="2"/>')

        if icon["item"] == "wash_pot":
            e.append(wash_pot(ix, iy+50, 0.9))
        elif icon["item"] == "hair_dryer":
            e.append(hair_dryer(ix, iy+50, 0.9))
        else:
            e.append(bathtub(ix, iy+50, 0.9))

        # 綠色勾勾
        e.append(f'<path d="M {ix-30:.0f} {iy+110:.0f} L {ix-10:.0f} {iy+130:.0f} L {ix+30:.0f} {iy+100:.0f}" '
                 f'fill="none" stroke="#7BC47F" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')

    # 下方：April 和 Owen 並肩靠近（完整可見，不嵌入色帶）
    e.append(april(cx=380, cy=420, scale=0.95, pose="cheer"))
    e.append(boy(pose="stand", expr="big", cx=480, cy=440, scale=0.85))

    # 語音泡泡："One call, Owen! Wow!"（加邊框、修正文字空格）
    e.append(f'<rect x="680" y="350" width="280" height="120" rx="12" fill="#FFFFFF" stroke="#D4A574" stroke-width="3"/>')
    e.append(f'<polygon points="700,470 680,500 720,480" fill="#FFFFFF" stroke="#D4A574" stroke-width="2"/>')
    e.append(svgtext(820, 390, "One call, Owen!", size=36, fill=TXT, weight="bold"))
    e.append(svgtext(820, 430, "Wow!", size=36, fill=TXT, weight="bold"))

    return svg(W, H, "".join(e), bg=None)

def scene_p9():
    """p9: Owen run 衝回，玩具歡呼＋速度線＋火箭"""
    e = []
    bg_color = BG["p9"]
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{bg_color}"/>')

    # 地墊
    e.append(f'<rect x="120" y="340" width="900" height="180" rx="20" fill="#E6D4C0" stroke="#D4A574" stroke-width="3"/>')

    # Owen run 左側衝入
    e.append(boy(pose="run", expr="big", cx=250, cy=220, scale=1.15))

    # 速度線（只在身後軀幹高度 y ≥ 280，不穿過頭部）
    for i in range(4):
        e.append(f'<line x1="{180-i*25:.0f}" y1="{310:.0f}" x2="{130-i*25:.0f}" y2="{310:.0f}" '
                 f'stroke="#F4A460" stroke-width="5" stroke-linecap="round" stroke-dasharray="6 10"/>')

    # 火箭圖案（改清楚：三角鼻錐＋筒身＋尾焰）
    # 三角鼻錐（置中在筒身正上方）
    e.append(f'<polygon points="775,140 845,140 810,88" fill="#E4574C" stroke="#C0392B" stroke-width="2"/>')
    # 筒身
    e.append(f'<rect x="775" y="140" width="70" height="80" rx="8" fill="#C9CDD4" stroke="#9AA0A8" stroke-width="2"/>')
    # 尾焰（筒身正下方，外橙內黃）
    e.append(f'<polygon points="788,222 832,222 810,262" fill="#FF8C42" stroke="#E55C00" stroke-width="1.5"/>')
    e.append(f'<polygon points="798,222 822,222 810,246" fill="#FFD700"/>')
    # 窗口（裝飾）
    e.append(f'<circle cx="810" cy="160" r="6" fill="#B0E0E6" stroke="#888888" stroke-width="1.5"/>')

    # 玩具們歡呼（右側地墊上，位置更靠上使 cheer 手臂更明顯）
    e.append(toy_block(750, 320, 0.95, "#F4A460", face=True, arms="cheer"))
    e.append(toy_block(850, 310, 0.9, "#87CEEB", face=True, arms="cheer"))
    e.append(toy_car(950, 350, 0.85, face=True))

    return svg(W, H, "".join(e), bg=None)

def scene_p10():
    """p10: Owen 英雄頁，披紅披風、單腳踩起跑線＋聲波＋滿天星"""
    e = []
    bg_color = BG["p10"]
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{bg_color}"/>')

    # 起跑線
    e.append(startline(550, 400, 0.9))

    # Owen 披紅披風，單腳踩起跑線（hips 姿勢＋cape）
    e.append(boy(pose="hips", expr="proud", cx=550, cy=200, scale=1.2, cape=True))

    # 聲波（耳朵旁大的）
    e.append(sound_wave(510, 140, 0.8, num_arcs=4))

    # 滿天星
    for (x, y, r) in [(150, 80, 16), (350, 120, 14), (850, 100, 18), (1000, 200, 15),
                       (200, 380, 12), (950, 350, 14), (100, 480, 13), (1050, 470, 15)]:
        e.append(star(x, y, r, fill="#FFE9A8", stroke=STAR_DK))
    e.append(sparkle(450, 300, 14))
    e.append(sparkle(750, 320, 12))

    return svg(W, H, "".join(e), bg=None)

# ---- PAGE TEXTS ----
PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I love my toys and games.'),
    ("p2", scene_p2, 'Mommy calls,<br/>&ldquo;<b>Owen</b>! Nose wash time!&rdquo;'),
    ("p3", scene_p3, 'My toys are SO fun.<br/>My hands keep playing, playing.<br/>I do not want to stop.'),
    ("p4", scene_p4, 'My toys say, &ldquo;Stay! Stay!&rdquo;<br/>My feet feel <b>glued</b> to the floor.<br/>My mouth says, &ldquo;One more minute&hellip;&rdquo;'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/><b>Listen and GO!</b>'),
    ("p6", scene_p6, 'I say, &ldquo;OK, Mommy!&rdquo;<br/>I put my toys down.<br/>I go right away!'),
    ("p7", scene_p7, 'One call makes Mommy happy.<br/>My toys wait for me.<br/>More play time comes back!'),
    ("p8", scene_p8, 'Nose wash, bath, hair dryer too.<br/>One call is all I need!<br/>Mommy April hugs me. &ldquo;One call, <b>Owen</b>! Wow!&rdquo;'),
    ("p9", scene_p9, 'Quick like a rocket!<br/>Back to my toys.<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Say OK. Toys down.<br/><b>Listen and go!</b><br/>I practice every day!'),
]

PARENT_TIPS = [
    ("大人的配套：只講一次", "統一句式「Owen! X time!」講一次，然後<b>走到他面前</b>等，不要遠端重複喊——重複喊等於教他「前四次可以不理」。他拖延時指口訣說 &ldquo;Listen and go?&rdquo; 即可，不重述指令。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("第一次叫就動 = 立刻大稱讚", "具體說出「你第一次叫就來了！」；可搭配聯絡卡式集點（一天三次 GO 就兌現小獎勵）。"),
    ("玩具要真的「等他」", "他回來前不收走玩具（書裡承諾過玩具會等）——承諾兌現，腳本才可信。"),
    ("讀完玩 2 分鐘角色扮演", "你當 Mommy、他練「聽到呼喚 &rarr; 說 OK &rarr; 放下玩具 &rarr; 出發」，再交換角色。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁、寫 Mommy 還有什麼 task。參與越多，效果越好。"),
]

BOOK = {
    "slug": "listen-and-go",
    "order": 13,
    "title_pre": "", "title_hi": "Listen", "title_post": " and Go!",
    "title_zh": "聽一次就出發",
    "subtitle": "Owen's first-call story",
    "tagline_zh": "Owen 的一次就做故事",
    "chips": ["Social Story", "Home", "12 pages"],
    "pdf_name": "Listen_And_Go.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": [],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Listen and go!</b> 完整動作步驟：<b>Say \"OK, Mommy!\" "
                 "&rarr; Toys down &rarr; Go right away!</b>&nbsp;"
                 "第一次聽到大人講，就立刻說 OK、放下玩具、立刻出發，是本書的核心。"),
    "cover": scene_cover,
}
