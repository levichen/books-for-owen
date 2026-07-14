# -*- coding: utf-8 -*-
"""Book: My Quiet Morning — 清晨不吵醒媽媽（waiting for 6:30）"""
from parts import *
from book_common import svg, svgtext, TXT, W, H

# soft page palettes — 清晨色調：p1~p6 深藍→紫藍暗色、p8 起晨光轉亮、p9 廚房陽光
BG = {
    "cover": "#FFF4D6", "p1": "#1A2A4A", "p2": "#1F2D4F", "p3": "#2A3355",
    "p4": "#2E3860", "p5": "#3D2E5A", "p6": "#2B3A55", "p7": "#5A7080",
    "p8": "#4A5F75", "p9": "#FFE8B6", "p10": "#FFF4D6", "p11": "#FBF4E8",
}

# ============== SCENES ==============

def scene_cover():
    """封面：暖色、Owen 白T、大時鐘 6:30、星星月亮氛圍"""
    e = []
    # stars & moon
    for (x, y, r) in [(140, 100, 18), (280, 140, 16), (1010, 80, 20), (1050, 160, 14)]:
        e.append(star(x, y, r))
    e.append(f'<circle cx="220" cy="200" r="32" fill="#FFF9D6" stroke="#E8C25F" stroke-width="3"/>')
    e.append(sparkle(320, 90, 12)); e.append(sparkle(950, 280, 12))
    # ground
    e.append(f'<ellipse cx="594" cy="640" rx="560" ry="120" fill="#FFDD7E"/>')
    # Owen standing waving, white T
    e.append(boy(pose="stand", expr="big", cx=420, cy=220, scale=1.3))
    # Big clock 6:30 on the right
    e.append(clock_digital(cx=850, cy=240, scale=1.5, time="6:30", glow=True))
    return svg(1188, 620, "".join(e), bg=BG["cover"])

def scene_p1():
    """清晨臥室：Owen 從被子裡坐起，窗外深藍將亮的天空、殘星"""
    e = []
    # 窗戶：深藍天空
    e.append(f'<rect x="820" y="20" width="320" height="280" rx="8" fill="#0F1820" stroke="#4A3A30" stroke-width="6"/>')
    e.append(f'<line x1="980" y1="20" x2="980" y2="300" stroke="#4A3A30" stroke-width="4"/>')
    e.append(f'<line x1="820" y1="160" x2="1140" y2="160" stroke="#4A3A30" stroke-width="4"/>')
    # 窗外深藍漸亮、殘星
    e.append(star(850, 50, 12)); e.append(star(1100, 120, 14)); e.append(sparkle(920, 80, 10))
    # 床框：棕色
    e.append(f'<rect x="80" y="240" width="520" height="260" rx="12" fill="#8B6F47" stroke="#5A4530" stroke-width="4"/>')
    e.append(f'<rect x="100" y="260" width="480" height="220" fill="#E8D9C5"/>')  # mattress
    # 床上：被子 + Owen 坐起的頭
    e.append(f'<path d="M 100 380 Q 200 320 340 340 L 340 440 L 100 450 Z" fill="#F2A9A0" stroke="#D97060" stroke-width="2"/>')
    e.append(head(expr="big", cx=290, cy=320, scale=1.1))
    # text background
    e.append(f'<rect x="50" y="460" width="1088" height="90" fill="none"/>')
    return svg(W, H, "".join(e), bg=BG["p1"])

def scene_p2():
    """床頭數字時鐘特寫 5:30（左格焦點）；旁邊大床上媽媽 April 睡著（右格）"""
    e = []
    # 左格：床頭櫃 + 放大的時鐘焦點
    e.append(f'<rect x="60" y="320" width="280" height="180" rx="12" fill="#C4A272" stroke="#8B6F47" stroke-width="4"/>')
    e.append(f'<rect x="80" y="340" width="240" height="140" fill="#D4B896"/>')  # 櫃面
    # 放大的 clock_digital（床頭櫃上）
    e.append(f'<circle cx="210" cy="160" r="130" fill="#F4D9A0" fill-opacity="0.12"/>')  # 小夜燈光暈
    e.append(clock_digital(cx=210, cy=160, scale=1.8, time="5:30", glow=False))

    # 右格：Owen 的床 + April asleep
    # 床框（棕色床頭板 + 床腳）
    e.append(f'<rect x="520" y="80" width="600" height="360" rx="14" fill="#8B6F47" stroke="#5A4530" stroke-width="5"/>')
    # 床墊面（淺色）
    e.append(f'<rect x="555" y="115" width="530" height="290" rx="10" fill="#E8D9C5"/>')
    # 床上：枕頭 + April asleep
    e.append(f'<ellipse cx="630" cy="155" rx="65" ry="30" fill="#FFFFFF" stroke="#E5D9C9" stroke-width="2"/>')  # 枕頭
    # April 睡著（頭靠在枕頭上）
    e.append(april_asleep(cx=720, cy=200, scale=1.0))

    return svg(W, H, "".join(e), bg=BG["p2"])

def scene_p3():
    """Owen 星星眼扒在媽媽床邊，頭上思考泡泡裡是積木和繪本"""
    e = []
    # 床框 & April sleeping
    e.append(f'<rect x="620" y="140" width="480" height="300" rx="12" fill="#8B6F47" stroke="#5A4530" stroke-width="4"/>')
    e.append(f'<rect x="640" y="160" width="440" height="260" fill="#E8D9C5"/>')
    e.append(april_asleep(cx=770, cy=240, scale=1.0))
    # Owen head 靠著床邊（星星眼）
    e.append(head(expr="star", cx=380, cy=280, scale=1.0))
    # 思考泡泡：大橢圓 + 積木和書
    e.append(f'<ellipse cx="550" cy="120" rx="140" ry="100" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="5"/>')
    e.append(f'<circle cx="400" cy="140" r="8" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
    e.append(f'<circle cx="420" cy="100" r="12" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
    e.append(f'<circle cx="490" cy="80" r="14" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
    # 積木（紅、藍、黃方塊）
    e.append(f'<rect x="480" y="100" width="28" height="28" fill="#E4574C" stroke="#B83C2D" stroke-width="2"/>')
    e.append(f'<rect x="520" y="105" width="28" height="28" fill="#5CA8E8" stroke="#3A7DB8" stroke-width="2"/>')
    e.append(f'<rect x="560" y="100" width="32" height="32" fill="#FFD34D" stroke="#E8A20C" stroke-width="2"/>')
    # 繪本（棕色書脊）
    e.append(f'<rect x="480" y="140" width="20" height="28" fill="#8B6F47" stroke="#5A4530" stroke-width="2"/>')
    e.append(f'<rect x="480" y="140" width="20" height="4" fill="#FFE9C2"/>')
    return svg(W, H, "".join(e), bg=BG["p3"])

def scene_p4():
    """衝動頁：Owen 在自己床上彈起（jump 姿勢），嘴邊音量波紋，四周紅熱氣線"""
    e = []
    # 床框（棕色床頭板 + 床腳）
    e.append(f'<rect x="80" y="200" width="420" height="280" rx="12" fill="#8B6F47" stroke="#5A4530" stroke-width="4"/>')
    # 床墊面（淺色）
    e.append(f'<rect x="105" y="225" width="370" height="240" rx="8" fill="#E8D9C5"/>')
    # 枕頭
    e.append(f'<ellipse cx="170" cy="260" rx="55" ry="26" fill="#FFFFFF" stroke="#E5D9C9" stroke-width="2"/>')
    # 被子（覆蓋下半身）
    e.append(f'<rect x="105" y="310" width="370" height="155" rx="10" fill="#F2A9A0" stroke="#D97060" stroke-width="2"/>')

    # 紅熱氣線（四角）
    for (x, y) in [(150, 100), (450, 120), (120, 420), (480, 440)]:
        for i in range(3):
            e.append(f'<path d="M {x+i*30} {y} q 8 -10 16 0 q 8 10 16 0" '
                    f'fill="none" stroke="#E85A54" stroke-width="5" stroke-linecap="round"/>')

    # Owen jump 在床上
    e.append(boy(pose="jump", expr="big", cx=290, cy=290, scale=1.15))

    # 彈跳線（床邊上下）
    for x in [220, 290, 360]:
        e.append(f'<line x1="{x}" y1="465" x2="{x}" y2="420" stroke="#E85A54" stroke-width="8" stroke-linecap="round"/>')
        e.append(f'<circle cx="{x}" cy="415" r="3.5" fill="#E85A54"/>')

    # 嘴邊音量波紋（忍住的聲音）
    e.append(f'<path d="M 325 280 Q 345 275 365 280" fill="none" stroke="#E8944A" stroke-width="5" stroke-linecap="round"/>')
    e.append(f'<path d="M 330 300 Q 352 292 372 305" fill="none" stroke="#E8944A" stroke-width="5" stroke-linecap="round"/>')

    # 床搖晃視覺線
    e.append(f'<path d="M 100 230 L 92 222 M 500 230 L 508 222" stroke="#8B6F47" stroke-width="6" stroke-linecap="round"/>')

    return svg(W, H, "".join(e), bg=BG["p4"])

def scene_p5():
    """紫色星空背景：Owen（press 表情）站立，手指比在嘴前，身上柔和月光光暈"""
    e = []
    # 星星滿天
    for (x, y, r) in [(140, 80, 14), (1010, 120, 16), (200, 420, 12), (1040, 400, 14), (600, 100, 10)]:
        e.append(star(x, y, r))
    e.append(sparkle(320, 200, 12)); e.append(sparkle(880, 320, 12))
    # 月亮
    e.append(f'<circle cx="1080" cy="180" r="36" fill="#F9F4D0" stroke="#E8C25F" stroke-width="3"/>')
    # Owen 身上月光光暈
    e.append(f'<circle cx="594" cy="280" r="140" fill="#F9F4D0" fill-opacity="0.08"/>')
    # Owen 站立 press 表情（嘴前手指）
    e.append(boy(pose="stand", expr="press", cx=594, cy=280, scale=1.2))
    # 手指指向嘴（手臂與部分手指指）
    e.append(f'<circle cx="540" cy="310" r="8" fill="{SKIN}"/>')  # 手指
    e.append(f'<line x1="548" y1="310" x2="570" y2="305" stroke="{SKIN}" stroke-width="8" stroke-linecap="round"/>')  # 手腕連接
    # "Shh..." 語音泡泡
    e.append(f'<ellipse cx="750" cy="180" rx="90" ry="50" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="4"/>')
    e.append(f'<circle cx="690" cy="220" r="6" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
    e.append(f'<circle cx="670" cy="235" r="8" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
    return svg(W, H, "".join(e), bg=BG["p5"])

def scene_p6():
    """兩格選項：左格 Owen 頭靠在媽媽旁邊被窩＋愛心；右格 Owen 踮腳走向玩具角"""
    e = []
    # 左格框（圓角矩形）
    e.append(f'<rect x="50" y="50" width="520" height="450" rx="20" fill="#2B3A55" stroke="#6A7F99" stroke-width="4" fill-opacity="0.6"/>')
    # 左格：床框 + April asleep + Owen head（縮小）
    e.append(f'<rect x="100" y="100" width="420" height="300" rx="10" fill="#8B6F47" stroke="#5A4530" stroke-width="3"/>')
    # 床墊面
    e.append(f'<rect x="115" y="125" width="390" height="260" rx="8" fill="#E8D9C5"/>')
    # 枕頭
    e.append(f'<ellipse cx="160" cy="160" rx="50" ry="24" fill="#FFFFFF" stroke="#E5D9C9" stroke-width="2"/>')
    # April asleep（縮小）
    e.append(april_asleep(cx=210, cy=190, scale=0.75))
    # Owen 頭（縮小到 April 的 ~75%）
    e.append(head(expr="sleep", cx=330, cy=200, scale=0.65))  # 靠著被子
    # 愛心（左上角）
    e.append(f'<path d="M 380 130 C 380 118 388 110 397 110 C 406 110 414 118 414 130 C 414 142 397 155 397 155 C 397 155 380 142 380 130 Z" fill="#F26B8E" stroke="#D9467F" stroke-width="2"/>')
    e.append(f'<path d="M 345 125 C 345 115 351 108 359 108 C 367 108 373 115 373 125 C 373 135 359 145 359 145 C 359 145 345 135 345 125 Z" fill="#F26B8E" stroke="#D9467F" stroke-width="2"/>')

    # 右格框（圓角矩形）
    e.append(f'<rect x="618" y="50" width="520" height="450" rx="20" fill="#2B3A55" stroke="#6A7F99" stroke-width="4" fill-opacity="0.6"/>')
    # 右格：玩具角 + Owen 踮腳
    # 積木堆
    e.append(f'<rect x="680" y="320" width="28" height="28" fill="#E4574C" stroke="#B83C2D" stroke-width="2"/>')
    e.append(f'<rect x="715" y="328" width="28" height="28" fill="#5CA8E8" stroke="#3A7DB8" stroke-width="2"/>')
    e.append(f'<rect x="750" y="320" width="32" height="32" fill="#FFD34D" stroke="#E8A20C" stroke-width="2"/>')
    e.append(f'<rect x="695" y="355" width="28" height="28" fill="#7BC47F" stroke="#5A9E5F" stroke-width="2"/>')
    # 書（棕色）
    e.append(f'<rect x="750" y="350" width="24" height="36" fill="#8B6F47" stroke="#5A4530" stroke-width="2"/>')
    e.append(f'<path d="M 750 350 L 774 350" stroke="#FFE9C2" stroke-width="3"/>')
    # Owen 踮腳走
    e.append(boy(pose="walk", expr="smile", cx=800, cy=280, scale=1.0))
    # 時鐘小版本 5:30（右上）
    e.append(clock_digital(cx=1060, cy=120, scale=1.0, time="5:30", glow=False))

    return svg(W, H, "".join(e), bg=BG["p6"])

def scene_p7():
    """觀點頁：兩格對比——累累的媽媽（灰藍色、眼下陰影）vs 睡飽的媽媽（亮色、april cheer）"""
    e = []
    # 左格：累媽媽（灰藍背景）
    e.append(f'<rect x="50" y="80" width="500" height="400" rx="16" fill="#7A8A9A" fill-opacity="0.4"/>')
    # 灰藍色光線
    e.append(f'<rect x="50" y="80" width="500" height="400" fill="none" stroke="#6A7A8A" stroke-width="3" rx="16"/>')
    # 累媽媽：april stand，加眼下陰影
    e.append(april(cx=300, cy=240, scale=1.1, pose="stand"))
    # 眼下陰影（半月形）
    e.append(f'<path d="M 270 265 Q 280 270 290 265" fill="#5A6A7A" fill-opacity="0.3"/>')
    e.append(f'<path d="M 310 265 Q 320 270 330 265" fill="#5A6A7A" fill-opacity="0.3"/>')

    # 右格：睡飽媽媽（亮色背景）
    e.append(f'<rect x="638" y="80" width="500" height="400" rx="16" fill="#B8D4E0" fill-opacity="0.4"/>')
    e.append(f'<rect x="638" y="80" width="500" height="400" fill="none" stroke="#9AC4D4" stroke-width="3" rx="16"/>')
    # 睡飽媽媽：april cheer，充滿活力
    e.append(april(cx=888, cy=240, scale=1.1, pose="cheer"))
    # 小星星光環
    e.append(star(850, 140, 12)); e.append(star(920, 150, 10)); e.append(sparkle(1000, 180, 8))

    return svg(W, H, "".join(e), bg=BG["p7"])

def scene_p8():
    """時鐘跳到發光的 6:30 + 小星星；Owen 在床邊輕聲說話（語音泡泡含文字），April 張開手臂"""
    e = []
    # 床框（棕色床頭板 + 床腳）
    e.append(f'<rect x="250" y="180" width="420" height="290" rx="12" fill="#8B6F47" stroke="#5A4530" stroke-width="4"/>')
    # 床墊面
    e.append(f'<rect x="270" y="205" width="380" height="250" rx="8" fill="#E8D9C5"/>')
    # 枕頭
    e.append(f'<ellipse cx="330" cy="245" rx="60" ry="28" fill="#FFFFFF" stroke="#E5D9C9" stroke-width="2"/>')
    # 被子
    e.append(f'<rect x="270" y="295" width="380" height="140" rx="8" fill="#F2A9A0" stroke="#D97060" stroke-width="2"/>')

    # April 醒來（張手 cheer）
    e.append(april(cx=420, cy=300, scale=1.0, pose="cheer"))

    # Owen 在床邊（左側）
    e.append(boy(pose="stand", expr="smile", cx=310, cy=330, scale=1.0))

    # 語音泡泡（含文字"Good morning, Mommy!"）
    e.append(f'<ellipse cx="380" cy="140" rx="110" ry="65" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="4"/>')
    e.append(f'<circle cx="280" cy="190" r="8" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
    e.append(f'<circle cx="255" cy="210" r="10" fill="#FFFFFF" stroke="#B9CFE8" stroke-width="3"/>')
    # 泡泡內文字
    e.append(svgtext(380, 145, "Good morning,", size=22, fill="#D97060", weight="bold"))
    e.append(svgtext(380, 168, "Mommy!", size=22, fill="#D97060", weight="bold"))

    # 大時鐘 6:30 發光（右上）
    e.append(clock_digital(cx=900, cy=180, scale=1.8, time="6:30", glow=True))

    # 小星星
    e.append(star(1040, 100, 14)); e.append(sparkle(920, 280, 10))

    return svg(W, H, "".join(e), bg=BG["p8"])

def scene_p9():
    """廚房：Owen 和 April 一起做鬆餅，陽光從窗戶進來"""
    e = []
    # 窗戶（陽光）
    e.append(f'<rect x="820" y="40" width="300" height="280" rx="8" fill="#FFF9E6" stroke="#D4B896" stroke-width="5"/>')
    e.append(f'<line x1="970" y1="40" x2="970" y2="320" stroke="#D4B896" stroke-width="3"/>')
    e.append(f'<line x1="820" y1="180" x2="1120" y2="180" stroke="#D4B896" stroke-width="3"/>')
    # 窗邊陽光光暈
    e.append(f'<ellipse cx="1000" cy="200" rx="220" ry="160" fill="#FFE8B6" fill-opacity="0.12"/>')

    # 廚房流理台（棕色長方形）
    e.append(f'<rect x="100" y="280" width="600" height="220" rx="10" fill="#D4B896" stroke="#8B6F47" stroke-width="4"/>')
    e.append(f'<rect x="115" y="300" width="570" height="180" fill="#F5E6D3"/>')  # 台面

    # 平底鍋 + 鬆餅
    e.append(f'<ellipse cx="300" cy="350" rx="80" ry="35" fill="#4A4A4A" stroke="#2A2A2A" stroke-width="3"/>')
    # 鬆餅（棕色圓形 + 方格）
    e.append(f'<circle cx="300" cy="340" r="42" fill="#C9A26B" stroke="#8B6F47" stroke-width="2"/>')
    for i in range(2):
        for j in range(2):
            e.append(f'<rect x="{285+i*30}" y="{325+j*30}" width="28" height="28" fill="none" stroke="#8B6F47" stroke-width="1.5"/>')

    # April 站著拿著鬆餅
    e.append(april(cx=420, cy=260, scale=1.1, pose="stand"))

    # Owen 踮腳幫忙，開心表情
    e.append(boy(pose="walk", expr="big", cx=200, cy=300, scale=1.0))

    # 早餐盤子（右側）
    e.append(f'<circle cx="580" cy="340" r="38" fill="#FFF" stroke="#C9BFA8" stroke-width="3"/>')
    e.append(f'<circle cx="580" cy="340" r="34" fill="none" stroke="#E8D4B8" stroke-width="2"/>')

    return svg(W, H, "".join(e), bg=BG["p9"])

def scene_p10():
    """英雄收尾：Owen 披紅披風叉腰（hips pose），旁邊立著大時鐘顯示 6:30，滿天小星星"""
    e = []
    # 滿天星星
    for (x, y, r) in [(120, 80, 16), (280, 60, 14), (920, 100, 18), (1040, 140, 12),
                       (160, 420, 14), (1000, 420, 16), (600, 80, 12)]:
        e.append(star(x, y, r))
    e.append(sparkle(340, 200, 10)); e.append(sparkle(880, 320, 12))

    # 金色地面光暈
    e.append(f'<ellipse cx="594" cy="560" rx="520" ry="100" fill="#FFDD7E" fill-opacity="0.6"/>')

    # Owen 英雄姿勢（hips + cape + proud）
    e.append(boy(pose="hips", expr="proud", cx=380, cy=260, scale=1.25, cape=True))

    # 大時鐘 6:30（右側，發光）
    e.append(clock_digital(cx=880, cy=240, scale=2.0, time="6:30", glow=True))

    return svg(W, H, "".join(e), bg=BG["p10"])


# ============== PAGE TEXTS ================
PAGES = [
    ("p1", scene_p1, 'This is me, <b>Owen</b>!<br/>I wake up early. The sky is still sleepy.'),
    ("p2", scene_p2, 'My clock says <b>5:30</b>.<br/>Mommy April is still sleeping.'),
    ("p3", scene_p3, 'I want to play!<br/>I want to wake Mommy <b>NOW</b>!'),
    ("p4", scene_p4, 'My body wants to <b>bounce</b>!<br/>My voice wants to be LOUD.<br/><b>Shake, shake</b> goes my bed!'),
    ("p5", scene_p5, '<b>STOP!</b> I use my superpower&hellip;<br/>Shh&hellip; quiet power <b>ON</b>!'),
    ("p6", scene_p6, 'I check my clock. Not 6:30 yet!<br/>I stay close to Mommy,<br/>or I <b>tiptoe</b> out and play.'),
    ("p7", scene_p7, 'Mommy needs sleep.<br/>Sleep makes Mommy strong and happy.<br/>Then Mommy can play with me!'),
    ("p8", scene_p8, 'Ding! My clock says <b>6:30</b>!<br/>I <b>whisper</b>, &ldquo;Good morning, Mommy!&rdquo;<br/>Mommy hugs me. &ldquo;Thank you, <b>Owen</b>!&rdquo;'),
    ("p9", scene_p9, 'We make breakfast together. Pancakes!<br/>I feel <b>GREAT</b>!'),
    ("p10", scene_p10, 'Check my clock. Play quiet.<br/><b>Wait for 6:30!</b><br/>I practice every day!'),
]

PARENT_TIPS = [
    ("只在平靜時光共讀", "睡前最好。每週讀 3&ndash;4 次，重複是關鍵，讓腳本自動化。"),
    ("出事後絕對不拿出來讀", "一旦變成懲罰教材，這本書就報廢了。"),
    ("檢查家裡有沒有時鐘", "床邊的數字時鐘得夠大、夠清楚，Owen 坐起來就能看到（可用手機放在床頭櫃）。"),
    ("「Wait for 6:30」成為全家咒語", "讀完玩 2 分鐘角色扮演：你當睡著的媽媽、他練「看時鐘 → 安靜玩 → 等 6:30 → 輕聲說早安」。再交換。"),
    ("接納「My body wants to bounce」", "當他主動說出這句 = 他察覺到衝動信號了，馬上大力稱讚。這是最關鍵的勝利。"),
    ("規則絕對一致：早晚都是 6:30", "不要因為想多睡就臨時改成 7:00——規則一動搖，整個等待框架就瓦解了。"),
]

BOOK = {
    "slug": "quiet-morning",
    "order": 4,
    "title_pre": "My ", "title_hi": "Quiet", "title_post": " Morning!",
    "title_zh": "安靜的早晨",
    "subtitle": "Owen's morning story",
    "tagline_zh": "Owen 的早晨故事",
    "chips": ["Social Story", "Morning", "12 pages"],
    "pdf_name": "My_Quiet_Morning.pdf",
    "bg": BG,
    "pages": PAGES,
    "vocab": ['bounce', 'tiptoe', 'whisper'],
    "parent_tips": PARENT_TIPS,
    "parent_intro": ("這是一本社會故事（Social Story）。清晨 5:30 醒來很正常，"
                     "但吵醒睡夢中的媽媽不是。這本書教 Owen 兩套合法選項："
                     "<b>靠著媽媽安靜窩著、或自己安靜玩——直到時鐘 6:30</b>。"),
    "cue_html": ("口訣（全書通關密語）：<b>Check my clock → Play quiet → Wait for 6:30!</b>&nbsp;"
                 "當他哪天主動說出 &ldquo;My body wants to bounce&rdquo;（我察覺到衝動了），"
                 "就是最值得大力稱讚的時刻。"),
    "cover": scene_cover,
}
