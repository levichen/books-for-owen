# -*- coding: utf-8 -*-
"""Book 11: Volume Down! — Owen 學會控制音量與身體力度的社會故事。
核心視覺：音量表 1-2-3（三格量表＋指針）
"""
from parts import *
from book_common import svg, svgtext, TXT, W, H
import math

# soft page palettes
BG = {
    "cover": "#FFE9C9", "p1": "#FFF3D6", "p2": "#FFF3D6", "p3": "#FFE3C2",
    "p4": "#FFD9CF", "p5": "#3A2652", "p6": "#D7E9F8", "p7": "#E8F0E6",
    "p8": "#FFF0C9", "p9": "#FFE2EC", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

# ============================================================
# CORE ASSET: VOLUME METER
# ============================================================

def volume_meter(cx, cy, scale, level=2, glow=False, compact=False):
    """音量表：1-2-3 三格量表＋指針。
    level: 1=悄悄話 | 2=室內聲 | 3=戶外聲（指針指向該格）
    glow: True 時外圈 2 層半透明金圓（發光）
    compact: True 時用更小的尺寸（寬 ~90）；False 時標準尺寸（寬 ~180）
    """
    m = []

    # 光暈（如果 glow=True）- 金色半透明疊圈，貼住底板邊緣
    if glow:
        # compact=True: board_w=90, 光暈 r~120/90
        # compact=False: board_w=180, 光暈 r~140/110
        halo_r1 = 140 if not compact else 120
        halo_r2 = 110 if not compact else 90
        m.append(f'<g opacity="0.30"><circle cx="0" cy="0" r="{halo_r1}" fill="#FFE9A8"/></g>')
        m.append(f'<g opacity="0.18"><circle cx="0" cy="0" r="{halo_r2}" fill="#FFE9A8"/></g>')

    # 底板：圓角矩形背景（灰棕色）- compact 版寬 ~90，標準版寬 ~180
    if compact:
        board_x, board_w = -45, 90
        grid_positions = [-30, 0, 30]
    else:
        board_x, board_w = -90, 180
        grid_positions = [-65, 0, 65]

    m.append(f'<rect x="{board_x}" y="-45" width="{board_w}" height="90" rx="20" fill="#E8DCD0" stroke="#C9B9A8" stroke-width="4"/>')

    # 三格量表（橫排）
    grid_labels = ['1', '2', '3']

    for i, (gx, label) in enumerate(zip(grid_positions, grid_labels)):
        # 格子框（淡色，選中時亮色）
        is_selected = (level == i + 1)
        grid_fill = "#FFE8D0" if is_selected else "#DCCFD8"
        grid_half = 22 if compact else 30
        m.append(f'<rect x="{gx-grid_half}" y="-30" width="{grid_half*2}" height="60" rx="8" fill="{grid_fill}" stroke="#A8947F" stroke-width="2"/>')

        # icon 與文字（各格不同）
        if i == 0:  # 1 = 悄悄話（小老鼠）
            # 小老鼠簡筆：圓頭 + 耳朵 + 小尾巴
            m.append(f'<circle cx="{gx}" cy="-8" r="8" fill="#999999" stroke="#555555" stroke-width="1.5"/>')  # 頭
            m.append(f'<circle cx="{gx-10}" cy="-20" r="5" fill="#999999"/>')  # 左耳
            m.append(f'<circle cx="{gx+10}" cy="-20" r="5" fill="#999999"/>')  # 右耳
            m.append(f'<path d="M {gx+8} {-8} Q {gx+30} {0} {gx+20} {12}" fill="none" stroke="#999999" stroke-width="2" stroke-linecap="round"/>')  # 尾巴
        elif i == 1:  # 2 = 室內聲（小房子）
            # 小房子：方形屋身 + 三角形屋頂 + 小門
            m.append(f'<rect x="{gx-12}" y="{0}" width="24" height="16" fill="#D4A574" stroke="#A8754D" stroke-width="1.5"/>')  # 屋身
            m.append(f'<polygon points="{gx-14},{0} {gx},{-12} {gx+14},{0}" fill="#C74A2E" stroke="#9E391F" stroke-width="1.5"/>')  # 屋頂
            m.append(f'<rect x="{gx-4}" y="{4}" width="8" height="8" fill="#8B6D47"/>')  # 小門
        else:  # 3 = 戶外聲（太陽）
            # 太陽簡筆：黃圓 + 短射線
            m.append(f'<circle cx="{gx}" cy="-8" r="10" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="2"/>')  # 太陽
            for j in range(4):  # 四條射線
                angle = j * 90
                a = math.radians(angle)
                x1, y1 = gx + 16*math.cos(a), -8 + 16*math.sin(a)
                x2, y2 = gx + 22*math.cos(a), -8 + 22*math.sin(a)
                m.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{STAR_DK}" stroke-width="2" stroke-linecap="round"/>')

        # 數字（固定字級，外層 scale 會放大）
        m.append(svgtext(gx, 28, label, size=18, fill="#4A3B32", weight="bold"))

    # 指針（粗箭頭指向 level 格）
    needle_x = grid_positions[level - 1]
    # 箭頭：從下往上指，尖端在格子上方
    m.append(f'<path d="M {needle_x} 48 L {needle_x-11} 72 L {needle_x+11} 72 Z" fill="#E8574C" stroke="#C74338" stroke-width="2"/>')

    inner = "".join(m)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


# ============================================================
# SCENE FUNCTIONS
# ============================================================

def scene_cover():
    """封面：Owen 拿著積木＋音量表＋客廳暖色背景"""
    e = []
    # 背景：暖米色
    e.append(f'<rect x="0" y="0" width="1188" height="620" fill="#FFE9C9"/>')

    # 地面：棕黃色
    e.append(f'<ellipse cx="594" cy="580" rx="560" ry="100" fill="#FFD9A0"/>')

    # 星星點綴
    for (x, y, r) in [(180, 120, 16), (1000, 150, 20), (320, 380, 12), (900, 450, 14)]:
        e.append(star(x, y, r))

    # Owen 白 T 拿著積木 (feet_y = cy+228*scale)
    # cy=240, scale=1.3 → feet_y = 240+228*1.3 = 536.4
    e.append(boy(pose="stand", expr="big", cx=420, cy=240, scale=1.3))

    # 積木塔（彩色方塊，Owen 身旁，feet_y 與 Owen 對齊）
    # Owen 右側畫積木
    block_colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3"]
    blocks = [
        (550, 420, 50, 50, 0),  # 紅底層
        (550, 350, 50, 50, 1),  # 綠中層
        (550, 280, 50, 50, 2),  # 黃上層
        (620, 420, 50, 50, 3),  # 藍底層
        (620, 350, 50, 50, 0),  # 紅中層
    ]
    for bx, by, bw, bh, color_idx in blocks:
        e.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="6" fill="{block_colors[color_idx]}" stroke="#333333" stroke-width="2"/>')

    # 音量表在前景（標準寬 ~180）
    e.append(volume_meter(cx=850, cy=400, scale=1.0, level=2, glow=False, compact=False))

    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """p1: Owen 白 T 拿著積木開心玩，客廳暖色（This is me, Owen! I love to play and laugh!）"""
    e = []
    # 背景：暖色客廳
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p1"]}"/>')

    # 地毯：大橢圓，棕色
    e.append(f'<ellipse cx="594" cy="420" rx="450" ry="80" fill="#E8C9A0"/>')

    # 沙發：圓角矩形 + 靠墊
    e.append(f'<rect x="100" y="350" width="300" height="120" rx="20" fill="#D4A574" stroke="#A8754D" stroke-width="4"/>')
    e.append(f'<ellipse cx="120" cy="350" rx="25" ry="35" fill="#E8B896"/>')  # 左靠墊
    e.append(f'<ellipse cx="380" cy="350" rx="25" ry="35" fill="#E8B896"/>')  # 右靠墊

    # Owen 白 T，拿著積木開心玩 (feet_y = cy+228*scale)
    # cy=250, scale=1.0 → feet_y = 478
    e.append(boy(pose="stand", expr="big", cx=650, cy=250, scale=1.0))

    # 積木塔（彩色小塔，Owen 腳邊）
    block_colors = ["#FF6B6B", "#4ECDC4", "#FFE66D"]
    for i, color in enumerate(block_colors):
        e.append(f'<rect x="{700}" y="{420 - i*50}" width="50" height="50" rx="6" fill="{color}" stroke="#333333" stroke-width="2"/>')

    # 星星＆音符
    e.append(star(800, 150, 16))
    e.append(sparkle(900, 200, 12))

    return svg(W, H, "".join(e), bg=None)


def scene_p2():
    """p2: 客廳全景：Owen 玩積木，April 看書，Daddy 靠著閉眼休息（Inside, we play at home. Mommy reads. Daddy rests.）"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p2"]}"/>')

    # 地毯
    e.append(f'<ellipse cx="594" cy="420" rx="450" ry="80" fill="#E8C9A0"/>')

    # 沙發
    e.append(f'<rect x="80" y="320" width="350" height="140" rx="20" fill="#D4A574" stroke="#A8754D" stroke-width="4"/>')
    e.append(f'<ellipse cx="100" cy="320" rx="30" ry="40" fill="#E8B896"/>')
    e.append(f'<ellipse cx="410" cy="320" rx="30" ry="40" fill="#E8B896"/>')

    # Daddy 靠著沙發睡覺（pose="stand", scale 縮小，頭上 Zzz）
    # feet_y = cy+216*scale，沙發底部約 460，所以 cy ≈ 180, scale=0.9 → feet_y ≈ 385
    e.append(daddy(cx=180, cy=280, scale=1.0, pose="stand"))
    # Daddy 頭上 Zzz（睡意符號）
    e.append(svgtext(220, 80, "Z", size=36, fill="#FFB6C1", weight="bold"))
    e.append(svgtext(260, 60, "z", size=28, fill="#FFB6C1", weight="bold"))

    # Owen 玩積木 (feet_y = cy+228*scale)
    # cy=280, scale=1.0 → feet_y = 508
    e.append(boy(pose="stand", expr="smile", cx=700, cy=280, scale=1.0))

    # 積木塔（Owen 身旁，較高）
    block_colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3", "#FFB6C1"]
    for i, color in enumerate(block_colors):
        e.append(f'<rect x="{750}" y="{450 - i*50}" width="50" height="50" rx="6" fill="{color}" stroke="#333333" stroke-width="2"/>')

    # April 坐著看書（身體縮小，在右側）
    # feet_y = cy+212*scale，沙發邊約 450
    e.append(april(cx=980, cy=300, scale=1.0, pose="stand"))
    # April 手上的書（簡筆：攤開的矩形）
    e.append(f'<path d="M 960 280 L 950 320 L 1010 320 L 1000 280 Z" fill="#D4A574" stroke="#A8754D" stroke-width="2"/>')
    e.append(f'<path d="M 980 280 L 980 320" stroke="#A8754D" stroke-width="2"/>')

    return svg(W, H, "".join(e), bg=None)


def scene_p3():
    """p3: Owen 特寫（big 表情），積木塔越疊越高，星星與音符變多變大（The game gets SO fun! More fun, more BIG!）"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p3"]}"/>')

    # 地毯
    e.append(f'<ellipse cx="594" cy="440" rx="450" ry="80" fill="#E8C9A0"/>')

    # Owen 特寫（boy_bust）
    e.append(boy_bust(expr="big", cx=400, cy=280, scale=1.3))

    # 積木塔（身旁，較高較寬）
    block_colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3", "#FFB6C1", "#FF9999"]
    for i, color in enumerate(block_colors):
        base_x = 700
        if i >= 3:  # 上層偏移
            base_x = 680
        e.append(f'<rect x="{base_x}" y="{450 - i*50}" width="50" height="50" rx="6" fill="{color}" stroke="#333333" stroke-width="2"/>')

    # 星星與音符（變多變大）
    for (x, y, r) in [(250, 150, 22), (950, 100, 26), (180, 400, 18), (1050, 350, 20)]:
        e.append(star(x, y, r))

    # 音符
    for (x, y, r) in [(320, 200, 14), (1000, 250, 12)]:
        e.append(sparkle(x, y, r))

    return svg(W, H, "".join(e), bg=None)


def scene_p4():
    """p4: 衝動頁核心——Owen 大叫（嘴邊三層放大聲波弧）+手臂揮舞殘影+積木塔倒（CRASH 字效）
    +April 頭側手掌圖示摀耳+Daddy 頭上驚醒符號（！）
    (My voice grows big, big, BIG! My body feels buzzy! CRASH! Too loud!)"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p4"]}"/>')

    # 地毯
    e.append(f'<ellipse cx="594" cy="440" rx="450" ry="80" fill="#E8C9A0"/>')

    # 沙發
    e.append(f'<rect x="80" y="320" width="350" height="140" rx="20" fill="#D4A574" stroke="#A8754D" stroke-width="4"/>')

    # Daddy 驚醒（在沙發後面，下半身被沙發背擋住）
    # feet_y = cy+216*scale，沙發底部 460，所以 cy ≈ 260 讓腳在 476，被擋住
    e.append(daddy(cx=180, cy=260, scale=1.0, pose="stand"))
    # 驚醒符號（！在頭上）
    e.append(svgtext(220, 90, "!", size=48, fill="#E8574C", weight="bold"))

    # April 摀耳朵（兩側膚色橢圓手掌）
    e.append(april(cx=980, cy=300, scale=1.0, pose="stand"))
    # 摀耳朵：頭兩側膚色橢圓（手掌貼住耳朵）
    e.append(f'<ellipse cx="938" cy="322" rx="15" ry="20" fill="{SKIN}" stroke="#A8754D" stroke-width="2"/>')  # 左手掌貼耳
    e.append(f'<ellipse cx="1022" cy="322" rx="15" ry="20" fill="{SKIN}" stroke="#A8754D" stroke-width="2"/>')  # 右手掌貼耳
    # 頭頂上方不悅符號（小漩渦線）
    e.append(f'<path d="M 965 262 Q 980 248 995 262" fill="none" stroke="#D8574C" stroke-width="3" stroke-linecap="round"/>')

    # Owen 大叫（boy_bust big 表情，嘴邊三層聲波弧）
    e.append(boy_bust(expr="big", cx=400, cy=240, scale=1.2))

    # 嘴邊聲波（三層向右開口的弧，從臉右緣外側放大，不碰臉）
    for i in range(3):
        radius = 30 + i * 26
        x0, y0 = 478, 264
        e.append(f'<path d="M {x0 + radius*0.25} {y0 - radius} Q {x0 + radius} {y0} {x0 + radius*0.25} {y0 + radius}" fill="none" stroke="#E8574C" stroke-width="6" stroke-linecap="round" opacity="{1 - i*0.28}"/>')

    # 手臂揮舞殘影（從肩膀向右下方向，避開頭部）
    for j in range(3):
        e.append(f'<path d="M {430 + j*20} {240 + j*15} L {480 + j*30} {290 + j*20}" fill="none" stroke="#E8574C" stroke-width="5" stroke-linecap="round" opacity="{0.8 - j*0.25}"/>')

    # 積木塔倒塌（方塊散落）
    block_colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3"]
    for i, color in enumerate(block_colors):
        scatter_x = 650 + i * 80 + (-30 + i*15)
        scatter_y = 380 + i * 40
        e.append(f'<rect x="{scatter_x}" y="{scatter_y}" width="50" height="50" rx="6" fill="{color}" stroke="#333333" stroke-width="2" transform="rotate({i*15} {scatter_x+25} {scatter_y+25})"/>')

    # CRASH 字效
    e.append(svgtext(650, 320, "CRASH!", size=56, fill="#E8574C", weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p5():
    """p5: 紫色星空＋Owen press 表情＋浮著發光的音量表＋指針旋轉箭頭（3→2）
    (STOP! I use my superpower… I turn my volume down!)"""
    e = []
    # 背景：紫色星空
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p5"]}"/>')

    # 星星點綴（淡色）
    for (x, y, r) in [(150, 120, 16), (1030, 130, 20), (200, 420, 14), (1000, 430, 16)]:
        e.append(star(x, y, r, fill="#C5A6FF", stroke="#9B7FD8"))

    # sparkle
    e.append(sparkle(320, 90, 12))
    e.append(sparkle(860, 80, 12))

    # Owen press 表情（小尺寸，左下）
    e.append(boy(pose="stand", expr="press", cx=320, cy=340, scale=1.0))

    # 浮著的音量表（深紫背景上半透明光暈會變泥棕色——改用 sparkle 表達發光）
    e.append(volume_meter(cx=750, cy=200, scale=1.0, level=2, glow=False, compact=False))
    e.append(sparkle(640, 120, 14)); e.append(sparkle(870, 130, 12))
    e.append(sparkle(650, 280, 10)); e.append(sparkle(866, 262, 12))

    # 旋轉箭頭（3→2 的指針轉動）
    # 箭頭從右下指向左下（代表從 level 3 轉向 level 2）
    arrow_path = f'<path d="M 850 250 Q 800 240 750 260" fill="none" stroke="{STAR_Y}" stroke-width="5" stroke-linecap="round"/>'
    arrow_head = f'<polygon points="750,260 740,240 760,245" fill="{STAR_Y}"/>'
    e.append(arrow_path)
    e.append(arrow_head)

    return svg(W, H, "".join(e), bg=None)


def scene_p6():
    """p6: 三步腳本三格——①耳朵旁聲波＋問號 ②音量表特寫（2 發光） ③小聲說話＋輕拿積木
    (I check my volume. Three is outside. Two is inside. I pick two!)"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p6"]}"/>')

    # 地毯
    e.append(f'<ellipse cx="594" cy="450" rx="450" ry="80" fill="#E8C9A0"/>')

    # 三步腳本三格（橫排）

    # ① 左格：耳朵旁聲波＋問號（聽自己）
    e.append(f'<rect x="80" y="180" width="280" height="280" rx="16" fill="#FFFFFF" stroke="#B8D8E8" stroke-width="4"/>')
    # Owen 小尺寸，listening pose（stand）
    e.append(boy(pose="stand", expr="think", cx=180, cy=310, scale=0.8))
    # 耳朵旁聲波
    for i in range(2):
        radius = 40 + i * 25
        e.append(f'<path d="M {120} {280} Q {120 - radius*0.4} {280 - radius*0.6} {120} {280 - radius}" fill="none" stroke="#FFB6C1" stroke-width="3" stroke-linecap="round"/>')
    # 問號
    e.append(svgtext(240, 250, "?", size=48, fill="#4A78A8", weight="bold"))

    # ② 中格：音量表特寫（2 發光，compact 版）
    e.append(f'<rect x="414" y="180" width="280" height="280" rx="16" fill="#FFFFFF" stroke="#B8D8E8" stroke-width="4"/>')
    e.append(volume_meter(cx=554, cy=320, scale=1.0, level=2, glow=True, compact=True))

    # ③ 右格：小聲說話＋輕拿積木
    e.append(f'<rect x="748" y="180" width="280" height="280" rx="16" fill="#FFFFFF" stroke="#B8D8E8" stroke-width="4"/>')
    # Owen 小尺寸，輕聲（small pose）
    e.append(boy(pose="stand", expr="smile", cx=848, cy=310, scale=0.8))
    # 語音泡泡（小尺寸，旁邊）
    e.append(f'<ellipse cx="920" cy="240" rx="50" ry="35" fill="#FFFFFF" stroke="#8A5A3C" stroke-width="2"/>')
    e.append(svgtext(920, 250, "2", size=24, fill="#D97706", weight="bold"))
    # 積木（小尺寸，手邊）
    e.append(f'<rect x="870" y="330" width="30" height="30" rx="4" fill="#FF6B6B" stroke="#333333" stroke-width="1.5"/>')

    return svg(W, H, "".join(e), bg=None)


def scene_p7():
    """p7: 觀點頁左右對比——左側灰調（April 摀耳）／右側亮色（April 微笑看書、Daddy 睡得香、Owen 玩積木）
    (Big noise hurts ears. Small voice keeps play going. Everyone plays happy!)"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p7"]}"/>')

    # 中央分割線（虛線）
    e.append(f'<line x1="594" y1="0" x2="594" y2="560" stroke="#999999" stroke-width="3" stroke-dasharray="10 8" opacity="0.5"/>')

    # 左側：灰調（大聲不好）
    # 背景變暗
    e.append(f'<rect x="0" y="0" width="594" height="560" fill="#D0C9C0" fill-opacity="0.4"/>')
    # 地毯
    e.append(f'<ellipse cx="297" cy="440" rx="200" ry="60" fill="#D4C0B0"/>')

    # 小尺寸 Owen（big 表情）大叫，聲波直逼 April
    e.append(boy(pose="stand", expr="big", cx=180, cy=340, scale=0.85))
    # 嘴邊聲波（三層，從 Owen 嘴邊向 April 放大）
    for i in range(3):
        radius = 22 + i * 20
        x0, y0 = 236, 369
        e.append(f'<path d="M {x0 + radius*0.25} {y0 - radius} Q {x0 + radius} {y0} {x0 + radius*0.25} {y0 + radius}" fill="none" stroke="#E8574C" stroke-width="5" stroke-linecap="round" opacity="{1 - i*0.28}"/>')

    # April 摀耳朵，皺眉不悅
    e.append(april(cx=360, cy=300, scale=1.0, pose="stand"))
    # 摀耳朵：膚色橢圓手掌（貼住耳朵）
    e.append(f'<ellipse cx="318" cy="322" rx="15" ry="20" fill="{SKIN}" stroke="#A8754D" stroke-width="2"/>')  # 左手掌貼耳
    e.append(f'<ellipse cx="402" cy="322" rx="15" ry="20" fill="{SKIN}" stroke="#A8754D" stroke-width="2"/>')  # 右手掌貼耳
    # 頭頂上方不悅線
    e.append(f'<path d="M 345 262 Q 360 248 375 262" fill="none" stroke="#D8574C" stroke-width="3" stroke-linecap="round"/>')

    # 右側：亮色（小聲很好）
    # 背景亮色
    e.append(f'<rect x="594" y="0" width="594" height="560" fill="#E8F0E6" fill-opacity="0.6"/>')
    # 地毯
    e.append(f'<ellipse cx="891" cy="440" rx="200" ry="60" fill="#D4E0C0"/>')
    # Owen 玩積木（高興）
    e.append(boy(pose="stand", expr="big", cx=750, cy=320, scale=0.9))
    # 小積木塔（在 Owen 身旁地板上，不是疊在身上）
    for i in range(3):
        e.append(f'<rect x="820" y="{420 - i*40}" width="40" height="40" rx="4" fill="#FF6B6B" stroke="#333333" stroke-width="1.5"/>')
    # April 微笑看書（放鬆）
    e.append(april(cx=1030, cy=300, scale=0.9, pose="stand"))
    # 放鬆笑容（已包含在 pose="stand" 的 smile expr）
    # Daddy 睡得香
    e.append(daddy(cx=891, cy=240, scale=0.9, pose="stand"))
    # Daddy 頭上 Zzz
    e.append(svgtext(920, 100, "Z", size=28, fill="#FFB6C1", weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p8():
    """p8: April 蹲下比讚，語音泡泡 "Nice inside voice, Owen!"；Owen 疊好高高的完好積木塔
    (Mommy April smiles. "Nice inside voice, Owen!" My tower is TALL!)"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p8"]}"/>')

    # 地毯
    e.append(f'<ellipse cx="594" cy="440" rx="450" ry="80" fill="#E8C9A0"/>')

    # Owen 疊好的積木塔（右側，高而完好）
    block_colors = ["#FF6B6B", "#4ECDC4", "#FFE66D", "#95E1D3", "#FFB6C1", "#FF9999", "#C5A6FF"]
    for i, color in enumerate(block_colors):
        e.append(f'<rect x="950" y="{450 - i*50}" width="50" height="50" rx="6" fill="{color}" stroke="#333333" stroke-width="2"/>')

    # Owen 開心站立，看著自己的塔
    e.append(boy(pose="stand", expr="proud", cx=750, cy=320, scale=1.0))

    # April 蹲下（scale 縮小，cy 提高到低位）
    e.append(april(cx=280, cy=380, scale=0.9, pose="stand"))
    # April 比讚（拇指向上圖示）
    e.append(f'<circle cx="240" cy="320" r="15" fill="{SKIN}" stroke="#A8754D" stroke-width="2"/>')  # 拇指
    e.append(f'<path d="M 240 320 L 240 280" stroke="{SKIN}" stroke-width="12" stroke-linecap="round"/>')  # 拇指豎起

    # 語音泡泡："Nice inside voice, Owen!"
    e.append(f'<path d="M 350 240 Q 350 180 450 180 L 550 180 Q 580 180 580 220 Q 580 260 550 260 L 430 260 L 380 300 L 420 260 Q 350 260 350 240 Z" fill="#FFFFFF" stroke="#8A5A3C" stroke-width="3"/>')
    e.append(svgtext(465, 225, "Nice inside voice,", size=20, fill="#000000", weight="normal"))
    e.append(svgtext(465, 250, "Owen!", size=20, fill="#000000", weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p9():
    """p9: Owen 開心玩（音符變小顆但笑容大），旁邊小音量表指著 2 發光
    (Small voice, big fun! We play more and more. I feel GREAT!)"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p9"]}"/>')

    # 地毯
    e.append(f'<ellipse cx="594" cy="440" rx="450" ry="80" fill="#E8C9A0"/>')

    # Owen 開心玩（big 表情，騎馬姿勢或 hips）
    e.append(boy(pose="hips", expr="big", cx=450, cy=280, scale=1.1))

    # 小顆音符（快樂）
    for (x, y, r) in [(320, 200, 10), (380, 150, 8), (520, 190, 9)]:
        e.append(sparkle(x, y, r))

    # 小音量表（旁邊，發光，指著 2，compact 版）
    e.append(volume_meter(cx=800, cy=320, scale=0.8, level=2, glow=True, compact=True))

    # 星星
    e.append(star(150, 120, 16))
    e.append(star(1050, 180, 18))

    return svg(W, H, "".join(e), bg=None)


def scene_p10():
    """p10: 英雄頁——Owen 披紅披風叉腰，胸前掛著發光的音量表（指針在 2），滿天星
    (Check my volume. Pick two. Volume down! I practice every day!)"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p10"]}"/>')

    # 地面：橢圓光暈
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="110" fill="#FFDD7E"/>')

    # 滿天星
    for (x, y, r) in [(160, 120, 20), (1020, 120, 24), (120, 380, 16), (1060, 380, 16), (330, 70, 12), (860, 70, 14)]:
        e.append(star(x, y, r))

    # sparkle
    e.append(sparkle(260, 260, 12))
    e.append(sparkle(930, 260, 12))

    # Owen 英雄姿勢（hips 叉腰）披紅披風
    e.append(boy(pose="hips", expr="proud", cx=594, cy=200, scale=1.25, cape=True))

    # 胸前掛著的發光音量表（縮小，位置在胸口 cy+60*s 到 cy+110*s）
    # cy=200, scale=1.25: 胸口位置約 200+75 到 200+138，取中點 ~275
    e.append(volume_meter(cx=594, cy=332, scale=0.55, level=2, glow=True, compact=True))

    return svg(W, H, "".join(e), bg=None)


# ============================================================
# PAGE DEFINITIONS
# ============================================================

PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I love to play and laugh!'),
    ("p2", scene_p2, 'Inside, we play at home.<br/>Mommy reads. Daddy rests.'),
    ("p3", scene_p3, 'The game gets SO fun!<br/>More fun, more <b>BIG</b>!'),
    ("p4", scene_p4, 'My voice grows big, big, <b>BIG</b>!<br/>My body feels <b>buzzy</b>!<br/><b>CRASH!</b> Too loud!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I turn my <b>volume</b> down!'),
    ("p6", scene_p6, 'I check my volume.<br/>Three is outside. Two is inside.<br/>I pick <b>two</b>!'),
    ("p7", scene_p7, 'Big noise hurts ears.<br/>Small voice keeps play going.<br/>Everyone plays happy!'),
    ("p8", scene_p8, 'Mommy April smiles.<br/>&ldquo;Nice inside voice, <b>Owen</b>!&rdquo;<br/>My tower is TALL!'),
    ("p9", scene_p9, 'Small voice, big fun!<br/>We play more and more.<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Check my volume. Pick two.<br/><b>Volume down!</b><br/>I practice every day!'),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3–4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("音量表要實體化", "印一張 1-2-3 音量表貼在客廳（跟書裡同款），提醒時只要指著表說 &ldquo;Volume?&rdquo;，讓他自己說出「2」——自己說出來的才算自我調節。"),
    ("3 不是壞的", "戶外、操場就是 3 的地方——這本書教的是「選對等級」不是「永遠小聲」。在公園可以大聲提醒他「這裡可以 3！」，等級才有意義。"),
    ("與 Freeze 的分工", "情況失控要立刻停用 &ldquo;Freeze!&rdquo;（外部開關）；還在可控範圍想讓他自己降音量用 &ldquo;Volume?&rdquo;（自我監控）。"),
    ("當他主動說 &ldquo;My voice grows big&rdquo;", "= 自我覺察里程碑，大力稱讚。"),
]

BOOK = {
    "slug": "volume-down",
    "order": 11,
    "title_pre": "", "title_hi": "Volume", "title_post": " Down!",
    "title_zh": "音量轉小",
    "subtitle": "Owen's inside voice story",
    "tagline_zh": "Owen 的音量故事",
    "chips": ["Social Story", "Home", "12 pages"],
    "pdf_name": "Volume_Down.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ['volume', 'buzzy'],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的自我調節腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Check my volume &rarr; Pick two &rarr; Volume down!</b>&nbsp;"
                 "當他哪天主動說出 &ldquo;My voice grows big&rdquo;（我察覺到聲音太大了），"
                 "就是最值得大力稱讚的時刻。提醒時只要指著客廳的音量表問「Volume?」，讓他自己說出「2」。"),
    "cover": scene_cover,
}
