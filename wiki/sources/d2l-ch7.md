# 動手學深度學習 第 7 章：卷積神經網路（Dive into Deep Learning, Chapter 7: Convolutional Neural Networks）

- 作者：Aston Zhang、Zachary C. Lipton、Mu Li、Alexander J. Smola ／ 年份：2023 ／ 原文：https://d2l.ai/chapter_convolutional-neural-networks/ ／ 授權：CC BY-SA 4.0
- 收錄範圍：7.1–7.5 的正文與圖，不含程式碼與習題。

## 一句話

從全連接層出發，加上平移不變性和局部性兩個原則，推導出卷積層；再說明卷積層實際怎麼計算、控制輸出大小的填充與步幅、多個通道，以及池化（§ 全文）。

## 重點

**1. 卷積層是從兩個原則推出來的。** 早期層對同一塊圖案不管它在哪裡都要有相似的反應（平移不變性），而且只看局部區域（局部性）；第三個要求是越深的層要能抓到越大範圍的特徵（§ 7.1.1. Invariance）。

> 原文（d2l-ch7）：This principle is called translation invariance (or translation equivariance).

**2. 參數量大幅下降。** 把 1000×1000 的影像接到同樣大小的隱藏表示，全連接層要 $10^{12}$ 個參數；加上平移不變性後降到 $4 \times 10^6$；再加上局部性降到 $4\Delta^2$，$\Delta$ 通常小於 10（§ 7.1.2. Constraining the MLP；§ 7.1.2.1. Translation Invariance；§ 7.1.2.2. Locality）。代價是歸納偏置：如果影像其實不符合這些假設，模型可能連訓練資料都擬合不好（§ 7.1.2.2. Locality）。

> 原文（d2l-ch7）：As such, we reduced the number of parameters by another four orders of magnitude.

**3. 卷積層實際算的是互相關。** 嚴格的卷積要先把卷積核上下左右翻轉；但卷積核是從資料學出來的，兩種算法得到的輸出一樣，所以照深度學習的慣例仍叫卷積（§ 7.2.1. The Cross-Correlation Operation；§ 7.2.5. Cross-Correlation and Convolution）。

> 原文（d2l-ch7）：In keeping with standard terminology in deep learning literature, we will continue to refer to the cross-correlation operation as a convolution even though, strictly-speaking, it is slightly different.

**4. 通道。** 每個空間位置對應一整個向量；多輸入通道時各通道分別做卷積再相加，每個輸出通道各有一組卷積核；1×1 卷積只在通道維度上計算（§ 7.1.4. Channels；§ 7.4.1. Multiple Input Channels；§ 7.4.2. Multiple Output Channels；§ 7.4.3. 1×1 Convolutional Layer）。一個通道不一定對應一種特徵，可能是通道空間裡的某個方向對應偵測邊緣（§ 7.4.2. Multiple Output Channels）。

> 原文（d2l-ch7）：Instead, channels are optimized to be jointly useful.

**5. 感受野與池化。** 感受野是前向傳播中可能影響某個元素的所有前層元素，網路越深感受野越大（§ 7.2.6. Feature Map and Receptive Field）。池化沒有參數，每個通道分開做；它降低空間解析度、讓感受野長得更快，並減輕卷積層對位置的敏感（§ 7.5. Pooling；§ 7.5.3. Multiple Channels）。

> 原文（d2l-ch7）：This section introduces pooling layers, which serve the dual purposes of mitigating the sensitivity of convolutional layers to location and of spatially downsampling representations.

## 方法

本章從第一原則推導 CNN 的結構，作者也說明不確定這是不是當初發明 CNN 的路徑（§ 7.1.5. Summary and Discussion）。

> 原文（d2l-ch7）：In this section we derived the structure of convolutional neural networks from first principles.

每種運算都先用小矩陣手算一次（例如 3×3 輸入配 2×2 卷積核），再寫成函式，用圖上的數值驗證輸出；1×1 卷積另外用全連接層實作，確認結果和先前的多通道函式相同（§ 7.2.1. The Cross-Correlation Operation；§ 7.4.3. 1×1 Convolutional Layer；§ 7.5.1. Maximum Pooling and Average Pooling）。邊緣偵測的例子先手動設計卷積核 [1, −1]，再只看輸入輸出對、用平方誤差和梯度把卷積核學回來（§ 7.2.3. Object Edge Detection in Images；§ 7.2.4. Learning a Kernel）。

## 結論

- 卷積層的核心計算很簡單，一個巢狀迴圈就能算出來；而且計算高度局部，因此能做大量硬體最佳化（§ 7.2.7. Summary）。
- 不必由人設計卷積核，可以直接從資料學出來（§ 7.2.7. Summary）。
- 通道把被局部性和平移不變性拿掉的一部分複雜度補回來，讓 CNN 能同時用多種特徵推理（§ 7.1.5. Summary and Discussion；§ 7.4.4. Discussion）。
- 兩種常見的池化中，最大池化比平均池化好，因為它讓輸出有一定程度的不變性；常用 2×2 的池化窗口把空間解析度降為四分之一（§ 7.5.4. Summary）。

> 原文（d2l-ch7）：Instead, we can simply learn them from data.

## 限制

- 歸納偏置和現實不符時，模型可能連訓練資料都擬合不好（§ 7.1.2.2. Locality）。
- 通道帶來計算成本：$h \times w$ 的影像配 $k \times k$ 卷積核、$c_i$ 個輸入通道和 $c_o$ 個輸出通道，成本是 $\mathcal{O}(h \cdot w \cdot k^2 \cdot c_i \cdot c_o)$（§ 7.4.4. Discussion）。
- 「每個通道對應一種特徵」只是直覺，實際情況更複雜（§ 7.4.2. Multiple Output Channels）。
- 零填充以外還有很多填充方式，但何時該用非零填充沒有明確結論（§ 7.3.3. Summary and Discussion）。

> 原文（d2l-ch7）：For a \(256 \times 256\) pixel image with a \(5 \times 5\) kernel and \(128\) input and output channels respectively this amounts to over 53 billion operations (we count multiplications and additions separately).

## 相關頁面

- [卷積層](../concepts/convolutional-layer.md)
- [平移不變性](../concepts/translation-invariance.md)
- [局部性](../concepts/locality.md)
- [通道](../concepts/channel.md)
- [感受野](../concepts/receptive-field.md)
- [卷積運算](../methods/convolution-operation.md)
- [填充與步幅](../methods/padding-and-stride.md)
- [池化](../methods/pooling.md)
