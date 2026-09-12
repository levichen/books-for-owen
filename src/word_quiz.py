# -*- coding: utf-8 -*-
"""單字小考（site/games/word-quiz/）：每天 10 題，中文選英文＋聽音拼字。

單字來源：試算表 `words` 工作表（欄位 word / zh / unit），透過 Apps Script GET ?mode=words 取得，
本機快取；抓不到或工作表空白時退回內建 SEED_WORDS（學校 Unit 1）。

每日流程三步（同一入口，2026-09-12 由「考試優先」改版）：
  1. 學新字：每天照單元順序介紹 5 個新字（固定，不讓使用者選），卡片＝英文＋中文＋朗讀，按「會了」才算已介紹
  2. 複習不熟：弱字堆＝已介紹且 box 0 的舊字，翻卡＋「再看一次」排回堆尾；上限 10 張
  3. 小考：只考已介紹過的字，優先 答錯過 → 今天新字 → 快會了 → 已經會；10 題（不足則全考）
熟練度（簡化 Leitner）：答對 box+1（最高 2）、答錯回 box 0；字只能靠小考答對離開弱字堆，
卡片上的「會了」不改熟練度（六歲自評不可靠）。
題型：zh→en 四選一（約 4 成）、聽音拼字用字母磚（其餘），不打字、全靠點。
成績 0–100 存今日最佳與歷代最佳（比照 Make It!）。
跨裝置同步（2026-09-12）：熟練度與最佳成績存試算表 kv_words 工作表（通用鍵值 API：GET ?mode=kv&sheet=kv_words、
POST kv_set items:{key:jsonString}）。開頁先讀雲端與本機合併（seen 多者勝、再比 last、同則雲端勝），
本機每次改動進佇列、0.8 秒後合併成一次 POST；離線或後端未更新時佇列保留，回線自動補傳。
"""

import json

from reading_log import API_URL

# 學校單字表（照片轉錄）——試算表沒資料時的備援。Unit 1 兩頁（2026-09-05、09-12）、Unit 2（09-12）
SEED_WORDS = [
    ("family", "家人", "U1"), ("grandmother", "奶奶；外婆", "U1"), ("grandfather", "爺爺；外公", "U1"),
    ("father", "爸爸", "U1"), ("mother", "媽媽", "U1"), ("brother", "哥哥；弟弟", "U1"),
    ("sister", "姊姊；妹妹", "U1"), ("friend", "朋友", "U1"), ("predict", "預料、預測", "U1"),
    ("it has", "它有；牠有", "U1"), ("I have", "我有", "U1"), ("live", "住；居住", "U1"),
    ("families", "家庭（複數）", "U1"), ("each other", "互相", "U1"), ("the same", "相同的", "U1"),
    ("kinds of", "種類", "U1"), ("meet", "認識；遇見", "U1"), ("important", "重要的", "U1"),
    ("together", "一起", "U1"), ("share", "分享", "U1"), ("favorite", "最喜歡的", "U1"),
    ("I", "我", "U1"), ("am", "是（與 I 連用）", "U1"), ("you", "你；你們", "U1"),
    ("we", "我們", "U1"), ("they", "他們", "U1"),
    ("are", "是（與 you, we, they 連用）", "U1"), ("he", "他", "U1"), ("she", "她", "U1"),
    ("it", "它；牠", "U1"), ("is", "是（與 he, she, it 連用）", "U1"),
    ("uncle", "伯父；叔叔；姑丈；姨丈；舅舅", "U1"), ("aunt", "伯母；嬸嬸；姑姑；阿姨；舅媽", "U1"),
    ("daughter", "女兒", "U1"), ("parents", "父母親", "U1"), ("son", "兒子", "U1"),
    ("cousin", "堂（表）兄弟姊妹", "U1"), ("opposite", "相反的", "U1"), ("old", "老的", "U1"),
    ("young", "年輕的", "U1"), ("small", "小的", "U1"), ("big", "大的", "U1"),
    ("cold", "冷的", "U1"), ("hot", "熱的", "U1"),
    ("elephant", "大象", "U2"), ("tortoise", "陸龜", "U2"), ("lonely", "孤獨的", "U2"),
    ("sad", "傷心的", "U2"), ("scared", "驚嚇的、害怕的", "U2"), ("eat", "吃", "U2"),
    ("play", "玩耍", "U2"), ("sleep", "睡覺", "U2"), ("look at", "看", "U2"),
    ("find", "找到", "U2"), ("Let's go", "讓我們一起走", "U2"), ("run away", "逃走、跑走", "U2"),
    ("are scared of", "害怕某物", "U2"), ("this", "這", "U2"), ("that", "那", "U2"),
    ("these", "這些", "U2"), ("those", "那些", "U2"), ("hamster", "倉鼠", "U2"),
    ("goldfish", "金魚", "U2"), ("bird", "小鳥", "U2"), ("rabbit", "兔子", "U2"),
    ("lizard", "蜥蜴", "U2"), ("kitten", "小貓", "U2"),
]

QUIZ_SIZE = 10
CHOICE_RATIO = 0.4   # zh→en 題數比例（其餘為拼字題）
NEW_PER_DAY = 5      # 每天新字數（固定）
REVIEW_CAP = 10      # 每天複習弱字上限

STYLE = """
@font-face { font-family:'Huninn'; src:url('../../assets/huninn.woff2') format('woff2'); font-display:swap; }
*{margin:0;padding:0;box-sizing:border-box;-webkit-tap-highlight-color:transparent;user-select:none;-webkit-user-select:none}
body{font-family:'Huninn',system-ui,sans-serif;background:#F3F0FA;min-height:100vh;color:#3B3352}
.wrap{max-width:560px;margin:0 auto;padding:20px 14px 50px;text-align:center}
h1{font-size:clamp(22px,5vw,30px)}
.sub{color:#7E749A;font-size:13px;margin:4px 0 12px}
.hud{display:flex;justify-content:center;gap:8px;margin-bottom:12px;flex-wrap:wrap}
.hud > span{font-size:13px;color:#7E749A;background:#fff;border-radius:999px;padding:6px 14px;box-shadow:0 2px 8px rgba(59,51,82,.08)}
.hud > span.src{color:#9A90B8}
.hud > span.sync.ok{color:#2E9B5F}.hud > span.sync.busy{color:#7E749A}.hud > span.sync.off,.hud > span.sync.stale,.hud > span.sync.bad{color:#B0563F}
button{font-family:inherit;border:none;cursor:pointer}
.panel{background:#fff;border-radius:22px;box-shadow:0 8px 26px rgba(59,51,82,.10);padding:22px 18px;margin-bottom:16px}
.bigbtn{background:#6C4DD6;color:#fff;font-size:20px;border-radius:999px;padding:14px 34px;margin-top:10px;
  box-shadow:0 4px 0 #4E36A6}
.bigbtn:active{transform:translateY(2px);box-shadow:0 2px 0 #4E36A6}
.bigbtn.alt{background:#fff;color:#6C4DD6;border:2px solid #6C4DD6;box-shadow:none;font-size:16px;padding:10px 24px}
.stat{color:#7E749A;font-size:14px;margin-top:8px;line-height:1.7}
.units{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin:10px 0 4px}
.chip{background:#EAE5F7;color:#6C4DD6;border-radius:999px;padding:6px 14px;font-size:13px}
.chip.on{background:#6C4DD6;color:#fff}
.boxes{display:flex;gap:6px;justify-content:center;margin-top:10px;font-size:13px;color:#7E749A;flex-wrap:wrap}
.boxes b{color:#3B3352}

/* --- 題目 --- */
.progress{display:flex;gap:4px;margin-bottom:14px}
.progress i{flex:1;height:8px;border-radius:4px;background:#E2DCF3}
.progress i.ok{background:#4CB77A}.progress i.ng{background:#E4574C}.progress i.cur{background:#B8A9F0}
.qtype{font-size:13px;color:#7E749A;margin-bottom:6px}
.prompt{font-size:clamp(30px,8vw,44px);line-height:1.3;margin:8px 0 14px;min-height:56px}
.speaker{background:#6C4DD6;color:#fff;width:84px;height:84px;border-radius:50%;font-size:40px;margin:6px auto 12px;
  display:flex;align-items:center;justify-content:center;box-shadow:0 4px 0 #4E36A6}
.speaker:active{transform:translateY(2px);box-shadow:0 2px 0 #4E36A6}
.zh-hint{font-size:26px;color:#3B3352;margin-bottom:10px}
.choices{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.choice{background:#F7F5FC;border:2px solid #E2DCF3;border-radius:16px;padding:16px 8px;font-size:22px;color:#3B3352}
.choice.ok{background:#E3F6EA;border-color:#4CB77A}
.choice.ng{background:#FDE7E4;border-color:#E4574C}
.choice:disabled{cursor:default}
.slots{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin:6px 0 14px;min-height:52px}
.slot{width:44px;height:52px;border-bottom:4px solid #C9BFEA;font-size:28px;display:flex;align-items:center;justify-content:center;color:#3B3352}
.slot.gap{width:18px;border:none}
.slot.fixed{width:22px;border:none;color:#9A90B8}
.slot.ok{border-color:#4CB77A}.slot.ng{border-color:#E4574C;color:#E4574C}
.tiles{display:flex;gap:8px;justify-content:center;flex-wrap:wrap}
.tile{width:48px;height:54px;background:#fff;border:2px solid #C9BFEA;border-radius:12px;font-size:26px;color:#3B3352;
  box-shadow:0 3px 0 #C9BFEA}
.tile:active{transform:translateY(2px);box-shadow:0 1px 0 #C9BFEA}
.tile.used{opacity:.25;pointer-events:none}
.tools{display:flex;gap:10px;justify-content:center;margin-top:14px}
.tool{background:#EAE5F7;color:#6C4DD6;border-radius:999px;padding:8px 18px;font-size:14px}
.tool:disabled{opacity:.4}
.feedback{font-size:18px;min-height:28px;margin-top:12px}
.feedback.ok{color:#2E9B5F}.feedback.ng{color:#E4574C}
.feedback b{font-size:24px}

/* --- 結果 --- */
.score{font-size:64px;line-height:1;color:#6C4DD6}
.stars{font-size:34px;letter-spacing:4px;margin:6px 0}
.wrongs{text-align:left;margin-top:12px;border-top:1px dashed #E2DCF3;padding-top:10px}
.wrongs .w{display:flex;align-items:center;gap:10px;padding:6px 0;font-size:17px}
.wrongs .w small{color:#7E749A;font-size:17px}
.wrongs .w button{background:#EAE5F7;border-radius:999px;width:34px;height:34px;font-size:16px}
.rec{color:#E4574C;font-size:16px;margin-top:8px}

/* --- 單字卡 --- */
.card{background:#fff;border-radius:22px;box-shadow:0 8px 26px rgba(59,51,82,.10);padding:34px 18px;margin-bottom:14px;
  min-height:220px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px}
.card .en{font-size:clamp(34px,9vw,48px)}
.card .zh{font-size:30px;color:#7E749A}
.card .sp{background:#EAE5F7;color:#6C4DD6;border-radius:999px;padding:8px 18px;font-size:16px}
.cardnav{display:flex;gap:10px;justify-content:center}
/* 直式注音在字右側（台灣課本式），em 單位跟著容器字級縮放 */
.zc{display:inline-flex;align-items:center;vertical-align:middle;margin:0 .14em 0 0}
.zc .h{font-size:1em;line-height:1.25}
.zc .zy{display:inline-flex;flex-direction:column;justify-content:center;margin-left:.06em}
.zc .zy i{font-style:normal;font-size:.42em;line-height:1.15;color:#7E749A;text-align:center;font-family:'Huninn',system-ui,sans-serif}
.zc .tn{font-size:.46em;color:#7E749A;align-self:center;line-height:1;font-family:'Huninn',system-ui,sans-serif}
.bigbtn .zc .zy i,.bigbtn .zc .tn,.chip .zc .zy i,.chip .zc .tn{color:inherit;opacity:.85}
/* --- 步驟指示 / 今日計畫 --- */
.steps{display:flex;justify-content:center;gap:6px;margin-bottom:12px;flex-wrap:wrap}
.steps > span{font-size:13px;color:#9A90B8;background:#EAE5F7;border-radius:999px;padding:5px 12px;white-space:nowrap}
.steps > span.on{background:#6C4DD6;color:#fff}
.steps > span.done{background:#E3F6EA;color:#2E9B5F}
.steps > span .zc .zy i,.steps > span .zc .tn{color:inherit;opacity:.8}
.plan{font-size:17px;line-height:1.9;margin:6px 0 4px}
.plan b{color:#6C4DD6}
.donebox{background:#E3F6EA;color:#2E9B5F;border-radius:14px;padding:10px 14px;font-size:15px;margin-bottom:10px}
.card .zh.dim{color:#B8AEDC}
.cardbtns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.cardbtns .bigbtn{margin-top:0}
.hidden{display:none !important}
footer{text-align:center;color:#9A90B8;font-size:13px;margin-top:30px}
"""

GAME_JS = r"""
'use strict';
const API = '__API__';
const SEED = __SEED__;
const QUIZ_SIZE = __QUIZ_SIZE__;
const CHOICE_RATIO = __CHOICE_RATIO__;
const NEW_PER_DAY = __NEW_PER_DAY__;
const REVIEW_CAP = __REVIEW_CAP__;
const WORDS_CACHE = 'owen-words-cache-v1';
const STATE_KEY = 'owen-wq-state-v1';    // {wordLower: {box, seen, wrong, last, intro}}
const BEST_KEY = 'owen-wq-best-v1';      // {allTime:{score,date}, today:{date,score}, plays}
const UNIT_KEY = 'owen-wq-unit';
const PROG_SHEET = 'kv_words';            // 雲端進度工作表（通用鍵值 API）
const PQUEUE_KEY = 'owen-wq-pqueue-v1';   // 待上傳 {key: jsonString}
const $ = id => document.getElementById(id);

/* ---------- 本機儲存 ---------- */
function lsGetObj(key, fallback) {
  try { const v = JSON.parse(localStorage.getItem(key) || 'null'); return (v && typeof v === 'object') ? v : fallback; }
  catch (e) { console.error('read', key, e); return fallback; }
}
function lsSet(key, val) { try { localStorage.setItem(key, JSON.stringify(val)); } catch (e) { console.error('write', key, e); } }
function lsGetStr(key, fallback) { try { return localStorage.getItem(key) || fallback; } catch (e) { return fallback; } }
function lsSetStr(key, val) { try { localStorage.setItem(key, val); } catch (e) { console.error('write', key, e); } }
function todayStr() {
  const d = new Date();
  return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
}

/* ---------- 單字資料 ---------- */
function normWords(list) {
  const seen = new Set(), out = [];
  for (const w of list || []) {
    const word = String((w && w.word) || '').trim(), zh = String((w && w.zh) || '').trim(), unit = String((w && w.unit) || '').trim();
    if (!word || !zh || word.length > 40 || !/^[A-Za-z][A-Za-z' -]*$/.test(word)) continue;
    const key = word.toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key); out.push({ word, zh, unit });
  }
  return out;
}
let words = normWords(lsGetObj(WORDS_CACHE, null) || SEED.map(a => ({ word: a[0], zh: a[1], unit: a[2] })));
let source = lsGetObj(WORDS_CACHE, null) ? 'cache' : 'seed';
let unit = lsGetStr(UNIT_KEY, 'ALL');
const newPerDay = NEW_PER_DAY;

function fetchWords() {
  return fetch(API + '?mode=words', { cache: 'no-store' })
    .then(r => r.json())
    .then(j => {
      if (!j || !j.ok || !Array.isArray(j.words)) throw new Error((j && j.error) || 'bad response');
      const fresh = normWords(j.words);
      if (fresh.length) { words = fresh; lsSet(WORDS_CACHE, fresh); source = 'cloud'; }
      else source = 'empty';
      renderHome();
    })
    .catch(err => { console.warn('words fetch failed', err); renderHome(); });
}
function unitsOf() { return Array.from(new Set(words.map(w => w.unit).filter(Boolean))); }
function pool() { return unit === 'ALL' ? words : words.filter(w => w.unit === unit); }

/* ---------- 熟練度（簡化 Leitner）＋「已介紹」 ----------
   box 0 不熟／1 快會了／2 已經會。intro＝第一次在卡片按「會了」的日期；小考只考 intro 過的字。
   舊版資料（沒有 intro 但 seen>0）視為已介紹，日期取 last。 */
let state = migrateState(lsGetObj(STATE_KEY, {}));
function migrateState(st) {
  let changed = false; const out = {};
  for (const k of Object.keys(st)) {
    const s = st[k];
    if (s && s.seen > 0 && !s.intro) { out[k] = Object.assign({}, s, { intro: s.last || todayStr() }); changed = true; }
    else out[k] = s;
  }
  if (changed) lsSet(STATE_KEY, out);
  return out;
}
function stOf(w) { return state[w.word.toLowerCase()] || null; }
function boxOf(w) { const s = stOf(w); return s ? (s.box | 0) : 0; }
function introOf(w) { const s = stOf(w); return s ? (s.intro || null) : null; }
function saveState(k, next) { state = Object.assign({}, state, { [k]: next }); lsSet(STATE_KEY, state); enqueue(k, next); }
function introduce(w) {
  const k = w.word.toLowerCase(), old = state[k] || { box: 0, seen: 0, wrong: 0 };
  if (old.intro) return;
  saveState(k, Object.assign({}, old, { intro: todayStr(), last: todayStr() }));
}
function mark(w, correct) {
  const k = w.word.toLowerCase(), old = state[k] || { box: 0, seen: 0, wrong: 0, intro: todayStr() };
  saveState(k, { box: correct ? Math.min(2, old.box + 1) : 0, seen: old.seen + 1, wrong: old.wrong + (correct ? 0 : 1), last: todayStr(), intro: old.intro || todayStr() });
}
function shuffle(a) { const b = a.slice(); for (let i = b.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [b[i], b[j]] = [b[j], b[i]]; } return b; }

/* ---------- 跨裝置同步：kv_words 工作表 ----------
   本機先寫、進佇列，0.8 秒後合併成一次 kv_set；開頁 GET 全部後與本機合併。 */
let pqueue = lsGetObj(PQUEUE_KEY, {});
let syncStatus = 'idle', flushTimer = null, flushing = false;
function setSync(st, msg) {
  syncStatus = st;
  const el = $('sync'); if (!el) return;
  el.textContent = msg; el.className = 'sync ' + st;
}
function enqueue(key, val) {
  pqueue = Object.assign({}, pqueue, { [key]: JSON.stringify(val) });
  lsSet(PQUEUE_KEY, pqueue);
  scheduleFlush();
}
function scheduleFlush() { clearTimeout(flushTimer); flushTimer = setTimeout(flush, 800); }
async function flush() {
  if (flushing) return;
  const batch = pqueue;
  if (!Object.keys(batch).length) return;
  flushing = true;
  setSync('busy', '⏳ 同步中');
  try {
    const r = await fetch(API, { method: 'POST', body: JSON.stringify({ action: 'kv_set', sheet: PROG_SHEET, items: batch }) });
    const j = await r.json();
    if (j && j.ok) {
      const rest = {};
      for (const k of Object.keys(pqueue)) if (pqueue[k] !== batch[k]) rest[k] = pqueue[k];   // 傳送期間又改過的保留
      pqueue = rest; lsSet(PQUEUE_KEY, pqueue);
      setSync('ok', '☁️ 進度已同步');
      if (Object.keys(pqueue).length) scheduleFlush();
    } else if (j && j.error === 'unknown action') {
      setSync('stale', '⚠️ 雲端待更新，進度先存這台');
    } else {
      setSync('bad', '⚠️ 同步失敗：' + ((j && j.error) || '未知錯誤'));
    }
  } catch (err) {
    console.warn('progress flush failed', err);
    setSync('off', '📵 離線，回線後自動補傳');
  } finally { flushing = false; }
}
function newer(a, b) {   // 兩筆同一字的紀錄挑較新的：seen 多者勝 → last 晚者勝 → 平手取 b
  if (!a) return b; if (!b) return a;
  if ((a.seen | 0) !== (b.seen | 0)) return (a.seen | 0) > (b.seen | 0) ? a : b;
  if (String(a.last || '') !== String(b.last || '')) return String(a.last || '') > String(b.last || '') ? a : b;
  return b;
}
function mergeBest(local, remote) {
  if (!remote) return local; if (!local || !local.allTime) return Object.assign({}, remote);
  const allTime = (!remote.allTime || (local.allTime.score > remote.allTime.score)) ? local.allTime : remote.allTime;
  let today = local.today;
  if (remote.today && (!today || remote.today.date > today.date || (remote.today.date === today.date && remote.today.score > today.score))) today = remote.today;
  return { allTime, today, plays: Math.max(local.plays || 0, remote.plays || 0) };
}
function mergeRemote(items) {
  let merged = {}, changedLocal = false;
  const keys = new Set(Object.keys(state).concat(Object.keys(items).filter(k => k !== 'best')));
  for (const k of keys) {
    let remote = null;
    try { remote = items[k] ? JSON.parse(items[k]) : null; } catch (e) { remote = null; }
    const local = state[k] || null;
    const chosen = newer(local, remote);         // 平手時雲端勝
    merged[k] = chosen;
    if (JSON.stringify(chosen) !== JSON.stringify(local)) changedLocal = true;
    if (JSON.stringify(chosen) !== (items[k] || null) && !(k in pqueue)) enqueue(k, chosen);   // 本機較新 → 補傳
  }
  state = merged;
  if (changedLocal) lsSet(STATE_KEY, state);
  let remoteBest = null;
  try { remoteBest = items.best ? JSON.parse(items.best) : null; } catch (e) { remoteBest = null; }
  const mb = mergeBest(best, remoteBest);
  if (JSON.stringify(mb) !== JSON.stringify(best)) { best = mb; lsSet(BEST_KEY, best); }
  if (JSON.stringify(mb) !== (items.best || null) && !('best' in pqueue) && best.allTime) enqueue('best', best);
}
function fetchProgress() {
  return fetch(API + '?mode=kv&sheet=' + PROG_SHEET, { cache: 'no-store' })
    .then(r => r.json())
    .then(j => {
      if (j && j.ok && j.entries) { setSync('stale', '⚠️ 雲端待更新，進度先存這台'); return; }   // 舊後端
      if (!j || !j.ok || !j.items || typeof j.items !== 'object') throw new Error((j && j.error) || 'bad response');
      mergeRemote(j.items);
      renderHome();
      if (Object.keys(pqueue).length) flush(); else setSync('ok', '☁️ 進度已同步');
    })
    .catch(err => {
      console.warn('progress fetch failed', err);
      setSync('off', '📵 讀不到雲端進度，先用這台的');
      if (Object.keys(pqueue).length) flush();
    });
}
window.addEventListener('online', () => { if (Object.keys(pqueue).length) flush(); });
document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible' && Object.keys(pqueue).length) flush(); });

/* ---------- 今日計畫 ---------- */
function plan() {
  const p = pool(), today = todayStr();
  const introduced = p.filter(w => introOf(w));
  const introducedToday = introduced.filter(w => introOf(w) === today);
  const allowance = Math.max(0, newPerDay - introducedToday.length);
  const fresh = p.filter(w => !introOf(w)).slice(0, allowance);            // 照單元／表格順序介入
  const weak = introduced.filter(w => introOf(w) !== today && boxOf(w) === 0)
    .sort((a, b) => String((stOf(a) || {}).last || '') < String((stOf(b) || {}).last || '') ? -1 : 1)
    .slice(0, REVIEW_CAP);
  const quizPool = introduced.length + fresh.length;                        // 學完新字後可考的字數
  return { fresh, weak, quizN: Math.min(QUIZ_SIZE, quizPool), introduced };
}
function pickQuiz() {
  const p = pool().filter(w => introOf(w)), today = todayStr();
  const wrongOld = p.filter(w => boxOf(w) === 0 && introOf(w) !== today);
  const fresh = p.filter(w => introOf(w) === today);
  const b1 = p.filter(w => boxOf(w) === 1), b2 = p.filter(w => boxOf(w) === 2);
  const seen = new Set(), out = [];
  for (const list of [shuffle(wrongOld), shuffle(fresh), shuffle(b1), shuffle(b2)]) {
    for (const w of list) { if (!seen.has(w.word)) { seen.add(w.word); out.push(w); } }
  }
  return shuffle(out.slice(0, QUIZ_SIZE));
}

/* ---------- 語音 / 音效 ---------- */
function speak(text) {
  try {
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'en-US'; u.rate = 0.8;
    speechSynthesis.cancel(); speechSynthesis.speak(u);
  } catch (e) {}
}
let AC = null;
function beep(freq, dur, type, gain) {
  try {
    if (!AC) AC = new (window.AudioContext || window.webkitAudioContext)();
    const o = AC.createOscillator(), g = AC.createGain();
    o.type = type || 'sine'; o.frequency.value = freq;
    g.gain.setValueAtTime(gain || 0.12, AC.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, AC.currentTime + dur);
    o.connect(g); g.connect(AC.destination);
    o.start(); o.stop(AC.currentTime + dur);
  } catch (e) {}
}
const sfx = {
  tap: () => beep(660, .05, 'triangle'),
  ok: () => { beep(660, .1); setTimeout(() => beep(880, .14), 100); },
  ng: () => beep(200, .3, 'sine', .1),
  win: () => { beep(660, .12); setTimeout(() => beep(830, .12), 110); setTimeout(() => beep(990, .2), 230); },
};

/* ---------- 注音（小一還看不懂國字：題目、答案、提示全部逐字上 ruby）---------- */
let ZY = null;
function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function zyHtml(zy) {
  const last = zy.slice(-1);
  const tone = 'ˊˇˋ'.includes(last) ? last : '';
  const light = last === '˙';
  const syms = (tone || light) ? zy.slice(0, -1) : zy;
  let col = light ? '<i>˙</i>' : '';
  for (const c of syms) col += '<i>' + c + '</i>';
  return '<span class="zy">' + col + '</span>' + (tone ? '<span class="tn">' + tone + '</span>' : '');
}
function ruby(text) {
  let out = '';
  for (const ch of String(text)) {
    out += (ZY && ZY[ch]) ? '<span class="zc"><span class="h">' + esc(ch) + '</span>' + zyHtml(ZY[ch]) + '</span>' : esc(ch);
  }
  return out;
}
function setZh(el, text) { el.dataset.zh = text; el.innerHTML = ruby(text); }
function refreshRuby() { for (const el of document.querySelectorAll('[data-zh]')) el.innerHTML = ruby(el.dataset.zh); }
fetch('../../assets/zhuyin.json')
  .then(r => r.ok ? r.json() : null)
  .then(m => { if (m) { ZY = m; refreshRuby(); } })
  .catch(err => console.error('zhuyin load failed', err));

/* ---------- 畫面切換 ---------- */
function show(id) { for (const p of ['home', 'cards', 'quiz', 'result']) $(p).classList.toggle('hidden', p !== id); }
const STEP_NAMES = ['學新字', '複習不熟', '小考'];
function renderSteps(cur) {
  $('steps').innerHTML = STEP_NAMES.map((n, i) =>
    '<span class="' + (i < cur ? 'done' : i === cur ? 'on' : '') + '">' + (i + 1) + ' ' + ruby(n) + '</span>').join('');
  $('steps').classList.toggle('hidden', cur < 0);
}

/* ---------- 首頁 ---------- */
let best = lsGetObj(BEST_KEY, {});
function renderHome() {
  const p = pool(), units = unitsOf(), pl = plan(), today = todayStr();
  $('units').innerHTML = units.length > 1
    ? ['ALL'].concat(units).map(u => '<button class="chip' + (u === unit ? ' on' : '') + '" data-u="' + u + '">' + (u === 'ALL' ? ruby('全部') : u) + '</button>').join('')
    : '';
  const n0 = p.filter(w => introOf(w) && boxOf(w) === 0).length, n1 = p.filter(w => boxOf(w) === 1).length, n2 = p.filter(w => boxOf(w) === 2).length;
  const nNew = p.filter(w => !introOf(w)).length;
  $('boxes').innerHTML = '<span>&#128218; ' + ruby('還沒學') + ' <b>' + nNew + '</b></span><span>&#127793; ' + ruby('不熟') + ' <b>' + n0 + '</b></span><span>&#127807; ' + ruby('快會了') + ' <b>' + n1 + '</b></span><span>&#127794; ' + ruby('已經會') + ' <b>' + n2 + '</b></span>';
  $('count').textContent = p.length + ' 個單字';
  $('src').textContent = { cloud: '☁️ 雲端單字表', cache: '☁️ 雲端單字表（快取）', seed: '📘 內建單字表', empty: '📘 內建單字表（雲端表是空的）' }[source] || '';
  const t = best.today && best.today.date === today ? best.today.score : null;
  $('best').innerHTML = (t !== null ? 'TODAY: ' + t + ' 分　' : '') + (best.allTime ? '🏆 EVER: ' + best.allTime.score + ' 分' : '🏆 EVER: —');
  $('plan').innerHTML = ruby('今天：') +
    (pl.fresh.length ? ruby('學') + ' <b>' + pl.fresh.length + '</b> ' + ruby('個新字') + '　' : '') +
    (pl.weak.length ? ruby('複習') + ' <b>' + pl.weak.length + '</b> ' + ruby('個不熟的字') + '　' : '') +
    (pl.quizN >= 2 ? ruby('小考') + ' <b>' + pl.quizN + '</b> ' + ruby('題') : '');
  $('donebox').classList.toggle('hidden', t === null);
  if (t !== null) $('donebox').innerHTML = '&#10004; ' + ruby('今天的小考做過了：') + t + ' ' + ruby('分。再練一次也可以！');
  const canStart = pl.fresh.length > 0 || pl.weak.length > 0 || pl.quizN >= 2;
  $('start').disabled = !canStart;
  setZh($('start'), canStart ? '開始今天的練習 ▶' : '單字不夠');
}
$('units').addEventListener('click', e => {
  const b = e.target.closest('.chip'); if (!b) return;
  unit = b.dataset.u; lsSetStr(UNIT_KEY, unit); renderHome();
});

/* ---------- 每日流程：學新字 → 複習不熟 → 小考 ---------- */
let flow = null;  // {step}
function startFlow() {
  flow = { step: 0 };
  runStep();
}
function runStep() {
  if (!flow) return;
  const pl = plan();
  if (flow.step === 0) {
    if (pl.fresh.length) return startDeck({ mode: 'learn', list: pl.fresh, step: 0, title: '學新字' });
    flow = { step: 1 };
  }
  if (flow.step === 1) {
    if (pl.weak.length) return startDeck({ mode: 'review', list: pl.weak, step: 1, title: '複習不熟的字' });
    flow = { step: 2 };
  }
  if (flow.step === 2) {
    if (plan().quizN >= 2) return startQuiz(2);
    flow = null; renderHome(); show('home');
  }
}
function advanceFlow() { if (!flow) return; flow = { step: flow.step + 1 }; runStep(); }

/* ---------- 卡片堆（學新字／複習）---------- */
let deck = null;  // {mode:'learn'|'review', list, i, title, step}
function startDeck(opts) {
  deck = Object.assign({ i: 0 }, opts);
  renderSteps(typeof opts.step === 'number' ? opts.step : -1);
  show('cards');
  renderCard();
}
function renderCard() {
  if (!deck || deck.i >= deck.list.length) return;
  const w = deck.list[deck.i];
  setZh($('cardTitle'), deck.title);
  $('cardNum').textContent = (deck.i + 1) + ' / ' + deck.list.length;
  $('cardEn').textContent = w.word;
  setZh($('cardZh'), w.zh);
  setZh($('cardKnow'), deck.mode === 'learn' ? '會了 ✓' : '記得 ✓');
  speak(w.word);
}
$('cardSay').onclick = () => { if (deck) speak(deck.list[deck.i].word); };
$('cardAgain').onclick = () => {   // 再看一次：排到堆尾，稍後再出現
  if (!deck) return;
  sfx.tap();
  const w = deck.list[deck.i];
  const rest = deck.list.slice(0, deck.i).concat(deck.list.slice(deck.i + 1), [w]);
  deck = Object.assign({}, deck, { list: rest });
  renderCard();
};
$('cardKnow').onclick = () => {
  if (!deck) return;
  sfx.ok();
  const w = deck.list[deck.i];
  if (deck.mode === 'learn') introduce(w);     // 只有「學新字」的會了＝已介紹；不改熟練度
  if (deck.i + 1 >= deck.list.length) return deckDone();
  deck = Object.assign({}, deck, { i: deck.i + 1 });
  renderCard();
};
function deckDone() {
  deck = null;
  advanceFlow();
}

/* ---------- 小考 ---------- */
let quiz = null;  // {items:[{w,type}], i, results:[bool], wrongs:[w]}
function startQuiz(step) {
  const chosen = pickQuiz();
  if (chosen.length < 2) { flow = null; renderHome(); show('home'); return; }
  const nChoice = Math.round(chosen.length * CHOICE_RATIO);
  const types = shuffle(chosen.map((_, i) => i < nChoice ? 'choice' : 'spell'));
  quiz = { items: chosen.map((w, i) => ({ w, type: types[i] })), i: 0, results: [], wrongs: [] };
  renderSteps(typeof step === 'number' ? step : -1);
  show('quiz');
  renderQuestion();
}
function renderProgress() {
  $('progress').innerHTML = quiz.items.map((_, i) =>
    '<i class="' + (i < quiz.results.length ? (quiz.results[i] ? 'ok' : 'ng') : (i === quiz.i ? 'cur' : '')) + '"></i>').join('');
}
function renderQuestion() {
  renderProgress();
  $('feedback').textContent = ''; $('feedback').className = 'feedback';
  $('next').classList.add('hidden');
  const item = quiz.items[quiz.i];
  $('qnum').textContent = (quiz.i + 1) + ' / ' + quiz.items.length;
  $('choiceQ').classList.toggle('hidden', item.type !== 'choice');
  $('spellQ').classList.toggle('hidden', item.type !== 'spell');
  if (item.type === 'choice') renderChoice(item.w); else renderSpell(item.w);
}

function renderChoice(w) {
  setZh($('qtype'), '中文選英文');
  setZh($('prompt'), w.zh);
  const others = shuffle(words.filter(x => x.word !== w.word)).slice(0, 3);
  const opts = shuffle([w].concat(others));
  $('choices').innerHTML = opts.map(o => '<button class="choice" data-w="' + esc(o.word).replace(/"/g, '&quot;') + '">' + esc(o.word) + '</button>').join('');
}
$('choices').addEventListener('click', e => {
  const b = e.target.closest('.choice'); if (!b || b.disabled) return;
  const w = quiz.items[quiz.i].w, correct = b.dataset.w === w.word;
  for (const c of $('choices').querySelectorAll('.choice')) { c.disabled = true; if (c.dataset.w === w.word) c.classList.add('ok'); }
  if (!correct) b.classList.add('ng');
  answer(correct);
});

let spell = null;  // {w, letters:[], order:[idx], picks:[idx]}
function isLetter(c) { return /^[A-Za-z]$/.test(c); }
function renderSpell(w) {
  setZh($('qtype'), '聽音拼字');
  setZh($('zhHint'), w.zh);
  const letters = w.word.split('');
  const tileIdx = letters.map((c, i) => isLetter(c) ? i : -1).filter(i => i >= 0);
  spell = { w, letters, order: shuffle(tileIdx), picks: [] };
  $('tiles').innerHTML = spell.order.map(i => '<button class="tile" data-i="' + i + '">' + letters[i] + '</button>').join('');
  renderSlots();
  setTimeout(() => speak(w.word), 250);
}
function renderSlots() {
  const filled = spell.picks.map(i => spell.letters[i]);
  let k = 0;
  $('slots').innerHTML = spell.letters.map(c => {
    if (c === ' ') return '<span class="slot gap"></span>';
    if (!isLetter(c)) return '<span class="slot fixed">' + esc(c) + '</span>';
    const ch = filled[k++]; return '<span class="slot">' + (ch === undefined ? '' : esc(ch)) + '</span>';
  }).join('');
  for (const t of $('tiles').querySelectorAll('.tile')) t.classList.toggle('used', spell.picks.indexOf(+t.dataset.i) >= 0);
  $('undo').disabled = !spell.picks.length;
}
$('tiles').addEventListener('click', e => {
  const t = e.target.closest('.tile'); if (!t || !spell || t.classList.contains('used')) return;
  sfx.tap();
  spell = Object.assign({}, spell, { picks: spell.picks.concat([+t.dataset.i]) });
  renderSlots();
  if (spell.picks.length === spell.order.length) checkSpell();
});
$('undo').onclick = () => { if (!spell || !spell.picks.length) return; spell = Object.assign({}, spell, { picks: spell.picks.slice(0, -1) }); renderSlots(); };
$('replay').onclick = () => { if (spell) speak(spell.w.word); };
function checkSpell() {
  const typed = spell.picks.map(i => spell.letters[i]).join('');
  const target = spell.letters.filter(isLetter).join('');
  const correct = typed.toLowerCase() === target.toLowerCase();
  const slots = $('slots').querySelectorAll('.slot:not(.gap):not(.fixed)');
  slots.forEach((s, k) => s.classList.add(typed[k].toLowerCase() === target[k].toLowerCase() ? 'ok' : 'ng'));
  for (const t of $('tiles').querySelectorAll('.tile')) t.classList.add('used');
  $('undo').disabled = true;
  answer(correct);
}

function answer(correct) {
  const w = quiz.items[quiz.i].w;
  mark(w, correct);
  quiz = Object.assign({}, quiz, { results: quiz.results.concat([correct]), wrongs: correct ? quiz.wrongs : quiz.wrongs.concat([w]) });
  renderProgress();
  const fb = $('feedback');
  fb.className = 'feedback ' + (correct ? 'ok' : 'ng');
  fb.innerHTML = correct ? '&#10004; ' + ruby('答對了！') : '&#10006; ' + ruby('是') + ' <b>' + esc(w.word) + '</b>';
  if (correct) sfx.ok(); else sfx.ng();
  setTimeout(() => speak(w.word), 300);
  setZh($('next'), quiz.i + 1 >= quiz.items.length ? '看成績 ★' : '下一題 ▶');
  $('next').classList.remove('hidden');
}
$('next').onclick = () => {
  if (quiz.i + 1 >= quiz.items.length) return finish();
  quiz = Object.assign({}, quiz, { i: quiz.i + 1 });
  renderQuestion();
};

/* ---------- 成績 ---------- */
function finish() {
  const n = quiz.items.length, right = quiz.results.filter(Boolean).length;
  const score = Math.round(right / n * 100);
  const today = todayStr();
  const prevToday = (best.today && best.today.date === today) ? best.today.score : null;
  const newToday = prevToday === null || score > prevToday;
  const newAll = !best.allTime || score > best.allTime.score;
  best = {
    today: newToday ? { date: today, score } : best.today,
    allTime: newAll ? { score, date: today } : best.allTime,
    plays: (best.plays || 0) + 1,
  };
  lsSet(BEST_KEY, best); enqueue('best', best);
  flow = null;
  renderSteps(-1);
  show('result');
  $('score').textContent = score;
  $('stars').textContent = score === 100 ? '⭐⭐⭐' : score >= 80 ? '⭐⭐' : score >= 60 ? '⭐' : '💪';
  setZh($('rstat'), right + ' / ' + n + ' 題答對');
  setZh($('rrec'), score === 100 ? '🏆 滿分！全部都會了！' : newAll && best.plays > 1 ? '🏆 歷代最佳紀錄！' : newToday && prevToday !== null ? '⭐ 今天的新紀錄！' : '');
  $('wrongs').innerHTML = quiz.wrongs.length
    ? '<div class="stat">' + ruby('這些字明天會再複習、再考一次：') + '</div>' + quiz.wrongs.map(w =>
        '<div class="w"><button data-say="' + esc(w.word).replace(/"/g, '&quot;') + '">&#128264;</button><span>' + esc(w.word) + '</span><small data-zh="' + esc(w.zh).replace(/"/g, '&quot;') + '">' + ruby(w.zh) + '</small></div>').join('')
    : '<div class="stat">' + ruby('今天的練習完成了，明天再來！👋') + '</div>';
  if (score === 100) sfx.win(); else if (score >= 60) sfx.ok();
}
$('wrongs').addEventListener('click', e => { const b = e.target.closest('button[data-say]'); if (b) speak(b.dataset.say); });
$('again').onclick = () => startQuiz(-1);
$('home2').onclick = () => { renderHome(); show('home'); };

$('start').onclick = startFlow;
refreshRuby();
renderHome();
fetchWords();
fetchProgress();
"""


def word_quiz_html():
    js = (GAME_JS.replace("__API__", API_URL)
          .replace("__SEED__", json.dumps(SEED_WORDS, ensure_ascii=False))
          .replace("__QUIZ_SIZE__", str(QUIZ_SIZE))
          .replace("__CHOICE_RATIO__", str(CHOICE_RATIO))
          .replace("__NEW_PER_DAY__", str(NEW_PER_DAY))
          .replace("__REVIEW_CAP__", str(REVIEW_CAP)))
    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>單字小考</title>
<meta name="robots" content="noindex">
<style>{STYLE}</style></head><body><div class="wrap">
<h1>&#128221; 單字小考</h1>
<div class="sub">每天三步：學新字 → 複習不熟 → 小考 10 題，錯的字會一直回來</div>
<div class="steps hidden" id="steps"></div>

<div id="home">
  <div class="hud"><span id="count"></span><span id="best"></span><span class="src" id="src"></span><span class="sync" id="sync">⏳ 讀取雲端進度</span></div>
  <div class="panel">
    <div class="units" id="units"></div>
    <div class="donebox hidden" id="donebox"></div>
    <div class="plan" id="plan"></div>
    <div class="boxes" id="boxes"></div>
    <button class="bigbtn" id="start"></button>
    <div class="stat">單字表在爸媽的試算表 words 分頁，加了新字重新開頁面就會更新</div>
  </div>
</div>

<div id="cards" class="hidden">
  <div class="hud"><span id="cardTitle"></span><span id="cardNum"></span></div>
  <div class="card">
    <div class="en" id="cardEn"></div>
    <div class="zh" id="cardZh"></div>
    <button class="sp" id="cardSay" data-zh="🔈 再唸一次"></button>
  </div>
  <div class="cardbtns">
    <button class="bigbtn alt" id="cardAgain" data-zh="再看一次 ↻"></button>
    <button class="bigbtn" id="cardKnow"></button>
  </div>
</div>

<div id="quiz" class="hidden">
  <div class="progress" id="progress"></div>
  <div class="panel">
    <div class="qtype"><span id="qtype"></span>　<span id="qnum"></span></div>
    <div id="choiceQ">
      <div class="prompt" id="prompt"></div>
      <div class="choices" id="choices"></div>
    </div>
    <div id="spellQ" class="hidden">
      <button class="speaker" id="replay">&#128264;</button>
      <div class="zh-hint" id="zhHint"></div>
      <div class="slots" id="slots"></div>
      <div class="tiles" id="tiles"></div>
      <div class="tools"><button class="tool" id="undo" data-zh="⌫ 退一格"></button></div>
    </div>
    <div class="feedback" id="feedback"></div>
    <button class="bigbtn hidden" id="next"></button>
  </div>
</div>

<div id="result" class="hidden">
  <div class="panel">
    <div class="score" id="score"></div>
    <div class="stars" id="stars"></div>
    <div class="stat" id="rstat"></div>
    <div class="rec" id="rrec"></div>
    <div class="wrongs" id="wrongs"></div>
    <button class="bigbtn" id="again" data-zh="再考一次 ▶"></button>
    <div><button class="bigbtn alt" id="home2" data-zh="回首頁"></button></div>
  </div>
</div>

<footer>made with &hearts; by Daddy &amp; Claude</footer>
</div><script>{js}</script></body></html>"""
