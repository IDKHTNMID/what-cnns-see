# 簡報大綱：CNN 看到什麼

狀態：已確認（2026-11-23）

- 讀者：不熟 CNN 的人
- 主線：先懂 CNN 怎麼看圖，再問一個神經元、一張圖、一整層，最後問這些解釋能信多少
- 跳讀：學過 CNN 的人從第 6 頁開始
- 全程地圖：影像 → 低層特徵圖 → 中層特徵圖 → 高層特徵圖 → logit → softmax → 類別機率
- 範圍：只用 `wiki/` 的內容
- 不講：感受野公式、轉置卷積的矩陣細節、預條件的數學、經典架構、ReLU 的原理
- 自繪圖：只用方塊、箭頭和 Wiki 裡有的數字，每個標籤都要有 Wiki 依據

## 第 1 頁：CNN 到底看到什麼？

- 段落：開場
- 帶走：這份簡報沿著「影像 → 一層層特徵圖 → logit → softmax → 類別機率」這條路，看網路中間看到什麼。
- Wiki：`index.md`、`concepts/feature-map.md`、`methods/feature-visualization.md`
- 圖：自繪全程地圖，之後每頁都用它標出現在的位置
- 地圖位置：全部

## 第 2 頁：看圖為什麼不直接用全連接層？

- 段落：基礎
- 帶走：1000×1000 的影像接同樣大小的隱藏表示，全連接層要 10¹² 個參數；加上平移不變性降到 4×10⁶，再加上局部性降到 4Δ²。
- Wiki：`concepts/convolutional-layer.md`、`concepts/translation-invariance.md`、`concepts/locality.md`
- 圖：自繪參數量下降的三階段
- 地圖位置：影像 → 低層特徵圖

## 第 3 頁：卷積實際上怎麼算？

- 段落：基礎
- 帶走：窗口滑過輸入，每個位置把對應的值相乘再加總；卷積核 [1, −1] 就能偵測垂直邊緣。
- Wiki：`methods/convolution-operation.md`
- 圖：`raw/d2l-ch7/_images/correlation.svg`
- 互動：一步步移動窗口，旁邊同步顯示 19、25、37、43 的算式；接著用 [1, −1] 算一列黑白影像，看邊緣變成 1 和 −1
- 地圖位置：影像 → 低層特徵圖

## 第 4 頁：一層的輸出長什麼樣子？

- 段落：基礎
- 帶走：一層的輸出叫特徵圖；x、y 軸是影像上的位置，z 軸是通道。
- Wiki：`concepts/feature-map.md`、`concepts/channel.md`
- 圖：`raw/d2l-ch7/_images/conv-multi-in.svg`
- 地圖位置：低層特徵圖

## 第 5 頁：後面的層為什麼看得到更大範圍？

- 段落：基礎
- 帶走：感受野是可能影響某個元素的所有前層元素，網路越深越大；步幅和池化可以用來降採樣。
- Wiki：`methods/padding-and-stride.md`、`methods/pooling.md`、`concepts/receptive-field.md`
- 圖：`raw/screenshots/computing-receptive-fields/fig05.png`
- 地圖位置：低層特徵圖 → 高層特徵圖

## 第 6 頁：怎麼知道一個神經元在找什麼？

- 段落：一個神經元
- 帶走：從雜訊出發，依導數一步步調整影像，讓目標變大，就能看神經元在找什麼。
- Wiki：`methods/feature-visualization.md`
- 圖：`raw/screenshots/feature-visualization/fig03.png`
- 地圖位置：中層特徵圖

## 第 7 頁：為什麼直接最佳化只得到雜訊？

- 段落：一個神經元
- 帶走：不加限制的最佳化會得到滿是雜訊和高頻圖樣的影像，要靠正則化和預條件。
- Wiki：`methods/regularization-and-preconditioning.md`、`concepts/checkerboard-artifacts.md`
- 圖：`raw/screenshots/feature-visualization/fig20.png`、`raw/screenshots/feature-visualization/fig30.png`
- 地圖位置：中層特徵圖

## 第 8 頁：各層分別在看什麼？

- 段落：一個神經元
- 帶走：GoogLeNet 由低到高，各層的通道依序像邊緣、紋理、圖案、部件、物體；這裡呼應第 3 頁的邊緣偵測。
- Wiki：`concepts/layer-abstraction.md`、`concepts/channel.md`
- 圖：`raw/screenshots/feature-visualization/fig00.png`
- 地圖位置：低層特徵圖 → 高層特徵圖

## 第 9 頁：一個神經元只看一種東西嗎？

- 段落：一個神經元
- 帶走：不一定；有些是多義神經元，同時回應幾種顯著概念，例如貓和車。
- Wiki：`methods/feature-visualization.md`、`concepts/semantic-dictionary.md`、`concepts/activation-space.md`
- 圖：`raw/feature-visualization/images/diversity/mixed4e_55_diversity.png`
- 地圖位置：高層特徵圖

## 第 10 頁：這張圖的每個位置，網路看到什麼？

- 段落：一張圖
- 帶走：把每個元素的激活向量畫出來排成網格，就能看網路在每個位置看到什麼。
- Wiki：`methods/activation-grid.md`、`concepts/semantic-dictionary.md`
- 圖：`raw/screenshots/building-blocks/fig06.png`
- 地圖位置：低層特徵圖 → 高層特徵圖

## 第 11 頁：網路為什麼判斷成這個類別？

- 段落：一張圖
- 帶走：歸因把一個神經元的影響估計成「激活值 × 提高激活值會讓輸出提高多快」；神經元太多時，可以用矩陣分解分成少數群組。
- Wiki：`methods/attribution.md`、`methods/matrix-factorization.md`
- 圖：自繪歸因算式；附原文連結 https://distill.pub/2018/building-blocks/#AttributionSpatial
- 地圖位置：高層特徵圖 → logit

## 第 12 頁：一整層能表示哪些概念？

- 段落：一整層
- 帶走：激活圖譜取樣一百萬個激活向量，降到二維、分格平均，再用特徵視覺化畫出來，看一層能表示的概念全貌。
- Wiki：`methods/activation-atlas.md`、`sources/activation-atlas.md`
- 圖：`raw/activation-atlas/assets/images/mixed4c-layout.jpg`
- 地圖位置：中層特徵圖

## 第 13 頁：同一個類別，不同層靠什麼判斷？

- 段落：一整層
- 帶走：判斷「消防船」時，mixed5b 集中在紅色的船和噴濺的水；往前的 mixed4d 分成窗戶、間歇泉和水花、像起重機的東西。
- Wiki：`concepts/layer-abstraction.md`、`methods/activation-atlas.md`
- 圖：`raw/activation-atlas/assets/images/renders/focus-1-1.jpg`、`raw/activation-atlas/assets/images/renders/focus-2-1.jpg`
- 地圖位置：中層特徵圖 → 高層特徵圖

## 第 14 頁：看懂之後，能改變它的判斷嗎？

- 段落：一整層
- 帶走：在灰鯨的照片上加一顆小棒球，最高分類就變成大白鯊；十種補丁各測 1,000 張影像，約五分之二被翻成目標類別，但只在一個模型上測過。
- Wiki：`concepts/multi-use-features.md`
- 圖：自繪補丁前後的分類變化；附原文連結 https://distill.pub/2019/activation-atlas/#shark-grey-whale
- 地圖位置：影像 → 類別機率

## 第 15 頁：這些解釋能信到什麼程度？

- 段落：收束
- 帶走：作者自己也列出限制：很多歸因技術被指出不可靠，正則化越強越可能出現誤導的相關，圖譜只能顯示取樣到的激活值。
- Wiki：`sources/building-blocks.md`、`sources/feature-visualization.md`、`sources/activation-atlas.md`
- 圖：無
- 地圖位置：全部
