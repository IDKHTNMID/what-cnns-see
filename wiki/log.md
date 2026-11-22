# 紀錄

只往後加。每筆開頭用 `## [YYYY-MM-DD] 類型 | 標題`。

## [2026-11-22] setup | 建立 Wiki 結構

- 需求訪談 11 題、補問 2 題，需求摘要兩輪確認後定案（見 `需求摘要.md`）。
- 生成 `AGENTS.md`、`CLAUDE.md`、資料夾結構與檢查程式。
- 5 篇 Distill 原文已存進 `raw/`；d2l 第 7 章在第一篇 ingest 時下載。

## [2026-11-22] ingest | Dive into Deep Learning, Chapter 7 (Sections 7.1–7.5)

- 新增：`sources/d2l-ch7.md`；概念頁 `convolutional-layer`、`translation-invariance`、`locality`、`channel`、`receptive-field`；方法頁 `convolution-operation`、`padding-and-stride`、`pooling`。
- 更新：`index.md`（基礎區 7 頁、概念區 1 頁、來源區 1 頁）、`glossary.md`（20 個名詞）。
- 名詞決定（使用者已確認）：
  - 卷積為主名詞，互相關列為別名；d2l 說明照深度學習慣例把互相關叫卷積。嚴格卷積只在說明名稱由來時使用。
  - 卷積核為主名詞，濾波器、權重列為別名。
  - 通道指一張二維格子；特徵圖只指一層卷積層的整個輸出。d2l 7.1.4 節也把單一通道叫特徵圖，本 Wiki 不採用。
  - 平移不變性為主名詞，平移等變性照 d2l 原文列為別名。
  - 中文譯名：卷積、卷積核、通道、特徵圖、感受野、填充、步幅、池化、局部性。
- 感受野放在概念區，不放在可跳過的基礎區，因為下一篇 computing-receptive-fields 會擴充。
- 說法不一致：無（目前只有一篇來源）。
- 圖：d2l 自己畫的 7 張 SVG 全部使用；Waldo 照片與 Field (1987) 的圖只附原文連結。
- 檢查：第 1 輪通過。之後逐句對原文修了 2 處推論過頭的說法，再跑一次也通過。
- 檢查程式：`check_quotes.py` 的小節標題比對改成忽略 d2l 的 ¶ 後按鈕文字與行內數學（`\(1\times 1\)` 可寫成 `1×1`），並加了測試。
