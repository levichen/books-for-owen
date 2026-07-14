# -*- coding: utf-8 -*-
"""Book 3: My Cup Only! — 喝自己的水杯（社會故事繪本）。"""
from parts import *
from book_common import svg, svgtext, TXT, W, H
import math

# soft page palettes
BG = {
    "cover": "#FFF9E6", "p1": "#E8F4F8", "p2": "#FFF3D6", "p3": "#FFE8D6",
    "p4": "#FFEAE8", "p5": "#E6D9F8", "p6": "#F0E6FF", "p7": "#DFF7EB",
    "p8": "#FFF0C9", "p9": "#FFEDEE", "p10": "#FFF5E6", "p11": "#FBF4E8",
}

# JERSEY 常數與水壺顏色
JERSEY_39 = ('39', '#F28C3A', '#C05A1E')
BOTTLE_OWEN = '#F28C3A'   # 橘，配 39 號
BOTTLE_LUCAS = '#7BC47F'  # 綠
BOTTLE_ANN = '#F6C445'    # 黃

# ============ HELPER: bottle ============
def bottle(cx, cy, scale, name="OWEN", color="#F28C3A", faded=False):
    """運動水壺（圓柱身＋瓶蓋＋吸嘴）＋大名字貼紙（橫向，固定寬度≥壺身90%）。
    貼紙名字字級隨 scale 等比，最小有效 12pt 保證可讀（渲染寬度≥70px）。
    如 faded=True，整體灰化。"""
    b = []
    alpha = 0.4 if faded else 1.0

    # 圓柱身（水壺）寬 44 單位
    b.append(f'<rect x="-22" y="0" width="44" height="80" rx="8" fill="{color}" fill-opacity="{alpha}" stroke="#999999" stroke-width="2"/>')
    # 高光（讓壺看起來有光澤）
    if not faded:
        b.append(f'<ellipse cx="-10" cy="20" rx="6" ry="14" fill="#FFFFFF" fill-opacity="0.3"/>')

    # 瓶蓋（較小的矩形，頂部）
    b.append(f'<rect x="-12" y="-12" width="24" height="14" rx="4" fill="#333333" fill-opacity="{alpha}"/>')

    # 吸嘴（從蓋子伸出的小弧線＋球）
    b.append(f'<path d="M 0 -12 Q 8 -20 12 -28" fill="none" stroke="#333333" stroke-width="3" stroke-linecap="round" stroke-opacity="{alpha}"/>')
    b.append(f'<circle cx="12" cy="-32" r="4" fill="#333333" fill-opacity="{alpha}"/>')

    # 發光效果（OWEN 壺）——畫在貼紙之前，避免蓋到名字
    if not faded and name == "OWEN":
        b.append(f'<circle cx="0" cy="40" r="28" fill="{STAR_Y}" fill-opacity="0.15"/>')
        b.append(f'<circle cx="0" cy="40" r="18" fill="{STAR_Y}" fill-opacity="0.20"/>')

    # 名字貼紙：本函式所有元素都在同一個 scale 群組內，
    # 字級必須用「群組內固定值」——外層 scale 會一併放大，寫成 scale 相關字級會被縮放吃兩次
    sticker_width = 46
    sticker_height = 24
    b.append(f'<rect x="{-sticker_width/2}" y="48" width="{sticker_width}" height="{sticker_height}" rx="5" fill="#FFFFFF" stroke="#CCCCCC" stroke-width="1.5"/>')
    font_size = 15 if len(name) <= 4 else 12
    b.append(svgtext(0, 65, name, size=font_size, fill="#333333", weight="bold", anchor="middle"))

    inner = "".join(b)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'

# ============ HELPER: germs ============
def germ(cx, cy, scale=1.0):
    """可愛的小 germs 卡通：圓身＋2 根觸角＋兩點眼＋淘氣微笑。
    scale 調整大小（半徑 12*scale px）。"""
    g = []
    # 圓身（綠色）
    r = 12
    g.append(f'<circle cx="0" cy="0" r="{r}" fill="#7BC47F" stroke="#5A9B5C" stroke-width="2"/>')

    # 觸角（2 根，從頭頂伸出，彎曲向上）
    g.append(f'<path d="M {-r*0.35} {-r*0.8} Q {-r*0.6} {-r*1.8} {-r*0.3} {-r*2.3}" fill="none" stroke="#5A9B5C" stroke-width="{max(2, r*0.17)}" stroke-linecap="round"/>')
    g.append(f'<path d="M {r*0.35} {-r*0.8} Q {r*0.6} {-r*1.8} {r*0.3} {-r*2.3}" fill="none" stroke="#5A9B5C" stroke-width="{max(2, r*0.17)}" stroke-linecap="round"/>')

    # 觸角頂端的小球
    g.append(f'<circle cx="{-r*0.3}" cy="{-r*2.3}" r="{r*0.2}" fill="#5A9B5C"/>')
    g.append(f'<circle cx="{r*0.3}" cy="{-r*2.3}" r="{r*0.2}" fill="#5A9B5C"/>')

    # 眼睛（兩個白點，表示淘氣）
    g.append(f'<circle cx="{-r*0.4}" cy="{-r*0.15}" r="{r*0.15}" fill="#FFFFFF"/>')
    g.append(f'<circle cx="{r*0.4}" cy="{-r*0.15}" r="{r*0.15}" fill="#FFFFFF"/>')

    # 微笑（淘氣微笑弧線）
    g.append(f'<path d="M {-r*0.45} {r*0.2} Q 0 {r*0.55} {r*0.45} {r*0.2}" fill="none" stroke="#FFFFFF" stroke-width="{max(1.5, r*0.13)}" stroke-linecap="round"/>')

    inner = "".join(g)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'

# ============ SCENES ============

def scene_cover():
    """封面：Owen（39 號）中央抱著大水壺＋名字貼紙特寫＋球場氛圍"""
    e = []
    e.append(sun(1050, 110, 38))
    e.append(cloud(200, 90, 1.0)); e.append(cloud(700, 70, 0.8))
    # 星星點綴
    for (x, y, r) in [(240, 200, 20), (950, 250, 22), (420, 140, 14), (850, 380, 16), (150, 450, 16)]:
        e.append(star(x, y, r))
    e.append(sparkle(580, 110, 12)); e.append(sparkle(300, 380, 10))
    # 籃框背景（遠處）
    e.append(f'<rect x="920" y="200" width="200" height="220" rx="12" fill="#F5DCC9" stroke="#D4A57A" stroke-width="3"/>')
    e.append(f'<polygon points="920,200 1020,100 1120,200" fill="#E8574C"/>')
    e.append(f'<rect x="970" y="250" width="50" height="100" fill="#8B5E52"/>')
    # ground
    e.append(f'<ellipse cx="594" cy="640" rx="560" ry="120" fill="#FFDD7E"/>')
    # Owen 中央抱著大水壺（39 號）
    e.append(boy(pose="stand", expr="big", cx=400, cy=240, scale=1.2, jersey=JERSEY_39))
    # 大水壺在 Owen 懷裡（略低於中心）
    e.append(bottle(cx=480, cy=310, scale=1.5, name="OWEN", color=BOTTLE_OWEN))
    # 水壺發光
    e.append(f'<circle cx="480" cy="310" r="80" fill="{STAR_Y}" fill-opacity="0.12"/>')
    e.append(f'<circle cx="480" cy="310" r="50" fill="{STAR_Y}" fill-opacity="0.15"/>')
    # 音符點綴
    e.append(f'<text x="220" y="150" font-family="Arial" font-size="48" fill="#FFB700">♪</text>')
    return svg(1188, 620, "".join(e), bg=None)


def scene_p1():
    """p1：球場：Owen（39 號）運球奔跑，滿頭汗（汗滴），太陽在上"""
    e = []
    e.append(sun(1060, 90, 36))
    e.append(cloud(220, 80, 1.0)); e.append(cloud(560, 60, 0.7))
    # 球場地板線
    e.append(f'<rect x="0" y="460" width="1188" height="100" fill="#D4A574"/>')
    e.append(f'<line x1="0" y1="480" x2="1188" y2="480" stroke="#FFFFFF" stroke-width="4"/>')
    # 籃框（右側上方）
    e.append(f'<rect x="1050" y="280" width="12" height="200" fill="#8B5E52"/>')
    e.append(hoop(cx=1056, cy=280, scale=1.1))
    # 灌木
    e.append(f'<circle cx="80" cy="430" r="40" fill="#8FCB84"/><circle cx="130" cy="440" r="30" fill="#79BD6E"/>')
    # Owen 運球奔跑（39 號）
    e.append(boy(pose="run", expr="smile", cx=400, cy=200, scale=1.2, jersey=JERSEY_39))
    # 籃球在手邊
    e.append(basketball(cx=490, cy=240, r=26))
    # 汗滴（頭側）
    e.append(f'<path d="M 540 100 q 12 14 0 24 q -12 -10 0 -24 Z" fill="#8FD3F2"/>')
    e.append(f'<path d="M 560 120 q 10 12 0 20 q -10 -8 0 -20 Z" fill="#8FD3F2"/>')
    # 星星點綴
    e.append(star(180, 140, 18))
    e.append(sparkle(320, 110, 12))
    return svg(W, H, "".join(e), bg=BG["p1"])


def scene_p2():
    """p2：球場邊長凳：三個水壺排排站（OWEN／LUCAS／ANNE，各有名字貼紙），Lucas、Anne 走向"""
    e = []
    # 球場地板
    e.append(f'<rect x="0" y="460" width="1188" height="100" fill="#D4A574"/>')
    e.append(f'<line x1="0" y1="480" x2="1188" y2="480" stroke="#FFFFFF" stroke-width="4"/>')
    # 長凳（簡單線條）
    bench_y = 420
    e.append(f'<rect x="200" y="{bench_y}" width="800" height="18" rx="6" fill="#A0826D" stroke="#7A5D52" stroke-width="2"/>')
    e.append(f'<rect x="220" y="{bench_y+18}" width="14" height="40" fill="#7A5D52"/>')
    e.append(f'<rect x="760" y="{bench_y+18}" width="14" height="40" fill="#7A5D52"/>')

    # 三個水壺排排站在長凳上（OWEN / LUCAS / ANNE）
    e.append(bottle(cx=320, cy=350, scale=1.0, name="OWEN", color=BOTTLE_OWEN))
    e.append(bottle(cx=594, cy=350, scale=1.0, name="LUCAS", color=BOTTLE_LUCAS))
    e.append(bottle(cx=868, cy=350, scale=1.0, name="ANNE", color=BOTTLE_ANN))

    # Lucas 和 Anne 走向長凳（左邊 Lucas，右邊 Anne）
    e.append(lucas(cx=280, cy=310, scale=1.1, expr="smile"))
    e.append(ann(cx=920, cy=310, scale=1.1, expr="smile"))

    # 星星點綴
    e.append(star(150, 120, 20))
    e.append(star(1020, 140, 18))
    e.append(sparkle(420, 90, 12))
    e.append(sparkle(780, 100, 12))
    return svg(W, H, "".join(e), bg=BG["p2"])


def scene_p3():
    """p3：Owen 特寫（oh 表情），嘴巴乾（乾裂小線條），頭上思考泡泡是一大杯水"""
    e = []
    # 思考泡泡：三個連結圓球 + 大杯水在頂部
    e.append(f'<circle cx="580" cy="200" r="8" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
    e.append(f'<circle cx="600" cy="180" r="12" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
    e.append(f'<ellipse cx="580" cy="120" rx="50" ry="50" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="4"/>')
    # 杯子在思考泡泡內（藍色水的杯子）
    e.append(f'<rect x="540" y="90" width="80" height="60" rx="6" fill="none" stroke="#4A78A8" stroke-width="3"/>')
    e.append(f'<path d="M 550 130 L 570 150" stroke="#4A78A8" stroke-width="2.5" stroke-linecap="round"/>')  # 把手
    e.append(f'<rect x="545" y="105" width="70" height="30" fill="#8FD3F2" fill-opacity="0.6"/>')  # 水

    # Owen 特寫（oh 表情 + 嘴巴乾裂線條）
    e.append(boy_bust(expr="oh", cx=320, cy=350, scale=1.3, jersey=JERSEY_39))
    # 嘴巴乾裂線條（嘴邊）
    e.append(f'<line x1="280" y1="370" x2="275" y2="380" stroke="#C9A26B" stroke-width="2" stroke-linecap="round"/>')
    e.append(f'<line x1="360" y1="370" x2="365" y2="380" stroke="#C9A26B" stroke-width="2" stroke-linecap="round"/>')

    # 星星點綴
    e.append(star(200, 240, 20))
    e.append(star(850, 250, 22))
    e.append(sparkle(120, 120, 12))
    e.append(sparkle(1050, 320, 14))
    return svg(W, H, "".join(e), bg=BG["p3"])


def scene_p4():
    """p4 **衝動頁**：Owen 雙臂伸向右側（swing 姿勢），伸手抓 ANNE 水壺；頭上大「?」，紅熱氣線"""
    e = []
    # 熱氣線（四周蛇形）
    for (x, y) in [(200, 150), (980, 160), (180, 400), (1010, 390)]:
        e.append(f'<path d="M {x} {y} q 12 -18 24 0 q 12 18 24 0" fill="none" stroke="#F26B5E" stroke-width="10" stroke-linecap="round"/>')

    # Owen swing 姿勢（雙臂伸向右側），big 表情（渴望），39 號
    # feet_y = cy + 228*scale = 180 + 228*1.3 = 476.4（OK，≤520）
    e.append(boy(pose="swing", expr="big", cx=350, cy=180, scale=1.3, jersey=JERSEY_39))

    # swing 姿勢手的位置：(cx+88*scale, cy+50*scale) = (464.4, 245)
    # ANNE 水壺放大（scale=2.2），放在手前方 50px（手指向水壺）
    hand_x = 350 + 88 * 1.3  # 464.4
    hand_y = 180 + 50 * 1.3  # 245
    bottle_x = hand_x + 70
    bottle_y = hand_y + 60
    e.append(bottle(cx=bottle_x, cy=bottle_y, scale=2.2, name="ANNE", color=BOTTLE_ANN))

    # 手到水壺之間的速度線（3 條）
    for i in range(3):
        offset_y = (i - 1) * 10
        e.append(f'<path d="M {hand_x + 20 + i*8} {hand_y + offset_y} L {hand_x - 20 + i*8} {hand_y + offset_y}" fill="none" stroke="#F26B5E" stroke-width="6" stroke-linecap="round"/>')

    # 頭上大問號 "?"
    e.append(f'<circle cx="350" cy="40" r="32" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="3"/>')
    e.append(svgtext(350, 60, "?", size=52, fill="#E8A20C", weight="bold", anchor="middle"))

    # 跳動心臟（右側）
    e.append(f'<path d="M 1000 280 c 0 -30 44 -30 44 -2 c 0 -28 44 -28 44 2 c 0 30 -44 46 -44 60 c 0 -14 -44 -30 -44 -60 Z" fill="#F2665A" stroke="#D14A3F" stroke-width="4"/>')
    e.append(f'<path d="M 978 328 q -16 0 -20 -14 M 1110 328 q 16 0 20 -14" fill="none" stroke="#D14A3F" stroke-width="6" stroke-linecap="round"/>')

    return svg(W, H, "".join(e), bg=BG["p4"])


def scene_p5():
    """p5：紫色星空背景：Owen（press 表情）站立，手停在半空，手腕畫 STOP 光圈；視線虛線掃向發光 OWEN 貼紙"""
    e = []
    # 星空背景（紫色已在 BG，加星星）
    for (x, y, r) in [(120, 130, 18), (1050, 140, 20), (180, 420, 14), (1080, 410, 16)]:
        e.append(star(x, y, r, fill=STAR_Y))
    e.append(sparkle(320, 80, 12))
    e.append(sparkle(880, 90, 12))
    e.append(sparkle(100, 320, 10))
    e.append(sparkle(1100, 300, 10))

    # Owen 站立（press 表情 = 決定/停住）
    # feet_y = 270 + 228*1.15 = 532.2，略超 520，改用 cy=260 → feet_y=521，還是有點超，改 cy=255 → feet_y=516（OK）
    e.append(boy(pose="stand", expr="press", cx=450, cy=255, scale=1.15, jersey=JERSEY_39))

    # 手停在半空（伸出的手在身體右側，位置約 (510, 380)）
    # 手腕畫 STOP 光圈（2 層半透明圓，中心黃色小圓）
    e.append(f'<circle cx="510" cy="380" r="44" fill="{STAR_Y}" fill-opacity="0.18"/>')
    e.append(f'<circle cx="510" cy="380" r="30" fill="{STAR_Y}" fill-opacity="0.24"/>')
    e.append(f'<circle cx="510" cy="380" r="18" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="3"/>')
    # 白色 STOP 文字在圓內
    e.append(svgtext(510, 388, "STOP", size=16, fill="#FFFFFF", weight="bold", anchor="middle", family="Arial"))

    # 視線虛線（從 Owen 眼睛掃向右方的水壺）
    e.append(f'<path d="M 420 220 Q 650 250 850 300" fill="none" stroke="{STAR_DK}" stroke-width="4" stroke-dasharray="6 6" stroke-linecap="round"/>')

    # OWEN 水壺在右邊，發光
    e.append(bottle(cx=900, cy=330, scale=1.2, name="OWEN", color=BOTTLE_OWEN))

    return svg(W, H, "".join(e), bg=BG["p5"])


def scene_p6():
    """p6：三步腳本（橫列三格）：①縮手 ②貼紙對比 ③拿起自己壺"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#BFD9EE"/>')

    # 三格區域（用淡線分隔）
    grid_h = 380
    for grid_x in [396, 792]:
        e.append(f'<line x1="{grid_x}" y1="40" x2="{grid_x}" y2="{grid_h}" stroke="#DDDDDD" stroke-width="2" stroke-dasharray="3 3"/>')

    # 第一格（左）：Owen bust 縮手（小圖示）
    e.append(f'<circle cx="198" cy="150" r="28" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="4"/>')
    e.append(svgtext(198, 170, "1", size=36, fill="#4A78A8", weight="bold", anchor="middle"))
    # Owen 縮手小圖（boy_bust，arms="desk" 默認放低，或手向後）
    e.append(boy_bust(expr="press", cx=198, cy=280, scale=0.75, jersey=JERSEY_39))
    # 向後收手箭頭（粗粗的，清楚）
    e.append(f'<path d="M 80 280 L 140 280" fill="none" stroke="#E4574C" stroke-width="8" stroke-linecap="round"/>')
    e.append(f'<polygon points="80,280 100,270 100,290" fill="#E4574C"/>')

    # 第二格（中）：水壺對比（放大到 scale=2.8，寬 ~123px）
    e.append(f'<circle cx="594" cy="150" r="28" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="4"/>')
    e.append(svgtext(594, 170, "2", size=36, fill="#4A78A8", weight="bold", anchor="middle"))
    # OWEN 壺（發光，放大，左邊）
    e.append(bottle(cx=470, cy=280, scale=2.8, name="OWEN", color=BOTTLE_OWEN))
    # ANNE 壺（灰化，放大，右邊，距離夠遠不重疊）
    e.append(bottle(cx=720, cy=280, scale=2.8, name="ANNE", color=BOTTLE_ANN, faded=True))
    # 箭頭指向 OWEN 壺
    e.append(f'<path d="M 470 420 L 470 460" fill="none" stroke="{STAR_DK}" stroke-width="6" stroke-linecap="round"/>')
    e.append(f'<polygon points="470,460 462,445 478,445" fill="{STAR_DK}"/>')

    # 第三格（右）：Owen 拿起自己的壺微笑
    e.append(f'<circle cx="990" cy="150" r="28" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="4"/>')
    e.append(svgtext(990, 170, "3", size=36, fill="#4A78A8", weight="bold", anchor="middle"))
    # Owen 微笑拿壺
    e.append(boy(pose="stand", expr="smile", cx=940, cy=280, scale=1.0, jersey=JERSEY_39))
    # 水壺在手邊（scale=1.2，清楚可讀）
    e.append(bottle(cx=1020, cy=330, scale=1.2, name="OWEN", color=BOTTLE_OWEN))

    # 星星點綴
    e.append(star(1050, 100, 20))
    e.append(sparkle(150, 220, 12))
    e.append(sparkle(950, 280, 12))
    return svg(W, H, "".join(e), bg=BG["p6"])


def scene_p7():
    """p7：觀點頁：Anne 的水壺上有 2-3 隻放大的可愛 germs，Owen 的水壺乾淨發亮"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#DFF7EB"/>')

    # ANNE 的水壺（左邊，放大到 scale=3.2，高度 ~256px）
    ann_x, ann_y = 310, 280
    e.append(bottle(cx=ann_x, cy=ann_y, scale=3.2, name="ANNE", color=BOTTLE_ANN))

    # 在 ANNE 壺上「坐」2-3 隻 germs（大一點，半徑 ~20px）
    # 水壺坐標系：壺身上邊 y≈-80*3.2+280=-16，下邊 y≈80*3.2+280=536
    # germs 位置調整（坐在壺身和瓶蓋上，不飄在空中）
    germs_scale = 1.67  # 12*1.67 ≈ 20px
    germs_positions = [
        (ann_x - 30, ann_y - 100, germs_scale),  # 瓶蓋附近左邊
        (ann_x + 25, ann_y - 80, germs_scale),   # 瓶蓋附近右邊
        (ann_x - 10, ann_y + 40, germs_scale),   # 壺身中段
    ]
    for gx, gy, gs in germs_positions[:3]:
        e.append(germ(cx=gx, cy=gy, scale=gs))

    # OWEN 的水壺（右邊，放大到 scale=3.2，高度 ~256px，乾淨發亮）
    owen_x, owen_y = 880, 280
    e.append(bottle(cx=owen_x, cy=owen_y, scale=3.2, name="OWEN", color=BOTTLE_OWEN))
    # 發光效果（多層光圈）
    e.append(f'<circle cx="{owen_x}" cy="{owen_y}" r="130" fill="{STAR_Y}" fill-opacity="0.12"/>')
    e.append(f'<circle cx="{owen_x}" cy="{owen_y}" r="90" fill="{STAR_Y}" fill-opacity="0.16"/>')
    e.append(f'<circle cx="{owen_x}" cy="{owen_y}" r="50" fill="{STAR_Y}" fill-opacity="0.20"/>')

    # sparkles 環繞 OWEN 壺
    e.append(sparkle(owen_x - 100, owen_y - 120, 16))
    e.append(sparkle(owen_x + 100, owen_y - 120, 16))
    e.append(sparkle(owen_x - 90, owen_y + 130, 14))
    e.append(sparkle(owen_x + 90, owen_y + 130, 14))

    # 星星點綴（背景）
    e.append(star(150, 100, 20))
    e.append(star(1040, 120, 22))
    e.append(sparkle(250, 420, 10))
    e.append(sparkle(1050, 380, 12))
    return svg(W, H, "".join(e), bg=BG["p7"])


def scene_p8():
    """p8：April 蹲低指著 OWEN 名字貼紙，語音泡泡 "That one is yours, Owen!"，Owen 舉起壺"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#FFF0C9"/>')

    # April 蹲低（用 scale 縮小並放低）
    e.append(april(cx=250, cy=320, scale=0.95, pose="stand"))
    # April 的手指向右邊
    e.append(f'<path d="M 300 280 L 420 260" stroke="{SKIN}" stroke-width="8" stroke-linecap="round"/>')
    e.append(f'<circle cx="420" cy="258" r="8" fill="{SKIN}"/>')

    # April 的語音泡泡
    e.append(f'<path d="M 200 140 Q 200 100 280 100 L 480 100 Q 540 100 540 150 Q 540 200 480 200 L 350 200 L 300 240 L 320 200 L 280 200 Q 200 200 200 140 Z" fill="#FFFFFF" stroke="#E3C98F" stroke-width="4"/>')
    e.append(svgtext(370, 140, "That one is", size=24, fill="#D97706", weight="bold", anchor="middle"))
    e.append(svgtext(370, 165, "yours, Owen!", size=24, fill="#D97706", weight="bold", anchor="middle"))

    # Owen 舉起水壺（handup 動作）
    e.append(boy(pose="handup", expr="big", cx=750, cy=240, scale=1.2, jersey=JERSEY_39))
    # 水壺在舉起的手上方
    e.append(bottle(cx=850, cy=200, scale=1.0, name="OWEN", color=BOTTLE_OWEN))

    # 星星加油
    e.append(star(600, 180, 18))
    e.append(sparkle(900, 140, 12))
    return svg(W, H, "".join(e), bg=BG["p8"])


def scene_p9():
    """p9：Owen 大口喝水（頭仰起、水壺舉高、gulp 泡泡文字），Lucas、Anne 各自拿自己壺乾杯"""
    e = []
    # 背景
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#FFEDEE"/>')

    # Owen 大口喝水（jump 騰空姿勢，big 表情，舉高水壺）
    # feet_y = 200 + 214*1.2 = 456.8（OK）
    e.append(boy(pose="jump", expr="big", cx=550, cy=200, scale=1.2, jersey=JERSEY_39))
    # 水壺舉到嘴邊（高位置）
    e.append(bottle(cx=620, cy=140, scale=1.0, name="OWEN", color=BOTTLE_OWEN))

    # gulp 泡泡文字（喉嚨位置）
    e.append(f'<ellipse cx="620" cy="240" rx="30" ry="22" fill="#FFFFFF" stroke="#F49AB5" stroke-width="3"/>')
    e.append(svgtext(620, 248, "gulp!", size=22, fill="#F26B5E", weight="bold", anchor="middle"))

    # Lucas 左邊拿自己的壺
    e.append(lucas(cx=200, cy=300, scale=1.1, expr="smile"))
    e.append(bottle(cx=280, cy=280, scale=0.95, name="LUCAS", color=BOTTLE_LUCAS))

    # Anne 右邊拿自己的壺
    e.append(ann(cx=950, cy=300, scale=1.1, expr="smile"))
    e.append(bottle(cx=870, cy=280, scale=0.95, name="ANNE", color=BOTTLE_ANN))

    # 星星點綴
    e.append(star(400, 150, 20))
    e.append(sparkle(750, 90, 12))
    e.append(sparkle(920, 380, 12))
    return svg(W, H, "".join(e), bg=BG["p9"])


def scene_p10():
    """p10：英雄收尾：Owen 披紅披風叉腰（39 號），另一手舉著發光 OWEN 水壺，滿天星"""
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
    e.append(boy(pose="hips", expr="proud", cx=594, cy=160, scale=1.3, cape=True, jersey=JERSEY_39))

    # 另一隻手舉著發光的 OWEN 水壺
    # hips 姿勢兩隻手都在兩側，我們在右手位置畫水壺
    e.append(bottle(cx=750, cy=180, scale=1.1, name="OWEN", color=BOTTLE_OWEN))

    return svg(W, H, "".join(e), bg=BG["p10"])


# ============ PAGES ============
PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I play hard.<br/>I get SO <b>thirsty</b>!'),
    ("p2", scene_p2, 'Water break!<br/><b>Bottles</b> sit in a row.<br/>Lucas, Anne, and me!'),
    ("p3", scene_p3, 'I am so thirsty!<br/>My mouth is dry, dry, dry!'),
    ("p4", scene_p4, 'My mouth feels dry.<br/>My hands <b>grab, grab, grab</b>!<br/>Wait&mdash;whose bottle is this?'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I look for my <b>name</b>!'),
    ("p6", scene_p6, 'I stop my hands.<br/>I find my name.<br/><b>My cup only!</b>'),
    ("p7", scene_p7, 'Anne\'s bottle has Anne\'s <b>germs</b>.<br/>Germs can make me sick.<br/>My bottle is just for me!'),
    ("p8", scene_p8, 'Mom April smiles.<br/>&ldquo;That one is yours, <b>Owen</b>!&rdquo;<br/>I found my name!'),
    ("p9", scene_p9, '<b>Gulp, gulp!</b> Cold water!<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Stop. Find my name.<br/><b>My cup only!</b><br/>I practice every day!'),
]

# ============ PARENT TIPS ============
PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("書裡的樣子＝現實的樣子", "Owen 的水壺請貼上大大的名字貼紙（和書裡同款式最好），學校水壺、家裡杯子都貼。腳本依賴「找名字」這個動作，名字不在就無從練習。"),
    ("germs 講衛生不講嫌惡", "p7 的 germs 是「Anne 的小夥伴住在 Anne 的瓶子」，不是「別人的東西很髒」——別把腳本教成排斥別人。"),
    ("當他主動問『誰的杯子？』時大力稱讚", "拿之前先問 &ldquo;Whose bottle is this?&rdquo; = 腳本啟動的訊號，是最值得鼓勵的時刻。"),
    ("搭配每日聯絡卡", "請老師每天打勾 2&ndash;3 條「有沒有喝對杯子」；當天達標 → 當天兌現小獎勵。"),
]

# ============ BOOK DICT ============
BOOK = {
    "slug": "my-cup-only",
    "order": 8,
    "title_pre": "My ", "title_hi": "Cup", "title_post": " Only!",
    "title_zh": "只喝我的杯子",
    "subtitle": "Owen's water break story",
    "tagline_zh": "Owen 的喝水故事",
    "chips": ["Social Story", "Health", "12 pages"],
    "pdf_name": "My_Cup_Only.pdf",
    "bg": BG,
    "pages": PAGES,
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。目標不是「講道理」，"
                     "而是替 Owen 安裝一套<b>當下用得出來的喝水認杯腳本</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Stop → Find my name → My cup only!</b>&nbsp;"
                 "當他哪天主動問出 &ldquo;Whose bottle is this?&rdquo;（拿之前先問），"
                 "就是最值得大力稱讚的時刻。"),
    "cover": scene_cover,
}
