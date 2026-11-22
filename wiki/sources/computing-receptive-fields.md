# 計算卷積神經網路的感受野（Computing Receptive Fields of Convolutional Neural Networks）

- 作者：André Araujo、Wade Norris、Jack Sim ／ 年份：2019 ／ 原文：https://distill.pub/2019/computing-receptive-fields/ ／ 授權：CC BY 4.0

## 一句話

推導全卷積網路的感受野大小，以及輸出元素在輸入影像上對應的區域：先給單一路徑網路的閉式解，再推廣到有多條路徑的計算圖，最後用開源函式庫算出現代網路的感受野（§ 全文）。

## 重點

**1. 感受野是把輸出元素對應回輸入的關鍵參數。** 作者想知道輸入能影響輸出到什麼程度，並把網路裡任何一處的元素對應回產生它的輸入區域；原文把感受野定義成這個區域的大小（§ Computing Receptive Fields of Convolutional Neural Networks）。這類計算過去多半手算，既繁瑣又容易出錯，因為沒有函式庫能自動算（§ Computing Receptive Fields of Convolutional Neural Networks）。

> 原文（computing-receptive-fields）：The key parameter to associate an output feature to an input region is the receptive field of the convolutional network, which is defined as the size of the region in the input that produces the feature.

**2. 單一路徑網路的感受野大小有閉式解。** 從最後一層往回推，每層用遞迴式 $r_{l-1} = s_l \cdot r_l + (k_l - s_l)$；解開後只需要各層的卷積核大小和步幅，不需要填充（§ Computing receptive field size）。

> 原文（computing-receptive-fields）：Finally, note that padding does not need to be taken into account for this derivation.

**3. 先算好三個量，就能把任何輸出元素對回輸入區域。** 有效步幅 $S_0$、有效填充 $P_0$ 和感受野大小 $r_0$ 算好之後，由輸出元素的位置就能算出它在輸入影像上的區域左右端與中心；相鄰輸出元素的感受野中心相距 $S_0$（§ Computing receptive field region in input image）。

> 原文（computing-receptive-fields）：When one is interested in computing feature locations for a given network, it is handy to pre-compute three variables: \(P_0,S_0,r_0\).

**4. 多路徑網路要考慮對齊。** ResNet、Inception 這類網路從輸入到輸出有多條路徑；各路徑對應到的輸入區域可能沒對齊，這時感受野大小可能隨輸出元素的位置改變（§ Arbitrary computation graphs）。網路對齊時，整個網路的感受野大小是各路徑中最大的；依反向拓撲順序走一次計算圖，就能算出整個網路的感受野參數（§ Arbitrary computation graphs）。

> 原文（computing-receptive-fields）：This means that the receptive field size may not be shift-invariant when the network is not aligned.

**5. 現代網路的感受野越來越大。** 從 AlexNet、VGG 到 ResNet、Inception，感受野隨層數增加而變大，最新的網路通常蓋住整張輸入影像；ImageNet 準確率和感受野大小呈對數關係（§ Discussion: receptive fields of modern networks）。

> 原文（computing-receptive-fields）：In the most recent networks, the receptive field usually covers the entire input image: this means that the context used by each feature in the final output feature map includes all of the input pixels.

## 方法

對象是有 $L$ 層的全卷積網路（fully-convolutional network，FCN）；第 $l$ 層的輸出是特徵圖 $f_l$，輸入影像記成 $f_0$（§ Problem setup）。推導只看一維訊號，二維影像的每個維度分開套用；每層用卷積核大小、步幅、左側填充、右側填充四個參數描述（§ Problem setup）。

> 原文（computing-receptive-fields）：To simplify the presentation, the derivations presented in this document consider \(1\)-dimensional input signals and feature maps.

適用的層不只卷積，池化、非線性、相加這類輸出只依賴局部輸入的運算都算；逐元素運算的卷積核大小當成 1（§ Problem setup）。每層的第一個輸出元素，是把卷積核放在輸入（含填充）最左邊算出來的，主要的深度學習函式庫都用這個慣例（§ Problem setup）。

> 原文（computing-receptive-fields）：We adopt the convention where the first output feature for each layer is computed by placing the kernel on the left-most position of the input, including padding.

推導先寫出從後一層推回前一層的遞迴式，再兩邊乘上前面各層步幅的乘積、從第 1 層加到第 $L$ 層，消去中間項得到閉式（§ Solving recurrence equations: receptive field size；§ Solving recurrence equations: receptive field region）。多路徑網路則依反向拓撲順序走訪計算圖（§ Arbitrary computation graphs）。現代網路的數值用作者的開源函式庫算出，模型和 ImageNet 準確率取自 TF-Slim 影像分類模型庫（§ Discussion: receptive fields of modern networks）。

## 結論

- 從 AlexNet、VGG 到 ResNet、Inception，感受野隨層數增加而變大，最新的網路通常蓋住整張輸入影像（§ Discussion: receptive fields of modern networks）。
- 分類準確率和感受野大小呈對數關係，表示高階辨識任務需要大感受野，但效益遞減（§ Discussion: receptive fields of modern networks）。
- MobileNet 用 depth-wise 卷積，以很小的計算量得到大感受野；VGG-16 的 FLOPs 是 MobileNet 的 27 倍，感受野卻比較小，準確率只高一點；這表示能有效率產生大感受野的網路，辨識效能可能比較好（§ Discussion: receptive fields of modern networks）。

> 原文（computing-receptive-fields）：We observe a logarithmic relationship between classification accuracy and receptive field size, which suggests that large receptive fields are necessary for high-level recognition tasks, but with diminishing rewards.

各模型的感受野大小 $r$、有效步幅 $S$、有效填充 $P$（§ Discussion: receptive fields of modern networks）：

| 模型 | $r$ | $S$ | $P$ | 年份 | 出處 |
|---|---|---|---|---|---|
| alexnet_v2 | 195 | 32 | 64 | 2014 | （§ Discussion: receptive fields of modern networks） |
| vgg_16 | 212 | 32 | 90 | 2014 | （§ Discussion: receptive fields of modern networks） |
| mobilenet_v1 | 315 | 32 | 126 | 2017 | （§ Discussion: receptive fields of modern networks） |
| mobilenet_v1_075 | 315 | 32 | 126 | 2017 | （§ Discussion: receptive fields of modern networks） |
| resnet_v1_50 | 483 | 32 | 239 | 2015 | （§ Discussion: receptive fields of modern networks） |
| inception_v2 | 699 | 32 | 318 | 2015 | （§ Discussion: receptive fields of modern networks） |
| resnet_v1_101 | 1027 | 32 | 511 | 2015 | （§ Discussion: receptive fields of modern networks） |
| inception_v3 | 1311 | 32 | 618 | 2015 | （§ Discussion: receptive fields of modern networks） |
| resnet_v1_152 | 1507 | 32 | 751 | 2015 | （§ Discussion: receptive fields of modern networks） |
| resnet_v1_200 | 1763 | 32 | 879 | 2015 | （§ Discussion: receptive fields of modern networks） |
| inception_v4 | 2071 | 32 | 998 | 2016 | （§ Discussion: receptive fields of modern networks） |
| inception_resnet_v2 | 3039 | 32 | 1482 | 2016 | （§ Discussion: receptive fields of modern networks） |

## 限制

- 感受野大小不是準確率提升的唯一因素，網路深度（層數）、寬度（每層的卷積核數）等其他因素也很重要；作者推測大感受野是必要的，但絕不充分，還需要實驗確認，例如改變不同架構的卷積核大小和步幅，看準確率怎麼變（§ Discussion: receptive fields of modern networks）。
- 感受野大小只量範圍：區域裡每個輸入像素的影響並不相同，越靠中心的像素影響越大（§ Discussion: receptive fields of modern networks）。
- 用了填充時，邊界元素的感受野會包含填充的區域，所以每個輸出元素在原影像上實際用到的大小可能不同（§ Computing receptive field size）。

> 原文（computing-receptive-fields）：In other words, while we conjecture that a large receptive field is necessary, by no means it is sufficient.

## 相關頁面

- [感受野](../concepts/receptive-field.md)
- [感受野的計算](../methods/receptive-field-computation.md)
- [填充與步幅](../methods/padding-and-stride.md)
- [池化](../methods/pooling.md)
- [通道](../concepts/channel.md)
- [d2l 第 7 章](d2l-ch7.md)
