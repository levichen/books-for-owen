# -*- coding: utf-8 -*-
"""多書 PDF 渲染器（A4 橫式）。用法：
    python3 render_pdf.py           # 渲染全部書
    python3 render_pdf.py <slug>    # 只渲染一本（如 wait-my-spot）
書籍內容在 book_<slug>.py，由 books_all.load_books() 自動發現。"""
import sys
from book_common import FONT, TXT, vocab_sentence
from books_all import load_books


def build_html(book):
    bg = book["bg"]
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
    pages.append(f"""
    <div class="page" style="background:{bg['cover']}">
      <div style="position:absolute; top:6mm; left:0; right:0; text-align:center;">
        <div style="font-size:44pt; color:#4A3B32; letter-spacing:1px;">{book['title_pre']}<span style="color:#E4574C;">{book['title_hi']}</span>{book['title_post']}</div>
        <div style="font-size:16pt; color:#8A7460; margin-top:2mm;">&#9733; {book['subtitle']} &#9733;</div>
      </div>
      <div style="position:absolute; top:44mm; left:10mm; right:10mm; height:132mm;">{book['cover']()}</div>
      <div style="position:absolute; bottom:10mm; left:0; right:0; text-align:center; font-size:15pt; color:#8A7460;">
        This book belongs to <span style="display:inline-block; border-bottom:2px dotted #B49B7F; width:60mm;">&nbsp;</span>
      </div>
    </div>""")

    # ---- STORY PAGES ----
    for i, (key, fn, text) in enumerate(book["pages"], start=1):
        pages.append(f"""
    <div class="page" style="background:{bg[key]}">
      <div class="pnum">{i}</div>
      <div class="art">{fn()}</div>
      <div class="band"><div class="t">{text}</div></div>
    </div>""")

    # ---- VOCAB REVIEW PAGE（倒數第二頁：生字複習；零生字書自動略過）----
    vocab = book.get("vocab") or []
    if vocab:
        vrows = []
        for w in vocab:
            sent = vocab_sentence(book["pages"], w)
            vrows.append(
                f'<div style="display:flex; align-items:center; background:#FFFFFF; border-radius:8mm; '
                f'padding:8mm 12mm; margin-bottom:7mm;">'
                f'<div style="min-width:78mm; font-size:34pt; color:#E4574C;">&#9733; {w}</div>'
                f'<div style="font-size:16pt; color:{TXT}; line-height:1.55;">{sent}</div></div>')
        pages.append(f"""
    <div class="page" style="background:{bg['p10']}">
      <div class="pnum">{len(book['pages']) + 1}</div>
      <div style="padding: 16mm 24mm;">
        <div style="font-size:30pt; color:{TXT}; text-align:center; margin-bottom:10mm;">&#9733; My New Words! &#9733;</div>
        {''.join(vrows)}
        <div style="text-align:center; font-size:16pt; color:#8A7460; margin-top:10mm;">Read it. Say it. Use it!</div>
      </div>
    </div>""")

    # ---- PARENT PAGE ----
    tips = "".join(
        f'<div style="display:flex; margin-bottom:5mm;">'
        f'<div style="min-width:9mm; height:9mm; border-radius:50%; background:#E4574C; color:#fff; '
        f'display:flex; align-items:center; justify-content:center; font-size:13pt; margin-right:5mm;">{i+1}</div>'
        f'<div style="font-size:13.5pt; color:{TXT}; line-height:1.5;"><b>{t}</b>&nbsp;&mdash;&nbsp;{d}</div></div>'
        for i, (t, d) in enumerate(book["parent_tips"])
    )
    pages.append(f"""
    <div class="page last" style="background:{bg['p11']}">
      <div style="padding: 14mm 22mm;">
        <div style="font-size:24pt; color:{TXT}; margin-bottom:3mm;">給爸爸媽媽的使用說明</div>
        <div style="font-size:12.5pt; color:#8A7460; margin-bottom:8mm;">{book['parent_intro']}</div>
        {tips}
        <div style="margin-top:8mm; padding:5mm 7mm; background:#FFF; border-radius:5mm; font-size:12pt; color:#8A7460; line-height:1.55;">
          {book['cue_html']}
        </div>
      </div>
    </div>""")

    return f"<!DOCTYPE html><html><head><meta charset='utf-8'><style>{css}</style></head><body>{''.join(pages)}</body></html>"


if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    from weasyprint import HTML
    for book in load_books():
        if only and book["slug"] != only:
            continue
        html = build_html(book)
        HTML(string=html, base_url=".").write_pdf(book["pdf_name"])
        print("PDF done:", book["pdf_name"])
