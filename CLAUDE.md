# Owen's Books Workshop

替 Owen 製作「社會故事繪本」的生產線。一本書 = 一個行為目標 = spec → 插圖 → 渲染 → 出版。

## Pipeline

```
/new-book  →  books/<slug>/story-spec.md   (social-story-writer skill)
           →  story-reviewer subagent 審稿通過
           →  場景實作 src/render_pdf.py    (picture-book-illustrator skill)
/render    →  dist/<slug>.pdf + site/books/<slug>/  (book-renderer skill)
/publish   →  git push → GitHub Pages       (library-publisher skill)
```

## 不可違反的原則

1. **一本書只處理一個行為**。想塞第二個行為 = 開新書。
2. **文案是 kindergarten sight words**：每句 ≤ 8 個字，全書生字 ≤ 3 個。
3. **角色一致性只來自 `src/parts.py`**。禁止在場景裡手畫 Owen——新姿勢/表情就擴充 parts.py 的 API。
4. **口訣詞彙表在 `context/owen.md`**，跨書共用（如 "Save it!"）。新書的口訣要先登記再使用。
5. **審稿是硬門檻**：story-spec 未經 story-reviewer 通過，不進入插圖階段。
6. **隱私**：只用名字不用姓氏，站台保持 `noindex`，不放照片。

## 環境

```bash
pip install -r requirements.txt
./setup_font.sh          # 下載 OFL 授權的 jf-openhuninn 字型（一次）
cd src && python3 render_pdf.py && python3 render_site.py
```

字型路徑可用環境變數 `HUNINN_TTF` 覆寫。

## 目錄

- `context/owen.md` — Owen 檔案＋行為主題 backlog（下一本書從這裡挑）
- `books/<slug>/story-spec.md` — 每本書的唯一真相來源
- `src/` — 角色引擎與雙渲染器（單一內容源：PDF 給列印、HTML 給網站）
- `site/` — GitHub Pages 產出（index.html 是書架）
- `dist/` — PDF 輸出（gitignore）

## 常見坑（都踩過了）

- weasyprint 不支援 SVG `filter` / `mask` / `clipPath`——用形狀疊加假裝。
- 舉手的手臂要畫在頭**之後**，且弧線外推避開臉（見 parts.py `handup`）。
- 人物落地公式：`feet_y = cy + 228 × scale`（stand/handup/hips 姿勢）。
- 網站字型必須子集化（4.5MB → ~54KB），新書加了新中文字要重跑 render_site.py。
