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

def boy(pose="stand", expr="smile", scale=1.0, cx=0, cy=0, backpack=False, cape=False):
    """pose: stand | walk | handup | hips | wave | sit(bust w/ desk handled by scene)"""
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
    else:
        b.append(f'<path d="M -14 210 L -14 252" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<path d="M 14 210 L 14 252" stroke="{SKIN}" stroke-width="18" stroke-linecap="round" fill="none"/>')
        b.append(f'<ellipse cx="-16" cy="258" rx="17" ry="10" fill="#C9BFA8"/>')
        b.append(f'<ellipse cx="16" cy="258" rx="17" ry="10" fill="#C9BFA8"/>')

    # shorts (camo)
    b.append(f'<path d="M -34 178 L 34 178 L 38 222 L 8 222 L 0 200 L -8 222 L -38 222 Z" fill="{SHORTS}"/>')
    b.append(f'<circle cx="-18" cy="196" r="6" fill="{SHORTS_DK}"/><circle cx="16" cy="208" r="7" fill="{SHORTS_DK}"/><circle cx="4" cy="188" r="5" fill="{SHORTS_DK}"/>')

    # torso tee
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
    inner = "".join(b)
    # head placed: head center at y≈34; body shoulders at 96
    return f'<g transform="translate({cx},{cy}) scale({scale})"><g transform="translate(0,-30)">{inner}</g></g>'


def boy_bust(expr="smile", scale=1.0, cx=0, cy=0, arms="desk"):
    """Bust for desk scenes: head + shoulders + arms on desk."""
    b = []
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
    """Simple friend characters (no glasses, different hair/colors)."""
    shirt = ["#F6C445", "#7BC47F", "#F49AB5"][variant % 3]
    hairc = ["#5A4632", "#20201F", "#7A4A2C"][variant % 3]
    skin = ["#FFD9B6", "#E8B98C", "#FFD9B6"][variant % 3]
    k = []
    k.append(f'<path d="M -34 78 Q 0 66 34 78 L 38 150 L -38 150 Z" fill="{shirt}"/>')
    k.append(f'<path d="M -34 86 Q -52 108 -44 128" stroke="{skin}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    k.append(f'<path d="M 34 86 Q 52 108 44 128" stroke="{skin}" stroke-width="13" stroke-linecap="round" fill="none"/>')
    k.append(f'<circle cx="0" cy="16" r="42" fill="{skin}"/>')
    if variant % 3 == 0:  # girl twin tails
        k.append(f'<path d="M -42 10 C -44 -34 44 -34 42 10 L 42 0 Q 0 -18 -42 0 Z" fill="{hairc}"/>')
        k.append(f'<circle cx="-46" cy="18" r="12" fill="{hairc}"/><circle cx="46" cy="18" r="12" fill="{hairc}"/>')
    elif variant % 3 == 1:  # curly boy
        k.append(f'<path d="M -42 8 C -46 -36 46 -36 42 8 L 42 -2 Q 0 -20 -42 -2 Z" fill="{hairc}"/>')
        k.append(f'<circle cx="-30" cy="-24" r="10" fill="{hairc}"/><circle cx="-10" cy="-30" r="11" fill="{hairc}"/>'
                 f'<circle cx="12" cy="-30" r="11" fill="{hairc}"/><circle cx="30" cy="-24" r="10" fill="{hairc}"/>')
    else:  # bob girl
        k.append(f'<path d="M -42 26 C -48 -34 48 -34 42 26 L 30 26 Q 34 -6 0 -8 Q -34 -6 -30 26 Z" fill="{hairc}"/>')
        k.append(f'<circle cx="32" cy="0" r="5" fill="#F0608A"/>')
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
