# 名詞表

| 主名詞 | 英文 | 別名 | 一句話解釋 | 出處 | 用語依據 |
|---|---|---|---|---|---|
| 卷積 | convolution | 互相關（cross-correlation） | 卷積層實際做的運算：窗口滑過輸入，窗口內逐元素相乘再加總 | （[d2l](sources/d2l-ch7.md) § 7.2.1. The Cross-Correlation Operation） | d2l 說明照深度學習的慣例把互相關叫卷積（[d2l](sources/d2l-ch7.md) § 7.2.5. Cross-Correlation and Convolution） |
| 嚴格卷積 | strict convolution | — | 數學上的卷積：先把卷積核上下、左右翻轉，再做互相關 | （[d2l](sources/d2l-ch7.md) § 7.2.5. Cross-Correlation and Convolution） | 只有一種叫法；只在說明名稱由來時使用 |
| 卷積層 | convolutional layer | — | 把輸入和卷積核做卷積、再加純量偏置的層 | （[d2l](sources/d2l-ch7.md) § 7.2.2. Convolutional Layers） | 只有一種叫法 |
| 卷積神經網路 | convolutional neural network（CNN） | — | 含有卷積層的神經網路 | （[d2l](sources/d2l-ch7.md) § 7.1.2.2. Locality） | 只有一種叫法 |
| 卷積核 | kernel | 濾波器（filter）、權重（weights） | 卷積層裡可學習的權重張量 | （[d2l](sources/d2l-ch7.md) § 7.1.2.2. Locality） | d2l 三種叫法並列（[d2l](sources/d2l-ch7.md) § 7.1.2.2. Locality）；小節標題用 kernel（[d2l](sources/d2l-ch7.md) § 7.2.4. Learning a Kernel） |
| 卷積窗口 | convolution window | kernel window | 卷積核在輸入上蓋住的範圍，形狀等於卷積核的高寬 | （[d2l](sources/d2l-ch7.md) § 7.2.1. The Cross-Correlation Operation） | d2l 兩個名稱並列，說明滑動步驟時用 convolution window（[d2l](sources/d2l-ch7.md) § 7.2.1. The Cross-Correlation Operation；[d2l](sources/d2l-ch7.md) § 7.3.2. Stride） |
| 通道 | channel | — | 一層表示沿通道維度切出的一張二維格子 | （[d2l](sources/d2l-ch7.md) § 7.1.4. Channels） | d2l 也把單一通道叫 feature map；本 Wiki 的特徵圖只指一層的整個輸出（[d2l](sources/d2l-ch7.md) § 7.1.4. Channels） |
| 通道維度 | channel dimension | — | 張量裡代表通道的那個軸，RGB 影像的大小是 3 | （[d2l](sources/d2l-ch7.md) § 7.4. Multiple Input and Multiple Output Channels） | 只有一種叫法 |
| 特徵圖 | feature map | — | 一層卷積層的整個輸出 | （[d2l](sources/d2l-ch7.md) § 7.2.6. Feature Map and Receptive Field） | 依 d2l 7.2.6 節的用法（[d2l](sources/d2l-ch7.md) § 7.2.6. Feature Map and Receptive Field） |
| 感受野 | receptive field | — | 前向傳播中可能影響某個元素的所有前層元素 | （[d2l](sources/d2l-ch7.md) § 7.2.6. Feature Map and Receptive Field） | 只有一種叫法 |
| 平移不變性 | translation invariance | 平移等變性（translation equivariance） | 早期層對同一塊圖案，不管它在哪裡都有相似的反應 | （[d2l](sources/d2l-ch7.md) § 7.1.1. Invariance） | d2l 原文把兩個名稱並列（[d2l](sources/d2l-ch7.md) § 7.1.1. Invariance）；推導的小節標題和總結都用 translation invariance（[d2l](sources/d2l-ch7.md) § 7.1.2.1. Translation Invariance；[d2l](sources/d2l-ch7.md) § 7.1.5. Summary and Discussion） |
| 局部性 | locality | — | 早期層只看局部區域，不管遠處的內容 | （[d2l](sources/d2l-ch7.md) § 7.1.1. Invariance） | 只有一種叫法 |
| 歸納偏置 | inductive bias | — | 學習時加在模型上的預設，例如平移不變性和局部性 | （[d2l](sources/d2l-ch7.md) § 7.1.2.2. Locality） | 只有一種叫法 |
| 填充 | padding | 零填充（zero-padding，補 0 的填充） | 在輸入邊界外補額外的像素，通常補 0 | （[d2l](sources/d2l-ch7.md) § 7.3.1. Padding） | 只有一種叫法 |
| 步幅 | stride | — | 窗口每次滑動跨過的列數和行數 | （[d2l](sources/d2l-ch7.md) § 7.3.2. Stride） | 只有一種叫法 |
| 1×1 卷積 | 1×1 convolution | — | 卷積核高寬都是 1、只在通道維度上計算的卷積 | （[d2l](sources/d2l-ch7.md) § 7.4.3. 1×1 Convolutional Layer） | 只有一種叫法 |
| 池化 | pooling | — | 用固定窗口取最大值或平均值、沒有參數的運算 | （[d2l](sources/d2l-ch7.md) § 7.5.1. Maximum Pooling and Average Pooling） | 只有一種叫法 |
| 池化窗口 | pooling window | — | 池化時滑過輸入的固定形狀窗口 | （[d2l](sources/d2l-ch7.md) § 7.5.1. Maximum Pooling and Average Pooling） | 只有一種叫法 |
| 最大池化 | max-pooling | maximum pooling | 取池化窗口內的最大值 | （[d2l](sources/d2l-ch7.md) § 7.5.1. Maximum Pooling and Average Pooling） | d2l 說 maximum pooling 簡稱 max-pooling（[d2l](sources/d2l-ch7.md) § 7.5.1. Maximum Pooling and Average Pooling），結論也用 max-pooling（[d2l](sources/d2l-ch7.md) § 7.5.4. Summary） |
| 平均池化 | average pooling | — | 取池化窗口內的平均值 | （[d2l](sources/d2l-ch7.md) § 7.5.1. Maximum Pooling and Average Pooling） | 只有一種叫法 |
