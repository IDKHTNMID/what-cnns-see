# 歸因

## 輸入

- 一張輸入影像和訓練好的網路；Building Blocks 用 GoogLeNet（[The Building Blocks of Interpretability](../sources/building-blocks.md) § The Building Blocks of Interpretability）。
- 要解釋的輸出類別，以及要歸因到的隱藏層（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps；[The Building Blocks of Interpretability](../sources/building-blocks.md) § Channel Attribution）。

## 步驟

### 線性近似

1. 一個神經元（neuron）對輸出的影響，估計成「它的激活值（activation）× 提高它的激活值會讓輸出提高多快」，也就是激活值乘上梯度（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Are Concepts Assembled?）。
2. 對激活值的線性組合，歸因是各單位歸因的線性組合，也等於這個組合的激活值和梯度的內積（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Are Concepts Assembled?）。
3. 做空間歸因時另外處理梯度：GoogLeNet 有步幅的最大池化會在梯度裡帶來很多雜訊和棋盤狀圖樣，見[棋盤狀假影](../concepts/checkerboard-artifacts.md)；作者把最大池化的梯度放寬，依激活值比例分給各輸入，不再全部給最大的那個，再把棋盤狀圖樣抵消掉（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Are Concepts Assembled?）。

> 原文（building-blocks）：That is, we estimate the effect of a neuron on the output is its activation times the rate at which increasing its activation increases the output.

> 原文（building-blocks）：To avoid our interface demonstrations being dominated by this noise, we (a) do a relaxation of the gradient of max pooling, distributing gradient to inputs proportional to their activation instead of winner takes all and (b) cancel out the checkerboard patterns.

### 空間歸因

1. 從每個隱藏層的每個元素（原文叫 spatial position），對全部 1,000 個輸出類別做歸因（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）。
2. 這個千維向量用降維（dimensionality reduction）畫成多方向的顯著圖（saliency map），疊在依大小縮放的[激活網格](activation-grid.md)上（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）。
3. 滑鼠移到一個位置時，圖例顯示這個位置最支持哪些類別；其他隱藏層上也出現顯著圖，這就是層到層歸因（layer-to-layer attribution）（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）。

> 原文（building-blocks）：Perhaps most interestingly, this interface allows us to interactively perform attribution between hidden layers.

圖見原文：[The Building Blocks of Interpretability：Spatial Attribution with Saliency Maps（空間歸因的互動圖）](https://distill.pub/2018/building-blocks/#AttributionSpatial)（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）

### 通道歸因

1. 改成按通道切：每個通道（原文也叫 detector）對最後的輸出貢獻多少，這叫通道歸因（channel attribution）（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Channel Attribution）。
2. 用[語意字典](../concepts/semantic-dictionary.md)（semantic dictionary）的圖示代表最支持輸出類別的通道（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Channel Attribution）。
3. 滑鼠移到一個通道上時，在輸入影像上疊出它的激活值熱圖（heatmap），圖例顯示它最支持哪些類別；點下去可以看層到層歸因：哪些低層通道貢獻最多，又支持了哪些高層通道（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Channel Attribution）。

> 原文（building-blocks）：Doing so allows us to perform channel attribution: how much did each detector contribute to the final output?

圖見原文：[The Building Blocks of Interpretability：Channel Attribution（通道歸因的互動圖）](https://distill.pub/2018/building-blocks/#AttributionChannel)（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Channel Attribution）

## 輸出

- 空間歸因：疊在激活網格上的多方向顯著圖，以及每個位置最支持的類別（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）。
- 通道歸因：每一層最支持某個類別的通道，以及層與層之間的通道怎麼互相支持（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Channel Attribution）。

## 公式與參數

$a_i$ 是神經元 $i$ 的激活值，$y$ 是輸出（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Are Concepts Assembled?）：

```math
\text{attr}(a_i) = a_i \cdot \frac{\partial y}{\partial a_i}
```

激活值的線性組合 $\sum_i w_i a_i$，歸因是各單位歸因的線性組合（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Are Concepts Assembled?）：

```math
\text{attr}\Big(\sum_i w_i a_i\Big) = \sum_i w_i \, a_i \frac{\partial y}{\partial a_i}
```

> 原文（building-blocks）：When we talk about a linear combination of activations, the attribution can be thought of as the linear combination of the attributions of the units, or equivalently as the dot product between the activation of that combination and the gradient.

參數：要歸因到哪幾層、對哪些輸出類別；空間歸因對 1,000 個類別都做（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）。

## 為什麼這樣設計

**為什麼需要歸因。** Feature Visualization 把可解釋性研究分成兩條主線：特徵視覺化（feature visualization）和歸因（attribution）（[Feature Visualization](../sources/feature-visualization.md) § Feature Visualization）。特徵視覺化回答網路偵測到什麼，但不回答網路怎麼把這些組成後面的決定、為什麼這樣決定；歸因解釋神經元之間的關係，回答這些問題（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Are Concepts Assembled?）。

> 原文（building-blocks）：Feature visualization helps us answer what the network detects, but it does not answer how the network assembles these individual pieces to arrive at later decisions, or why these decisions were made.

**為什麼用簡單的線性近似。** 歸因方法很多，還沒有明確對的答案；作者說這篇不在乎用哪一種，換成幾乎任何其他方法都可以，之後歸因方法改進，建在上面的介面也會跟著變好（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Are Concepts Assembled?）。

> 原文（building-blocks）：There are a wide variety of approaches to attribution but, so far, there doesn't seem to be a clear right answer.

**為什麼不只用顯著圖。** 作者指出顯著圖的兩個弱點（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）：

- 像素不一定適合當歸因的單位：每個像素的意義和其他像素糾纏在一起，對亮度、對比這類簡單變換不穩健，也離輸出類別這種高層概念很遠（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）。
- 傳統的顯著圖一次只顯示一個類別的歸因，也不能深入看單一個點（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）。

> 原文（building-blocks）：First, it is not clear that individual pixels should be the primary unit of attribution.

所以作者改在隱藏層上做歸因，問的不是某個像素的顏色重不重要，而是那個位置偵測到的高層概念（例如垂耳）重不重要（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）。

**為什麼再做通道歸因。** 同一個位置常同時偵測到好幾個概念，只看位置就分不開（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）。顯著圖等於按位置切、把所有通道加總，看不出每個位置上是哪些偵測器貢獻最多；通道歸因改成按通道切（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Channel Attribution）。

> 原文（building-blocks）：This aggregates over all channels and, as a result, we cannot tell which specific detectors at each position most contributed to the final output classification.

**兩種切法的共同問題。** 資訊太多，要花好幾個小時人工檢查才能看懂那一長串影響很小的通道；而且兩種匯總都嚴重失真，可能漏掉重要的部分；這是[矩陣分解](matrix-factorization.md)要解決的問題（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Channel Attribution；[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：On the other hand, both the aggregations we have explored are extremely lossy and can miss important parts of the story.

**為什麼在隱藏層之間做比較可信。** 近來的研究指出很多歸因技術不可靠；函數的輸出可能來自輸入之間的非線性交互作用，使歸因路徑相依（path-dependent）（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Trustworthy Are These Interfaces?）。作者認為相鄰層之間的對應很簡單、基本上是線性的，所以歸因有穩固的基礎；距離較遠的層，高層特徵對輸出的歸因也比對輸入的歸因一致得多（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Trustworthy Are These Interfaces?）。

> 原文（building-blocks）：Clearly, this is not a concern for attribution between adjacent layers because of the simple (essentially linear) mapping between them.

## 比較

Feature Visualization 說文獻偏好 attribution 和 saliency maps 這類叫法（[Feature Visualization](../sources/feature-visualization.md) § Feature Visualization）；Building Blocks 則把顯著圖定義成歸因最常見的介面：標出輸入影像中最影響輸出分類的像素的熱圖。本 Wiki 照 Building Blocks 的定義，把顯著圖當成歸因的一種呈現方式（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps）。

> 原文（feature-visualization）：Attribution has gone under many different names in the literature — including "feature visualization"! — but recent work seems to prefer terms like "attribution" and "saliency maps".

> 原文（building-blocks）：The most common interface for attribution is called a saliency map — a simple heatmap that highlights pixels of the input image that most caused the output classification.

| 做法 | 歸因到哪裡 | 怎麼呈現 |
|---|---|---|
| 顯著圖 | 輸入影像的像素 | 熱圖，一次一個類別（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps） |
| Class Activation Mapping（CAM） | 結果映回輸入影像 | 和空間歸因類似，但沒有用隱藏層的行為來說明（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps） |
| 空間歸因 | 隱藏層的元素 | 1,000 個類別降維成多方向顯著圖，疊在激活網格上（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Spatial Attribution with Saliency Maps） |
| 通道歸因 | 隱藏層的通道 | 語意字典的圖示，加上層到層的連結（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Channel Attribution） |

> 原文（building-blocks）：This approach is similar to what Class Activation Mapping (CAM) methods do but, because they interpret their results back onto the input image, they miss the opportunity to communicate in terms of the rich behavior of a network's hidden layers.

## 相關頁面

- [The Building Blocks of Interpretability](../sources/building-blocks.md)
- [Feature Visualization](../sources/feature-visualization.md)
- [特徵視覺化](feature-visualization.md)
- [語意字典](../concepts/semantic-dictionary.md)
- [激活網格](activation-grid.md)
- [特徵圖](../concepts/feature-map.md)
- [矩陣分解](matrix-factorization.md)
- [池化](pooling.md)
- [棋盤狀假影](../concepts/checkerboard-artifacts.md)
