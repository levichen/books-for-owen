# -*- coding: utf-8 -*-
"""閱讀紀錄頁（site/reading-log/）：記錄 Owen 每天讀了什麼書（含外部書籍）。

純前端＋localStorage：資料存在瀏覽器本機，無後端。
UI 靜態文字走 Huninn 子集字型；使用者輸入的書名為任意字元，自動 fallback 到系統字型。
"""

GOAL = 100  # 累積讀滿 100 本換禮物

STYLE = """
@font-face { font-family:'Huninn'; src:url('../assets/huninn.woff2') format('woff2'); font-display:swap; }
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Huninn',system-ui,sans-serif;background:#FBF4E8;min-height:100vh;color:#4A3B32}
.wrap{max-width:760px;margin:0 auto;padding:26px 16px 60px}
h1{font-size:clamp(24px,5vw,34px);text-align:center}
.sub{color:#8A7460;text-align:center;margin:6px 0 20px;font-size:14px}
.back{display:inline-block;color:#8A7460;text-decoration:none;font-size:14px;margin-bottom:6px}
.card{background:#fff;border-radius:22px;box-shadow:0 8px 26px rgba(74,59,50,.10);padding:18px;margin-bottom:18px}

/* --- 進度區：甜甜圈 + 大數字 --- */
.progress{display:flex;align-items:center;gap:18px;flex-wrap:wrap;justify-content:center}
.donut{position:relative;width:170px;height:170px;flex:0 0 auto}
.donut svg{width:100%;height:100%;transform:rotate(-90deg)}
.donut .center{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.donut .num{font-size:38px;line-height:1}
.donut .pct{font-size:13px;color:#8A7460;margin-top:4px}
.gift{flex:1 1 220px;min-width:220px}
.gift .big{font-size:19px}
.gift .left{color:#8A7460;font-size:14px;margin-top:6px}
.gift .done{color:#E4574C;font-size:17px;margin-top:6px}
.milestones{display:flex;gap:6px;margin-top:12px;flex-wrap:wrap}
.mile{font-size:12px;color:#8A7460;background:#FBF4E8;border-radius:999px;padding:4px 10px}
.mile.hit{background:#E4574C;color:#fff}

/* --- 新增表單 --- */
.form-row{display:flex;gap:8px;flex-wrap:wrap}
input[type=date],input[type=text]{font-family:inherit;font-size:15px;color:#4A3B32;
  border:2px solid #E5D9C9;border-radius:12px;padding:10px 12px;background:#FFFDF8;outline:none}
input:focus{border-color:#E4574C}
input[type=date]{flex:0 0 auto}
input[type=text]{flex:1 1 180px;min-width:0}
button{font-family:inherit;font-size:15px;border:none;border-radius:999px;cursor:pointer}
.add-btn{background:#E4574C;color:#fff;padding:10px 22px}
.add-btn:active{transform:scale(.97)}
.hint{color:#B8A88F;font-size:12px;margin-top:8px}
.err{color:#E4574C;font-size:13px;margin-top:8px;display:none}

/* --- 行事曆 --- */
.cal-head{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.cal-head .m{font-size:18px}
.nav-btn{background:#FBF4E8;color:#4A3B32;width:36px;height:36px;border-radius:50%;font-size:16px}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:4px}
.dow{text-align:center;color:#B8A88F;font-size:12px;padding:4px 0}
.day{position:relative;aspect-ratio:1;border-radius:10px;background:#FFFDF8;border:2px solid transparent;
  display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;font-size:14px}
.day.blank{background:transparent;cursor:default}
.day.today{border-color:#F0B429}
.day.sel{border-color:#E4574C}
.day .cnt{position:absolute;right:3px;top:3px;background:#E4574C;color:#fff;font-size:10px;
  min-width:16px;height:16px;border-radius:999px;display:flex;align-items:center;justify-content:center;padding:0 3px}
.day.has{background:#FDEAE0}

/* --- 當日清單 --- */
.day-title{font-size:15px;margin-bottom:8px}
.entry{display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px dashed #EFE4D4}
.entry:last-child{border-bottom:none}
.entry .bk{flex:1;font-size:15px;word-break:break-all}
.del{background:#FBF4E8;color:#8A7460;padding:6px 12px;font-size:13px}
.empty{color:#B8A88F;font-size:14px}
footer{text-align:center;color:#B8A88F;font-size:13px;margin-top:30px}
"""

SCRIPT = """
'use strict';
const KEY = 'owen-reading-log-v1';
const GOAL = __GOAL__;

/* ---------- 資料層（不可變更新；localStorage 讀寫都包 try/catch） ---------- */
function loadEntries() {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return [];
    const arr = JSON.parse(raw);
    if (!Array.isArray(arr)) return [];
    return arr.filter(e => e && typeof e.date === 'string' && typeof e.title === 'string' && e.id);
  } catch (err) { console.error('read log failed', err); return []; }
}
function saveEntries(entries) {
  try { localStorage.setItem(KEY, JSON.stringify(entries)); return true; }
  catch (err) { console.error('save log failed', err); showError('存檔失敗：瀏覽器儲存空間不可用'); return false; }
}
function addEntry(entries, date, title) {
  const id = Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
  return entries.concat([{ id, date, title }]);
}
function removeEntry(entries, id) { return entries.filter(e => e.id !== id); }

/* ---------- 狀態 ---------- */
let entries = loadEntries();
const todayStr = localDateStr(new Date());
let view = { y: +todayStr.slice(0, 4), m: +todayStr.slice(5, 7) - 1 };  // 行事曆顯示的年月
let selected = todayStr;                                                // 目前選取的日期

function localDateStr(d) {
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}
function byDate(date) { return entries.filter(e => e.date === date); }

/* ---------- 進度（甜甜圈 + 換禮物） ---------- */
function renderProgress() {
  const total = entries.length;
  const pct = Math.min(100, Math.round(total / GOAL * 100));
  const C = 2 * Math.PI * 70;  // r=70 圓周
  const arc = document.getElementById('arc');
  arc.setAttribute('stroke-dasharray', (pct / 100 * C) + ' ' + C);
  arc.style.display = pct === 0 ? 'none' : '';  // 0% 時隱藏，避免 round linecap 殘留一顆圓點
  document.getElementById('total').textContent = total;
  document.getElementById('pct').textContent = pct + '%';
  const gift = document.getElementById('gift-msg');
  if (total >= GOAL) {
    gift.innerHTML = '<div class="done">&#127873; 達成 ' + GOAL + ' 本！可以換禮物啦！</div>';
  } else {
    gift.innerHTML = '<div class="left">再讀 <b>' + (GOAL - total) + '</b> 本就能換禮物 &#127873;</div>';
  }
  const miles = [25, 50, 75, 100];
  document.getElementById('miles').innerHTML = miles.map(m =>
    '<span class="mile' + (total >= m ? ' hit' : '') + '">' + m + ' 本</span>').join('');
}

/* ---------- 行事曆 ---------- */
function renderCalendar() {
  const { y, m } = view;
  document.getElementById('cal-month').textContent = y + ' 年 ' + (m + 1) + ' 月';
  const first = new Date(y, m, 1).getDay();
  const days = new Date(y, m + 1, 0).getDate();
  const cells = [];
  for (let i = 0; i < first; i++) cells.push('<div class="day blank"></div>');
  for (let d = 1; d <= days; d++) {
    const ds = y + '-' + String(m + 1).padStart(2, '0') + '-' + String(d).padStart(2, '0');
    const n = byDate(ds).length;
    const cls = ['day', n ? 'has' : '', ds === todayStr ? 'today' : '', ds === selected ? 'sel' : ''].filter(Boolean).join(' ');
    cells.push('<div class="' + cls + '" data-date="' + ds + '">' + d + (n ? '<span class="cnt">' + n + '</span>' : '') + '</div>');
  }
  document.getElementById('cal-grid').innerHTML =
    ['日','一','二','三','四','五','六'].map(w => '<div class="dow">' + w + '</div>').join('') + cells.join('');
}

/* ---------- 當日清單 ---------- */
function esc(s) { const d = document.createElement('div'); d.textContent = s; return d.innerHTML; }
function renderDay() {
  document.getElementById('day-title').textContent = selected + ' 讀了什麼';
  const list = byDate(selected);
  const box = document.getElementById('day-list');
  if (!list.length) { box.innerHTML = '<div class="empty">這天還沒有紀錄</div>'; return; }
  box.innerHTML = list.map(e =>
    '<div class="entry"><span class="bk">&#128214; ' + esc(e.title) + '</span>' +
    '<button class="del" data-id="' + e.id + '">刪除</button></div>').join('');
}

function renderAll() { renderProgress(); renderCalendar(); renderDay(); }
function showError(msg) { const el = document.getElementById('err'); el.textContent = msg; el.style.display = 'block'; }
function clearError() { document.getElementById('err').style.display = 'none'; }

/* ---------- 事件 ---------- */
document.getElementById('add-form').addEventListener('submit', ev => {
  ev.preventDefault(); clearError();
  const date = document.getElementById('in-date').value;
  const title = document.getElementById('in-title').value.trim();
  if (!date) { showError('請選擇日期'); return; }
  if (!title) { showError('請填書名'); return; }
  if (title.length > 100) { showError('書名太長（100 字內）'); return; }
  const next = addEntry(entries, date, title);
  if (!saveEntries(next)) return;
  entries = next;
  selected = date;
  view = { y: +date.slice(0, 4), m: +date.slice(5, 7) - 1 };
  document.getElementById('in-title').value = '';
  renderAll();
});
document.getElementById('cal-grid').addEventListener('click', ev => {
  const cell = ev.target.closest('.day');
  if (!cell || !cell.dataset.date) return;
  selected = cell.dataset.date;
  renderCalendar(); renderDay();
});
document.getElementById('day-list').addEventListener('click', ev => {
  const btn = ev.target.closest('.del');
  if (!btn) return;
  const next = removeEntry(entries, btn.dataset.id);
  if (!saveEntries(next)) return;
  entries = next;
  renderAll();
});
document.getElementById('prev-m').addEventListener('click', () => {
  view = view.m === 0 ? { y: view.y - 1, m: 11 } : { y: view.y, m: view.m - 1 };
  renderCalendar();
});
document.getElementById('next-m').addEventListener('click', () => {
  view = view.m === 11 ? { y: view.y + 1, m: 0 } : { y: view.y, m: view.m + 1 };
  renderCalendar();
});

document.getElementById('in-date').value = todayStr;
renderAll();
"""


def reading_log_html():
    script = SCRIPT.replace("__GOAL__", str(GOAL))
    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Owen 的閱讀紀錄</title>
<meta name="robots" content="noindex">
<style>{STYLE}</style></head><body><div class="wrap">
<a class="back" href="../">&larr; 回書架</a>
<h1>&#128214; Owen 的閱讀紀錄</h1>
<div class="sub">每天讀的書都記下來，累積 {GOAL} 本換禮物 &#127873;</div>

<div class="card">
  <div class="progress">
    <div class="donut">
      <svg viewBox="0 0 170 170">
        <circle cx="85" cy="85" r="70" fill="none" stroke="#F0E4D3" stroke-width="18"/>
        <circle id="arc" cx="85" cy="85" r="70" fill="none" stroke="#E4574C" stroke-width="18"
                stroke-linecap="round" stroke-dasharray="0 440"/>
      </svg>
      <div class="center"><div class="num"><span id="total">0</span></div><div class="pct"><span id="pct">0%</span> / {GOAL} 本</div></div>
    </div>
    <div class="gift">
      <div class="big">禮物進度</div>
      <div id="gift-msg"></div>
      <div class="milestones" id="miles"></div>
    </div>
  </div>
</div>

<div class="card">
  <form id="add-form" class="form-row">
    <input type="date" id="in-date" required>
    <input type="text" id="in-title" placeholder="今天讀了哪本書？" maxlength="100" required>
    <button type="submit" class="add-btn">新增</button>
  </form>
  <div class="err" id="err"></div>
  <div class="hint">書架上的書、學校的書、圖書館借的書都可以記；一天可以記很多本。紀錄存在這台裝置的瀏覽器裡。</div>
</div>

<div class="card">
  <div class="cal-head">
    <button class="nav-btn" id="prev-m">&#8249;</button>
    <div class="m" id="cal-month"></div>
    <button class="nav-btn" id="next-m">&#8250;</button>
  </div>
  <div class="cal" id="cal-grid"></div>
</div>

<div class="card">
  <div class="day-title" id="day-title"></div>
  <div id="day-list"></div>
</div>

<footer>made with &hearts; by Daddy &amp; Claude</footer>
</div><script>{script}</script></body></html>"""
