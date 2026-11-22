# 卷積層

## 是什麼

卷積層（convolutional layer）把輸入和卷積核（kernel）做卷積運算，再加上一個純量偏置。它的兩個參數就是卷積核和偏置；訓練時卷積核通常隨機初始化，和全連接層一樣（[d2l](../sources/d2l-ch7.md) § 7.2.2. Convolutional Layers）。

> 原文（d2l-ch7）：A convolutional layer cross-correlates the input and kernel and adds a scalar bias to produce an output.

卷積神經網路（convolutional neural network，CNN）是含有卷積層的神經網路。卷積核也叫濾波器（filter），或直接叫這一層的權重，是可學習的參數（[d2l](../sources/d2l-ch7.md) § 7.1.2.2. Locality）。

> 原文（d2l-ch7）：In the deep learning research community, \(\mathbf{V}\) is referred to as a convolution kernel, a filter, or simply the layer's weights that are learnable parameters.

卷積核高 $h$、寬 $w$ 的卷積層，簡稱 $h \times w$ 卷積層（[d2l](../sources/d2l-ch7.md) § 7.2.2. Convolutional Layers）。

## 為什麼重要

全連接層處理影像時參數太多。100 萬像素的照片接 1000 個隱藏單元，就要 $10^6 \times 10^3 = 10^9$ 個參數（[d2l](../sources/d2l-ch7.md) § 7.1. From Fully Connected Layers to Convolutions）。如果隱藏表示也保留 1000×1000 的空間結構，一層就要 $10^{12}$ 個參數（[d2l](../sources/d2l-ch7.md) § 7.1.2. Constraining the MLP）。

> 原文（d2l-ch7）：This requires \(10^{12}\) parameters, far beyond what computers currently can handle.

d2l 對這個全連接層依序加上兩個限制，推出卷積層（[d2l](../sources/d2l-ch7.md) § 7.1.2.1. Translation Invariance；[d2l](../sources/d2l-ch7.md) § 7.1.2.2. Locality）：

| 限制 | 做法 | 參數量 |
|---|---|---|
| 無（全連接） | 每個輸出位置對每個輸入像素各有一個權重 | $10^{12}$（[d2l](../sources/d2l-ch7.md) § 7.1.2. Constraining the MLP） |
| 平移不變性 | 權重和偏置不隨輸出位置 $(i, j)$ 改變 | $4 \times 10^6$（[d2l](../sources/d2l-ch7.md) § 7.1.2.1. Translation Invariance） |
| 再加局部性 | 偏移量超過 $\Delta$ 的權重設為 0，$\Delta$ 通常小於 10 | $4\Delta^2$（[d2l](../sources/d2l-ch7.md) § 7.1.2.2. Locality） |

原本一層要數十億個參數，現在通常只要幾百個，而且輸入和隱藏表示的維度都沒變（[d2l](../sources/d2l-ch7.md) § 7.1.2.2. Locality）。代價是特徵變得平移不變，每個隱藏單元也只能用到局部資訊。d2l 把這種預設叫歸納偏置（inductive bias）：偏置符合現實時，模型需要的樣本少、泛化好；不符合時，模型可能連訓練資料都擬合不好（[d2l](../sources/d2l-ch7.md) § 7.1.2.2. Locality）。

> 原文（d2l-ch7）：All learning depends on imposing inductive bias.

卷積核不必由人設計，可以從資料學出來，這讓特徵工程的經驗法則換成以證據為本的統計（[d2l](../sources/d2l-ch7.md) § 7.2.7. Summary）。卷積的計算高度局部，可以做大量硬體最佳化，晶片設計可以把資源放在快速計算而不是記憶體（[d2l](../sources/d2l-ch7.md) § 7.2.7. Summary）。

> 原文（d2l-ch7）：This replaces feature engineering heuristics by evidence-based statistics.

## 和其他概念的關係

- [平移不變性](translation-invariance.md)和[局部性](locality.md)：卷積層就是由這兩個原則推出來的（[d2l](../sources/d2l-ch7.md) § 7.1.5. Summary and Discussion）。
- [通道](channel.md)：加入多個通道，把被這兩個限制拿掉的一部分複雜度補回來（[d2l](../sources/d2l-ch7.md) § 7.1.5. Summary and Discussion）。
- [感受野](receptive-field.md)：越深的層要表示影像中越大、越複雜的部分，做法是反覆交替疊非線性和卷積層（[d2l](../sources/d2l-ch7.md) § 7.1.2.2. Locality）。
- [卷積運算](../methods/convolution-operation.md)是卷積層實際的計算；[填充與步幅](../methods/padding-and-stride.md)控制輸出大小；[池化](../methods/pooling.md)可以把卷積層的輸出再匯總（[d2l](../sources/d2l-ch7.md) § 7.2.1. The Cross-Correlation Operation；[d2l](../sources/d2l-ch7.md) § 7.3. Padding and Stride；[d2l](../sources/d2l-ch7.md) § 7.5.1. Maximum Pooling and Average Pooling）。

> 原文（d2l-ch7）：This can be achieved by interleaving nonlinearities and convolutional layers repeatedly.

## 相關頁面

- [d2l 第 7 章](../sources/d2l-ch7.md)
- [平移不變性](translation-invariance.md)
- [局部性](locality.md)
- [通道](channel.md)
- [感受野](receptive-field.md)
- [卷積運算](../methods/convolution-operation.md)
