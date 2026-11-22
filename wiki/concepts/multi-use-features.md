# 多用途特徵

## 是什麼

多用途特徵（multi-use features）是 Activation Atlas 取的名字：一個偵測器（detector）回應幾種很不一樣、但看起來相似的概念（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）。這裡的偵測器是類別激活圖譜上的一個圖示，也就是一格的平均激活向量（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes；[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Aggregating Multiple Images）。

> 原文（activation-atlas）：We'll call these "multi-use" features — detectors that react to very different concepts that are nonetheless visually similar.

作者比較兩個相近類別的[類別激活圖譜](../methods/activation-atlas.md)，找到三個例子（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）：

- **浮潛（snorkel）和水肺潛水員（scuba diver）：** 水肺潛水員那一側有一個圓的、亮的金屬物體，這個激活值強烈歸因到「蒸汽火車頭」（steam locomotive）；網路用蒸汽火車頭的偵測器辨認氣瓶，幫助判斷水肺潛水員（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）。
- **灰鯨（grey whale）和大白鯊（great white shark）：** 一個偵測器同時偵測棒球的紅色縫線，以及鯊魚的白牙和粉紅色口腔；它也出現在 mixed5b 篩出大白鯊的圖譜裡，歸因指向各種球，第一名是「棒球」（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）。
- **平底鍋（frying pan）和炒鍋（wok）：** 炒鍋那一側有像麵條的東西，強烈歸因到「carbonara」（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）。

> 原文（activation-atlas）：The failure mode here seems to be that the model is using its detectors for the class "steam locomotive" to identify air tanks to help classify "scuba diver".

> 原文（activation-atlas）：In this example we see another detector that seems to be playing two roles: detecting red stitching on a baseball and a sharks's white teeth and pink inner mouth.

圖見原文：[Exploring Neural Networks with Activation Atlases：Further Isolating Classes（「grey whale」和「great white shark」的歸因差）](https://distill.pub/2019/activation-atlas/#class-gradient-shark)（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）

## 為什麼重要

**看得出模型的誤解，也能利用它。** 作者說激活圖譜能揭露模型高層次的誤解，而且可以被利用，例如看圖譜就能理解為什麼一張棒球的照片能把分類從「灰鯨」換成「大白鯊」（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Introduction）。

> 原文（activation-atlas）：For example, by looking at an activation atlas we will be able to see why a picture of a baseball can switch the classification of an image from "grey whale" to "great white shark".

**貼上補丁的結果。** 作者把像那個圖示的東西貼進 ImageNet 的照片，做成補丁（patch）（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）：

- 在灰鯨的照片上加一顆小棒球，最高分類就變成大白鯊；棒球變大後蓋過一切，最高分類變成棒球（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）。
- 在平底鍋的照片上加一塊麵條，降低原分類的效果沒那麼好；麵條圖示在比較圖裡比較靠近中間，兩類的歸因差較小；作者推測訓練資料裡炒鍋配麵條的照片比平底鍋多（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）。

> 原文（activation-atlas）：Adding a small-sized baseball does change the top classification to "great white shark", and as it gets bigger it overpowers the classification, so the top slot goes to "baseball".

> 原文（activation-atlas）：We suspect that the training set simply contained more images of woks with noodles than frying pans with noodles.

圖見原文：[Exploring Neural Networks with Activation Atlases：Further Isolating Classes（在灰鯨照片上加棒球）](https://distill.pub/2019/activation-atlas/#shark-grey-whale)（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）

**大量測試。** 十種補丁各在該類別 1,000 張 ImageNet 訓練影像上測試，約五分之二的影像被翻成目標類別；如果允許把補丁放在四個角中效果最好的一個、用最有效的大小，成功率約二分之一（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Testing dozens of patches on thousands of images）。為了確認補丁不只是擋住原類別的證據，每個攻擊都和隨機雜訊的補丁比較（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Testing dozens of patches on thousands of images）。

> 原文（activation-atlas）：The success rate reaches about 1 in 2 images if we also allow to position the patch in the best of the four corners of the image (top left, top right, bottom left, bottom right) at the most effective size.

圖見原文：[Exploring Neural Networks with Activation Atlases：Testing dozens of patches on thousands of images（補丁的測試結果）](https://distill.pub/2019/activation-atlas/#patch-examples)（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Testing dozens of patches on thousands of images）

**限制。** 不是每對類別都找得到這種補丁，不是每個圖示都有效，也只在一個模型上測過；但這些補丁是類別激活圖譜先揭露的，作者事前並不知道要找（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Testing dozens of patches on thousands of images）。

> 原文（activation-atlas）：However, the class activation atlas technique was what revealed the existence of these patches before we knew to look for them.

## 和其他概念的關係

- [激活圖譜](../methods/activation-atlas.md)：多用途特徵是比較兩個類別的類別激活圖譜時找到的；比較圖的橫軸是兩類的歸因差（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）。
- [語意字典](semantic-dictionary.md)：Building Blocks 說的多義神經元（poly-semantic neurons）是單一神經元同時回應幾種顯著概念，例如貓和車；Activation Atlas 的多用途特徵是圖譜上的一個偵測器回應幾種很不一樣、但看起來相似的概念（[The Building Blocks of Interpretability](../sources/building-blocks.md) § How Trustworthy Are These Interfaces?；[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）。
- 對抗樣本（adversarial examples）：作者把這些攻擊放在一個更大的趨勢裡，也就是研究傳統 epsilon ball 對抗樣本以外的輸入攻擊；最像的是對抗補丁（adversarial patch），也是在影像上加一小塊補丁（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Testing dozens of patches on thousands of images）。對抗補丁有效、可靠得多；作者覺得自己的攻擊有意思的地方，是人根據對模型的理解做出來的，而且似乎在更高的抽象層次攻擊模型（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Testing dozens of patches on thousands of images）。對抗樣本也出現在[正則化與預條件](../methods/regularization-and-preconditioning.md)：特徵視覺化完全不正則化時，得到的就是對抗樣本（[Feature Visualization](../sources/feature-visualization.md) § The Spectrum of Regularization）。
- [歸因](../methods/attribution.md)：比較圖的橫軸是兩類的歸因差；麵條圖示畫得比較靠中間，歸因差較小，補丁降低原本分類的效果也比較差（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Further Isolating Classes）。

> 原文（activation-atlas）：From this perspective, adversarial patches are far more effective, working much more reliably.

## 相關頁面

- [Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md)
- [激活圖譜](../methods/activation-atlas.md)
- [語意字典](semantic-dictionary.md)
- [歸因](../methods/attribution.md)
- [正則化與預條件](../methods/regularization-and-preconditioning.md)
- [The Building Blocks of Interpretability](../sources/building-blocks.md)
