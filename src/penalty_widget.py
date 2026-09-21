# -*- coding: utf-8 -*-
"""扣分紀錄小卡（三本集點頁共用）：條列每一筆扣分的日期、−10、原因，中文逐字加注音。

資料：penalty 工作表（通用 counter API，各頁的 fetchPenalty 已抓，抓到後呼叫 PenaltyWidget.setItems）
＋ kv_penalty 工作表（原因，key＝扣分列 id；由本小卡自己抓）。沒有扣分時整張卡隱藏。
注音字典 ../assets/zhuyin.json 懶載入；ruby class 以 pz 開頭，避免與閱讀紀錄頁的 .zc 衝突。"""

PEN_CSS = """
/* --- 扣分紀錄小卡 --- */
.pen-box{border:2px dashed #E0B8A8;background:#FBF1EC}
.pen-title{font-size:17px;color:#8A5A48}
.pen-note{font-size:13px;color:#A8887A;margin-top:4px}
.pen-list{list-style:none;margin-top:10px}
.pen-list li{display:flex;gap:10px;align-items:baseline;padding:8px 0;border-top:1px dashed #F0DDD4;font-size:17px;color:#6E4A3C}
.pen-list .d{color:#A8887A;font-size:13px;flex:0 0 auto}
.pen-list .v{color:#B0563F;flex:0 0 auto}
.pen-list .r{flex:1;line-height:1.6}
.pen-list .r.none{color:#C4A99C}
.pz{display:inline-flex;align-items:center;vertical-align:middle;margin:0 .14em 0 0}
.pz .h{font-size:1em;line-height:1.25}
.pz .y{display:inline-flex;flex-direction:column;justify-content:center;margin-left:.06em}
.pz .y i{font-style:normal;font-size:.42em;line-height:1.15;color:#A8887A;text-align:center;font-family:'Huninn',system-ui,sans-serif}
.pz .t{font-size:.46em;color:#A8887A;align-self:center;line-height:1;font-family:'Huninn',system-ui,sans-serif}
"""

PEN_HTML = """
<div class="card pen-box" id="pen-box" hidden>
  <div class="pen-title" id="pen-title">&#9888;&#65039; 扣分紀錄</div>
  <div class="pen-note" id="pen-note">每一筆：閱讀、牛奶、跳繩三本各扣 10 分</div>
  <ul class="pen-list" id="pen-list"></ul>
</div>
"""

PEN_JS = """
window.PenaltyWidget = (function () {
  'use strict';
  var API = '__API__', items = null, reasons = null, ZY = null;
  function esc(t) { return String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function zyHtml(zy) {
    var last = zy.slice(-1), tone = 'ˊˇˋ'.indexOf(last) >= 0 ? last : '', light = last === '˙';
    var syms = (tone || light) ? zy.slice(0, -1) : zy, col = light ? '<i>˙</i>' : '';
    for (var i = 0; i < syms.length; i++) col += '<i>' + syms[i] + '</i>';
    return '<span class="y">' + col + '</span>' + (tone ? '<span class="t">' + tone + '</span>' : '');
  }
  function ruby(text) {
    var out = '';
    for (var ch of String(text)) out += (ZY && ZY[ch]) ? '<span class="pz"><span class="h">' + esc(ch) + '</span>' + zyHtml(ZY[ch]) + '</span>' : esc(ch);
    return out;
  }
  function reasonOf(id) {
    try { var v = JSON.parse((reasons && reasons[id]) || 'null'); return (v && v.reason) ? String(v.reason) : ''; } catch (e) { return ''; }
  }
  function render() {
    var box = document.getElementById('pen-box'); if (!box) return;
    if (!items || !items.length) { box.hidden = true; return; }
    box.hidden = false;
    document.getElementById('pen-title').innerHTML = '&#9888;&#65039; ' + ruby('扣分紀錄');
    document.getElementById('pen-note').innerHTML = ruby('每一筆：閱讀、牛奶、跳繩三本各扣 10 分');
    var rows = items.slice().sort(function (a, b) { return a.date < b.date ? 1 : a.date > b.date ? -1 : 0; }).map(function (e) {
      var r = reasonOf(e.id);
      return '<li><span class="d">' + esc(e.date) + '</span><span class="v">−' + esc(e.value) + '</span>' +
        (r ? '<span class="r">' + ruby(r) + '</span>' : '<span class="r none">' + ruby('（未填原因）') + '</span>') + '</li>';
    });
    document.getElementById('pen-list').innerHTML = rows.join('');
  }
  fetch('../assets/zhuyin.json').then(function (r) { return r.ok ? r.json() : null; })
    .then(function (m) { if (m) { ZY = m; render(); } }).catch(function (e) { console.error('zhuyin load failed', e); });
  fetch(API + '?mode=kv&sheet=kv_penalty', { cache: 'no-store' }).then(function (r) { return r.json(); })
    .then(function (j) { if (j && j.ok && j.items && typeof j.items === 'object') { reasons = j.items; render(); } })
    .catch(function (e) { console.warn('penalty reasons fetch failed', e); });
  return { setItems: function (list) { items = Array.isArray(list) ? list : []; render(); } };
})();
"""


def penalty_js(api_url):
    return PEN_JS.replace("__API__", api_url)
