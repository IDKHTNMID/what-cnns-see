# 通道

## 是什麼

彩色影像有紅、綠、藍三個通道（channel），所以影像不是二維，而是高 × 寬 × 通道的三階張量，例如 1024×1024×3。前兩個軸是空間關係，第三個軸可以看成替每個像素位置配一個多維的表示（[d2l](../sources/d2l-ch7.md) § 7.1.4. Channels）。這個軸叫通道維度（channel dimension）（[d2l](../sources/d2l-ch7.md) § 7.4. Multiple Input and Multiple Output Channels）。

> 原文（d2l-ch7）：While the first two of these axes concern spatial relationships, the third can be regarded as assigning a multidimensional representation to each pixel location.

隱藏表示也寫成三階張量：每個空間位置對應一整個向量，可以想成好幾張二維格子疊在一起，每一張就是一個通道（[d2l](../sources/d2l-ch7.md) § 7.1.4. Channels）。

> 原文（d2l-ch7）：We could think of the hidden representations as comprising a number of two-dimensional grids stacked on top of each other.

本 Wiki 的用法：一張二維格子叫「通道」，一層卷積層的整個輸出叫「特徵圖（feature map）」。d2l 在 7.2.6 節把卷積層的輸出叫特徵圖，在 7.1.4 節也把單一張二維格子叫特徵圖，這個用法本 Wiki 不採用（[d2l](../sources/d2l-ch7.md) § 7.1.4. Channels；[d2l](../sources/d2l-ch7.md) § 7.2.6. Feature Map and Receptive Field）。

> 原文（d2l-ch7）：They are also sometimes called feature maps, as each provides a spatialized set of learned features for the subsequent layer.

computing-receptive-fields 也把第 $l$ 層的整個輸出叫特徵圖，寫成 $f_l \in R^{h_l \times w_l \times d_l}$；第三維 $d_l$ 原文叫 depth，就是通道數。本 Wiki 的「深度」只指網路的層數（[Computing Receptive Fields](../sources/computing-receptive-fields.md) § Problem setup；[Computing Receptive Fields](../sources/computing-receptive-fields.md) § Discussion: receptive fields of modern networks）。

> 原文（computing-receptive-fields）：Define feature map \(f_l \in R^{h_l\times w_l\times d_l}\) to denote the output of the \(l\)-th layer, with height \(h_l\), width \(w_l\) and depth \(d_l\).

直覺上，靠近輸入的低層可能有些通道專門辨認邊緣，有些辨認紋理（[d2l](../sources/d2l-ch7.md) § 7.1.4. Channels）。但實際情況更複雜：通道是一起被最佳化、一起發揮作用的，所以不一定是單一通道對應邊緣偵測器，可能是通道空間裡的某個方向對應偵測邊緣（[d2l](../sources/d2l-ch7.md) § 7.4.2. Multiple Output Channels）。

> 原文（d2l-ch7）：This means that rather than mapping a single channel to an edge detector, it may simply mean that some direction in channel space corresponds to detecting edges.

Feature Visualization 用最佳化把 GoogLeNet 各層的通道畫出來：低層的結果像邊緣，往上依序像紋理、圖案、部件、物體，見[特徵視覺化](../methods/feature-visualization.md)（[Feature Visualization](../sources/feature-visualization.md) § Feature Visualization）。它對「方向」也有類似的說法：神經元的組合是激活空間裡的向量，隨機方向常常也看得懂，見[激活空間](activation-space.md)（[Feature Visualization](../sources/feature-visualization.md) § Interaction between Neurons）。

## 為什麼重要

局部性和平移不變性限制了卷積核，加入通道把一部分失去的複雜度補回來（[d2l](../sources/d2l-ch7.md) § 7.1.5. Summary and Discussion）。通道讓 CNN 能同時用多種特徵推理，例如邊緣偵測器和形狀偵測器，也在大幅減少參數和模型的表達力之間取得平衡（[d2l](../sources/d2l-ch7.md) § 7.4.4. Discussion）。

> 原文（d2l-ch7）：Adding channels allowed us to bring back some of the complexity that was lost due to the restrictions imposed on the convolutional kernel by locality and translation invariance.

主流架構通常越深通道越多，用降採樣犧牲空間解析度，換取更多通道（[d2l](../sources/d2l-ch7.md) § 7.4.2. Multiple Output Channels）。

> 原文（d2l-ch7）：In the most popular neural network architectures, we actually increase the channel dimension as we go deeper in the neural network, typically downsampling to trade off spatial resolution for greater channel depth.

代價是計算量：輸入、輸出通道數 $c_i$、$c_o$ 會直接乘進成本 $\mathcal{O}(h \cdot w \cdot k^2 \cdot c_i \cdot c_o)$（[d2l](../sources/d2l-ch7.md) § 7.4.4. Discussion）。

## 和其他概念的關係

- [卷積運算](../methods/convolution-operation.md)：多輸入通道時各通道分別做卷積再相加；每個輸出通道有自己的一組卷積核（[d2l](../sources/d2l-ch7.md) § 7.4.1. Multiple Input Channels；[d2l](../sources/d2l-ch7.md) § 7.4.2. Multiple Output Channels）。1×1 卷積只在通道維度上計算（[d2l](../sources/d2l-ch7.md) § 7.4.3. 1×1 Convolutional Layer）。
- [池化](../methods/pooling.md)：每個通道分開池化，輸出通道數等於輸入通道數（[d2l](../sources/d2l-ch7.md) § 7.5.3. Multiple Channels）。
- [局部性](locality.md)與[平移不變性](translation-invariance.md)：通道補回這兩個限制拿掉的複雜度（[d2l](../sources/d2l-ch7.md) § 7.1.5. Summary and Discussion）。
- [感受野](receptive-field.md)：通道數不影響感受野的計算（[Computing Receptive Fields](../sources/computing-receptive-fields.md) § Problem setup）。
- [特徵視覺化](../methods/feature-visualization.md)：通道目標 $	ext{layer}_n[:,:,z]$ 讓一整個通道所有空間位置的值變大；原文大部分的圖片用這個目標（[Feature Visualization](../sources/feature-visualization.md) § Optimization Objectives）。
- [激活空間](activation-space.md)：通道裡的每個值是一個神經元，神經元的組合是激活空間裡的向量（[Feature Visualization](../sources/feature-visualization.md) § Optimization Objectives；[Feature Visualization](../sources/feature-visualization.md) § Interaction between Neurons）。

## 相關頁面

- [d2l 第 7 章](../sources/d2l-ch7.md)
- [Computing Receptive Fields](../sources/computing-receptive-fields.md)
- [感受野](receptive-field.md)
- [卷積層](convolutional-layer.md)
- [卷積運算](../methods/convolution-operation.md)
- [池化](../methods/pooling.md)
- [Feature Visualization](../sources/feature-visualization.md)
- [特徵視覺化](../methods/feature-visualization.md)
- [激活空間](activation-space.md)
