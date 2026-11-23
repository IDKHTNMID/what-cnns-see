# 簡報大綱：CNN 看到什麼（極簡核心版）

目標：只用 `wiki/` 的內容，用最少的文字和最清楚的單一主線，帶不熟 CNN 的人看懂網路怎麼看圖，以及怎麼看出它在一個神經元、一張圖、一整層分別看到什麼。共 13 頁，一頁只講一件事；學過 CNN 的人可以從第 5 頁開始。

---

## 第 1 頁：CNN 到底看到什麼？

- 段落：開始之前
- Wiki：`concepts/layer-abstraction.md`、`concepts/convolutional-layer.md`、`glossary.md`
- 圖：無（5 站章節卡片與跳讀連結）
- 地圖位置：全部

## 第 2 頁：看一張圖，為什麼不把每個像素都接起來？

- 段落：CNN 基礎
- Wiki：`concepts/neural-network-basics.md`、`concepts/convolutional-layer.md`、`concepts/translation-invariance.md`、`concepts/locality.md`、`glossary.md`
- 圖：`raw/d2l-basics/_images/mlp.svg`
- 地圖位置：影像 → 低層

## 第 3 頁：只看一小塊窗口，實際怎麼算？

- 段落：CNN 基礎
- Wiki：`methods/convolution-operation.md`、`concepts/convolutional-layer.md`、`glossary.md`
- 圖：無（5 步卷積計算與邊緣偵測互動）
- 地圖位置：影像 → 低層

## 第 4 頁：一層只看一小塊，後面怎麼看得到更大範圍？

- 段落：CNN 基礎
- Wiki：`concepts/receptive-field.md`、`methods/receptive-field-computation.md`
- 圖：`raw/screenshots/computing-receptive-fields/fig05.png`
- 地圖位置：低層 → 高層

## 第 5 頁：知道怎麼算了，怎麼看一個神經元在找什麼？

- 段落：看神經元
- Wiki：`methods/feature-visualization.md`、`methods/gradient-descent.md`、`sources/feature-visualization.md`、`glossary.md`
- 圖：`raw/screenshots/feature-visualization/fig03.png`
- 地圖位置：中層

## 第 6 頁：直接調整輸入影像，為什麼只得到雜訊？

- 段落：看神經元
- Wiki：`methods/regularization-and-preconditioning.md`、`sources/feature-visualization.md`、`glossary.md`
- 圖：`raw/screenshots/feature-visualization/fig20.png`、`raw/screenshots/feature-visualization/fig30.png`
- 地圖位置：中層

## 第 7 頁：加上限制後，從低層到高層分別看到什麼？

- 段落：看神經元
- Wiki：`concepts/layer-abstraction.md`、`concepts/channel.md`
- 圖：`raw/screenshots/feature-visualization/fig00.png`
- 地圖位置：低層 → 高層

## 第 8 頁：但一個神經元只看一種東西嗎？

- 段落：看神經元
- Wiki：`methods/feature-visualization.md`、`concepts/semantic-dictionary.md`、`concepts/activation-space.md`
- 圖：`raw/feature-visualization/images/diversity/mixed4e_55_diversity.png`
- 地圖位置：高層

## 第 9 頁：換看一張真實照片：每個位置看到什麼？

- 段落：看一張圖
- Wiki：`methods/activation-grid.md`、`concepts/feature-map.md`
- 圖：`raw/screenshots/building-blocks/fig06.png`
- 地圖位置：低層 → 高層

## 第 10 頁：看到這些之後，網路靠什麼做出分類決定？

- 段落：看一張圖
- Wiki：`methods/attribution.md`、`methods/matrix-factorization.md`、`glossary.md`
- 圖：無（3 格歸因公式圖；附原文連結）
- 地圖位置：高層 → 類別機率

## 第 11 頁：擴大到大量照片：一整層能表示哪些概念？

- 段落：看一整層
- Wiki：`sources/activation-atlas.md`、`methods/activation-atlas.md`、`concepts/layer-abstraction.md`
- 圖：`raw/activation-atlas/assets/images/renders/focus-1-1.jpg`、`raw/activation-atlas/assets/images/renders/focus-2-1.jpg`
- 地圖位置：中層 → 高層

## 第 12 頁：看懂這些概念之後，能改變它的分類嗎？

- 段落：看一整層
- Wiki：`concepts/multi-use-features.md`、`sources/activation-atlas.md`、`glossary.md`
- 圖：無（補丁流程圖；附原文連結）
- 地圖位置：全部

## 第 13 頁：最後一問：這些解釋能信到什麼程度？

- 段落：能信多少
- Wiki：`sources/building-blocks.md`、`sources/feature-visualization.md`、`sources/activation-atlas.md`、`glossary.md`
- 圖：無（三張限制卡）
- 地圖位置：全部
