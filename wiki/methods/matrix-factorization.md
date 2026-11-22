# 矩陣分解

## 輸入

- 一張影像在某一層的特徵圖（feature map）（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
- 要分成幾個群組，以及分解要完整描述什麼：激活值（activation）、梯度或歸因（attribution）（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

## 步驟

1. 把特徵圖攤平成「空間位置 × 通道」的矩陣（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
2. 對這個矩陣做矩陣分解（matrix factorization）；Building Blocks 用非負矩陣分解（non-negative matrix factorization，NMF），限制因子都是正的（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
3. 分出來的每一組是一個神經元群組（neuron groups），是元素（原文叫 spatial location）和通道的組合；這些群組就是使用者在介面上操作的單位（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
4. 每個群組用特徵視覺化（feature visualization）畫出它在找什麼，並列出它對各輸出類別的影響（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：By flattening our cube into a matrix of spatial locations and channels, we can apply these techniques to get more meaningful groups of neurons.

> 原文（building-blocks）：The groups that come out of this factorization will be the atoms of the interface a user works with.

圖見原文：[The Building Blocks of Interpretability：Making Things Human-Scale（mixed4d 的神經元群組）](https://distill.pub/2018/building-blocks/#ActivationGroups)（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）

### 跨層相容

1. 想一起看好幾層時，希望每層的分解「相容」：前面層的群組自然地組成後面層的群組（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
2. 對這一層的每個神經元（neuron），算它對要相容的 N 個群組的歸因（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
3. 把激活矩陣的每一格在通道維度上拆成 N 格，依它對各群組歸因的絕對值按比例分配（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
4. 分解拆開後的矩陣，再把行因子裡重複的格子合併回去，就得到原矩陣的分解（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：The basic idea is to split each entry in the activation matrix into N entries on the channel dimension, spreading the values proportional to the absolute value of its attribution to the corresponding group.

圖見原文：[The Building Blocks of Interpretability：Making Things Human-Scale（兩層神經元群組之間的歸因）](https://distill.pub/2018/building-blocks/#AttributionGroups)（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）

## 輸出

少數幾個神經元群組，把數量龐大的神經元濃縮成網路在這張影像上的簡短故事（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：Notice how the overwhelmingly large number of neurons has been reduced to a small set of groups, concisely summarizing the story of the neural network.

## 公式與參數

特徵圖的高、寬、通道數是 $h$、$w$、$c$，群組數是 $k$；攤平後的矩陣 $A$ 有 $h \cdot w$ 列（空間位置）、$c$ 行（通道）（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。多數矩陣分解的演算法和函式庫，是讓重建矩陣的均方誤差最小（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）：

```math
\min_{W \ge 0,\; H \ge 0} \; \lVert A - W H \rVert^2, \quad W \in \mathbb{R}^{hw \times k},\; H \in \mathbb{R}^{k \times c}
```

> 原文（building-blocks）：Most matrix factorization algorithms and libraries are set up to minimize the mean squared error of the reconstruction of a matrix you give them.

- $W \ge 0$、$H \ge 0$ 是 NMF 的限制；ReLU 網路的激活值本來就是正的，所以這個限制沒有問題（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
- 群組數 $k$：互動圖可以調整，mixed4d 預設 6 組（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
- 要描述其他目標時，可以巧妙地改造餵給函式庫的矩陣；更一般地說，矩陣分解是最佳化問題，用自訂工具可以做各種自訂的分解（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：This is fine for the activations of a ReLU network, which must be positive as well.

## 為什麼這樣設計

**為什麼要分組。** 很多通道或空間位置會高度相關地一起運作，當成一個單位最好理解；有些幾乎沒有活動，做高層概覽時可以忽略（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：Often, many channels or spatial positions will work together in a highly correlated way and are most useful to think of as one unit.

**為什麼用矩陣分解。** 任何分組都要在「壓到人看得完」和「保留資訊」之間取捨；矩陣分解可以指定分組要為什麼最佳化，取捨得比特徵圖的自然切法好（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：Unfortunately, any grouping is inherently a tradeoff between reducing things to human scale and, because any aggregation is lossy, preserving information.

**分解要描述什麼，由介面的目標決定**（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）：

- 重視網路偵測到什麼：分解要完整描述激活值（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
- 重視什麼會改變網路的行為：分解要完整描述梯度（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
- 重視什麼造成目前的行為：分解要完整描述歸因（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。
- 也可以在三者之間折衷（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：The goals of our user interface should influence what we optimize our matrix factorization to prioritize.

**為什麼用 NMF。** 作者的經驗是 NMF 得到的群組比沒有非負限制時更獨立、更有語意；代價是表示激活值的效率比較差（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：Our experience is that the groups we get from NMF seem more independent and semantically meaningful than those without this constraint.

**為什麼每張影像都要重算。** 群組是為了解釋網路在某一張影像上的行為建的，拿到另一張影像上重用效果不好（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：It would not be effective to reuse the same groupings on another image; each image requires calculating a unique set of groups.

**跨層相容的限制。** 拆開後的矩陣遇到同一個通道在不同位置有不同的歸因時，會傾向分成不同的因子；作者也沒有把握這個形式化是最好的，不意外它被後續研究取代（[The Building Blocks of Interpretability](../sources/building-blocks.md) § Making Things Human-Scale）。

> 原文（building-blocks）：We formalize this "compatibility" in a manner described below, although we're not confident it's the best formalization and won't be surprised if it is superseded in future work.

**和激活圖譜的關係。** Activation Atlas 說激活圖譜完全失去激活值的組合結構；要部分呈現組合結構，可以像 Feature Visualization 的神經元相加圖那樣做；作者也隱約覺得巧妙地用矩陣分解或許能做到，但還不知道怎麼做，見[激活圖譜](activation-atlas.md)（[Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md) § Doesn't Surface Compositionality）。

> 原文（activation-atlas）：We vaguely suspect that there may be a way to thread the needle with clever use of matrix factorization, but we do not yet know how.

## 相關頁面

- [The Building Blocks of Interpretability](../sources/building-blocks.md)
- [特徵圖](../concepts/feature-map.md)
- [語意字典](../concepts/semantic-dictionary.md)
- [歸因](attribution.md)
- [特徵視覺化](feature-visualization.md)
- [激活空間](../concepts/activation-space.md)
- [激活圖譜](activation-atlas.md)
- [Exploring Neural Networks with Activation Atlases](../sources/activation-atlas.md)
