# -*- coding: utf-8 -*-
"""Book 15: Ask First! — 先問一問（未出版）。安裝「先問→聽答案→手收好」的腳本。"""
from parts import *
from book_common import svg, svgtext, TXT, W, H
import math

# soft page palettes
BG = {
    "cover": "#FFF8F0", "p1": "#FFF3D6", "p2": "#FFF3D6", "p3": "#FFF3D6",
    "p4": "#FFE9D5", "p5": "#E6D5F8", "p6": "#FFF3D6", "p7": "#FFE8E0",
    "p8": "#FFF3D6", "p9": "#FFE8E0", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

# ============= HELPER FUNCTION: STORYBOOK =============
def storybook(cx, cy, scale=1.0, torn=False, taped=False, held=False):
    """Anne 的粉紅封面小書。
    torn=True：中間鋸齒裂縫（白底）
    taped=True：裂縫上貼米色膠帶（圓角，微斜）
    held=True：書貼在身體前方（用於 p2）
    """
    e = []
    book_w, book_h = 86, 110  # 書的寬高（scale=1 時）

    # 粉紅封面＋圓角＋封面小星星圖案
    e.append(f'<g transform="translate({cx},{cy}) scale({scale})">')
    e.append(f'<rect x="-{book_w/2}" y="-{book_h/2}" width="{book_w}" height="{book_h}" rx="8" fill="#F49AB5" stroke="#E87BA6" stroke-width="2"/>')
    # 封面星星圖案（小星星）
    e.append(f'<polygon points="{star_pts(-20, -30, 6)}" fill="#FFE9A8"/>')
    e.append(f'<polygon points="{star_pts(20, -25, 5)}" fill="#FFE9A8"/>')
    e.append(f'<polygon points="{star_pts(0, -10, 5.5)}" fill="#FFE9A8"/>')

    # 白色內頁側邊（厚度感）
    e.append(f'<rect x="{book_w/2-3}" y="-{book_h/2+2}" width="4" height="{book_h-4}" rx="2" fill="#FFFFFF"/>')

    if torn:
        # 鋸齒裂縫（白底路徑，書中央）——鋸齒往上下兩側
        zips = []
        for i in range(8):
            y_offset = -book_h/2 + i * book_h / 7
            if i % 2 == 0:
                zips.append(f"L {-4} {y_offset}")
                zips.append(f"L 4 {y_offset + 6}")
            else:
                zips.append(f"L 4 {y_offset}")
                zips.append(f"L -4 {y_offset + 6}")
        zips_path = " ".join(zips)
        e.append(f'<path d="M 0 -{book_h/2} {zips_path} L 0 {book_h/2}" fill="#FFFFFF" stroke="#E87BA6" stroke-width="1.5"/>')

    if taped:
        # 米色膠帶蓋住裂縫（圓角長條，微斜角度）
        e.append(f'<g transform="rotate(-8)">')
        e.append(f'<rect x="-12" y="-{book_h/2}" width="24" height="{book_h}" rx="6" fill="#D4C4B0" fill-opacity="0.75"/>')
        e.append(f'</g>')

    e.append(f'</g>')
    return "".join(e)


# ============= SCENES =============
def scene_cover():
    e = []
    # 暖色星星背景
    for (x, y, r) in [(150, 100, 18), (1030, 120, 22), (220, 420, 16), (980, 450, 20), (380, 80, 14), (820, 140, 16)]:
        e.append(star(x, y, r, fill=STAR_Y))
    e.append(sparkle(500, 150, 12)); e.append(sparkle(700, 380, 14))
    # 地面
    e.append(f'<ellipse cx="594" cy="640" rx="560" ry="120" fill="#FFDD7E"/>')
    # Owen 在左邊
    e.append(boy(pose="stand", expr="smile", cx=350, cy=280, scale=1.2))
    # Owen 右手臂扶住書（肩膀在 (350+40*1.2, 280+106*1.2) = (398, 407) 附近）
    e.append(f'<path d="M 398 407 L 480 320" stroke="{SKIN}" stroke-width="16" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="485" cy="315" r="11" fill="{SKIN}"/>')

    # Anne 在右邊抱著書
    e.append(anne(cx=750, cy=310, scale=1.15, expr="smile"))
    # Anne 左手臂扶住書（肩膀在 (750-30*1.15, 310+84*1.15) = (715, 407) 附近）
    e.append(f'<path d="M 715 407 L 640 320" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="635" cy="322" r="10" fill="{SKIN}"/>')

    # 完好的書在兩人之間，由雙方手臂扶住
    e.append(storybook(cx=560, cy=320, scale=0.9, torn=False, taped=False, held=False))
    return svg(1188, 620, "".join(e), bg=BG["cover"])

def scene_p1():
    """Owen 開心幫 Tr. Mina 抱一疊紙。"""
    e = []
    # 教室背景
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D4C5B0"/>')  # 地板
    # 黑板背景
    e.append(f'<rect x="180" y="80" width="600" height="280" rx="12" fill="#C9A26B"/>')
    e.append(f'<rect x="200" y="100" width="560" height="240" rx="8" fill="#3E7C5B"/>')
    # Owen 抱一疊紙（白色矩形疊 4 張，明顯分層）
    e.append(boy(pose="stand", expr="smile", cx=500, cy=240, scale=1.2))
    # 紙張堆（白色矩形疊層，明顯分層，放在 Owen 胸前）
    for i in range(4):
        offset_y = -50 + i * 18
        offset_x = -4 + i * 3
        e.append(f'<rect x="{380 + offset_x}" y="{240 + offset_y}" width="100" height="16" rx="3" fill="#FFFFFF" stroke="#D4D0CA" stroke-width="2"/>')
        # 紙張邊界陰影
        if i < 3:
            e.append(f'<line x1="{380 + offset_x}" y1="{256 + offset_y}" x2="{480 + offset_x}" y2="{256 + offset_y}" stroke="#A8A29A" stroke-width="1.5" opacity="0.7"/>')
    # Tr. Mina 在右側指向 Owen
    e.append(teacher(cx=900, cy=280, scale=1.0, point="left"))
    # 頭上愛心＋星星
    e.append(f'<path d="M 480 120 c 0 -15 22 -15 22 -1 c 0 -14 22 -14 22 1 c 0 15 -22 23 -22 30 c 0 -7 -22 -15 -22 -30 Z" fill="#F2665A" stroke="#D14A3F" stroke-width="2"/>')
    e.append(star(560, 90, 16))
    e.append(sparkle(440, 110, 10))
    return svg(W, H, "".join(e), bg=BG["p1"])

def scene_p2():
    """Anne 抱著她心愛的書（粉紅封面小書貼胸前）走過。"""
    e = []
    # 教室背景
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D4C5B0"/>')
    # 黑板
    e.append(f'<rect x="500" y="100" width="400" height="240" rx="12" fill="#C9A26B"/>')
    e.append(f'<rect x="520" y="120" width="360" height="200" rx="8" fill="#3E7C5B"/>')
    # Anne 抱著書（書在她胸前）
    e.append(anne(cx=350, cy=280, scale=1.15, expr="smile"))
    e.append(storybook(cx=350, cy=290, scale=0.9, torn=False, taped=False, held=True))
    # Owen 在左側看著 Anne
    e.append(boy_bust(expr="smile", cx=800, cy=320, scale=1.0))
    # 裝飾
    e.append(star(250, 150, 16)); e.append(sparkle(900, 200, 12))
    return svg(W, H, "".join(e), bg=BG["p2"])

def scene_p3():
    """Owen 特寫看著 Anne 的書，雙手已微微伸出，頭上思考泡泡。"""
    e = []
    # 教室背景
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D4C5B0"/>')
    # 大發光燈泡（思考）在上方
    e.append(f'<circle cx="594" cy="100" r="72" fill="{STAR_Y}" fill-opacity="0.22"/>')
    e.append(f'<circle cx="594" cy="100" r="50" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="4"/>')
    e.append(f'<rect x="574" y="152" width="40" height="18" rx="6" fill="#C9BFA8"/>')
    # Owen bust 特寫（看著書，star 表情）
    e.append(boy_bust(expr="star", cx=594, cy=330, scale=1.3))
    # 雙手微微伸出的感覺（從 bust 兩側伸出來）
    e.append(f'<path d="M 520 350 Q 450 360 420 380" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="415" cy="385" r="9" fill="{SKIN}"/>')
    e.append(f'<path d="M 668 350 Q 740 360 770 380" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="775" cy="385" r="9" fill="{SKIN}"/>')
    # 思考泡泡（大泡泡＋尾巴，在 Owen 上方右側）
    e.append(f'<ellipse cx="800" cy="160" rx="90" ry="55" fill="#F5FBFF" stroke="#B9CFE8" stroke-width="4"/>')
    # 泡泡尾巴指向 Owen 頭部
    e.append(f'<path d="M 720 200 L 660 250 L 680 220 Z" fill="#F5FBFF" stroke="#B9CFE8" stroke-width="3"/>')
    # 內部小圓點（思考泡泡經典圖案）
    e.append(f'<circle cx="740" cy="170" r="8" fill="#E0F0F8"/>')
    e.append(f'<circle cx="840" cy="155" r="7" fill="#E0F0F8"/>')
    e.append(f'<circle cx="800" cy="210" r="6" fill="#E0F0F8"/>')
    # 裝飾星星
    e.append(star(350, 240, 18)); e.append(star(850, 260, 20)); e.append(sparkle(280, 120, 10))
    return svg(W, H, "".join(e), bg=BG["p3"])

def scene_p4():
    """衝動頁：Owen 與 Anne 拉書，書在兩人中間胸口高度，兩側手臂線拉力明顯；鋸齒裂縫＋RIP!；角落小格隊伍推人。"""
    e = []
    # 教室背景
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D4C5B0"/>')
    # 熱氣波紋
    for (x, y) in [(250, 120), (900, 140), (220, 300), (920, 320)]:
        e.append(f'<path d="M {x} {y} q 12 -16 24 0 q 12 16 24 0" fill="none" stroke="#F26B5E" stroke-width="7" stroke-linecap="round"/>')

    # Owen 在左側（標準站姿）
    e.append(boy(pose="stand", expr="oh", cx=300, cy=250, scale=1.2))
    # Owen 左手臂線從肩膀（約 340, 330）伸到書左邊
    e.append(f'<path d="M 340 330 L 520 300" stroke="{SKIN}" stroke-width="16" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="525" cy="297" r="11" fill="{SKIN}"/>')

    # Anne 在右側
    e.append(anne(cx=870, cy=290, scale=1.15, expr="oh"))
    # Anne 右手臂線從肩膀（約 840, 375）伸到書右邊
    e.append(f'<path d="M 840 375 L 720 300" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="715" cy="302" r="10" fill="{SKIN}"/>')

    # 書在中間（胸口高度，y ≈ 300）
    book_cx, book_cy = 620, 300
    book_scale = 1.0
    e.append(storybook(cx=book_cx, cy=book_cy, scale=book_scale, torn=True, taped=False, held=False))

    # 拉力短線（書兩側各 2 條反向短線）
    # 左側拉力線（Owen 拉）
    e.append(f'<line x1="540" y1="295" x2="560" y2="280" stroke="#F26B5E" stroke-width="5" stroke-linecap="round"/>')
    e.append(f'<line x1="540" y1="305" x2="560" y2="320" stroke="#F26B5E" stroke-width="5" stroke-linecap="round"/>')
    # 右側拉力線（Anne 拉）
    e.append(f'<line x1="700" y1="295" x2="680" y2="280" stroke="#F26B5E" stroke-width="5" stroke-linecap="round"/>')
    e.append(f'<line x1="700" y1="305" x2="680" y2="320" stroke="#F26B5E" stroke-width="5" stroke-linecap="round"/>')

    # RIP! 大字效（書上方）
    e.append(svgtext(620, 180, "RIP!", size=56, fill="#E4574C", weight="bold"))

    # 速度線（軀幹高度）
    for i in range(4):
        x_start = 380 + i * 50
        e.append(f'<line x1="{x_start}" y1="290" x2="{x_start + 70}" y2="290" stroke="#F26B5E" stroke-width="6" stroke-linecap="round" fill-opacity="0.7"/>')

    # 右下角小格：隊伍裡 Owen 推 Anne（小尺寸人物＋oops 星號）
    e.append(f'<rect x="900" y="380" width="230" height="140" rx="12" fill="#FFFFFF" stroke="#D4C5B0" stroke-width="3"/>')
    # 隊伍裡的小 Owen 推人姿勢
    e.append(boy(pose="stand", expr="oh", cx=950, cy=430, scale=0.7))
    # 隊伍裡的小 Anne 被推
    e.append(anne(cx=1050, cy=450, scale=0.7, expr="oh"))
    # Oops 星號
    e.append(f'<polygon points="{star_pts(1020, 380, 18)}" fill="#F2B2A8" stroke="#E4574C" stroke-width="2"/>')

    return svg(W, H, "".join(e), bg=BG["p4"])

def scene_p5():
    """紫星空＋Owen bust arms='desk'＋面前發光問號。"""
    e = []
    # 紫色星空
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#E6D5F8"/>')
    for (x, y, r) in [(120, 80, 16), (1050, 100, 20), (180, 420, 14), (1020, 440, 18), (400, 60, 12), (800, 440, 14)]:
        e.append(star(x, y, r, fill=STAR_Y))
    e.append(sparkle(280, 150, 10)); e.append(sparkle(900, 160, 12)); e.append(sparkle(140, 350, 10)); e.append(sparkle(1080, 350, 10))

    # 地面
    e.append(f'<ellipse cx="594" cy="536" rx="100" ry="20" fill="#C9BBE8"/>')

    # Owen bust press 表情，雙手收胸前（arms='desk'）
    e.append(boy_bust(expr="press", cx=380, cy=340, scale=1.2, arms="desk"))

    # 面前發光問號泡泡（大「?」svgtext＋金色光暈圈）
    e.append(f'<circle cx="750" cy="220" r="80" fill="{STAR_Y}" fill-opacity="0.18"/>')
    e.append(f'<circle cx="750" cy="220" r="60" fill="{STAR_Y}" fill-opacity="0.22"/>')
    e.append(svgtext(750, 250, "?", size=120, fill=STAR_Y, weight="bold"))

    return svg(W, H, "".join(e), bg=None)

def scene_p6():
    """三步腳本三格：①語音泡泡②綠勾/紅叉②Owen bust 收好手。"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#FFF3D6"/>')
    e.append(f'<rect x="0" y="480" width="1188" height="80" fill="#BFD9EE"/>')

    # ① 大語音泡泡「Can I help?」（左上）
    bubble_x, bubble_y = 280, 140
    e.append(f'<ellipse cx="{bubble_x}" cy="{bubble_y}" rx="140" ry="60" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="4"/>')
    e.append(f'<path d="M {bubble_x-80} {bubble_y+60} L {bubble_x-60} {bubble_y+100} L {bubble_x-40} {bubble_y+60} Z" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')
    e.append(svgtext(bubble_x, bubble_y+10, "Can I help?", size=36, fill="#4A78A8", weight="bold"))

    # ② 綠勾「Yes」& 紅叉「No」圖示（中上）
    yes_x, no_x = 400, 580
    yes_y = no_y = 200
    # YES 綠色圓＋勾
    e.append(f'<circle cx="{yes_x}" cy="{yes_y}" r="40" fill="#7BC47F" stroke="#5A9C5F" stroke-width="3"/>')
    e.append(f'<path d="M {yes_x-15} {yes_y+5} L {yes_x+5} {yes_y+20} L {yes_x+20} {yes_y-10}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    # NO 紅色圓＋叉
    e.append(f'<circle cx="{no_x}" cy="{no_y}" r="40" fill="#E4574C" stroke="#C83C2C" stroke-width="3"/>')
    e.append(f'<path d="M {no_x-15} {no_y-15} L {no_x+15} {no_y+15}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>')
    e.append(f'<path d="M {no_x+15} {no_y-15} L {no_x-15} {no_y+15}" fill="none" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round"/>')

    # ③ Owen bust 雙手收好（arms='desk'）微笑站在 Anne 旁
    e.append(boy_bust(expr="smile", cx=450, cy=380, scale=1.0, arms="desk"))
    e.append(anne(cx=680, cy=390, scale=0.95, expr="smile"))

    # 裝飾星星
    e.append(star(150, 300, 14)); e.append(sparkle(950, 250, 12))

    return svg(W, H, "".join(e), bg=None)

def scene_p7():
    """観點頁：Anne 抱完好書微笑＋Owen 微笑＋中間愛心。"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#FFE8E0"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D4C5B0"/>')

    # Anne 左側抱著完好的書，微笑
    e.append(anne(cx=350, cy=280, scale=1.15, expr="smile"))
    e.append(storybook(cx=350, cy=290, scale=0.9, torn=False, taped=False, held=True))

    # Owen 右側微笑
    e.append(boy(pose="stand", expr="smile", cx=820, cy=240, scale=1.2))

    # 兩人之間一顆紅色愛心
    heart_cx = 594
    heart_cy = 200
    e.append(f'<path d="M {heart_cx} {heart_cy} c 0 -24 36 -24 36 -2 c 0 -22 36 -22 36 2 c 0 24 -36 37 -36 48 c 0 -11 -36 -24 -36 -48 Z" fill="#F2665A" stroke="#D14A3F" stroke-width="3"/>')

    # 裝飾星星
    e.append(star(200, 140, 16)); e.append(star(1000, 160, 18)); e.append(sparkle(280, 380, 12))

    return svg(W, H, "".join(e), bg=None)

def scene_p8():
    """修復場景：Owen 與 Anne 用膠帶黏書，Tr. Mina 遞膠帶；兩個語音泡泡。"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#FFF3D6"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D4C5B0"/>')

    # 桌面（中央）
    e.append(desk(cx=594, cy=440, w=280, scale=1.1))

    # 修復後的書（貼上膠帶）在桌上
    e.append(storybook(cx=594, cy=360, scale=1.0, torn=True, taped=True, held=False))

    # Owen 在桌後左側（bust），語音泡泡「Sorry, Anne!」
    e.append(boy_bust(expr="smile", cx=350, cy=300, scale=1.0))
    bubble_ox, bubble_oy = 280, 160
    e.append(f'<ellipse cx="{bubble_ox}" cy="{bubble_oy}" rx="110" ry="50" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')
    e.append(f'<path d="M {bubble_ox-50} {bubble_oy+50} L {bubble_ox-30} {bubble_oy+85} L {bubble_ox-10} {bubble_oy+50} Z" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="2.5"/>')
    e.append(svgtext(bubble_ox, bubble_oy+5, "Sorry,", size=28, fill="#4A78A8", weight="bold"))
    e.append(svgtext(bubble_ox, bubble_oy+35, "Anne!", size=28, fill="#4A78A8", weight="bold"))

    # Anne 在桌後右側（bust），語音泡泡「Thank you, Owen!」
    e.append(anne(cx=820, cy=300, scale=1.0, expr="smile"))
    bubble_ax, bubble_ay = 900, 160
    e.append(f'<ellipse cx="{bubble_ax}" cy="{bubble_ay}" rx="120" ry="50" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="3"/>')
    e.append(f'<path d="M {bubble_ax+50} {bubble_ay+50} L {bubble_ax+30} {bubble_ay+85} L {bubble_ax+10} {bubble_ay+50} Z" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="2.5"/>')
    e.append(svgtext(bubble_ax, bubble_ay+5, "Thank you,", size=26, fill="#4A78A8", weight="bold"))
    e.append(svgtext(bubble_ax, bubble_ay+35, "Owen!", size=26, fill="#4A78A8", weight="bold"))

    # Tr. Mina 在桌右側（scale≥1.0 讓大人比小孩高），point="left" 指向書方向
    e.append(teacher(cx=960, cy=300, scale=1.1, point="left"))
    # 膠帶捲（donut 圓環）貼在 Tr. Mina 指向的手上：point='left' 手在 (-100,46)*1.1 → (850, 351)
    e.append(f'<circle cx="850" cy="352" r="16" fill="none" stroke="#D4C4B0" stroke-width="9"/>')
    e.append(f'<circle cx="850" cy="352" r="7" fill="#FFF7E6"/>')

    return svg(W, H, "".join(e), bg=None)

def scene_p9():
    """Owen 與 Anne 並肩坐看貼膠帶的書＋頭上小愛心與星星。"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="0" width="1188" height="560" fill="#FFE8E0"/>')
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#D4C5B0"/>')

    # 桌面
    e.append(desk(cx=594, cy=440, w=340, scale=1.15))

    # Owen 與 Anne 並肩坐（用 bust 靠近桌後）
    e.append(boy_bust(expr="smile", cx=420, cy=330, scale=1.0, arms="desk"))
    e.append(anne(cx=750, cy=330, scale=1.0, expr="smile"))

    # 攤開的書（兩頁矩形呈 V 形＋膠帶痕）
    book_left_x = 520
    book_right_x = 650
    book_y = 280
    # 左頁
    e.append(f'<path d="M {book_left_x} {book_y-40} L {book_left_x-35} {book_y-40} L {book_left_x-35} {book_y+50} L {book_left_x} {book_y+50} Z" fill="#FFFFFF" stroke="#E87BA6" stroke-width="2"/>')
    # 右頁
    e.append(f'<path d="M {book_right_x} {book_y-40} L {book_right_x+35} {book_y-40} L {book_right_x+35} {book_y+50} L {book_right_x} {book_y+50} Z" fill="#FFFFFF" stroke="#E87BA6" stroke-width="2"/>')
    # 膠帶痕（米色半透明線）
    e.append(f'<rect x="{book_left_x-8}" y="{book_y-35}" width="16" height="85" rx="4" fill="#D4C4B0" fill-opacity="0.4"/>')

    # 頭上小愛心與星星
    e.append(f'<path d="M 450 180 c 0 -12 18 -12 18 -1 c 0 -11 18 -11 18 1 c 0 12 -18 19 -18 24 c 0 -5 -18 -12 -18 -24 Z" fill="#F2665A" stroke="#D14A3F" stroke-width="1.5"/>')
    e.append(star(520, 160, 14))
    e.append(star(680, 170, 12)); e.append(sparkle(750, 140, 10))

    return svg(W, H, "".join(e), bg=None)

def scene_p10():
    """英雄收尾：Owen handup+cape＋舉發光問號牌＋Anne 比讚＋滿天星。"""
    e = []
    # 背景＋地面
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="110" fill="#FFDD7E"/>')
    for (x, y, r) in [(140, 100, 20), (1040, 110, 24), (100, 380, 16), (1080, 400, 18), (320, 60, 14), (880, 80, 16)]:
        e.append(star(x, y, r))
    e.append(sparkle(260, 280, 12)); e.append(sparkle(950, 280, 12))

    # Owen handup + cape
    e.append(boy(pose="handup", expr="proud", cx=480, cy=180, scale=1.3, cape=True))

    # 舉起的手位置畫發光問號牌（手在 (cx+74s, cy-94s)）
    hand_x = 480 + 74 * 1.3
    hand_y = 180 - 94 * 1.3
    # 問號牌：圓角矩形＋大「?」
    e.append(f'<rect x="{hand_x-36}" y="{hand_y-44}" width="72" height="88" rx="10" fill="#FFE9A8" stroke="{STAR_DK}" stroke-width="3"/>')
    e.append(svgtext(hand_x, hand_y+14, "?", size=72, fill=STAR_DK, weight="bold"))

    # Anne 在右邊（雙手身側揮手——比讚）
    e.append(anne(cx=760, cy=240, scale=1.2, expr="smile"))
    # Anne 的右手臂線（從肩膀出發往下揮）——身側比讚
    # Anne 肩膀在 (760+30*1.2, 240+84*1.2) = (796, 341)
    e.append(f'<path d="M 796 341 L 830 380" stroke="{SKIN}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="835" cy="385" r="10" fill="{SKIN}"/>')
    # 豎起大拇指姿勢（拇指向上）
    e.append(f'<path d="M 835 385 L 835 320" stroke="{SKIN}" stroke-width="12" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="835" cy="315" r="11" fill="{SKIN}"/>')

    # Anne 的左手臂線（另一側比讚）
    e.append(f'<path d="M 724 341 L 690 380" stroke="{SKIN}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="685" cy="385" r="10" fill="{SKIN}"/>')
    e.append(f'<path d="M 685 385 L 685 320" stroke="{SKIN}" stroke-width="12" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="685" cy="315" r="11" fill="{SKIN}"/>')

    return svg(W, H, "".join(e), bg=None)

# ============= PAGE TEXTS ================
PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I love to help!'),
    ("p2", scene_p2, 'Anne has her favorite book.<br/>She holds it tight.'),
    ("p3", scene_p3, 'I want to help!<br/>I want to <b>carry</b> it for her!'),
    ("p4", scene_p4, 'My hands jump first, hot and fast!<br/>I pull. Anne pulls. <b>RIP!</b><br/>In line, my hands push too.'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I ask <b>FIRST</b>!'),
    ("p6", scene_p6, 'I say, &ldquo;Can I help?&rdquo;<br/>Yes means I help.<br/>No means hands to myself.'),
    ("p7", scene_p7, 'Anne can say no.<br/>Her book, her choice.<br/>No still means we are friends.'),
    ("p8", scene_p8, 'I say, &ldquo;Sorry, Anne!&rdquo;<br/>We <b>tape</b> the book together.<br/>Anne smiles. &ldquo;Thank you, <b>Owen</b>!&rdquo;'),
    ("p9", scene_p9, 'The book is happy again.<br/>We read it together.<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Ask first. Listen.<br/>Hands to myself!<br/><b>Ask first!</b> I practice every day!'),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "本書源自真實事件。<b>事發當天與隔天都不要讀</b>——等完全平靜的日子當新故事引入，否則會變成羞辱教材。"),
    ("保住幫忙的心", "討論時永遠先肯定「你想幫 Anne 是很棒的心意」，再談「先問一問」——把「幫忙」跟「先問」綁在一起。"),
    ("練「聽到 No」遊戲", "在家玩「Can I help?」遊戲，大人故意輪流回答 Yes 和 No——練習聽到 No 時把手收胸前說 \"OK!\"，聽到 No 不炸就大力稱讚。"),
    ("修復劇本可重演", "當他主動說 &ldquo;My hands jump first&rdquo; 或動手前先問 = 覺察里程碑，大力稱讚；p8 的修復劇本（Sorry → 一起修 → 和好）可在任何弄壞東西的場合重演。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

BOOK = {
    "slug": "ask-first",
    "order": 15,
    "title_pre": "", "title_hi": "Ask", "title_post": " First!",
    "title_zh": "先問一問",
    "subtitle": "Owen's helping story",
    "tagline_zh": "Owen 的幫忙故事",
    "chips": ["Social Story", "School", "13 pages"],
    "pdf_name": "Ask_First.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ['rip', 'tape', 'carry'],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Ask first &rarr; Listen &rarr; Hands to myself!</b>&nbsp;"
                 "當他哪天主動說 &ldquo;My hands jump first&rdquo;（我察覺到衝動了）或動手前先問了一句，"
                 "就是最值得大力稱讚的時刻。"),
    "cover": scene_cover,
}
