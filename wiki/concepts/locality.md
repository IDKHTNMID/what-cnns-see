# 局部性

## 是什麼

局部性（locality）是 CNN 的第二個設計原則：網路最前面幾層只看局部區域，不管影像遠處的內容；這些局部表示最後再匯總起來，對整張影像做預測（[d2l](../sources/d2l-ch7.md) § 7.1.1. Invariance）。

> 原文（d2l-ch7）：The earliest layers of the network should focus on local regions, without regard for the contents of the image in distant regions.

寫成數學：計算位置 $(i, j)$ 的隱藏表示時，只用附近的輸入；偏移量 $|a| > \Delta$ 或 $|b| > \Delta$ 的權重一律設為 0（[d2l](../sources/d2l-ch7.md) § 7.1.2.2. Locality）。

> 原文（d2l-ch7）：Locality means that only a small neighborhood of pixels will be used to compute the corresponding hidden representations.

## 為什麼重要

在平移不變性之後再加上局部性，參數從 $4 \times 10^6$ 降到 $4\Delta^2$，$\Delta$ 通常小於 10，又少了四個數量級（[d2l](../sources/d2l-ch7.md) § 7.1.2.2. Locality）。代價是每個隱藏單元只能用到局部資訊（[d2l](../sources/d2l-ch7.md) § 7.1.2.2. Locality）。

> 原文（d2l-ch7）：While previously, we might have required billions of parameters to represent just a single layer in an image-processing network, we now typically need just a few hundred, without altering the dimensionality of either the inputs or the hidden representations.

因為計算高度局部，卷積可以做大量硬體最佳化（[d2l](../sources/d2l-ch7.md) § 7.2.7. Summary）。

> 原文（d2l-ch7）：As can be seen, the computation is straightforward and, most importantly, highly local.

## 和其他概念的關係

- [卷積層](convolutional-layer.md)：[平移不變性](translation-invariance.md)加上局部性，就推出卷積層（[d2l](../sources/d2l-ch7.md) § 7.1.5. Summary and Discussion）。
- [感受野](receptive-field.md)：單一層只看局部，但網路做深之後，深層元素的感受野會變大，能偵測較大範圍的特徵（[d2l](../sources/d2l-ch7.md) § 7.2.6. Feature Map and Receptive Field）。
- [卷積運算](../methods/convolution-operation.md)的 1×1 卷積用最小的窗口，完全不看相鄰像素，只在通道維度上計算（[d2l](../sources/d2l-ch7.md) § 7.4.3. 1×1 Convolutional Layer）。
- [通道](channel.md)讓 CNN 兼顧兩邊：全連接層的大量非線性，和卷積的局部特徵分析（[d2l](../sources/d2l-ch7.md) § 7.4.4. Discussion）。

## 相關頁面

- [d2l 第 7 章](../sources/d2l-ch7.md)
- [卷積層](convolutional-layer.md)
- [平移不變性](translation-invariance.md)
- [感受野](receptive-field.md)
