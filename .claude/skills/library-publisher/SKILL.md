---
name: library-publisher
description: 把 site/ 發佈到 GitHub Pages。觸發條件：使用者說 publish、部署、上線、push 網站、開 Pages。使用本機既有 git/gh 憑證，絕不在對話中要求 token。
---

# Library Publisher

架構：整個 workshop 是單一 repo（`books-for-owen`，main branch），
GitHub Pages 從 `gh-pages` branch 供站，內容 = `site/` 的 subtree split。
站台網址：https://levichen.github.io/books-for-owen/

## 首次部署（已於 2026-07-10 完成，留作參考）

```bash
# repo 根目錄
git init -b main && git add -A && git commit -m "feat: ..."
gh repo create books-for-owen --public --source=. --push
git subtree split --prefix site -b gh-pages && git push origin gh-pages
gh api -X POST repos/{owner}/books-for-owen/pages -f "source[branch]=gh-pages" -f "source[path]=/" || true
```

## 日常更新（新書上架）

```bash
cd src && python3 render_site.py
cd .. && git add -A && git commit -m "feat: add <slug>" && git push origin main
# 重新切 gh-pages 並強推（subtree split 的 history 不連續，force 是預期行為）
git branch -D gh-pages 2>/dev/null; git subtree split --prefix site -b gh-pages
git push -f origin gh-pages
```

## 發佈前檢核

- [ ] 兩個 index.html 都還有 `<meta name="robots" content="noindex">`
- [ ] 站內只有名字、無姓氏、無照片（隱私原則見 CLAUDE.md）
- [ ] 新中文字已重新子集化（家長頁目視無豆腐字）
- [ ] reader 在手機寬度（~380px）翻頁正常

## 憑證原則

一律用本機已登入的 `gh auth` / git credential helper。
若未登入：請使用者自己跑 `gh auth login`（device flow），不代跑、不收 token。
