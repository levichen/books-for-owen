# -*- coding: utf-8 -*-
"""Reusable SVG parts for the picture book character (cartoon boy based on photos:
round black glasses w/ orange temples, straight bangs, white army-print tee, red backpack)."""
import math

SKIN = "#FFD9B6"
SKIN_DK = "#F3C69B"
HAIR = "#2A2320"
LINE = "#33291F"
BLUSH = "#FFB3A0"
TEE = "#FFFFFF"
TEE_LINE = "#E4DCD2"
PRINT_GREEN = "#7B8F5A"
SHORTS = "#4C5445"
SHORTS_DK = "#3C443A"
BAG_RED = "#E4574C"
BAG_NAVY = "#2E3E66"
STRAP = "#BDB6A9"
STAR_Y = "#FFC93C"
STAR_DK = "#E8A20C"

def star_pts(cx, cy, r, r2=None, n=5, rot=-90):
    r2 = r2 if r2 else r * 0.45
    pts = []
    for i in range(n * 2):
        rr = r if i % 2 == 0 else r2
        a = math.radians(rot + i * 180.0 / n)
        pts.append(f"{cx + rr*math.cos(a):.1f},{cy + rr*math.sin(a):.1f}")
    return " ".join(pts)

def star(cx, cy, r, fill=STAR_Y, stroke=STAR_DK, sw=3, face=False):
    s = f'<polygon points="{star_pts(cx,cy,r)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'
    if face:
        s += f'<circle cx="{cx-r*0.22:.0f}" cy="{cy:.0f}" r="{r*0.07:.1f}" fill="{LINE}"/>'
        s += f'<circle cx="{cx+r*0.22:.0f}" cy="{cy:.0f}" r="{r*0.07:.1f}" fill="{LINE}"/>'
        s += f'<path d="M {cx-r*0.16:.0f} {cy+r*0.18:.0f} Q {cx:.0f} {cy+r*0.34:.0f} {cx+r*0.16:.0f} {cy+r*0.18:.0f}" fill="none" stroke="{LINE}" stroke-width="{max(2,r*0.06):.1f}" stroke-linecap="round"/>'
    return s

def sparkle(cx, cy, r, fill=STAR_Y):
    return (f'<path d="M {cx} {cy-r} Q {cx+r*0.18} {cy-r*0.18} {cx+r} {cy} '
            f'Q {cx+r*0.18} {cy+r*0.18} {cx} {cy+r} Q {cx-r*0.18} {cy+r*0.18} {cx-r} {cy} '
            f'Q {cx-r*0.18} {cy-r*0.18} {cx} {cy-r} Z" fill="{fill}"/>')

def cloud(cx, cy, s=1.0, fill="#FFFFFF", op=0.95):
    return (f'<g transform="translate({cx},{cy}) scale({s})" fill="{fill}" fill-opacity="{op}">'
            f'<ellipse cx="0" cy="0" rx="46" ry="22"/><circle cx="-26" cy="-10" r="18"/>'
            f'<circle cx="2" cy="-18" r="22"/><circle cx="28" cy="-8" r="16"/></g>')

def sun(cx, cy, r=34):
    rays = ""
    for i in range(8):
        a = math.radians(i * 45)
        x1, y1 = cx + (r+8)*math.cos(a), cy + (r+8)*math.sin(a)
        x2, y2 = cx + (r+20)*math.cos(a), cy + (r+20)*math.sin(a)
        rays += f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{STAR_Y}" stroke-width="7" stroke-linecap="round"/>'
    return f'{rays}<circle cx="{cx}" cy="{cy}" r="{r}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="3"/>'

# ---------------- HEAD ----------------
def head(expr="smile", scale=1.0, cx=0, cy=0):
    """expr: smile | big | star | hold | press | proud | oh | think"""
    e = []
    # ears
    e.append(f'<circle cx="-56" cy="6" r="12" fill="{SKIN}"/>')
    e.append(f'<circle cx="56" cy="6" r="12" fill="{SKIN}"/>')
    # face
    e.append(f'<ellipse cx="0" cy="0" rx="56" ry="52" fill="{SKIN}"/>')
    # hair dome + straight bangs with soft notches (like the photos)
    e.append(f'<path d="M -56 6 C -60 -62 60 -62 56 6 L 56 -6 '
             f'Q 44 -22 34 -14 Q 24 -24 12 -16 Q 0 -26 -12 -16 Q -24 -24 -34 -14 Q -44 -22 -56 -6 Z" fill="{HAIR}"/>')
    # side hair
    e.append(f'<path d="M -56 -4 Q -60 10 -54 18 L -48 6 Z" fill="{HAIR}"/>')
    e.append(f'<path d="M 56 -4 Q 60 10 54 18 L 48 6 Z" fill="{HAIR}"/>')
    # glasses (signature): round black frames + orange temples
    e.append(f'<line x1="-50" y1="-2" x2="-56" y2="2" stroke="#E8944A" stroke-width="6" stroke-linecap="round"/>')
    e.append(f'<line x1="50" y1="-2" x2="56" y2="2" stroke="#E8944A" stroke-width="6" stroke-linecap="round"/>')
    e.append(f'<circle cx="-27" cy="0" r="22" fill="#FFFFFF" fill-opacity="0.25" stroke="#161616" stroke-width="7"/>')
    e.append(f'<circle cx="27" cy="0" r="22" fill="#FFFFFF" fill-opacity="0.25" stroke="#161616" stroke-width="7"/>')
    e.append(f'<path d="M -6 -2 Q 0 -7 6 -2" fill="none" stroke="#161616" stroke-width="6" stroke-linecap="round"/>')

    # brows / eyes / mouth per expression
    if expr in ("smile", "proud"):
        e.append(f'<path d="M -36 -26 Q -27 -31 -18 -26" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 18 -26 Q 27 -31 36 -26" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M -34 2 Q -27 -7 -20 2" fill="none" stroke="{LINE}" stroke-width="5.5" stroke-linecap="round"/>')
        e.append(f'<path d="M 20 2 Q 27 -7 34 2" fill="none" stroke="{LINE}" stroke-width="5.5" stroke-linecap="round"/>')
    elif expr == "big":  # open excited eyes
        e.append(f'<path d="M -36 -27 Q -27 -33 -18 -27" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 18 -27 Q 27 -33 36 -27" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<circle cx="-27" cy="0" r="6" fill="{LINE}"/><circle cx="27" cy="0" r="6" fill="{LINE}"/>')
        e.append(f'<circle cx="-25" cy="-2" r="2" fill="#FFF"/><circle cx="29" cy="-2" r="2" fill="#FFF"/>')
    elif expr == "star":
        e.append(f'<path d="M -36 -27 Q -27 -33 -18 -27" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 18 -27 Q 27 -33 36 -27" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<polygon points="{star_pts(-27,0,10)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="2"/>')
        e.append(f'<polygon points="{star_pts(27,0,10)}" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="2"/>')
    elif expr == "hold":  # puffed cheeks, squeezed shut eyes — holding it in!
        e.append(f'<path d="M -37 -29 Q -27 -24 -18 -29" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 18 -29 Q 27 -24 37 -29" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M -34 0 Q -27 5 -20 0" fill="none" stroke="{LINE}" stroke-width="5.5" stroke-linecap="round"/>')
        e.append(f'<path d="M 20 0 Q 27 5 34 0" fill="none" stroke="{LINE}" stroke-width="5.5" stroke-linecap="round"/>')
    elif expr == "press":  # determined pout (photo #1!)
        e.append(f'<path d="M -36 -30 Q -27 -26 -18 -28" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 18 -28 Q 27 -26 36 -30" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<circle cx="-27" cy="0" r="5.5" fill="{LINE}"/><circle cx="27" cy="0" r="5.5" fill="{LINE}"/>')
    elif expr == "oh":
        e.append(f'<path d="M -36 -28 Q -27 -33 -18 -28" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 18 -28 Q 27 -33 36 -28" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<circle cx="-27" cy="0" r="5.5" fill="{LINE}"/><circle cx="27" cy="0" r="5.5" fill="{LINE}"/>')
    elif expr == "think":
        e.append(f'<path d="M -36 -27 Q -27 -31 -18 -27" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 18 -27 Q 27 -31 36 -27" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<circle cx="-27" cy="0" r="5" fill="{LINE}"/><circle cx="27" cy="0" r="5" fill="{LINE}"/>')
    elif expr == "sleep":  # 安詳閉眼（睡覺/被窩），眉毛放鬆
        e.append(f'<path d="M -36 -27 Q -27 -30 -18 -27" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 18 -27 Q 27 -30 36 -27" fill="none" stroke="{HAIR}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M -34 2 Q -27 8 -20 2" fill="none" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>')
        e.append(f'<path d="M 20 2 Q 27 8 34 2" fill="none" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>')

    # nose
    e.append(f'<path d="M -3 14 Q 0 18 3 14" fill="none" stroke="{SKIN_DK}" stroke-width="4" stroke-linecap="round"/>')

    # blush
    e.append(f'<ellipse cx="-40" cy="18" rx="9" ry="6" fill="{BLUSH}" fill-opacity="0.75"/>')
    e.append(f'<ellipse cx="40" cy="18" rx="9" ry="6" fill="{BLUSH}" fill-opacity="0.75"/>')

    # mouths
    if expr == "smile":
        e.append(f'<path d="M -18 26 Q 0 42 18 26 Q 0 34 -18 26 Z" fill="#8C4A3C"/>')
        e.append(f'<path d="M -14 27 Q 0 33 14 27 L 12 30 Q 0 35 -12 30 Z" fill="#FFFFFF"/>')
    elif expr in ("big", "star"):
        e.append(f'<path d="M -20 24 A 20 16 0 0 0 20 24 Z" fill="#8C4A3C"/>')
        e.append(f'<rect x="-14" y="24" width="28" height="5" rx="2.5" fill="#FFFFFF"/>')
        e.append(f'<path d="M -10 38 Q 0 44 10 38 Q 0 48 -10 38 Z" fill="#E8837A"/>')
    elif expr == "hold":
        # puffed cheeks + tight wavy mouth
        e.append(f'<ellipse cx="-44" cy="24" rx="12" ry="10" fill="{SKIN_DK}" fill-opacity="0.55"/>')
        e.append(f'<ellipse cx="44" cy="24" rx="12" ry="10" fill="{SKIN_DK}" fill-opacity="0.55"/>')
        e.append(f'<path d="M -14 30 q 7 5 14 0 q 7 -5 14 0" fill="none" stroke="{LINE}" stroke-width="5.5" stroke-linecap="round"/>')
    elif expr == "press":
        # the pout from photo 1: pressed lips slightly down + chin bump
        e.append(f'<path d="M -16 29 Q 0 24 16 29" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>')
        e.append(f'<path d="M -6 40 Q 0 43 6 40" fill="none" stroke="{SKIN_DK}" stroke-width="4" stroke-linecap="round"/>')
    elif expr == "proud":
        e.append(f'<path d="M -14 28 Q 0 38 14 28" fill="none" stroke="{LINE}" stroke-width="6" stroke-linecap="round"/>')
    elif expr == "sleep":
        e.append(f'<path d="M -8 30 Q 0 34 8 30" fill="none" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>')
    elif expr == "oh":
        e.append(f'<ellipse cx="0" cy="30" rx="8" ry="10" fill="#8C4A3C"/>')
    elif expr == "think":
        e.append(f'<path d="M -10 30 Q 0 33 10 30" fill="none" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>')

    inner = "".join(e)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


# ---------------- BODY POSES ----------------
def tee_print():
    return (f'<g><rect x="-16" y="8" width="32" height="34" rx="4" fill="none" stroke="{PRINT_GREEN}" stroke-width="3"/>'
            f'<rect x="-9" y="14" width="7" height="10" rx="2" fill="{PRINT_GREEN}"/>'
            f'<rect x="3" y="16" width="7" height="10" rx="2" fill="{PRINT_GREEN}"/>'
            f'<rect x="-4" y="29" width="8" height="8" rx="2" fill="{PRINT_GREEN}"/></g>')

def boy(pose="stand", expr="smile", scale=1.0, cx=0, cy=0, backpack=False, cape=False, jersey=None):
    """pose: stand | walk | handup | hips | wave | jump | swing | run
    jersey: (號碼字串, 底色, 深色描邊) — 球場頁球衣蓋掉白T；眼鏡/瀏海/短褲不變。
    落地公式：stand/handup/hips/wave/swing feet_y = cy+228*scale；
    walk/run 前腳約 cy+228*scale；jump 為騰空姿勢，腳底約 cy+214*scale。"""
    b = []
    # cape (behind everything)
    if cape:
        b.append(f'<path d="M -46 96 Q -78 170 -58 224 L 58 224 Q 78 170 46 96 Z" fill="#E4574C"/>')
        b.append(f'<path d="M -46 96 Q -78 170 -58 224 L 58 224 Q 78 170 46 96" fill="none" stroke="#C74338" stroke-width="4"/>')
    # backpack behind
    if backpack:
        b.append(f'<rect x="-58" y="100" width="42" height="66" rx="16" fill="{BAG_RED}"/>')
        b.append(f'<rect x="-58" y="142" width="42" height="24" rx="10" fill="{BAG_NAVY}"/>')
        b.append(f'<rect x="16" y="100" width="42" height="66" rx="16" fill="{BAG_RED}"/>')
        b.append(f'<rect x="16" y="142" width="42" height="24" rx="10" fill="{BAG_NAVY}"/>')

    # legs + shoes
    if pose == "walk":
        b.append(f'<path d="M -14 210 L -22 252" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<path d="M 14 210 L 26 246" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<ellipse cx="-26" cy="258" rx="17" ry="10" fill="#C9BFA8"/>')
        b.append(f'<ellipse cx="31" cy="252" rx="17" ry="10" fill="#C9BFA8"/>')
    elif pose == "jump":  # 騰空：膝蓋微收
        b.append(f'<path d="M -14 208 Q -30 222 -22 236" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<path d="M 14 208 Q 30 222 22 236" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<ellipse cx="-26" cy="242" rx="16" ry="10" fill="#C9BFA8"/>')
        b.append(f'<ellipse cx="26" cy="242" rx="16" ry="10" fill="#C9BFA8"/>')
    elif pose == "run":  # 跑：前腳踏地、後腳後勾
        b.append(f'<path d="M 14 206 L 40 240" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<path d="M -14 206 Q -36 216 -52 206" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<ellipse cx="46" cy="248" rx="17" ry="10" fill="#C9BFA8"/>')
        b.append(f'<ellipse cx="-60" cy="208" rx="15" ry="10" fill="#C9BFA8" transform="rotate(-24 -60 208)"/>')
    elif pose == "kick":  # 踢球：左腳站立、右腳前踢（球由場景畫在腳尖 (cx+72s, cy+160s) 附近）
        b.append(f'<path d="M -14 210 L -14 252" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<ellipse cx="-16" cy="258" rx="17" ry="10" fill="#C9BFA8"/>')
        b.append(f'<path d="M 14 206 Q 44 208 62 186" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<ellipse cx="70" cy="182" rx="16" ry="10" fill="#C9BFA8" transform="rotate(-34 70 182)"/>')
    else:
        b.append(f'<path d="M -14 210 L -14 252" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<path d="M 14 210 L 14 252" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<ellipse cx="-16" cy="258" rx="17" ry="10" fill="#C9BFA8"/>')
        b.append(f'<ellipse cx="16" cy="258" rx="17" ry="10" fill="#C9BFA8"/>')

    # shorts (camo)
    b.append(f'<path d="M -34 178 L 34 178 L 38 222 L 8 222 L 0 200 L -8 222 L -38 222 Z" fill="{SHORTS}"/>')
    b.append(f'<circle cx="-18" cy="196" r="6" fill="{SHORTS_DK}"/><circle cx="16" cy="208" r="7" fill="{SHORTS_DK}"/><circle cx="4" cy="188" r="5" fill="{SHORTS_DK}"/>')

    # torso: jersey（球衣＋號碼）或招牌白 T
    if jersey:
        jnum, jfill, jline = jersey
        b.append(f'<path d="M -40 96 Q 0 84 40 96 L 46 118 Q 50 124 42 128 L 38 122 L 38 182 L -38 182 L -38 122 L -42 128 Q -50 124 -46 118 Z" fill="{jfill}" stroke="{jline}" stroke-width="3"/>')
        b.append(f'<path d="M -40 96 Q 0 110 40 96" fill="none" stroke="{jline}" stroke-width="4"/>')  # 領口
        fs = 46 if len(jnum) <= 2 else 36
        b.append(f'<text x="0" y="152" font-family="Huninn" font-size="{fs}" font-weight="bold" fill="#FFFFFF" stroke="{jline}" stroke-width="1.5" text-anchor="middle">{jnum}</text>')
    else:
        b.append(f'<path d="M -40 96 Q 0 84 40 96 L 46 118 Q 50 124 42 128 L 38 122 L 38 182 L -38 182 L -38 122 L -42 128 Q -50 124 -46 118 Z" fill="{TEE}" stroke="{TEE_LINE}" stroke-width="3"/>')
        b.append(f'<g transform="translate(0,116)">{tee_print()}</g>')

    # straps if backpack
    if backpack:
        b.append(f'<path d="M -26 96 L -20 178" stroke="{STRAP}" stroke-width="12" stroke-linecap="round"/>')
        b.append(f'<path d="M 26 96 L 20 178" stroke="{STRAP}" stroke-width="12" stroke-linecap="round"/>')

    # arms (pre-head; raised arms for handup/wave are drawn after the head)
    if pose == "handup":
        b.append(f'<path d="M -40 106 Q -58 140 -50 164" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="-50" cy="168" r="12" fill="{SKIN}"/>')
    elif pose == "hips":
        b.append(f'<path d="M -40 106 Q -66 128 -44 150" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<path d="M 40 106 Q 66 128 44 150" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
    elif pose == "wave":
        b.append(f'<path d="M -40 106 Q -58 140 -50 164" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="-50" cy="168" r="12" fill="{SKIN}"/>')
    elif pose == "walk":
        b.append(f'<path d="M -40 106 Q -60 132 -52 158" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="-52" cy="162" r="11" fill="{SKIN}"/>')
        b.append(f'<path d="M 40 106 Q 60 126 56 152" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="56" cy="156" r="11" fill="{SKIN}"/>')
    elif pose == "swing":  # 揮棒：雙臂走胸前低位再伸向右側，避開臉；雙手交疊在 (90,78) 附近
        b.append(f'<path d="M -40 106 Q 10 118 84 84" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<path d="M 40 106 Q 68 104 88 88" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="88" cy="80" r="12" fill="{SKIN}"/><circle cx="96" cy="90" r="11" fill="{SKIN}"/>')
    elif pose == "run":  # 跑：前臂前擺、後臂後擺
        b.append(f'<path d="M 40 106 Q 76 94 92 68" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="94" cy="62" r="11" fill="{SKIN}"/>')
        b.append(f'<path d="M -40 106 Q -68 128 -80 150" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="-82" cy="154" r="11" fill="{SKIN}"/>')
    elif pose == "jump":
        pass  # 雙手都畫在 head 之後
    elif pose == "kick":  # 平衡手：左臂後擺、右臂側舉
        b.append(f'<path d="M -40 106 Q -72 122 -86 144" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="-88" cy="148" r="11" fill="{SKIN}"/>')
        b.append(f'<path d="M 40 106 Q 72 96 90 78" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="92" cy="72" r="11" fill="{SKIN}"/>')
    else:  # stand
        b.append(f'<path d="M -40 106 Q -54 138 -48 162" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="-48" cy="166" r="11" fill="{SKIN}"/>')
        b.append(f'<path d="M 40 106 Q 54 138 48 162" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="48" cy="166" r="11" fill="{SKIN}"/>')

    # head
    b.append(head(expr=expr, cy=34, cx=0, scale=1.0))

    # post-head raised arm: clearly ABOVE the head
    if pose == "handup":
        b.append(f'<path d="M 44 104 Q 98 24 76 -56" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="74" cy="-64" r="13" fill="{SKIN}"/>')
        b.append(sparkle(98, -82, 12) + sparkle(52, -92, 8))
    elif pose == "wave":
        b.append(f'<path d="M 42 102 Q 86 56 88 -18" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="88" cy="-26" r="13" fill="{SKIN}"/>')
    elif pose == "jump":  # 雙手高舉過頭（上籃/歡呼），弧線外推避開臉
        b.append(f'<path d="M 44 104 Q 98 24 76 -56" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="74" cy="-64" r="13" fill="{SKIN}"/>')
        b.append(f'<path d="M -44 104 Q -98 24 -76 -56" stroke="{SKIN}" stroke-width="17" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="-74" cy="-64" r="13" fill="{SKIN}"/>')
    inner = "".join(b)
    # head placed: head center at y≈34; body shoulders at 96
    return f'<g transform="translate({cx},{cy}) scale({scale})"><g transform="translate(0,-30)">{inner}</g></g>'


def boy_bust(expr="smile", scale=1.0, cx=0, cy=0, arms="desk", jersey=None):
    """Bust for desk/close-up scenes: head + shoulders + arms. jersey 同 boy()。"""
    b = []
    if jersey:
        jnum, jfill, jline = jersey
        b.append(f'<path d="M -46 96 Q 0 82 46 96 L 52 150 L -52 150 Z" fill="{jfill}" stroke="{jline}" stroke-width="3"/>')
        b.append(f'<path d="M -46 96 Q 0 108 46 96" fill="none" stroke="{jline}" stroke-width="4"/>')
        fs = 34 if len(jnum) <= 2 else 27
        b.append(f'<text x="0" y="136" font-family="Huninn" font-size="{fs}" font-weight="bold" fill="#FFFFFF" stroke="{jline}" stroke-width="1.2" text-anchor="middle">{jnum}</text>')
    else:
        b.append(f'<path d="M -46 96 Q 0 82 46 96 L 52 150 L -52 150 Z" fill="{TEE}" stroke="{TEE_LINE}" stroke-width="3"/>')
        b.append(f'<g transform="translate(0,112) scale(0.9)">{tee_print()}</g>')
    if arms == "desk":
        b.append(f'<path d="M -46 104 Q -70 128 -58 148" stroke="{SKIN}" stroke-width="16" stroke-linecap="round" fill="none"/>')
        b.append(f'<path d="M 46 104 Q 70 128 58 148" stroke="{SKIN}" stroke-width="16" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="-56" cy="150" r="11" fill="{SKIN}"/><circle cx="56" cy="150" r="11" fill="{SKIN}"/>')
    elif arms == "handup":
        b.append(f'<path d="M -46 104 Q -70 128 -58 148" stroke="{SKIN}" stroke-width="16" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="-56" cy="150" r="11" fill="{SKIN}"/>')
        b.append(f'<path d="M 48 102 Q 72 56 66 14" stroke="{SKIN}" stroke-width="16" stroke-linecap="round" fill="none"/>')
        b.append(f'<circle cx="65" cy="6" r="12" fill="{SKIN}"/>')
    b.append(head(expr=expr, cy=30, scale=1.0))
    inner = "".join(b)
    return f'<g transform="translate({cx},{cy}) scale({scale})"><g transform="translate(0,-40)">{inner}</g></g>'


# ---------------- OTHER CHARACTERS ----------------
def teacher(cx=0, cy=0, scale=1.0, point="right", expr="smile"):
    t = []
    # dress
    t.append(f'<path d="M -34 70 Q 0 58 34 70 L 46 178 L -46 178 Z" fill="#6FA8DC"/>')
    # arms
    if point == "right":
        t.append(f'<path d="M 32 84 Q 74 70 96 50" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
        t.append(f'<circle cx="100" cy="46" r="10" fill="{SKIN}"/>')
        t.append(f'<path d="M -32 84 Q -50 116 -42 140" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
        t.append(f'<circle cx="-42" cy="144" r="9" fill="{SKIN}"/>')
    else:
        t.append(f'<path d="M -32 84 Q -74 70 -96 50" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
        t.append(f'<circle cx="-100" cy="46" r="10" fill="{SKIN}"/>')
        t.append(f'<path d="M 32 84 Q 50 116 42 140" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
        t.append(f'<circle cx="42" cy="144" r="9" fill="{SKIN}"/>')
    # legs
    t.append(f'<path d="M -14 178 L -14 206" stroke="{SKIN}" stroke-width="12" stroke-linecap="round"/>')
    t.append(f'<path d="M 14 178 L 14 206" stroke="{SKIN}" stroke-width="12" stroke-linecap="round"/>')
    t.append(f'<ellipse cx="-15" cy="212" rx="13" ry="7" fill="#8B5E52"/><ellipse cx="15" cy="212" rx="13" ry="7" fill="#8B5E52"/>')
    # head
    t.append(f'<circle cx="0" cy="20" r="40" fill="{SKIN}"/>')
    t.append(f'<path d="M -40 14 C -42 -30 42 -30 40 14 L 40 4 Q 20 -14 0 -8 Q -20 -14 -40 4 Z" fill="#4A3A33"/>')
    t.append(f'<circle cx="0" cy="-26" r="16" fill="#4A3A33"/>')
    t.append(f'<circle cx="-14" cy="18" r="4" fill="{LINE}"/><circle cx="14" cy="18" r="4" fill="{LINE}"/>')
    t.append(f'<path d="M -10 34 Q 0 42 10 34" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
    t.append(f'<ellipse cx="-26" cy="30" rx="7" ry="4" fill="{BLUSH}" fill-opacity="0.7"/>')
    t.append(f'<ellipse cx="26" cy="30" rx="7" ry="4" fill="{BLUSH}" fill-opacity="0.7"/>')
    inner = "".join(t)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def kid(variant=0, cx=0, cy=0, scale=1.0, expr="think"):
    """Simple friend characters (no glasses, different hair/colors).
    variant: 0=Anne(雙馬尾黃衣) 1=Lucas(捲髮綠衣) 2=bob女孩粉衣 3=Ethan(刺蝟頭藍衣)"""
    shirt = ["#F6C445", "#7BC47F", "#F49AB5", "#5CA8E8"][variant % 4]
    hairc = ["#5A4632", "#20201F", "#7A4A2C", "#3A2E24"][variant % 4]
    skin = ["#FFD9B6", "#E8B98C", "#FFD9B6", "#FFD9B6"][variant % 4]
    k = []
    k.append(f'<path d="M -34 78 Q 0 66 34 78 L 38 150 L -38 150 Z" fill="{shirt}"/>')
    k.append(f'<path d="M -34 86 Q -52 108 -44 128" stroke="{skin}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    k.append(f'<path d="M 34 86 Q 52 108 44 128" stroke="{skin}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    k.append(f'<circle cx="0" cy="16" r="42" fill="{skin}"/>')
    if variant % 4 == 0:  # girl twin tails
        k.append(f'<path d="M -42 10 C -44 -34 44 -34 42 10 L 42 0 Q 0 -18 -42 0 Z" fill="{hairc}"/>')
        k.append(f'<circle cx="-46" cy="18" r="12" fill="{hairc}"/><circle cx="46" cy="18" r="12" fill="{hairc}"/>')
    elif variant % 4 == 1:  # curly boy
        k.append(f'<path d="M -42 8 C -46 -36 46 -36 42 8 L 42 -2 Q 0 -20 -42 -2 Z" fill="{hairc}"/>')
        k.append(f'<circle cx="-30" cy="-24" r="10" fill="{hairc}"/><circle cx="-10" cy="-30" r="11" fill="{hairc}"/>'
                 f'<circle cx="12" cy="-30" r="11" fill="{hairc}"/><circle cx="30" cy="-24" r="10" fill="{hairc}"/>')
    elif variant % 4 == 2:  # bob girl
        k.append(f'<path d="M -42 26 C -48 -34 48 -34 42 26 L 30 26 Q 34 -6 0 -8 Q -34 -6 -30 26 Z" fill="{hairc}"/>')
        k.append(f'<circle cx="32" cy="0" r="5" fill="#F0608A"/>')
    else:  # spiky boy (Ethan)
        k.append(f'<path d="M -42 8 C -46 -34 46 -34 42 8 L 42 -2 Q 0 -18 -42 -2 Z" fill="{hairc}"/>')
        k.append(f'<polygon points="-34,-22 -26,-42 -20,-24" fill="{hairc}"/>'
                 f'<polygon points="-14,-26 -4,-46 4,-27" fill="{hairc}"/>'
                 f'<polygon points="12,-26 22,-44 28,-23" fill="{hairc}"/>')
    if expr == "think":
        k.append(f'<circle cx="-14" cy="16" r="4.5" fill="{LINE}"/><circle cx="14" cy="16" r="4.5" fill="{LINE}"/>')
        k.append(f'<path d="M -8 32 Q 0 35 8 32" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
    else:  # smile
        k.append(f'<path d="M -18 14 Q -14 8 -10 14" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
        k.append(f'<path d="M 10 14 Q 14 8 18 14" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
        k.append(f'<path d="M -10 28 Q 0 38 10 28" fill="none" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>')
    k.append(f'<ellipse cx="-26" cy="28" rx="7" ry="4.5" fill="{BLUSH}" fill-opacity="0.7"/>')
    k.append(f'<ellipse cx="26" cy="28" rx="7" ry="4.5" fill="{BLUSH}" fill-opacity="0.7"/>')
    inner = "".join(k)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def april(cx=0, cy=0, scale=1.0, pose="wave"):
    """媽媽 April：珊瑚色洋裝＋棕色馬尾。pose: wave（單手揮）| cheer（雙手高舉）| stand
    落地：鞋底約 cy + 212*scale（同 teacher）。"""
    DRESS = "#F2917E"
    DRESS_DK = "#D9705C"
    AHAIR = "#6B4A35"
    a = []
    # dress
    a.append(f'<path d="M -34 70 Q 0 58 34 70 L 44 178 L -44 178 Z" fill="{DRESS}"/>')
    a.append(f'<path d="M -44 178 L 44 178" stroke="{DRESS_DK}" stroke-width="4"/>')
    # arms
    if pose == "cheer":
        a.append(f'<path d="M -32 82 Q -70 40 -76 -6" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
        a.append(f'<circle cx="-77" cy="-12" r="10" fill="{SKIN}"/>')
        a.append(f'<path d="M 32 82 Q 70 40 76 -6" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
        a.append(f'<circle cx="77" cy="-12" r="10" fill="{SKIN}"/>')
    elif pose == "wave":
        a.append(f'<path d="M 32 82 Q 68 48 78 4" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
        a.append(f'<circle cx="80" cy="-2" r="10" fill="{SKIN}"/>')
        a.append(f'<path d="M -32 84 Q -50 116 -42 140" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
        a.append(f'<circle cx="-42" cy="144" r="9" fill="{SKIN}"/>')
    else:  # stand
        a.append(f'<path d="M -32 84 Q -50 116 -42 140" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
        a.append(f'<circle cx="-42" cy="144" r="9" fill="{SKIN}"/>')
        a.append(f'<path d="M 32 84 Q 50 116 42 140" stroke="{SKIN}" stroke-width="14" stroke-linecap="round" fill="none"/>')
        a.append(f'<circle cx="42" cy="144" r="9" fill="{SKIN}"/>')
    # legs + shoes
    a.append(f'<path d="M -14 178 L -14 206" stroke="{SKIN}" stroke-width="12" stroke-linecap="round"/>')
    a.append(f'<path d="M 14 178 L 14 206" stroke="{SKIN}" stroke-width="12" stroke-linecap="round"/>')
    a.append(f'<ellipse cx="-15" cy="212" rx="13" ry="7" fill="#B0574A"/><ellipse cx="15" cy="212" rx="13" ry="7" fill="#B0574A"/>')
    # head：圓臉＋瀏海（沿用 teacher 驗證過的髮頂路徑）＋高馬尾
    a.append(f'<circle cx="0" cy="20" r="40" fill="{SKIN}"/>')
    a.append(f'<path d="M -40 14 C -42 -30 42 -30 40 14 L 40 4 Q 20 -14 0 -8 Q -20 -14 -40 4 Z" fill="{AHAIR}"/>')
    a.append(f'<circle cx="24" cy="-26" r="13" fill="{AHAIR}"/>')
    a.append(f'<path d="M 32 -20 Q 54 2 46 32 Q 40 8 26 -12 Z" fill="{AHAIR}"/>')  # 馬尾垂落
    a.append(f'<circle cx="-14" cy="18" r="4" fill="{LINE}"/><circle cx="14" cy="18" r="4" fill="{LINE}"/>')
    a.append(f'<path d="M -10 34 Q 0 42 10 34" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
    a.append(f'<ellipse cx="-26" cy="30" rx="7" ry="4" fill="{BLUSH}" fill-opacity="0.7"/>')
    a.append(f'<ellipse cx="26" cy="30" rx="7" ry="4" fill="{BLUSH}" fill-opacity="0.7"/>')
    inner = "".join(a)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def ethan(cx=0, cy=0, scale=1.0, expr="smile"):
    """同學 Ethan（2026-07 照片參考重繪）：深棕蓬鬆微亂髮＋長瀏海、
    綠袖深藍身棒球 T（raglan 雙色）、露齒大笑。半身無腿，底部 y≈cy+150*scale。"""
    EHAIR = "#4A362A"
    NAVY = "#2E3A5C"
    GREEN = "#7BC08A"
    k = []
    # 棒球 T：深藍身
    k.append(f'<path d="M -34 78 Q 0 66 34 78 L 38 150 L -38 150 Z" fill="{NAVY}" stroke="#232D48" stroke-width="2.5"/>')
    # 綠色肩袖（raglan 斜線兩側）
    k.append(f'<path d="M -34 78 Q -20 70 -8 72 L -18 96 Q -30 96 -36 90 Z" fill="{GREEN}"/>')
    k.append(f'<path d="M 34 78 Q 20 70 8 72 L 18 96 Q 30 96 36 90 Z" fill="{GREEN}"/>')
    # 手臂
    k.append(f'<path d="M -34 86 Q -52 108 -44 128" stroke="{SKIN}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    k.append(f'<path d="M 34 86 Q 52 108 44 128" stroke="{SKIN}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    # 頭
    k.append(f'<circle cx="0" cy="16" r="42" fill="{SKIN}"/>')
    # 深棕蓬鬆髮：厚圓頂＋長而微亂的瀏海（幾撮不齊的髮尖）
    k.append(f'<path d="M -42 12 C -48 -44 48 -44 42 12 L 42 2 '
             f'Q 34 -6 28 2 Q 22 -10 14 0 Q 6 -12 -2 -2 Q -10 -12 -18 -2 Q -26 -8 -34 2 Q -38 -4 -42 4 Z" fill="{EHAIR}"/>')
    # 蓬鬆感：頂上兩撮翹起
    k.append(f'<path d="M -14 -28 Q -8 -38 0 -30 Q -6 -26 -14 -28 Z" fill="{EHAIR}"/>')
    k.append(f'<path d="M 10 -29 Q 18 -37 24 -28 Q 16 -25 10 -29 Z" fill="{EHAIR}"/>')
    # 表情（照片的露齒大笑）
    if expr == "think":
        k.append(f'<circle cx="-14" cy="16" r="4.5" fill="{LINE}"/><circle cx="14" cy="16" r="4.5" fill="{LINE}"/>')
        k.append(f'<path d="M -8 32 Q 0 35 8 32" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
    elif expr == "oh":
        k.append(f'<circle cx="-14" cy="16" r="4.5" fill="{LINE}"/><circle cx="14" cy="16" r="4.5" fill="{LINE}"/>')
        k.append(f'<ellipse cx="0" cy="34" rx="6" ry="7" fill="#8C4A3C"/>')
    else:  # smile：開口大笑＋牙齒
        k.append(f'<path d="M -19 12 Q -14 6 -9 12" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
        k.append(f'<path d="M 9 12 Q 14 6 19 12" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
        k.append(f'<path d="M -14 28 A 14 11 0 0 0 14 28 Z" fill="#8C4A3C"/>')
        k.append(f'<rect x="-10" y="28" width="20" height="4" rx="2" fill="#FFFFFF"/>')
    k.append(f'<ellipse cx="-27" cy="26" rx="7" ry="4.5" fill="{BLUSH}" fill-opacity="0.7"/>')
    k.append(f'<ellipse cx="27" cy="26" rx="7" ry="4.5" fill="{BLUSH}" fill-opacity="0.7"/>')
    inner = "".join(k)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def anne(cx=0, cy=0, scale=1.0, expr="smile"):
    """朋友 Anne（2026-07 照片參考重繪）：雙丸子頭＋齊瀏海＋圓黑框眼鏡（深灰鏡腳，
    與 Owen 的橘鏡腳區分）＋粉紅紗裙（藍綠滾邊）。半身無腿，底部 y≈cy+152*scale。"""
    DRESS = "#F8BCC8"
    TRIM = "#4EC9B8"
    AHAIR = "#2A2320"
    k = []
    # 蓬蓬紗裙（上窄下寬＋裙襬滾邊）
    k.append(f'<path d="M -30 76 Q 0 64 30 76 L 44 146 Q 0 160 -44 146 Z" fill="{DRESS}"/>')
    k.append(f'<path d="M -44 146 Q 0 160 44 146" fill="none" stroke="{TRIM}" stroke-width="5" stroke-linecap="round"/>')
    k.append(f'<path d="M -30 76 Q 0 88 30 76" fill="none" stroke="{TRIM}" stroke-width="4"/>')  # 領口滾邊
    # 手臂
    k.append(f'<path d="M -30 84 Q -50 106 -44 126" stroke="{SKIN}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    k.append(f'<path d="M 30 84 Q 50 106 44 126" stroke="{SKIN}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    # 頭
    k.append(f'<circle cx="0" cy="16" r="42" fill="{SKIN}"/>')
    # 齊瀏海髮（深髮頂＋壓低的小鋸齒瀏海，蓋住上額）
    k.append(f'<path d="M -42 16 C -46 -42 46 -42 42 16 L 42 6 '
             f'Q 32 -8 22 -2 Q 12 -10 2 -4 Q -8 -12 -18 -4 Q -28 -10 -42 6 Z" fill="{AHAIR}"/>')
    # 雙丸子頭（貼在髮頂兩側，不外飄）＋粉色髮飾
    k.append(f'<circle cx="-25" cy="-27" r="11" fill="{AHAIR}"/><circle cx="25" cy="-27" r="11" fill="{AHAIR}"/>')
    k.append(f'<circle cx="-25" cy="-21" r="3.5" fill="#F088A8"/><circle cx="25" cy="-21" r="3.5" fill="#F088A8"/>')
    # 圓黑框眼鏡（深灰鏡腳）
    k.append(f'<line x1="-38" y1="12" x2="-42" y2="15" stroke="#4A4A4A" stroke-width="4" stroke-linecap="round"/>')
    k.append(f'<line x1="38" y1="12" x2="42" y2="15" stroke="#4A4A4A" stroke-width="4" stroke-linecap="round"/>')
    k.append(f'<circle cx="-17" cy="14" r="15" fill="#FFFFFF" fill-opacity="0.25" stroke="#161616" stroke-width="5"/>')
    k.append(f'<circle cx="17" cy="14" r="15" fill="#FFFFFF" fill-opacity="0.25" stroke="#161616" stroke-width="5"/>')
    k.append(f'<path d="M -4 12 Q 0 9 4 12" fill="none" stroke="#161616" stroke-width="4" stroke-linecap="round"/>')
    # 表情
    if expr == "think":
        k.append(f'<circle cx="-17" cy="14" r="4" fill="{LINE}"/><circle cx="17" cy="14" r="4" fill="{LINE}"/>')
        k.append(f'<path d="M -8 34 Q 0 37 8 34" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
    elif expr == "oh":
        k.append(f'<circle cx="-17" cy="14" r="4" fill="{LINE}"/><circle cx="17" cy="14" r="4" fill="{LINE}"/>')
        k.append(f'<ellipse cx="0" cy="34" rx="6" ry="7" fill="#8C4A3C"/>')
    else:  # smile
        k.append(f'<circle cx="-17" cy="14" r="4" fill="{LINE}"/><circle cx="17" cy="14" r="4" fill="{LINE}"/>')
        k.append(f'<path d="M -9 32 Q 0 40 9 32" fill="none" stroke="{LINE}" stroke-width="5" stroke-linecap="round"/>')
    k.append(f'<ellipse cx="-28" cy="26" rx="7" ry="4.5" fill="{BLUSH}" fill-opacity="0.7"/>')
    k.append(f'<ellipse cx="28" cy="26" rx="7" ry="4.5" fill="{BLUSH}" fill-opacity="0.7"/>')
    inner = "".join(k)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def daddy(cx=0, cy=0, scale=1.0, pose="stand", whistle=False):
    """爸爸 Daddy：戴同款圓框眼鏡（親子呼應）＋短黑髮＋藍綠 polo。
    pose: stand | point（右指）| cheer（雙手高舉）。鞋底 ≈ cy + 216*scale。"""
    POLO = "#3E8E8C"
    POLO_DK = "#2E6D6B"
    d = []
    # polo 上衣
    d.append(f'<path d="M -38 66 Q 0 54 38 66 L 44 150 L -44 150 Z" fill="{POLO}"/>')
    d.append(f'<path d="M -10 66 L 0 84 L 10 66" fill="none" stroke="{POLO_DK}" stroke-width="4"/>')
    # arms
    if pose == "point":
        d.append(f'<path d="M 34 80 Q 78 64 100 44" stroke="{SKIN}" stroke-width="15" stroke-linecap="round" fill="none"/>')
        d.append(f'<circle cx="104" cy="40" r="10" fill="{SKIN}"/>')
        d.append(f'<path d="M -34 82 Q -54 114 -46 138" stroke="{SKIN}" stroke-width="15" stroke-linecap="round" fill="none"/>')
        d.append(f'<circle cx="-46" cy="142" r="9" fill="{SKIN}"/>')
    elif pose == "cheer":
        d.append(f'<path d="M -34 80 Q -74 36 -80 -10" stroke="{SKIN}" stroke-width="15" stroke-linecap="round" fill="none"/>')
        d.append(f'<circle cx="-81" cy="-16" r="10" fill="{SKIN}"/>')
        d.append(f'<path d="M 34 80 Q 74 36 80 -10" stroke="{SKIN}" stroke-width="15" stroke-linecap="round" fill="none"/>')
        d.append(f'<circle cx="81" cy="-16" r="10" fill="{SKIN}"/>')
    else:
        d.append(f'<path d="M -34 82 Q -54 114 -46 138" stroke="{SKIN}" stroke-width="15" stroke-linecap="round" fill="none"/>')
        d.append(f'<circle cx="-46" cy="142" r="9" fill="{SKIN}"/>')
        d.append(f'<path d="M 34 82 Q 54 114 46 138" stroke="{SKIN}" stroke-width="15" stroke-linecap="round" fill="none"/>')
        d.append(f'<circle cx="46" cy="142" r="9" fill="{SKIN}"/>')
    # 卡其短褲＋腿
    d.append(f'<path d="M -32 150 L 32 150 L 34 184 L 6 184 L 0 168 L -6 184 L -34 184 Z" fill="#C9B48A"/>')
    d.append(f'<path d="M -14 184 L -14 210" stroke="{SKIN}" stroke-width="13" stroke-linecap="round"/>')
    d.append(f'<path d="M 14 184 L 14 210" stroke="{SKIN}" stroke-width="13" stroke-linecap="round"/>')
    d.append(f'<ellipse cx="-15" cy="216" rx="14" ry="8" fill="#7A6A50"/><ellipse cx="15" cy="216" rx="14" ry="8" fill="#7A6A50"/>')
    # 哨子（掛繩）
    if whistle:
        d.append(f'<path d="M -12 66 Q 0 96 12 66" fill="none" stroke="#8A7460" stroke-width="3"/>')
        d.append(f'<rect x="-8" y="94" width="18" height="12" rx="5" fill="#F2B035" stroke="#C98A18" stroke-width="2.5"/>')
    # head：方一點的臉＋短黑髮＋圓框眼鏡
    d.append(f'<circle cx="0" cy="16" r="38" fill="{SKIN}"/>')
    d.append(f'<path d="M -38 10 C -40 -30 40 -30 38 10 L 38 0 Q 18 -14 0 -10 Q -18 -14 -38 0 Z" fill="{HAIR}"/>')
    d.append(f'<circle cx="-16" cy="14" r="13" fill="#FFFFFF" fill-opacity="0.25" stroke="#161616" stroke-width="5"/>')
    d.append(f'<circle cx="16" cy="14" r="13" fill="#FFFFFF" fill-opacity="0.25" stroke="#161616" stroke-width="5"/>')
    d.append(f'<path d="M -4 12 Q 0 9 4 12" fill="none" stroke="#161616" stroke-width="4" stroke-linecap="round"/>')
    d.append(f'<circle cx="-16" cy="14" r="3.5" fill="{LINE}"/><circle cx="16" cy="14" r="3.5" fill="{LINE}"/>')
    d.append(f'<path d="M -9 36 Q 0 43 9 36" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
    inner = "".join(d)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def april_asleep(cx=0, cy=0, scale=1.0):
    """睡著的媽媽 April：枕頭＋側躺頭（閉眼）＋被子隆起。頭中心在原點，被子往右延伸約 220。"""
    DRESS_DK = "#D9705C"
    AHAIR = "#6B4A35"
    a = []
    a.append(f'<ellipse cx="-6" cy="18" rx="64" ry="26" fill="#FFFFFF" stroke="#E5D9C9" stroke-width="3"/>')  # 枕頭
    a.append(f'<circle cx="0" cy="0" r="36" fill="{SKIN}"/>')  # 頭
    a.append(f'<path d="M -36 -6 C -38 -44 38 -44 36 -6 L 36 -14 Q 18 -28 0 -24 Q -18 -28 -36 -14 Z" fill="{AHAIR}"/>')
    a.append(f'<circle cx="30" cy="-30" r="12" fill="{AHAIR}"/>')  # 髮髻
    a.append(f'<path d="M -20 2 Q -14 8 -8 2" fill="none" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>')  # 閉眼
    a.append(f'<path d="M 8 2 Q 14 8 20 2" fill="none" stroke="{LINE}" stroke-width="4" stroke-linecap="round"/>')
    a.append(f'<path d="M -4 22 Q 2 26 8 22" fill="none" stroke="{LINE}" stroke-width="3.5" stroke-linecap="round"/>')  # 安詳微笑
    a.append(f'<ellipse cx="-22" cy="16" rx="6" ry="4" fill="{BLUSH}" fill-opacity="0.6"/>')
    a.append(f'<path d="M 30 6 Q 40 -2 52 6 L 230 6 Q 250 6 250 30 L 250 44 Q 250 58 230 58 L 44 58 Q 28 58 30 40 Z" fill="#F2A9A0"/>')  # 被子
    a.append(f'<path d="M 56 6 L 56 58 M 96 6 L 96 58" stroke="{DRESS_DK}" stroke-width="3" stroke-opacity="0.4"/>')
    inner = "".join(a)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


# ---------------- HOME / SOCCER PROPS ----------------
def clock_digital(cx=0, cy=0, scale=1.0, time="6:30", glow=False):
    """數字時鐘：圓角矩形＋螢幕顯示時間。glow=True 時亮金色光暈（6:30 時刻用）。"""
    c = []
    if glow:
        c.append(f'<circle cx="0" cy="0" r="110" fill="{STAR_Y}" fill-opacity="0.16"/>')
        c.append(f'<circle cx="0" cy="0" r="80" fill="{STAR_Y}" fill-opacity="0.16"/>')
    c.append(f'<rect x="-70" y="-46" width="140" height="86" rx="16" fill="#5C6BC0" stroke="#3F4E9E" stroke-width="4"/>')
    c.append(f'<rect x="-56" y="-32" width="112" height="58" rx="8" fill="#1F2440"/>')
    c.append(f'<text x="0" y="12" font-family="Huninn" font-size="38" font-weight="bold" fill="{"#FFD34D" if glow else "#9FE8B8"}" text-anchor="middle">{time}</text>')
    c.append(f'<rect x="-26" y="-56" width="52" height="12" rx="6" fill="#3F4E9E"/>')  # 上方按鈕
    c.append(f'<ellipse cx="-46" cy="46" rx="12" ry="6" fill="#3F4E9E"/><ellipse cx="46" cy="46" rx="12" ry="6" fill="#3F4E9E"/>')
    inner = "".join(c)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def soccer_ball(cx=0, cy=0, r=24):
    penta = " ".join(f"{r*0.42*math.cos(math.radians(-90+i*72)):.1f},{r*0.42*math.sin(math.radians(-90+i*72)):.1f}" for i in range(5))
    p = [f'<circle cx="0" cy="0" r="{r}" fill="#FFFFFF" stroke="#4A4A4A" stroke-width="3"/>',
         f'<polygon points="{penta}" fill="#4A4A4A"/>']
    for i in range(5):
        a = math.radians(-90 + i * 72)
        x1, y1 = r*0.40*math.cos(a), r*0.40*math.sin(a)
        x2, y2 = r*0.92*math.cos(a), r*0.92*math.sin(a)
        p.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#4A4A4A" stroke-width="3"/>')
    return f'<g transform="translate({cx},{cy})">{"".join(p)}</g>'


def goal(cx=0, cy=0, scale=1.0):
    """足球門：底部中心在原點，寬 280 高 150，含網格。"""
    g = [f'<path d="M -140 0 L -140 -150 L 140 -150 L 140 0" fill="none" stroke="#FFFFFF" stroke-width="10"/>',
         f'<path d="M -140 0 L -140 -150 L 140 -150 L 140 0" fill="none" stroke="#D9D2C4" stroke-width="3"/>']
    for x in range(-120, 140, 28):
        g.append(f'<line x1="{x}" y1="-144" x2="{x}" y2="-4" stroke="#D9D2C4" stroke-width="2"/>')
    for y in range(-140, 0, 26):
        g.append(f'<line x1="-134" y1="{y}" x2="134" y2="{y}" stroke="#D9D2C4" stroke-width="2"/>')
    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(g)}</g>'


def lucas(cx=0, cy=0, scale=1.0, expr="smile"):
    """朋友 Lucas（2026-07 照片參考重繪）：黑色短直髮＋淺灰 T 恤＋大笑容。
    半身無腿，底部 y≈cy+150*scale。"""
    LHAIR = "#26201C"
    SHIRT = "#C9CDD4"
    k = []
    # 淺灰 T 恤
    k.append(f'<path d="M -34 78 Q 0 66 34 78 L 38 150 L -38 150 Z" fill="{SHIRT}" stroke="#AEB4BC" stroke-width="2.5"/>')
    # 手臂
    k.append(f'<path d="M -34 86 Q -52 108 -44 128" stroke="{SKIN}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    k.append(f'<path d="M 34 86 Q 52 108 44 128" stroke="{SKIN}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    # 頭
    k.append(f'<circle cx="0" cy="16" r="42" fill="{SKIN}"/>')
    # 黑色短直髮：深圓頂＋自然短瀏海（蓋住上額，微露額頭）
    k.append(f'<path d="M -42 10 C -46 -42 46 -42 42 10 L 42 0 '
             f'Q 26 -8 10 -5 Q -6 -10 -22 -5 Q -34 -9 -42 0 Z" fill="{LHAIR}"/>')
    k.append(f'<path d="M -42 4 Q -46 12 -42 18 L -38 6 Z" fill="{LHAIR}"/>')
    k.append(f'<path d="M 42 4 Q 46 12 42 18 L 38 6 Z" fill="{LHAIR}"/>')
    # 表情（照片的大笑容）
    if expr == "think":
        k.append(f'<circle cx="-14" cy="14" r="4.5" fill="{LINE}"/><circle cx="14" cy="14" r="4.5" fill="{LINE}"/>')
        k.append(f'<path d="M -8 32 Q 0 35 8 32" fill="none" stroke="{LINE}" stroke-width="4.5" stroke-linecap="round"/>')
    elif expr == "oh":
        k.append(f'<circle cx="-14" cy="14" r="4.5" fill="{LINE}"/><circle cx="14" cy="14" r="4.5" fill="{LINE}"/>')
        k.append(f'<ellipse cx="0" cy="34" rx="6" ry="7" fill="#8C4A3C"/>')
    else:  # smile：開口大笑＋牙齒
        k.append(f'<circle cx="-14" cy="12" r="4.5" fill="{LINE}"/><circle cx="14" cy="12" r="4.5" fill="{LINE}"/>')
        k.append(f'<path d="M -14 28 A 14 11 0 0 0 14 28 Z" fill="#8C4A3C"/>')
        k.append(f'<rect x="-10" y="28" width="20" height="4" rx="2" fill="#FFFFFF"/>')
    k.append(f'<ellipse cx="-26" cy="26" rx="7" ry="4.5" fill="{BLUSH}" fill-opacity="0.7"/>')
    k.append(f'<ellipse cx="26" cy="26" rx="7" ry="4.5" fill="{BLUSH}" fill-opacity="0.7"/>')
    inner = "".join(k)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'


def ann(cx=0, cy=0, scale=1.0, expr="smile"):
    """朋友 Anne 的舊別名（相容既有場景呼叫）——實體見 anne()。"""
    return anne(cx=cx, cy=cy, scale=scale, expr=expr)


# ---------------- SPORTS PROPS ----------------
def basketball(cx=0, cy=0, r=26):
    p = [f'<circle cx="0" cy="0" r="{r}" fill="#E8823C" stroke="#B85E22" stroke-width="3"/>',
         f'<line x1="0" y1="{-r}" x2="0" y2="{r}" stroke="#B85E22" stroke-width="3"/>',
         f'<line x1="{-r}" y1="0" x2="{r}" y2="0" stroke="#B85E22" stroke-width="3"/>',
         f'<path d="M {-r*0.72:.0f} {-r*0.72:.0f} Q {r*0.30:.0f} 0 {-r*0.72:.0f} {r*0.72:.0f}" fill="none" stroke="#B85E22" stroke-width="3"/>',
         f'<path d="M {r*0.72:.0f} {-r*0.72:.0f} Q {-r*0.30:.0f} 0 {r*0.72:.0f} {r*0.72:.0f}" fill="none" stroke="#B85E22" stroke-width="3"/>']
    return f'<g transform="translate({cx},{cy})">{"".join(p)}</g>'


def hoop(cx=0, cy=0, scale=1.0):
    """籃框：籃板＋籃圈＋網。籃圈中心在 (0,0)，籃板在上方，柱子由場景自行決定要不要畫。"""
    p = [f'<rect x="-52" y="-96" width="104" height="72" rx="8" fill="#FFF7E6" stroke="#C9A26B" stroke-width="5"/>',
         f'<rect x="-24" y="-58" width="48" height="34" rx="4" fill="none" stroke="#E4574C" stroke-width="4"/>',
         f'<ellipse cx="0" cy="0" rx="34" ry="9" fill="none" stroke="#E4574C" stroke-width="6"/>',
         f'<path d="M -30 4 L -16 44 M -12 6 L -4 46 M 12 6 L 4 46 M 30 4 L 16 44 M -16 44 Q 0 52 16 44" fill="none" stroke="#DDD3C2" stroke-width="3"/>']
    return f'<g transform="translate({cx},{cy}) scale({scale})">{"".join(p)}</g>'


def baseball(cx=0, cy=0, r=14):
    p = [f'<circle cx="0" cy="0" r="{r}" fill="#FFFFFF" stroke="#C9BFA8" stroke-width="2.5"/>',
         f'<path d="M {-r*0.5:.0f} {-r*0.87:.0f} Q {-r*1.05:.0f} 0 {-r*0.5:.0f} {r*0.87:.0f}" fill="none" stroke="#E4574C" stroke-width="2.5"/>',
         f'<path d="M {r*0.5:.0f} {-r*0.87:.0f} Q {r*1.05:.0f} 0 {r*0.5:.0f} {r*0.87:.0f}" fill="none" stroke="#E4574C" stroke-width="2.5"/>']
    return f'<g transform="translate({cx},{cy})">{"".join(p)}</g>'


def bat(cx=0, cy=0, angle=-40, scale=1.0):
    """球棒：握把端在 (0,0)，往右上延伸；angle 為旋轉角（度，負值朝上）。"""
    p = [f'<path d="M 0 0 L 96 0" stroke="#C89355" stroke-width="14" stroke-linecap="round"/>',
         f'<path d="M 96 0 L 132 0" stroke="#B87F42" stroke-width="20" stroke-linecap="round"/>',
         f'<circle cx="-2" cy="0" r="9" fill="#8A5A3C"/>']
    return f'<g transform="translate({cx},{cy}) rotate({angle}) scale({scale})">{"".join(p)}</g>'


def desk(cx=0, cy=0, w=240, scale=1.0):
    return (f'<g transform="translate({cx},{cy}) scale({scale})">'
            f'<rect x="{-w/2}" y="0" width="{w}" height="26" rx="10" fill="#D9B98C" stroke="#C4A272" stroke-width="3"/>'
            f'<rect x="{-w/2+18}" y="26" width="14" height="70" rx="6" fill="#C4A272"/>'
            f'<rect x="{w/2-32}" y="26" width="14" height="70" rx="6" fill="#C4A272"/></g>')


def brain_pocket(cx=0, cy=0, scale=1.0, open_flap=True, glow=True):
    """The 'brain pocket': a cute pouch with a zipper."""
    p = []
    if glow:
        p.append(f'<circle cx="0" cy="0" r="86" fill="{STAR_Y}" fill-opacity="0.18"/>')
        p.append(f'<circle cx="0" cy="0" r="64" fill="{STAR_Y}" fill-opacity="0.18"/>')
    p.append(f'<path d="M -52 -10 Q -52 -46 0 -46 Q 52 -46 52 -10 L 52 22 Q 52 44 0 44 Q -52 44 -52 22 Z" fill="#8E6FD8" stroke="#6E52B4" stroke-width="4"/>')
    # zipper
    p.append(f'<line x1="-44" y1="-12" x2="44" y2="-12" stroke="#FFFFFF" stroke-width="6" stroke-dasharray="7 5"/>')
    if open_flap:
        p.append(f'<path d="M -52 -10 Q 0 -70 52 -10" fill="#A98FE8" stroke="#6E52B4" stroke-width="4"/>')
        p.append(f'<circle cx="52" cy="-12" r="6" fill="#FFD34D" stroke="#6E52B4" stroke-width="3"/>')
    else:
        p.append(f'<circle cx="44" cy="-12" r="6" fill="#FFD34D" stroke="#6E52B4" stroke-width="3"/>')
    p.append(f'<polygon points="{star_pts(-26, 20, 9)}" fill="#C9B6F2"/>')
    inner = "".join(p)
    return f'<g transform="translate({cx},{cy}) scale({scale})">{inner}</g>'
