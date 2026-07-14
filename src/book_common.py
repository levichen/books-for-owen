# -*- coding: utf-8 -*-
"""跨書共用：SVG 小工具、字型路徑、viewBox 常數。每本書一個 book_<slug>.py 模組。"""
import os

FONT_PATH = os.path.abspath(os.environ.get("HUNINN_TTF", "../assets/fonts/jf-openhuninn-2.0.ttf"))
FONT = "file://" + FONT_PATH
TXT = "#4A3B32"

W, H = 1188, 560       # 故事頁插圖 viewBox（297mm × 140mm 比例）
COVER_W, COVER_H = 1188, 620   # 封面插圖 viewBox


def svg(w, h, inner, bg=None):
    r = (f'<svg viewBox="0 0 {w} {h}" width="100%" height="100%" '
         f'preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">')
    if bg:
        r += f'<rect x="0" y="0" width="{w}" height="{h}" fill="{bg}"/>'
    return r + inner + "</svg>"


def svgtext(x, y, s, size=48, fill=TXT, weight="normal", anchor="middle", family="Huninn"):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{s}</text>')


def vocab_sentence(pages, word):
    """生字複習頁用：從 PAGES 文案中找出第一個含該生字的句段（保留 <b> 標記）。
    找不到時回空字串（呼叫端自行處理）。"""
    import re
    wl = word.lower()
    for _key, _fn, text in pages:
        for seg in text.split("<br/>"):
            plain = re.sub(r"<[^>]+>", "", seg).lower()
            if wl in plain:
                return seg.strip()
    return ""
