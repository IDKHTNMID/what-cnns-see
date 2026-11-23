# 動手學深度學習 基礎小節（Dive into Deep Learning, Sections 1.1–1.2, 2.4, 3.1 and 5.1）

- 作者：Aston Zhang、Zachary C. Lipton、Mu Li、Alexander J. Smola ／ 年份：2023 ／ 原文：https://d2l.ai/ ／ 授權：CC BY-SA 4.0
- 收錄範圍：1.1、1.2、2.4.1、3.1.1.4、3.1.4、5.1.1.2 講參數、訓練、導數和全連接層的正文，不含程式碼與習題。

## 一句話

從「用資料調整參數」講起，再說明導數、梯度下降，以及一層層疊起來的全連接網路（§ 1.1. A Motivating Example；§ 1.2.4. Optimization Algorithms；§ 5.1.1.2. Incorporating Hidden Layers）。

## 重點

**1. 參數決定程式的行為。** 做法是定義一個有彈性的程式，它的行為由一些參數（parameter）決定；參數可以想成能轉動的旋鈕，參數固定下來的程式叫模型（model）（§ 1.1. A Motivating Example）。

> 原文（d2l-basics）：You can think of the parameters as knobs that we can turn, manipulating the behavior of the program.

> 原文（d2l-basics）：Once the parameters are fixed, we call the program a model.

**2. 訓練是用資料找出最好的參數值。** 最好的參數值，是讓程式在選定的表現指標上變好的那組值（§ 1.1. A Motivating Example）。衡量模型做得多好或多差的函數叫目標函數（objective function）；習慣上定義成越低越好，所以也叫損失函數（loss function）（§ 1.2. Key Components；§ 1.2.3. Objective Functions）。

> 原文（d2l-basics）：Then we use the dataset to determine the best possible parameter values, i.e., those that improve the performance of our program with respect to a chosen performance measure.

> 原文（d2l-basics）：Because we choose lower to be better, these functions are sometimes called loss functions.

**3. 導數是變化率。** 導數（derivative）是函數隨輸入改變的變化率；它能告訴我們，把每個參數增加或減少極小的量時，損失函數會增加或減少得多快（§ 2.4.1. Derivatives and Differentiation）。

> 原文（d2l-basics）：Put simply, a derivative is the rate of change in a function with respect to changes in its arguments.

**4. 梯度下降一步步降低損失。** 梯度下降（gradient descent）每一步檢查：每個參數稍微改變一點時，訓練集的損失會怎麼變；然後把參數往讓損失變低的方向更新（§ 1.2.4. Optimization Algorithms）。

> 原文（d2l-basics）：In brief, at each step, this method checks to see, for each parameter, how that training set loss would change if you perturbed that parameter by just a small amount.

> 原文（d2l-basics）：It would then update the parameter in the direction that lowers the loss.

**5. 神經網路一層接一層。** 最簡單的做法是把很多全連接層（fully connected layer）疊起來，每一層把結果交給下一層，直到產生輸出（§ 5.1.1.2. Incorporating Hidden Layers）。全連接表示每個輸入都影響隱藏層的每個神經元，隱藏層的每個神經元又影響輸出層的每個神經元（§ 5.1.1.2. Incorporating Hidden Layers）。

> 原文（d2l-basics）：Each layer feeds into the layer above it, until we generate outputs.

> 原文（d2l-basics）：Every input influences every neuron in the hidden layer, and each of these in turn influences every neuron in the output layer.

## 方法

先用喚醒詞（wake word）辨識的例子帶出參數和模型，再整理出機器學習的核心元件（§ 1.1. A Motivating Example；§ 1.2. Key Components）。之後把線性迴歸畫成單層全連接神經網路，再加入隱藏層，變成多層感知機（multilayer perceptron，MLP）（§ 3.1.4. Linear Regression as a Neural Network；§ 5.1.1.2. Incorporating Hidden Layers）。

> 原文（d2l-basics）：An objective function that quantifies how well (or badly) the model is doing.

## 結論

- 不管哪一種機器學習問題，核心元件都是資料、模型、目標函數，以及調整模型參數來最佳化目標函數的演算法（§ 1.2. Key Components）。
- 深度學習常見的最佳化演算法，都建立在梯度下降上（§ 1.2.4. Optimization Algorithms）。
- 線性迴歸可以看成單層全連接神經網路；把很多全連接層疊起來就是多層感知機（§ 3.1.4. Linear Regression as a Neural Network；§ 5.1.1.2. Incorporating Hidden Layers）。

## 限制

- 最單純的梯度下降要走過整個資料集才能更新一次，實際上可能非常慢（§ 3.1.1.4. Minibatch Stochastic Gradient Descent）。

## 相關頁面

- [神經網路基礎](../concepts/neural-network-basics.md)
- [訓練與梯度下降](../methods/gradient-descent.md)
- [卷積層](../concepts/convolutional-layer.md)
