# 訓練與梯度下降

## 輸入

- 資料：模型可以從中學習的內容（[d2l 基礎](../sources/d2l-basics.md) § 1.2. Key Components）。
- 模型：行為由參數（parameter）決定的程式（[d2l 基礎](../sources/d2l-basics.md) § 1.1. A Motivating Example）。
- 損失函數（loss function）：衡量模型做得多差的函數，習慣上定義成越低越好（[d2l 基礎](../sources/d2l-basics.md) § 1.2.3. Objective Functions）。

> 原文（d2l-basics）：Because we choose lower to be better, these functions are sometimes called loss functions.

## 步驟

訓練（training）是用資料找出最好的參數值，也就是讓程式在選定的表現指標上變好的那組值（[d2l 基礎](../sources/d2l-basics.md) § 1.1. A Motivating Example）。常見的做法是梯度下降（gradient descent）（[d2l 基礎](../sources/d2l-basics.md) § 1.2.4. Optimization Algorithms）：

1. 看每個參數稍微改變一點時，訓練集的損失會怎麼變（[d2l 基礎](../sources/d2l-basics.md) § 1.2.4. Optimization Algorithms）。
2. 把參數往讓損失變低的方向更新（[d2l 基礎](../sources/d2l-basics.md) § 1.2.4. Optimization Algorithms）。
3. 重複這兩步，一步步降低損失（[d2l 基礎](../sources/d2l-basics.md) § 3.1.1.4. Minibatch Stochastic Gradient Descent）。

> 原文（d2l-basics）：In brief, at each step, this method checks to see, for each parameter, how that training set loss would change if you perturbed that parameter by just a small amount.

> 原文（d2l-basics）：It would then update the parameter in the direction that lowers the loss.

## 輸出

- 一組固定下來的參數；參數固定下來的程式就是模型（[d2l 基礎](../sources/d2l-basics.md) § 1.1. A Motivating Example）。

> 原文（d2l-basics）：Once the parameters are fixed, we call the program a model.

## 公式與參數

導數（derivative）是函數隨輸入改變的變化率；它能告訴我們，把每個參數增加或減少極小的量時，損失函數會增加或減少得多快（[d2l 基礎](../sources/d2l-basics.md) § 2.4.1. Derivatives and Differentiation）。

函數 $f$ 在 $x$ 的導數定義成 $f'(x) = \lim_{h \rightarrow 0} \frac{f(x+h) - f(x)}{h}$（[d2l 基礎](../sources/d2l-basics.md) § 2.4.1. Derivatives and Differentiation）。

> 原文（d2l-basics）：Put simply, a derivative is the rate of change in a function with respect to changes in its arguments.

## 為什麼這樣設計

幾乎每個深度學習模型都靠這個做法最佳化：反覆更新參數，往讓損失函數逐漸變低的方向走（[d2l 基礎](../sources/d2l-basics.md) § 3.1.1.4. Minibatch Stochastic Gradient Descent）。

> 原文（d2l-basics）：The key technique for optimizing nearly every deep learning model, and which we will call upon throughout this book, consists of iteratively reducing the error by updating the parameters in the direction that incrementally lowers the loss function.

最單純的梯度下降要走過整個資料集才能更新一次，實際上可能非常慢（[d2l 基礎](../sources/d2l-basics.md) § 3.1.1.4. Minibatch Stochastic Gradient Descent）。

## 比較

訓練時用導數調整模型的參數，讓損失變低；特徵視覺化也用導數，但調整的是輸入影像，往目標變大的方向走（[d2l 基礎](../sources/d2l-basics.md) § 2.4.1. Derivatives and Differentiation；[Feature Visualization](../sources/feature-visualization.md) § Feature Visualization by Optimization）。

| 做法 | 調整什麼 | 往哪個方向 |
|---|---|---|
| 訓練 | 模型的參數 | 讓損失變低（[d2l 基礎](../sources/d2l-basics.md) § 1.2.4. Optimization Algorithms） |
| 特徵視覺化 | 輸入影像 | 讓目標變大（[Feature Visualization](../sources/feature-visualization.md) § Feature Visualization by Optimization） |

## 相關頁面

- [d2l 基礎小節](../sources/d2l-basics.md)
- [神經網路基礎](../concepts/neural-network-basics.md)
- [特徵視覺化](feature-visualization.md)
