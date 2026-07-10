# -*- coding: utf-8 -*-
"""Build 'I Can Save My Answer!' — a social-story picture book (A4 landscape PDF)."""
from parts import *
import os

FONT_PATH = os.path.abspath(os.environ.get("HUNINN_TTF", "../assets/fonts/jf-openhuninn-2.0.ttf"))

FONT = "file://" + FONT_PATH
TXT = "#4A3B32"

# soft page palettes
BG = {
    "cover": "#FFE9A8", "p1": "#CFEAF8", "p2": "#FFF3D6", "p3": "#FFE3C2",
    "p4": "#FFD9CF", "p5": "#E6DCF8", "p6": "#D7E9F8", "p7": "#DFF0DC",
    "p8": "#FFF0C9", "p9": "#FFE2EC", "p10": "#FFE9A8", "p11": "#FBF4E8",
}

def svg(w, h, inner, bg=None):
    r = f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">'
    if bg:
        r += f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}"/>'
    return r + inner + "</svg>"

def svgtext(x, y, s, size=48, fill=TXT, weight="normal", anchor="middle", family="Huninn"):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{s}</text>')

W, H = 1188, 560   # story art viewBox (297mm x 140mm ratio)

# ---------------- SCENES ----------------
def scene_cover():
    e = []
    e.append(sun(120, 110, 40))
    e.append(cloud(950, 100, 1.2)); e.append(cloud(760, 60, 0.8)); e.append(cloud(260, 70, 0.7))
    for (x, y, r) in [(180, 330, 22), (1010, 300, 26), (330, 150, 14), (880, 170, 16), (1080, 460, 18), (110, 480, 16)]:
        e.append(star(x, y, r))
    e.append(sparkle(420, 120, 14)); e.append(sparkle(700, 400, 12)); e.append(sparkle(240, 430, 10))
    # ground
    e.append(f'<ellipse cx="594" cy="640" rx="560" ry="120" fill="#FFDD7E"/>')
    # boy waving, holding a smiling star
    e.append(boy(pose="wave", expr="big", cx=594, cy=214, scale=1.35))
    e.append(star(524, 408, 36, face=True))
    return svg(1188, 620, "".join(e), bg=None)

def scene_p1():
    e = []
    e.append(sun(1060, 90, 36))
    e.append(cloud(220, 80, 1.0)); e.append(cloud(560, 60, 0.7))
    # ground / path
    e.append(f'<rect x="0" y="430" width="1188" height="130" fill="#BFE3B4"/>')
    e.append(f'<path d="M 0 560 Q 594 400 1188 560 L 1188 560 L 0 560 Z" fill="#EED9A8"/>')
    # school in distance
    e.append(f'<rect x="880" y="270" width="230" height="160" rx="10" fill="#F6C9A0" stroke="#D8A377" stroke-width="4"/>')
    e.append(f'<rect x="960" y="350" width="60" height="80" rx="6" fill="#8A5A3C"/>')
    e.append(f'<rect x="906" y="300" width="44" height="36" rx="4" fill="#BEE3F2"/>')
    e.append(f'<rect x="1040" y="300" width="44" height="36" rx="4" fill="#BEE3F2"/>')
    e.append(f'<polygon points="870,270 995,205 1120,270" fill="#E4574C"/>')
    e.append(f'<circle cx="995" cy="240" r="10" fill="#FFD34D"/>')
    # bushes
    e.append(f'<circle cx="80" cy="430" r="40" fill="#8FCB84"/><circle cx="130" cy="440" r="30" fill="#79BD6E"/>')
    # boy walking with backpack + idea sparkles
    e.append(boy(pose="walk", expr="smile", cx=400, cy=196, scale=1.12, backpack=True))
    e.append(sparkle(560, 90, 12)); e.append(sparkle(680, 130, 14)); e.append(star(620, 60, 16))
    e.append(f'<circle cx="560" cy="160" r="18" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="3"/>')
    e.append(f'<rect x="551" y="176" width="18" height="10" rx="3" fill="#C9BFA8"/>')  # lightbulb
    return svg(W, H, "".join(e))

def scene_p2():
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#E8D2AC"/>')  # floor
    # blackboard
    e.append(f'<rect x="360" y="60" width="560" height="300" rx="14" fill="#C9A26B"/>')
    e.append(f'<rect x="376" y="76" width="528" height="268" rx="8" fill="#3E7C5B"/>')
    e.append(svgtext(640, 260, "?", size=150, fill="#FFF7E0", weight="bold"))
    e.append(f'<circle cx="820" cy="140" r="6" fill="#FFF7E0" fill-opacity="0.7"/>')
    e.append(f'<circle cx="440" cy="300" r="5" fill="#FFF7E0" fill-opacity="0.5"/>')
    # chalk tray
    e.append(f'<rect x="500" y="360" width="280" height="12" rx="6" fill="#B08A56"/>')
    # teacher pointing at board
    e.append(teacher(cx=210, cy=250, scale=1.0, point="right"))
    # boy small at desk right
    e.append(desk(cx=1020, cy=430, w=220))
    e.append(boy_bust(expr="oh", cx=1020, cy=330, scale=0.85))
    return svg(W, H, "".join(e))

def scene_p3():
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#E8D2AC"/>')
    # big glowing bulb above
    e.append(f'<circle cx="594" cy="120" r="88" fill="{STAR_Y}" fill-opacity="0.25"/>')
    e.append(f'<circle cx="594" cy="112" r="52" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="5"/>')
    e.append(f'<rect x="574" y="158" width="40" height="20" rx="6" fill="#C9BFA8"/>')
    for i in range(6):
        a = math.radians(-150 + i * 60)
        x1, y1 = 594 + 100*math.cos(a), 116 + 100*math.sin(a)
        x2, y2 = 594 + 130*math.cos(a), 116 + 130*math.sin(a)
        e.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{STAR_DK}" stroke-width="7" stroke-linecap="round"/>')
    e.append(star(340, 240, 20)); e.append(star(850, 230, 24)); e.append(sparkle(280, 130, 12)); e.append(sparkle(910, 130, 14))
    e.append(boy_bust(expr="star", cx=594, cy=352, scale=1.3))
    e.append(desk(cx=594, cy=474, w=360, scale=1.1))
    return svg(W, H, "".join(e))

def scene_p4():
    e = []
    # heat squiggles around
    for (x, y) in [(300, 120), (880, 120), (250, 300), (930, 300)]:
        e.append(f'<path d="M {x} {y} q 12 -18 24 0 q 12 18 24 0" fill="none" stroke="#F26B5E" stroke-width="8" stroke-linecap="round"/>')
    e.append(boy_bust(expr="hold", cx=594, cy=330, scale=1.5))
    # star trying to escape right at the mouth (little wings + push lines)
    e.append(star(594, 372, 24, face=True))
    e.append(f'<path d="M 562 360 q -16 -8 -12 -24" fill="none" stroke="{STAR_DK}" stroke-width="6" stroke-linecap="round"/>')
    e.append(f'<path d="M 626 360 q 16 -8 12 -24" fill="none" stroke="{STAR_DK}" stroke-width="6" stroke-linecap="round"/>')
    for dx, dy in ((-56, 26), (0, 34), (56, 26)):
        e.append(f'<line x1="{594+dx*0.6:.0f}" y1="{382+dy*0.4:.0f}" x2="{594+dx}" y2="{382+dy}" stroke="#F26B5E" stroke-width="6" stroke-linecap="round"/>')
    e.append(desk(cx=594, cy=486, w=380, scale=1.15))
    # beating heart at side
    e.append(f'<path d="M 950 340 c 0 -30 44 -30 44 -2 c 0 -28 44 -28 44 2 c 0 30 -44 46 -44 60 c 0 -14 -44 -30 -44 -60 Z" fill="#F2665A" stroke="#D14A3F" stroke-width="4"/>')
    e.append(f'<path d="M 928 388 q -16 0 -20 -14 M 1060 388 q 16 0 20 -14" fill="none" stroke="#D14A3F" stroke-width="6" stroke-linecap="round"/>')
    # sweat drop by the head
    e.append(f'<path d="M 716 176 q 18 30 0 44 q -18 -14 0 -44 Z" fill="#8FD3F2"/>')
    return svg(W, H, "".join(e))

def scene_p5():
    e = []
    for (x, y, r) in [(150, 120, 16), (1030, 130, 20), (200, 420, 14), (1000, 430, 16)]:
        e.append(star(x, y, r, fill="#CDeBFF" if False else STAR_Y))
    e.append(sparkle(320, 90, 12)); e.append(sparkle(860, 80, 12)); e.append(sparkle(90, 300, 10)); e.append(sparkle(1100, 300, 10))
    # boy pressing lips, pocket above, star flying from mouth into pocket
    e.append(f'<ellipse cx="450" cy="536" rx="90" ry="14" fill="#C9BBE8"/>')
    e.append(boy(pose="stand", expr="press", cx=450, cy=270, scale=1.15))
    e.append(brain_pocket(cx=790, cy=150, scale=1.2, open_flap=True))
    e.append(f'<path d="M 486 306 Q 620 150 738 142" fill="none" stroke="{STAR_DK}" stroke-width="6" stroke-dasharray="2 16" stroke-linecap="round"/>')
    e.append(star(624, 202, 26, face=True))
    return svg(W, H, "".join(e))

def scene_p6():
    e = []
    e.append(f'<rect x="0" y="480" width="1188" height="80" fill="#BFD9EE"/>')
    # counting bubbles 1 2 3
    for i, x in enumerate((300, 380, 460)):
        e.append(f'<circle cx="{x}" cy="150" r="34" fill="#FFFFFF" stroke="#9BC1E0" stroke-width="5"/>')
        e.append(svgtext(x, 166, str(i + 1), size=44, fill="#4A78A8", weight="bold"))
    e.append(boy(pose="handup", expr="press", cx=680, cy=208, scale=1.25))
    e.append(star(790, 90, 24)); e.append(sparkle(950, 200, 12)); e.append(sparkle(180, 320, 12))
    return svg(W, H, "".join(e))

def scene_p7():
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#CBE3C2"/>')
    # three friends thinking with bubbles
    for i, x in enumerate((260, 594, 928)):
        e.append(kid(variant=i, cx=x, cy=330, scale=1.0, expr="think"))
        bx = x + 70
        e.append(f'<circle cx="{bx-46}" cy="200" r="8" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
        e.append(f'<circle cx="{bx-30}" cy="176" r="12" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
        e.append(f'<ellipse cx="{bx+8}" cy="130" rx="56" ry="38" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="4"/>')
        e.append(f'<circle cx="{bx-8}" cy="130" r="5" fill="#B9CFE8"/><circle cx="{bx+8}" cy="130" r="5" fill="#B9CFE8"/><circle cx="{bx+24}" cy="130" r="5" fill="#B9CFE8"/>')
    return svg(W, H, "".join(e))

def scene_p8():
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#E8D2AC"/>')
    # teacher with speech bubble "Yes!"
    e.append(teacher(cx=250, cy=270, scale=1.0, point="right"))
    e.append(f'<path d="M 350 90 Q 350 40 420 40 L 600 40 Q 660 40 660 90 Q 660 140 600 140 L 470 140 L 420 176 L 436 140 L 420 140 Q 350 140 350 90 Z" fill="#FFFFFF" stroke="#E3C98F" stroke-width="5"/>')
    e.append(svgtext(505, 108, "Yes, Owen!", size=42, fill="#D97706", weight="bold"))
    # boy hand up + pocket open + star popping out
    e.append(boy(pose="handup", expr="big", cx=830, cy=222, scale=1.15))
    e.append(brain_pocket(cx=1030, cy=120, scale=0.85, open_flap=True))
    e.append(star(1030, 66, 24, face=True))
    e.append(sparkle(1090, 36, 12)); e.append(sparkle(966, 44, 10))
    return svg(W, H, "".join(e))

def scene_p9():
    e = []
    e.append(f'<rect x="0" y="470" width="1188" height="90" fill="#F2CFDC"/>')
    # confetti
    import random
    random.seed(7)
    cols = ["#F6C445", "#7BC47F", "#6FA8DC", "#F49AB5", "#E4574C"]
    for i in range(26):
        x, y = random.randint(40, 1148), random.randint(30, 250)
        c = cols[i % 5]
        e.append(f'<rect x="{x}" y="{y}" width="12" height="18" rx="4" fill="{c}" transform="rotate({random.randint(-40,40)} {x} {y})"/>')
    # boy speaking out loud
    e.append(boy(pose="stand", expr="big", cx=560, cy=204, scale=1.2))
    e.append(star(700, 130, 20)); e.append(sparkle(760, 90, 12))
    e.append(f'<path d="M 626 236 q 26 10 26 34 M 654 222 q 40 16 40 54 M 682 208 q 54 22 54 74" '
             f'fill="none" stroke="#D98CA6" stroke-width="7" stroke-linecap="round"/>')
    # friends cheering small
    e.append(kid(variant=0, cx=170, cy=380, scale=0.8, expr="smile"))
    e.append(kid(variant=1, cx=1010, cy=380, scale=0.8, expr="smile"))
    return svg(W, H, "".join(e))

def scene_p10():
    e = []
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="110" fill="#FFDD7E"/>')
    for (x, y, r) in [(160, 120, 20), (1020, 120, 24), (120, 380, 16), (1060, 380, 16), (330, 70, 12), (860, 70, 14)]:
        e.append(star(x, y, r))
    e.append(sparkle(260, 260, 12)); e.append(sparkle(930, 260, 12))
    # hero boy with cape + medal
    e.append(boy(pose="hips", expr="proud", cx=594, cy=180, scale=1.25, cape=True))
    # medal on chest
    e.append(f'<path d="M 574 296 L 594 336 L 614 296" fill="#E4574C"/>')
    e.append(f'<circle cx="594" cy="352" r="30" fill="{STAR_Y}" stroke="{STAR_DK}" stroke-width="5"/>')
    e.append(f'<polygon points="{star_pts(594, 352, 16)}" fill="#FFFFFF"/>')
    return svg(W, H, "".join(e))

# ---------------- PAGE TEXTS ----------------
PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I love school. My brain is full of ideas!'),
    ("p2", scene_p2, 'In class, Tr. Mina asks a question.'),
    ("p3", scene_p3, 'I know it! I know the answer!<br/><b>WOW!</b>'),
    ("p4", scene_p4, 'The answer wants to jump out!<br/>My mouth feels itchy. My body feels hot.<br/><b>Boom, boom</b> goes my heart!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>I save my answer in my <b>brain pocket</b>!'),
    ("p6", scene_p6, 'I close my mouth. I count 1, 2, 3.<br/>I put my hand up <b>HIGH</b>!'),
    ("p7", scene_p7, 'I wait. My friends are thinking too.<br/>Everyone gets a turn.'),
    ("p8", scene_p8, 'Tr. Mina says, &ldquo;Yes, Owen!&rdquo;<br/>I open my pocket. My answer is still there!'),
    ("p9", scene_p9, 'I say it out loud. Everyone can hear me.<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Hand up. Wait. <b>Save it!</b><br/>That is my superpower. I practice every day!'),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("讓孩子替超能力取名字", "書裡叫 &ldquo;Save it!&rdquo;，他想改名就改。全家和老師之後都用同一個詞提醒。"),
    ("讀完玩 2 分鐘角色扮演", "你當老師、他練「閉嘴巴 &rarr; 數 123 &rarr; 舉手」，再交換角色。"),
    ("搭配每日聯絡卡", "請老師每天就 2&ndash;3 條目標打勾；當天達標 &rarr; 當天兌現小獎勵。"),
    ("邀請他加工這本書", "畫畫、貼貼紙、加新頁。參與越多，效果越好。"),
]

def build_html():
    css = f"""
    @font-face {{ font-family: 'Huninn'; src: url('{FONT}'); }}
    @page {{ size: 297mm 210mm; margin: 0; }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: 'Huninn'; }}
    .page {{ width: 297mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; }}
    .page.last {{ page-break-after: auto; }}
    .art {{ position: absolute; top: 4mm; left: 4mm; right: 4mm; height: 140mm; }}
    .band {{ position: absolute; left: 14mm; right: 14mm; bottom: 9mm; height: 50mm;
             background: rgba(255,255,255,0.94); border-radius: 9mm;
             display: flex; align-items: center; justify-content: center;
             text-align: center; padding: 4mm 12mm; }}
    .band .t {{ font-size: 21pt; line-height: 1.45; color: {TXT}; }}
    .band .t b {{ color: #E4574C; }}
    .pnum {{ position: absolute; top: 6mm; right: 8mm; width: 13mm; height: 13mm; border-radius: 50%;
             background: rgba(255,255,255,0.9); color: {TXT}; font-size: 13pt;
             display: flex; align-items: center; justify-content: center; }}
    """

    pages = []

    # ---- COVER ----
    cover_art = scene_cover()
    pages.append(f"""
    <div class="page" style="background:{BG['cover']}">
      <div style="position:absolute; top:6mm; left:0; right:0; text-align:center;">
        <div style="font-size:44pt; color:#4A3B32; letter-spacing:1px;">I Can <span style="color:#E4574C;">Save</span> My Answer!</div>
        <div style="font-size:16pt; color:#8A7460; margin-top:2mm;">&#9733; Owen's superpower story &#9733;</div>
      </div>
      <div style="position:absolute; top:44mm; left:10mm; right:10mm; height:132mm;">{cover_art}</div>
      <div style="position:absolute; bottom:10mm; left:0; right:0; text-align:center; font-size:15pt; color:#8A7460;">
        This book belongs to <span style="display:inline-block; border-bottom:2px dotted #B49B7F; width:60mm;">&nbsp;</span>
      </div>
    </div>""")

    # ---- STORY PAGES ----
    for i, (key, fn, text) in enumerate(PAGES, start=1):
        pages.append(f"""
    <div class="page" style="background:{BG[key]}">
      <div class="pnum">{i}</div>
      <div class="art">{fn()}</div>
      <div class="band"><div class="t">{text}</div></div>
    </div>""")

    # ---- PARENT PAGE ----
    tips = "".join(
        f'<div style="display:flex; margin-bottom:5mm;">'
        f'<div style="min-width:9mm; height:9mm; border-radius:50%; background:#E4574C; color:#fff; '
        f'display:flex; align-items:center; justify-content:center; font-size:13pt; margin-right:5mm;">{i+1}</div>'
        f'<div style="font-size:13.5pt; color:{TXT}; line-height:1.5;"><b>{t}</b>&nbsp;&mdash;&nbsp;{d}</div></div>'
        for i, (t, d) in enumerate(PARENT_TIPS)
    )
    pages.append(f"""
    <div class="page last" style="background:{BG['p11']}">
      <div style="padding: 14mm 22mm;">
        <div style="font-size:24pt; color:{TXT}; margin-bottom:3mm;">給爸爸媽媽的使用說明</div>
        <div style="font-size:12.5pt; color:#8A7460; margin-bottom:8mm;">這是一本社會故事（Social Story）。它的目標不是「講道理」，而是替孩子安裝一套<b>當下用得出來的動作腳本</b>。</div>
        {tips}
        <div style="margin-top:8mm; padding:5mm 7mm; background:#FFF; border-radius:5mm; font-size:12pt; color:#8A7460; line-height:1.55;">
          口訣（全書通關密語）：<b style="color:#E4574C;">Hand up &rarr; Wait &rarr; Save it!</b>&nbsp;&nbsp;
          當他哪天主動說出 &ldquo;My mouth feels itchy&rdquo;（我察覺到衝動了），就是最值得大力稱讚的時刻。
        </div>
      </div>
    </div>""")

    html = f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(pages)}</body></html>"
    return html


if __name__ == "__main__":
    html = build_html()
    with open("book.html", "w", encoding="utf-8") as f:
        f.write(html)
    from weasyprint import HTML
    HTML(string=html, base_url=".").write_pdf("I_Can_Save_My_Answer.pdf")
    print("PDF done")
