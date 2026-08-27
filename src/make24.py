# -*- coding: utf-8 -*-
"""湊 24 對戰——頁面組裝（site/games/make-24/）。
規格 v1.3：分割旋轉畫面（§6）、操作層/數學層文案（D-4）、題庫內嵌（§8.1 產物）。"""

import json
from make24_deals import build_deals, verify
from make24_js import GAME_JS

STYLE = """
@font-face { font-family:'Huninn'; src:url('../../assets/huninn.woff2') format('woff2'); font-display:swap; }
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;user-select:none;-webkit-user-select:none}
html,body{height:100%;overflow:hidden}
body{font-family:'Huninn',system-ui,sans-serif;background:#2E2A3A;color:#4A3B32}
#app{height:100dvh;display:flex;flex-direction:column}
.half{flex:1;min-height:0;display:flex}
.half.top .panel{transform:rotate(180deg)}
.panel{flex:1;display:flex;flex-direction:column;background:#FBF4E8;padding:8px 12px;min-height:0}
.half.top .panel{background:#EEF4FB}

/* 中央帶（雙向可讀） */
#mid{background:#2E2A3A;color:#FFF;display:flex;align-items:center;justify-content:space-between;
  padding:4px 14px;min-height:56px;gap:8px}
.midcell{display:flex;flex-direction:column;align-items:center;min-width:86px}
.midcell.rot{transform:rotate(180deg)}
.m-main{font-size:24px;line-height:1.1}
.m-sub{font-size:10px;color:#B8AECF;letter-spacing:.5px}
.lights{display:flex;gap:4px;align-items:center}
.lights.rot{transform:rotate(180deg)}
.lt{width:18px;height:18px;border-radius:50%;border:2px solid #6B6383;display:flex;align-items:center;
  justify-content:center;font-size:9px;color:#fff}
.lt.wA{background:#E4574C;border-color:#E4574C}
.lt.wB{background:#3D7BC4;border-color:#3D7BC4}
.lt.none{border-style:dashed}
#gear{background:none;border:none;color:#6B6383;font-size:18px;cursor:pointer}

/* 面板內部 */
.pname{font-size:12px;color:#8A7460;text-align:center}
.pstatus{text-align:center;font-size:15px;min-height:22px}
.pstatus.go{color:#43A047}
.pstatus.dim{color:#B8A88F}
.pstatus.warn{color:#E08A00}
.hintline{text-align:center;font-size:16px;color:#3D7BC4;min-height:20px}
.cards{flex:1;display:flex;align-items:center;justify-content:center;gap:12px;min-height:0}
button{font-family:inherit;border:none;cursor:pointer}
.tile{width:72px;height:100px;border-radius:14px;background:#FFF;color:#4A3B32;font-size:34px;
  box-shadow:0 4px 12px rgba(0,0,0,.15);border:3px solid transparent;transition:transform .12s,opacity .12s}
.tile:disabled{opacity:.4;cursor:default}
.tile.sel{border-color:#F0B429;transform:scale(1.06)}
.tile.hl{border-color:#43A047;box-shadow:0 0 14px rgba(67,160,71,.6)}
.tile.fresh{animation:pop .24s}
@keyframes pop{from{transform:scale(.6)}to{transform:scale(1)}}
.oprow{display:flex;justify-content:center;gap:20px;margin:6px 0}
.op{width:64px;height:64px;border-radius:50%;background:#FFE9A8;font-size:26px;color:#4A3B32}
.op:disabled{opacity:.35}
.op.sel{background:#F0B429;color:#FFF}
.ctrl{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:2px 4px 6px}
.small{width:64px;height:64px;border-radius:50%;background:#EFE4D4;font-size:20px;color:#8A7460;
  display:flex;flex-direction:column;align-items:center;justify-content:center;line-height:1}
.small span{font-size:9px;margin-top:2px}
.small:disabled{opacity:.35}
.buzz{flex:1;max-width:230px;height:72px;border-radius:999px;background:#E4574C;color:#FFF;font-size:22px;
  box-shadow:0 6px 16px rgba(228,87,76,.4)}
.buzz:disabled{background:#C9BFB2;box-shadow:none}
.leftcnt{font-size:11px;color:#B8A88F;text-align:center;min-height:14px}
.flash{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:44px;
  color:#43A047;pointer-events:none;opacity:0;transition:opacity .2s;text-shadow:0 2px 8px rgba(255,255,255,.8)}
.flash.show{opacity:1}
.panelwrap{position:relative;flex:1;display:flex;min-height:0}

/* 開場與結算 overlay */
#overlay,#endpanel{position:fixed;inset:0;background:rgba(46,42,58,.92);display:flex;flex-direction:column;
  align-items:center;justify-content:center;gap:14px;z-index:10;color:#FFF;text-align:center}
#endpanel{display:none}
#overlay h1{font-size:34px}
#overlay p,#endpanel p{color:#B8AECF;font-size:14px;max-width:420px;line-height:1.6}
.bigbtn{background:#E4574C;color:#FFF;font-size:22px;border-radius:999px;padding:16px 44px;
  box-shadow:0 6px 20px rgba(228,87,76,.5)}
#end-title{font-size:32px}
#end-score{font-size:44px}
#end-bar{font-size:18px;letter-spacing:2px}
#end-notes{font-size:14px;color:#B8AECF;line-height:1.8}

@media (max-width:760px){
  .tile{width:56px;height:78px;font-size:26px}
  .op,.small{width:52px;height:52px}
  .buzz{height:60px;font-size:18px}
}
@media (prefers-reduced-motion: reduce){
  *{transition:none !important;animation:none !important}
}
"""


def _panel(side):
    ops = "".join(
        f'<button class="op" id="op-{ord(op)}-{side}">{sym}</button>'
        for op, sym in [("+", "+"), ("-", "&minus;"), ("*", "&times;"), ("/", "&divide;")])
    return f"""
<div class="panelwrap"><div class="flash" id="flash-{side}"></div>
<div class="panel">
  <div class="pname" id="name-{side}">PLAYER {side}</div>
  <div class="pstatus" id="status-{side}"></div>
  <div class="hintline" id="hintline-{side}"></div>
  <div class="cards" id="cards-{side}"></div>
  <div class="leftcnt" id="left-{side}"></div>
  <div class="oprow">{ops}</div>
  <div class="ctrl">
    <button class="small" id="hint-{side}">💡<span>HINT</span></button>
    <button class="buzz" id="buzz-{side}" disabled>⚡ I KNOW!</button>
    <button class="small" id="undo-{side}">↩<span>UNDO</span></button>
    <button class="small" id="reset-{side}">⟳<span>RESET</span></button>
  </div>
</div></div>"""


def make24_html():
    deals = build_deals()
    verify(deals)
    js = GAME_JS.replace("__DEALS__", json.dumps(deals, separators=(",", ":")))
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,user-scalable=no">
<title>Make 24 Battle</title>
<meta name="robots" content="noindex">
<style>{STYLE}</style></head><body>
<div id="app">
  <div class="half top">{_panel("B")}</div>
  <div id="mid">
    <div class="midcell rot"><div class="m-main" id="m-main-b"></div><div class="m-sub" id="m-sub-b"></div></div>
    <div class="lights rot" id="lights-b"></div>
    <button id="gear" aria-label="settings">⚙</button>
    <div class="lights" id="lights-a"></div>
    <div class="midcell"><div class="m-main" id="m-main-a"></div><div class="m-sub" id="m-sub-a"></div></div>
  </div>
  <div class="half bottom">{_panel("A")}</div>
</div>

<div id="overlay">
  <h1>&#9889; MAKE 24</h1>
  <p>Four cards. Use + &minus; &times; &divide; to make 24.<br>
  First to 4 round wins takes the match!<br>
  Put the tablet flat between you &mdash; top player sees it right-side up.</p>
  <button class="bigbtn" id="start-btn">&#9654; START</button>
</div>

<div id="endpanel">
  <div id="end-title"></div>
  <div id="end-score"></div>
  <div id="end-bar"></div>
  <div id="end-notes"></div>
  <button class="bigbtn" id="again-btn">PLAY AGAIN</button>
  <p><a href="../" style="color:#B8AECF">&larr; GAMES</a></p>
</div>
<script>{js}</script></body></html>"""
