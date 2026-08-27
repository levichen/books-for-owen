# -*- coding: utf-8 -*-
"""遊戲區（site/games/）：遊戲大廳＋各遊戲頁。
每個遊戲＝一個自包含 HTML（site/games/<name>/index.html），未來遊戲往 GAMES 清單加。

第一個遊戲 word-match：生字翻牌配對——資料來自 20 本書的 vocab（word＋書中例句），
翻開卡片用 Web Speech API 唸出英文字，配對成功顯示例句。
"""

import json

GAMES = [
    {
        "slug": "word-match",
        "emoji": "&#127183;",
        "name": "生字翻翻樂",
        "desc": "翻牌找出兩張一樣的生字，翻開會唸給你聽！",
    },
    {
        "slug": "make-24",
        "emoji": "&#9889;",
        "name": "Make 24 對戰",
        "desc": "一台平板、兩個人、四張牌——用加減乘除湊出 24，七戰四勝！",
    },
]

LOBBY_STYLE = """
@font-face { font-family:'Huninn'; src:url('../assets/huninn.woff2') format('woff2'); font-display:swap; }
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Huninn',system-ui,sans-serif;background:#FBF4E8;min-height:100vh;color:#4A3B32}
.wrap{max-width:760px;margin:0 auto;padding:26px 16px 60px}
h1{font-size:clamp(24px,5vw,34px);text-align:center}
.sub{color:#8A7460;text-align:center;margin:6px 0 24px;font-size:14px}
.gcard{display:block;background:#fff;border-radius:22px;box-shadow:0 8px 26px rgba(74,59,50,.10);
  padding:20px 22px;margin-bottom:16px;text-decoration:none;color:#4A3B32}
.gcard .t{font-size:20px}
.gcard .d{display:block;font-size:14px;color:#8A7460;margin-top:6px}
.gcard .go{float:right;color:#B8A88F;font-size:14px;margin-top:4px}
.soon{border:2px dashed #E5D9C9;border-radius:22px;text-align:center;color:#B8A88F;
  font-size:15px;padding:26px;background:transparent}
footer{text-align:center;color:#B8A88F;font-size:13px;margin-top:30px}
"""


def games_index_html():
    cards = "".join(
        f'<a class="gcard" href="{g["slug"]}/"><span class="go">開始玩 &rarr;</span>'
        f'<div class="t">{g["emoji"]} {g["name"]}</div>'
        f'<span class="d">{g["desc"]}</span></a>'
        for g in GAMES)
    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Owen 的遊戲間</title>
<meta name="robots" content="noindex">
<style>{LOBBY_STYLE}</style></head><body><div class="wrap">
<h1>&#127918; Owen 的遊戲間</h1>
<div class="sub">玩遊戲也在學習 &#11088;</div>
{cards}
<div class="soon">更多遊戲製作中&hellip;</div>
<footer>made with &hearts; by Daddy &amp; Claude</footer>
</div></body></html>"""


# ---------------------------------------------------------------- word-match
WM_STYLE = """
@font-face { font-family:'Huninn'; src:url('../../assets/huninn.woff2') format('woff2'); font-display:swap; }
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent}
body{font-family:'Huninn',system-ui,sans-serif;background:#FBF4E8;min-height:100vh;color:#4A3B32}
.wrap{max-width:640px;margin:0 auto;padding:22px 14px 50px}
h1{font-size:clamp(22px,5vw,30px);text-align:center}
.sub{color:#8A7460;text-align:center;margin:6px 0 14px;font-size:13px}
.hud{display:flex;justify-content:center;gap:10px;margin-bottom:14px;flex-wrap:wrap}
.hud span{font-size:13px;color:#8A7460;background:#fff;border-radius:999px;padding:6px 14px;box-shadow:0 2px 8px rgba(74,59,50,.08)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.tile{aspect-ratio:4/3;border-radius:16px;border:none;cursor:pointer;font-family:inherit;
  display:flex;align-items:center;justify-content:center;font-size:clamp(15px,4.5vw,22px);
  background:#E4574C;color:#fff;box-shadow:0 6px 14px rgba(74,59,50,.15);transition:transform .12s}
.tile:active{transform:scale(.96)}
.tile.open{background:#fff;color:#4A3B32;border:3px solid #F0B429}
.tile.done{background:#7BC47F;color:#fff;border:none;box-shadow:none}
.tile .back{font-size:26px}
.sentence{min-height:44px;text-align:center;color:#8A7460;font-size:14px;line-height:1.5;
  background:#fff;border-radius:14px;padding:10px 14px;margin-top:14px}
.sentence b{color:#E4574C}
.win{display:none;text-align:center;background:#fff;border-radius:20px;padding:22px;margin-top:16px;
  box-shadow:0 8px 26px rgba(74,59,50,.12)}
.win .big{font-size:24px}
.win .stat{color:#8A7460;font-size:14px;margin-top:8px}
button.again{font-family:inherit;border:none;cursor:pointer;background:#E4574C;color:#fff;
  border-radius:999px;padding:12px 28px;font-size:16px;margin-top:14px}
footer{text-align:center;color:#B8A88F;font-size:12px;margin-top:26px}
"""

WM_SCRIPT = """
'use strict';
const VOCAB = __VOCAB__;  // [{w:生字, s:例句}]
const PAIRS = 6;
let deck = [], open = [], lock = false, matched = 0, moves = 0, t0 = null, timerId = null;

function speak(word) {
  try {
    const u = new SpeechSynthesisUtterance(word);
    u.lang = 'en-US'; u.rate = 0.85;
    speechSynthesis.cancel();
    speechSynthesis.speak(u);
  } catch (e) {}
}
function shuffle(a) {
  const r = a.slice();
  for (let i = r.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const t = r[i]; r[i] = r[j]; r[j] = t;
  }
  return r;
}
function newGame() {
  const pick = shuffle(VOCAB).slice(0, PAIRS);
  deck = shuffle(pick.concat(pick).map((v, i) => ({ key: v.w, s: v.s, id: i })));
  open = []; lock = false; matched = 0; moves = 0; t0 = null;
  if (timerId) { clearInterval(timerId); timerId = null; }
  document.getElementById('time').textContent = '0 秒';
  document.getElementById('moves').textContent = '0 步';
  document.getElementById('win').style.display = 'none';
  document.getElementById('sentence').innerHTML = '點卡片翻開，找出兩張一樣的生字！';
  const grid = document.getElementById('grid');
  grid.innerHTML = deck.map((c, i) =>
    '<button class="tile" data-i="' + i + '"><span class="back">&#11088;</span></button>').join('');
}
function tick() {
  document.getElementById('time').textContent = Math.round((Date.now() - t0) / 1000) + ' 秒';
}
function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
function flip(i, el) {
  if (lock || el.classList.contains('open') || el.classList.contains('done')) return;
  if (!t0) { t0 = Date.now(); timerId = setInterval(tick, 1000); }
  el.classList.add('open');
  el.innerHTML = esc(deck[i].key);
  speak(deck[i].key);
  open.push({ i, el });
  if (open.length < 2) return;
  moves++;
  document.getElementById('moves').textContent = moves + ' 步';
  const [a, b] = open;
  if (deck[a.i].key === deck[b.i].key) {
    a.el.classList.remove('open'); b.el.classList.remove('open');
    a.el.classList.add('done'); b.el.classList.add('done');
    matched++;
    document.getElementById('sentence').innerHTML =
      '&#11088; <b>' + esc(deck[a.i].key) + '</b>&nbsp;&mdash;&nbsp;' + esc(deck[a.i].s);
    open = [];
    if (matched === PAIRS) finish();
  } else {
    lock = true;
    setTimeout(() => {
      a.el.classList.remove('open'); b.el.classList.remove('open');
      a.el.innerHTML = '<span class="back">&#11088;</span>';
      b.el.innerHTML = '<span class="back">&#11088;</span>';
      open = []; lock = false;
    }, 900);
  }
}
function finish() {
  clearInterval(timerId); timerId = null;
  const secs = Math.round((Date.now() - t0) / 1000);
  document.getElementById('win-stat').textContent = '用了 ' + secs + ' 秒、' + moves + ' 步';
  document.getElementById('win').style.display = 'block';
}
document.getElementById('grid').addEventListener('click', ev => {
  const el = ev.target.closest('.tile');
  if (!el) return;
  flip(+el.dataset.i, el);
});
document.getElementById('again').addEventListener('click', newGame);
newGame();
"""


def word_match_html(vocab):
    """vocab: [{"w": word, "s": sentence}]"""
    script = WM_SCRIPT.replace("__VOCAB__", json.dumps(vocab, ensure_ascii=False))
    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>生字翻翻樂</title>
<meta name="robots" content="noindex">
<style>{WM_STYLE}</style></head><body><div class="wrap">
<h1>&#127183; 生字翻翻樂</h1>
<div class="sub">翻牌找出兩張一樣的生字——翻開會唸給你聽 &#128264;</div>
<div class="hud"><span id="time">0 秒</span><span id="moves">0 步</span></div>
<div class="grid" id="grid"></div>
<div class="sentence" id="sentence"></div>
<div class="win" id="win">
  <div class="big">&#127881; 全部配對成功！</div>
  <div class="stat" id="win-stat"></div>
  <button class="again" id="again">再玩一次</button>
</div>
<footer>made with &hearts; by Daddy &amp; Claude</footer>
</div><script>{script}</script></body></html>"""
