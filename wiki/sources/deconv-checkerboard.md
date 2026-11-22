# 轉置卷積與棋盤狀假影（Deconvolution and Checkerboard Artifacts）

- 作者：Augustus Odena、Vincent Dumoulin、Chris Olah ／ 年份：2016 ／ 原文：https://distill.pub/2016/deconv-checkerboard/ ／ 授權：CC BY 2.0

## 一句話

神經網路產生的影像常有棋盤狀假影（checkerboard artifacts），原因是轉置卷積（transposed convolution）的不均勻重疊（uneven overlap）；先放大影像再做卷積（resize-convolution）就能避免；卷積層的梯度裡也有同樣的假影（§ 全文）。

## 重點

**1. 棋盤狀假影來自轉置卷積的不均勻重疊。** 產生影像時，網路常從低解析度的描述逐步放大，通常用轉置卷積：小圖的每一點在大圖上「畫」一塊方形（§ Deconvolution & Overlap）。原文為了簡短叫它 deconvolution，並說另一個名字是 transposed convolution；本 Wiki 用轉置卷積（§ Deconvolution & Overlap）。卷積核大小不能被步幅整除時，有些位置被畫到的比其他位置多，這叫不均勻重疊；二維時兩個軸的不均勻相乘，形成棋盤狀假影（§ Deconvolution & Overlap）。

> 原文（deconv-checkerboard）：In particular, deconvolution has uneven overlap when the kernel size (the output window size) is not divisible by the stride (the spacing between points on the top).

**2. 很難靠學習避開。** 理論上模型可以學會在重疊不均勻的位置小心調整，讓輸出平衡；實際上很難完全做到，而且均勻重疊的模型也常學出造成類似假影的卷積核（§ Overlap & Learning）。作者說，轉置卷積最好的情況是很脆弱，最壞的情況是產生假影就是它的預設行為（§ Overlap & Learning）。

> 原文（deconv-checkerboard）：At worst, creating artifacts is the default behavior of deconvolution.

**3. resize-convolution 可以修好。** 把放大和算特徵分開：先用最近鄰插值（nearest-neighbor interpolation）或雙線性插值（bilinear interpolation）放大影像，再做一層卷積層（§ Better Upsampling）。生成對抗網路（GAN）把轉置卷積層換成最近鄰放大加卷積後，不同頻率的假影都消失了（§ Image Generation Results）。

> 原文（deconv-checkerboard）：Simply switching out the standard deconvolutional layers for nearest-neighbor resize followed by convolution causes artifacts of different frequencies to disappear.

**4. 梯度裡也有棋盤狀假影。** 計算卷積層的梯度時，反向傳播做的就是轉置卷積，所以梯度裡也可能出現棋盤狀假影（§ Artifacts in Gradients）。特徵視覺化領域早就知道影像模型的梯度裡有高頻「雜訊」，這是一大挑戰（§ Artifacts in Gradients）。

> 原文（deconv-checkerboard）：Whenever we compute the gradients of a convolutional layer, we do deconvolution (transposed convolution) on the backward pass.

**5. 梯度假影的影響還不清楚。** 有些神經元拿到的梯度是鄰居的好幾倍，等於網路沒來由地特別在意某些像素；作者推測這可能放大對抗樣本，但沒有研究（§ Artifacts in Gradients）。

> 原文（deconv-checkerboard）：It seems possible that having some pixels affect the network output much more than others may exaggerate adversarial counter-examples.

## 方法

作者在三種模型上看假影（§ Image Generation Results；§ Artifacts in Gradients）：

- GAN：把生成器（generator）的轉置卷積層換掉，比較訓練後和隨機權重時的輸出；另外比較鑑別器（discriminator）第一層用不用步幅 2 的卷積（§ Image Generation Results；§ Artifacts in Gradients）。
- 即時藝術風格轉換：直接產生風格轉換影像的網路（§ Image Generation Results）。
- DeepDream：比較網路每一步都套在同一個位置，和每一步換位置的結果（§ Artifacts in Gradients）。
- 分工：Augustus 做 GAN 實驗，Vincent 做藝術風格轉換實驗，Chris 做 DeepDream 實驗（§ Author Contributions）。

> 原文（deconv-checkerboard）：Chris ran the DeepDream experiments, created the visualizations and wrote most of the article.

實作上，TensorFlow 可以用 `tf.image.resize_images()` 做 resize-convolution 層；先用 `tf.pad()` 補邊再用 `tf.nn.conv2d()` 做卷積，避免邊界假影（§ Code）。

> 原文（deconv-checkerboard）：For best results, use tf.pad() before doing convolution with tf.nn.conv2d() to avoid boundary artifacts.

## 結論

- 用轉置卷積產生影像的標準做法雖然成功，但有概念上很簡單的問題會造成假影；換成沒有這些問題的自然替代做法，假影就消失（§ Conclusion）。
- 類似的論證表示，一般有步幅的卷積層可能也有問題（§ Conclusion）。
- 作者認為仔細想過網路架構，還有容易摘的果實，即使是看起來已經有乾淨解法的架構（§ Conclusion）。

> 原文（deconv-checkerboard）：Analogous arguments suggest that standard strided convolutional layers may also have issues

## 限制

- 雙線性插值很難用好；可能只是作者的超參數是為轉置卷積調的，也可能是雙線性插值太抗拒高頻的影像特徵（§ Better Upsampling）。
- 作者不認為兩種 resize-convolution 是上採樣的最終解法，只是它們確實修好了棋盤狀假影（§ Better Upsampling）。
- DeepDream 的假影有些不是棋盤狀，而是比較不規則的高頻圖樣，作者認為是最大池化造成的（§ Artifacts in Gradients）。
- 梯度假影可能放大對抗樣本，作者沒有研究（§ Artifacts in Gradients）。

> 原文（deconv-checkerboard）：We don't necessarily think that either approach is the final solution to upsampling, but they do fix the checkerboard artifacts.

## 相關頁面

- [上採樣](../methods/upsampling.md)
- [棋盤狀假影](../concepts/checkerboard-artifacts.md)
- [填充與步幅](../methods/padding-and-stride.md)
- [卷積運算](../methods/convolution-operation.md)
- [池化](../methods/pooling.md)
- [正則化與預條件](../methods/regularization-and-preconditioning.md)
