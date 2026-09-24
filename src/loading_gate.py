# -*- coding: utf-8 -*-
"""載入遮罩（點數區四頁共用）：開頁先蓋住整頁，等第一次雲端讀取結束才放行，
避免使用者在舊資料上操作（重複記、撤銷錯筆）。

頁面 JS 在第一次同步結束時呼叫 window.LoadingGate.done()（成功、失敗、離線都要呼叫，
狀態交給頁面自己的狀態列說明）。保險：25 秒沒人呼叫就自動放行，避免離線時卡死。"""

GATE_CSS = """
/* --- 載入遮罩 --- */
#load-gate{position:fixed;inset:0;z-index:999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;
  background:rgba(255,255,255,.94);color:#6E5A50;font-size:17px;text-align:center;padding:24px;transition:opacity .25s}
#load-gate.hide{opacity:0;pointer-events:none}
#load-gate .spin{width:46px;height:46px;border-radius:50%;border:5px solid #E8E0F5;border-top-color:#6C4DD6;animation:lg-spin .9s linear infinite}
#load-gate .sub{font-size:13px;color:#A8988F}
@keyframes lg-spin{to{transform:rotate(360deg)}}
"""

GATE_HTML = """<div id="load-gate" aria-busy="true"><div class="spin"></div><div>&#9729;&#65039; 正在讀取雲端紀錄&hellip;</div><div class="sub">讀完才能操作，避免重複記錄</div></div>"""

GATE_JS = """
window.LoadingGate = (function () {
  'use strict';
  var el = document.getElementById('load-gate'), doneFlag = false;
  function done() {
    if (doneFlag || !el) return;
    doneFlag = true;
    el.classList.add('hide');
    setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 300);
  }
  setTimeout(done, 25000);  // 保險：離線或後端卡住時不要永遠鎖住
  return { done: done };
})();
"""
