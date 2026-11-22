# 平移不變性

## 是什麼

平移不變性（translation invariance）是 CNN 的第一個設計原則：網路最前面幾層對同一塊圖案，不管它出現在影像的哪裡，都要有相似的反應。d2l 在同一句裡也把它叫平移等變性（translation equivariance）（[d2l](../sources/d2l-ch7.md) § 7.1.1. Invariance）。

> 原文（d2l-ch7）：In the earliest layers, our network should respond similarly to the same patch, regardless of where it appears in the image.

> 原文（d2l-ch7）：This principle is called translation invariance (or translation equivariance).

d2l 用「Where's Waldo」遊戲說明：Waldo 長什麼樣子和他在哪裡無關，所以可以用同一個 Waldo 偵測器掃過影像的每一塊，替每一塊打分數（[d2l](../sources/d2l-ch7.md) § 7.1.1. Invariance）。

圖見原文：[d2l 7.1.1 Invariance](https://d2l.ai/chapter_convolutional-neural-networks/why-conv.html#invariance)（[d2l](../sources/d2l-ch7.md) § 7.1.1. Invariance）

> 原文（d2l-ch7）：However, what Waldo looks like does not depend upon where Waldo is located.

寫成數學：輸入平移時，隱藏表示只跟著平移。這只有在權重和偏置都不依賴輸出位置 $(i, j)$ 時才成立，於是每個位置共用同一組權重 $[\mathbf{V}]_{a, b}$ 和同一個偏置 $u$（[d2l](../sources/d2l-ch7.md) § 7.1.2.1. Translation Invariance）。

> 原文（d2l-ch7）：This implies that a shift in the input \(\mathbf{X}\) should simply lead to a shift in the hidden representation \(\mathbf{H}\).

## 為什麼重要

CNN 把這個「空間不變性」系統化，用較少的參數學到有用的表示（[d2l](../sources/d2l-ch7.md) § 7.1.1. Invariance）。權重不隨位置改變後，一層的參數從 $10^{12}$ 降到 $4 \times 10^6$（[d2l](../sources/d2l-ch7.md) § 7.1.2.1. Translation Invariance）。

> 原文（d2l-ch7）：In particular, translation invariance in images implies that all patches of an image will be treated in the same manner.

這也是一種歸納偏置：如果影像其實不是平移不變的，模型可能連訓練資料都擬合不好（[d2l](../sources/d2l-ch7.md) § 7.1.2.2. Locality）。

## 和其他概念的關係

- [卷積層](convolutional-layer.md)：平移不變性加上[局部性](locality.md)，就推出卷積層（[d2l](../sources/d2l-ch7.md) § 7.1.5. Summary and Discussion）。
- [池化](../methods/pooling.md)：卷積層的輸出會跟著輸入移動。把黑白分界的影像整張往右移一個像素，邊緣偵測的輸出可能差很多（[d2l](../sources/d2l-ch7.md) § 7.5. Pooling）。池化的目的之一就是減輕卷積層對位置的敏感；2×2 最大池化讓卷積層辨認出的圖案在高或寬方向移動一個元素以內時仍偵測得到（[d2l](../sources/d2l-ch7.md) § 7.5. Pooling；[d2l](../sources/d2l-ch7.md) § 7.5.1. Maximum Pooling and Average Pooling）。

> 原文（d2l-ch7）：Moreover, when detecting lower-level features, such as edges (as discussed in Section 7.2), we often want our representations to be somewhat invariant to translation.

## 相關頁面

- [d2l 第 7 章](../sources/d2l-ch7.md)
- [卷積層](convolutional-layer.md)
- [局部性](locality.md)
- [池化](../methods/pooling.md)
