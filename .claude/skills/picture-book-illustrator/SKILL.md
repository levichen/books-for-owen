---
name: picture-book-illustrator
description: 把 story-spec.md 的場景描述實作成 SVG 場景函式（scene_pN）。觸發條件：story spec 已審稿通過需要插圖、新增/修改繪本場景、擴充角色姿勢或表情。只能透過 src/parts.py 的 API 畫 Owen，禁止手畫角色。
---

# Picture Book Illustrator

## 角色引擎 API（src/parts.py）

Owen 只能用這些函式生成——一致性是這條 pipeline 的命：

```python
boy(pose, expr, cx, cy, scale, backpack=False, cape=False)
  # pose: stand | walk | handup | hips | wave
boy_bust(expr, cx, cy, scale, arms="desk"|"handup")   # 桌前半身
head(expr)   # expr: smile | big | star | hold | press | proud | oh | think
teacher(cx, cy, scale, point="right"|"left")           # Tr. Mina
kid(variant=0..2, expr="think"|"smile")                # 同學（無眼鏡，好區分）
desk(cx, cy, w) / brain_pocket(open_flap, glow) / star(face=) / sparkle / cloud / sun
```

表情語意：`hold`=鼓臉閉眼憋住（衝動頁）、`press`=抿嘴堅定（執行腳本頁，
來自 Owen 本人照片的嘟嘴表情）、`star`=星星眼（興奮）、`big`=開口大笑。

## 場景組裝規則

- 場景 viewBox 統一 `0 0 1188 560`（封面 1188×620）
- **落地公式**：站姿 `feet_y = cy + 228 × scale`；半身桌前 `bust_bottom = cy + 110 × scale`，
  應略低於桌面 y 再讓桌子疊在前面
- 一頁一個視覺焦點；配角縮小放邊緣；星星/sparkle 點綴 ≤ 6 個
- 頁面底色用 render_pdf.py 的 `BG` palette，新頁配新柔和色
- SVG 內文字用 `svgtext()`（僅限短字：?、123、"Yes, Owen!" 這類）

## weasyprint 限制（會靜默壞掉，不會報錯）

- 不支援 `filter`、`mask`、`clipPath`、`foreignObject` —— 光暈用多層半透明圓假裝
- 漸層 OK、dasharray OK、transform OK

## 已知構圖陷阱

1. 舉高的手臂必須畫在 head **之後**，且弧線外推（`Q 98 24 76 -56`）避免劃過臉
2. 星星壓嘴時 wing 曲線放星星後面會被蓋住——可接受，別放大 wing
3. 新姿勢先在 parts.py 加 API 再用，不要在場景檔內聯人體

## 驗證流程（必做）

```bash
cd src && python3 render_pdf.py
pdftoppm -png -r 50 I_Can_Save_My_Answer.pdf /tmp/prev
# 逐頁目視：落地、遮擋、表情語意是否符合 spec
```
