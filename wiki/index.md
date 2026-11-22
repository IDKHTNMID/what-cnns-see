# 目錄：CNN 看到什麼

## 基礎（學過 CNN 可跳過）

- [卷積層](concepts/convolutional-layer.md) — 從全連接層加上兩個原則推出卷積層，參數從 10¹² 降到 4Δ²
- [平移不變性](concepts/translation-invariance.md) — 同一塊圖案不管出現在哪裡，早期層的反應都相似
- [局部性](concepts/locality.md) — 早期層只看局部區域，代價是每個單元只用到局部資訊
- [通道](concepts/channel.md) — 每個位置對應一個向量；通道不一定一對一對應某種特徵
- [卷積運算](methods/convolution-operation.md) — 卷積窗口的滑動計算、多通道與 1×1 卷積
- [填充與步幅](methods/padding-and-stride.md) — 補 0 讓輸出不縮小，步幅用來降採樣；輸出大小公式
- [池化](methods/pooling.md) — 沒有參數的最大值或平均值匯總，用來降採樣並減輕對位置的敏感

## 概念

- [感受野](concepts/receptive-field.md) — 可能影響某個元素的所有前層元素，網路越深越大；感受野大小、區域與有效感受野
- [激活空間](concepts/activation-space.md) — 神經元的激活值是基底向量，神經元的組合是空間裡的向量；隨機方向也常看得懂
- [棋盤狀假影](concepts/checkerboard-artifacts.md) — 產生影像時來自轉置卷積的不均勻重疊，梯度裡來自卷積層的反向傳播；池化的說法不一致
- [特徵圖](concepts/feature-map.md) — 一層的整個輸出；四種切法：神經元、元素、通道、神經元群組
- [語意字典](concepts/semantic-dictionary.md) — 每個神經元的激活值配上它的特徵視覺化，讓隱藏層有意義；多義神經元
- [多用途特徵](concepts/multi-use-features.md) — 一個偵測器回應幾種很不一樣但看起來相似的概念；照它做的補丁能改變分類
- [逐層抽象](concepts/layer-abstraction.md) — 越後面的層越具體、越接近類別；四篇的描述、組合出新概念、mixed3a 的說法不一致

## 方法

- [感受野的計算](methods/receptive-field-computation.md) — 由各層的卷積核大小、步幅、填充算出感受野大小、區域與中心；多路徑網路要對齊
- [特徵視覺化](methods/feature-visualization.md) — 從雜訊出發最佳化輸入，看神經元、通道、層或類別在找什麼；多樣性項
- [正則化與預條件](methods/regularization-and-preconditioning.md) — 壓掉高頻圖樣：頻率懲罰、變換穩健性、學習先驗，以及在去相關空間最佳化
- [上採樣](methods/upsampling.md) — 轉置卷積和 resize-convolution 怎麼把影像放大；不均勻重疊與比較表
- [激活網格](methods/activation-grid.md) — 把每個元素的激活向量畫出來排成網格，看網路在每個位置看到什麼
- [歸因](methods/attribution.md) — 激活值乘梯度的線性近似；空間歸因、通道歸因、層到層歸因，和顯著圖的比較
- [矩陣分解](methods/matrix-factorization.md) — 用 NMF 把特徵圖分成少數神經元群組，把資訊壓到人看得完；跨層相容
- [激活圖譜](methods/activation-atlas.md) — 取樣一百萬個激活向量，降維、分格平均後畫成圖譜；聚焦單一類別、類別激活圖譜

## 來源

- [d2l 第 7 章（7.1–7.5）](sources/d2l-ch7.md) — CNN 基礎：卷積層、填充與步幅、通道、池化
- [Computing Receptive Fields（2019）](sources/computing-receptive-fields.md) — 感受野大小與區域的閉式解、多路徑對齊、現代網路的感受野
- [Feature Visualization（2017）](sources/feature-visualization.md) — 用最佳化看 GoogLeNet 各層在找什麼：目標、多樣性、神經元互動、正則化光譜、預條件
- [Deconvolution and Checkerboard Artifacts（2016）](sources/deconv-checkerboard.md) — 棋盤狀假影的成因與 resize-convolution 解法；梯度裡的假影
- [The Building Blocks of Interpretability（2018）](sources/building-blocks.md) — 把特徵視覺化、歸因、矩陣分解組成可解釋性介面；語意字典、激活網格、神經元群組
- [Exploring Neural Networks with Activation Atlases（2019）](sources/activation-atlas.md) — 激活圖譜：一層能表示的概念全貌、逐層變化、類別激活圖譜、多用途特徵與補丁

## 名詞表

- [名詞表](glossary.md) — 術語的主名詞、別名、出處與用語依據
