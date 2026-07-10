# Owen's Little Library

專屬 Owen 的繪本書架（GitHub Pages 靜態站）。

## 部署
1. 建一個 repo（例如 `owen-books`），把本資料夾內容推上 `main`。
2. Repo Settings → Pages → Source: Deploy from a branch → `main` / `(root)` → Save。
3. 網址：`https://<username>.github.io/owen-books/`

## 新增一本書
1. 複製 `books/save-my-answer/` 成新資料夾（一本書 = 一個自包含的 index.html）。
2. 在根目錄 `index.html` 的 `.grid` 內加一張書卡。
3. 若新書用到新的中文字，重新子集化 `assets/huninn.woff2`（fonttools pyftsubset）。

> 注意：GitHub Pages 免費方案為公開網站。本站已加 `noindex`（不進搜尋引擎），但知道網址的人都能開啟。
