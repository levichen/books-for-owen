# -*- coding: utf-8 -*-
"""Book 5: Eyes on Teacher! — 上課分心後把注意力帶回來（refocusing in class）。
內容架構參考 book_save_my_answer.py，核心創新：腦小狗吉祥物自繪 + Ethan 新角色。"""
from parts import *
from book_common import svg, svgtext, TXT, W, H
import math

# soft page palettes (教室氛圍延續)
BG = {
    "cover": "#FFE9D6", "p1": "#E8F4FF", "p2": "#FFF3D6", "p3": "#FFE3C2",
    "p4": "#FFD9CF", "p5": "#D7C8FF", "p6": "#D7E9F8", "p7": "#DFF0DC",
    "p8": "#FFF0C9", "p9": "#FFE2EC", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

# Brain puppy colors
PUPPY_BODY = "#B49AE8"
PUPPY_BRAIN = "#8B6BC8"
PUPPY_NOSE = "#FFB6A0"
PUPPY_GLOW = "#D7C8FF"

# ============================================================================
# Brain Puppy Helper Functions
# ============================================================================

def puppy(cx=0, cy=0, scale=1.0, mood="happy"):
    """淡紫色小狗吉祥物：明確的狗吻部 + 垂耳 + 搖尾巴 + 頭頂腦紋捲毛。
    mood: "happy" (發光微笑) | "run" (奔跑、速度線) | "sleep" (打呼、星星)
    """
    p = []

    # 光暈（happy 時）
    if mood == "happy":
        p.append(f'<circle cx="0" cy="0" r="76" fill="{PUPPY_GLOW}" fill-opacity="0.25"/>')
        p.append(f'<circle cx="0" cy="0" r="52" fill="{PUPPY_GLOW}" fill-opacity="0.15"/>')

    # 身體（圓胖形）
    p.append(f'<ellipse cx="0" cy="16" rx="48" ry="52" fill="{PUPPY_BODY}" stroke="{PUPPY_BRAIN}" stroke-width="3"/>')

    # 四隻腿（小圓腿）
    legs = [(-28, 62), (28, 62), (-20, 76), (20, 76)]
    for lx, ly in legs:
        p.append(f'<circle cx="{lx}" cy="{ly}" r="11" fill="{PUPPY_BODY}" stroke="{PUPPY_BRAIN}" stroke-width="2"/>')

    # 腳掌（下方小橢圓）
    for lx, ly in legs:
        p.append(f'<ellipse cx="{lx}" cy="{ly+16}" rx="12" ry="8" fill="#E8D0B8" stroke="{PUPPY_BRAIN}" stroke-width="1.5"/>')

    # 尾巴：上翹的粗曲線 + 搖動波紋
    if mood in ("happy", "sleep"):
        p.append(f'<path d="M 40 38 Q 62 12 66 -12" fill="none" stroke="{PUPPY_BODY}" stroke-width="18" stroke-linecap="round"/>')
        # 搖動波紋（2 條小弧）
        p.append(f'<path d="M 44 30 Q 48 20 52 28" fill="none" stroke="{PUPPY_BRAIN}" stroke-width="2.5" opacity="0.6"/>')
        p.append(f'<path d="M 54 18 Q 60 6 64 16" fill="none" stroke="{PUPPY_BRAIN}" stroke-width="2.5" opacity="0.6"/>')
    elif mood == "run":
        p.append(f'<path d="M 40 28 Q 68 8 80 -24" fill="none" stroke="{PUPPY_BODY}" stroke-width="18" stroke-linecap="round"/>')
        # 奔跑時搖動波紋更活潑
        p.append(f'<path d="M 44 22 Q 52 8 60 20" fill="none" stroke="{PUPPY_BRAIN}" stroke-width="2.5" opacity="0.7"/>')
        p.append(f'<path d="M 58 10 Q 68 -6 76 8" fill="none" stroke="{PUPPY_BRAIN}" stroke-width="2.5" opacity="0.7"/>')

    # 頭部（橢圓形）
    p.append(f'<ellipse cx="0" cy="-28" rx="42" ry="40" fill="{PUPPY_BODY}" stroke="{PUPPY_BRAIN}" stroke-width="3"/>')

    # 垂耳（兩側下垂的長橢圓，深紫色）
    p.append(f'<ellipse cx="-36" cy="-8" rx="13" ry="24" fill="{PUPPY_BRAIN}" stroke="{PUPPY_BRAIN}" stroke-width="1"/>')
    p.append(f'<ellipse cx="36" cy="-8" rx="13" ry="24" fill="{PUPPY_BRAIN}" stroke="{PUPPY_BRAIN}" stroke-width="1"/>')

    # 吻部（頭前下方淺色橢圓凸出）
    p.append(f'<ellipse cx="0" cy="0" rx="26" ry="28" fill="#D4C8F0" stroke="{PUPPY_BRAIN}" stroke-width="2"/>')

    # 黑鼻頭（吻部前端的圓形）
    p.append(f'<circle cx="0" cy="10" r="7" fill="#2A2320"/>')

    # 微笑嘴線（吻部下方）
    p.append(f'<path d="M -8 18 Q 0 24 8 18" fill="none" stroke="#2A2320" stroke-width="3" stroke-linecap="round"/>')

    # 眼睛（大黑眼珠 + 亮點）
    if mood in ("happy", "run"):
        p.append(f'<circle cx="-14" cy="-34" r="7" fill="#2A2320"/>')
        p.append(f'<circle cx="14" cy="-34" r="7" fill="#2A2320"/>')
        p.append(f'<circle cx="-13" cy="-35" r="2.5" fill="#FFFFFF"/>')
        p.append(f'<circle cx="15" cy="-35" r="2.5" fill="#FFFFFF"/>')
    elif mood == "sleep":
        p.append(f'<path d="M -20 -34 Q -14 -30 -8 -34" fill="none" stroke="#2A2320" stroke-width="3.5" stroke-linecap="round"/>')
        p.append(f'<path d="M 8 -34 Q 14 -30 20 -34" fill="none" stroke="#2A2320" stroke-width="3.5" stroke-linecap="round"/>')

    # 腦紋捲毛（頭頂 2-3 圈，核心識別元素）
    if mood != "run":
        for i, (bx, by, br) in enumerate([(-20, -72, 11), (0, -78, 13), (20, -72, 11)]):
            p.append(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="none" stroke="{PUPPY_BRAIN}" stroke-width="3"/>')
    else:
        # run 時簡化捲毛但保留
        for i, (bx, by, br) in enumerate([(-16, -74, 10), (16, -74, 10)]):
            p.append(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="none" stroke="{PUPPY_BRAIN}" stroke-width="2.5"/>')

    # 速度線（mood="run" 時）
    if mood == "run":
        for i, (sx, sy) in enumerate([(50, 20), (68, 35), (76, 8)]):
            p.append(f'<line x1="{sx}" y1="{sy}" x2="{sx+26}" y2="{sy+8}" stroke="#F26B5E" stroke-width="4" stroke-linecap="round" opacity="0.7"/>')

    # 打呼 Z 字（mood="sleep" 時）
    if mood == "sleep":
        p.append(f'<path d="M -10 -90 l 7 -7 l 7 7" fill="none" stroke="#8B6BC8" stroke-width="2.5" stroke-linecap="round"/>')

    inner = "".join(p)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


# ============================================================================
# SCENES
# ============================================================================

def scene_cover():
    """封面：Owen 白T + puppy 互看，教室元素點綴"""
    e = []
    # 教室背景元素（左上黑板、右下書架）
    e.append(f'<rect x="80" y="40" width="200" height="140" rx="10" fill="#C9A26B"/>')  # 黑板框
    e.append(f'<rect x="100" y="60" width="160" height="100" rx="6" fill="#3E7C5B"/>')  # 黑板面
    e.append(f'<rect x="840" y="220" width="220" height="180" rx="8" fill="#D4A574"/>')  # 書架
    for i in range(3):
        e.append(f'<line x1="850" y1="{240+i*50}" x2="1040" y2="{240+i*50}" stroke="#B08A56" stroke-width="3"/>')

    # 地板
    e.append(f'<ellipse cx="594" cy="640" rx="560" ry="120" fill="#E8D2AC"/>')

    # Owen 與 puppy 互看
    e.append(boy(pose="stand", expr="big", cx=320, cy=320, scale=1.25))
    e.append(puppy(cx=800, cy=300, scale=0.75, mood="happy"))

    # 視線虛線連接
    e.append(f'<path d="M 360 260 Q 580 220 740 240" fill="none" stroke="#D9B6E8" stroke-width="3" stroke-dasharray="5 8"/>')

    # 星星裝飾
    e.append(star(200, 100, 18))
    e.append(star(1000, 140, 16))
    e.append(sparkle(450, 120, 12))
    e.append(sparkle(750, 380, 10))

    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """Owen 白T 開心站立，身旁飄著微笑的淡紫色腦小狗（發光），互相對看"""
    e = []
    e.append(f'<rect x="0" y="420" width="1188" height="140" fill="#BFE3B4"/>')  # 草地
    e.append(f'<path d="M 0 560 Q 594 400 1188 560 L 1188 560 L 0 560 Z" fill="#EED9A8"/>')  # 路

    # 遠景校舍
    e.append(f'<rect x="880" y="270" width="230" height="160" rx="10" fill="#F6C9A0" stroke="#D8A377" stroke-width="4"/>')
    e.append(f'<rect x="960" y="350" width="60" height="80" rx="6" fill="#8A5A3C"/>')
    e.append(f'<rect x="906" y="300" width="44" height="36" rx="4" fill="#BEE3F2"/>')
    e.append(f'<rect x="1040" y="300" width="44" height="36" rx="4" fill="#BEE3F2"/>')
    e.append(f'<polygon points="870,270 995,205 1120,270" fill="#E4574C"/>')

    # 樹叢
    e.append(f'<circle cx="80" cy="430" r="40" fill="#8FCB84"/><circle cx="130" cy="440" r="30" fill="#79BD6E"/>')

    # Owen 開心站立
    e.append(boy(pose="stand", expr="big", cx=420, cy=250, scale=1.2))

    # 腦小狗在身旁（互相對看）
    e.append(puppy(cx=800, cy=210, scale=1.1, mood="happy"))

    # 視線虛線
    e.append(f'<path d="M 460 220 Q 640 180 760 200" fill="none" stroke="#D9B6E8" stroke-width="3" stroke-dasharray="5 8"/>')

    # 星星和火花
    e.append(star(300, 80, 18))
    e.append(sparkle(550, 120, 14))
    e.append(sparkle(250, 350, 10))

    return svg(W, H, "".join(e))


def scene_p2():
    """教室：Tr. Mina 在綠黑板前教學（板上畫ABC），Owen 坐課桌前專心，腦小狗乖坐在他頭頂"""
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#E8D2AC"/>')  # 地板

    # 黑板
    e.append(f'<rect x="360" y="60" width="560" height="300" rx="14" fill="#C9A26B"/>')
    e.append(f'<rect x="376" y="76" width="528" height="268" rx="8" fill="#3E7C5B"/>')
    # 板上寫 ABC
    e.append(svgtext(500, 220, "A", size=80, fill="#FFF7E0", weight="bold"))
    e.append(svgtext(640, 220, "B", size=80, fill="#FFF7E0", weight="bold"))
    e.append(svgtext(780, 220, "C", size=80, fill="#FFF7E0", weight="bold"))
    # 粉筆盒
    e.append(f'<rect x="500" y="360" width="280" height="12" rx="6" fill="#B08A56"/>')

    # 老師指著黑板
    e.append(teacher(cx=200, cy=280, scale=1.0, point="right"))

    # Owen 坐在課桌前（右側），專心聽課
    e.append(desk(cx=1000, cy=430, w=220))
    e.append(boy_bust(expr="oh", cx=1000, cy=330, scale=0.85))

    # 腦小狗乖乖坐在 Owen 頭頂
    e.append(puppy(cx=1000, cy=220, scale=0.75, mood="happy"))

    return svg(W, H, "".join(e))


def scene_p3():
    """兩格觸發：左格 Ethan 的腳碰到 Owen 椅腳（oops星號）；右格 Owen 頭上思考泡泡冒出好笑的香蕉臉"""
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#E8D2AC"/>')  # 地板

    # 分格：左右兩個圓角矩形
    # 左格框
    e.append(f'<rect x="80" y="100" width="460" height="340" rx="20" fill="none" stroke="#D4B8A0" stroke-width="4"/>')
    # 右格框
    e.append(f'<rect x="660" y="100" width="460" height="340" rx="20" fill="none" stroke="#D4B8A0" stroke-width="4"/>')

    # 左格：Ethan 不小心碰到 Owen 的椅子
    e.append(f'<text x="270" y="135" font-family="Huninn" font-size="24" font-weight="bold" fill="#4A4A4A" text-anchor="middle">Oops!</text>')
    desk_x, desk_y = 250, 420
    e.append(desk(cx=desk_x, cy=desk_y, w=200, scale=0.9))
    e.append(boy_bust(expr="smile", cx=desk_x, cy=300, scale=0.8))
    e.append(ethan(cx=350, cy=350, scale=0.9, expr="think"))  # Ethan 腳往椅子踢
    # oops 星號
    e.append(star(360, 320, 22, fill="#FFB6A0"))

    # 右格：Owen 頭上思考泡泡
    e.append(f'<text x="890" y="135" font-family="Huninn" font-size="24" font-weight="bold" fill="#4A4A4A" text-anchor="middle">Giggle!</text>')
    desk_x2, desk_y2 = 850, 420
    e.append(desk(cx=desk_x2, cy=desk_y2, w=200, scale=0.9))
    e.append(boy_bust(expr="big", cx=desk_x2, cy=300, scale=0.8))

    # 思考泡泡（頭上）
    e.append(f'<circle cx="920" cy="200" r="60" fill="#FFFFFF" stroke="#D9B6E8" stroke-width="4"/>')
    e.append(f'<path d="M 920 260 Q 905 280 890 290" fill="none" stroke="#D9B6E8" stroke-width="3"/>')
    # 香蕉臉笑臉（泡泡內）
    e.append(f'<path d="M 900 180 Q 910 175 920 180" fill="none" stroke="#FFD34D" stroke-width="3" stroke-linecap="round"/>')  # 眼
    e.append(f'<path d="M 920 180 Q 930 175 940 180" fill="none" stroke="#FFD34D" stroke-width="3" stroke-linecap="round"/>')
    e.append(f'<path d="M 905 210 Q 920 225 935 210" fill="none" stroke="#FFD34D" stroke-width="4" stroke-linecap="round"/>')  # 嘴

    return svg(W, H, "".join(e))


def scene_p4():
    """衝動頁：腦小狗從Owen頭頂跳出去追彩球（虛線軌跡），Owen側身跟Ethan笑成一團，眼睛離開黑板方向，Tr.Mina在遠處變小"""
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#E8D2AC"/>')  # 地板

    # 黑板遠景（左上，變小，褪色）
    e.append(f'<rect x="120" y="80" width="280" height="180" rx="10" fill="#C9A26B" opacity="0.5"/>')
    e.append(f'<rect x="138" y="100" width="244" height="140" rx="6" fill="#3E7C5B" opacity="0.5"/>')

    # Tr. Mina 遠景（變小，右上角）
    e.append(teacher(cx=950, cy=200, scale=0.6, point="right"))

    # 彩球（中上方，Owen 和 Ethan 朝向）
    e.append(f'<circle cx="750" cy="200" r="28" fill="#FF6B9D" stroke="#E8574C" stroke-width="3"/>')
    e.append(f'<ellipse cx="750" cy="200" rx="8" ry="20" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.6"/>')

    # 腦小狗軌跡虛線（從左下出發追彩球）
    e.append(f'<path d="M 380 350 Q 520 240 710 200" fill="none" stroke="#D9B6E8" stroke-width="3" stroke-dasharray="6 10"/>')

    # 腦小狗跳出去（中間位置，朝彩球）
    e.append(puppy(cx=550, cy=260, scale=0.95, mood="run"))

    # Owen 側身坐（左側，半身，笑成一團）
    e.append(f'<rect x="180" y="420" width="200" height="30" rx="12" fill="#D9B98C"/>')  # 課桌
    e.append(boy_bust(expr="big", cx=220, cy=310, scale=0.9, arms="desk"))

    # Ethan 側身坐（Owen 旁邊，也笑）
    e.append(f'<rect x="420" y="420" width="200" height="30" rx="12" fill="#D9B98C"/>')  # 課桌
    e.append(ethan(cx=460, cy=310, scale=0.9, expr="smile"))

    # 速度線四周
    for (sx, sy) in [(650, 150), (700, 120), (640, 260)]:
        e.append(f'<path d="M {sx} {sy} l 30 -15" fill="none" stroke="#F26B5E" stroke-width="5" stroke-linecap="round"/>')

    return svg(W, H, "".join(e))


def scene_p5():
    """紫色星空背景：Owen（press表情）張開雙臂，腦小狗沿虛線弧跑回他懷裡，柔和光暈"""
    e = []
    # 星空背景（深紫）
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#4A3A5C"/>')

    # 星星散佈
    for (x, y, r) in [(150, 80, 16), (1030, 100, 20), (200, 440, 14), (1000, 420, 16), (450, 150, 12), (950, 340, 14)]:
        e.append(star(x, y, r, fill="#E8D9FF"))

    sparkles = [(320, 90, 12), (860, 80, 12), (90, 300, 10), (1100, 300, 10), (600, 50, 10)]
    for (sx, sy, sr) in sparkles:
        e.append(sparkle(sx, sy, sr, fill="#E8D9FF"))

    # Owen 張開雙臂（press 表情，姿態像要擁抱 puppy）
    e.append(boy(pose="hips", expr="press", cx=450, cy=280, scale=1.15))

    # 柔和光暈（圓形，漸層效果用半透明圓）
    e.append(f'<circle cx="450" cy="280" r="160" fill="#D7C8FF" fill-opacity="0.15"/>')
    e.append(f'<circle cx="450" cy="280" r="100" fill="#D7C8FF" fill-opacity="0.25"/>')

    # 腦小狗沿虛線弧跑回來
    e.append(f'<path d="M 750 180 Q 650 160 520 280" fill="none" stroke="#D9B6E8" stroke-width="3" stroke-dasharray="6 10"/>')

    # 腦小狗在軌跡上（朝向 Owen）
    e.append(puppy(cx=650, cy=200, scale=1.0, mood="run"))

    return svg(W, H, "".join(e))


def scene_p6():
    """三步腳本：①Owen 轉頭對 Ethan 小語音泡泡"Play later!" ②腦小狗回到頭頂 ③視線虛線連到teacher"""
    e = []
    e.append(f'<rect x="0" y="480" width="1188" height="80" fill="#BFD9EE"/>')  # 天藍地板

    # 三個步驟圓形分隔（上方）
    for i, (cx, label) in enumerate([(280, "1"), (594, "2"), (908, "3")]):
        e.append(f'<circle cx="{cx}" cy="120" r="40" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="4"/>')
        e.append(svgtext(cx, 135, label, size=44, fill="#4A78A8", weight="bold"))

    # 步驟 1：Owen 對 Ethan 說 "Play later!"
    desk_x1, desk_y1 = 220, 380
    e.append(desk(cx=desk_x1, cy=desk_y1, w=180, scale=0.85))
    e.append(boy_bust(expr="smile", cx=desk_x1, cy=280, scale=0.8, arms="desk"))
    e.append(ethan(cx=280, cy=300, scale=0.85, expr="smile"))
    # 小語音泡泡
    e.append(f'<path d="M 240 220 Q 250 180 300 170 L 350 170 Q 370 170 370 190 Q 370 210 350 210 L 310 210 Q 290 210 280 220 Z" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
    e.append(svgtext(310, 195, "Play later!", size=18, fill="#4A78A8", weight="bold"))

    # 步驟 2：腦小狗回到頭頂
    desk_x2, desk_y2 = 594, 380
    e.append(desk(cx=desk_x2, cy=desk_y2, w=180, scale=0.85))
    e.append(boy_bust(expr="press", cx=desk_x2, cy=280, scale=0.8))
    e.append(puppy(cx=desk_x2, cy=200, scale=0.8, mood="happy"))

    # 步驟 3：視線虛線到 teacher
    desk_x3, desk_y3 = 908, 380
    e.append(desk(cx=desk_x3, cy=desk_y3, w=180, scale=0.85))
    e.append(boy_bust(expr="press", cx=desk_x3, cy=280, scale=0.8))
    e.append(teacher(cx=1020, cy=240, scale=0.7, point="left"))
    # 視線虛線
    e.append(f'<path d="M 920 260 L 980 240" fill="none" stroke="#D9B6E8" stroke-width="2" stroke-dasharray="4 6"/>')

    return svg(W, H, "".join(e))


def scene_p7():
    """觀點頁：Tr. Mina 在黑板前（板上有趣圖案），台下三位同學（含 Ethan）眼睛都有視線虛線連到老師"""
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#CBE3C2"/>')  # 綠地板

    # 黑板
    e.append(f'<rect x="340" y="60" width="500" height="280" rx="12" fill="#C9A26B"/>')
    e.append(f'<rect x="360" y="80" width="460" height="240" rx="8" fill="#3E7C5B"/>')
    # 板上有趣圖案（簡單的笑臉和星星）
    e.append(f'<circle cx="450" cy="180" r="40" fill="none" stroke="#FFF7E0" stroke-width="5"/>')
    e.append(f'<circle cx="440" cy="170" r="4" fill="#FFF7E0"/>')
    e.append(f'<circle cx="460" cy="170" r="4" fill="#FFF7E0"/>')
    e.append(f'<path d="M 440 190 Q 450 200 460 190" fill="none" stroke="#FFF7E0" stroke-width="4" stroke-linecap="round"/>')
    e.append(star(560, 160, 30, fill="#FFF7E0", stroke="#FFF7E0", sw=0))

    # Tr. Mina 指著黑板
    e.append(teacher(cx=180, cy=280, scale=1.0, point="right"))

    # 三位同學（視線連到老師）
    kid_positions = [(280, 330), (594, 330), (928, 330)]
    for i, (kid_x, kid_y) in enumerate(kid_positions):
        if i == 2:  # 第三個是 Ethan
            e.append(ethan(cx=kid_x, cy=kid_y, scale=0.95, expr="think"))
        else:
            e.append(kid(variant=i, cx=kid_x, cy=kid_y, scale=0.95, expr="think"))

        # 視線虛線（從眼睛連到老師）
        e.append(f'<path d="M {kid_x+20} {kid_y-70} L 210 240" fill="none" stroke="#B9CFE8" stroke-width="2" stroke-dasharray="4 6"/>')

    return svg(W, H, "".join(e))


def scene_p8():
    """Tr. Mina 豎拇指 + 語音泡泡"Great listening, Owen!"；角落小格：Owen 和 Ethan 追逐玩"""
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#E8D2AC"/>')  # 地板

    # 主場景：Tr. Mina 豎拇指
    e.append(teacher(cx=280, cy=280, scale=1.05, point="right"))
    # 修改 teacher 顯示豎拇指：用 SVG 額外元素
    e.append(f'<path d="M 380 220 L 400 140" stroke="#FFD9B6" stroke-width="16" stroke-linecap="round"/>')  # 拇指
    e.append(f'<circle cx="405" cy="135" r="13" fill="#FFD9B6"/>')  # 拇指頂

    # 語音泡泡
    e.append(f'<path d="M 500 100 Q 500 50 600 50 L 900 50 Q 950 50 950 100 Q 950 150 900 150 L 700 150 L 650 200 L 680 150 L 600 150 Q 500 150 500 100 Z" fill="#FFFFFF" stroke="#E3C98F" stroke-width="5"/>')
    e.append(svgtext(725, 110, "Great listening, Owen!", size=32, fill="#D97706", weight="bold"))

    # 右下小格：Owen 和 Ethan 追逐（離開課桌）
    e.append(f'<rect x="800" y="340" width="340" height="180" rx="12" fill="#FFF8F0" stroke="#D4B8A0" stroke-width="3"/>')
    e.append(boy(pose="run", expr="big", cx=900, cy=400, scale=0.8))
    e.append(ethan(cx=1020, cy=410, scale=0.8, expr="smile"))

    return svg(W, H, "".join(e))


def scene_p9():
    """Owen 抬頭挺胸微笑，腦小狗在他頭頂戴著小星星獎牌趴著滿足睡"""
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#F2CFDC"/>')  # 粉紅地板

    # 滿天彩帶（上方）
    import random
    random.seed(9)
    cols = ["#F6C445", "#7BC47F", "#6FA8DC", "#F49AB5", "#E4574C"]
    for i in range(24):
        x, y = random.randint(40, 1148), random.randint(20, 200)
        c = cols[i % 5]
        e.append(f'<rect x="{x}" y="{y}" width="10" height="16" rx="3" fill="{c}" transform="rotate({random.randint(-40,40)} {x} {y})"/>')

    # Owen 抬頭挺胸
    e.append(boy(pose="hips", expr="proud", cx=594, cy=240, scale=1.2))

    # 腦小狗在頭頂戴小星星（趴著睡）
    e.append(puppy(cx=594, cy=60, scale=0.85, mood="sleep"))
    # 星星獎牌（小星星在 puppy 頭頂）
    e.append(f'<circle cx="594" cy="20" r="18" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="3"/>')
    e.append(f'<polygon points="{star_pts(594, 20, 9)}" fill="#FFFFFF"/>')

    # 星星和火花
    e.append(star(450, 130, 18))
    e.append(star(750, 140, 16))
    e.append(sparkle(380, 90, 12))
    e.append(sparkle(820, 100, 12))

    return svg(W, H, "".join(e))


def scene_p10():
    """英雄收尾：Owen 披紅披風叉腰，腦小狗披迷你披風站旁邊，滿天星"""
    e = []
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="110" fill="#FFDD7E"/>')  # 金色地板

    # 滿天星
    for (x, y, r) in [(160, 90, 18), (1020, 100, 22), (120, 380, 16), (1060, 380, 16), (330, 50, 14), (860, 60, 16), (420, 320, 12)]:
        e.append(star(x, y, r))

    sparkles = [(260, 240, 12), (930, 240, 12), (600, 120, 10)]
    for (sx, sy, sr) in sparkles:
        e.append(sparkle(sx, sy, sr))

    # Owen 披紅披風叉腰
    e.append(boy(pose="hips", expr="proud", cx=480, cy=200, scale=1.3, cape=True))

    # 腦小狗披迷你披風站旁邊
    puppy_cape_x, puppy_cape_y = 740, 260
    # 迷你披風
    e.append(f'<path d="M {puppy_cape_x-40} {puppy_cape_y-20} Q {puppy_cape_x-60} {puppy_cape_y+20} {puppy_cape_x-40} {puppy_cape_y+60} L {puppy_cape_x+40} {puppy_cape_y+60} Q {puppy_cape_x+60} {puppy_cape_y+20} {puppy_cape_x+40} {puppy_cape_y-20} Z" fill="#E4574C" opacity="0.9"/>')
    e.append(puppy(cx=puppy_cape_x, cy=puppy_cape_y, scale=1.0, mood="happy"))

    return svg(W, H, "".join(e))


# ============================================================================
# PAGE TEXTS（直接來自 story-spec.md）
# ============================================================================

PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>My brain is like a <b>puppy</b>.<br/>It loves fun things!'),
    ("p2", scene_p2, 'In class, Tr. Mina is teaching.<br/>I listen and learn.'),
    ("p3", scene_p3, 'Ethan\'s foot bumps my chair.<br/>Or a funny thought pops up!<br/>We <b>giggle</b> and giggle.'),
    ("p4", scene_p4, 'My brain runs away!<br/><b>Giggle, giggle</b> goes my mouth.<br/>My eyes leave Tr. Mina.'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower…<br/>I <b>catch</b> my puppy brain!'),
    ("p6", scene_p6, 'I tell Ethan, "Play later!"<br/>I catch my brain.<br/><b>Eyes on teacher!</b>'),
    ("p7", scene_p7, 'Tr. Mina teaches fun things.<br/>My friends are listening.<br/>Learning needs my eyes and ears.'),
    ("p8", scene_p8, 'Tr. Mina smiles at me.<br/>"Great listening, <b>Owen</b>!"<br/>Ethan and I play later!'),
    ("p9", scene_p9, 'I feel proud.<br/>Learning is fun.<br/>My puppy brain sits happy!'),
    ("p10", scene_p10, 'Catch my brain. Play later.<br/><b>Eyes on teacher!</b><br/>I practice every day!'),
]

# ============================================================================
# PARENT TIPS（六條標準格式＋本書特有三條）
# ============================================================================

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3–4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("請 Tr. Mina 用同一暗號", "上課看到他飄走，只要說「Eyes on teacher」（或指指眼睛），不用長篇提醒。"),
    ("Ethan 不是壞人", "這本書教的是「Play later」不是「不要理 Ethan」——下課跟 Ethan 玩是腳本的一部分。"),
    ("當他主動說「My brain ran away」", "代表他察覺到分心了，這是後設認知里程碑，大力稱讚。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

# ============================================================================
# BOOK DICT
# ============================================================================

BOOK = {
    "slug": "eyes-on-teacher",
    "order": 5,
    "title_pre": "", "title_hi": "Eyes", "title_post": " on Teacher!",
    "title_zh": "眼睛看老師",
    "subtitle": "Owen's classroom story",
    "tagline_zh": "Owen 的專心故事",
    "chips": ["Social Story", "Classroom", "12 pages"],
    "pdf_name": "Eyes_On_Teacher.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ['puppy', 'giggle', 'catch'],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>：發現分心（My brain ran away）→ 叫牠回來（Catch my brain）→ 眼睛回到老師身上（Eyes on teacher!）。"),
    "cue_html": ("口訣（全書通關密語）：<b>Catch my brain → Play later → Eyes on teacher!</b>&nbsp;"
                 "當他哪天主動說出「My brain ran away」（我的大腦跑掉了），"
                 "就是最值得大力稱讚的時刻——代表他有後設認知了。"),
    "cover": scene_cover,
}
