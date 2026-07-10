---
description: 渲染指定書籍為 PDF + 網站（含目視驗證）
---
使用 book-renderer skill 渲染：$ARGUMENTS

1. cd src && python3 render_pdf.py && python3 render_site.py
2. pdftoppm 逐頁轉圖目視驗證（重點：落地、遮擋、表情符合 spec、家長頁無缺字）
3. PDF 移到 dist/，回報產物路徑與發現的問題
