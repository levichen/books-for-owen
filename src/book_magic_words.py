# -*- coding: utf-8 -*-
"""Book: My Magic Words! — 匹克球禮貌語魔法詞彙（全書 white T，無背號）。"""
from parts import *
from book_common import svg, svgtext, TXT, W, H, COVER_W, COVER_H
import math

# soft page palettes
BG = {
    "cover": "#FFE5CC", "p1": "#C8EBF5", "p2": "#E0F0FF", "p3": "#FFF8E0",
    "p4": "#FFE8DC", "p5": "#E8DCFF", "p6": "#F0EAF8", "p7": "#E0F8E4",
    "p8": "#FFF3E0", "p9": "#FFECF5", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

# ============ HELPER FUNCTIONS ============

def paddle(cx, cy, angle, scale):
    """匹克球拍：握把端在 (0,0)，拍面圓角橢圓（藍）＋握把。
    返回以 (cx, cy) 為中心、旋轉 angle 度的 SVG。"""
    p = []
    # 握把：粗棒，寬 14px，長 60px，讓手能清楚握住
    p.append(f'<rect x="-7" y="0" width="14" height="60" rx="4" fill="#8A5A3C" stroke="#5C3E2C" stroke-width="2"/>')
    # 握把上有淺色條紋增加質感
    for y_pos in [12, 30, 48]:
        p.append(f'<line x1="-5" y1="{y_pos}" x2="5" y2="{y_pos}" stroke="#C9A887" stroke-width="2" stroke-linecap="round"/>')
    # 拍面：圓角橢圓，寬 72, 高 95
    p.append(f'<ellipse cx="0" cy="-88" rx="36" ry="48" fill="#1E90FF" stroke="#0054CC" stroke-width="3"/>')
    # 邊框深色
    p.append(f'<ellipse cx="0" cy="-88" rx="36" ry="48" fill="none" stroke="#003366" stroke-width="1.5" stroke-dasharray="5 7"/>')
    inner = "".join(p)
    return f'<g transform="translate({cx},{cy}) rotate({angle}) scale({scale})">{inner}</g>'


def wiffle(cx, cy, r):
    """洞洞球（Wiffle ball）：黃色圓＋5-6 個小圓孔分佈。"""
    w = []
    w.append(f'<circle cx="0" cy="0" r="{r}" fill="#FFD34D" stroke="#E8A20C" stroke-width="2.5"/>')
    # 5 個洞孔，均勻分佈
    for i in range(5):
        angle = math.radians(i * 72)
        hole_x = r * 0.55 * math.cos(angle)
        hole_y = r * 0.55 * math.sin(angle)
        w.append(f'<circle cx="{hole_x:.0f}" cy="{hole_y:.0f}" r="{r*0.18:.0f}" fill="#C98A0C" fill-opacity="0.7"/>')
    inner = "".join(w)
    return f'<g transform="translate({cx},{cy})">{"".join(w)}</g>'


def magic_card(cx, cy, word, scale, glow=False, hiding=False):
    """魔法卡片：白色圓角卡＋彩色邊框＋文字（固定字級）＋底部兩隻小腳。
    word: "PLEASE" (粉紅) / "THANK YOU" (綠，兩行) / "SORRY" (藍)
    glow=True 時外圈 2 層半透明金圓；hiding=True 時卡片變半透明淡色（躲藏狀態）。"""
    colors = {
        "PLEASE": "#FF69B4",      # 粉紅
        "THANK YOU": "#7BC47F",   # 綠
        "SORRY": "#5CA8E8",       # 藍
    }
    edge_color = colors.get(word, "#FF69B4")

    c = []

    # 光暈（如果 glow=True）
    if glow:
        c.append(f'<circle cx="0" cy="0" r="62" fill="#FFD34D" fill-opacity="0.22"/>')
        c.append(f'<circle cx="0" cy="0" r="48" fill="#FFD34D" fill-opacity="0.18"/>')

    # 卡片主體：白色圓角矩形
    if word == "THANK YOU":
        card_w, card_h = 100, 70  # 加寬以容納兩行
    else:
        card_w, card_h = 84, 60

    fill_color = "#FFFFFF" if not hiding else "#F5F5F5"
    fill_opacity = "1" if not hiding else "0.45"
    stroke_opacity = "1" if not hiding else "0.5"

    c.append(f'<rect x="{-card_w/2}" y="{-card_h/2}" width="{card_w}" height="{card_h}" rx="8" fill="{fill_color}" fill-opacity="{fill_opacity}" stroke="{edge_color}" stroke-width="4" stroke-opacity="{stroke_opacity}"/>')

    # 文字（固定字級，不隨外層 scale 縮放）
    text_opacity = "1" if not hiding else "0.55"

    if word == "THANK YOU":
        # 兩行：THANK 上、YOU 下
        c.append(f'<text x="0" y="-4" font-family="Huninn" font-size="14" font-weight="bold" fill="{edge_color}" fill-opacity="{text_opacity}" text-anchor="middle">THANK</text>')
        c.append(f'<text x="0" y="14" font-family="Huninn" font-size="14" font-weight="bold" fill="{edge_color}" fill-opacity="{text_opacity}" text-anchor="middle">YOU</text>')
    else:
        # 單行
        fontsize = 20
        c.append(f'<text x="0" y="8" font-family="Huninn" font-size="{fontsize}" font-weight="bold" fill="{edge_color}" fill-opacity="{text_opacity}" text-anchor="middle" dominant-baseline="middle">{word}</text>')

    # 小腳：兩隻腳，左右分開
    foot_y = card_h/2 + 8
    foot_opacity = "1" if not hiding else "0.5"
    c.append(f'<circle cx="-16" cy="{foot_y}" r="5" fill="{edge_color}" fill-opacity="{foot_opacity}"/>')
    c.append(f'<circle cx="16" cy="{foot_y}" r="5" fill="{edge_color}" fill-opacity="{foot_opacity}"/>')

    inner = "".join(c)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def pickleball_net(cx, cy, net_height=80):
    """匹克球網：中央位置，兩根柱子 + 橫帶 + 網格線。
    cx, cy 為中央下底端；net_height 為網的高度（含柱子頂）。"""
    n = []
    # 左柱
    n.append(f'<rect x="-180" y="{-net_height}" width="14" height="{net_height}" fill="#8B4513" stroke="#654321" stroke-width="2"/>')
    # 右柱
    n.append(f'<rect x="166" y="{-net_height}" width="14" height="{net_height}" fill="#8B4513" stroke="#654321" stroke-width="2"/>')
    # 頂部橫帶
    n.append(f'<rect x="-180" y="{-net_height-8}" width="360" height="16" rx="4" fill="#4A4A4A"/>')
    # 網格線（豎）
    for x in range(-170, 170, 28):
        n.append(f'<line x1="{x}" y1="{-net_height+4}" x2="{x}" y2="-8" stroke="#D9D2C4" stroke-width="1.5" stroke-opacity="0.6"/>')
    # 網格線（橫）
    for y in range(-net_height+4, 0, 16):
        n.append(f'<line x1="-170" y1="{y}" x2="170" y2="{y}" stroke="#D9D2C4" stroke-width="1.5" stroke-opacity="0.6"/>')
    inner = "".join(n)
    return f'<g transform="translate({cx},{cy})">{"".join(n)}</g>'


def speech_bubble(cx, cy, text, color="#FFFFFF", text_color=TXT, width=120, height=50):
    """語音泡泡：圓角矩形＋三角指針。"""
    s = []
    s.append(f'<rect x="{-width/2}" y="{-height/2}" width="{width}" height="{height}" rx="12" fill="{color}" stroke="{text_color}" stroke-width="3"/>')
    # 三角指針（指向下方）
    s.append(f'<polygon points="0,{height/2} -14,{height/2+16} 14,{height/2+16}" fill="{color}" stroke="{text_color}" stroke-width="2"/>')
    # 文字
    fontsize = 18 if len(text) <= 10 else 16
    s.append(svgtext(0, 2, text, size=fontsize, fill=text_color, anchor="middle", weight="bold"))
    inner = "".join(s)
    return f'<g transform="translate({cx},{cy})">{"".join(s)}</g>'


# ============ SCENES ============

def scene_cover():
    """封面：Owen 拿拍＋Daddy＋wiffle 球＋暖色星星。"""
    e = []
    # 背景星星（暖色）
    for (x, y, r) in [(140, 100, 18), (1040, 140, 22), (180, 480, 14), (1020, 520, 16), (350, 80, 12), (850, 500, 14)]:
        e.append(star(x, y, r, fill="#FFD34D"))
    e.append(sparkle(280, 220, 11, fill="#FFD34D")); e.append(sparkle(900, 300, 10, fill="#FFD34D"))

    # 場地
    e.append(f'<ellipse cx="594" cy="650" rx="560" ry="120" fill="#F4B847"/>')

    # Daddy 左側（feet_y ≈ 260 + 216*1.2 = 519）
    e.append(daddy(cx=280, cy=260, scale=1.2, pose="stand"))

    # Owen 中央，拿拍
    # swing 姿勢，握把在 (cx+88*scale, cy+50*scale) = (594+88*1.3, 200+50*1.3) ≈ (708, 265)
    e.append(boy(pose="swing", expr="smile", cx=594, cy=200, scale=1.3))
    # paddle 握把端設在 swing 的雙手位置，angle=-50 讓拍面朝右下，遠離頭
    e.append(paddle(708, 265, angle=60, scale=1.1))

    # wiffle 球（掉落在身邊下方）
    e.append(wiffle(550, 420, 24))

    return svg(COVER_W, COVER_H, "".join(e), bg=BG["cover"])


def scene_p1():
    """p1：Owen 拿拍＋Daddy 開心出發。"""
    e = []
    # 背景：陽光、雲、遠景球場
    e.append(sun(1050, 90, 36))
    e.append(cloud(220, 100, 1.0)); e.append(cloud(900, 80, 0.8))

    # 路徑
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#C9EBB8"/>')
    e.append(f'<path d="M 0 560 Q 594 400 1188 560 L 1188 560 L 0 560 Z" fill="#E8D2AC"/>')

    # 遠景球場建築
    e.append(f'<rect x="900" y="280" width="200" height="140" rx="8" fill="#E8C9A0" stroke="#C9A577" stroke-width="3"/>')
    e.append(f'<rect x="960" y="360" width="50" height="60" rx="4" fill="#8A5A3C"/>')
    e.append(f'<rect x="920" y="310" width="40" height="34" rx="3" fill="#B8E3F2"/>')
    e.append(f'<rect x="1010" y="310" width="40" height="34" rx="3" fill="#B8E3F2"/>')

    # 人物：Daddy 左側
    e.append(daddy(cx=320, cy=260, scale=1.0, pose="stand"))

    # Owen 中央偏右，拿拍（swing 姿勢），表情開心
    e.append(boy(pose="swing", expr="smile", cx=520, cy=220, scale=1.15))
    # paddle 在握手位置
    e.append(paddle(520+88*1.15, 220+50*1.15, angle=60, scale=0.95))

    # 星星和火花表示興奮
    e.append(star(680, 100, 18)); e.append(sparkle(760, 140, 12)); e.append(sparkle(420, 110, 10))

    return svg(W, H, "".join(e), bg=BG["p1"])


def scene_p2():
    """p2：球場全景，中央矮網，球飛虛線弧線，POP 字效。"""
    e = []
    # 球場地面：淺藍綠色帶 + 白線
    e.append(f'<rect x="0" y="350" width="1188" height="210" fill="#D4F0E8"/>')
    e.append(f'<line x1="594" y1="350" x2="594" y2="560" stroke="#FFFFFF" stroke-width="4"/>')  # 中線
    e.append(f'<line x1="200" y1="480" x2="988" y2="480" stroke="#FFFFFF" stroke-width="3"/>')  # 邊界線

    # 球網（中央）
    e.append(pickleball_net(594, 480, net_height=90))

    # Owen 左側，swing 姿勢
    e.append(boy(pose="swing", expr="big", cx=280, cy=320, scale=1.1))
    e.append(paddle(280+88*1.1, 320+50*1.1, angle=60, scale=0.9))

    # Daddy 右側，swing 姿勢
    e.append(daddy(cx=910, cy=320, scale=1.1, pose="stand"))

    # 球飛的虛線弧 + POP 字效
    # 虛線弧從 Owen 的拍面位置經過網上空，到 Daddy 方向
    e.append(f'<path d="M 368 340 Q 594 280 820 360" fill="none" stroke="#FFD34D" stroke-width="4" stroke-dasharray="8 12" stroke-linecap="round"/>')

    # wiffle 球在弧線中點
    e.append(wiffle(594, 310, 22))

    # POP 字效
    e.append(f'<circle cx="650" cy="250" r="28" fill="none" stroke="#FF6B6B" stroke-width="3"/>')
    e.append(svgtext(650, 260, "POP", size=32, fill="#FF6B6B", weight="bold"))

    return svg(W, H, "".join(e), bg=BG["p2"])


def scene_p3():
    """p3：Owen 特寫（star 表情），眼睛盯著球，身體前傾。"""
    e = []
    # 球場地面
    e.append(f'<rect x="0" y="480" width="1188" height="80" fill="#D4F0E8"/>')

    # 大型 wiffle 球在上方，發光
    e.append(f'<circle cx="420" cy="140" r="85" fill="#FFD34D" fill-opacity="0.25"/>')
    e.append(f'<circle cx="420" cy="140" r="55" fill="#FFD34D" stroke="#E8A20C" stroke-width="4"/>')
    # 球面細節
    for i in range(5):
        angle = math.radians(i * 72)
        hole_x = 420 + 55 * 0.55 * math.cos(angle)
        hole_y = 140 + 55 * 0.55 * math.sin(angle)
        e.append(f'<circle cx="{hole_x:.0f}" cy="{hole_y:.0f}" r="10" fill="#C98A0C" fill-opacity="0.8"/>')

    # 星星裝飾（表情）
    e.append(star(280, 220, 22, fill=STAR_Y)); e.append(star(560, 60, 20))
    e.append(sparkle(180, 140, 11)); e.append(sparkle(720, 220, 12))

    # Owen 特寫（star 表情），身體前傾感（用 walk 或自訂位置）
    e.append(boy(pose="stand", expr="star", cx=700, cy=340, scale=1.4))

    return svg(W, H, "".join(e), bg=BG["p3"])


def scene_p4():
    """p4：衝動頁。Owen 左中 swing 伸向右邊，速度線向右，大聲線在嘴邊右側。
    Anne 在右側完整可見，三張 hiding 卡片在 Owen 身後左下不碰身體。"""
    e = []
    # 球場
    e.append(f'<rect x="0" y="420" width="1188" height="140" fill="#D4F0E8"/>')

    # Owen swing 姿勢，左中位置（feet_y ≈ 250 + 228*1.2 = 524，調整到 235）
    e.append(boy(pose="swing", expr="hold", cx=350, cy=235, scale=1.2))
    # paddle 握把端在 swing 手位置 (350+88*1.2, 235+50*1.2) = (455, 295)
    # angle=-45 讓拍面朝右下外側，遠離頭
    e.append(paddle(455, 295, angle=60, scale=0.95))

    # 速度線（從 Owen 向右伸出，表示衝動）
    for i in range(5):
        angle = math.radians(-30 + i * 30)  # 右側半圓
        x1, y1 = 350 + 110*math.cos(angle), 235 + 110*math.sin(angle)
        x2, y2 = 350 + 160*math.cos(angle), 235 + 160*math.sin(angle)
        e.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#FF4444" stroke-width="6" stroke-linecap="round"/>')

    # 大聲線（在嘴邊右側，只在右邊）
    for (offset_x, offset_y) in [(25, -12), (32, 0), (28, 12), (38, -6), (40, 6)]:
        e.append(f'<path d="M {370+offset_x} {260+offset_y} l 12 0" fill="none" stroke="#FF4444" stroke-width="5" stroke-linecap="round"/>')

    # Anne 在右側，完整可見，oh 表情，驚訝
    e.append(ann(cx=880, cy=330, scale=1.15, expr="oh"))

    # wiffle 球在 Anne 手邊（不碰 Anne 身體）
    e.append(wiffle(820, 270, 20))

    # 三張 magic_card(hiding=True) 躲在 Owen 身後左下
    # 卡片位置：在 Owen 身後（距身體中心 > 100），不碰身體
    e.append(magic_card(240, 360, "PLEASE", scale=0.78, glow=False, hiding=True))
    e.append(magic_card(280, 420, "THANK YOU", scale=0.78, glow=False, hiding=True))
    e.append(magic_card(200, 420, "SORRY", scale=0.78, glow=False, hiding=True))

    return svg(W, H, "".join(e), bg=BG["p4"])


def scene_p5():
    """p5：紫星空＋Owen press＋三張 magic_card(glow=True) 繞身飛回（虛線弧）。
    卡片軌道半徑 ≥200，離身體中心遠，不碰頭。"""
    e = []
    # 紫色星空背景（整個畫面）
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#E8DCFF"/>')

    # 星星（紫空中）
    for (x, y, r) in [(140, 120, 18), (1040, 130, 20), (200, 420, 14), (1000, 430, 16), (350, 60, 12), (850, 80, 14)]:
        e.append(star(x, y, r, fill="#FFD34D" if (x+y) % 2 == 0 else STAR_Y))
    e.append(sparkle(280, 200, 12)); e.append(sparkle(900, 240, 11))

    # Owen 中央，press 表情（cy=230 → feet_y = 230+228*1.25 = 515，畫布內）
    e.append(boy(pose="stand", expr="press", cx=594, cy=230, scale=1.25))

    # 三張 magic_card 發光，繞身飛回（不碰身體：上左／上右／左下）
    cards = [(400, 130, "PLEASE"), (788, 130, "SORRY"), (350, 400, "THANK YOU")]
    # 虛線弧只連卡片之間（繞過人物上方）
    e.append(f'<path d="M 440 110 Q 594 40 748 110" fill="none" stroke="{STAR_DK}" stroke-width="2" stroke-dasharray="4 8" stroke-linecap="round"/>')
    for card_x, card_y, word in cards:
        e.append(magic_card(card_x, card_y, word, scale=0.85, glow=True, hiding=False))

    return svg(W, H, "".join(e), bg=BG["p5"])


def scene_p6():
    """p6：三格腳本，各一時刻＋語音泡泡（尾巴指向嘴）。人物拉開不重疊。"""
    e = []
    # 球場地面
    e.append(f'<rect x="0" y="480" width="1188" height="80" fill="#D4F0E8"/>')

    # 三格分隔線
    e.append(f'<line x1="396" y1="60" x2="396" y2="480" stroke="#4A4A4A" stroke-width="2" stroke-dasharray="3 6"/>')
    e.append(f'<line x1="792" y1="60" x2="792" y2="480" stroke="#4A4A4A" stroke-width="2" stroke-dasharray="3 6"/>')

    # 格 1：Owen 指向球，說 "Please!"
    e.append(wiffle(280, 240, 20))
    e.append(boy(pose="stand", expr="smile", cx=180, cy=340, scale=0.95))
    # 語音泡泡帶尾巴指向 Owen 嘴（Owen 嘴在約 180, 380）
    e.append(f'<ellipse cx="280" cy="130" rx="55" ry="32" fill="#FFE0F0" stroke="#FF1493" stroke-width="3"/>')
    e.append(f'<polygon points="280,160 265,180 295,180" fill="#FFE0F0" stroke="#FF1493" stroke-width="3"/>')
    e.append(svgtext(280, 135, "Please!", size=18, fill="#FF1493", anchor="middle", weight="bold"))

    # 格 2：Owen 接球，說 "Thank you!"
    e.append(wiffle(594, 240, 20))
    e.append(boy(pose="stand", expr="big", cx=520, cy=340, scale=0.95))
    # 語音泡泡帶尾巴指向 Owen 嘴（Owen 嘴在約 520, 380）
    e.append(f'<ellipse cx="594" cy="130" rx="62" ry="32" fill="#E0F8E4" stroke="#228B22" stroke-width="3"/>')
    e.append(f'<polygon points="594,160 572,180 616,180" fill="#E0F8E4" stroke="#228B22" stroke-width="3"/>')
    e.append(svgtext(594, 135, "Thank you!", size=16, fill="#228B22", anchor="middle", weight="bold"))

    # 格 3：Owen 和 Anne 拉開，球在兩人之間
    e.append(wiffle(850, 360, 20))
    e.append(boy(pose="stand", expr="press", cx=750, cy=340, scale=0.95))
    e.append(ann(cx=900, cy=340, scale=0.95, expr="smile"))
    # 語音泡泡帶尾巴指向 Owen 嘴（Owen 嘴在約 750, 380）
    e.append(f'<ellipse cx="900" cy="130" rx="50" ry="32" fill="#E0F0FF" stroke="#0066CC" stroke-width="3"/>')
    e.append(f'<polygon points="900,160 880,180 920,180" fill="#E0F0FF" stroke="#0066CC" stroke-width="3"/>')
    e.append(svgtext(900, 135, "Sorry!", size=18, fill="#0066CC", anchor="middle", weight="bold"))

    return svg(W, H, "".join(e), bg=BG["p6"])


def scene_p7():
    """p7：觀點頁。Anne 和 Daddy 都笑著，頭上小愛心；三張魔法卡片在空中發光。"""
    e = []
    # 球場地面
    e.append(f'<rect x="0" y="400" width="1188" height="160" fill="#D4F0E8"/>')

    # Owen 中央，開心表情
    e.append(boy(pose="stand", expr="smile", cx=594, cy=280, scale=1.25))

    # Anne 左側，開心笑容
    e.append(ann(cx=240, cy=340, scale=1.1, expr="smile"))

    # Daddy 右側，開心笑容
    e.append(daddy(cx=948, cy=340, scale=1.1, pose="stand"))

    # 愛心（在三人頭上方）
    for (hx, hy) in [(240, 180), (594, 140), (948, 180)]:
        e.append(f'<path d="M {hx} {hy} c 0 -8 8 -16 16 -16 c 8 0 16 8 16 16 c 0 8 -16 24 -16 24 c 0 -24 -16 -24 -16 -24 c 0 -8 8 -16 16 -16" '
                 f'fill="#FF6B9D" stroke="#E84A7F" stroke-width="2"/>')

    # 三張發光卡片在空中（靜止狀態，不飛）
    e.append(magic_card(200, 160, "PLEASE", scale=0.85, glow=True, hiding=False))
    e.append(magic_card(594, 100, "THANK YOU", scale=0.85, glow=True, hiding=False))
    e.append(magic_card(988, 160, "SORRY", scale=0.85, glow=True, hiding=False))

    # 星星和火花
    e.append(star(350, 80, 18)); e.append(star(800, 90, 16))
    e.append(sparkle(480, 140, 11)); e.append(sparkle(700, 150, 10))

    return svg(W, H, "".join(e), bg=BG["p7"])


def scene_p8():
    """p8：球滾到 Daddy 腳邊。Owen 語音泡泡 "Please, Daddy!"，Daddy 遞球，語音泡泡 "Nice words, Owen!"。"""
    e = []
    # 球場地面
    e.append(f'<rect x="0" y="420" width="1188" height="140" fill="#D4F0E8"/>')

    # wiffle 球在中央地面
    e.append(wiffle(594, 480, 22))

    # Owen 左側，站立，專注表情，喊 "Please, Daddy!"（feet_y ≈ 260 + 228*1.1 = 511）
    e.append(boy(pose="stand", expr="smile", cx=280, cy=260, scale=1.1))
    e.append(speech_bubble(280, 140, "Please,\nDaddy!", color="#FFE0F0", text_color="#FF1493", width=110, height=60))

    # Daddy 右側，point 姿勢（指向球），拿著球，喊 "Nice words, Owen!"（feet_y ≈ 280 + 216*1.1 = 518）
    e.append(daddy(cx=910, cy=280, scale=1.1, pose="point"))
    # 球在 Daddy 指向的手位置（point 手大約在 (104*scale, 40*scale) 相對身體中心）
    ball_x = 910 + 100*1.1
    ball_y = 280 - 20
    e.append(wiffle(ball_x, ball_y, 18))

    e.append(speech_bubble(910, 140, "Nice words,\nOwen!", color="#E0F8E4", text_color="#228B22", width=130, height=60))

    return svg(W, H, "".join(e), bg=BG["p8"])


def scene_p9():
    """p9：開心對打，球飛、POP、三人笑，卡片小小探頭（隨身攜帶）。"""
    e = []
    # 球場地面
    e.append(f'<rect x="0" y="420" width="1188" height="140" fill="#D4F0E8"/>')

    # 球網
    e.append(pickleball_net(594, 480, net_height=85))

    # 彩紙條（慶祝）
    import random
    random.seed(9)
    cols = ["#F6C445", "#7BC47F", "#6FA8DC", "#F49AB5", "#E4574C"]
    for i in range(20):
        x, y = random.randint(40, 1148), random.randint(30, 280)
        c = cols[i % 5]
        e.append(f'<rect x="{x}" y="{y}" width="10" height="16" rx="3" fill="{c}" transform="rotate({random.randint(-40,40)} {x} {y})"/>')

    # Owen 中央，開心表情，揮拍
    e.append(boy(pose="swing", expr="big", cx=594, cy=240, scale=1.2))
    e.append(paddle(594+88*1.2, 240+50*1.2, angle=60, scale=1.0))

    # Anne 左側，開心微笑
    e.append(ann(cx=200, cy=340, scale=1.0, expr="smile"))

    # Daddy 右側，開心微笑（feet_y ≈ 300 + 216 = 516）
    e.append(daddy(cx=988, cy=300, scale=1.0, pose="stand"))

    # 球飛虛線 + POP
    e.append(f'<path d="M 470 220 Q 594 160 718 220" fill="none" stroke="#FFD34D" stroke-width="4" stroke-dasharray="8 12" stroke-linecap="round"/>')
    e.append(wiffle(594, 180, 20))
    e.append(f'<circle cx="700" cy="160" r="28" fill="none" stroke="#FF6B6B" stroke-width="3"/>')
    e.append(svgtext(700, 170, "POP", size=32, fill="#FF6B6B", weight="bold"))

    # 三張小卡片在 Owen 腰間（隨身攜帶）
    e.append(magic_card(560, 380, "PLEASE", scale=0.6, glow=False, hiding=False))
    e.append(magic_card(594, 395, "THANK YOU", scale=0.6, glow=False, hiding=False))
    e.append(magic_card(628, 380, "SORRY", scale=0.6, glow=False, hiding=False))

    return svg(W, H, "".join(e), bg=BG["p9"])


def scene_p10():
    """p10：英雄頁。Owen 披紅披風 + hips 姿勢 + 垂手位置握拍 + 三張 glow 卡片繞身 ≥220 + 滿天星。"""
    e = []
    # 場地
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="110" fill="#FFD34D"/>')

    # 滿天星星
    for (x, y, r) in [(160, 100, 20), (1020, 120, 24), (120, 380, 16), (1060, 380, 16), (330, 50, 12), (860, 60, 14)]:
        e.append(star(x, y, r, fill=STAR_Y))
    e.append(sparkle(240, 240, 12)); e.append(sparkle(950, 240, 12))

    # Owen 英雄姿勢：hips + cape + proud 表情
    # Owen 頭中心在 (594, 180+34*1.3) ≈ (594, 224)，頭半徑 ≈ 73
    e.append(boy(pose="hips", expr="proud", cx=594, cy=180, scale=1.3, cape=True))

    # 球拍握在垂手位置（hips 姿勢時左手在約 (cx-44*s, cy+150*s)）
    # stand/hips 手在 (cx±48*s, cy+136*s)
    # 握把端在 (594-48*1.3, 180+136*1.3) ≈ (538, 357)
    # angle=10 讓拍面朝左下外側，不碰身體
    e.append(paddle(538, 357, angle=-35, scale=1.0))

    # 三張發光卡片繞身飛舞（軌道半徑 ≥220）
    # 位置：上左、下中、上右
    cards_pos = [
        (594 - 220*math.cos(math.radians(30)), 180 - 220*math.sin(math.radians(30)), "PLEASE"),
        (330, 330, "THANK YOU"),
        (594 + 220*math.cos(math.radians(30)), 180 - 220*math.sin(math.radians(30)), "SORRY"),
    ]
    for card_x, card_y, word in cards_pos:
        e.append(magic_card(card_x, card_y, word, scale=0.9, glow=True, hiding=False))

    return svg(W, H, "".join(e), bg=BG["p10"])


# ============ PAGE TEXTS ============
PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I play <b>pickleball</b> with Daddy!'),
    ("p2", scene_p2, 'We hit the ball.<br/><b>Pop, pop, pop!</b><br/>Pickleball is fun!'),
    ("p3", scene_p3, 'I want the ball <b>NOW</b>!<br/>I want to hit it again!'),
    ("p4", scene_p4, 'I grab. I yell.<br/>My hands feel fast, my mouth feels loud.<br/>My <b>magic</b> words hide away!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I find my magic words!'),
    ("p6", scene_p6, 'Want the ball? &ldquo;<b>Please!</b>&rdquo;<br/>Get the ball? &ldquo;<b>Thank you!</b>&rdquo;<br/>Bump a friend? &ldquo;<b>Sorry!</b>&rdquo;'),
    ("p7", scene_p7, 'Magic words make friends smile.<br/>Everyone loves to play with me!'),
    ("p8", scene_p8, '&ldquo;<b>Please, Daddy!</b>&rdquo; He gives the ball.<br/>&ldquo;<b>Thank you!</b>&rdquo;<br/>Daddy smiles. &ldquo;Nice words, <b>Owen</b>!&rdquo;'),
    ("p9", scene_p9, 'Pop, pop! Great game!<br/><b>Magic words</b> all day.<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, '<b>Please. Thank you. Sorry.</b><br/>My <b>magic words!</b><br/>I practice every day!'),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("大人先示範魔法詞", "對 Owen 說話時自己先用 please / thank you / sorry——魔法詞是模仿來的，不是要求來的。"),
    ("抓到就放大稱讚", "他自發說出任何一個魔法詞的瞬間，立刻具體稱讚（「你剛剛說了 thank you！」），比事後糾正一百次有效。"),
    ("三個詞對三個時刻", "要東西 = Please、被幫助 = Thank you、碰撞 = Sorry。提醒時只說 &ldquo;Magic words!&rdquo; 讓他自己選對的那張卡。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

BOOK = {
    "slug": "magic-words",
    "order": 9,
    "title_pre": "My ", "title_hi": "Magic", "title_post": " Words!",
    "title_zh": "我的魔法詞語",
    "subtitle": "Owen's pickleball story",
    "tagline_zh": "Owen 的匹克球故事",
    "chips": ["Social Story", "Pickleball", "12 pages"],
    "pdf_name": "My_Magic_Words.pdf",
    "bg": BG,
    "pages": PAGES,
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Please → Thank you → Sorry!</b>&nbsp;"
                 "搭配 &ldquo;Magic words!&rdquo; 提醒。大人先示範，抓到自發說出時立刻大力稱讚。"),
    "cover": scene_cover,
}
