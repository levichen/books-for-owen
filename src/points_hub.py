# -*- coding: utf-8 -*-
"""點數 hub 頁（site/points/）：三個計數器的入口＋即時進度總覽＋家長區表現扣分（無大人鎖，2026-09-21 移除）。
未來新計數器都掛這一頁。HOME_JS 同時供首頁預覽按鈕使用。"""

from reading_log import API_URL

# 即時進度 JS（首頁與點數 hub 共用）：三 API 平行抓，先顯示快取再更新
HOME_JS = """
(function(){
'use strict';
var API='__API__';
var PTS={'小安素':3,'保久乳':1,'水':1};
function fmt(n){return n.toLocaleString('en-US');}
function line(total, goal, unit){
  if(total===0) return '每滿 '+fmt(goal)+' '+unit+'換禮物 \\u{1F381}';
  if(total%goal===0) return '<b>'+fmt(total)+'</b> '+unit+'・達標可以換禮物啦！\\u{1F381}';
  return '<b>'+fmt(total)+'</b> '+unit+'・再 '+fmt(goal-total%goal)+' '+unit+'換禮物 \\u{1F381}';
}
function show(id, html){var el=document.getElementById(id); if(el) el.innerHTML=html;}
function render(s){
  if(!s) return;
  if(typeof s.books==='number') show('sum-books', line(s.books,100,'本'));
  if(typeof s.drinks==='number') show('sum-drinks', line(s.drinks,100,'點'));
  if(typeof s.jumps==='number') show('sum-jumps', line(s.jumps,10000,'次'));
}
try{ render(JSON.parse(localStorage.getItem('owen-home-summary')||'null')); }catch(e){}
function jget(u){return fetch(u,{cache:'no-store'}).then(function(r){return r.json()}).catch(function(){return null});}
function loadAll(){
  return jget(API+'?mode=all').then(function(a){
    if(a&&a.ok&&Array.isArray(a.drinks)) return [{ok:true,entries:a.entries},{ok:true,drinks:a.drinks},{ok:true,items:a.jumps},{ok:true,items:a.penalty},a.penalty_reasons||null];
    return Promise.all([jget(API), jget(API+'?mode=drinks'), jget(API+'?mode=counter&sheet=jumps'), jget(API+'?mode=counter&sheet=penalty'), null]);  // 舊後端
  });
}
loadAll().then(function(rs){
  var b=rs[0],d=rs[1],j=rs[2],p=rs[3],reasons=rs[4];
  var pen=0;
  if(p&&p.ok&&Array.isArray(p.items)) pen=p.items.reduce(function(t,e){return t+(parseInt(e.value,10)||0)},0);
  try{localStorage.setItem('owen-penalty-cache', String(pen));}catch(e){}
  var s={penalty:pen};
  if(b&&b.ok&&Array.isArray(b.entries)) s.books=Math.max(0, b.entries.length-pen);
  if(d&&d.ok&&Array.isArray(d.drinks)) s.drinks=Math.max(0, d.drinks.reduce(function(t,e){return t+(PTS[e.kind]||1)},0)-pen);
  if(j&&j.ok&&Array.isArray(j.items)) s.jumps=Math.max(0, j.items.reduce(function(t,e){return t+(parseInt(e.value,10)||0)},0)-pen);
  render(s);
  if(typeof window.onPenaltyData==='function') window.onPenaltyData(p, reasons);
  try{localStorage.setItem('owen-home-summary', JSON.stringify(s));}catch(e){}
});
})();
"""

STYLE = """
@font-face { font-family:'Huninn'; src:url('../assets/huninn.woff2') format('woff2'); font-display:swap; }
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Huninn',system-ui,sans-serif;background:#FBF4E8;min-height:100vh;color:#4A3B32}
.wrap{max-width:760px;margin:0 auto;padding:26px 16px 60px}
h1{font-size:clamp(24px,5vw,34px);text-align:center}
.sub{color:#8A7460;text-align:center;margin:6px 0 24px;font-size:14px}
.pcard{display:block;background:#fff;border-radius:22px;box-shadow:0 8px 26px rgba(74,59,50,.10);
  padding:20px 22px;margin-bottom:16px;text-decoration:none;color:#4A3B32}
.pcard .t{font-size:19px}
.pcard .s{display:block;font-size:14px;color:#8A7460;margin-top:6px}
.pcard.books .s b{color:#E4574C}
.pcard.drinks .s b{color:#3D7BC4}
.pcard.jumps .s b{color:#43A047}
.pcard .go{float:right;color:#B8A88F;font-size:14px;margin-top:4px}
/* 家長區：表現扣分 */
.pen-card{background:#FBF1EC;border:2px dashed #E0B8A8;border-radius:22px;padding:18px 22px;margin-top:28px}
.pen-card .t{font-size:16px;color:#8A5A48}
.pen-card .s{font-size:13px;color:#A8887A;margin-top:6px;line-height:1.6}
.pen-btns{display:flex;gap:10px;margin-top:12px;flex-wrap:wrap}
button{font-family:inherit;border:none;cursor:pointer}
.pen-btn{background:#B0563F;color:#fff;border-radius:999px;padding:10px 20px;font-size:14px}
.pen-undo{background:#EFE0D8;color:#8A5A48;border-radius:999px;padding:10px 20px;font-size:14px}
.pen-msg{font-size:13px;color:#B0563F;margin-top:8px;min-height:18px}
.pen-list{list-style:none;margin-top:14px;border-top:1px dashed #E0B8A8;padding-top:10px}
.pen-list li{display:flex;gap:10px;align-items:baseline;padding:6px 0;font-size:14px;color:#6E4A3C;border-bottom:1px dashed #F0DDD4}
.pen-list li:last-child{border-bottom:none}
.pen-list .d{color:#A8887A;font-size:13px;flex:0 0 auto}
.pen-list .v{color:#B0563F;flex:0 0 auto}
.pen-list .r{flex:1;word-break:break-all}
.pen-list .r.none{color:#C4A99C}
footer{text-align:center;color:#B8A88F;font-size:13px;margin-top:30px}
"""

PENALTY_JS = """
(function(){
'use strict';
var API='__API__';
var REASON_SHEET='kv_penalty';   // 扣分原因：key＝penalty 列 id，value＝{reason,date}
var items=[], reasons={};
function esc(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function fetchReasons(){
  return fetch(API+'?mode=kv&sheet='+REASON_SHEET,{cache:'no-store'}).then(function(r){return r.json()}).then(function(j){
    if(j&&j.ok&&j.items&&typeof j.items==='object'){ reasons=j.items; renderPen(); }
  }).catch(function(e){ console.warn('reasons fetch failed', e); });
}
function reasonOf(id){
  try{ var v=JSON.parse(reasons[id]||'null'); return (v&&v.reason)?String(v.reason):''; }catch(e){ return ''; }
}
function saveReason(id, reason, date){
  var body={action:'kv_set',sheet:REASON_SHEET,items:{}}; body.items[id]=JSON.stringify({reason:reason,date:date});
  return fetch(API,{method:'POST',body:JSON.stringify(body)}).then(function(r){return r.json()});
}
function renderPen(){
  var sum=items.reduce(function(t,e){return t+(parseInt(e.value,10)||0)},0);
  document.getElementById('pen-stat').textContent = sum>0
    ? '目前累計扣分：已扣 '+items.length+' 次、三本各 −'+sum
    : '目前沒有扣分紀錄';
  document.getElementById('pen-undo').disabled = !items.length;
  var rows=items.slice().sort(function(a,b){return a.date<b.date?1:a.date>b.date?-1:0}).map(function(e){
    var r=reasonOf(e.id);
    return '<li><span class="d">'+esc(e.date)+'</span><span class="v">−'+esc(e.value)+'</span>'+
      (r?'<span class="r">'+esc(r)+'</span>':'<span class="r none">（未填原因）</span>')+'</li>';
  });
  document.getElementById('pen-list').innerHTML = rows.join('');
}
window.onPenaltyData = function(p, r){
  if(r&&typeof r==='object') reasons=r; else fetchReasons();
  if(p&&p.ok&&Array.isArray(p.items)){ items=p.items; renderPen(); }
};
function msg(t){ document.getElementById('pen-msg').textContent=t; }
document.getElementById('pen-add').onclick=function(){
  var reason=prompt('扣分原因（會列在清單上，最多 100 字）');
  if(reason===null){ msg('已取消'); return; }
  reason=String(reason).trim().slice(0,100);
  msg('記錄中…');
  var today=(function(d){return d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0')})(new Date());
  var before={}; items.forEach(function(e){before[e.id]=1});
  fetch(API,{method:'POST',body:JSON.stringify({action:'counter_add',sheet:'penalty',date:today,value:10})})
    .then(function(r){return r.json()}).then(function(j){
      if(!(j&&j.ok&&Array.isArray(j.items))){ msg('失敗：'+(j&&j.error||'連線問題')); return; }
      items=j.items; renderPen();
      var added=items.filter(function(e){return !before[e.id]}); var id=added.length?added[added.length-1].id:null;
      var p = (id&&reason) ? saveReason(id, reason, today).then(function(k){ if(k&&k.ok){ reasons[id]=JSON.stringify({reason:reason,date:today}); renderPen(); } else msg('扣分成功但原因未存：'+(k&&k.error||'?')); }).catch(function(){ msg('扣分成功但原因未存（連線問題）'); }) : Promise.resolve();
      p.then(function(){ msg('已扣分：三本各 −10'); setTimeout(function(){location.reload()},1200); });
    }).catch(function(){ msg('連不上雲端，稍後再試'); });
};
document.getElementById('pen-undo').onclick=function(){
  if(!items.length) return;
  if(!confirm('確定撤銷最近一筆扣分？')) return;
  msg('撤銷中…');
  var last=items[items.length-1];
  fetch(API,{method:'POST',body:JSON.stringify({action:'counter_del',sheet:'penalty',id:last.id})})
    .then(function(r){return r.json()}).then(function(j){
      if(j&&j.ok&&Array.isArray(j.items)){ items=j.items; renderPen(); msg('已撤銷最近一筆扣分'); setTimeout(function(){location.reload()},1200); }
      else msg('失敗：'+(j&&j.error||'連線問題'));
    }).catch(function(){ msg('連不上雲端，稍後再試'); });
};
renderPen();
})();
"""


def points_html():
    js = HOME_JS.replace("__API__", API_URL) + PENALTY_JS.replace("__API__", API_URL)
    return f"""<!DOCTYPE html><html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Owen 的點數</title>
<meta name="robots" content="noindex">
<style>{STYLE}</style></head><body><div class="wrap">
<h1>&#127873; Owen 的點數</h1>
<div class="sub">三種累積，滿了都能換禮物</div>

<a class="pcard books" href="../reading-log/"><span class="go">前往 &rarr;</span>
  <div class="t">&#128214; 閱讀紀錄</div>
  <span class="s" id="sum-books">每滿 100 本換禮物 &#127873;</span></a>

<a class="pcard drinks" href="../drink-log/"><span class="go">前往 &rarr;</span>
  <div class="t">&#129475; 牛奶點數</div>
  <span class="s" id="sum-drinks">每滿 100 點換禮物 &#127873;</span></a>

<a class="pcard jumps" href="../jump-log/"><span class="go">前往 &rarr;</span>
  <div class="t">&#129336; 跳繩次數</div>
  <span class="s" id="sum-jumps">每滿 10,000 次換禮物 &#127873;</span></a>

<div class="pen-card">
  <div class="t">&#9888;&#65039; 表現扣分（家長區）</div>
  <div class="s">表現不好時按一下：<b>閱讀、牛奶、跳繩三本各扣 10 分</b>，會問扣分原因並列在下方。按錯可撤銷最近一筆。<br>
  <span id="pen-stat">讀取中&hellip;</span></div>
  <div class="pen-btns">
    <button class="pen-btn" id="pen-add">三本各扣 10 分</button>
    <button class="pen-undo" id="pen-undo" disabled>撤銷最近一筆</button>
  </div>
  <div class="pen-msg" id="pen-msg"></div>
  <ul class="pen-list" id="pen-list"></ul>
</div>

<footer>made with &hearts; by Daddy &amp; Claude</footer>
</div><script>{js}</script></body></html>"""
