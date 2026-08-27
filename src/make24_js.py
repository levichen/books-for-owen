# -*- coding: utf-8 -*-
"""湊 24 對戰——遊戲邏輯 JS（規格 §3–§5、§8.2–8.3）。
佔位符：__DEALS__ 題庫 JSON。狀態機照 §4.1 轉移表實作。"""

GAME_JS = r"""
'use strict';
const DEALS = __DEALS__;
const TARGET = 24, WINS_NEEDED = 4, MAX_ROUNDS = 11, K = 24;
const T = { THINK: 10, ANSWER: 20, STEAL: 30, RACE: 30, EXT: 40 };
const OP_SYM = { '+': '+', '-': '−', '*': '×', '/': '÷' };
const OP_WORD = { '+': 'plus', '-': 'minus', '*': 'times', '/': 'divided by' };

/* ---------- 本機資料 ---------- */
function lsGet(k, fb) { try { const v = JSON.parse(localStorage.getItem(k)); return v == null ? fb : v; } catch (e) { return fb; } }
function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
let profiles = lsGet('owen-m24-profiles', { A: { id: 'A', label: 'PLAYER A', rating: 1000 }, B: { id: 'B', label: 'PLAYER B', rating: 1000 } });
let settings = lsGet('owen-m24-settings', { sound: true, voice: true });

/* ---------- 語音（偏離規格：v1 以 speechSynthesis 代替預錄音檔） ---------- */
const ONES = ['zero','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'];
const TENS = ['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety'];
function numWord(n) {
  if (n < 20) return ONES[n];
  if (n < 100) return TENS[Math.floor(n / 10)] + (n % 10 ? '-' + ONES[n % 10] : '');
  return String(n);
}
function speak(text) {
  if (!settings.voice) return;
  try {
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'en-US'; u.rate = 0.82;
    speechSynthesis.cancel(); speechSynthesis.speak(u);
  } catch (e) {}
}
function stepSentence(s) {
  return numWord(s.left) + ' ' + OP_WORD[s.op] + ' ' + numWord(s.right) + ' equals ' + numWord(s.result) + '.';
}

/* ---------- 音效（WebAudio 合成） ---------- */
let AC = null;
function audio() { if (!AC) AC = new (window.AudioContext || window.webkitAudioContext)(); return AC; }
function beep(freq, dur, type, gain) {
  if (!settings.sound) return;
  try {
    const ctx = audio(), o = ctx.createOscillator(), g = ctx.createGain();
    o.type = type || 'sine'; o.frequency.value = freq;
    g.gain.setValueAtTime(gain || 0.12, ctx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + dur);
    o.connect(g); g.connect(ctx.destination);
    o.start(); o.stop(ctx.currentTime + dur);
  } catch (e) {}
}
const sfx = {
  deal: () => { beep(420, .08); setTimeout(() => beep(520, .08), 90); },
  select: () => beep(660, .05, 'triangle'),
  merge: () => beep(880, .12, 'triangle'),
  buzz: () => { beep(980, .15, 'square', .08); },
  win: () => { beep(660, .12); setTimeout(() => beep(830, .12), 110); setTimeout(() => beep(990, .2), 230); },
  soft: () => beep(200, .25, 'sine', .08),
  tick: () => beep(1200, .03, 'sine', .04),
  go: () => beep(740, .25, 'square', .1),
};

/* ---------- 狀態 ---------- */
let match = null;          // {rounds, wins:{A,B}, usedIds, hardCount}
let round = null;          // {deal, buzzedBy, outcome, winner, roundNo, noneExtra}
let state = 'IDLE';
let boards = {};           // side -> {cards:[{id,value}], sel:{left,op}, undo:[], frozen}
let timers = {};           // side/main -> {deadline, iv}
let hint = {};             // side -> {usedRound, availableAt, level}
let cardSeq = 0;
const $ = id => document.getElementById(id);
const now = () => Date.now();

function otherSide(s) { return s === 'A' ? 'B' : 'A'; }
function delta(side) { return profiles[otherSide(side)].rating - profiles[side].rating; }
function hintPlan(side) {
  const d = delta(side);
  if (d > 250) return { level: 2, cd: 4, ext: true };
  if (d > 100) return { level: 1, cd: 8, ext: false };
  return { level: 1, cd: 20, ext: false };
}

/* ---------- 抽題（§8.1 難度規則） ---------- */
function pickDeal() {
  const avg = (profiles.A.rating + profiles.B.rating) / 2;
  const rNo = match.rounds.length + 1;
  let want;
  if (rNo <= 2 || avg < 950) want = 'easy';
  else if (avg > 1150 && match.hardCount < 3) want = 'hard';
  else want = 'medium';
  const prev = match.rounds.length ? match.rounds[match.rounds.length - 1].deal.difficulty : null;
  if (prev === 'easy' && want === 'hard') want = 'medium';
  let pool = DEALS.filter(d => d.difficulty === want && !match.usedIds.includes(d.id));
  if (!pool.length) pool = DEALS.filter(d => !match.usedIds.includes(d.id));
  const deal = pool[Math.floor(Math.random() * pool.length)];
  match.usedIds.push(deal.id);
  if (deal.difficulty === 'hard') match.hardCount++;
  return deal;
}

/* ---------- Board ---------- */
function newBoard(deal) {
  return { cards: deal.values.map(v => ({ id: 'c' + (++cardSeq), value: v })), sel: { left: null, op: null }, undo: [], frozen: true };
}
function legalRight(b, leftCard, op, c) {
  if (c.id === leftCard.id) return false;
  const a = leftCard.value, v = c.value;
  if (op === '-') return a - v >= 0;
  if (op === '/') return v !== 0 && a % v === 0;
  return true;
}
function opLegal(b, leftCard, op) {
  return b.cards.some(c => legalRight(b, leftCard, op, c));
}
function doMerge(b, leftId, op, rightId) {
  b.undo.push(JSON.stringify({ cards: b.cards }));
  const l = b.cards.find(c => c.id === leftId), r = b.cards.find(c => c.id === rightId);
  const v = op === '+' ? l.value + r.value : op === '-' ? l.value - r.value : op === '*' ? l.value * r.value : l.value / r.value;
  const merged = { id: 'c' + (++cardSeq), value: v, fresh: true };
  b.cards = b.cards.filter(c => c.id !== leftId && c.id !== rightId).concat([merged]);
  b.sel = { left: null, op: null };
  sfx.merge();
  return v;
}
function undoBoard(b) {
  if (!b.undo.length) return;
  b.cards = JSON.parse(b.undo.pop()).cards;
  b.sel = { left: null, op: null };
}
function resetBoard(b, deal) {
  b.cards = deal.values.map(v => ({ id: 'c' + (++cardSeq), value: v }));
  b.sel = { left: null, op: null }; b.undo = [];
}
function solved(b) { return b.cards.length === 1 && b.cards[0].value === TARGET; }

/* ---------- 計時 ---------- */
function startTimer(name, secs, onEnd, tickCb) {
  stopTimer(name);
  const deadline = now() + secs * 1000;
  timers[name] = { deadline, iv: setInterval(() => {
    const left = Math.max(0, Math.ceil((deadline - now()) / 1000));
    if (tickCb) tickCb(left);
    if (deadline - now() <= 0) { stopTimer(name); onEnd(); }
  }, 200) };
}
function stopTimer(name) { if (timers[name]) { clearInterval(timers[name].iv); delete timers[name]; } }
function stopAllTimers() { Object.keys(timers).forEach(stopTimer); }

/* ---------- 畫面 ---------- */
function setMid(text, sub) {
  ['m-main-a', 'm-main-b'].forEach(id => { $(id).textContent = text; });
  ['m-sub-a', 'm-sub-b'].forEach(id => { $(id).textContent = sub || ''; });
}
function renderLights() {
  const total = Math.max(7, match ? match.rounds.length + (state === 'MATCH_END' ? 0 : 1) : 7);
  ['lights-a', 'lights-b'].forEach(id => {
    const el = $(id); el.innerHTML = '';
    if (!match) return;
    match.rounds.forEach(r => {
      const d = document.createElement('span');
      d.className = 'lt ' + (r.outcome === 'none' ? 'none' : ('w' + r.winner + (r.outcome === 'buzz_win' ? ' zap' : '')));
      d.textContent = r.outcome === 'none' ? '' : (r.outcome === 'buzz_win' ? '⚡' : '');
      el.appendChild(d);
    });
    for (let i = match.rounds.length; i < total; i++) {
      const d = document.createElement('span'); d.className = 'lt'; el.appendChild(d);
    }
  });
}
function renderBoard(side, viewBoard, operable) {
  const b = viewBoard || boards[side];
  const wrap = $('cards-' + side); wrap.innerHTML = '';
  b.cards.forEach(c => {
    const btn = document.createElement('button');
    btn.className = 'tile' + (b.sel.left === c.id ? ' sel' : '') + (c.fresh ? ' fresh' : '');
    btn.textContent = c.value;
    let dis = !operable || b.frozen;
    if (!dis && b.sel.left && b.sel.op) {
      const leftCard = b.cards.find(x => x.id === b.sel.left);
      if (!legalRight(b, leftCard, b.sel.op, c) && c.id !== b.sel.left) dis = true;
    }
    btn.disabled = dis;
    btn.onclick = () => onCard(side, c.id);
    wrap.appendChild(btn);
  });
  const leftCard = b.sel.left ? b.cards.find(x => x.id === b.sel.left) : null;
  ['+', '-', '*', '/'].forEach(op => {
    const el = $('op-' + op.charCodeAt(0) + '-' + side);
    el.classList.toggle('sel', b.sel.op === op);
    el.disabled = !operable || b.frozen || !leftCard || !opLegal(b, leftCard, op);
  });
  $('undo-' + side).disabled = !operable || b.frozen || !b.undo.length;
  $('reset-' + side).disabled = !operable || b.frozen;
  $('left-' + side).textContent = operable && !b.frozen ? b.cards.length + (b.cards.length === 1 ? ' CARD LEFT' : ' CARDS LEFT') : '';
  b.cards.forEach(c => delete c.fresh);
}
function setStatus(side, text, cls) {
  const el = $('status-' + side);
  el.textContent = text; el.className = 'pstatus ' + (cls || '');
}
function flash(side, text) {
  const el = $('flash-' + side);
  el.textContent = text; el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 1100);
}
function setBuzz(side, on) { $('buzz-' + side).disabled = !on; }
function setHintBtn(side) {
  const h = hint[side], btn = $('hint-' + side);
  if (!h || h.usedRound === roundNo() || !operableNow(side)) { btn.disabled = true; btn.textContent = 'HINT 💡'; return; }
  const wait = Math.ceil((h.availableAt - now()) / 1000);
  if (wait > 0) { btn.disabled = true; btn.textContent = wait + 's'; }
  else { btn.disabled = false; btn.textContent = 'HINT 💡'; }
}
function roundNo() { return round ? round.roundNo : 0; }
function operableNow(side) {
  if (state === 'ANSWERING') return round.buzzedBy === side;
  if (state === 'STEALING') return round.buzzedBy !== side;
  if (state === 'RACING') return !boards[side].frozen;
  return false;
}
function renderAll() {
  ['A', 'B'].forEach(s => {
    let view = null, op = operableNow(s);
    if (state === 'ANSWERING' && round.buzzedBy !== s) view = boards[round.buzzedBy]; // 對手看得到搶答方操作
    renderBoard(s, view, op);
    setHintBtn(s);
  });
  renderLights();
}

/* ---------- 互動 ---------- */
let lastTap = 0;
function throttled() { const t = now(); if (t - lastTap < 250) return true; lastTap = t; return false; }
function onCard(side, cardId) {
  if (throttled() || !operableNow(side)) return;
  const b = boards[side];
  if (!b.sel.left) { b.sel.left = cardId; sfx.select(); }
  else if (cardId === b.sel.left) { b.sel = { left: null, op: null }; }
  else if (b.sel.op) {
    doMerge(b, b.sel.left, b.sel.op, cardId);
    if (solved(b)) return onSolved(side);
    if (b.cards.length === 1) { flash(side, 'SO CLOSE!'); sfx.soft(); }
  } else { b.sel.left = cardId; sfx.select(); }
  renderAll();
}
function onOp(side, op) {
  if (throttled() || !operableNow(side)) return;
  const b = boards[side];
  if (!b.sel.left) return;
  b.sel.op = (b.sel.op === op ? null : op);
  sfx.select();
  renderAll();
}
function onUndo(side) { if (throttled() || !operableNow(side)) return; undoBoard(boards[side]); renderAll(); }
function onReset(side) { if (throttled() || !operableNow(side)) return; resetBoard(boards[side], round.deal); renderAll(); }
function onHint(side) {
  if (throttled() || !operableNow(side)) return;
  const h = hint[side];
  if (!h || h.usedRound === roundNo() || now() < h.availableAt) return;
  h.usedRound = roundNo();
  const first = round.deal.canonicalSolution[0];
  if (h.level >= 2) {
    $('hintline-' + side).textContent = 'START WITH ' + first.left + ' ' + OP_SYM[first.op] + ' ' + first.right;
  } else {
    const b = boards[side];
    const ids = [];
    for (const v of [first.left, first.right]) {
      const c = b.cards.find(x => x.value === v && !ids.includes(x.id));
      if (c) ids.push(c.id);
    }
    const tiles = $('cards-' + side).querySelectorAll('.tile');
    b.cards.forEach((c, i) => { if (ids.includes(c.id)) tiles[i] && tiles[i].classList.add('hl'); });
    setTimeout(() => renderAll(), 4000);
  }
  setHintBtn(side);
}

/* ---------- 狀態機（§4.1） ---------- */
function startMatch() {
  audio().resume && audio().resume();
  match = { rounds: [], wins: { A: 0, B: 0 }, usedIds: [], hardCount: 0, startedAt: now() };
  $('overlay').style.display = 'none';
  nextRound();
}
function nextRound() {
  state = 'DEALING';
  const deal = pickDeal();
  round = { deal, buzzedBy: null, outcome: null, winner: null, roundNo: match.rounds.length + 1, buzzAt: null, operStart: null };
  boards = { A: newBoard(deal), B: newBoard(deal) };
  hint = {};
  ['A', 'B'].forEach(s => {
    const p = hintPlan(s);
    hint[s] = { level: p.level, cd: p.cd, ext: p.ext, usedRound: -1, availableAt: Infinity };
    setStatus(s, 'ROUND ' + round.roundNo, '');
    $('hintline-' + s).textContent = '';
    setBuzz(s, false);
  });
  setMid('ROUND ' + round.roundNo, 'FIRST TO 4');
  renderAll();
  sfx.deal();
  setTimeout(enterThinking, 700);
}
function enterThinking() {
  state = 'THINKING';
  ['A', 'B'].forEach(s => { boards[s].frozen = true; setBuzz(s, true); setStatus(s, 'I KNOW? BUZZ!', 'warn'); });
  renderAll();
  round.dealtAt = now();
  startTimer('main', T.THINK, enterRacing, left => { setMid(String(left), 'BUZZ NOW'); if (left <= 3) sfx.tick(); });
}
function onBuzz(side) {
  if (state !== 'THINKING' || throttled()) return;
  stopTimer('main');
  state = 'ANSWERING';
  round.buzzedBy = side;
  round.buzzAt = now() - round.dealtAt;
  round.operStart = now();
  sfx.buzz();
  boards[side].frozen = false;
  hint[side].availableAt = now() + hint[side].cd * 1000;
  ['A', 'B'].forEach(s => setBuzz(s, false));
  setStatus(side, 'YOUR TURN', 'go');
  setStatus(otherSide(side), 'THEIR TURN', 'dim');
  renderAll();
  startTimer('main', T.ANSWER, () => failAnswer(side), left => setMid(String(left), profiles[side].label));
  const hi = setInterval(() => { if (state !== 'ANSWERING' && state !== 'STEALING' && state !== 'RACING') clearInterval(hi); ['A','B'].forEach(setHintBtn); }, 500);
}
function failAnswer(side) {
  // ANSWERING 失敗 → STEALING：牌面重設、對手獨享
  stopTimer('main');
  state = 'STEALING';
  const stealer = otherSide(side);
  resetBoard(boards[stealer], round.deal);
  boards[stealer].frozen = false;
  boards[side].frozen = true;
  round.operStart = now();
  hint[stealer].availableAt = now() + hint[stealer].cd * 1000;
  flash(stealer, 'STEAL IT!');
  setStatus(stealer, 'STEAL IT!', 'go');
  setStatus(side, "TIME'S UP ⏰", 'dim');
  sfx.soft();
  renderAll();
  const secs = hint[stealer].ext ? T.EXT : T.STEAL;
  startTimer('main', secs, () => endRound('none', null), left => setMid(String(left), 'STEAL'));
}
function enterRacing() {
  state = 'RACING';
  sfx.go();
  ['A', 'B'].forEach(s => {
    boards[s].frozen = false;
    setBuzz(s, false);
    setStatus(s, 'GO!', 'go');
    flash(s, 'GO!');
    hint[s].availableAt = now() + hint[s].cd * 1000;
    const secs = hint[s].ext ? T.EXT : T.RACE;
    startTimer('race-' + s, secs, () => {
      boards[s].frozen = true;
      setStatus(s, "TIME'S UP ⏰", 'dim');
      renderAll();
      if (boards.A.frozen && boards.B.frozen) endRound('none', null);
    }, left => { if (s === 'A') setMid(String(left), 'RACE'); });
  });
  round.operStart = now();
  renderAll();
}
function onSolved(side) {
  const outcome = state === 'ANSWERING' ? 'buzz_win' : state === 'STEALING' ? 'steal_win' : 'race_win';
  endRound(outcome, side);
}
function endRound(outcome, winner) {
  stopAllTimers();
  round.outcome = outcome; round.winner = winner;
  round.solveTimeMs = winner ? now() - round.operStart : null;
  if (winner) {
    state = 'SCORING';
    sfx.win();
    speak('Twenty-four! ' + (Math.random() < 0.5 ? 'Nice!' : 'Great!'));
    flash(winner, Math.random() < 0.5 ? 'YES!' : 'GOT IT!');
    setStatus(winner, 'YES! ⭐', 'go');
    setStatus(otherSide(winner), 'GOOD TRY', 'dim');
    match.wins[winner]++;
    updateRating(winner);
    finishScoring();
  } else {
    state = 'REVEAL';
    playReveal(() => { state = 'SCORING'; finishScoring(); });
  }
}
function updateRating(winner) {
  const loser = otherSide(winner);
  const eW = 1 / (1 + Math.pow(10, (profiles[loser].rating - profiles[winner].rating) / 400));
  profiles[winner].rating += K * (1 - eW);
  profiles[loser].rating += K * (0 - (1 - eW));
  lsSet('owen-m24-profiles', profiles);
}
function finishScoring() {
  match.rounds.push(round);
  renderLights();
  if (match.wins.A >= WINS_NEEDED || match.wins.B >= WINS_NEEDED || match.rounds.length >= MAX_ROUNDS) return matchEnd();
  setMid('NEXT ▶', match.wins.A + ' : ' + match.wins.B);
  setTimeout(nextRound, 2200);
}
function playReveal(done) {
  // 教學設計：none 局必播解法演示，每步 800ms＋完整英語句
  setMid('ONE WAY TO 24', '');
  const steps = round.deal.canonicalSolution;
  ['A', 'B'].forEach(s => { resetBoard(boards[s], round.deal); boards[s].frozen = true; setStatus(s, 'ONE WAY TO 24', 'warn'); });
  renderAll();
  let i = 0;
  function step() {
    if (i >= steps.length) { setTimeout(done, 1200); return; }
    const st = steps[i];
    ['A', 'B'].forEach(s => {
      const b = boards[s];
      const l = b.cards.find(c => c.value === st.left);
      const r = b.cards.find(c => c.value === st.right && c.id !== (l && l.id));
      if (l && r) { b.sel = { left: l.id, op: st.op }; renderBoard(s, null, false); doMerge(b, l.id, st.op, r.id); }
    });
    speak(stepSentence(st));
    ['A', 'B'].forEach(s => renderBoard(s, null, false));
    i++;
    setTimeout(step, 2600);
  }
  setTimeout(step, 600);
}
function matchEnd() {
  state = 'MATCH_END';
  const a = match.wins.A, b = match.wins.B;
  const winner = a > b ? 'A' : b > a ? 'B' : null;
  const hist = lsGet('owen-m24-history', []);
  hist.unshift({ at: match.startedAt, wins: match.wins, rounds: match.rounds.map(r => ({ o: r.outcome, w: r.winner })) });
  lsSet('owen-m24-history', hist.slice(0, 50));
  // 結算
  const bar = match.rounds.map(r =>
    r.outcome === 'none' ? '○' : (r.winner === 'A' ? '🔴' : '🔵') + (r.outcome === 'buzz_win' ? '⚡' : r.outcome === 'steal_win' ? '✓' : '')).join(' ');
  const buzzWins = match.rounds.filter(r => r.outcome === 'buzz_win' && r.solveTimeMs);
  const fastest = buzzWins.length ? Math.min(...buzzWins.map(r => r.solveTimeMs)) : null;
  const special = match.rounds.find(r => r.outcome === 'steal_win' || r.outcome === 'race_win');
  $('end-title').textContent = winner ? profiles[winner].label + ' WINS!' : 'A TIE!';
  $('end-score').textContent = a + ' : ' + b;
  $('end-bar').textContent = bar;
  $('end-notes').innerHTML =
    (fastest ? '⚡ FASTEST BUZZ WIN: ' + (fastest / 1000).toFixed(1) + 's<br>' : '') +
    (special ? (special.outcome === 'steal_win' ? '✓ STEAL WIN' : '🏁 RACE WIN') + ' BY ' + profiles[special.winner].label : '');
  $('endpanel').style.display = 'flex';
  ['A', 'B'].forEach(s => { setStatus(s, winner === s ? 'YOU WIN!' : winner ? 'GOOD GAME' : 'A TIE!', winner === s ? 'go' : 'dim'); setBuzz(s, false); });
  speak(winner ? 'Good game!' : 'A tie!');
}

/* ---------- 設定與大人鎖 ---------- */
function grownUpGate() {
  const x = 11 + Math.floor(Math.random() * 19), y = 3 + Math.floor(Math.random() * 7);
  const ans = prompt('GROWN-UPS ONLY 🔒  ' + x + ' × ' + y + ' = ?');
  return ans !== null && parseInt(ans, 10) === x * y;
}
function openSettings() {
  if (!grownUpGate()) return;
  const s = prompt('sound on/off?', settings.sound ? 'on' : 'off');
  if (s !== null) settings.sound = s.trim() !== 'off';
  const v = prompt('voice on/off?', settings.voice ? 'on' : 'off');
  if (v !== null) settings.voice = v.trim() !== 'off';
  const la = prompt('Player A name (A-Z, max 8)?', profiles.A.label);
  if (la) profiles.A.label = la.toUpperCase().replace(/[^A-Z ]/g, '').slice(0, 8) || profiles.A.label;
  const lb = prompt('Player B name (A-Z, max 8)?', profiles.B.label);
  if (lb) profiles.B.label = lb.toUpperCase().replace(/[^A-Z ]/g, '').slice(0, 8) || profiles.B.label;
  lsSet('owen-m24-settings', settings); lsSet('owen-m24-profiles', profiles);
  $('name-A').textContent = profiles.A.label; $('name-B').textContent = profiles.B.label;
}

/* ---------- 綁定 ---------- */
['A', 'B'].forEach(s => {
  $('buzz-' + s).onclick = () => onBuzz(s);
  $('hint-' + s).onclick = () => onHint(s);
  $('undo-' + s).onclick = () => onUndo(s);
  $('reset-' + s).onclick = () => onReset(s);
  ['+', '-', '*', '/'].forEach(op => { $('op-' + op.charCodeAt(0) + '-' + s).onclick = () => onOp(s, op); });
});
$('start-btn').onclick = () => { if (!throttled()) startMatch(); };
$('again-btn').onclick = () => { $('endpanel').style.display = 'none'; startMatch(); };
$('gear').onclick = openSettings;
window.addEventListener('beforeunload', e => {
  if (state !== 'IDLE' && state !== 'MATCH_END') { e.preventDefault(); e.returnValue = ''; }
});
$('name-A').textContent = profiles.A.label; $('name-B').textContent = profiles.B.label;
setMid('FIRST TO 4', 'PRESS START');
"""
