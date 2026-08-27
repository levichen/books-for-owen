# -*- coding: utf-8 -*-
"""Book 20: Quiet Cheer! — 課堂情緒激動時大聲叫喊（答對、遊戲贏了、太興奮時瞬間爆音）
安裝「抓住喊聲 → 握拳擠壓 → 無聲歡呼」的尖峰替代腳本。
核心意象：喊聲小怪獸——紅色小聲波怪從喉嚨往上衝；抓住、塞進握緊的拳頭裡、拳頭發光。"""
import math
from parts import *
from book_common import svg, svgtext, TXT, W, H

# soft page palettes
BG = {
    "cover": "#FFF8E8", "p1": "#E8F4FF", "p2": "#FFF3D6", "p3": "#FFE8E8",
    "p4": "#FFE8E8", "p5": "#3D2E5C", "p6": "#FFE9A8", "p7": "#E8F8D8",
    "p8": "#FFF0C9", "p9": "#FFE2EC", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

SHOUT_MONSTER_RED = "#E4574C"
SHOUT_GLOW = "#FFE9A8"

# ================== SHARED COMPONENT: FIST GLOW ==================

def fist_glow(cx, cy, s=1.0):
    """發光拳頭：光暈（#FFE9A8）+ 拳頭本體（膚色）+ 指節 + 拇指。用於 p5/p6②/p10。"""
    f = []
    # 光暈（先畫，在拳頭後面）
    f.append(f'<circle cx="0" cy="0" r="{30*s}" fill="{SHOUT_GLOW}" fill-opacity="0.45"/>')
    f.append(f'<circle cx="0" cy="0" r="{18*s}" fill="{SHOUT_GLOW}" fill-opacity="0.7"/>')

    # 拳頭本體
    f.append(f'<circle cx="0" cy="0" r="{15*s}" fill="{SKIN}" stroke="#E8B48C" stroke-width="2"/>')

    # 指節（三條小弧，等距排在拳面上半）
    for dy in [-6*s, 0, 6*s]:
        f.append(f'<path d="M {-8*s} {dy} q {4*s} {-3*s} {8*s} {-2*s}" fill="none" stroke="#E8B48C" stroke-width="2" stroke-linecap="round"/>')

    # 拇指
    f.append(f'<ellipse cx="{9*s}" cy="{3*s}" rx="{6*s}" ry="{4*s}" fill="{SKIN}" stroke="#E8B48C" stroke-width="1.5"/>')

    return f'<g transform="translate({cx},{cy})">{"".join(f)}</g>'

# ================== SHOUT MONSTER ==================

def shout_monster(cx, cy, scale=1.0, in_fist=False):
    """紅色喊聲小怪獸：圓潤水滴形身體 + 小白眼 + 鋸齒聲波邊緣。
    in_fist=True 時縮小、位置調整為被握在拳頭裡。"""
    m = []
    s = scale if not in_fist else scale * 0.6

    if not in_fist:
        # 身體：左上尖刺 → 圓潤水滴形
        m.append(f'<ellipse cx="0" cy="8" rx="20" ry="26" fill="{SHOUT_MONSTER_RED}"/>')
        m.append(f'<circle cx="0" cy="-14" r="18" fill="{SHOUT_MONSTER_RED}"/>')
        # 鋸齒聲波邊緣（上方）
        for i in range(7):
            x = -18 + i * 6
            y = -32 + (i % 2) * 4
            m.append(f'<polygon points="{x},{y} {x-3},{y-6} {x+3},{y-6}" fill="{SHOUT_MONSTER_RED}"/>')
        # 兩顆小白眼（黑眼珠在中間偏上）
        m.append(f'<circle cx="-8" cy="-6" r="5" fill="#FFFFFF" stroke="{TXT}" stroke-width="1"/>')
        m.append(f'<circle cx="8" cy="-6" r="5" fill="#FFFFFF" stroke="{TXT}" stroke-width="1"/>')
        m.append(f'<circle cx="-8" cy="-6" r="2" fill="{TXT}"/>')
        m.append(f'<circle cx="8" cy="-6" r="2" fill="{TXT}"/>')
        # 驚恐嘴型（上弧，超音速狀態）
        m.append(f'<ellipse cx="0" cy="6" rx="8" ry="6" fill="#FFFFFF"/>')
    else:
        # 縮小版本：被關進拳頭，只露頭
        m.append(f'<ellipse cx="0" cy="0" rx="14" ry="18" fill="{SHOUT_MONSTER_RED}"/>')
        m.append(f'<circle cx="0" cy="-10" r="12" fill="{SHOUT_MONSTER_RED}"/>')
        m.append(f'<circle cx="-5" cy="-4" r="3" fill="#FFFFFF" stroke="{TXT}" stroke-width="0.8"/>')
        m.append(f'<circle cx="5" cy="-4" r="3" fill="#FFFFFF" stroke="{TXT}" stroke-width="0.8"/>')
        m.append(f'<circle cx="-5" cy="-4" r="1.2" fill="{TXT}"/>')
        m.append(f'<circle cx="5" cy="-4" r="1.2" fill="{TXT}"/>')

    return f'<g transform="translate({cx},{cy}) scale({s})">{"".join(m)}</g>'




def silent_cheer_pose(cx, cy, scale=1.0):
    """無聲歡呼的動作視覺：雙拳張開 + 滿手星星 + 大大的 YES 嘴型 + 零聲音符號 + 跳動線。
    返回 SVG group（不含人物本體，配合場景）。"""
    c = []
    s = scale

    # 雙拳張開狀（兩側膚色圓）
    c.append(f'<circle cx="{-30*s}" cy="{-10*s}" r="14*s" fill="{SKIN}" stroke="{SKIN_DK}" stroke-width="1.5"/>')
    c.append(f'<circle cx="{30*s}" cy="{-10*s}" r="14*s" fill="{SKIN}" stroke="{SKIN_DK}" stroke-width="1.5"/>')

    # 每個拳頭邊三顆小星星
    star_offsets = [(-22*s, -28*s), (-22*s, -8*s), (-22*s, 12*s)]
    for ox, oy in star_offsets:
        c.append(f'<polygon points="{star_pts(ox, oy, 5)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="1"/>')

    star_offsets_r = [(22*s, -28*s), (22*s, -8*s), (22*s, 12*s)]
    for ox, oy in star_offsets_r:
        c.append(f'<polygon points="{star_pts(ox, oy, 5)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="1"/>')

    # 大大的 YES 嘴型（下方）
    c.append(f'<path d="M {-8*s} {40*s} A 8 8 0 0 0 {8*s} {40*s} Z" fill="#8C4A3C" stroke="{TXT}" stroke-width="1"/>')
    c.append(svgtext(0, 50*s, "YES!", size=int(24*s), fill=TXT, weight="bold"))

    # 零聲音符號（音符 + 斜線圈）
    c.append(f'<path d="M {-40*s} {-40*s} Q {-35*s} {-50*s} {-30*s} {-48*s} L {-26*s} {-32*s} Q {-32*s} {-22*s} {-38*s} {-28*s} Z" fill="none" stroke="{SHOUT_MONSTER_RED}" stroke-width="2"/>')
    c.append(f'<circle cx="{-32*s}" cy="{-35*s}" r="12*s" fill="none" stroke="{SHOUT_MONSTER_RED}" stroke-width="2"/>')
    c.append(f'<line x1="{-44*s}" y1="{-20*s}" x2="{-20*s}" y2="{-50*s}" stroke="{SHOUT_MONSTER_RED}" stroke-width="2"/>')

    # 原地跳動線（腳下）
    c.append(f'<path d="M {-8*s} {70*s} Q {-12*s} {74*s} {-8*s} {78*s}" fill="none" stroke="{SHOUT_MONSTER_RED}" stroke-width="2" stroke-linecap="round"/>')
    c.append(f'<path d="M {8*s} {70*s} Q {12*s} {74*s} {8*s} {78*s}" fill="none" stroke="{SHOUT_MONSTER_RED}" stroke-width="2" stroke-linecap="round"/>')

    return f'<g transform="translate({cx},{cy})">{"".join(c)}</g>'


# ================== SCENES ==================

def scene_cover():
    """封面：Owen 精神抖擻走進教室（動作姿勢走步 run），頭上小星星與太陽，喊聲小怪獸從身邊飛過。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="620" fill="{BG["cover"]}"/>')

    # 地板
    e.append(f'<ellipse cx="594" cy="620" rx="560" ry="100" fill="#FFDD7E"/>')

    # Owen 走進教室（run pose）
    e.append(boy(pose="run", expr="big", cx=350, cy=320, scale=1.2))

    # 頭頂星星與太陽
    e.append(sun(150, 100, r=30))
    for (x, y, r) in [(280, 140, 18), (1050, 120, 20)]:
        e.append(star(x, y, r, fill=STAR_Y))

    # 喊聲小怪獸飛過（動線虛線指向方向）
    monster_x, monster_y = 850, 200
    e.append(f'<path d="M 750 280 Q 800 240 {monster_x} {monster_y}" fill="none" stroke="#FFB3BA" stroke-width="2" stroke-dasharray="5 5" opacity="0.7"/>')
    e.append(shout_monster(monster_x, monster_y, scale=1.1))

    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """p1：教室門口，Owen 白 T 精神抖擻站立，雙手握拳舉高（活力滿滿），頭上小星星與太陽。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p1"]}"/>')
    e.append(f'<ellipse cx="594" cy="560" rx="560" ry="80" fill="#D4E8FF"/>')

    # 雲朵裝飾
    e.append(cloud(150, 80, 0.9))
    e.append(cloud(900, 100, 1.1))

    # 星星與太陽
    e.append(sun(1000, 120, r=28))
    for (x, y, r) in [(200, 140, 18), (450, 100, 16)]:
        e.append(star(x, y, r, fill=STAR_Y))

    # Owen 握拳舉高站立
    e.append(boy(pose="handup", expr="big", cx=450, cy=280, scale=1.15))

    return svg(W, H, "".join(e), bg=None)


def scene_p2():
    """p2：教室問答時間，Tr. Mina 在黑板前出題（2+3=?），Owen 與同學們坐課桌，Owen 眼睛發亮舉手。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p2"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#E8D2AC"/>')

    # 黑板
    e.append(f'<rect x="300" y="50" width="550" height="200" rx="10" fill="#C9A26B"/>')
    e.append(f'<rect x="320" y="70" width="510" height="160" rx="6" fill="#3E7C5B"/>')
    e.append(svgtext(595, 150, "2 + 3 = ?", size=80, fill="#FFFFFF", weight="bold"))

    # Tr. Mina 教書（右指）
    e.append(teacher(cx=200, cy=280, scale=1.0, point="right"))

    # 同學們的課桌與半身
    desk_positions = [(550, 350, "owen"), (800, 350, "kid1"), (1000, 350, "kid2")]

    # Owen 眼睛發亮（star 表情）舉手（handup pose）
    e.append(desk(cx=550, cy=350, w=160, scale=0.85))
    e.append(boy_bust(expr="star", cx=550, cy=250, scale=0.8, arms="handup"))

    # 同學 1 和同學 2（思考狀態）
    e.append(desk(cx=800, cy=350, w=160, scale=0.85))
    e.append(kid(variant=0, cx=800, cy=270, scale=0.8, expr="think"))

    e.append(desk(cx=1000, cy=350, w=160, scale=0.85))
    e.append(kid(variant=1, cx=1000, cy=270, scale=0.8, expr="think"))

    return svg(W, H, "".join(e), bg=None)


def scene_p3():
    """p3：Owen 特寫（star 表情），胸口畫快速跳動的心（動態線）。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p3"]}"/>')

    # Owen 大頭特寫（star 表情的 boy_bust）
    e.append(boy_bust(expr="star", cx=400, cy=300, scale=1.4))

    # 快速跳動的心（胸口 T 恤上：bust 衣身 y = cy+(96..150-40)*s = 378..454，避開中央圖案）
    heart_cx, heart_cy = 352, 402
    # 心形
    e.append(f'<path d="M {heart_cx} {heart_cy} c 0 -6 -6 -12 -12 -12 c -6 0 -12 6 -12 12 c 0 12 12 18 12 18 s 12 -6 12 -18 Z" fill="#FF6B6B" stroke="#E8574C" stroke-width="2"/>')
    # 動態線（縮短版，半徑 14-24）
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = math.radians(angle)
        x1 = heart_cx + 14 * math.cos(rad)
        y1 = heart_cy + 14 * math.sin(rad)
        x2 = heart_cx + 24 * math.cos(rad)
        y2 = heart_cy + 24 * math.sin(rad)
        e.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#FF6B6B" stroke-width="2.5" stroke-linecap="round"/>')

    # 星星裝飾
    e.append(star(150, 100, 16, fill=STAR_Y))
    e.append(star(1050, 120, 18, fill=STAR_Y))

    return svg(W, H, "".join(e), bg=None)


def scene_p4():
    """p4：【衝動頁】Owen 站起來張大嘴爆音「YES!!」，紅色喊聲小怪獸從嘴衝出，
    兩位同學摀耳朵（oh 表情），Tr. Mina 食指輕靠嘴溫和提醒。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p4"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#E8D2AC"/>')

    # 前景：Owen 爆音
    # 嘴位置在 cy+34*scale：Owen cy=260, scale=0.95，嘴≈299
    e.append(boy(pose="stand", expr="big", cx=300, cy=260, scale=0.95))

    # 喊聲小怪獸從嘴衝出（動線虛線）
    mouth_x, mouth_y = 300, 260 + 34 * 0.95  # ≈292
    monster_x, monster_y = 380, 140
    e.append(f'<path d="M 320 {mouth_y} Q 350 220 {monster_x} {monster_y}" fill="none" stroke="#FFB3BA" stroke-width="2" stroke-dasharray="4 6" opacity="0.8"/>')
    e.append(shout_monster(monster_x, monster_y, scale=1.0))

    # 音波線（2 圈上半弧：半徑 55*s=52 和 75*s=71）
    s = 0.95
    for r, op in [(52, 0.6), (71, 0.4)]:
        # 上半弧（-60° 到 +60°）
        e.append(f'<path d="M {mouth_x-r*0.866:.0f} {mouth_y-r*0.5:.0f} A {r} {r} 0 0 1 {mouth_x+r*0.866:.0f} {mouth_y-r*0.5:.0f}" fill="none" stroke="{SHOUT_MONSTER_RED}" stroke-width="3" opacity="{op}"/>')

    # YES!! 文字（嘴右上方，離頭≥30px）
    e.append(f'<text x="{mouth_x+40}" y="{mouth_y-60}" font-family="Huninn" font-size="30" fill="{SHOUT_MONSTER_RED}" font-weight="bold" text-anchor="middle">YES!!</text>')

    # 背景：同學摀耳朵（kid() + oh 表情）——kid 身體底=cy+150*s，cy=325 → 底 462 落在地帶內
    kid1_cx, kid1_cy = 650, 325
    e.append(kid(variant=0, cx=kid1_cx, cy=kid1_cy, scale=0.9, expr="oh"))
    e.append(f'<path d="M {kid1_cx-28} {kid1_cy-35} Q {kid1_cx-35} {kid1_cy-28} {kid1_cx-28} {kid1_cy-20}" fill="none" stroke="{SKIN}" stroke-width="12" stroke-linecap="round"/>')

    kid2_cx, kid2_cy = 900, 325
    e.append(kid(variant=2, cx=kid2_cx, cy=kid2_cy, scale=0.9, expr="oh"))
    e.append(f'<path d="M {kid2_cx+28} {kid2_cy-35} Q {kid2_cx+35} {kid2_cy-28} {kid2_cx+28} {kid2_cy-20}" fill="none" stroke="{SKIN}" stroke-width="12" stroke-linecap="round"/>')

    # Tr. Mina 食指輕靠嘴提醒（溫和手勢）
    e.append(teacher(cx=1050, cy=280, scale=1.0, point="right"))
    # 食指輕靠嘴（Tr. Mina 嘴在 cy+42*1.0 = 322，食指在臉旁 x=1070 附近）
    e.append(f'<circle cx="1070" cy="315" r="8" fill="{SKIN}" stroke="{SKIN_DK}" stroke-width="1"/>')
    e.append(f'<path d="M 1080 310 Q 1078 320 1075 325" fill="none" stroke="{SKIN}" stroke-width="8" stroke-linecap="round"/>')

    return svg(W, H, "".join(e), bg=None)


def scene_p5():
    """p5：紫色星空背景，Owen press 表情，雙拳握緊在胸前發光，喊聲小怪獸被關進發光拳頭裡。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p5"]}"/>')

    # 星空點綴
    for (x, y, r) in [(120, 100, 14), (1050, 120, 16), (200, 450, 12), (1000, 430, 14), (350, 80, 10), (850, 70, 12)]:
        e.append(star(x, y, r, fill="#E8D9FF"))
    for (sx, sy, sr) in [(320, 90, 12), (860, 80, 12), (90, 300, 10), (1100, 300, 10), (600, 50, 10)]:
        e.append(sparkle(sx, sy, sr, fill="#E8D9FF"))

    # Owen 半身 press 表情（執行超能力）
    e.append(boy_bust(expr="press", cx=450, cy=300, scale=1.3, arms="desk"))

    # 雙拳握緊發光（boy_bust 手位：cx±56*s, cy+110*s）
    e.append(fist_glow(450 - 56*1.3, 300 + 110*1.3, s=1.2))
    e.append(fist_glow(450 + 56*1.3, 300 + 110*1.3, s=1.2))

    # 紅色小怪獸縮小（0.5）夾在右拳上方（被抓住）
    e.append(shout_monster(450 + 56*1.3 + 8, 300 + 110*1.3 - 40, scale=0.5))

    return svg(W, H, "".join(e), bg=None)


def scene_p6():
    """p6：三步腳本三格：
    ①喉嚨處紅色小怪獸被手抓住（箭頭：從嘴邊抓下來）
    ②雙拳用力擠壓、拳頭發光（squeeze 字效）
    ③無聲歡呼：雙手張開滿手星星 + YES 嘴型 + 零聲音符號 + 跳動小線"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p6"]}"/>')

    # 三個圓形標誌與格子
    grid_positions = [(280, 280), (594, 280), (908, 280)]
    grid_w, grid_h = 240, 280

    for idx, (gx, gy) in enumerate(grid_positions):
        # 格子邊框
        e.append(f'<rect x="{gx-grid_w//2}" y="{gy-grid_h//2}" width="{grid_w}" height="{grid_h}" rx="12" fill="#FFFFFF" stroke="#FFB3D9" stroke-width="3"/>')
        # 圓形標誌
        e.append(f'<circle cx="{gx}" cy="{gy-130}" r="28" fill="#FFE9A8" stroke="#FFE9A8" stroke-width="3"/>')
        e.append(svgtext(gx, gy-120, str(idx+1), size=40, fill=SHOUT_MONSTER_RED, weight="bold"))

        if idx == 0:  # ①抓住小怪獸
            # Owen 頭部特寫（半身）
            e.append(boy_bust(expr="press", cx=gx-40, cy=gy-40, scale=0.9, arms="desk"))
            # 喊聲小怪獸在嘴邊被手抓住
            monster_x, monster_y = gx + 60, gy - 40
            e.append(shout_monster(monster_x, monster_y, scale=0.8))
            # 抓住的手臂（紅線指向）
            e.append(f'<path d="M {gx-20} {gy} L {monster_x-15} {monster_y+15}" fill="none" stroke="#E8574C" stroke-width="3" stroke-linecap="round"/>')
            e.append(f'<path d="M {monster_x-15} {monster_y+15} L {monster_x-12} {monster_y+20} L {monster_x-20} {monster_y+12}" fill="#E8574C"/>')
            # 文字：「Catch the shout!」
            e.append(svgtext(gx, gy+100, "Catch", size=22, fill=TXT, weight="bold"))

        elif idx == 1:  # ②握拳擠壓
            # 雙拳發光（並排，s=1.2）
            e.append(fist_glow(gx-45, gy-20, s=1.2))
            e.append(fist_glow(gx+45, gy-20, s=1.2))
            # SQUEEZE 字效
            e.append(svgtext(gx, gy+50, "SQUEEZE!", size=28, fill=SHOUT_MONSTER_RED, weight="bold"))

        else:  # ③無聲歡呼
            # 無聲歡呼完整動作視覺（半身快樂表情）
            e.append(boy_bust(expr="big", cx=gx-30, cy=gy-30, scale=0.9, arms="handup"))
            # 雙手揮動星星
            for ox, oy in [(-50, -60), (-40, -40), (40, -60), (50, -40)]:
                e.append(f'<polygon points="{star_pts(gx+ox, gy+oy, 6)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="1.5"/>')
            # 腳下跳動小弧線
            e.append(f'<path d="M {gx-55} {gy+65} Q {gx-50} {gy+72} {gx-45} {gy+65}" fill="none" stroke="{SHOUT_MONSTER_RED}" stroke-width="2" stroke-linecap="round"/>')
            e.append(f'<path d="M {gx-5} {gy+65} Q {gx} {gy+72} {gx+5} {gy+65}" fill="none" stroke="{SHOUT_MONSTER_RED}" stroke-width="2" stroke-linecap="round"/>')
            # 「零聲音」符號（右上角）
            e.append(f'<circle cx="{gx+110}" cy="{gy-110}" r="16" fill="#FFFFFF" stroke="{SHOUT_MONSTER_RED}" stroke-width="2.5"/>')
            e.append(f'<text x="{gx+110}" y="{gy-103}" font-family="Huninn" font-size="16" fill="{SHOUT_MONSTER_RED}" font-weight="bold" text-anchor="middle">♪</text>')
            e.append(f'<line x1="{gx+95}" y1="{gy-125}" x2="{gx+125}" y2="{gy-95}" stroke="{SHOUT_MONSTER_RED}" stroke-width="2.5" stroke-linecap="round"/>')
            # 文字：「Quiet cheer」
            e.append(svgtext(gx, gy+100, "Quiet cheer!", size=22, fill=TXT, weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p7():
    """p7：觀點頁，左格安靜教室（同學微笑聽課、小音符）；
    右格：Owen 做無聲歡呼，Tr. Mina 也對他回無聲歡呼（拳頭互舉，愛心）。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p7"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#E8F8D8"/>')

    # 左格：安靜教室
    e.append(f'<rect x="80" y="100" width="360" height="300" rx="12" fill="#FFFFFF" stroke="#C4E8B4" stroke-width="3"/>')
    # Tr. Mina 講課
    e.append(teacher(cx=180, cy=260, scale=0.95, point="right"))
    # 同學們聽課（kid 群）
    e.append(kid(variant=0, cx=320, cy=260, scale=0.85, expr="smile"))
    e.append(kid(variant=1, cx=420, cy=270, scale=0.8, expr="think"))
    # 小音符（很輕）
    e.append(f'<path d="M 240 180 Q 250 170 260 180 Q 270 170 280 180" fill="none" stroke="#FFD93D" stroke-width="1.5" opacity="0.5"/>')

    # 右格：無聲歡呼對暗號
    e.append(f'<rect x="748" y="100" width="360" height="300" rx="12" fill="#FFFFFF" stroke="#C4E8B4" stroke-width="3"/>')
    # Owen 做無聲歡呼（半身 + 揮手）
    e.append(boy_bust(expr="big", cx=850, cy=240, scale=1.0, arms="handup"))
    # 星星在手邊
    e.append(f'<polygon points="{star_pts(790, 180, 8)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="2"/>')
    e.append(f'<polygon points="{star_pts(910, 180, 8)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="2"/>')
    # Tr. Mina 也舉拳頭回應（右側）
    e.append(teacher(cx=980, cy=260, scale=0.95, point="left"))
    # 重疊愛心在中間（象徵應答）
    e.append(f'<path d="M 940 150 c 0 -6 -6 -12 -12 -12 c -6 0 -12 6 -12 12 c 0 12 12 18 12 18 s 12 -6 12 -18 Z" fill="#FF6B6B" stroke="#E8574C" stroke-width="2"/>')

    return svg(W, H, "".join(e), bg=None)


def scene_p8():
    """p8：成功時刻，Owen 答對（黑板打勾），他做無聲歡呼（揮拳 + 星星 + 跳），
    全班同學也跟著做無聲歡呼，Tr. Mina 語音泡泡「Super quiet cheer, Owen!」。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p8"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#FFF0C9"/>')

    # 黑板（背景左側）
    e.append(f'<rect x="100" y="60" width="200" height="140" rx="8" fill="#C9A26B"/>')
    e.append(f'<rect x="120" y="80" width="160" height="100" rx="4" fill="#3E7C5B"/>')
    # 打勾
    e.append(f'<path d="M 135 120 L 155 140 L 185 100" fill="none" stroke="#7FD93D" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>')

    # 中央：Owen 做無聲歡呼（完整姿勢）
    owen_x, owen_y = 450, 280
    e.append(boy(pose="jump", expr="big", cx=owen_x, cy=owen_y, scale=1.0))
    # 雙手高舉星星
    for ox, oy in [(-50, -70), (-30, -70), (30, -70), (50, -70)]:
        e.append(f'<polygon points="{star_pts(owen_x+ox, owen_y+oy, 7)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="2"/>')

    # 兩側同學也跟著做（kid 群跳躍 + 星星）
    for kid_x in [250, 350, 650, 750, 850, 950]:
        e.append(kid(variant=(kid_x//50) % 4, cx=kid_x, cy=310, scale=0.8, expr="smile"))
        e.append(f'<polygon points="{star_pts(kid_x, kid_x-260, 5)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="1.5"/>')

    # Tr. Mina 在右上角，語音泡泡
    e.append(teacher(cx=1050, cy=220, scale=0.95, point="left"))
    bubble_x, bubble_y = 900, 120
    e.append(f'<path d="M {bubble_x-70} {bubble_y} L {bubble_x-100} {bubble_y-40} L {bubble_x+100} {bubble_y-40} Q {bubble_x+110} {bubble_y-50} {bubble_x+100} {bubble_y-40} Q {bubble_x+110} {bubble_y} {bubble_x+90} {bubble_y+40} L {bubble_x} {bubble_y+50} L {bubble_x-70} {bubble_y} Z" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="2.5"/>')
    e.append(svgtext(bubble_x, bubble_y, "Super quiet cheer,\nOwen!", size=20, fill=TXT, weight="bold"))

    return svg(W, H, "".join(e), bg=None)


def scene_p9():
    """p9：課後擊掌，Owen 和同學們開心擊掌（安靜慶祝），頭上星星與小愛心，教室和樂。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p9"]}"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#FFE2EC"/>')

    # Owen 站立微笑（中央）
    e.append(boy(pose="stand", expr="smile", cx=450, cy=280, scale=1.0))

    # 兩側同學擊掌（kid 群，手接觸）
    # 左邊同學
    e.append(kid(variant=0, cx=280, cy=300, scale=0.9, expr="smile"))
    # 擊掌短弧（左 kid 手 (316,415) → Owen 左手 (402,416)，手的高度、不穿身體）
    e.append(f'<path d="M 316 418 Q 360 402 402 416" fill="none" stroke="#FFD93D" stroke-width="5" stroke-linecap="round" opacity="0.85"/>')
    # 擊掌點星星
    e.append(f'<polygon points="{star_pts(352, 398, 6)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="1.5"/>')
    e.append(f'<polygon points="{star_pts(368, 408, 5)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="1.5"/>')

    # 右邊同學
    e.append(kid(variant=2, cx=620, cy=300, scale=0.9, expr="smile"))
    # 擊掌短弧（Owen 右手 (498,416) → 右 kid 手 (584,415)）
    e.append(f'<path d="M 498 416 Q 541 402 584 418" fill="none" stroke="#FFD93D" stroke-width="5" stroke-linecap="round" opacity="0.85"/>')
    # 擊掌點星星
    e.append(f'<polygon points="{star_pts(532, 398, 6)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="1.5"/>')
    e.append(f'<polygon points="{star_pts(548, 408, 5)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="1.5"/>')

    # 頭頂星星與愛心
    for (x, y, r) in [(350, 100, 14), (550, 80, 16), (750, 100, 14)]:
        e.append(star(x, y, r, fill=STAR_Y))

    # 3 顆正常大小愛心（寬 14px）
    for (hx, hy) in [(300, 120), (600, 100), (900, 120)]:
        e.append(f'<path d="M {hx} {hy} c 0 -7 -7 -14 -14 -14 c -7 0 -14 7 -14 14 c 0 14 14 21 14 21 s 14 -7 14 -21 Z" fill="#FF6B6B"/>')

    return svg(W, H, "".join(e), bg=None)


def scene_p10():
    """p10：英雄收尾，Owen 披紅披風，雙拳舉高發光、拳邊滿天小星星（無聲歡呼英雄 pose）。"""
    e = []
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="{BG["p10"]}"/>')

    # 滿天星星（背景）
    for _ in range(15):
        import random
        random.seed(hash((_,)) % 10000)
        sx = random.randint(100, 1088)
        sy = random.randint(50, 400)
        sr = random.randint(8, 16)
        e.append(star(sx, sy, sr, fill=STAR_Y))

    # Owen 披披風，雙拳舉高（jump pose + cape）
    e.append(boy(pose="jump", expr="big", cx=594, cy=280, scale=1.2, cape=True))

    # 雙拳發光（jump 手位：cx±74*s, cy-64*s）
    # s=1.2: 594±88.8, 280-76.8
    e.append(fist_glow(594-89, 280-77, s=1.2))
    e.append(fist_glow(594+89, 280-77, s=1.2))

    # 拳邊星星群
    for ox, oy in [(-110, -100), (-80, -120), (-60, -80), (110, -100), (80, -120), (60, -80)]:
        e.append(f'<polygon points="{star_pts(594+ox, 280+oy, 8)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="2"/>')

    return svg(W, H, "".join(e), bg=None)


# ================== PAGES & METADATA ==================

PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>School makes me SO excited!'),
    ("p2", scene_p2, 'Question time with Tr. Mina!<br/>I know it! I know it!'),
    ("p3", scene_p3, 'My answer is right!<br/>My happy grows big, big, BIG!'),
    ("p4", scene_p4, 'A <b>shout</b> jumps up my throat!<br/>&ldquo;YES!!&rdquo; It is so loud.<br/>My friends cover their ears.'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I catch the <b>shout</b>!'),
    ("p6", scene_p6, 'Catch the <b>shout</b>!<br/><b>Squeeze</b> my <b>fists</b> tight!<br/>Quiet cheer&mdash;YES! No sound!'),
    ("p7", scene_p7, 'Quiet rooms help everyone learn.<br/>Tr. Mina quiet cheers with me!<br/>Loud fun can be quiet fun.'),
    ("p8", scene_p8, 'I am right again!<br/>Fists tight&mdash;quiet cheer!<br/>&ldquo;Super quiet cheer, <b>Owen</b>!&rdquo;'),
    ("p9", scene_p9, 'My class loves my quiet cheer.<br/>My happy is still big!<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Catch the <b>shout</b>. <b>Squeeze</b> my <b>fists</b>.<br/><b>Quiet cheer!</b><br/>I practice every day!'),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3–4 次，重複讓腳本自動化——激動當下大腦來不及思考，只提取練過一百次的動作。"),
    ("出事後絕對不拿出來讀", "大叫被反映的當天不讀不罵。平靜時再讀，否則書變懲罰教材就報廢了。"),
    ("在家把無聲歡呼練成反射", "看比賽、玩遊戲、他答對任何事的時候，全家一起做「quiet cheer」（揮拳、原地跳、誇張嘴型都可以，就是零聲音）——練習時越浮誇越好，讓他覺得無聲版一樣爽。"),
    ("與 Tr. Mina 對暗號", "請老師提醒時只說 'Quiet cheer!'（指向替代動作，不說「不要叫」）；並區分兩個口訣——聲音漸變大用 'Volume down!'、興奮瞬間爆音用 'Quiet cheer!'，是兩顆不同肌肉。"),
    ("當他主動說 'A shout jumps up my throat'", "覺察里程碑，大力稱讚——他察覺衝動訊號了。"),
    ("當他爆音後自己改成無聲歡呼", "補救也算成功——從爆音到自我修正就是進步，要大力稱讚。"),
]

BOOK = {
    "slug": "quiet-cheer",
    "order": 20,
    "title_pre": "", "title_hi": "Quiet", "title_post": " Cheer!",
    "title_zh": "無聲歡呼",
    "subtitle": "Owen's excitement story",
    "tagline_zh": "課堂激動時大聲叫喊→抓住喊聲→握拳擠壓→無聲歡呼",
    "chips": ["Social Story", "Classroom", "12 pages"],
    "pdf_name": "Quiet_Cheer.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ['shout', 'squeeze', 'fist'],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。本書教的不是「不要太興奮」，"
                     "而是替 Owen 安裝一套<b>激動當下用得出來的正向替代腳本</b>："
                     "感覺到大聲叫喊的衝動 → 抓住喊聲 → 握拳擠壓 → 打開變成無聲歡呼 → "
                     "能量沒有消失，只是變形。目標是幫他看到<b>興奮本身是好的</b>，要換的是<b>出口</b>不是熱情。"),
    "cue_html": ("口訣（全書通關密語）：<b>Catch the shout → Squeeze my fists → Quiet cheer!</b>&nbsp;"
                 "完整三部曲是「Catch the shout（抓住喊聲）→ Squeeze my fists（握拳擠壓）→ Quiet cheer!（無聲歡呼）」。"
                 "老師現場提醒時只說 <b>'Quiet cheer!'</b> 兩個字，指向替代動作，不說「不要叫」。"),
    "cover": scene_cover,
}
