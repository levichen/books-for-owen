---
name: library-publisher
description: 把 site/ 發佈到 GitHub Pages。觸發條件：使用者說 publish、部署、上線、push 網站、開 Pages。使用本機既有 git/gh 憑證，絕不在對話中要求 token。
---

# Library Publisher

## 首次部署

```bash
cd site
git init && git add -A && git commit -m "feat: Owen's little library"
gh repo create owen-books --public --source=. --push
gh api -X POST repos/{owner}/owen-books/pages -f "source[branch]=main" -f "source[path]=/" || true
# 或 repo Settings → Pages → main /(root)
echo "https://$(gh api user -q .login).github.io/owen-books/"
```

## 日常更新（新書上架）

```bash
cd src && python3 render_site.py
cd ../site && git add -A && git commit -m "feat: add <slug>" && git push
```

## 發佈前檢核

- [ ] 兩個 index.html 都還有 `<meta name="robots" content="noindex">`
- [ ] 站內只有名字、無姓氏、無照片（隱私原則見 CLAUDE.md）
- [ ] 新中文字已重新子集化（家長頁目視無豆腐字）
- [ ] reader 在手機寬度（~380px）翻頁正常

## 憑證原則

一律用本機已登入的 `gh auth` / git credential helper。
若未登入：請使用者自己跑 `gh auth login`（device flow），不代跑、不收 token。
