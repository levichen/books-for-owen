---
name: social-story-writer
description: 把一個兒童行為目標轉成社會故事繪本的 story-spec.md（頁面計畫＋英文文案）。觸發條件：使用者要做新繪本、說「新書」「new book」、從 backlog 挑行為主題、或要求撰寫/修改 story spec。輸出到 books/<slug>/story-spec.md，不做插圖與渲染。
---

# Social Story Writer

## 你在做什麼

社會故事（Carol Gray 方法）不是講道理，是替孩子**安裝一套當下用得出來的動作腳本**。
先讀 `context/owen.md` 取得孩子檔案、既有口訣、行為 backlog。

## 十頁固定骨架（cover 與家長頁另計）

| 頁 | 功能 | 規則 |
|---|---|---|
| p1 | 自我介紹 | 正向開場，帶名字 "This is me, Owen!" |
| p2 | 情境 | 行為發生的場景（教室/隊伍/早晨…） |
| p3 | 觸發 | 興奮/衝動被點燃的瞬間 |
| p4 | **衝動頁（全書核心）** | 用具體**身體感覺**描述衝動（itchy mouth、hot body、boom-boom heart）。無法辨識的衝動就無法抑制——這頁是整個介入的第一步 |
| p5 | 超能力宣告 | 命名策略（存進 brain pocket 之類的具象隱喻） |
| p6 | 動作腳本 | 2–3 個可執行動作（close mouth → count 123 → hand up HIGH） |
| p7 | 觀點頁 | 同儕視角**只佔這一頁**，放動機層，不當主軸 |
| p8 | 成功時刻 | 帶入真實人物（Tr. Mina says, "Yes, Owen!"）——預演教室場景 |
| p9 | 結果與感受 | I feel GREAT! |
| p10 | 口訣總結 | 3 步口訣，登記進 owen.md 詞彙表 |

## 文案硬規則

- 每句 ≤ 8 個英文字；kindergarten sight words 為主，全書新生字 ≤ 3 個
- 第一人稱（社會故事標準）；名字出現在 p1、p8
- 描述句＋觀點句 : 指令句 ≥ 2:1（Carol Gray 比例——指令句太多會變說教）
- 口訣必須 ≤ 3 個詞、可喊、可當老師暗號（如 "Save it!"）

## story-spec.md 格式（books/<slug>/story-spec.md）

```markdown
# Book: <slug>
- behavior_target: <一句話，只能一個行為>
- cue_phrase: "<口訣>"
- new_vocabulary: [<超出 sight words 的字，≤3>]

## Pages
| id | scene 描述（給插圖用） | text（含 <b> 標記） |
| p1 | Owen 背書包走路上學 | This is me, <b>Owen</b>!<br/>... |
...

## Parent page notes
<本書特有的提醒，若無寫「標準六條」>
```

## 完成後

1. 更新 `context/owen.md` 口訣詞彙表（狀態：草稿）
2. 呼叫 **story-reviewer** subagent 審稿；未通過不得進入插圖階段
3. 參考範例：`books/save-my-answer/story-spec.md`
