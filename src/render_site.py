# -*- coding: utf-8 -*-
"""Build the GitHub Pages static site: Owen's little library + 每本書的互動 reader。
單一內容源（book_<slug>.py 的 BOOK dict）→ web 渲染；書籍清單由 books_all 自動發現。"""
import os
import subprocess
import html
from book_common import TXT, vocab_sentence
from books_all import load_books
import json
from reading_log import reading_log_html, write_zhuyin_asset, BOPO_CHARS, API_URL
from drink_log import drink_log_html
from jump_log import jump_log_html

SITE = "../site"


# ---------------------------------------------------------------- reader page
def reader_html(book):
    bg = book["bg"]
    title_en = f"{book['title_pre']}{book['title_hi']}{book['title_post']}"
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
.vocab{{background:#fff;border-radius:18px;padding:18px 22px}}
.vocab h2{{font-size:22px;color:{TXT};text-align:center;margin-bottom:14px}}
.vrow{{display:flex;align-items:center;gap:16px;background:#FBF4E8;border-radius:14px;padding:12px 16px;margin-bottom:10px}}
.vw{{min-width:160px;font-size:28px;color:#E4574C}}
.vs{{font-size:16.5px;color:{TXT};line-height:1.5}}
.vs b{{color:#E4574C}}
.vfoot{{text-align:center;color:#8A7460;margin-top:12px;font-size:15px}}
button{{border:none;cursor:pointer;font-family:inherit}}
#donebtn{{display:block;margin:12px auto 0;background:#E4574C;color:#fff;font-size:clamp(16px,2.5vw,21px);
        border-radius:999px;padding:12px 30px;box-shadow:0 6px 16px rgba(228,87,76,.35)}}
#donebtn:disabled{{opacity:.6;cursor:wait}}
#donebtn.ok{{background:#7BC47F;box-shadow:0 6px 16px rgba(123,196,127,.35)}}
#donemsg{{text-align:center;color:#8A7460;font-size:14px;margin-top:8px;min-height:20px}}
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
// 「我讀完了！」→ 記進雲端閱讀紀錄（同一本同一天只記一次，先查雲端再寫，跨裝置也不重複）
const doneBtn=document.getElementById('donebtn'),doneMsg=document.getElementById('donemsg');
if(doneBtn)doneBtn.onclick=async()=>{
 doneBtn.disabled=true;doneMsg.textContent='記錄中…';
 const today=(d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0'))(new Date());
 try{
  const list=await (await fetch(LOG_API)).json();
  if(!list.ok)throw new Error('api');
  if(list.entries.some(e=>e.title===BOOK_TITLE&&e.date===today)){
   doneBtn.classList.add('ok');doneBtn.innerHTML='&#11088; 今天記過囉！';
   doneMsg.textContent='這本今天已經在紀錄裡了，明天再讀再記一筆';return;}
  const resp=await (await fetch(LOG_API,{method:'POST',body:JSON.stringify({action:'add',date:today,title:BOOK_TITLE})})).json();
  if(!resp.ok)throw new Error(resp.error||'api');
  doneBtn.classList.add('ok');doneBtn.innerHTML='&#127881; 已記錄！';
  doneMsg.textContent='目前累積 '+resp.entries.length+' 本，繼續加油！';
 }catch(err){console.error(err);doneBtn.disabled=false;doneMsg.textContent='連不上網路，請稍後再按一次（或到閱讀紀錄頁手動記）';}
};
"""
    js = f"const LOG_API={json.dumps(API_URL)};const BOOK_TITLE={json.dumps(title_en)};\n" + js
    secs = []

    # cover
    secs.append(f"""
<section class="pg" style="--bg:{bg['cover']}"><div class="card">
  <div class="cover-ttl"><div class="t1">{book['title_pre']}<span>{book['title_hi']}</span>{book['title_post']}</div>
  <div class="t2">&#9733; {book['subtitle']} &#9733;</div></div>
  <div class="art">{book['cover']()}</div>
</div></section>""")

    # story pages（最後一個故事頁附「我讀完了！」按鈕，記進閱讀紀錄）
    last_key = book["pages"][-1][0]
    for key, fn, text in book["pages"]:
        done = ('<button id="donebtn">&#11088; 我讀完了！</button><div id="donemsg"></div>'
                if key == last_key else "")
        secs.append(f"""
<section class="pg" style="--bg:{bg[key]}"><div class="card">
  <div class="art">{fn()}</div>
  <div class="band">{text}</div>
  {done}
</div></section>""")

    # vocab review page（倒數第二頁：生字複習；零生字書自動略過）
    vocab = book.get("vocab") or []
    if vocab:
        vrows = "".join(
            f'<div class="vrow"><div class="vw">&#9733; {w}</div>'
            f'<div class="vs">{vocab_sentence(book["pages"], w)}</div></div>'
            for w in vocab)
        secs.append(f"""
<section class="pg" style="--bg:{bg['p10']}"><div class="card"><div class="vocab">
  <h2>&#9733; My New Words! &#9733;</h2>
  {vrows}
  <div class="vfoot">Read it. Say it. Use it!</div>
</div></div></section>""")

    # parent page
    tips = "".join(
        f'<div class="tip"><div class="n">{i+1}</div><div><b>{t}</b>&nbsp;&mdash;&nbsp;{d}</div></div>'
        for i, (t, d) in enumerate(book["parent_tips"]))
    secs.append(f"""
<section class="pg" style="--bg:{bg['p11']}"><div class="card"><div class="parent">
  <h2>給爸爸媽媽的使用說明</h2>
  <div class="sub">{book['parent_intro']}</div>
  {tips}
  <div class="cue">{book['cue_html']}</div>
</div></div></section>""")

    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<title>{title_en} · Owen's Library</title>
<meta name="robots" content="noindex">
<style>{css}</style></head><body>
<header><a href="../../index.html">&larr; 書架 Bookshelf</a><div class="ttl">{title_en}</div>
<button id="fsbtn" aria-label="全螢幕"><svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 6V2h4M10 2h4v4M14 10v4h-4M6 14H2v-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg><span>全螢幕</span></button></header>
<div id="stage">{''.join(secs)}</div>
<button id="fsexit" aria-label="離開全螢幕"><svg width="13" height="13" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>離開全螢幕</button>
<footer><button id="prev" aria-label="previous page">&#8249;</button><button id="next" aria-label="next page">&#8250;</button><div id="cnt"></div></footer>
<script>{js}</script></body></html>"""


# ---------------------------------------------------------------- library page
def library_html(books):
    first_bg = books[0]["bg"]["cover"]
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
.thumb{{padding:12px}}
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
.log-link{{display:block;max-width:420px;margin:0 auto 26px;text-align:center;text-decoration:none;
      background:#fff;color:#4A3B32;border-radius:999px;padding:12px 22px;font-size:15px;
      box-shadow:0 6px 18px rgba(74,59,50,.10)}}
.log-link b{{color:#E4574C}}
.log-drink{{margin-top:-14px}}
.log-drink b{{color:#3D7BC4}}
.log-jump{{margin-top:-14px}}
.log-jump b{{color:#43A047}}
footer{{text-align:center;color:#B8A88F;font-size:13px;margin-top:40px}}
"""
    cards = []
    for b in books:
        title_en = f"{b['title_pre']}{b['title_hi']}{b['title_post']}"
        total_pages = 2 + len(b["pages"]) + (1 if b.get("vocab") else 0)
        chips = "".join(
            f'<span class="chip">{(f"{total_pages} pages" if c.endswith("pages") else c)}</span>'
            for c in b["chips"])
        cards.append(f"""
  <a class="book" href="books/{b['slug']}/index.html">
    <div class="thumb" style="background:{b['bg']['cover']}">{b['cover']()}</div>
    <div class="meta">
      <div class="t">{title_en}</div>
      <div class="z">{b['title_zh']} &mdash; {b['tagline_zh']}</div>
      <div class="chips">{chips}</div>
      <span class="read">Read &rarr;</span>
    </div>
  </a>""")

    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Owen's Little Library · 小小圖書館</title>
<meta name="robots" content="noindex">
<style>{css}</style></head><body><div class="wrap">
<h1>Owen's Little Library</h1>
<div class="sub">&#9733; 專屬 Owen 的繪本書架 &#9733;</div>
<a class="log-link" href="reading-log/">&#128214; 閱讀紀錄 &mdash; 每滿 100 本<b>換禮物</b> &#127873;</a>
<a class="log-link log-drink" href="drink-log/">&#129475; 牛奶點數 &mdash; 每滿 100 點<b>換禮物</b> &#127873;</a>
<a class="log-link log-jump" href="jump-log/">&#129336; 跳繩次數 &mdash; 每滿 10,000 次<b>換禮物</b> &#127873;</a>
<div class="grid">{''.join(cards)}
  <div class="soon">更多繪本製作中&hellip;</div>
</div>
<footer>made with &hearts; by Daddy &amp; Claude</footer>
</div></body></html>"""


# ---------------------------------------------------------------- README
README = """# Owen's Little Library

專屬 Owen 的繪本書架（GitHub Pages 靜態站）。本資料夾由 src/render_site.py 產生，勿手改。

> 注意：GitHub Pages 免費方案為公開網站。本站已加 `noindex`（不進搜尋引擎），但知道網址的人都能開啟。
"""

# ---------------------------------------------------------------- build
if __name__ == "__main__":
    books = load_books()
    all_html = []
    for book in books:
        os.makedirs(f"{SITE}/books/{book['slug']}", exist_ok=True)
        reader = reader_html(book)
        with open(f"{SITE}/books/{book['slug']}/index.html", "w", encoding="utf-8") as f:
            f.write(reader)
        all_html.append(reader)

    lib = library_html(books)
    os.makedirs(f"{SITE}/assets", exist_ok=True)
    with open(f"{SITE}/index.html", "w", encoding="utf-8") as f:
        f.write(lib)
    log_page = reading_log_html()
    os.makedirs(f"{SITE}/reading-log", exist_ok=True)
    with open(f"{SITE}/reading-log/index.html", "w", encoding="utf-8") as f:
        f.write(log_page)
    write_zhuyin_asset(f"{SITE}/assets/zhuyin.json")  # 注音字典（存在即跳過）
    drink_page = drink_log_html()
    os.makedirs(f"{SITE}/drink-log", exist_ok=True)
    with open(f"{SITE}/drink-log/index.html", "w", encoding="utf-8") as f:
        f.write(drink_page)
    jump_page = jump_log_html()
    os.makedirs(f"{SITE}/jump-log", exist_ok=True)
    with open(f"{SITE}/jump-log/index.html", "w", encoding="utf-8") as f:
        f.write(jump_page)
    with open(f"{SITE}/README.md", "w", encoding="utf-8") as f:
        f.write(README)

    # font subset: every unique char used across the site (incl. unescaped entities)
    chars = set(html.unescape(lib) + README + html.unescape(log_page)
                + html.unescape(drink_page) + html.unescape(jump_page))
    for r in all_html:
        chars |= set(html.unescape(r))
    chars |= set("0123456789/ ")
    chars |= BOPO_CHARS  # 注音符號（閱讀紀錄書名 ruby 用）
    text = "".join(sorted(c for c in chars if ord(c) >= 32))
    with open("subset_chars.txt", "w", encoding="utf-8") as f:
        f.write(text)
    subprocess.run(["pyftsubset", os.path.abspath(os.environ.get("HUNINN_TTF", "../assets/fonts/jf-openhuninn-2.0.ttf")),
                    "--text-file=subset_chars.txt",
                    f"--output-file={SITE}/assets/huninn.woff2",
                    "--flavor=woff2"], check=True)
    print("site built:", len(books), "books,", sum(len(files) for _, _, files in os.walk(SITE)), "files")
