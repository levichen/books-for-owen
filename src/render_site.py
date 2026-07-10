# -*- coding: utf-8 -*-
"""Build a GitHub Pages static site: Owen's little library + interactive book reader.
Single content source (build_book.PAGES / scenes) -> web renderer."""
import os, re, subprocess, html
from render_pdf import PAGES, PARENT_TIPS, BG, scene_cover, TXT

SITE = "../site"
BOOK_SLUG = "save-my-answer"
BOOK_TITLE_EN = "I Can Save My Answer!"
BOOK_TITLE_ZH = "把答案存起來"

os.makedirs(f"{SITE}/assets", exist_ok=True)
os.makedirs(f"{SITE}/books/{BOOK_SLUG}", exist_ok=True)

# ---------------------------------------------------------------- reader page
def reader_html():
    css = f"""
@font-face {{ font-family:'Huninn'; src:url('../../assets/huninn.woff2') format('woff2'); font-display:swap; }}
*{{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}}
html,body{{height:100%}}
body{{font-family:'Huninn',system-ui,sans-serif;background:#FBF4E8;display:flex;flex-direction:column}}
header{{display:flex;align-items:center;justify-content:space-between;padding:10px 16px}}
header a{{color:#8A7460;text-decoration:none;font-size:15px;background:#fff;border-radius:999px;padding:6px 14px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
header .ttl{{color:#4A3B32;font-size:16px}}
#stage{{flex:1;overflow:auto;display:flex;align-items:center;justify-content:center;padding:14px 12px}}
.pg{{display:none;width:min(96vw,1080px,calc((100vh - 185px)*2.12));width:min(96vw,1080px,calc((100dvh - 185px)*2.12))}}
body.fs .pg{{width:min(96vw,1080px,calc((100vh - 125px)*2.12));width:min(96vw,1080px,calc((100dvh - 125px)*2.12))}}
.pg.on{{display:block}}
.card{{background:var(--bg,#FFE9A8);border-radius:26px;padding:14px;box-shadow:0 10px 30px rgba(74,59,50,.12)}}
.art svg{{width:100%;height:auto;display:block}}
.band{{background:rgba(255,255,255,.95);border-radius:18px;padding:14px 20px;text-align:center;
      font-size:clamp(17px,2.7vw,25px);line-height:1.55;color:{TXT};margin-top:12px}}
.band b{{color:#E4574C}}
.cover-ttl{{text-align:center;padding:6px 0 10px}}
.cover-ttl .t1{{font-size:clamp(26px,5vw,44px);color:{TXT}}}
.cover-ttl .t1 span{{color:#E4574C}}
.cover-ttl .t2{{font-size:clamp(13px,2vw,18px);color:#8A7460;margin-top:4px}}
.parent{{background:#fff;border-radius:18px;padding:18px 20px;color:{TXT};font-size:15px;line-height:1.7}}
.parent h2{{font-size:20px;margin-bottom:6px}}
.parent .sub{{color:#8A7460;font-size:13.5px;margin-bottom:12px}}
.parent .tip{{display:flex;gap:10px;margin-bottom:10px}}
.parent .n{{min-width:26px;height:26px;border-radius:50%;background:#E4574C;color:#fff;display:flex;
           align-items:center;justify-content:center;font-size:14px;flex:none;margin-top:2px}}
.parent .cue{{margin-top:12px;background:#FBF4E8;border-radius:12px;padding:10px 14px;font-size:14px;color:#8A7460}}
.parent .cue b{{color:#E4574C}}
button{{border:none;cursor:pointer;font-family:inherit}}
#prev,#next{{position:fixed;top:50%;transform:translateY(-50%);z-index:8;width:52px;height:52px;border-radius:50%;
 background:rgba(228,87,76,.9);color:#fff;font-size:24px;box-shadow:0 4px 12px rgba(228,87,76,.3);
 display:flex;align-items:center;justify-content:center}}
#prev{{left:max(8px,env(safe-area-inset-left))}}
#next{{right:max(8px,env(safe-area-inset-right))}}
#prev:disabled,#next:disabled{{background:rgba(229,217,201,.75);box-shadow:none;cursor:default}}
#cnt{{position:fixed;bottom:max(10px,env(safe-area-inset-bottom));left:50%;transform:translateX(-50%);z-index:8;
 color:#8A7460;font-size:13px;background:rgba(255,255,255,.85);border-radius:999px;padding:4px 14px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
#fsbtn{{display:flex;align-items:center;gap:6px;width:auto;height:auto;background:#fff;color:#8A7460;
      font-size:15px;font-family:inherit;border-radius:999px;padding:6px 14px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
#fsexit{{display:none;position:fixed;top:max(12px,env(safe-area-inset-top));right:max(12px,env(safe-area-inset-right));z-index:9;width:auto;height:auto;
        align-items:center;gap:6px;padding:7px 14px;border-radius:999px;font-family:inherit;
        background:rgba(74,59,50,.55);color:#fff;font-size:14px;box-shadow:none}}
body.fs header{{display:none}}
body.fs #fsexit{{display:flex}}
body.fs #cnt{{display:none}}
@media (max-width:719px){{ #fsbtn span{{display:none}} }}
/* 橫向手機：視口矮，壓縮間距並加大高度預算，讓整頁塞進畫面 */
@media (max-height:520px){{
 header{{padding:6px 16px}}
 .card{{padding:10px;border-radius:18px}}
 .band{{padding:8px 14px;font-size:15px;margin-top:8px}}
 #prev,#next{{width:44px;height:44px;font-size:19px}}
 #cnt{{bottom:6px;font-size:12px}}
 .cover-ttl{{padding:2px 0 6px}} .cover-ttl .t1{{font-size:24px}} .cover-ttl .t2{{font-size:12px}}
 .pg,.pg.on{{width:min(96vw,calc((100vh - 148px)*2.12))}}
 .pg,.pg.on{{width:min(96vw,calc((100dvh - 148px)*2.12))}}
 body.fs .pg{{width:min(96vw,calc((100vh - 112px)*2.12))}}
 body.fs .pg{{width:min(96vw,calc((100dvh - 112px)*2.12))}}
}}
"""
    js = """
const pgs=[...document.querySelectorAll('.pg')];let i=0;
const prev=document.getElementById('prev'),next=document.getElementById('next'),cnt=document.getElementById('cnt');
function go(n){i=Math.max(0,Math.min(pgs.length-1,n));
 pgs.forEach((p,k)=>p.classList.toggle('on',k===i));
 cnt.textContent=(i+1)+' / '+pgs.length;
 prev.disabled=(i===0);next.disabled=(i===pgs.length-1);
 document.getElementById('stage').scrollTop=0;}
prev.onclick=()=>go(i-1);next.onclick=()=>go(i+1);
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(i+1);if(e.key==='ArrowLeft')go(i-1);});
let sx=0;
document.addEventListener('touchstart',e=>{sx=e.touches[0].clientX;},{passive:true});
document.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-sx;
 if(Math.abs(dx)>60)go(i+(dx<0?1:-1));},{passive:true});
// 全螢幕：桌機/Android/iPad 走 Fullscreen API；iPhone Safari 不支援，退回 CSS 假全螢幕（body.fs）
const root=document.documentElement;
function setFS(on){document.body.classList.toggle('fs',on);
 if(on){if(root.requestFullscreen)root.requestFullscreen().catch(()=>{});
  else if(root.webkitRequestFullscreen)root.webkitRequestFullscreen();}
 else{if(document.fullscreenElement&&document.exitFullscreen)document.exitFullscreen();
  else if(document.webkitFullscreenElement&&document.webkitExitFullscreen)document.webkitExitFullscreen();}}
document.getElementById('fsbtn').onclick=()=>setFS(true);
document.getElementById('fsexit').onclick=()=>setFS(false);
['fullscreenchange','webkitfullscreenchange'].forEach(ev=>document.addEventListener(ev,()=>{
 if(!(document.fullscreenElement||document.webkitFullscreenElement))document.body.classList.remove('fs');}));
go(0);
"""
    secs = []

    # cover
    secs.append(f"""
<section class="pg" style="--bg:{BG['cover']}"><div class="card">
  <div class="cover-ttl"><div class="t1">I Can <span>Save</span> My Answer!</div>
  <div class="t2">&#9733; Owen's superpower story &#9733;</div></div>
  <div class="art">{scene_cover()}</div>
</div></section>""")

    # story pages
    for key, fn, text in PAGES:
        secs.append(f"""
<section class="pg" style="--bg:{BG[key]}"><div class="card">
  <div class="art">{fn()}</div>
  <div class="band">{text}</div>
</div></section>""")

    # parent page
    tips = "".join(
        f'<div class="tip"><div class="n">{i+1}</div><div><b>{t}</b>&nbsp;&mdash;&nbsp;{d}</div></div>'
        for i, (t, d) in enumerate(PARENT_TIPS))
    secs.append(f"""
<section class="pg" style="--bg:{BG['p11']}"><div class="card"><div class="parent">
  <h2>給爸爸媽媽的使用說明</h2>
  <div class="sub">這是一本社會故事（Social Story）。它的目標不是「講道理」，而是替 Owen 安裝一套<b>當下用得出來的動作腳本</b>。</div>
  {tips}
  <div class="cue">口訣（全書通關密語）：<b>Hand up &rarr; Wait &rarr; Save it!</b>&nbsp;
  當他哪天主動說出 &ldquo;My mouth feels itchy&rdquo;（我察覺到衝動了），就是最值得大力稱讚的時刻。</div>
</div></div></section>""")

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>{BOOK_TITLE_EN} · Owen's Library</title>
<meta name="robots" content="noindex">
<style>{css}</style></head><body>
<header><a href="../../index.html">&larr; 書架 Bookshelf</a><div class="ttl">{BOOK_TITLE_EN}</div>
<button id="fsbtn" aria-label="全螢幕"><svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 6V2h4M10 2h4v4M14 10v4h-4M6 14H2v-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span>全螢幕</span></button></header>
<div id="stage">{''.join(secs)}</div>
<button id="fsexit" aria-label="離開全螢幕"><svg width="13" height="13" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>離開全螢幕</button>
<button id="prev" aria-label="previous page">&#8249;</button><button id="next" aria-label="next page">&#8250;</button><div id="cnt"></div>
<script>{js}</script></body></html>"""

# ---------------------------------------------------------------- library page
def library_html():
    css = f"""
@font-face {{ font-family:'Huninn'; src:url('assets/huninn.woff2') format('woff2'); font-display:swap; }}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Huninn',system-ui,sans-serif;background:#FBF4E8;min-height:100vh}}
.wrap{{max-width:980px;margin:0 auto;padding:34px 20px 60px}}
h1{{color:#4A3B32;font-size:clamp(26px,5vw,40px);text-align:center}}
.sub{{color:#8A7460;text-align:center;margin:8px 0 30px;font-size:15px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:22px}}
.book{{background:#fff;border-radius:22px;overflow:hidden;box-shadow:0 8px 26px rgba(74,59,50,.10);
      display:flex;flex-direction:column;text-decoration:none}}
.thumb{{background:{BG['cover']};padding:12px}}
.thumb svg{{width:100%;height:auto;display:block;border-radius:12px}}
.meta{{padding:14px 16px 18px}}
.meta .t{{color:#4A3B32;font-size:19px}}
.meta .z{{color:#8A7460;font-size:14px;margin-top:2px}}
.chips{{display:flex;gap:6px;margin-top:10px;flex-wrap:wrap}}
.chip{{font-size:12px;color:#8A7460;background:#FBF4E8;border-radius:999px;padding:4px 10px}}
.read{{margin-top:12px;display:inline-block;background:#E4574C;color:#fff;border-radius:999px;
      padding:8px 18px;font-size:14px;align-self:flex-start}}
.soon{{border:2px dashed #E5D9C9;border-radius:22px;display:flex;align-items:center;justify-content:center;
      color:#B8A88F;font-size:15px;min-height:220px;background:transparent}}
footer{{text-align:center;color:#B8A88F;font-size:13px;margin-top:40px}}
"""
    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Owen's Little Library · 小小圖書館</title>
<meta name="robots" content="noindex">
<style>{css}</style></head><body><div class="wrap">
<h1>Owen's Little Library</h1>
<div class="sub">&#9733; 專屬 Owen 的繪本書架 &#9733;</div>
<div class="grid">
  <a class="book" href="books/{BOOK_SLUG}/index.html">
    <div class="thumb">{scene_cover()}</div>
    <div class="meta">
      <div class="t">{BOOK_TITLE_EN}</div>
      <div class="z">{BOOK_TITLE_ZH} &mdash; Owen 的超能力故事</div>
      <div class="chips"><span class="chip">Social Story</span><span class="chip">English</span><span class="chip">12 pages</span></div>
      <span class="read">Read &rarr;</span>
    </div>
  </a>
  <div class="soon">更多繪本製作中&hellip;</div>
</div>
<footer>made with &hearts; by Daddy &amp; Claude</footer>
</div></body></html>"""

# ---------------------------------------------------------------- README
README = """# Owen's Little Library

專屬 Owen 的繪本書架（GitHub Pages 靜態站）。

## 部署
1. 建一個 repo（例如 `owen-books`），把本資料夾內容推上 `main`。
2. Repo Settings → Pages → Source: Deploy from a branch → `main` / `(root)` → Save。
3. 網址：`https://<username>.github.io/owen-books/`

## 新增一本書
1. 複製 `books/save-my-answer/` 成新資料夾（一本書 = 一個自包含的 index.html）。
2. 在根目錄 `index.html` 的 `.grid` 內加一張書卡。
3. 若新書用到新的中文字，重新子集化 `assets/huninn.woff2`（fonttools pyftsubset）。

> 注意：GitHub Pages 免費方案為公開網站。本站已加 `noindex`（不進搜尋引擎），但知道網址的人都能開啟。
"""

# ---------------------------------------------------------------- build
if __name__ == "__main__":
    reader = reader_html()
    lib = library_html()
    with open(f"{SITE}/books/{BOOK_SLUG}/index.html", "w", encoding="utf-8") as f:
        f.write(reader)
    with open(f"{SITE}/index.html", "w", encoding="utf-8") as f:
        f.write(lib)
    with open(f"{SITE}/README.md", "w", encoding="utf-8") as f:
        f.write(README)

    # font subset: every unique char used across the site (incl. unescaped entities)
    chars = set(html.unescape(reader) + html.unescape(lib) + README)
    chars |= set("0123456789/ ")
    text = "".join(sorted(c for c in chars if ord(c) >= 32))
    with open("subset_chars.txt", "w", encoding="utf-8") as f:
        f.write(text)
    subprocess.run(["pyftsubset", os.path.abspath(os.environ.get("HUNINN_TTF", "../assets/fonts/jf-openhuninn-2.0.ttf")),
                    "--text-file=subset_chars.txt",
                    f"--output-file={SITE}/assets/huninn.woff2",
                    "--flavor=woff2"], check=True)
    print("site built:", sum(len(files) for _, _, files in os.walk(SITE)), "files")
