# 語意字典

## 是什麼

語意字典（semantic dictionary）把每個神經元（neuron）的激活值（activation）配上那個神經元的特徵視覺化（feature visualization），再依激活值大小排序（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。這樣激活值就對應到圖示（icon），不再是抽象的索引；很多圖示看起來像人熟悉的概念，例如「垂耳」「狗鼻」「毛」（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。這個詞是 Building Blocks 的作者 Ian 和 Chris 創的（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Author Contributions）。

> 原文（building-blocks）：To make a semantic dictionary, we pair every neuron activation with a visualization of that neuron and sort them by the magnitude of the activation.

特徵視覺化用以最佳化為基礎的做法，避免假相關；作者說也可以用其他方法（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。語意字典雖然以神經元介紹，但可以用在任何激活值的基底上（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。

> 原文（building-blocks）：We use optimization-based feature visualization to avoid spurious correlation, but one could use other methods.

> 原文（building-blocks）：While we introduce semantic dictionaries in terms of neurons, they can be used with any basis of activations.

圖見原文：[The Building Blocks of Interpretability：Making Sense of Hidden Layers（一個位置的語意字典）](https://distill.pub/2018/building-blocks/#SemanticDict)（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）

## 為什麼重要

語意字典不只是擺脫沒有意義的索引，而是用典型的例子表達網路學到的抽象概念；影像分類網路學到的是視覺上的抽象概念，所以影像是最自然的符號，如果是處理音訊，比較自然的符號可能是音訊片段（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。

> 原文（building-blocks）：With image classification, the neural network learns a set of visual abstractions and thus images are the most natural symbols to represent them.

把神經元化成文字會失真，作者舉了三種情況（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）：

- 就算是熟悉的概念，網路也可能學到更細的差別；例如 GoogLeNet 有好幾個偵測垂耳的通道，偵測的下垂程度、耳朵長度和周圍脈絡略有不同（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。
- 有些概念看得懂，卻沒有好的文字描述，例如陽光照在漣漪上的那一道閃光（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。
- 網路可能學到人類陌生的抽象概念，這時文字完全派不上用場（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。

> 原文（building-blocks）：For instance, GoogLeNet has multiple floppy ear detectors that appear to detect slightly different levels of droopiness, length, and surrounding context to the ears.

隱藏層有了意義，既有的可解釋性技術才能當成可以組合的元件；例如歸因不再只在輸入層和輸出層之間做，也可以從特定的隱藏層出發，或歸因到特定的隱藏層（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。

> 原文（building-blocks）：For example, besides the one-way attribution that we currently perform with the input and output layers, semantic dictionaries allow us to attribute to-and-from specific hidden layers.

語意字典的前提是：神經元在不同輸入影像之間的意義大致一致，而且特徵視覺化如實呈現了這個意義（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Trustworthy Are These Interfaces?）。作者在 Feature Visualization 裡發現 GoogLeNet 很多神經元對應到有意義的概念，但也有多義神經元（poly-semantic neurons），同時回應幾種顯著概念，例如貓和車（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Trustworthy Are These Interfaces?）。

> 原文（building-blocks）：Semantic dictionaries, and the interfaces that build on top of them, are premised off this question being true.

> 原文（building-blocks）：Besides these neurons, however, we also found many neurons that do not have as clean a meaning including "poly-semantic" neurons that respond to a mixture of salient ideas (e.g., "cat" and "car").

介面可以這樣應對多義神經元：用多樣性的視覺化顯示一個神經元的各種意義，或旋轉語意字典，讓各成分更分得開（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Trustworthy Are These Interfaces?）。作者認為特徵不必是完美的偵測器，把它們當偵測器看仍然有用，找出偵測器誤判的時候也很有意思（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Trustworthy Are These Interfaces?）。

> 原文（building-blocks）：In our view, features do not need to be flawless detectors for it to be useful for us to think about them as such.

## 和其他概念的關係

- [特徵視覺化](../methods/feature-visualization.md)：語意字典裡的每個圖示都是特徵視覺化的結果（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。
- [特徵圖](feature-map.md)：語意字典替特徵圖裡的激活值配上圖示（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers）。
- [激活網格](../methods/activation-grid.md)：把同樣的做法套到每個元素的激活向量，排成網格（[The Building Blocks of Interpretability](../sources/building-blocks.md) § What Does the Network See?）。
- [歸因](../methods/attribution.md)：通道歸因的介面用語意字典的圖示代表通道（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Channel Attribution）。
- [激活空間](activation-space.md)：語意字典可以用在任何激活值的基底上；遇到多義神經元時，也可以旋轉語意字典（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Sense of Hidden Layers；[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Trustworthy Are These Interfaces?）。
- [矩陣分解](../methods/matrix-factorization.md)：神經元群組是另一種基底；作者說用其他基底提供更好的理解單位，才剛開始探索（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
- [多用途特徵](multi-use-features.md)：多義神經元是單一神經元同時回應幾種顯著概念；Activation Atlas 的多用途特徵是類別激活圖譜上的一個偵測器，回應幾種很不一樣、但看起來相似的概念（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Trustworthy Are These Interfaces?；[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）。

> 原文（building-blocks）：Our visualizations have only begun to explore the potential of alternate bases in providing better atoms for understanding neural networks.

## 相關頁面

- [The Building Blocks of Interpretability](../sources/building-blocks.md)
- [Feature Visualization](../sources/feature-visualization.md)
- [特徵視覺化](../methods/feature-visualization.md)
- [特徵圖](feature-map.md)
- [激活網格](../methods/activation-grid.md)
- [歸因](../methods/attribution.md)
- [激活空間](activation-space.md)
- [矩陣分解](../methods/matrix-factorization.md)
- [多用途特徵](multi-use-features.md)
- [Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md)
