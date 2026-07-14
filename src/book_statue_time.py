# -*- coding: utf-8 -*-
"""Book: Statue Time — Owen 的雕像時間照護腳本（浴室、吹頭髮場景）。"""
from parts import *
from book_common import svg, svgtext, TXT, W, H
import math

# 頁面背景色調
BG = {
    "cover": "#FFF4D9",      # 暖色氛圍
    "p1": "#F5E8D8",         # 浴室暖色
    "p2": "#F5E8D8",         # 浴室磁磚感
    "p3": "#FFE8C2",         # 暖風四周
    "p4": "#FFD9C0",         # 衝動頁
    "p5": "#4A3F7B",         # 紫色星空
    "p6": "#E8DDD0",         # 三步腳本
    "p7": "#EAE0D8",         # 觀點對比
    "p8": "#F5E8D8",         # 吹好了
    "p9": "#F0E5D5",         # 轉移頁
    "p10": "#5B4A8E",        # 英雄星空
    "p11": "#FBF4E8",        # 家長頁
}

# =============== SCENES ===============

def scene_cover():
    """封面：Owen 坐凳子 + April 拿吹風機 + 暖色星星"""
    e = []
    # 星星
    for (x, y, r) in [(140, 120, 18), (1050, 140, 20), (180, 450, 16), (1020, 480, 16)]:
        e.append(star(x, y, r))
    e.append(sparkle(350, 80, 12)); e.append(sparkle(800, 420, 12))

    # 地面
    e.append(f'<ellipse cx="594" cy="620" rx="500" ry="80" fill="#FFD9A8"/>')

    # 凳子（下方）
    stool_cx, stool_cy = 420, 500
    e.append(f'<ellipse cx="{stool_cx}" cy="{stool_cy}" rx="60" ry="16" fill="#D4B896"/>')
    e.append(f'<rect x="{stool_cx-5}" y="{stool_cy}" width="10" height="50" rx="5" fill="#B09070"/>')

    # Owen 坐在凳子上（用 boy_bust）
    e.append(boy_bust(expr="big", cx=420, cy=380, scale=1.2, arms="desk"))

    # April 拿吹風機（pose='wave'）
    s = 1.15
    april_cx, april_cy = 760, 400
    e.append(april(cx=april_cx, cy=april_cy, scale=s, pose="wave"))
    # April 舉起的手位置：(cx + 80*s, cy - 2*s)
    hand_x = april_cx + 80*s
    hand_y = april_cy - 2*s
    # 吹風機握把在手上
    e.append(f'<ellipse cx="{hand_x-10}" cy="{hand_y}" rx="18" ry="22" fill="#E8823C"/>')  # 機身
    e.append(f'<circle cx="{hand_x+6}" cy="{hand_y-24}" r="15" fill="#FFD9A8"/>')  # 風口
    # 風流線（3 條暖黃波浪線從風口連到 Owen）
    for dy in [-10, 0, 10]:
        e.append(f'<path d="M {hand_x+18} {hand_y-24+dy} q 18 -8 36 0 q 18 8 36 0 q 18 -8 36 0" fill="none" stroke="#F7C977" stroke-width="3" stroke-linecap="round"/>')

    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """p1：浴室場景。Owen 洗完澡，頭髮濕濕（頭頂水滴），肩上圍浴巾。April 拿大浴巾。"""
    e = []

    # 浴室磁磚背景（簡單）：淺奶油 + 一條磁磚線
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#F5E8D8"/>')
    e.append(f'<line x1="0" y1="300" x2="1188" y2="300" stroke="#D9C8B0" stroke-width="3"/>')

    # 地面
    e.append(f'<rect x="0" y="480" width="1188" height="80" fill="#E8D7C5"/>')

    # 浴缸（右側，簡單弧形）
    e.append(f'<path d="M 900 280 Q 950 240 1000 280 L 1000 380 Q 950 400 900 380 Z" fill="#FFFFFF" stroke="#D9C8B0" stroke-width="3"/>')

    # Owen：站姿，開心，頭髮濕濕
    e.append(boy(pose="stand", expr="smile", cx=380, cy=220, scale=1.1))
    # 浴巾圍在肩上（畫一個弧形布料在肩膀上）
    e.append(f'<path d="M 320 180 Q 380 160 440 180" fill="#F9E5D0" stroke="#D9C8B0" stroke-width="3"/>')
    # 頭頂水滴（3 個）
    for dx in [-20, 0, 20]:
        e.append(f'<path d="M {380+dx} 40 q 6 8 0 12 q -6 -4 0 -12 Z" fill="#A0D8F5"/>')

    # April：拿大浴巾
    e.append(april(cx=800, cy=280, scale=1.0, pose="stand"))
    # 大浴巾（April 手邊，簡單矩形）
    e.append(f'<rect x="720" y="240" width="100" height="120" rx="8" fill="#F9E5D0" stroke="#D9C8B0" stroke-width="3"/>')

    return svg(W, H, "".join(e))


def scene_p2():
    """p2：April 拿吹風機幫坐在小凳子上的 Owen 吹頭髮。"""
    e = []

    # 浴室背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#F5E8D8"/>')
    e.append(f'<line x1="0" y1="300" x2="1188" y2="300" stroke="#D9C8B0" stroke-width="3"/>')
    e.append(f'<rect x="0" y="480" width="1188" height="80" fill="#E8D7C5"/>')

    # 小凳子（中央）
    stool_cx, stool_cy = 450, 420
    e.append(f'<ellipse cx="{stool_cx}" cy="{stool_cy}" rx="50" ry="14" fill="#D4B896"/>')
    e.append(f'<rect x="{stool_cx-5}" y="{stool_cy}" width="10" height="50" rx="5" fill="#B09070"/>')

    # Owen 坐在凳子上（boy_bust，arms="desk"）
    e.append(boy_bust(expr="smile", cx=stool_cx, cy=360, scale=1.1, arms="desk"))

    # April 拿吹風機（pose='wave'）
    s = 1.0
    april_cx, april_cy = 800, 340
    e.append(april(cx=april_cx, cy=april_cy, scale=s, pose="wave"))
    # April 舉起的手位置：(cx + 80*s, cy - 2*s)
    hand_x = april_cx + 80*s
    hand_y = april_cy - 2*s
    # 吹風機握把在手上
    e.append(f'<ellipse cx="{hand_x-8}" cy="{hand_y}" rx="16" ry="20" fill="#E8823C"/>')
    e.append(f'<circle cx="{hand_x+5}" cy="{hand_y-20}" r="13" fill="#FFD9A8"/>')
    # 風流線（3 條暖黃波浪線從風口連到 Owen 頭部）
    for dy in [-10, 0, 10]:
        e.append(f'<path d="M {hand_x+13} {hand_y-20+dy} q 15 -8 30 0 q 15 8 30 0 q 15 -8 30 0" fill="none" stroke="#F7C977" stroke-width="3" stroke-linecap="round"/>')

    return svg(W, H, "".join(e))


def scene_p3():
    """p3：Owen 特寫（star 表情），暖風把頭髮吹起，四周音符與星星。"""
    e = []

    # 暖色背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#FFE8C2"/>')

    # 大光暈（風的感覺）
    e.append(f'<circle cx="594" cy="280" r="180" fill="#FFE8C2" fill-opacity="0.3"/>')
    e.append(f'<circle cx="594" cy="280" r="140" fill="#FFE8C2" fill-opacity="0.5"/>')

    # Owen 特寫（head）
    e.append(head(expr="star", cx=594, cy=240, scale=1.8))

    # 頭頂吹起的髮絲（用幾條弧線表示）
    for dx in [-40, -20, 0, 20, 40]:
        e.append(f'<path d="M {594+dx} 100 Q {594+dx+15} 60 {594+dx+10} 30" fill="none" stroke="#2A2320" stroke-width="4" stroke-linecap="round"/>')

    # 四周星星和音符
    e.append(star(350, 150, 22)); e.append(star(850, 160, 24))
    e.append(sparkle(420, 100, 14)); e.append(sparkle(780, 110, 14))

    # 簡單音符（兩組）
    e.append(f'<text x="300" y="380" font-family="Arial" font-size="48" fill="#E8944A">♪</text>')
    e.append(f'<text x="900" y="380" font-family="Arial" font-size="48" fill="#E8944A">♪</text>')

    return svg(W, H, "".join(e))


def scene_p4():
    """p4：衝動頁——Owen 坐凳上扭動。身體兩側波浪線、頭部殘影、凳子清楚。"""
    e = []

    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#FFD9C0"/>')

    # 凳子（明確的座面 + 腿）
    stool_cx, stool_cy = 450, 420
    # 座面（椅面）
    e.append(f'<ellipse cx="{stool_cx}" cy="{stool_cy}" rx="55" ry="16" fill="#D4B896" stroke="#B09070" stroke-width="2"/>')
    # 兩隻腿
    e.append(f'<rect x="{stool_cx-18}" y="{stool_cy}" width="8" height="50" rx="4" fill="#B09070"/>')
    e.append(f'<rect x="{stool_cx+10}" y="{stool_cy}" width="8" height="50" rx="4" fill="#B09070"/>')
    # 震動效果（淡化的重影凳子）
    for offset in [-6, 6]:
        e.append(f'<ellipse cx="{stool_cx+offset}" cy="{stool_cy}" rx="55" ry="16" fill="#D4B896" fill-opacity="0.2"/>')

    # Owen 坐在凳子上（boy_bust）
    e.append(boy_bust(expr="hold", cx=450, cy=360, scale=1.1, arms="desk"))

    # 身體兩側波浪扭動線
    for side_x in [330, 570]:
        e.append(f'<path d="M {side_x} 320 q 20 -15 40 0 q 20 15 40 0 q 20 -15 40 0" fill="none" stroke="#E4574C" stroke-width="6" stroke-linecap="round"/>')

    # 頭部左右搖殘影弧線（3 條弧）
    for dy in [-20, 0, 20]:
        e.append(f'<path d="M 350 {280+dy} Q 450 {240+dy} 550 {280+dy}" fill="none" stroke="#F26B5E" stroke-width="5" stroke-linecap="round" stroke-opacity="0.4"/>')

    # 紅熱氣線（幾條波浪在兩邊）
    for x_pos in [280, 620]:
        for dy in [-20, 0, 20]:
            e.append(f'<path d="M {x_pos} {300+dy} q 8 -12 16 0 q 8 12 16 0" fill="none" stroke="#F26B5E" stroke-width="4" stroke-linecap="round"/>')

    # April 的吹風機（追不上，在右邊，pose='wave'）
    s = 0.85
    april_cx, april_cy = 830, 340
    e.append(april(cx=april_cx, cy=april_cy, scale=s, pose="wave"))
    # 根據視覺調整，吹風機握把在舉起的手上（相對位置調整）
    # April wave pose 時舉起的手約在 (cx+68*s, cy+48*s) 到 (cx+78*s, cy+4*s) 之間
    dryer_x = april_cx + 75*s
    dryer_y = april_cy - 15*s
    # 吹風機機身和風口
    e.append(f'<ellipse cx="{dryer_x-12}" cy="{dryer_y}" rx="14" ry="17" fill="#E8823C"/>')
    e.append(f'<circle cx="{dryer_x+4}" cy="{dryer_y-18}" r="11" fill="#FFD9A8"/>')

    return svg(W, H, "".join(e))


def scene_p5():
    """p5：紫色星空。Owen press 表情端正坐在梯形基座上（雕像），身體外圈發光描邊。"""
    e = []

    # 紫色星空背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#4A3F7B"/>')

    # 滿天星星
    for (x, y, r) in [(140, 100, 16), (1050, 110, 18), (200, 450, 14), (1000, 470, 16)]:
        e.append(star(x, y, r, fill="#E8D4B0", stroke="#C9B88C"))
    e.append(sparkle(380, 70, 12, fill="#E8D4B0")); e.append(sparkle(820, 80, 12, fill="#E8D4B0"))

    # 雕像基座（梯形石台）
    base_cx, base_cy = 594, 480
    # 梯形：底部寬、頂部窄
    e.append(f'<path d="M {base_cx-110} {base_cy} L {base_cx-60} {base_cy-80} L {base_cx+60} {base_cy-80} L {base_cx+110} {base_cy} Z" fill="#9B9B9B" stroke="#6B6B6B" stroke-width="3"/>')
    # 石紋線（2 條橫線表示石台層次）
    e.append(f'<line x1="{base_cx-100}" y1="{base_cy-25}" x2="{base_cx+100}" y2="{base_cy-25}" stroke="#B0B0B0" stroke-width="2"/>')
    e.append(f'<line x1="{base_cx-90}" y1="{base_cy-50}" x2="{base_cx+90}" y2="{base_cy-50}" stroke="#B0B0B0" stroke-width="2"/>')

    # Owen 坐在基座頂部（boy_bust，press 表情）
    # bust 底部應該貼在基座台面（base_cy - 80）
    # boy_bust cy 決定頭部中心，底部約在 cy + 110*scale
    # 要讓底部 ≈ base_cy - 80，所以 cy + 110*scale ≈ base_cy - 80
    # cy ≈ base_cy - 80 - 110*scale
    # 用 scale=1.0：cy ≈ 480 - 80 - 110 = 290
    e.append(boy_bust(expr="press", cx=base_cx, cy=290, scale=1.0, arms="desk"))

    # 石雕發光描邊（人物外圈 2-3 層半透明白/金圓弧）
    e.append(f'<circle cx="{base_cx}" cy="290" r="140" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-opacity="0.3"/>')
    e.append(f'<circle cx="{base_cx}" cy="290" r="120" fill="none" stroke="#F7D99C" stroke-width="6" stroke-opacity="0.25"/>')
    e.append(f'<circle cx="{base_cx}" cy="290" r="100" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-opacity="0.2"/>')

    return svg(W, H, "".join(e))


def scene_p6():
    """p6：三步腳本。①腳貼地特寫 ②手放膝蓋 ③Owen 端坐數數（1/2/3 泡泡）。"""
    e = []

    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#E8DDD0"/>')

    # 地面
    e.append(f'<rect x="0" y="480" width="1188" height="80" fill="#D4C4B8"/>')

    # 第一格：腳貼地特寫（左上）
    # 畫兩個簡單腳印形狀 + 向下箭頭
    e.append(f'<g transform="translate(280, 180)">')
    # 左腳印
    e.append(f'<ellipse cx="-20" cy="0" rx="18" ry="28" fill="#FFFFFF" stroke="#B0A099" stroke-width="2"/>')
    # 右腳印
    e.append(f'<ellipse cx="20" cy="0" rx="18" ry="28" fill="#FFFFFF" stroke="#B0A099" stroke-width="2"/>')
    # 向下箭頭
    e.append(f'<line x1="0" y1="40" x2="0" y2="90" stroke="#B0A099" stroke-width="4" stroke-linecap="round"/>')
    e.append(f'<polygon points="0,90 -10,75 10,75" fill="#B0A099"/>')
    e.append(f'</g>')

    # 第二格：手放膝蓋特寫（右上）
    e.append(f'<g transform="translate(880, 180)">')
    # 圓角矩形（膝蓋框）
    e.append(f'<rect x="-40" y="-30" width="80" height="80" rx="16" fill="#FFFFFF" stroke="#B0A099" stroke-width="2"/>')
    # 手掌形狀圖示（簡單）
    e.append(f'<circle cx="-8" cy="0" r="16" fill="#FFD9B6"/>')  # 掌心
    e.append(f'<line x1="-8" y1="-16" x2="-8" y2="-32" stroke="#FFD9B6" stroke-width="5" stroke-linecap="round"/>')  # 拇指
    e.append(f'<line x1="-2" y1="-18" x2="8" y2="-35" stroke="#FFD9B6" stroke-width="5" stroke-linecap="round"/>')  # 食指
    e.append(f'<line x1="8" y1="-16" x2="16" y2="-30" stroke="#FFD9B6" stroke-width="5" stroke-linecap="round"/>')  # 中指
    e.append(f'</g>')

    # 第三格：Owen 端坐數數（底部中央）
    e.append(boy_bust(expr="press", cx=594, cy=340, scale=1.0, arms="desk"))

    # 頭上數數泡泡（1, 2, 3）
    for i, x_offset in enumerate([-50, 0, 50]):
        r = 28
        e.append(f'<circle cx="{594+x_offset}" cy="220" r="{r}" fill="#FFFFFF" stroke="#B0A8A0" stroke-width="3"/>')
        e.append(svgtext(594+x_offset, 235, str(i+1), size=40, fill="#5A7BA6", weight="bold"))

    return svg(W, H, "".join(e))


def scene_p7():
    """p7：觀點頁。兩格對比——左格灰調亂動 vs 右格亮色雕像。"""
    e = []

    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#EAE0D8"/>')

    # 左格背景（灰調）
    e.append(f'<rect x="20" y="80" width="540" height="420" rx="12" fill="#D0C5BA" stroke="#9B9B9B" stroke-width="2"/>')

    # 左格內容：亂動場景
    # April 皺眉版（站著，但表情不同——簡單用 stand 並加皺眉）
    e.append(april(cx=240, cy=320, scale=0.9, pose="stand"))
    # 吹風機
    e.append(f'<ellipse cx="320" cy="240" rx="16" ry="20" fill="#E8823C"/>')
    e.append(f'<circle cx="330" cy="210" r="12" fill="#FFD9A8"/>')
    # 時鐘轉很多圈（多層同心圓 + 箭頭轉動多圈）
    e.append(f'<circle cx="420" cy="200" r="40" fill="none" stroke="#9B9B9B" stroke-width="3"/>')
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        x1, y1 = 420 + 25*math.cos(rad), 200 + 25*math.sin(rad)
        x2, y2 = 420 + 35*math.cos(rad), 200 + 35*math.sin(rad)
        e.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#9B9B9B" stroke-width="2"/>')
    # 時鐘指針轉多圈（用多條半透明箭頭表示轉動）
    for rotation in [0, -60, -120, -180]:
        e.append(f'<line x1="420" y1="200" x2="420" y2="155" stroke="#9B9B9B" stroke-width="3" stroke-opacity="0.3" transform="rotate({rotation} 420 200)"/>')

    # Owen 坐著亂動（左格右下）
    e.append(boy_bust(expr="hold", cx=380, cy=380, scale=0.85, arms="desk"))
    # 扭動線
    e.append(f'<path d="M 310 340 q 15 -12 30 0 q 15 12 30 0" fill="none" stroke="#E4574C" stroke-width="4" stroke-linecap="round"/>')

    # 右格背景（亮色）
    e.append(f'<rect x="628" y="80" width="540" height="420" rx="12" fill="#FFF5E8" stroke="#E8C9A8" stroke-width="2"/>')

    # 右格內容：雕像時間
    # April 微笑 + 比讚手勢（pose='wave'）
    s_right = 0.9
    april_cx_r, april_cy_r = 750, 320
    e.append(april(cx=april_cx_r, cy=april_cy_r, scale=s_right, pose="wave"))
    # 簡單用星星表示比讚
    e.append(star(820, 200, 16, fill="#F7C977"))

    # 吹風機（握在舉起的手上）
    hand_x_r = april_cx_r + 80*s_right
    hand_y_r = april_cy_r - 2*s_right
    e.append(f'<ellipse cx="{hand_x_r-7}" cy="{hand_y_r}" rx="13" ry="16" fill="#E8823C"/>')
    e.append(f'<circle cx="{hand_x_r+3}" cy="{hand_y_r-16}" r="10" fill="#FFD9A8"/>')

    # 時鐘（只走一格）
    e.append(f'<circle cx="920" cy="200" r="40" fill="none" stroke="#7BC47F" stroke-width="3"/>')
    for angle in range(0, 360, 90):
        rad = math.radians(angle)
        x1, y1 = 920 + 25*math.cos(rad), 200 + 25*math.sin(rad)
        x2, y2 = 920 + 35*math.cos(rad), 200 + 35*math.sin(rad)
        e.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#7BC47F" stroke-width="2"/>')
    # 時鐘指針（單方向）
    e.append(f'<line x1="920" y1="200" x2="920" y2="155" stroke="#7BC47F" stroke-width="3"/>')
    e.append(f'<polygon points="920,155 916,165 924,165" fill="#7BC47F"/>')

    # Owen 端坐（右格右下）
    e.append(boy_bust(expr="press", cx=880, cy=380, scale=0.85, arms="desk"))
    # 光暈（小版本）
    e.append(f'<circle cx="880" cy="380" r="80" fill="none" stroke="#F7D99C" stroke-width="4" stroke-opacity="0.3"/>')

    return svg(W, H, "".join(e))


def scene_p8():
    """p8：吹好了。Owen 頭髮蓬鬆（sparkle ×3），April 舉手歡呼，語音泡泡。"""
    e = []

    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#F5E8D8"/>')

    # 地面
    e.append(f'<rect x="0" y="480" width="1188" height="80" fill="#E8D7C5"/>')

    # Owen 坐著（boy_bust，big 表情）
    e.append(boy_bust(expr="big", cx=380, cy=340, scale=1.1, arms="desk"))

    # 頭髮上 sparkle ×3
    e.append(sparkle(330, 210, 14, fill="#F7D99C"))
    e.append(sparkle(380, 170, 14, fill="#F7D99C"))
    e.append(sparkle(430, 200, 14, fill="#F7D99C"))

    # April 舉手歡呼（cheer 姿勢）
    e.append(april(cx=850, cy=300, scale=1.0, pose="cheer"))

    # 語音泡泡（大一點、文字清楚）
    bubble_x, bubble_y = 620, 140
    # 泡泡主體（橢圓＋尾巴）
    e.append(f'<ellipse cx="{bubble_x}" cy="{bubble_y}" rx="150" ry="60" fill="#FFFFFF" stroke="#E8C9A8" stroke-width="4"/>')
    # 泡泡尾巴（指向 April）
    e.append(f'<path d="M {bubble_x-100} {bubble_y+60} L {bubble_x-120} {bubble_y+110} L {bubble_x-60} {bubble_y+70}" fill="#FFFFFF" stroke="#E8C9A8" stroke-width="3"/>')
    # 文字（分兩行，確保在泡泡內）
    e.append(svgtext(bubble_x, bubble_y-8, "Wow, my statue boy,", size=18, fill="#B85E22", weight="bold"))
    e.append(svgtext(bubble_x, bubble_y+22, "Owen!", size=18, fill="#B85E22", weight="bold"))

    return svg(W, H, "".join(e))


def scene_p9():
    """p9：轉移頁三個直式並排面板。①浴缸 ②刷牙 ③吹頭髮——每格右上角小雕像 icon。"""
    e = []

    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#F0E5D5"/>')

    # 三個並排面板，每個約 360 寬（11px 邊距）
    panel_w = 360
    panel_h = 560
    panel_gaps = [10, 10 + panel_w, 10 + 2*panel_w]

    # ===== 面板 1：浴缸 =====
    panel_x = panel_gaps[0]
    e.append(f'<rect x="{panel_x}" y="10" width="{panel_w}" height="{panel_h-20}" rx="14" fill="#FFFFFF" stroke="#D4C4B8" stroke-width="2"/>')

    # 浴缸（夠大且清楚）
    tub_cx = panel_x + panel_w // 2
    tub_cy = 220
    e.append(f'<path d="M {tub_cx-110} {tub_cy-50} Q {tub_cx-130} {tub_cy+30} {tub_cx-110} {tub_cy+90} L {tub_cx+110} {tub_cy+90} Q {tub_cx+130} {tub_cy+30} {tub_cx+110} {tub_cy-50} Z" fill="#FFFFFF" stroke="#B0A099" stroke-width="3"/>')
    # 泡泡
    e.append(f'<circle cx="{tub_cx-60}" cy="{tub_cy}" r="12" fill="#A0D8F5"/>')
    e.append(f'<circle cx="{tub_cx}" cy="{tub_cy-25}" r="10" fill="#A0D8F5"/>')
    e.append(f'<circle cx="{tub_cx+60}" cy="{tub_cy+10}" r="11" fill="#A0D8F5"/>')
    # Owen 頭露出（用 head）
    e.append(head(expr="smile", cx=tub_cx, cy=tub_cy-100, scale=1.0))

    # 小雕像 icon（右上角）
    e.append(f'<g transform="translate({panel_x + panel_w - 35}, 30)">')
    e.append(f'<circle cx="0" cy="-8" r="9" fill="#8B8B8B"/>')
    e.append(f'<path d="M -6 0 L 6 0 L 5 20 L -5 20 Z" fill="#8B8B8B"/>')
    e.append(f'<ellipse cx="-7" cy="22" rx="4" ry="3" fill="#8B8B8B"/>')
    e.append(f'<ellipse cx="7" cy="22" rx="4" ry="3" fill="#8B8B8B"/>')
    e.append(f'</g>')

    # ===== 面板 2：刷牙 =====
    panel_x = panel_gaps[1]
    e.append(f'<rect x="{panel_x}" y="10" width="{panel_w}" height="{panel_h-20}" rx="14" fill="#FFFFFF" stroke="#D4C4B8" stroke-width="2"/>')

    # Owen 全身站姿拿牙刷
    boy_cx = panel_x + panel_w // 2
    boy_cy = 240
    s = 0.9
    e.append(boy(pose="stand", expr="smile", cx=boy_cx, cy=boy_cy, scale=s))
    # 牙刷（握在右手位置：cx+48*s, cy+136*s）
    brush_x = boy_cx + 48*s
    brush_y = boy_cy + 136*s
    e.append(f'<rect x="{brush_x-2}" y="{brush_y-24}" width="4" height="28" fill="#C9A26B" stroke="#A0824A" stroke-width="1"/>')  # 握把
    e.append(f'<rect x="{brush_x-8}" y="{brush_y-26}" width="16" height="16" rx="2" fill="#F9E5D0"/>')  # 刷毛

    # 小雕像 icon（右上角）
    e.append(f'<g transform="translate({panel_x + panel_w - 35}, 30)">')
    e.append(f'<circle cx="0" cy="-8" r="9" fill="#8B8B8B"/>')
    e.append(f'<path d="M -6 0 L 6 0 L 5 20 L -5 20 Z" fill="#8B8B8B"/>')
    e.append(f'<ellipse cx="-7" cy="22" rx="4" ry="3" fill="#8B8B8B"/>')
    e.append(f'<ellipse cx="7" cy="22" rx="4" ry="3" fill="#8B8B8B"/>')
    e.append(f'</g>')

    # ===== 面板 3：吹頭髮 =====
    panel_x = panel_gaps[2]
    e.append(f'<rect x="{panel_x}" y="10" width="{panel_w}" height="{panel_h-20}" rx="14" fill="#FFFFFF" stroke="#D4C4B8" stroke-width="2"/>')

    # 凳子 + Owen 坐著
    stool_cx = panel_x + panel_w // 2
    stool_cy = 320
    # 凳子座面 + 腿
    e.append(f'<ellipse cx="{stool_cx}" cy="{stool_cy}" rx="50" ry="15" fill="#D4B896" stroke="#B09070" stroke-width="2"/>')
    e.append(f'<rect x="{stool_cx-16}" y="{stool_cy}" width="8" height="45" rx="4" fill="#B09070"/>')
    e.append(f'<rect x="{stool_cx+8}" y="{stool_cy}" width="8" height="45" rx="4" fill="#B09070"/>')
    # Owen 坐著（boy_bust，稍大）
    e.append(boy_bust(expr="smile", cx=stool_cx, cy=240, scale=1.0, arms="desk"))
    # 吹風機（握在右手上）
    dryer_x = stool_cx + 70
    dryer_y = 180
    e.append(f'<ellipse cx="{dryer_x-12}" cy="{dryer_y}" rx="15" ry="19" fill="#E8823C"/>')
    e.append(f'<circle cx="{dryer_x+5}" cy="{dryer_y-22}" r="12" fill="#FFD9A8"/>')

    # 小雕像 icon（右上角）
    e.append(f'<g transform="translate({panel_x + panel_w - 35}, 30)">')
    e.append(f'<circle cx="0" cy="-8" r="9" fill="#8B8B8B"/>')
    e.append(f'<path d="M -6 0 L 6 0 L 5 20 L -5 20 Z" fill="#8B8B8B"/>')
    e.append(f'<ellipse cx="-7" cy="22" rx="4" ry="3" fill="#8B8B8B"/>')
    e.append(f'<ellipse cx="7" cy="22" rx="4" ry="3" fill="#8B8B8B"/>')
    e.append(f'</g>')

    return svg(W, H, "".join(e))


def scene_p10():
    """p10：英雄收尾。Owen 披紅披風站在雕像基座上，頭髮蓬鬆有光澤，滿天星。"""
    e = []

    # 星空背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#5B4A8E"/>')

    # 滿天星星
    for (x, y, r) in [(140, 90, 18), (1050, 100, 20), (180, 480, 16), (1020, 490, 18), (320, 240, 14), (900, 260, 14)]:
        e.append(star(x, y, r, fill="#E8D4B0", stroke="#C9B88C"))
    e.append(sparkle(400, 150, 14, fill="#E8D4B0")); e.append(sparkle(800, 160, 14, fill="#E8D4B0"))

    # 雕像基座
    base_cx, base_cy = 594, 480
    e.append(f'<path d="M {base_cx-100} {base_cy} L {base_cx-70} {base_cy-80} L {base_cx+70} {base_cy-80} L {base_cx+100} {base_cy} Z" fill="#9B9B9B" stroke="#6B6B6B" stroke-width="3"/>')
    e.append(f'<line x1="{base_cx-100}" y1="{base_cy-3}" x2="{base_cx+100}" y2="{base_cy-3}" stroke="#B0B0B0" stroke-width="2"/>')

    # Owen 站在基座上（boy with cape）
    # feet_y = cy + 228*scale
    # 要讓腳落在基座頂部（base_cy - 80），所以需要計算 cy
    # feet_y = base_cy - 80 = cy + 228*scale
    # cy = base_cy - 80 - 228*scale
    # 用 scale=1.0，cy = 480 - 80 - 228 = 172
    e.append(boy(pose="stand", expr="proud", cx=base_cx, cy=172, scale=1.0, cape=True))

    # 頭髮上 sparkle ×3（表示蓬鬆發亮）
    e.append(sparkle(base_cx-25, 130, 12, fill="#F7D99C"))
    e.append(sparkle(base_cx, 115, 14, fill="#F7D99C"))
    e.append(sparkle(base_cx+25, 130, 12, fill="#F7D99C"))

    return svg(W, H, "".join(e))


# =============== PAGE TEXTS ===============

PAGES = [
    ("p1", scene_p1, "This is me, <b>Owen</b>!<br/>Bath is done. My hair is wet!"),
    ("p2", scene_p2, "After bath, Mommy dries my hair.<br/><b>Whoosh!</b> The <b>dryer</b> is loud and warm."),
    ("p3", scene_p3, "The warm wind is funny!<br/>I want to jump and dance!"),
    ("p4", scene_p4, "My body feels <b>wiggly</b>!<br/>My feet want to dance.<br/><b>Wiggle, wiggle</b> goes my head!"),
    ("p5", scene_p5, "<b>STOP!</b> I use my superpower&hellip;<br/><b>Statue</b> time!"),
    ("p6", scene_p6, "Feet on the floor.<br/>Hands on my knees.<br/>I count: one, two, three!"),
    ("p7", scene_p7, "When I am still, Mommy is fast.<br/>The hot wind stays safe.<br/>Then play time comes quick!"),
    ("p8", scene_p8, "All done, so fast!<br/>Mommy April smiles.<br/>&ldquo;Wow, my statue boy, <b>Owen</b>!&rdquo;"),
    ("p9", scene_p9, "Bath time? <b>Statue</b> time!<br/>Teeth time? Statue time!<br/>I feel <b>GREAT</b>!"),
    ("p10", scene_p10, "Feet down. Hands on knees.<br/><b>Statue time!</b><br/>I practice every day!"),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3–4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("<b>Statue 和 Freeze 是兩顆不同的肌肉</b>", "Freeze（足球書）是「被叫到瞬間停」，Statue 是「照護期間持續不動」。喊對口訣——吹頭髮用 &ldquo;Statue time!&rdquo;，不要混用。"),
    ("把雕像變遊戲", "平時玩「誰能當最久的雕像」比賽（10 秒起跳、逐步加長），照護時間才提領這個存款。數數或唱一首固定的歌，讓「還要多久」變得可預測。"),
    ("當他主動說 'My body feels wiggly'", "= 他察覺到躁動了，大力稱讚。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

BOOK = {
    "slug": "statue-time",
    "order": 7,
    "title_pre": "",
    "title_hi": "Statue",
    "title_post": " Time!",
    "title_zh": "雕像時間",
    "subtitle": "Owen's bath time story",
    "tagline_zh": "Owen 的照護時間故事",
    "chips": ["Social Story", "Home", "12 pages"],
    "pdf_name": "Statue_Time.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ['wiggly', 'statue', 'dryer'],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>在照護時間用得出來的「雕像模式」動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Feet down → Hands on knees → Statue time!</b>&nbsp;"
                 "當他哪天主動說出 &ldquo;My body feels wiggly&rdquo;（我察覺到躁動了），"
                 "就是最值得大力稱讚的時刻。"),
    "cover": scene_cover,
}
