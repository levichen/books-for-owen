# -*- coding: utf-8 -*-
"""Book 12: Arms, Breath, Kick! — 游自由式技術分解。Coach Bear 大灰熊教練首次登場。"""
import math
from parts import *
from book_common import svg, svgtext, TXT, W, H, COVER_W, COVER_H

# soft page palettes (泳池主題：藍綠漸層)
BG = {
    "cover": "#E8F4F8", "p1": "#E3F2FD", "p2": "#B3E5FC", "p3": "#81D4FA",
    "p4": "#80DEEA", "p5": "#6C5BA6", "p6": "#B3E5FC", "p7": "#BBDEFB",
    "p8": "#80DEEA", "p9": "#B3E5FC", "p10": "#A5D6A7", "p11": "#FBF4E8",
}

POOL_WATER = "#7EC8E8"  # 水面色帶
POOL_LINE = "#E8A8A8"   # 浮球紅色


# ==================== COACH BEAR 輔助函式 ====================
def coach_bear(cx=0, cy=0, scale=1.0, pose="stand"):
    """Coach Bear 大灰熊教練：身體＋頭＋耳＋四肢＋哨子。
    pose: stand | point | crouch | cheer | thumbsup
    腳底 ≈ cy + 115*scale"""
    e = []

    # 身體：大橢圓 rx=70 ry=85，灰色＋描邊
    e.append(f'<ellipse cx="0" cy="0" rx="70" ry="85" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="4"/>')

    # 肚皮：淺灰 #C9C9C9 橢圓
    e.append(f'<ellipse cx="0" cy="20" rx="45" ry="55" fill="#C9C9C9"/>')

    # 頭：圓 r=48 在 (0, -105)
    e.append(f'<circle cx="0" cy="-105" r="48" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="3"/>')

    # 圓耳兩個 r=16 在 (-38,-142)/(38,-142)
    e.append(f'<circle cx="-38" cy="-142" r="16" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="2"/>')
    e.append(f'<circle cx="38" cy="-142" r="16" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="2"/>')
    # 內耳淺灰小圓
    e.append(f'<circle cx="-38" cy="-142" r="8" fill="#C9C9C9"/>')
    e.append(f'<circle cx="38" cy="-142" r="8" fill="#C9C9C9"/>')

    # 吻部：淺灰橢圓 rx=22 ry=16 在 (0,-92)
    e.append(f'<ellipse cx="0" cy="-92" rx="22" ry="16" fill="#C9C9C9"/>')
    # 黑色橢圓鼻 (0,-100) rx=8 ry=6
    e.append(f'<ellipse cx="0" cy="-100" rx="8" ry="6" fill="#2A2320"/>')
    # 微笑弧
    e.append(f'<path d="M -12 -88 Q 0 -80 12 -88" fill="none" stroke="#6E6E6E" stroke-width="3" stroke-linecap="round"/>')

    # 眼睛：兩個黑點 r=5
    e.append(f'<circle cx="-18" cy="-112" r="5" fill="#2A2320"/>')
    e.append(f'<circle cx="18" cy="-112" r="5" fill="#2A2320"/>')
    # 眉上小弧（和藹）
    e.append(f'<path d="M -26 -126 Q -18 -132 -10 -126" fill="none" stroke="#6E6E6E" stroke-width="2.5" stroke-linecap="round"/>')
    e.append(f'<path d="M 10 -126 Q 18 -132 26 -126" fill="none" stroke="#6E6E6E" stroke-width="2.5" stroke-linecap="round"/>')

    # 手臂：粗弧線
    if pose == "point":
        # 右臂指向前（右下方）
        e.append(f'<path d="M 58 -20 Q 120 0 140 40" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
        e.append(f'<circle cx="146" cy="48" r="14" fill="{SKIN}"/>')
        # 左臂自然垂下
        e.append(f'<path d="M -58 -20 Q -100 20 -80 60" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
        e.append(f'<circle cx="-80" cy="66" r="13" fill="{SKIN}"/>')
    elif pose == "crouch":
        # 下蹲：整體 cy 下移＋身體壓扁＋手臂抬起對齐
        # 由外層 transform 處理 cy，這裡單位是 scale
        # 雙臂抬起在胸前
        e.append(f'<path d="M -58 -20 Q -90 -40 -70 -60" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
        e.append(f'<circle cx="-68" cy="-68" r="14" fill="{SKIN}"/>')
        e.append(f'<path d="M 58 -20 Q 90 -40 70 -60" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
        e.append(f'<circle cx="68" cy="-68" r="14" fill="{SKIN}"/>')
    elif pose == "thumbsup":
        # 比讚：右臂上舉豎起，左臂自然
        e.append(f'<path d="M 58 -30 Q 90 -80 96 -120" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
        e.append(f'<circle cx="98" cy="-128" r="14" fill="{SKIN}"/>')
        e.append(f'<path d="M -58 -20 Q -100 20 -80 60" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
        e.append(f'<circle cx="-80" cy="66" r="13" fill="{SKIN}"/>')
    else:  # stand（預設）
        # 雙臂自然垂下
        e.append(f'<path d="M -58 -20 Q -100 20 -80 60" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
        e.append(f'<circle cx="-80" cy="66" r="13" fill="{SKIN}"/>')
        e.append(f'<path d="M 58 -20 Q 100 20 80 60" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
        e.append(f'<circle cx="80" cy="66" r="13" fill="{SKIN}"/>')

    # 腿：兩個短圓柱
    e.append(f'<path d="M -32 85 L -32 115" stroke="{SKIN}" stroke-width="28" stroke-linecap="round" fill="none"/>')
    e.append(f'<path d="M 32 85 L 32 115" stroke="{SKIN}" stroke-width="28" stroke-linecap="round" fill="none"/>')
    # 腳：棕色橢圓
    e.append(f'<ellipse cx="-32" cy="122" rx="18" ry="10" fill="#8B5E52"/>')
    e.append(f'<ellipse cx="32" cy="122" rx="18" ry="10" fill="#8B5E52"/>')

    # 紅色哨子掛胸前（繩線＋小紅圓角矩形）
    e.append(f'<path d="M -8 -30 Q 0 20 8 -30" fill="none" stroke="#8A7460" stroke-width="3"/>')
    e.append(f'<rect x="-12" y="12" width="24" height="16" rx="6" fill="#F2B035" stroke="#C98A18" stroke-width="2.5"/>')

    inner = "".join(e)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


# ==================== SCENE FUNCTIONS ====================
def scene_cover():
    """封面：Owen 白 T 背泳包拿蛙鏡＋水滴點綴（開心出發感）"""
    e = []
    # 背景：淺藍
    e.append(f'<rect x="0" y="0" width="{COVER_W}" height="{COVER_H}" fill="{BG["cover"]}"/>')

    # 水滴點綴
    for (x, y, r) in [(150, 80, 16), (1050, 90, 20), (200, 530, 14), (1000, 520, 18), (280, 140, 12), (900, 150, 14)]:
        e.append(f'<path d="M {x} {y} Q {x-r*0.6} {y+r*1.2} {x} {y+r*2.4} Q {x+r*0.6} {y+r*1.2} {x} {y} Z" fill="#7EC8E8" stroke="#5BA3D0" stroke-width="2"/>')

    # 白色背景圓圈
    e.append(f'<ellipse cx="594" cy="400" rx="520" ry="140" fill="#FFFFFF" fill-opacity="0.4"/>')

    # Owen 白 T 背泳包
    e.append(boy(pose="wave", expr="big", cx=594, cy=280, scale=1.3, backpack=True))

    # 蛙鏡掛在右手（波浪手臂末端，手圓圈在 ~600,360）帶子繞過手圓圈
    e.append(f'<path d="M 605 360 Q 670 340 710 370" fill="none" stroke="#E8944A" stroke-width="5" stroke-linecap="round"/>')  # 左帶
    e.append(f'<circle cx="720" cy="380" r="17" fill="#FFFFFF" stroke="#161616" stroke-width="4"/>')  # 左鏡框
    e.append(f'<circle cx="760" cy="380" r="17" fill="#FFFFFF" stroke="#161616" stroke-width="4"/>')  # 右鏡框
    e.append(f'<rect x="738" y="375" width="16" height="10" rx="4" fill="#161616"/>')  # 鏡架連結
    e.append(f'<line x1="703" y1="386" x2="777" y2="386" stroke="#E8944A" stroke-width="5" stroke-linecap="round"/>')  # 右帶

    # 開心星星
    e.append(star(350, 120, 24))
    e.append(star(860, 130, 28))
    e.append(sparkle(200, 250, 12))
    e.append(sparkle(980, 240, 14))

    return svg(COVER_W, COVER_H, "".join(e), bg=None)


def scene_p1():
    """p1: Owen 白 T 背泳包、手拿蛙鏡，開心出門，頭上水滴形狀點綴"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p1"]}"/>')

    # 太陽
    e.append(sun(1020, 80, 32))

    # 浮雲
    e.append(cloud(180, 70, 0.9))
    e.append(cloud(520, 60, 0.7))

    # 地面
    e.append(f'<rect x="0" y="430" width="{W}" height="130" fill="#A8D5BA"/>')

    # 泳池建築在遠處
    e.append(f'<rect x="850" y="260" width="260" height="180" rx="12" fill="#B3C6DB" stroke="#8A9FB1" stroke-width="4"/>')
    e.append(f'<polygon points="850,260 1110,260 1110,280 850,280 Z" fill="#7FA3C0"/>')  # 屋頂
    e.append(f'<rect x="920" y="300" width="70" height="90" rx="6" fill="#5BA8DB"/>')  # 窗
    e.append(f'<rect x="1020" y="300" width="70" height="90" rx="6" fill="#5BA8DB"/>')

    # 灌木
    e.append(f'<circle cx="80" cy="420" r="45" fill="#6FA8A8"/><circle cx="130" cy="430" r="35" fill="#559898"/>')
    e.append(f'<circle cx="1080" cy="420" r="40" fill="#6FA8A8"/><circle cx="1130" cy="435" r="32" fill="#559898"/>')

    # Owen 走向泳池，白 T 背泳包、手拿蛙鏡
    e.append(boy(pose="walk", expr="big", cx=380, cy=200, scale=1.1, backpack=True))

    # 蛙鏡在手裡（靠 Owen 右側）
    e.append(f'<circle cx="480" cy="250" r="16" fill="#FFFFFF" stroke="#161616" stroke-width="3.5"/>')
    e.append(f'<circle cx="520" cy="250" r="16" fill="#FFFFFF" stroke="#161616" stroke-width="3.5"/>')
    e.append(f'<rect x="498" y="246" width="16" height="8" rx="3" fill="#161616"/>')
    e.append(f'<line x1="466" y1="256" x2="534" y2="256" stroke="#E8944A" stroke-width="4" stroke-linecap="round"/>')

    # 頭上水滴點綴
    for (dx, dy, sz) in [(0, -60, 14), (-40, -40, 10), (40, -35, 12)]:
        x, y = 380 + dx, 140 + dy
        e.append(f'<path d="M {x} {y} Q {x-sz*0.5} {y+sz*1.0} {x} {y+sz*1.8} Q {x+sz*0.5} {y+sz*1.0} {x} {y} Z" fill="#7EC8E8" stroke="#5BA3D0" stroke-width="1.5"/>')

    # 想法泡泡
    e.append(f'<ellipse cx="580" cy="100" rx="120" ry="60" fill="#FFFFFF" stroke="#B3D9E8" stroke-width="4"/>')
    e.append(f'<circle cx="540" cy="140" r="12" fill="#FFFFFF" stroke="#B3D9E8" stroke-width="3"/>')
    e.append(f'<circle cx="520" cy="155" r="8" fill="#FFFFFF" stroke="#B3D9E8" stroke-width="2"/>')

    return svg(W, H, "".join(e))


def scene_p2():
    """p2: 泳池全景：水道線、Coach Bear 站池邊（掛哨子、揮手），Owen（泳褲＋蛙鏡）在水裡揮手"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p2"]}"/>')

    # 池邊上方：淺藍牆 + 白色磁磚線
    e.append(f'<rect x="0" y="0" width="{W}" height="200" fill="#A8D5F7"/>')
    for x in range(0, W+80, 80):
        e.append(f'<line x1="{x}" y1="0" x2="{x}" y2="200" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/>')
    for y in range(0, 201, 40):
        e.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#FFFFFF" stroke-width="2" opacity="0.6"/>')

    # 池邊地板（deck）：淺色磁磚地板，y=200-260（高度 60px）
    e.append(f'<rect x="0" y="200" width="{W}" height="60" fill="#D4C9BE"/>')
    for x in range(0, W+60, 60):
        e.append(f'<line x1="{x}" y1="200" x2="{x}" y2="260" stroke="#C4B9AE" stroke-width="2"/>')
    for y in range(200, 261, 30):
        e.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#C4B9AE" stroke-width="1.5"/>')

    # 水面色帶
    e.append(f'<rect x="0" y="260" width="{W}" height="160" fill="{POOL_WATER}"/>')

    # 水道線：紅白浮球
    for x in range(0, W+60, 60):
        if x % 120 == 0:
            e.append(f'<circle cx="{x}" cy="300" r="10" fill="{POOL_LINE}"/>')
        else:
            e.append(f'<circle cx="{x}" cy="300" r="10" fill="#FFFFFF"/>')

    # 池底
    e.append(f'<rect x="0" y="420" width="{W}" height="140" fill="#80DEEA"/>')

    # Coach Bear 站池邊左側：scale 1.3 全高 ~348 裝不進 deck 上方空間（頭會被畫布裁掉）
    # 縮成 0.7：頭頂 cy-153*0.7 ≈ 17 在畫布內、腳底 cy+115*0.7 ≈ 205 貼 deck 頂面
    e.append(coach_bear(cx=180, cy=124, scale=0.7, pose="stand"))

    # Owen 在水裡：boy_bust(arms="handup", jersey=泳衣) 放在水後面、下沉
    e.append(boy_bust(expr="big", cx=880, cy=330, scale=1.0, arms="handup", jersey=('', '#4C7DD0', '#2E5AA8')))

    # 水面波浪線（蓋住 bust 下緣）
    e.append(f'<path d="M 800 325 Q 820 310 840 325 Q 860 340 880 325 Q 900 310 920 325 Q 940 340 960 325" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>')

    # 水花
    e.append(star(900, 290, 20, fill="#FFFFFF"))
    e.append(f'<circle cx="870" cy="310" r="8" fill="#FFFFFF" fill-opacity="0.7"/>')
    e.append(f'<circle cx="910" cy="320" r="6" fill="#FFFFFF" fill-opacity="0.7"/>')

    return svg(W, H, "".join(e))


def scene_p3():
    """p3: Owen 在水道裡亂衝（星星眼、水花亂噴四散），魚的思考泡泡"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p3"]}"/>')

    # 池邊牆 + 水面 + 池底
    e.append(f'<rect x="0" y="0" width="{W}" height="200" fill="#A8D5F7"/>')
    for x in range(0, W+80, 80):
        e.append(f'<line x1="{x}" y1="0" x2="{x}" y2="200" stroke="#FFFFFF" stroke-width="3" opacity="0.5"/>')
    e.append(f'<rect x="0" y="280" width="{W}" height="160" fill="{POOL_WATER}"/>')
    for x in range(0, W+60, 60):
        color = POOL_LINE if x % 120 == 0 else "#FFFFFF"
        e.append(f'<circle cx="{x}" cy="320" r="10" fill="{color}"/>')
    e.append(f'<rect x="0" y="440" width="{W}" height="120" fill="#80DEEA"/>')

    # Owen 星星眼在水裡：boy_bust(expr="star", arms="handup")
    e.append(boy_bust(expr="star", cx=594, cy=350, scale=1.1, arms="handup", jersey=('', '#4C7DD0', '#2E5AA8')))

    # 水面波浪
    e.append(f'<path d="M 530 340 Q 550 320 570 340 Q 590 360 610 340 Q 630 320 650 340 Q 670 360 694 340" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>')

    # 亂噴的水花（四周散開）
    positions = [(520, 280), (680, 290), (480, 350), (700, 360), (450, 320), (750, 310)]
    for x, y in positions:
        e.append(star(x, y, 18, fill="#FFFFFF"))
        e.append(f'<circle cx="{x-8}" cy="{y+6}" r="5" fill="#FFFFFF" fill-opacity="0.6"/>')

    # 魚的思考泡泡（右上方）
    e.append(f'<ellipse cx="950" cy="120" rx="100" ry="70" fill="#FFFFFF" stroke="#7EC8E8" stroke-width="4"/>')
    e.append(f'<polygon points="900,150 920,180 880,160" fill="#FFFFFF" stroke="#7EC8E8" stroke-width="3"/>')
    # 簡單魚圖示在泡泡內
    e.append(f'<path d="M 920 100 L 980 120 L 920 140 Z" fill="#7EC8E8"/>')
    e.append(f'<circle cx="920" cy="120" r="6" fill="#161616"/>')

    return svg(W, H, "".join(e))


def scene_p4():
    """p4: 衝動頁：Owen 半身在水、手臂垂平貼水面（畫向下箭頭）、腳後方 zzz、嗆水表情（oh）＋嘴邊水滴；遠處 Coach Bear 舉手"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p4"]}"/>')

    # 池邊上方：淺藍牆 + 白色磁磚線
    e.append(f'<rect x="0" y="0" width="{W}" height="200" fill="#A8D5F7"/>')
    for x in range(0, W+80, 80):
        e.append(f'<line x1="{x}" y1="0" x2="{x}" y2="200" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/>')
    for y in range(0, 201, 40):
        e.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#FFFFFF" stroke-width="2" opacity="0.6"/>')

    # 池邊地板（deck）：淺色磁磚地板，y=200-260
    e.append(f'<rect x="0" y="200" width="{W}" height="60" fill="#D4C9BE"/>')
    for x in range(0, W+60, 60):
        e.append(f'<line x1="{x}" y1="200" x2="{x}" y2="260" stroke="#C4B9AE" stroke-width="2"/>')
    for y in range(200, 261, 30):
        e.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#C4B9AE" stroke-width="1.5"/>')

    # 水面色帶
    e.append(f'<rect x="0" y="260" width="{W}" height="160" fill="{POOL_WATER}"/>')

    # 水道線
    for x in range(0, W+60, 60):
        color = POOL_LINE if x % 120 == 0 else "#FFFFFF"
        e.append(f'<circle cx="{x}" cy="300" r="10" fill="{color}"/>')

    # 池底
    e.append(f'<rect x="0" y="420" width="{W}" height="140" fill="#80DEEA"/>')

    # Owen 衝動頁：boy_bust(arms="desk", expr="oh") 半身入水
    e.append(boy_bust(expr="oh", cx=400, cy=330, scale=1.15, arms="desk", jersey=('', '#4C7DD0', '#2E5AA8')))

    # 水面波浪
    e.append(f'<path d="M 320 315 Q 340 300 360 315 Q 380 330 400 315 Q 420 300 440 315 Q 460 330 480 315" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>')

    # 手臂下方向下箭頭
    e.append(f'<line x1="300" y1="350" x2="300" y2="410" stroke="#E4574C" stroke-width="5" stroke-linecap="round"/>')
    e.append(f'<polygon points="300,415 290,395 310,395" fill="#E4574C"/>')

    # 嘴邊水滴
    e.append(f'<path d="M 430 345 Q 425 355 430 365 Q 435 355 430 345 Z" fill="#B3E5FC"/>')

    # 腳後方 zzz（無水花）
    e.append(svgtext(470, 280, "zzz", size=40, fill="#D0D0D0", weight="bold"))

    # 遠處 Coach Bear 舉手（pose="point"）：腳踏實地在 deck
    # feet_y = cy + 115*scale = 260，cy = 260 - 115*0.9 = 156.5
    e.append(coach_bear(cx=900, cy=156, scale=0.9, pose="point"))

    return svg(W, H, "".join(e))


def scene_p5():
    """p5: 紫色星空背景：Coach Bear 發光登場比出三根手指，旁邊三個發光圖示（①高舉手臂弧 ②側頭氣泡 ③腳＋水花），Owen（press 表情）看著"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p5"]}"/>')

    # 星星背景
    for (x, y, r) in [(140, 100, 18), (1040, 110, 22), (180, 450, 16), (1000, 430, 16), (300, 80, 14), (880, 70, 12)]:
        e.append(star(x, y, r, fill="#FFE9A8"))

    # Coach Bear 發光登場：中央，比三根手指
    # 亮黃光暈（半透明疊圈）
    e.append(f'<circle cx="594" cy="320" r="180" fill="#FFE9A8" fill-opacity="0.2"/>')
    e.append(f'<circle cx="594" cy="320" r="120" fill="#FFE9A8" fill-opacity="0.15"/>')

    # Coach Bear（特別造型：比三根手指）
    bear_g = []
    # 身體
    bear_g.append(f'<ellipse cx="0" cy="0" rx="70" ry="85" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="4"/>')
    # 肚皮
    bear_g.append(f'<ellipse cx="0" cy="20" rx="45" ry="55" fill="#C9C9C9"/>')
    # 頭
    bear_g.append(f'<circle cx="0" cy="-105" r="48" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="3"/>')
    # 耳
    bear_g.append(f'<circle cx="-38" cy="-142" r="16" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="2"/>')
    bear_g.append(f'<circle cx="38" cy="-142" r="16" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="2"/>')
    bear_g.append(f'<circle cx="-38" cy="-142" r="8" fill="#C9C9C9"/>')
    bear_g.append(f'<circle cx="38" cy="-142" r="8" fill="#C9C9C9"/>')
    # 吻部
    bear_g.append(f'<ellipse cx="0" cy="-92" rx="22" ry="16" fill="#C9C9C9"/>')
    bear_g.append(f'<ellipse cx="0" cy="-100" rx="8" ry="6" fill="#2A2320"/>')
    bear_g.append(f'<path d="M -12 -88 Q 0 -80 12 -88" fill="none" stroke="#6E6E6E" stroke-width="3" stroke-linecap="round"/>')
    # 眼睛
    bear_g.append(f'<circle cx="-18" cy="-112" r="5" fill="#2A2320"/>')
    bear_g.append(f'<circle cx="18" cy="-112" r="5" fill="#2A2320"/>')
    # 手臂高舉，手指展開
    bear_g.append(f'<path d="M -58 -30 Q -90 -100 -70 -150" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
    bear_g.append(f'<circle cx="-68" cy="-158" r="14" fill="{SKIN}"/>')
    bear_g.append(f'<path d="M 58 -30 Q 90 -100 70 -150" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
    bear_g.append(f'<circle cx="68" cy="-158" r="14" fill="{SKIN}"/>')
    # 右手三根手指展開（在胸前）
    bear_g.append(f'<path d="M -20 20 L -20 50" stroke="{SKIN}" stroke-width="16" stroke-linecap="round"/>')
    bear_g.append(f'<path d="M 0 15 L 0 50" stroke="{SKIN}" stroke-width="16" stroke-linecap="round"/>')
    bear_g.append(f'<path d="M 20 20 L 20 50" stroke="{SKIN}" stroke-width="16" stroke-linecap="round"/>')
    # 腿
    bear_g.append(f'<path d="M -32 85 L -32 115" stroke="{SKIN}" stroke-width="28" stroke-linecap="round" fill="none"/>')
    bear_g.append(f'<path d="M 32 85 L 32 115" stroke="{SKIN}" stroke-width="28" stroke-linecap="round" fill="none"/>')
    bear_g.append(f'<ellipse cx="-32" cy="122" rx="18" ry="10" fill="#8B5E52"/>')
    bear_g.append(f'<ellipse cx="32" cy="122" rx="18" ry="10" fill="#8B5E52"/>')
    # 哨子
    bear_g.append(f'<path d="M -8 -30 Q 0 20 8 -30" fill="none" stroke="#8A7460" stroke-width="3"/>')
    bear_g.append(f'<rect x="-12" y="12" width="24" height="16" rx="6" fill="#F2B035" stroke="#C98A18" stroke-width="2.5"/>')

    e.append(f'<g transform="translate(594, 320) scale(1.1)">{"".join(bear_g)}</g>')

    # 三個發光圖示
    # ① 高舉手臂弧線特寫（左上）
    e.append(f'<circle cx="250" cy="140" r="70" fill="#FFFFFF" stroke="#FFE9A8" stroke-width="4" opacity="0.8"/>')
    e.append(f'<path d="M 220 150 Q 210 110 240 100" stroke="#4C7DD0" stroke-width="8" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="242" cy="95" r="10" fill="#4C7DD0"/>')
    e.append(f'<circle cx="250" cy="100" r="6" fill="#FFE9A8" opacity="0.6"/>')

    # ② 側頭換氣氣泡（右上）
    e.append(f'<circle cx="940" cy="140" r="70" fill="#FFFFFF" stroke="#FFE9A8" stroke-width="4" opacity="0.8"/>')
    # 側頭示意
    e.append(f'<circle cx="930" cy="130" r="18" fill="#FFD9B6"/>')
    e.append(f'<path d="M 948 135 Q 960 130 970 135" fill="none" stroke="#8C4A3C" stroke-width="2"/>')
    # 氣泡
    e.append(f'<circle cx="950" cy="110" r="8" fill="#FFFFFF" stroke="#B3D9E8" stroke-width="2"/>')
    e.append(f'<circle cx="970" cy="105" r="6" fill="#FFFFFF" stroke="#B3D9E8" stroke-width="2"/>')

    # ③ 腳＋水花（下方）
    e.append(f'<circle cx="594" cy="480" r="70" fill="#FFFFFF" stroke="#FFE9A8" stroke-width="4" opacity="0.8"/>')
    # 腳
    e.append(f'<ellipse cx="580" cy="475" rx="12" ry="18" fill="#FFD9B6"/>')
    e.append(f'<ellipse cx="610" cy="475" rx="12" ry="18" fill="#FFD9B6"/>')
    # 水花星形
    e.append(star(570, 430, 16, fill="#FFFFFF"))
    e.append(star(620, 435, 14, fill="#FFFFFF"))

    # Owen 看著（press 表情）
    e.append(boy(pose="stand", expr="press", cx=200, cy=280, scale=1.2))

    return svg(W, H, "".join(e))


def scene_p6():
    """p6: 三步腳本三格：①手臂高舉出水特寫 ②頭側轉快速換氣 ③雙腳打水"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p6"]}"/>')

    # 底部水面色帶
    e.append(f'<rect x="0" y="420" width="{W}" height="140" fill="{POOL_WATER}"/>')

    # 三個圓角矩形框
    frame_w, frame_h = 320, 320
    positions = [(200, 140), (594, 140), (988, 140)]

    for i, (cx, cy) in enumerate(positions):
        x0, y0 = cx - frame_w//2, cy - frame_h//2
        e.append(f'<rect x="{x0}" y="{y0}" width="{frame_w}" height="{frame_h}" rx="16" fill="#FFFFFF" stroke="#B3E5FC" stroke-width="4"/>')

    # 格子 1：手臂高舉出水特寫（手臂可用粗弧線＋手圓圈）
    e.append(f'<line x1="120" y1="220" x2="120" y2="300" stroke="#4C7DD0" stroke-width="12" stroke-linecap="round"/>')
    e.append(f'<path d="M 100 150 Q 90 160 95 210 Q 100 260 120 280" stroke="#4C7DD0" stroke-width="12" stroke-linecap="round" fill="none"/>')
    e.append(f'<circle cx="125" cy="140" r="14" fill="#FFD9B6"/>')
    # 水面線
    e.append(f'<line x1="80" y1="240" x2="160" y2="240" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>')

    # 格子 2：頭側轉快速換氣（嘴形＋兩顆氣泡）
    e.append(head(expr="big", cx=594, cy=200, scale=0.8))
    # 變側轉角度（旋轉 transform）
    e.append(f'<g transform="translate(594, 200) rotate(-25)">')
    e.append(f'<circle cx="-40" cy="0" r="5" fill="#2A2320"/>')
    e.append(f'</g>')
    # 氣泡（嘴邊）
    e.append(f'<circle cx="630" cy="210" r="10" fill="#FFFFFF" stroke="#B3D9E8" stroke-width="2"/>')
    e.append(f'<circle cx="655" cy="205" r="8" fill="#FFFFFF" stroke="#B3D9E8" stroke-width="2"/>')

    # 格子 3：雙腳打水大水花
    e.append(f'<ellipse cx="940" cy="240" rx="14" ry="22" fill="#FFD9B6"/>')
    e.append(f'<ellipse cx="1040" cy="240" rx="14" ry="22" fill="#FFD9B6"/>')
    # 大水花星形
    e.append(star(950, 160, 28, fill="#FFFFFF"))
    e.append(star(1030, 165, 26, fill="#FFFFFF"))

    return svg(W, H, "".join(e))


def scene_p7():
    """p7: 觀點頁：Coach Bear 蹲池邊對 Owen 比讚，Owen 游得又直又穩（直線軌跡虛線），安全浮標"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p7"]}"/>')

    # 池邊 + 水面 + 池底
    e.append(f'<rect x="0" y="0" width="{W}" height="200" fill="#A8D5F7"/>')
    e.append(f'<rect x="0" y="280" width="{W}" height="160" fill="{POOL_WATER}"/>')
    e.append(f'<rect x="0" y="440" width="{W}" height="120" fill="#80DEEA"/>')

    # 水道線
    for x in range(0, W+60, 60):
        color = POOL_LINE if x % 120 == 0 else "#FFFFFF"
        e.append(f'<circle cx="{x}" cy="320" r="10" fill="{color}"/>')

    # Coach Bear 蹲下，pose="crouch"，手臂抬起
    e.append(coach_bear(cx=140, cy=330, scale=1.2, pose="crouch"))

    # Owen 游直線：boy_bust(arms="handup") 遠距離
    e.append(boy_bust(expr="big", cx=850, cy=350, scale=0.85, arms="handup", jersey=('', '#4C7DD0', '#2E5AA8')))

    # 直線軌跡虛線（從 Owen 向回）
    e.append(f'<line x1="300" y1="360" x2="800" y2="360" stroke="#FFFFFF" stroke-width="3" stroke-dasharray="12 8"/>')

    # 水面波浪
    e.append(f'<path d="M 780 340 Q 800 320 820 340 Q 840 360 860 340 Q 880 320 900 340" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>')

    # 安全浮標（紅白相間圓形）
    e.append(f'<circle cx="600" cy="400" r="22" fill="none" stroke="{POOL_LINE}" stroke-width="6"/>')
    e.append(f'<path d="M 600 378 L 600 422 M 578 400 L 622 400" stroke="#FFFFFF" stroke-width="4"/>')

    return svg(W, H, "".join(e))


def scene_p8():
    """p8: Owen 游泳英姿（高手弧＋大水花＋速度線），池邊 Daddy 舉雙手歡呼，語音泡泡 "Super swim, Owen!" """
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p8"]}"/>')

    # 池邊 + 水面 + 池底
    e.append(f'<rect x="0" y="0" width="{W}" height="200" fill="#A8D5F7"/>')
    e.append(f'<rect x="0" y="280" width="{W}" height="160" fill="{POOL_WATER}"/>')
    e.append(f'<rect x="0" y="440" width="{W}" height="120" fill="#80DEEA"/>')

    # 水道線
    for x in range(0, W+60, 60):
        color = POOL_LINE if x % 120 == 0 else "#FFFFFF"
        e.append(f'<circle cx="{x}" cy="320" r="10" fill="{color}"/>')

    # 速度線（身後）
    for i, (x, y) in enumerate([(250, 350), (220, 360), (200, 340)]):
        e.append(f'<line x1="{x}" y1="{y}" x2="{x-40}" y2="{y}" stroke="#E4574C" stroke-width="4" stroke-linecap="round" opacity="{0.8-i*0.2}"/>')

    # Owen 游泳英姿：boy_bust(arms="handup")
    e.append(boy_bust(expr="big", cx=420, cy=360, scale=1.1, arms="handup", jersey=('', '#4C7DD0', '#2E5AA8')))

    # 水面波浪
    e.append(f'<path d="M 350 340 Q 370 320 390 340 Q 410 360 430 340 Q 450 320 470 340 Q 490 360 510 340" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>')

    # 大水花（身後）
    e.append(star(320, 310, 32, fill="#FFFFFF"))
    e.append(star(280, 340, 28, fill="#FFFFFF"))
    for x, y in [(300, 290), (340, 300), (310, 360)]:
        e.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#FFFFFF" fill-opacity="0.7"/>')

    # Daddy 池邊歡呼：daddy(pose="cheer")
    e.append(daddy(cx=900, cy=240, scale=1.25, pose="cheer"))

    # 語音泡泡 "Super swim, Owen!"
    e.append(f'<path d="M 750 80 Q 750 40 820 40 L 1000 40 Q 1050 40 1050 80 Q 1050 120 1000 120 L 880 120 L 830 160 L 840 120 L 820 120 Q 750 120 750 80 Z" fill="#FFFFFF" stroke="#D9D2C4" stroke-width="4"/>')
    e.append(svgtext(900, 95, "Super swim,", size=32, fill=TXT, weight="bold"))
    e.append(svgtext(900, 130, "Owen!", size=32, fill=TXT, weight="bold"))

    return svg(W, H, "".join(e))


def scene_p9():
    """p9: Owen 摸到池壁，Coach Bear 蹲下跟他擊掌（大熊掌 vs 小手掌），水花星星"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p9"]}"/>')

    # 池邊 + 水面 + 池底
    e.append(f'<rect x="0" y="0" width="{W}" height="200" fill="#A8D5F7"/>')
    e.append(f'<rect x="0" y="280" width="{W}" height="160" fill="{POOL_WATER}"/>')
    e.append(f'<rect x="0" y="440" width="{W}" height="120" fill="#80DEEA"/>')

    # 池壁（左側）
    e.append(f'<rect x="0" y="200" width="30" height="240" fill="#A8D5F7" stroke="#7FA3C0" stroke-width="3"/>')

    # 水道線
    for x in range(0, W+60, 60):
        color = POOL_LINE if x % 120 == 0 else "#FFFFFF"
        e.append(f'<circle cx="{x}" cy="320" r="10" fill="{color}"/>')

    # Coach Bear 蹲下 crouch，手掌往前（指向上方遠離 Owen 頭）
    bear_parts = []
    # 身體（壓扁）
    bear_parts.append(f'<ellipse cx="0" cy="0" rx="70" ry="72" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="4"/>')
    bear_parts.append(f'<ellipse cx="0" cy="15" rx="45" ry="48" fill="#C9C9C9"/>')
    # 頭（位置往下）
    bear_parts.append(f'<circle cx="0" cy="-85" r="48" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="3"/>')
    # 耳
    bear_parts.append(f'<circle cx="-38" cy="-122" r="16" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="2"/>')
    bear_parts.append(f'<circle cx="38" cy="-122" r="16" fill="#9A9A9A" stroke="#6E6E6E" stroke-width="2"/>')
    bear_parts.append(f'<circle cx="-38" cy="-122" r="8" fill="#C9C9C9"/>')
    bear_parts.append(f'<circle cx="38" cy="-122" r="8" fill="#C9C9C9"/>')
    # 吻部
    bear_parts.append(f'<ellipse cx="0" cy="-75" rx="22" ry="16" fill="#C9C9C9"/>')
    bear_parts.append(f'<ellipse cx="0" cy="-82" rx="8" ry="6" fill="#2A2320"/>')
    bear_parts.append(f'<path d="M -12 -70 Q 0 -62 12 -70" fill="none" stroke="#6E6E6E" stroke-width="3" stroke-linecap="round"/>')
    # 眼睛
    bear_parts.append(f'<circle cx="-18" cy="-92" r="5" fill="#2A2320"/>')
    bear_parts.append(f'<circle cx="18" cy="-92" r="5" fill="#2A2320"/>')
    # 手臂抬起（擊掌姿勢）
    bear_parts.append(f'<path d="M -58 -10 Q -80 -40 -70 -60" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
    bear_parts.append(f'<circle cx="-68" cy="-68" r="14" fill="{SKIN}"/>')
    bear_parts.append(f'<path d="M 58 -10 Q 80 -40 70 -60" stroke="{SKIN}" stroke-width="26" stroke-linecap="round" fill="none"/>')
    bear_parts.append(f'<circle cx="68" cy="-68" r="14" fill="{SKIN}"/>')
    # 大熊掌（指向上方遠離 Owen 頭）：cx=-40（靠左）, cy=-80（上方，遠離頭 ≥30px）
    bear_parts.append(f'<ellipse cx="-40" cy="-80" rx="28" ry="35" fill="{SKIN}"/>')
    # 腿（蹲下）
    bear_parts.append(f'<path d="M -32 70 L -32 95" stroke="{SKIN}" stroke-width="28" stroke-linecap="round"/>')
    bear_parts.append(f'<path d="M 32 70 L 32 95" stroke="{SKIN}" stroke-width="28" stroke-linecap="round"/>')
    bear_parts.append(f'<ellipse cx="-32" cy="102" rx="18" ry="10" fill="#8B5E52"/>')
    bear_parts.append(f'<ellipse cx="32" cy="102" rx="18" ry="10" fill="#8B5E52"/>')
    # 哨子
    bear_parts.append(f'<path d="M -8 -15 Q 0 15 8 -15" fill="none" stroke="#8A7460" stroke-width="3"/>')
    bear_parts.append(f'<rect x="-12" y="5" width="24" height="16" rx="6" fill="#F2B035" stroke="#C98A18" stroke-width="2.5"/>')

    e.append(f'<g transform="translate(220, 360) scale(1.1)">{"".join(bear_parts)}</g>')

    # Owen 在水裡摸池壁：boy_bust(arms="handup") 靠左
    e.append(boy_bust(expr="big", cx=140, cy=330, scale=1.0, arms="handup", jersey=('', '#4C7DD0', '#2E5AA8')))

    # 水面波浪
    e.append(f'<path d="M 80 315 Q 100 300 120 315 Q 140 330 160 315" fill="none" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>')

    # 擊掌對接點（上方外側星星處）：熊掌 translate(220,360) + scale(1.1) 中 cx=-40, cy=-80 → 實際 220-40*1.1=176, 360-80*1.1=272
    # Owen 頭約在 (140, 330+30) = (140, 360)，距離 = sqrt((176-140)^2 + (272-360)^2) = sqrt(36^2 + 88^2) = sqrt(1296+7744) = sqrt(9040) ≈ 95 > 30 ✓
    e.append(f'<circle cx="170" cy="290" r="8" fill="#FFD9B6"/>')

    # 水花星星（四周）：重新排列避開熊掌
    e.append(star(100, 290, 20, fill="#FFFFFF"))
    e.append(star(170, 280, 18, fill="#FFFFFF"))  # 靠近新擊掌點
    e.append(star(120, 380, 16, fill="#FFFFFF"))

    return svg(W, H, "".join(e))


def scene_p10():
    """p10: 英雄收尾：Owen 披紅披風站在跳水台上叉腰（泳褲＋蛙鏡推到額頭），Coach Bear 在旁比讚，滿天星"""
    e = []
    e.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG["p10"]}"/>')

    # 滿天星
    for (x, y, r) in [(120, 80, 20), (280, 70, 16), (940, 100, 22), (1060, 90, 18),
                       (180, 440, 16), (980, 420, 18), (400, 110, 14), (850, 130, 12)]:
        e.append(star(x, y, r))

    # 池水在下方（作為背景）
    e.append(f'<rect x="0" y="420" width="{W}" height="140" fill="#80DEEA" opacity="0.5"/>')

    # 跳水台：灰色平台＋雙柱，platform feet_y=360
    platform_y = 360
    e.append(f'<rect x="320" y="{platform_y-20}" width="320" height="24" rx="8" fill="#B0B0B0" stroke="#808080" stroke-width="4"/>')  # 平台板
    e.append(f'<rect x="380" y="{platform_y+4}" width="50" height="100" rx="10" fill="#9A9A9A" stroke="#707070" stroke-width="3"/>')  # 左柱
    e.append(f'<rect x="760" y="{platform_y+4}" width="50" height="100" rx="10" fill="#9A9A9A" stroke="#707070" stroke-width="3"/>')  # 右柱

    # Owen 站在跳水台上：feet_y = cy + 228*scale = 360，scale=1.1，cy = 360-228*1.1 ≈ 109
    # 用 cy 略低讓身體有足夠空間，feet_y 會自動對齐
    e.append(boy(pose="hips", expr="proud", cx=490, cy=110, scale=1.1, cape=True, jersey=('', '#4C7DD0', '#2E5AA8')))

    # 蛙鏡推到額頭：橘色帶沿瀏海上緣（弧線）+ 兩個小圓圈（黑描邊透明）
    # Owen 頭部中心約在 cx=490, cy=110+34 ≈ 144（根據 parts.py boy() 的變換）
    # 額頭區域 y ≈ 110 左右
    # 橘色帶沿瀏海（弧線貼髮際）
    e.append(f'<path d="M 430 110 Q 490 95 550 110" fill="none" stroke="#E8944A" stroke-width="6" stroke-linecap="round"/>')  # 橘色帶
    # 兩個小圓圈（鏡框）黑描邊＋透明填色
    e.append(f'<circle cx="450" cy="105" r="14" fill="#FFFFFF" fill-opacity="0.3" stroke="#161616" stroke-width="3"/>')  # 左鏡
    e.append(f'<circle cx="530" cy="105" r="14" fill="#FFFFFF" fill-opacity="0.3" stroke="#161616" stroke-width="3"/>')  # 右鏡

    # Coach Bear 在旁比讚：pose="thumbsup"，腳底貼地
    e.append(coach_bear(cx=750, cy=340, scale=1.3, pose="thumbsup"))

    return svg(W, H, "".join(e))


# ==================== PAGE TEXTS ================
PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>Today is swim day!'),
    ("p2", scene_p2, 'This is <b>Coach</b> Bear!<br/>He is big and kind.<br/>We swim with him!'),
    ("p3", scene_p3, 'I swim fast, fast!<br/>I want to zoom like a fish!'),
    ("p4", scene_p4, 'I zoom! My <b>breath</b> goes fast, fast!<br/>My arms go flat. My kicks sleep.<br/><b>Splash!</b> Water in my mouth!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I swim like Coach Bear!'),
    ("p6", scene_p6, 'Arms up <b>HIGH</b>!<br/>Quick, quick <b>breath</b>!<br/>Kick, kick, <b>splash</b>!'),
    ("p7", scene_p7, 'Coach Bear smiles.<br/>Good moves keep me safe.<br/>Good moves make me fast!'),
    ("p8", scene_p8, 'Watch me go!<br/>Arms, breath, kick!<br/>Daddy cheers, &ldquo;Super swim, <b>Owen</b>!&rdquo;'),
    ("p9", scene_p9, 'I touch the wall!<br/>Coach Bear gives me five.<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Arms up! Quick breath! Kick, kick, kick!<br/><b>Arms, breath, kick!</b><br/>I practice every day!'),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("把口訣交給真實教練", "請游泳教練用同一組詞提醒（Arms! / Breath! / Kick!），一次只喊一個字，不要整句技術講解。"),
    ("下水前先在岸上排練", "出發前站著做一次「手舉高→轉頭吸→原地踏水花」的三步操，身體先記得，水裡才提取得出來。"),
    ("當他自查動作 = 成就解鎖", "當他游完自己說出「我剛剛 arms 沒有 up」這類自查，動作覺察里程碑，比游得快更值得大力稱讚。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

BOOK = {
    "slug": "arms-breath-kick",
    "order": 12,
    "title_pre": "", "title_hi": "Arms", "title_post": ", Breath, Kick!",
    "title_zh": "手、換氣、踢水",
    "subtitle": "Owen's swimming story",
    "tagline_zh": "Owen 的游泳故事",
    "chips": ["Social Story", "Swimming", "12 pages"],
    "pdf_name": "Arms_Breath_Kick.pdf",
    "bg": BG,
    "pages": PAGES,
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。它的目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Arms up high → Quick breath → Kick, kick, splash!</b>&nbsp;"
                 "喊法：一次只喊一字（Arms! / Breath! / Kick!）。"
                 "下水前岸上排練：手舉高→轉頭吸→原地踏水花。"
                 "當他自查動作（「我剛剛 arms 沒有 up」）= 覺察里程碑，大力稱讚。"),
    "cover": scene_cover,
}
