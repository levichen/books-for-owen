---
name: book-renderer
description: 把完成插圖的書渲染成兩種產物：可列印 PDF（A4 橫式）與自包含 HTML reader（含網站書架更新、字型子集化）。觸發條件：使用者說 render、出書、產 PDF、更新網站、字型問題。
---

# Book Renderer

單一內容源、雙渲染器。內容真相在 `src/render_pdf.py` 的 `PAGES` / 場景函式 / `PARENT_TIPS`。

## 執行

```bash
cd src
python3 render_pdf.py     # → I_Can_Save_My_Answer.pdf（A4 橫式 12 頁）
python3 render_site.py    # → ../site/（reader + 書架 + 子集化 woff2）
```

## PDF 要點

- @page 297×210mm 零邊距；字型 jf-openhuninn（`HUNINN_TTF` 環境變數可覆寫路徑）
- 版式：上 140mm 插圖區＋下 50mm 白底圓角文字帶；家長頁走獨立版型
- 驗證：`pdftoppm -png -r 50` 逐頁目視，重點頁：衝動頁、舉手頁、封面

## Site 要點

- reader 是單檔自包含 HTML（SVG 內嵌），翻頁支援按鈕/方向鍵/滑動
- **字型子集化**：pyftsubset 收集全站 unique chars → woff2（4.5MB → ~54KB）。
  新書加了新中文字**必須**重跑，否則家長頁缺字
- 兩頁都有 `noindex`，不要拿掉
- 新書 = site/books/<slug>/index.html + 書架 index.html 加一張書卡

## 新書接入清單

1. render_pdf.py：新增場景函式＋PAGES 清單（或抽成 per-book module，書多再重構）
2. render_site.py：BOOK_SLUG/標題常數 → 產出新資料夾
3. 跑兩個 renderer → 目視驗證 → PDF 放 dist/
