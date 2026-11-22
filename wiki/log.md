# 紀錄

只往後加。每筆開頭用 `## [YYYY-MM-DD] 類型 | 標題`。

## [2026-11-22] setup | 建立 Wiki 結構

- 需求訪談 11 題、補問 2 題，需求摘要兩輪確認後定案（見 `需求摘要.md`）。
- 生成 `AGENTS.md`、`CLAUDE.md`、資料夾結構與檢查程式。
- 5 篇 Distill 原文已存進 `raw/`；d2l 第 7 章在第一篇 ingest 時下載。

## [2026-11-22] ingest | Dive into Deep Learning, Chapter 7 (Sections 7.1–7.5)

- 新增：`sources/d2l-ch7.md`；概念頁 `convolutional-layer`、`translation-invariance`、`locality`、`channel`、`receptive-field`；方法頁 `convolution-operation`、`padding-and-stride`、`pooling`。
- 更新：`index.md`（基礎區 7 頁、概念區 1 頁、來源區 1 頁）、`glossary.md`（20 個名詞）。
- 名詞決定（使用者已確認）：
  - 卷積為主名詞，互相關列為別名；d2l 說明照深度學習慣例把互相關叫卷積。嚴格卷積只在說明名稱由來時使用。
  - 卷積核為主名詞，濾波器、權重列為別名。
  - 通道指一張二維格子；特徵圖只指一層卷積層的整個輸出。d2l 7.1.4 節也把單一通道叫特徵圖，本 Wiki 不採用。
  - 平移不變性為主名詞，平移等變性照 d2l 原文列為別名。
  - 中文譯名：卷積、卷積核、通道、特徵圖、感受野、填充、步幅、池化、局部性。
- 感受野放在概念區，不放在可跳過的基礎區，因為下一篇 computing-receptive-fields 會擴充。
- 說法不一致：無（目前只有一篇來源）。
- 圖：d2l 自己畫的 7 張 SVG 全部使用；Waldo 照片與 Field (1987) 的圖只附原文連結。
- 檢查：第 1 輪通過。之後逐句對原文修了 2 處推論過頭的說法，再跑一次也通過。
- 檢查程式：`check_quotes.py` 的小節標題比對改成忽略 d2l 的 ¶ 後按鈕文字與行內數學（`\(1\times 1\)` 可寫成 `1×1`），並加了測試。
- 修正（同日）：頁面裡把別名「互相關」「濾波器」當一般用語的地方改回主名詞，別名只留在說明名稱由來的段落與名詞表；名詞表的用語依據改成可以對照原文的小節；來源頁「方法」段改正驗證方式的描述。檢查再跑一次，通過。
- 已知限制：`check_quotes.py` 比對小節標題時會去掉節號，所以節號寫錯（例如 `§ 7.9.9. Summary`）也會通過；d2l 有 Summary、Summary and Discussion、Padding and Stride 三個標題各出現兩次。

## [2026-11-22] setup | 規則補充：獨立作業

- 使用者要求這份 Wiki 和他的個人知識庫分開：需求摘要加第 50 條，`AGENTS.md` 第 11 節加一條。Wiki 的頁面、log、名詞表只寫在這個 repo，也不從個人知識庫取材。

## [2026-11-22] ingest | Computing Receptive Fields of Convolutional Neural Networks

- 新增：`sources/computing-receptive-fields.md`；方法頁 `receptive-field-computation`（大小、區域與中心、多路徑對齊三個小節）。
- 更新：`concepts/receptive-field.md`（感受野大小與區域、有效感受野、現代網路）、`concepts/channel.md`、`methods/padding-and-stride.md`、`methods/pooling.md`、`index.md`（方法區 1 頁、來源區 1 頁）、`glossary.md`（新增 12 條，共 32 條）。
- 名詞決定（使用者已確認）：
  - 新名詞：感受野大小、感受野區域、感受野中心、有效步幅、有效填充、有效感受野、對齊、計算圖、全卷積網路。原文只有英文，中文譯名是提案後確認的。
  - 特徵圖上的一個位置叫元素，這篇的 feature 列為別名；d2l 同一句話用 element 指位置、用 feature 指偵測到的東西。
  - 深度只指網路的層數；這篇用 depth 指通道數的地方寫成通道數，MobileNet 的 depth-wise 卷積保留英文。`channel.md` 原本的「通道深度」一併改掉。
  - d2l 留下的譯名一併確認：歸納偏置、卷積神經網路、嚴格卷積、1×1 卷積、卷積窗口、通道維度、池化窗口；降採樣補進名詞表。
- 說法不一致：無。d2l 把感受野定義成一組元素，這篇定義成區域的大小；判斷是量法不同、不是矛盾，所以當名詞處理（感受野、感受野大小、感受野區域），並在感受野頁註明區域中間可能有沒用到的元素。
- 符號：d2l 的 $p_h$ 是總共補幾列，這篇的 $p_l$、$q_l$ 是左、右各補幾個；在填充與步幅頁和方法頁的符號表各寫一行。
- 不收：附錄的其他運算（擴張卷積、上採樣、可分離卷積、批次正規化）；準確率對感受野的泡泡圖只寫文字結論。
- 圖：6 張 JS 圖的截圖（fig00、fig03、fig04、fig05、fig06、fig07），都打開看過。
- 截圖程式：圖裡的標籤會超出圖框（fig04 底下的標籤被切掉一半、fig00 的參數值沒出現），改成依圖內元素的實際範圍截，超出上限 24px、四周留 8px，並加了測試。一次截多張時有一半逾時，逾時之後下一張也截壞（縮成一半、混進正文），改成每張分開跑，程式說明補上這個做法。
- 檢查：第 1 輪 1 個問題（表格前的引言句沒標出處），第 2 輪通過。之後逐句對原文修了 2 處推論過頭的說法（「會」改「可能」、「填充會移動區域」改成「區域位置和填充有關」），再跑一次也通過。
- 修正（同日）：方法頁一處把這篇的 feature 寫成「特徵」，改回主名詞「元素」；填充與步幅頁註明對齊條件裡的填充是左側的 $p_l$（那頁的 $p_h$ 是總數）；來源頁結論的「表示」改成「作者認為這暗示」。檢查再跑一次，通過。

## [2026-11-22] ingest | Feature Visualization

- 新增：`sources/feature-visualization.md`；方法頁 `feature-visualization`、`regularization-and-preconditioning`；概念頁 `activation-space`。
- 更新：`concepts/channel.md`（通道目標、各層的視覺化、和激活空間的連結）、`methods/padding-and-stride.md` 和 `methods/pooling.md`（反向傳播時梯度出現棋盤狀圖樣）、`index.md`（概念區 1 頁、方法區 2 頁、來源區 1 頁）、`glossary.md`（新增 21 條，共 53 條；元素的解釋收緊）。
- 名詞決定（使用者已確認）：
  - 新增神經元，只指 $\text{layer}_n[x,y,z]$；元素收緊成特徵圖上的一個空間位置，一個元素上有通道數那麼多個神經元。
  - 原文把用通道目標畫的例子也叫 neuron、圖說標成 unit；講具體例子時照原文標籤寫（例如 mixed5a 層 unit 9），方法頁註明一次。
  - activation 譯成「激活」（激活值、激活空間），依 d2l 中文版的「激活函數」。
  - d2l 的 channel space 和這篇的 activation space 不合併；通道頁和激活空間頁各寫「有類似的說法」，互相連結。
  - 新譯名：特徵視覺化、歸因、最佳化目標、資料集範例、多樣性項、Gram 矩陣、對抗樣本、高頻圖樣、正則化、頻率懲罰、總變差、變換穩健性、學習先驗、預條件、參數化、去相關、最陡下降方向、抖動。logits、softmax、DeepDream、GoogLeNet 保留英文。
- 說法不一致：無。Szegedy 和 Bau 對「隨機方向是否和基底方向一樣好解讀」結論不同，這篇自己整合了兩者，照這篇寫在激活空間頁。
- 規則：`AGENTS.md` §3 補一條：資料集照片也算別人的圖，能分開下載的只取作者產生的圖，照片和作者的圖畫在同一張 JS 圖裡的整張只附連結。§8「圖見原文」的範例原本把 § 放在連結文字裡，和檢查程式衝突（見檢查第 1 輪），改成連結文字不放 §，和前兩篇的寫法一致。
- 圖：
  - 截圖 7 張（fig00、fig03、fig04、fig20、fig24、fig26、fig30），都打開看過；fig20、fig30 的縮圖放大確認過是最佳化結果，不是資料集照片。
  - fig19 連兩次逾時，改截它裡面的子圖 fig20（內容相同，少了圖說）。兩個神經元一起最佳化的圖（fig15，裡面的子圖 fig16 也一樣）比 1000px 的視窗高，改附原文連結；這張是作者自己的圖，所以沒列進 Figures not stored here。
  - 多樣性的兩組例子只下載 `*_optimized.png` 和 `*_diversity.png`；資料集照片（多樣性例子 4 張、開頭對照圖 2 張）和 3 張混了照片的 JS 圖列進 Figures not stored here，頁面只附連結。前人研究的光譜圖改寫成表格並附連結。
- 截圖程式（f748d34）：Distill 後半的圖原本會截成正文或空白。原因是捲到圖時上方的圖片才載入，版面往下推了 585px，程式還用舊座標截。改成只截視窗內、等圖裡的圖片載完、截圖前後位置一樣才保留；測試從 29 個增加到 38 個。單張偶爾仍會逾時，重跑即可。
- 檢查：第 1 輪 6 個問題（「圖見原文」的連結文字有 §，被當成出處解析），第 2 輪通過。之後逐句對原文修了 1 處推論過頭的說法（「任何方向都可以當最佳化目標」改成「方向也可以」），再跑一次也通過。
- 修正（同日）：通道頁「隨機方向常常也看得懂」補回「但比例低於基底方向」；方法頁、來源頁和名詞表的「一次最佳化好幾張」「同一批」改成原文的「多個例子」；激活空間頁 3 個「圖見原文」連結標明各自是哪張圖；多樣性例子的圖說「上面／下面」改成「第一張／第二張」。檢查再跑一次，通過。

## [2026-11-23] ingest | Deconvolution and Checkerboard Artifacts

- 新增：`sources/deconv-checkerboard.md`；方法頁 `upsampling`；概念頁 `checkerboard-artifacts`。
- 更新：`methods/padding-and-stride.md`（一般有步幅的卷積可能也有問題、GAN 鑑別器、轉置卷積的不均勻重疊）、`methods/convolution-operation.md`（卷積層的反向傳播就是轉置卷積）、`methods/pooling.md`（另一種說法，連到說法不一致段）、`methods/regularization-and-preconditioning.md`（DeepDream 的抖動）、`sources/feature-visualization.md`（相關頁面）、`index.md`（概念、方法、來源各 1 頁）、`glossary.md`（新增 17 條，共 70 條；對抗樣本加別名）。
- 名詞決定（使用者已確認）：
  - 轉置卷積當主名詞，反卷積（deconvolution）是別名。這篇為了簡短用 deconvolution，其他 5 篇都沒用到，依 PyTorch `nn.ConvTranspose2d`、TensorFlow `Conv2DTranspose` 的 API 名稱。
  - 棋盤狀假影當主名詞，artifacts 譯成假影；FV 那批頁面的「棋盤狀圖樣」改成棋盤狀假影（padding-and-stride、pooling、regularization-and-preconditioning 各 1 處），棋盤狀圖樣收為別名。
  - resize-convolution 保留英文。
  - 新譯名：上採樣、不均勻重疊、最近鄰插值、雙線性插值、子像素卷積、超解析度、生成對抗網路（GAN）、生成器、鑑別器、假影。
  - FV 補確認：白化、雙邊濾波器、潛在空間、去噪自編碼器，收進名詞表。
  - 這篇的 adversarial counter-examples 用既有的對抗樣本，收為別名。
- 說法不一致：池化在梯度裡造成什麼圖樣。這篇認為最大池化造成的是比較不規則的高頻圖樣；FV 說每個有步幅的卷積或池化都會造成棋盤狀假影。以 FV 為主軸，理由是比較新，寫在棋盤狀假影頁。building-blocks 也說有步幅的最大池化會帶來棋盤狀圖樣，那篇 ingest 時補進同一段，理由再加上「兩篇支持」。
- 圖：
  - 截圖 2 張（fig01 一維重疊、fig03 兩層疊加），都打開看過。二維重疊的圖（fig02）是循環動畫，截圖程式抓到的是重置後的空白網格，改附原文連結。
  - 下載 29 個靜態圖：SVG 3 張（學到的權重兩張、三種上採樣寫成矩陣）、GAN 換掉轉置卷積前後 12 張、訓練前隨機權重的輸出 6 張、DeepDream 有沒有抖動 2 張、鑑別器步幅 2 和 1 各 3 張；都看過，是作者的實驗結果。
  - 風格轉換那組是拿照片做的，列進 Figures not stored here，頁面只附連結；開頭別人模型的樣本原本就列在那裡。這兩張圖在原文都沒有錨點，連結指向文章網址。
- 修正：名詞表的神經元、通道頁的通道目標，`\text` 的 `\t` 先前被當成 tab 吃掉，補回。
- 檢查：第 1 輪 1 個問題（說法不一致段的粗體標題那行沒有出處），第 2 輪通過。

## [2026-11-23] ingest | The Building Blocks of Interpretability

- 新增：`sources/building-blocks.md`；概念頁 `feature-map`、`semantic-dictionary`；方法頁 `activation-grid`、`attribution`、`matrix-factorization`。
- 更新：`concepts/checkerboard-artifacts.md`（說法不一致段加這篇）、`methods/pooling.md`（放寬最大池化的梯度）、`concepts/channel.md`（通道也叫 detector；和特徵圖、歸因、語意字典的關係）、`concepts/activation-space.md`（多義神經元、旋轉語意字典、方向有語意；和三個新頁的關係）、`methods/feature-visualization.md`（語意字典也用以最佳化為基礎的特徵視覺化）、`sources/feature-visualization.md`（相關頁面）、`index.md`（概念 2 頁、方法 3 頁、來源 1 頁）、`glossary.md`（新增 18 條，共 88 條；通道、特徵圖、元素加別名，歸因拿掉 saliency maps 別名）。
- 名詞決定（使用者已確認）：
  - 這篇的 cube of activations 就是特徵圖，收為別名「激活立方體」；特徵圖頁補上四種切法。
  - 這篇的 spatial position／spatial location 用既有的元素，收為別名「空間位置」；頁面第一次出現時註明原文叫法。
  - 這篇把通道也叫 detector，收為通道的別名。
  - 顯著圖從歸因的別名獨立出來：FV 把 saliency maps 當成歸因的另一種叫法，這篇定義成歸因最常見的介面。照這篇的定義，歸因頁的比較段並列兩句原文。
  - 矩陣的一格寫「每一格」，不用元素。
  - 激活的複合詞沿用「激活」：激活向量、激活網格。
  - 新譯名：語意字典、激活向量、激活網格、空間歸因、通道歸因、層到層歸因、熱圖、降維、矩陣分解、非負矩陣分解（NMF）、神經元群組、多義神經元、路徑相依、可解釋性、可解釋性介面。
  - 寫名詞表時補收 CAM、ReLU，保留英文。
- 說法不一致：池化在梯度裡造成什麼圖樣。這篇說 GoogLeNet 有步幅的最大池化在梯度裡帶來很多雜訊和棋盤狀圖樣（原文在 § How Are Concepts Assembled? 的註腳），支持 FV 的說法，也和 deconv-checkerboard 說的不規則高頻圖樣不衝突。棋盤狀假影頁的主軸理由改成「比較新，而且 Building Blocks 也這樣說」。d2l 說偵測邊緣的可能是通道空間裡的某個方向，這篇說特徵不必是完美的偵測器；兩者不衝突，寫在通道頁的關係段，不列成說法不一致。
- 圖：
  - 截圖 2 張（fig06 四層的激活網格、fig12 介面的四個組成），都打開看過。
  - 下載 2 個 SVG（`images/design_space/empty.svg`、`teaser.svg`），是作者畫的介面文法圖，嵌在來源頁。
  - 文中的互動圖幾乎都畫在同一張輸入照片（拉布拉多幼犬和小貓）上：9 張 JS 圖和介面設計空間那段的 3 張步驟縮圖列進 Figures not stored here，頁面只附原文連結。原文 HTML 裡被註解掉的圖（`activation-pca.png`、`vector-eq-full.png`、`attribution-channels.png`）和 Neuron Attribution 小節不用。
- 寫法：激活網格第 2 步的最佳化目標只出現在 JS 產生的文字裡，`check_quotes.py --dump` 抓不到，所以只改寫、標出處並附 `#ActivationVecVis` 連結，不附原文句。
- 檢查：第 1 輪通過。寫頁面時先用 `check_quotes.py` 自查，把 4 處 `$$…$$` 的展示公式改成 math 區塊（`$$` 會被當成沒有出處的段落）。
- 修正（同日）：逐句對原文，拿掉 3 處推論過頭的說法：激活空間頁和語意字典頁的「旋轉後的成分是激活空間裡的其他方向」（原文只說讓成分更分得開）；通道頁「通道不一定乾淨」改回原文說的神經元，並拿掉對 "being run" 的引申；名詞表 ReLU 的「所以適合用 NMF」改成「NMF 的非負限制沒有問題」。SOURCES 的 9 張 JS 圖對照截圖確認過都畫在輸入照片上。檢查再跑一次，通過。
- lint 待辦：新頁把「空間位置」當一般用語（矩陣分解頁、來源頁、特徵圖頁、名詞表的矩陣分解列），它現在是元素的別名，lint 時和舊頁的「元素」用法一起掃。

## [2026-11-23] ingest | Exploring Neural Networks with Activation Atlases

- 新增：`sources/activation-atlas.md`；方法頁 `activation-atlas`（激活圖譜，含聚焦單一類別、類別激活圖譜兩小節，以及兩張比較表）；概念頁 `multi-use-features`（多用途特徵）、`layer-abstraction`（逐層抽象，使用者要求加的跨篇整合頁）。
- 更新：`methods/activation-grid.md`（這篇對激活網格的說明、只看一張影像的限制）、`methods/attribution.md`（激活圖譜的歸因向量小節、比較表加一列、Grad-CAM 原文句）、`methods/pooling.md`（這篇也放寬最大池化的梯度）、`methods/feature-visualization.md`（這篇的目標函數；從神經元到激活值的演進）、`methods/regularization-and-preconditioning.md`（沿用變換穩健性；白化激活空間）、`methods/matrix-factorization.md`（矩陣分解或許能呈現組合結構）、`concepts/activation-space.md`（組合結構、字母比喻、開頭的兩張圖、路徑只在投影裡平滑、和多用途特徵的區別）、`concepts/receptive-field.md`（後面的層感受野較大）、`concepts/semantic-dictionary.md`（多義神經元和多用途特徵）；BB、FV 來源頁的相關頁面。
- 名詞決定（使用者已確認）：
  - 主名詞 GoogLeNet，InceptionV1 收為別名：FV 和 BB 都叫 GoogLeNet，這篇叫 InceptionV1，並註明又叫 GoogLeNet。
  - activation atlas＝激活圖譜，class activation atlas＝類別激活圖譜。
  - 這篇的 spatial activation 用既有的激活向量，收為別名；feature inversion 收為特徵視覺化的別名。
  - 原文說同樣的 neurons 在每個區塊上都算一次，頁面寫通道，並註明原文叫 neurons；激活向量裡的每個值仍叫神經元。
  - 這篇的 detector 寫偵測器，指類別激活圖譜上的圖示（一格的平均激活向量），和 BB 指通道的 detector 不同。
  - patch 分開翻：神經元在前一層看的那一塊叫區塊，貼進影像的叫補丁；adversarial patch＝對抗補丁。
  - grid cell＝格子，和元素區分。
  - multi-use features＝多用途特徵，和多義神經元分開，兩頁互相連結。
  - 新譯名：歸因向量、流形、組合結構、分群、餘弦相似度、超參數、取樣。
  - 保留英文：t-SNE、UMAP、k-means、Grad-CAM；spherical k-means、DBSCAN、ImageNet 和層名只在頁面出現。
  - 寫名詞表時補一列「偵測器」：名詞決定裡有，但提案沒有列成名詞表的一列。
  - 最大池化梯度的 relaxation 沿用 BB 頁的「放寬」。
- 說法不一致：
  - 提案時判斷這篇和前幾篇沒有衝突。這篇描述歸因的那句話沒寫「激活值 ×」，但公式 $h_{x,y} \cdot \nabla_{h_{x,y}} \text{logit}_c$ 和 BB 一致，原文也說沿用 BB，所以照公式寫，不引那句。最大池化的放寬只說是為了減少雜訊，寫在池化頁，不放進棋盤狀假影的說法不一致段。
  - 寫逐層抽象頁時新發現一處：BB 說前面的層偵測邊緣（比較的最前一層是 mixed3a），FV 的圖把 mixed3a 標成紋理、邊緣標在 conv2d0。主流取 FV 的層名對照：FV 逐層標出，這篇說 mixed3b 是紋理和簡單圖案，兩篇一致；BB 那句描述的是整體趨勢。寫在逐層抽象頁的說法不一致段。
- 圖：
  - 下載 10 張作者產生的靜態圖，都打開看過：`overview-neuron.jpg`、`overview-pairwise.jpg`、`overview-atlas.jpg`、`mixed4c-layout.jpg`、`renders/focus-1-1.jpg`、`renders/focus-2-1.jpg`、`renders/focus-3-1.jpg`、`grid-size-2x2.png`、`grid-size-8x8.png`、`grid-size-32x32.png`。
  - 取樣數比較的三張圖（`#samples`）檔名很長而且含 `%3D`，只附原文連結。
  - 照片列進 Figures not stored here：開頭圖的子流形照片（`manifold-1～4.jpg`）、單張影像段的輸入照片 `dogcat.jpg`、消防船和路面電車的 ImageNet 範例照片、三組補丁示範照片；混了照片的 7 張 JS 圖只附原文連結。
  - 沒有截圖：其餘互動圖（圖譜瀏覽、各層比較、類別比較）只附原文連結。
- 寫法：開頭比較圖的說明文字，以及 mixed5b 消防船那一群的描述，只出現在 JS 產生的文字裡，只改寫並標出處，不附原文句。dump 裡有 4 行把註腳黏進正文（第 35、66、139、148 行），引用時避開。
- 檢查：第 1 輪通過。寫完頁面先用 `check_quotes.py` 自查，把方法頁 3 行單獨的粗體標題改成 `###` 小標（單獨的粗體行會被當成沒有出處的段落）。之後修了 1 處措辭（逐層抽象頁開頭「各篇看到的東西」改成「表示的東西」），再跑一次也通過。
- 逐句對原文核對（另一個 commit）：多義神經元原文是 a mixture of salient ideas，6 處「不相干的概念」改成「顯著概念」，包含 BB 時期寫的頁和名詞表；FV 的 strange mixtures of ideas 改寫成「好幾種概念奇怪地混在一起」；逐層抽象頁 3 處補回原文的 seem（「似乎」）；方法頁比較表 2 格、激活空間頁開頭圖說（not realistic）、多用途特徵頁歸因那條，改成照原文的說法。再跑一次也通過。
