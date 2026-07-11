# Owen 檔案

## 基本

- Owen，6 歲（2026），全美幼兒園三年 → 可自行朗讀 kindergarten sight words
- 老師：Tr. Mina
- 卡通角色辨識特徵（parts.py 已實作，勿改）：圓黑框眼鏡＋橘色鏡腳、齊瀏海黑髮、
  白色小士兵圖案 T-shirt、紅色書包（灰背帶＋深藍底）、深色迷彩短褲
- 運動場景服裝例外（2026-07 議定）：球場頁可穿球衣蓋掉白 T——籃球 **39 號**、棒球 **100 號**、
  足球 **0 號**；背號本身即辨識元素；眼鏡＋瀏海＋短褲仍不變，開場/學校頁維持白 T
- 匹克球（magic-words）無背號需求，全書白 T＋球拍
- 家規（2026-07 議定）：早上 **6:30** 才能叫媽媽起床（Owen 會看時鐘，數字鐘顯示 6:30 為準）

## 跨書角色（2026-07 登記；**全部是 Owen 生活中的真實人物**，僅卡通化呈現）

- 媽媽 **April**（wait-my-spot、one-more-try 場邊；quiet-morning、statue-time、my-cup-only 主角級配角）
- 爸爸 **Daddy**（freeze-and-look 帶足球練習＋吹哨）
- 朋友 **Lucas**、朋友 **Ann**（wait-my-spot 隊友；Lucas 亦為 freeze-and-look 隊友）
- 同學 **Ethan**（eyes-on-teacher；不小心碰到 Owen 的好朋友，非壞人設定）
- 老師 **Tr. Mina**（save-my-answer、eyes-on-teacher）

## 行為模型（教養診斷結論，2026-07）

- 服從能力完整（爸爸在場時 100%）→ 問題是**指令可信度**與**衝動抑制發展**，不是態度
- 加壓（罵、體罰）已驗證無效 → 介入走「技能安裝」路線：辨識衝動訊號 → 動作腳本
- 關鍵身體訊號詞：**"My mouth feels itchy"** = 他察覺到衝動了，出現即大力稱讚

## 口訣詞彙表（跨書共用，老師/家長/聯絡卡統一用詞）

| 口訣 | 行為 | 書 | 狀態 |
|---|---|---|---|
| Hand up → Wait → **Save it!** | 上課搶答 | save-my-answer | 已出版 |
| Glue → Cheer → **Wait my spot!** | 插隊／排隊心急 | wait-my-spot | 已出版 |
| Big breath → Keep playing → **One more try!** | 輸贏焦慮／賴皮 | one-more-try | 已出版 |
| Check my clock → Play quiet → **Wait for 6:30!** | 清晨吵醒媽媽 | quiet-morning | 已出版 |
| Catch my brain → Play later → **Eyes on teacher!** | 上課分心 | eyes-on-teacher | 已出版 |
| Freeze → Look → **Listen!**（喊法：Freeze and look!） | 玩太 high 聽不進勸 | freeze-and-look | 已出版 |
| Feet down → Hands on knees → **Statue time!** | 照護時間亂動（吹髮/洗澡/刷牙） | statue-time | 已出版 |
| Stop → Find my name → **My cup only!** | 喝別人的杯子 | my-cup-only | 已出版 |
| Please → Thank you → Sorry（喊法：**Magic words!**） | 忘記禮貌語 | magic-words | 草稿 |
| One at a time → Point and check → **Slow and check!** | 珠心算趕寫錯多 | slow-and-check | 草稿 |
| Check my volume → Pick two → **Volume down!** | 室內聲音動作太大 | volume-down | 草稿 |

對應身體訊號詞（出現即大力稱讚）：itchy mouth（搶答）、jumpy feet（插隊）、hot face + tight tummy（怕輸）、
body wants to bounce（清晨）、my brain ran away（分心）、wind fills my ears（玩太 high）、
body feels wiggly（照護亂動）、"Whose bottle is this?"（拿杯前先問）、
my magic words hide（忘禮貌）、my pencil zooms + heart goes fast（趕寫）、my voice grows big + body feels buzzy（太大聲）

口訣區隔備忘：**Freeze**（被叫到瞬間停）vs **Statue**（照護期間持續不動）vs **Volume down**（自己發現太大聲、轉小）
是三顆不同的肌肉——外部開關／持續靜止／自我監控，不可混用。

**已習得詞彙**（已出版書籍教過，跨書重用不計入該書新字上限）：itchy、superpower、pocket（save-my-answer）；
jumpy、glue、cheer（wait-my-spot）；strike、quit、home run（one-more-try）；
bounce、tiptoe、whisper（quiet-morning）；puppy、giggle、catch（eyes-on-teacher）；freeze、whistle（freeze-and-look）；
wiggly、statue、dryer（statue-time）；thirsty、germs、bottle（my-cup-only）。
其中 **superpower** 是系列固定儀式詞——每本 p5 都用 "STOP! I use my superpower&hellip;" 開場，刻意跨書重複。
新書出版後，其 new_vocabulary 併入此清單。

## 行為主題 backlog（下一本書從這裡挑）

（目前清空。已出 backlog：插隊→wait-my-spot、玩太high→freeze-and-look、早上5:30→quiet-morning、
吹頭髮亂動→statue-time、喝別人杯子→my-cup-only，均 2026-07）

## 出版原則

- 每本書封面留 "This book belongs to ______"（PDF 版）給 Owen 手寫——所有權儀式
- 家長頁固定六條使用規則，第 2 條永遠是：**出事後絕對不拿出來讀**
