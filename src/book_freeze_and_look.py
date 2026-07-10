# -*- coding: utf-8 -*-
"""Book 6: Freeze and Look! — Owen 在足球場學會停下來、看、聽（社會故事）。"""
from parts import *
from book_common import svg, svgtext, TXT, W, H
import math

# soft page palettes — 家→球場(綠)→衝動(紅紫)→冰凍(深紫星空)→定格(冰藍)→隊友(柔和)→球場(黃)→慶祝(彩)→英雄(金)
BG = {
    "cover": "#FFE9C9", "p1": "#E8F4F8", "p2": "#D4E8C9", "p3": "#D4E8C9",
    "p4": "#E8D4F0", "p5": "#2C1A4A", "p6": "#B8D8E8", "p7": "#E6D8C4",
    "p8": "#E8D8C9", "p9": "#F0D4E0", "p10": "#FFF0D0", "p11": "#FBF4E8",
}

# ============================================================
# SCENE FUNCTIONS
# ============================================================

def scene_cover():
    """封面：Owen 白 T 踩著足球，頭上星星"""
    e = []
    # 天空：淡藍
    e.append(f'<rect x="0" y="0" width="1188" height="620" fill="#E8F4F8"/>')
    e.append(sun(100, 80, 36))
    e.append(cloud(950, 100, 1.0))
    # 地面
    e.append(f'<rect x="0" y="450" width="1188" height="170" fill="#D4E8C9"/>')
    # 星星
    for (x, y, r) in [(200, 150, 18), (950, 200, 20), (350, 80, 14), (1030, 350, 16)]:
        e.append(star(x, y, r))
    # Owen 白 T，踩球 (feet_y = cy + 228*scale = 200 + 228*1.2 = 473)
    e.append(boy(pose="stand", expr="smile", cx=594, cy=200, scale=1.2, jersey=None))
    e.append(soccer_ball(cx=594, cy=470, r=28))
    return svg(1188, 620, "".join(e), bg=None)

def scene_p1():
    """Owen 白 T 踩著足球，頭上星星 (text: This is me, Owen! I am number 0. I love soccer!)"""
    e = []
    # 天空
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#E8F4F8"/>')
    e.append(sun(1050, 100, 40))
    e.append(cloud(180, 110, 1.0))
    e.append(cloud(600, 80, 0.7))
    # 星星環繞
    for (x, y, r) in [(200, 160, 20), (1020, 200, 22), (350, 100, 16), (700, 380, 18), (1060, 420, 14)]:
        e.append(star(x, y, r))
    # Owen，踩球 (feet_y = cy + 228*scale = 220 + 228*1.2 = 493)
    e.append(boy(pose="stand", expr="smile", cx=420, cy=220, scale=1.2, jersey=None))
    e.append(soccer_ball(cx=420, cy=495, r=32))
    return svg(W, H, "".join(e))

def scene_p2():
    """綠色球場：Daddy 掛著哨子舉手講解，Owen（0 號球衣）與 Lucas 站在旁邊聽，球門在遠處 (text: Practice day! Daddy blows the whistle. We run and kick!)"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#D4E8C9"/>')
    # 草地先畫（背景）
    e.append(f'<rect x="0" y="320" width="1188" height="240" fill="#7BC87F"/>')
    e.append(f'<ellipse cx="594" cy="400" rx="400" ry="30" fill="#6BA870"/>')  # 陰影
    # 球門遠景在右方
    e.append(goal(cx=950, cy=320, scale=0.6))
    # 中線
    e.append(f'<line x1="0" y1="380" x2="1188" y2="380" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="20 10"/>')
    # 人物（在草地之後）
    # Daddy：掛哨子，舉手講解，大尺寸
    e.append(daddy(cx=280, cy=260, scale=1.2, pose="point", whistle=True))
    # Owen 0 號球衣
    e.append(boy(pose="stand", expr="smile", cx=580, cy=320, scale=1.0, jersey=('0', '#57A863', '#2F7A44')))
    # Lucas
    e.append(lucas(cx=750, cy=330, scale=1.0, expr="smile"))
    # 語音泡泡："Let's go!"
    e.append(f'<ellipse cx="280" cy="160" rx="100" ry="50" fill="#FFFFFF" stroke="#8A5A3C" stroke-width="4"/>')
    e.append(f'<path d="M 240 190 L 180 240 L 220 200 Z" fill="#FFFFFF" stroke="#8A5A3C" stroke-width="3"/>')
    e.append(svgtext(280, 175, "Let's go!", size=32, fill="#000000", weight="bold"))
    return svg(W, H, "".join(e))

def scene_p3():
    """Owen 追球狂奔（run 姿勢＋速度線），星星眼，足球在前方滾 (text: I chase the ball. Fast, fast, faster! This is SO fun!)"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#D4E8C9"/>')
    # 草地
    e.append(f'<rect x="0" y="320" width="1188" height="240" fill="#7BC87F"/>')
    # 速度線（Owen 身後）
    for i in range(4):
        y_off = i * 40 - 60
        e.append(f'<line x1="200" y1="{340 + y_off}" x2="80" y2="{340 + y_off}" stroke="#F2A5A0" stroke-width="8" stroke-linecap="round" opacity="0.6"/>')
    # Owen run，大尺寸，星星眼 expr="star"（cy=225 → 前腳 feet_y ≈ 521，畫布內）
    e.append(boy(pose="run", expr="star", cx=350, cy=225, scale=1.3, jersey=('0', '#57A863', '#2F7A44')))
    # 球在前方滾動
    e.append(soccer_ball(cx=750, cy=420, r=26))
    # 星星點綴
    e.append(star(900, 200, 22))
    e.append(star(150, 180, 20))
    e.append(sparkle(1000, 280, 14))
    e.append(sparkle(200, 400, 12))
    return svg(W, H, "".join(e))

def scene_p4():
    """衝動頁：Owen 狂奔特寫（腿完整），耳朵兩側白色風漩渦，遠處小小的 Daddy 揮手喊話（語音泡泡 "Owen!" 字淡），紅色熱氣線
    (text: My legs go zoom, zoom! Wind fills my ears. I can not hear Daddy!)"""
    e = []
    # 深紫背景（衝動感）
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#E8D4F0"/>')
    # 紅色熱氣線（上下左右）
    for (x, y) in [(250, 120), (920, 130), (200, 420), (950, 410)]:
        e.append(f'<path d="M {x} {y} q 12 -18 24 0 q 12 18 24 0" fill="none" stroke="#F26B5E" stroke-width="10" stroke-linecap="round"/>')
    # Owen run 大特寫，cy=150 以確保腿在畫面內 (feet_y = 150 + 228*1.5 = 492 < 560)
    e.append(boy(pose="run", expr="star", cx=450, cy=150, scale=1.5, jersey=('0', '#57A863', '#2F7A44')))
    # 耳朵兩側白色風漩渦（螺旋線在耳朵附近）
    for ear_x in [450 - 100, 450 + 100]:  # 左右耳朵 (约 350, 550)
        for i in range(3):
            angle_start = i * 120
            for j in range(5):
                angle = math.radians(angle_start + j * 72)
                r_start = 30 + i * 20
                r_end = r_start + 25
                x1 = ear_x + r_start * math.cos(angle)
                y1 = 180 + r_start * math.sin(angle)  # 頭部高度約 180
                x2 = ear_x + r_end * math.cos(angle)
                y2 = 180 + r_end * math.sin(angle)
                e.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>')
    # 遠處小小的 Daddy 揮手，語音泡泡 "Owen!" 字淡
    e.append(daddy(cx=1000, cy=200, scale=0.6, pose="point", whistle=False))
    # 語音泡泡，字淡
    e.append(f'<ellipse cx="1000" cy="100" rx="70" ry="45" fill="#FFFFFF" stroke="#C9A26B" stroke-width="3"/>')
    e.append(f'<path d="M 970 130 L 920 160 L 960 135 Z" fill="#FFFFFF" stroke="#C9A26B" stroke-width="2"/>')
    e.append(svgtext(1000, 115, "Owen!", size=28, fill="#999999", weight="bold"))  # 淡色字
    return svg(W, H, "".join(e))

def scene_p5():
    """紫色星空背景：Owen（press 表情）站得直挺挺像雕像，周身冰藍色光暈＋雪花點綴（≤6），腳下小冰面
    (text: STOP! I use my superpower… I FREEZE like ice!)"""
    e = []
    # 深紫星空
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#2C1A4A"/>')
    # 雪花（≤6 個）
    for (x, y) in [(200, 150), (950, 200), (300, 380), (850, 320), (150, 500)]:
        e.append(f'<path d="M {x} {y-20} L {x} {y+20} M {x-17} {y-10} L {x+17} {y+10} M {x-17} {y+10} L {x+17} {y-10}" '
                 f'stroke="#E8F4F8" stroke-width="4" stroke-linecap="round"/>')
    # 冰藍光暈（在 Owen 之前畫，才不會蓋住手臂）
    for r in [160, 120, 80]:
        e.append(f'<circle cx="594" cy="280" r="{r}" fill="#A8D8F0" fill-opacity="0.15"/>')
    # 腳下冰面橢圓（淺藍）
    e.append(f'<ellipse cx="594" cy="480" rx="120" ry="30" fill="#A8D8F0" fill-opacity="0.4"/>')
    # Owen stand，press 表情（決心表情），中等尺寸
    e.append(boy(pose="stand", expr="press", cx=594, cy=280, scale=1.2, jersey=('0', '#57A863', '#2F7A44')))
    # 星星點綴（背景星空）
    for (x, y, r) in [(250, 100, 8), (1050, 130, 10), (180, 420, 7), (1000, 450, 9)]:
        e.append(star(x, y, r, fill="#A8D8F0", stroke="#7CBCE0", sw=2))
    return svg(W, H, "".join(e))

def scene_p6():
    """三步腳本圖：①哨子＋音符（聽到訊號）②冰藍色定格的 Owen ③Owen 眼睛視線虛線連到 Daddy
    (text: Whistle? My name? I freeze my body. I look and listen.)"""
    e = []
    # 冰藍背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#B8D8E8"/>')

    # 三個圓角矩形分格
    box_width = 340
    box_height = 380
    box_spacing = 60
    x_positions = [100, 100 + box_width + box_spacing, 100 + 2*(box_width + box_spacing)]

    for i, x_pos in enumerate(x_positions):
        # 圓角矩形
        e.append(f'<rect x="{x_pos}" y="80" width="{box_width}" height="{box_height}" rx="20" fill="#FFFFFF" stroke="#4A7A9E" stroke-width="4"/>')

        if i == 0:  # ① 哨子＋音符
            # 哨子
            e.append(f'<ellipse cx="{x_pos + box_width/2}" cy="200" rx="28" ry="24" fill="#F2B035" stroke="#C98A18" stroke-width="3"/>')
            e.append(f'<path d="M {x_pos + box_width/2 - 30} {180} Q {x_pos + box_width/2} {160} {x_pos + box_width/2 + 30} {180}" '
                     f'fill="none" stroke="#8A7460" stroke-width="3"/>')
            # 音符
            e.append(f'<circle cx="{x_pos + box_width/2 - 60}" cy="140" r="8" fill="#6FA8DC" stroke="#3D5A80" stroke-width="2"/>')
            e.append(f'<circle cx="{x_pos + box_width/2 - 30}" cy="120" r="8" fill="#6FA8DC" stroke="#3D5A80" stroke-width="2"/>')
            e.append(f'<path d="M {x_pos + box_width/2 - 52} {148} Q {x_pos + box_width/2 - 40} {110} {x_pos + box_width/2 - 22} {128}" '
                     f'fill="none" stroke="#6FA8DC" stroke-width="3"/>')
            # 標題數字
            e.append(svgtext(x_pos + box_width/2, 420, "1", size=48, fill="#4A7A9E", weight="bold"))

        elif i == 1:  # ② 冰藍定格 Owen
            # 冰藍光暈
            for r in [120, 90, 60]:
                e.append(f'<circle cx="{x_pos + box_width/2}" cy="220" r="{r}" fill="#A8D8F0" fill-opacity="0.2"/>')
            # Owen stand，小尺寸，press 表情
            e.append(boy(pose="stand", expr="press", cx=x_pos + box_width/2, cy=240, scale=0.85, jersey=('0', '#57A863', '#2F7A44')))
            # 冰藍描邊框
            e.append(f'<circle cx="{x_pos + box_width/2}" cy="240" r="140" fill="none" stroke="#A8D8F0" stroke-width="6"/>')
            e.append(svgtext(x_pos + box_width/2, 420, "2", size=48, fill="#4A7A9E", weight="bold"))

        else:  # ③ Owen 視線虛線連到 Daddy
            # Owen 小版本（看向右）
            e.append(boy(pose="stand", expr="smile", cx=x_pos + 60, cy=240, scale=0.8, jersey=('0', '#57A863', '#2F7A44')))
            # Daddy 小版本
            e.append(daddy(cx=x_pos + box_width - 60, cy=240, scale=0.7, pose="stand", whistle=False))
            # 視線虛線
            e.append(f'<line x1="{x_pos + 120}" y1="210" x2="{x_pos + box_width - 120}" y2="210" '
                     f'stroke="#4A7A9E" stroke-width="3" stroke-dasharray="8 6"/>')
            e.append(svgtext(x_pos + box_width/2, 420, "3", size=48, fill="#4A7A9E", weight="bold"))

    return svg(W, H, "".join(e))

def scene_p7():
    """觀點頁：Daddy 蹲下對小朋友們講解戰術板，Lucas 也定格站好在聽，安全感的柔色調
    (text: Daddy helps our team. Lucas freezes too. Listening keeps everyone safe.)"""
    e = []
    # 柔和黃色背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#E6D8C4"/>')
    # Daddy 蹲下講解（pose=stand 做蹲姿近似，調整位置）
    e.append(daddy(cx=300, cy=295, scale=1.1, pose="point", whistle=False))
    # 戰術板（簡單矩形＋線條）
    e.append(f'<rect x="450" y="160" width="240" height="200" rx="8" fill="#FFFFFF" stroke="#8A5A3C" stroke-width="4"/>')
    e.append(f'<circle cx="520" cy="220" r="18" fill="#6FA8DC"/>')  # 球
    e.append(f'<circle cx="600" cy="250" r="16" fill="#F49AB5"/>')  # 己隊
    e.append(f'<circle cx="660" cy="180" r="16" fill="#F49AB5"/>')
    e.append(f'<path d="M 520 220 L 600 250 M 600 250 L 660 180" stroke="#F26B5E" stroke-width="3" stroke-dasharray="5 3"/>')  # 傳球線
    # Lucas 站在右邊，定格，smile 表情
    e.append(lucas(cx=850, cy=320, scale=1.0, expr="smile"))
    # 語音泡泡："Go team!"（給 Lucas）
    e.append(f'<ellipse cx="850" cy="200" rx="90" ry="50" fill="#FFFFFF" stroke="#6FA8DC" stroke-width="3"/>')
    e.append(f'<path d="M 820 240 L 760 290 L 810 250 Z" fill="#FFFFFF" stroke="#6FA8DC" stroke-width="2"/>')
    e.append(svgtext(850, 210, "Go team!", size=28, fill="#3D5A80", weight="bold"))
    return svg(W, H, "".join(e))

def scene_p8():
    """高潮：Daddy 指向球門＋語音泡泡 "Owen, kick now!"；Owen 踢球（kick 姿勢），球飛進球網，GOAL 星爆
    (text: Daddy says, "Owen, kick now!" I listen. I kick… GOAL!)"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#E8D8C9"/>')
    # 草地（在人物之前）
    e.append(f'<rect x="0" y="320" width="1188" height="240" fill="#7BC87F"/>')
    # 球門（草地之後、人物之前）
    e.append(goal(cx=1000, cy=320, scale=1.0))
    # Daddy 在左側，指向球門
    e.append(daddy(cx=200, cy=280, scale=1.1, pose="point", whistle=False))
    # 語音泡泡
    e.append(f'<path d="M 300 80 Q 300 40 380 40 L 580 40 Q 640 40 640 100 Q 640 160 580 160 L 440 160 L 380 200 L 400 160 L 380 160 Q 300 160 300 100 Z" '
             f'fill="#FFFFFF" stroke="#C9A26B" stroke-width="4"/>')
    e.append(svgtext(450, 110, "Owen, kick now!", size=36, fill="#D97706", weight="bold"))
    # Owen 在中間，kick 姿勢，0 號球衣（cy=235 → 站立腳 feet_y = 235+228*1.2 ≈ 509，畫布內）
    e.append(boy(pose="kick", expr="big", cx=500, cy=235, scale=1.2, jersey=('0', '#57A863', '#2F7A44')))
    # 球在 Owen 腳尖（kick 公式：cx+72*scale, cy+160*scale）
    ball_x = 500 + 72*1.2
    ball_y = 235 + 160*1.2
    e.append(soccer_ball(cx=ball_x, cy=ball_y, r=26))
    # 球的虛線軌跡飛進球門
    goal_x = 1000
    goal_y = 320
    for i in range(6):
        t = i / 5.0
        x = ball_x + (goal_x - ball_x) * t
        y = ball_y + (goal_y - ball_y) * t
        e.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="#F2B035" opacity="0.4"/>')
    # GOAL 星爆（大字）
    e.append(svgtext(goal_x, 180, "GOAL!", size=72, fill="#E4574C", weight="bold"))
    # 星爆星星
    for (dx, dy, r) in [(-80, -100, 24), (80, -120, 20), (-120, -50, 18), (120, -80, 22), (0, -150, 26)]:
        e.append(star(goal_x + dx, goal_y + dy, r))
    return svg(W, H, "".join(e))

def scene_p9():
    """隊友們（Lucas＋不具名小孩）圍著 Owen 歡呼舉手，彩帶
    (text: My team cheers for me. Listening ears win games! I feel GREAT!)"""
    e = []
    # 彩色慶祝背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#F0D4E0"/>')
    # 彩帶（confetti）
    import random
    random.seed(42)
    cols = ["#F6C445", "#7BC47F", "#6FA8DC", "#F49AB5", "#E4574C"]
    for i in range(28):
        x, y = random.randint(40, 1148), random.randint(30, 250)
        c = cols[i % 5]
        e.append(f'<rect x="{x}" y="{y}" width="12" height="18" rx="4" fill="{c}" transform="rotate({random.randint(-40,40)} {x} {y})"/>')
    # Owen 在中央歡呼
    e.append(boy(pose="jump", expr="big", cx=594, cy=260, scale=1.2, jersey=('0', '#57A863', '#2F7A44')))
    # Lucas 在左邊舉手歡呼
    e.append(lucas(cx=250, cy=340, scale=1.0, expr="smile"))
    # Lucas 舉手（從肩膀出發）
    e.append(f'<path d="M 218 428 Q 190 330 200 256" stroke="#E8B98C" stroke-width="13" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="201" cy="246" r="11" fill="#E8B98C"/>')
    # Kid (variant=2) 在右邊舉手歡呼
    e.append(kid(variant=2, cx=930, cy=340, scale=1.0, expr="smile"))
    # Kid 舉手（從肩膀出發）
    e.append(f'<path d="M 962 428 Q 990 330 980 256" stroke="#FFD9B6" stroke-width="13" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="979" cy="246" r="11" fill="#FFD9B6"/>')
    # 星星點綴
    e.append(star(400, 150, 20))
    e.append(star(820, 180, 18))
    e.append(sparkle(150, 400, 12))
    e.append(sparkle(1050, 420, 14))
    return svg(W, H, "".join(e))

def scene_p10():
    """英雄收尾：Owen 披紅披風叉腰站在球場中圈，胸前 0 號，一腳踩足球，滿天星
    (text: Freeze! Look! Listen! Freeze and look! I practice every day!)"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#FFF0D0"/>')
    # 草地（在人物之前）
    e.append(f'<rect x="0" y="320" width="1188" height="240" fill="#7BC87F"/>')
    # 中圈（地面透視橢圓，在草地上、人物之前）
    e.append(f'<ellipse cx="594" cy="480" rx="230" ry="55" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-dasharray="12 10"/>')
    # 滿天星
    for (x, y, r) in [(180, 120, 20), (1040, 140, 24), (150, 400, 16), (1080, 380, 18), (350, 80, 14), (900, 100, 16), (250, 500, 12), (950, 480, 14)]:
        e.append(star(x, y, r))
    # Owen 英雄版：cape=True, pose='hips', jersey=0 號（cy=215 → feet_y = 215+228*1.3 ≈ 511，畫布內）
    e.append(boy(pose="hips", expr="proud", cx=594, cy=215, scale=1.3, cape=True, jersey=('0', '#57A863', '#2F7A44')))
    # 足球在右腳邊地面
    e.append(soccer_ball(cx=594 + 60, cy=505, r=30))
    return svg(W, H, "".join(e))

# ============================================================
# PAGE TEXTS
# ============================================================
PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I am number <b>0</b>. I love soccer!'),
    ("p2", scene_p2, 'Practice day!<br/>Daddy blows the <b>whistle</b>.<br/>We run and kick!'),
    ("p3", scene_p3, 'I chase the ball.<br/>Fast, fast, faster!<br/>This is SO fun!'),
    ("p4", scene_p4, 'My legs go zoom, zoom!<br/>Wind fills my ears.<br/>I can not hear Daddy!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I <b>FREEZE</b> like ice!'),
    ("p6", scene_p6, 'Whistle? My name?<br/>I freeze my body.<br/>I look and listen.'),
    ("p7", scene_p7, 'Daddy helps our team.<br/>Lucas freezes too.<br/>Listening keeps everyone safe.'),
    ("p8", scene_p8, 'Daddy says, &ldquo;<b>Owen</b>, kick now!&rdquo;<br/>I listen. I kick&hellip;<br/><b>GOAL!</b>'),
    ("p9", scene_p9, 'My team cheers for me.<br/>Listening ears win games!<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, '<b>Freeze! Look! Listen!</b><br/><b>Freeze and look!</b><br/>I practice every day!'),
]

PARENT_TIPS = [
    ("在家先玩木頭人／Freeze dance 遊戲",
     "哨音或叫名字＝定格挑戰。成功定格就大笑稱讚，讓 freeze 的肌肉記憶在低壓情境先長出來。"),
    ("出事後絕對不拿出來讀",
     "玩瘋的當下不讀，平靜時讀＋玩。一旦變成懲罰教材，這本書就報廢了。"),
    ("哨音不是處罰",
     "Freeze 之後永遠接「看＋聽＋繼續玩」，不要 freeze 完接罵人，否則這個開關會壞掉。"),
    ("當他主動說「Wind fills my ears」就大力稱讚",
     "這表示他察覺到自己 high 過頭了，那是最值得大力稱讚的自覺時刻。"),
    ("讀完玩 2 分鐘角色扮演",
     "你當 Daddy 吹哨子、他練「停下來 → 看 → 聽」；再交換角色。"),
    ("邀請他加工這本書",
     "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

BOOK = {
    "slug": "freeze-and-look",
    "order": 6,
    "title_pre": "", "title_hi": "Freeze", "title_post": " and Look!",
    "title_zh": "停下來，看！",
    "subtitle": "Owen's soccer story",
    "tagline_zh": "Owen 的足球故事",
    "chips": ["Social Story", "Soccer", "12 pages"],
    "pdf_name": "Freeze_And_Look.pdf",
    "bg": BG,
    "pages": PAGES,
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Freeze → Look → Listen!</b>&nbsp;"
                 "平時喊法是 &ldquo;<b>Freeze and look!</b>&rdquo;。"
                 "當他哪天主動說出 &ldquo;Wind fills my ears&rdquo;（我察覺到自己 high 過頭了），"
                 "就是最值得大力稱讚的時刻。"),
    "cover": scene_cover,
}
