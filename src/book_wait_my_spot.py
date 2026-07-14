# -*- coding: utf-8 -*-
"""Book 2: I Can Wait My Spot! — 排隊時不插隊（社會故事繪本）。"""
from parts import *
from book_common import svg, svgtext, TXT, W, H
import math

# soft page palettes
BG = {
    "cover": "#FFF5E6", "p1": "#E8F4F8", "p2": "#FFF9E6", "p3": "#FFE8D6",
    "p4": "#FFEAE8", "p5": "#E6D9F8", "p6": "#F0E6FF", "p7": "#DFF7EB",
    "p8": "#FFF3D6", "p9": "#FFEDEE", "p10": "#FFF5E6", "p11": "#FBF4E8",
}

# JERSEY 常數
JERSEY_39 = ('39', '#F28C3A', '#C05A1E')

# ============ SCENES ============

def scene_cover():
    """封面：Owen 中央偏左抱著籃球（白 T），媽媽 April 在右側房子旁完整站立拿車鑰匙"""
    e = []
    e.append(sun(1050, 110, 38))
    e.append(cloud(200, 90, 1.0)); e.append(cloud(700, 70, 0.8))
    # 星星點綴
    for (x, y, r) in [(240, 200, 20), (950, 250, 22), (420, 140, 14), (850, 380, 16), (150, 450, 16)]:
        e.append(star(x, y, r))
    e.append(sparkle(580, 110, 12)); e.append(sparkle(300, 380, 10))
    # 家門：簡單房子（右側）
    e.append(f'<rect x="820" y="280" width="280" height="200" rx="10" fill="#F5DCC9" stroke="#D4A57A" stroke-width="4"/>')
    e.append(f'<polygon points="820,280 960,180 1100,280" fill="#E8574C"/>')
    e.append(f'<rect x="880" y="340" width="60" height="80" rx="4" fill="#BEE3F2"/>')
    e.append(f'<rect x="1020" y="340" width="60" height="80" rx="4" fill="#BEE3F2"/>')
    e.append(f'<rect x="960" y="420" width="50" height="60" rx="6" fill="#8B5E52"/>')
    # ground
    e.append(f'<ellipse cx="594" cy="640" rx="560" ry="120" fill="#FFDD7E"/>')
    # Owen 中央偏左，白 T + 籃球（重心在 cx=320）
    e.append(boy(pose="stand", expr="big", cx=320, cy=240, scale=1.15, jersey=None))
    e.append(basketball(cx=320, cy=290, r=28))
    # 媽媽 April 右側房子旁，完整站立（拉開距離避免重疊，重心在 cx=680）
    e.append(april(cx=680, cy=280, scale=1.15, pose="stand"))
    # April 手拿著鑰匙
    e.append(f'<path d="M 730 210 L 760 170" stroke="#FFD34D" stroke-width="8" stroke-linecap="round"/>')
    e.append(f'<circle cx="765" cy="165" r="12" fill="#FFD34D" stroke="#E8A20C" stroke-width="3"/>')
    # 音符
    e.append(f'<text x="180" y="140" font-family="Arial" font-size="48" fill="#FFB700">♪</text>')
    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """p1：Owen 白 T-shirt 抱著籃球站在家門口，媽媽 April 在旁邊拿車鑰匙，頭上音符與星星"""
    e = []
    e.append(sun(1050, 90, 36))
    e.append(cloud(180, 80, 1.0)); e.append(cloud(650, 60, 0.7))
    # 地面
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#BFE3B4"/>')
    e.append(f'<path d="M 0 560 Q 594 400 1188 560 L 1188 560 L 0 560 Z" fill="#EED9A8"/>')
    # 家門背景
    e.append(f'<rect x="750" y="260" width="280" height="200" rx="10" fill="#F5DCC9" stroke="#D4A57A" stroke-width="4"/>')
    e.append(f'<polygon points="750,260 890,170 1030,260" fill="#E8574C"/>')
    e.append(f'<rect x="810" y="320" width="60" height="80" rx="4" fill="#BEE3F2"/>')
    e.append(f'<rect x="950" y="320" width="60" height="80" rx="4" fill="#BEE3F2"/>')
    e.append(f'<rect x="890" y="400" width="50" height="60" rx="6" fill="#8B5E52"/>')
    # 灌木
    e.append(f'<circle cx="80" cy="430" r="40" fill="#8FCB84"/><circle cx="130" cy="440" r="30" fill="#79BD6E"/>')
    # April 拿鑰匙（位置更靠右邊，更靠近房子）
    e.append(april(cx=580, cy=280, scale=1.1, pose="stand"))
    e.append(f'<path d="M 650 210 L 680 170" stroke="#FFD34D" stroke-width="8" stroke-linecap="round"/>')  # 鑰匙
    e.append(f'<circle cx="685" cy="165" r="12" fill="#FFD34D" stroke="#E8A20C" stroke-width="3"/>')
    # Owen 抱著籃球（位置靠左邊）
    e.append(boy(pose="stand", expr="smile", cx=300, cy=220, scale=1.1, jersey=None))
    e.append(basketball(cx=300, cy=270, r=26))
    # 星星和音符
    e.append(star(180, 140, 18))
    e.append(sparkle(480, 110, 12))
    e.append(f'<text x="650" y="160" font-family="Arial" font-size="42" fill="#FFB700">♪</text>')
    return svg(W, H, "".join(e))


def scene_p2():
    """p2：球場：籃框在右側，Owen（39 號球衣）排在隊伍最後，前面是 Lucas（持球準備上籃）和 Anne"""
    e = []
    # 球場地板線
    e.append(f'<rect x="0" y="460" width="1188" height="100" fill="#D4A574"/>')
    e.append(f'<line x1="0" y1="480" x2="1188" y2="480" stroke="#FFFFFF" stroke-width="4"/>')
    # 籃框右邊（中心點高度約 180，柱子自行繪製）
    e.append(f'<rect x="1050" y="390" width="12" height="110" fill="#8B5E52"/>')  # 柱子
    e.append(hoop(cx=1056, cy=390, scale=1.1))
    # 隊伍排列（左到右）：Lucas > Anne > Owen
    e.append(lucas(cx=300, cy=310, scale=1.15, expr="smile"))
    e.append(f'<circle cx="320" cy="240" r="24" fill="#E8823C" stroke="#B85E22" stroke-width="2"/>')  # Lucas 持球
    e.append(ann(cx=550, cy=310, scale=1.15, expr="smile"))
    e.append(boy(pose="stand", expr="smile", cx=800, cy=310, scale=1.15, jersey=JERSEY_39))
    # 數字標示
    e.append(f'<circle cx="300" cy="100" r="24" fill="#FFFFFF" stroke="#4A78A8" stroke-width="4"/>')
    e.append(svgtext(300, 120, "1", size=32, fill="#4A78A8", weight="bold"))
    e.append(f'<circle cx="550" cy="100" r="24" fill="#FFFFFF" stroke="#4A78A8" stroke-width="4"/>')
    e.append(svgtext(550, 120, "2", size=32, fill="#4A78A8", weight="bold"))
    e.append(f'<circle cx="800" cy="100" r="24" fill="#FFFFFF" stroke="#F28C3A" stroke-width="4"/>')
    e.append(svgtext(800, 120, "3", size=32, fill="#F28C3A", weight="bold"))
    return svg(W, H, "".join(e))


def scene_p3():
    """p3：Owen 半身特寫（星星眼），視線越過前面的人盯著籃框，籃框上方發光"""
    e = []
    # 籃框特寫（上方小圖）
    e.append(f'<circle cx="950" cy="140" r="80" fill="{STAR_Y}" fill-opacity="0.22"/>')
    e.append(f'<circle cx="950" cy="140" r="50" fill="{STAR_Y}" fill-opacity="0.18"/>')
    e.append(hoop(cx=950, cy=140, scale=0.9))
    # 視線箭頭
    e.append(f'<path d="M 420 280 Q 650 200 900 160" fill="none" stroke="#F28C3A" stroke-width="6" stroke-dasharray="8 8" stroke-linecap="round"/>')
    e.append(f'<polygon points="900,160 920,150 910,175" fill="#F28C3A"/>')
    # Owen 特寫（星星眼）
    e.append(boy_bust(expr="star", cx=420, cy=350, scale=1.3, jersey=JERSEY_39))
    # 星星點綴
    e.append(star(200, 240, 20))
    e.append(star(700, 420, 22))
    e.append(sparkle(120, 120, 12))
    e.append(sparkle(1050, 320, 14))
    return svg(W, H, "".join(e))


def scene_p4():
    """p4：**衝動頁**：全身 Owen（鼓臉表情），雙腳清晰可見，雙腳下方/兩側彈簧線+速度線，四周紅色熱氣線、跳動的心臟"""
    e = []
    # 熱氣線（四周蛇形）
    for (x, y) in [(200, 150), (980, 160), (180, 400), (1010, 390)]:
        e.append(f'<path d="M {x} {y} q 12 -18 24 0 q 12 18 24 0" fill="none" stroke="#F26B5E" stroke-width="10" stroke-linecap="round"/>')
    # 全身 Owen（stand 姿勢，鼓臉表情，39 號球衣）
    # 落地計算：feet_y = cy + 228*scale；使用 cy=180, scale=1.3 → feet_y ≈ 476
    e.append(boy(pose="stand", expr="hold", cx=594, cy=180, scale=1.3, jersey=JERSEY_39))
    # 雙腳底部約在 y=476；彈簧線在腳下方（y=485+）
    feet_y = 180 + 228 * 1.3
    # 彈簧線：左腳（約 cx=470）、右腳（約 cx=720）
    e.append(f'<path d="M 470 {feet_y+12} q 0 -16 10 -16 q 10 0 10 16" stroke="#4C5445" stroke-width="7" fill="none" stroke-linecap="round"/>')
    e.append(f'<path d="M 720 {feet_y+12} q 0 -16 10 -16 q 10 0 10 16" stroke="#4C5445" stroke-width="7" fill="none" stroke-linecap="round"/>')
    # 速度線（腳邊向外散射）
    for dy in range(-12, 16, 8):
        e.append(f'<line x1="440" y1="{feet_y+4+dy}" x2="400" y2="{feet_y+4+dy}" stroke="#F26B5E" stroke-width="6" stroke-linecap="round"/>')
        e.append(f'<line x1="750" y1="{feet_y+4+dy}" x2="790" y2="{feet_y+4+dy}" stroke="#F26B5E" stroke-width="6" stroke-linecap="round"/>')
    # 小星星點綴（腳邊）
    e.append(star(380, feet_y-8, 14))
    e.append(star(810, feet_y, 14))
    # 跳動心臟（左側）
    e.append(f'<path d="M 200 280 c 0 -30 44 -30 44 -2 c 0 -28 44 -28 44 2 c 0 30 -44 46 -44 60 c 0 -14 -44 -30 -44 -60 Z" fill="#F2665A" stroke="#D14A3F" stroke-width="4"/>')
    e.append(f'<path d="M 178 328 q -16 0 -20 -14 M 310 328 q 16 0 20 -14" fill="none" stroke="#D14A3F" stroke-width="6" stroke-linecap="round"/>')
    return svg(W, H, "".join(e))


def scene_p5():
    """p5：紫色星空背景：Owen（press 表情）站立，雙腳底下畫金色膠水黏在發光的圓形「spot」上"""
    e = []
    # 星空背景（已有紫色 BG，加星星點綴）
    for (x, y, r) in [(120, 130, 18), (1050, 140, 20), (180, 420, 14), (1080, 410, 16)]:
        e.append(star(x, y, r, fill=STAR_Y))
    e.append(sparkle(320, 80, 12))
    e.append(sparkle(880, 90, 12))
    e.append(sparkle(100, 320, 10))
    e.append(sparkle(1100, 300, 10))
    # 腳下的發光 SPOT（金色多層半透明圓）
    e.append(f'<circle cx="594" cy="520" r="78" fill="{STAR_Y}" fill-opacity="0.25"/>')
    e.append(f'<circle cx="594" cy="520" r="60" fill="{STAR_Y}" fill-opacity="0.30"/>')
    e.append(f'<circle cx="594" cy="520" r="42" fill="{STAR_Y}" fill-opacity="0.35"/>')
    e.append(f'<circle cx="594" cy="520" r="28" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="3"/>')
    # 膠水線條（雙腳→SPOT）
    e.append(f'<path d="M 470 450 Q 520 490 550 515" fill="none" stroke="{STAR_Y}" stroke-width="6" stroke-dasharray="4 4" stroke-linecap="round"/>')
    e.append(f'<path d="M 720 450 Q 670 490 640 515" fill="none" stroke="{STAR_Y}" stroke-width="6" stroke-dasharray="4 4" stroke-linecap="round"/>')
    # Owen 站立（press 表情 = 決定表情）
    e.append(boy(pose="stand", expr="press", cx=594, cy=270, scale=1.2, jersey=JERSEY_39))
    return svg(W, H, "".join(e))


def scene_p6():
    """p6：Owen 站在隊伍中，腳下金色 spot 圓圈，舉手幫 Lucas 加油，胸前 1/2 圓圈泡泡數前面的人"""
    e = []
    # 地板
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#BFE3C2"/>')
    # 隊伍：Lucas（左側）、Anne（中）、Owen（右側舉手）
    e.append(lucas(cx=280, cy=310, scale=1.0, expr="smile"))
    e.append(ann(cx=560, cy=310, scale=1.0, expr="smile"))
    # Owen 舉手（handup 動作）
    e.append(boy(pose="handup", expr="press", cx=820, cy=270, scale=1.15, jersey=JERSEY_39))
    # 腳下 SPOT
    e.append(f'<circle cx="820" cy="520" r="62" fill="{STAR_Y}" fill-opacity="0.28"/>')
    e.append(f'<circle cx="820" cy="520" r="45" fill="{STAR_Y}" fill-opacity="0.32"/>')
    e.append(f'<circle cx="820" cy="520" r="30" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="3"/>')
    # 數字泡泡（1, 2 = 前面的人）
    for i, x in enumerate((220, 350)):
        e.append(f'<circle cx="{x}" cy="160" r="28" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="4"/>')
        e.append(svgtext(x, 180, str(i + 1), size=40, fill="#4A78A8", weight="bold"))
    # 星星點綴
    e.append(star(1050, 100, 20))
    e.append(sparkle(150, 220, 12))
    e.append(sparkle(950, 280, 12))
    return svg(W, H, "".join(e))


def scene_p7():
    """p7：觀點頁：Lucas 和 Anne 各自站在自己的發光 spot 上微笑等待；角落一個灰色小畫面：有人插隊、被插的孩子哭臉"""
    e = []
    # 地板
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#D4E8D0"/>')
    # Lucas 左邊（有 SPOT）
    e.append(lucas(cx=280, cy=300, scale=1.1, expr="smile"))
    e.append(f'<circle cx="280" cy="518" r="52" fill="{STAR_Y}" fill-opacity="0.26"/>')
    e.append(f'<circle cx="280" cy="518" r="38" fill="{STAR_Y}" fill-opacity="0.30"/>')
    e.append(f'<circle cx="280" cy="518" r="26" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="2.5"/>')
    # Anne 右邊（有 SPOT）
    e.append(ann(cx=900, cy=300, scale=1.1, expr="smile"))
    e.append(f'<circle cx="900" cy="518" r="52" fill="{STAR_Y}" fill-opacity="0.26"/>')
    e.append(f'<circle cx="900" cy="518" r="38" fill="{STAR_Y}" fill-opacity="0.30"/>')
    e.append(f'<circle cx="900" cy="518" r="26" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="2.5"/>')
    # 灰色插隊場景框（右下角）
    e.append(f'<rect x="680" y="320" width="240" height="180" rx="8" fill="#D0D0D0" stroke="#909090" stroke-width="3"/>')
    e.append(f'<rect x="690" y="330" width="220" height="160" rx="6" fill="#E8E8E8"/>')
    # 小場景：插隊的小孩（無名小孩，不是 Owen）
    e.append(f'<ellipse cx="750" cy="410" rx="20" ry="24" fill="{SKIN}"/>')  # 頭
    e.append(f'<path d="M -20 24 C -22 0 22 0 20 24" fill="{SKIN}" transform="translate(750,410)"/>')  # 身體
    e.append(f'<path d="M -10 0 L -10 16" stroke="{SKIN}" stroke-width="6" stroke-linecap="round" transform="translate(750,420)"/>')  # 腿
    e.append(f'<path d="M 10 0 L 10 16" stroke="{SKIN}" stroke-width="6" stroke-linecap="round" transform="translate(750,420)"/>')
    # 被插的小孩（哭臉）
    e.append(f'<ellipse cx="810" cy="410" rx="20" ry="24" fill="{SKIN}"/>')
    e.append(f'<path d="M -20 24 C -22 0 22 0 20 24" fill="{SKIN}" transform="translate(810,410)"/>')
    e.append(f'<path d="M -10 0 L -10 16" stroke="{SKIN}" stroke-width="6" stroke-linecap="round" transform="translate(810,420)"/>')
    e.append(f'<path d="M 10 0 L 10 16" stroke="{SKIN}" stroke-width="6" stroke-linecap="round" transform="translate(810,420)"/>')
    # 哭臉：眼睛X + 嘴巴倒V
    e.append(f'<line x1="800" y1="400" x2="810" y2="410" stroke="#2A2320" stroke-width="2.5" stroke-linecap="round"/>')
    e.append(f'<line x1="810" y1="400" x2="800" y2="410" stroke="#2A2320" stroke-width="2.5" stroke-linecap="round"/>')
    e.append(f'<path d="M 800 415 Q 805 420 810 415" fill="none" stroke="#E4574C" stroke-width="2.5" stroke-linecap="round"/>')
    # 淚滴
    e.append(f'<ellipse cx="800" cy="425" rx="2" ry="4" fill="#8FD3F2"/>')
    e.append(f'<ellipse cx="810" cy="425" rx="2" ry="4" fill="#8FD3F2"/>')
    return svg(W, H, "".join(e))


def scene_p8():
    """p8：Owen 上籃姿勢躍向籃框，球在指尖；場邊媽媽 April 拍手，語音泡泡 "Great waiting, Owen!" """
    e = []
    # 地板
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#E8D2AC"/>')
    # 籃框（右側上方）
    e.append(f'<rect x="1010" y="280" width="14" height="190" fill="#8B5E52"/>')  # 柱子
    e.append(hoop(cx=1017, cy=280, scale=1.15))
    # 媽媽 April 左邊拍手
    e.append(april(cx=220, cy=260, scale=1.05, pose="cheer"))
    # April 的語音泡泡
    e.append(f'<path d="M 320 80 Q 320 40 390 40 L 560 40 Q 620 40 620 80 Q 620 120 560 120 L 450 120 L 400 150 L 410 120 L 390 120 Q 320 120 320 80 Z" fill="#FFFFFF" stroke="#E3C98F" stroke-width="4"/>')
    e.append(svgtext(490, 95, "Great waiting,", size=28, fill="#D97706", weight="bold"))
    e.append(svgtext(490, 125, "Owen!", size=28, fill="#D97706", weight="bold"))
    # Owen 上籃姿勢（jump 動作 = 騰空）
    e.append(boy(pose="jump", expr="big", cx=750, cy=140, scale=1.2, jersey=JERSEY_39))
    # 球在指尖（向籃框方向）
    e.append(basketball(cx=840, cy=80, r=24))
    # 軌跡線
    e.append(f'<path d="M 780 160 Q 810 120 840 85" fill="none" stroke="#F28C3A" stroke-width="4" stroke-dasharray="6 4" stroke-linecap="round"/>')
    # 星星加油
    e.append(star(600, 180, 18))
    e.append(sparkle(900, 140, 12))
    return svg(W, H, "".join(e))


def scene_p9():
    """p9：球空心入網（swish 弧線），Owen 叉腰大笑；右側小畫面：學校飲水機前 Owen（白 T）站在隊伍裡腳下有 spot 圓圈"""
    e = []
    # 地板
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#F2CFDC"/>')
    # 籃框（右上）
    e.append(f'<rect x="1010" y="150" width="14" height="200" fill="#8B5E52"/>')  # 柱子
    e.append(hoop(cx=1017, cy=150, scale=1.1))
    # SWISH 弧線（球入網）
    e.append(f'<path d="M 780 180 Q 900 220 980 240" fill="none" stroke="#F28C3A" stroke-width="5" stroke-dasharray="8 4" stroke-linecap="round"/>')
    # Owen 叉腰大笑（hips 動作）
    e.append(boy(pose="hips", expr="big", cx=560, cy=280, scale=1.25))
    # 笑聲泡泡（多個放射狀）
    e.append(f'<path d="M 620 220 q 26 10 26 34 M 650 210 q 40 16 40 54 M 680 200 q 54 22 54 74" fill="none" stroke="#F49AB5" stroke-width="7" stroke-linecap="round"/>')
    # 星星點綴
    e.append(star(400, 150, 20))
    e.append(sparkle(750, 90, 12))
    e.append(sparkle(920, 380, 12))
    # 右側小畫面：學校飲水機
    e.append(f'<rect x="780" y="320" width="210" height="160" rx="8" fill="#E0E0E0" stroke="#A0A0A0" stroke-width="3"/>')
    e.append(f'<rect x="790" y="330" width="190" height="140" rx="6" fill="#F5F5F5"/>')
    # 飲水機（矩形+出水口）
    e.append(f'<rect x="830" y="370" width="50" height="60" rx="4" fill="#7A9BB8" stroke="#4A5C7A" stroke-width="2.5"/>')
    e.append(f'<circle cx="855" cy="385" r="6" fill="#A8D8FF"/>')  # 出水口
    # 小 Owen（白 T）在隊伍裡
    e.append(f'<g transform="translate(810,420) scale(0.55)">')
    e.append(f'<circle cx="0" cy="-20" r="18" fill="{SKIN}"/>')  # 頭
    e.append(f'<ellipse cx="0" cy="5" rx="14" ry="20" fill="{TEE}"/>')  # 白T
    e.append(f'<path d="M -8 25 L -8 40" stroke="{SKIN}" stroke-width="6" stroke-linecap="round"/>')  # 腿
    e.append(f'<path d="M 8 25 L 8 40" stroke="{SKIN}" stroke-width="6" stroke-linecap="round"/>')
    e.append('</g>')
    # 小 SPOT（白 T Owen 腳下）
    e.append(f'<circle cx="810" cy="465" r="18" fill="{STAR_Y}" fill-opacity="0.24"/>')
    e.append(f'<circle cx="810" cy="465" r="12" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="1.5"/>')
    return svg(W, H, "".join(e))


def scene_p10():
    """p10：英雄收尾：Owen 披紅披風叉腰，一腳踩在金色 spot 上，胸前 39 號，滿天星"""
    e = []
    # 金色地面圓暈
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="110" fill="#FFDD7E"/>')
    # 滿天星
    for (x, y, r) in [(150, 100, 22), (1030, 110, 26), (130, 360, 18), (1060, 370, 20), (320, 60, 14), (870, 70, 16)]:
        e.append(star(x, y, r))
    e.append(sparkle(280, 260, 12))
    e.append(sparkle(910, 280, 12))
    # 腳下大 SPOT（金色光暈）
    e.append(f'<circle cx="594" cy="530" r="90" fill="{STAR_Y}" fill-opacity="0.26"/>')
    e.append(f'<circle cx="594" cy="530" r="70" fill="{STAR_Y}" fill-opacity="0.30"/>')
    e.append(f'<circle cx="594" cy="530" r="50" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="4"/>')
    # Owen 英雄姿勢（hips + cape + 39 號）
    e.append(boy(pose="hips", expr="proud", cx=594, cy=160, scale=1.35, cape=True, jersey=JERSEY_39))
    return svg(W, H, "".join(e))


# ============ PAGES ============
PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I am number <b>39</b>. I love basketball!'),
    ("p2", scene_p2, 'We line up to shoot.<br/>Lucas is first, then Anne, then me!'),
    ("p3", scene_p3, 'I want to shoot <b>NOW</b>!<br/>Waiting is so hard.'),
    ("p4", scene_p4, 'My feet feel <b>jumpy</b>!<br/>My legs want to run.<br/><b>Go, go, go</b>, says my heart!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I <b>glue</b> my feet to my spot!'),
    ("p6", scene_p6, 'I glue my feet down.<br/>I count: one, two.<br/>I <b>cheer</b> for my friends!'),
    ("p7", scene_p7, 'Lucas waits for his turn.<br/>Anne waits too.<br/>Jumping the line makes friends sad.'),
    ("p8", scene_p8, 'Now it is my turn!<br/>Mom April says, &ldquo;Great waiting, <b>Owen</b>!&rdquo;'),
    ("p9", scene_p9, '<b>Swish!</b> I feel <b>GREAT</b>!<br/>At school, I wait my spot too.'),
    ("p10", scene_p10, 'Glue my feet. Cheer for friends.<br/><b>Wait my spot!</b><br/>I practice every day!'),
]

# ============ PARENT TIPS ============
PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("教孩子三步口訣", "讀完玩角色扮演：膠水（把腳黏住）→ 加油（為隊友加油）→ 等我的位置。全家和老師統一用同一句提醒。"),
    ("讀完玩 2 分鐘角色扮演", "你當排隊裡的人、他是 Owen，練「腳黏住 → 數一數 → 為朋友加油 → 輪到我」，再交換角色。"),
    ("轉移到學校場景", "看到他在飲水機、洗手台、點心隊伍停住腳，就用暗號 &ldquo;Wait my spot!&rdquo;，讓技能離開球場。當他主動說 &ldquo;My feet feel jumpy&rdquo; = 他察覺到衝動了，大力稱讚。"),
    ("搭配每日聯絡卡", "請老師每天打勾 2&ndash;3 條「有沒有偷偷插隊」；當天達標 → 當天兌現小獎勵。"),
]

# ============ BOOK DICT ============
BOOK = {
    "slug": "wait-my-spot",
    "order": 2,
    "title_pre": "I Can ",
    "title_hi": "Wait",
    "title_post": " My Spot!",
    "title_zh": "等我的位置",
    "subtitle": "Owen's basketball story",
    "tagline_zh": "Owen 的籃球故事",
    "chips": ["Social Story", "Basketball", "12 pages"],
    "pdf_name": "I_Can_Wait_My_Spot.pdf",
    "bg": BG,
    "pages": PAGES,
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的排隊腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Glue → Cheer → Wait my spot!</b>&nbsp;"
                 "當他哪天主動說 &ldquo;My feet feel jumpy&rdquo;（我察覺到衝動了），"
                 "就是最值得大力稱讚的時刻。"),
    "cover": scene_cover,
}
