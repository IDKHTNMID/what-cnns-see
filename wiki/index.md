# 目錄：CNN 看到什麼

## 基礎（學過 CNN 可跳過）

- [卷積層](concepts/convolutional-layer.md) — 從全連接層加上兩個原則推出卷積層，參數從 10¹² 降到 4Δ²
- [平移不變性](concepts/translation-invariance.md) — 同一塊圖案不管出現在哪裡，早期層的反應都相似
- [局部性](concepts/locality.md) — 早期層只看局部區域，代價是每個單元只用到局部資訊
- [通道](concepts/channel.md) — 每個位置對應一個向量；通道不一定一對一對應某種特徵
- [卷積運算](methods/convolution-operation.md) — 卷積窗口的滑動計算、多通道與 1×1 卷積
- [填充與步幅](methods/padding-and-stride.md) — 補 0 讓輸出不縮小，步幅用來降採樣；輸出大小公式
- [池化](methods/pooling.md) — 沒有參數的最大值或平均值匯總，用來降採樣並減輕對位置的敏感

## 概念

- [感受野](concepts/receptive-field.md) — 可能影響某個元素的所有前層元素，網路越深越大；感受野大小、區域與有效感受野

## 方法

- [感受野的計算](methods/receptive-field-computation.md) — 由各層的卷積核大小、步幅、填充算出感受野大小、區域與中心；多路徑網路要對齊

## 來源

- [d2l 第 7 章（7.1–7.5）](sources/d2l-ch7.md) — CNN 基礎：卷積層、填充與步幅、通道、池化
- [Computing Receptive Fields（2019）](sources/computing-receptive-fields.md) — 感受野大小與區域的閉式解、多路徑對齊、現代網路的感受野

## 名詞表

- [名詞表](glossary.md) — 術語的主名詞、別名、出處與用語依據
