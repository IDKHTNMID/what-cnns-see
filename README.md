# CNN 看到什麼

這是一份關於卷積神經網路（CNN）可解釋性的 LLM Wiki，以及只用這份 Wiki 做成的教學簡報。簡報從卷積的基礎講起，帶不熟 CNN 的人看懂網路在一個神經元、一張圖和一整層分別看到什麼。

## 成果

| 內容 | 位置 |
|---|---|
| 教學 HTML 簡報（13 頁） | [線上簡報](https://idkhtnmid.github.io/what-cnns-see/deck/)（原始檔：[deck/index.html](deck/index.html)） |
| LLM Wiki（31 頁、名詞表 125 條） | [wiki/index.md](wiki/index.md) |
| 流程圖與流程說明 | [deck/workflow.md](deck/workflow.md) |
| 一次實際執行的紀錄與反思 | [deck/reports/run-report.md](deck/reports/run-report.md) |
| 忠實度審查 | [紀錄](deck/reports/faithfulness.md)、[考題與回覆](deck/reports/faithfulness-exam.md) |
| 需求摘要 | [需求摘要.md](需求摘要.md) |
| 給 AI 的維護規則 | [AGENTS.md](AGENTS.md) |

## 資料夾

```text
raw/       原始來源，加入後不修改
wiki/      來源摘要、概念、方法、名詞表、目錄和紀錄
deck/      大綱、逐頁稿、樣板、簡報和檢查報告
scripts/   Wiki 與簡報的檢查、組裝程式
tests/     簡報程式的測試
reports/   Wiki 每次檢查的結果
```

## 和 Karpathy 原版不一樣的地方

這份 Wiki 照 Karpathy 的 LLM Wiki 模式維護，並依這次的需求調整：

- 多了方法頁和名詞表，不做實體頁，比較表寫進方法頁或概念頁。
- 為了讓不熟的人看懂簡報，加入兩份基礎來源，並把基礎排在最前面。
- 出處標到小節，關鍵說法附英文原文句，並用程式到 `raw/` 核對。
- 說法不同時，兩種都寫出來，再挑一個主流說法當主軸。
- 簡報視為對 Wiki 的一次查詢，每句畫面文字都要對應一句 Wiki 原句。

完整對照見[需求摘要第四節](需求摘要.md#四和-karpathy-原版不一樣的地方)。

## 來源

| 標題 | 作者 | 年份 | 授權 |
|---|---|---|---|
| [Dive into Deep Learning, Sections 1.1–1.2, 2.4, 3.1 and 5.1](https://d2l.ai/) | Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola | 2023 | CC BY-SA 4.0 |
| [Dive into Deep Learning, Chapter 7 (Sections 7.1–7.5)](https://d2l.ai/chapter_convolutional-neural-networks/) | Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola | 2023 | CC BY-SA 4.0 |
| [Computing Receptive Fields of Convolutional Neural Networks](https://distill.pub/2019/computing-receptive-fields/) | André Araujo, Wade Norris, Jack Sim | 2019 | CC BY 4.0 |
| [Feature Visualization](https://distill.pub/2017/feature-visualization/) | Chris Olah, Alexander Mordvintsev, Ludwig Schubert | 2017 | CC BY 4.0 |
| [Deconvolution and Checkerboard Artifacts](https://distill.pub/2016/deconv-checkerboard/) | Augustus Odena, Vincent Dumoulin, Chris Olah | 2016 | CC BY 2.0 |
| [The Building Blocks of Interpretability](https://distill.pub/2018/building-blocks/) | Chris Olah, Arvind Satyanarayan, Ian Johnson, Shan Carter, Ludwig Schubert, Katherine Ye, Alexander Mordvintsev | 2018 | CC BY 4.0 |
| [Exploring Neural Networks with Activation Atlases](https://distill.pub/2019/activation-atlas/) | Shan Carter, Zan Armstrong, Ludwig Schubert, Ian Johnson, Chris Olah | 2019 | CC BY 4.0 |

每篇的下載日期、截圖和未收錄的圖，都記在 [raw/SOURCES.md](raw/SOURCES.md)。

## 授權

`wiki/` 和 `deck/` 的內容以 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 釋出。`raw/` 的檔案和簡報用到的圖片各自保留原本的授權，見 [LICENSE](LICENSE)。
