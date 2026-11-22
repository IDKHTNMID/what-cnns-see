# Sources

Manifest of the raw sources. Source files in `raw/` are never edited after they are added; this manifest is appended to on every ingest.

| Slug | Title | Authors | Year | URL | Licence | Downloaded |
|---|---|---|---|---|---|---|
| feature-visualization | Feature Visualization | Chris Olah, Alexander Mordvintsev, Ludwig Schubert | 2017 | https://distill.pub/2017/feature-visualization/ | CC BY 4.0 | 2026-11-22 |
| building-blocks | The Building Blocks of Interpretability | Chris Olah, Arvind Satyanarayan, Ian Johnson, Shan Carter, Ludwig Schubert, Katherine Ye, Alexander Mordvintsev | 2018 | https://distill.pub/2018/building-blocks/ | CC BY 4.0 | 2026-11-22 |
| activation-atlas | Exploring Neural Networks with Activation Atlases | Shan Carter, Zan Armstrong, Ludwig Schubert, Ian Johnson, Chris Olah | 2019 | https://distill.pub/2019/activation-atlas/ | CC BY 4.0 | 2026-11-22 |
| computing-receptive-fields | Computing Receptive Fields of Convolutional Neural Networks | André Araujo, Wade Norris, Jack Sim | 2019 | https://distill.pub/2019/computing-receptive-fields/ | CC BY 4.0 | 2026-11-22 |
| deconv-checkerboard | Deconvolution and Checkerboard Artifacts | Augustus Odena, Vincent Dumoulin, Chris Olah | 2016 | https://distill.pub/2016/deconv-checkerboard/ | CC BY 2.0 | 2026-11-22 |
| d2l-ch7 | Dive into Deep Learning, Chapter 7 (Sections 7.1–7.5) | Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola | 2023 | https://d2l.ai/chapter_convolutional-neural-networks/ | CC BY-SA 4.0 | 2026-11-22 |

The Distill articles state that diagrams and text are under the licence above "unless noted otherwise"; source code on their GitHub pages is under Apache 2.0. The d2l licence is the LICENSE file of https://github.com/d2l-ai/d2l-en (text CC BY-SA 4.0); d2l pages are stored under `d2l-ch7/` with the site's own folder layout.

## Figures not stored here

These figures are other authors' work or contain dataset photos. They are not downloaded or screenshotted; pages link to the original section instead.

| Source | Files | Original work |
|---|---|---|
| deconv-checkerboard | `assets/im_sample_dcgan.png`, `assets/im_sample_dcgan_contrast.png`, `assets/im_sample_salimans.png`, `assets/im_sample_donahue.png`, `assets/im_sample_dumoulin.png` | Samples from Radford et al. 2015, Salimans et al. 2016, Donahue et al. 2016, Dumoulin et al. 2016 |
| deconv-checkerboard | `assets/style_artifacts.png`, `assets/style_clean.png` | Style transfer results made from a photo |
| feature-visualization | `images/prior_vis_icons/*.png` (10 files) | Icons of prior work: Erhan 2009, Szegedy 2013, Mahendran 2015, Nguyen 2015, Mordvintsev 2015, Øygard 2015, Tyka 2016, Mordvintsev 2016, Nguyen 2016a, Nguyen 2016b |
| feature-visualization | `images/diversity/*_examples.jpg` (4 files) | Dataset example photos in the Diversity figures |
| feature-visualization | `images/attribution-1.png`, `images/attribution-2.jpg` | Dataset photo and its attribution map in the opening figure |
| feature-visualization | JS figures `#example-optimization-comparison`, `#random-optimization-and-examples`, `#steepest-descent` | Figures that mix dataset photos with the authors' results |
| d2l-ch7 | `_images/waldo-football.jpg`, `_images/waldo-mask.jpg` | Photos courtesy of William Murphy (Infomatique) |
| d2l-ch7 | `_images/field-visual.png` | Figure taken from Field (1987) |
| d2l-ch7 | `_static/logo-with-text.png` | Site logo, not a figure |

## Screenshots

Figures drawn by JavaScript are captured with `scripts/screenshot_figures.py` and stored under `screenshots/<slug>/`. Each capture shows the figure's default state.

| Source | File | Figure | Captured |
|---|---|---|---|
| computing-receptive-fields | `screenshots/computing-receptive-fields/fig00.png` | Problem setup: the four layer parameters (k=2, p=1, q=1, s=3) | 2026-11-22 |
| computing-receptive-fields | `screenshots/computing-receptive-fields/fig03.png` | Computing receptive field size: k=1, s=3 | 2026-11-22 |
| computing-receptive-fields | `screenshots/computing-receptive-fields/fig04.png` | Computing receptive field size: k=5, s=3 | 2026-11-22 |
| computing-receptive-fields | `screenshots/computing-receptive-fields/fig05.png` | Computing receptive field region: two-layer network, u0=-1, v0=4 | 2026-11-22 |
| computing-receptive-fields | `screenshots/computing-receptive-fields/fig06.png` | Arbitrary computation graphs: misaligned two-path network | 2026-11-22 |
| computing-receptive-fields | `screenshots/computing-receptive-fields/fig07.png` | Arbitrary computation graphs: aligned two-path network | 2026-11-22 |
| feature-visualization | `screenshots/feature-visualization/fig00.png` | Hero: features from edges (conv2d0) to objects (mixed4d & mixed4e) in GoogLeNet | 2026-11-22 |
| feature-visualization | `screenshots/feature-visualization/fig03.png` | Optimization from random noise to activate layer mixed4a, unit 11: steps 0, 4, 48, 2048 | 2026-11-22 |
| feature-visualization | `screenshots/feature-visualization/fig04.png` | Optimization objectives: neuron, channel, layer/DeepDream, class logits, class probability | 2026-11-22 |
| feature-visualization | `screenshots/feature-visualization/fig20.png` | Unregularized optimization at learning rate 0.05: steps 1 to 2048 (inner part of figure 19) | 2026-11-22 |
| feature-visualization | `screenshots/feature-visualization/fig24.png` | Frequency penalization: L1 -0.05, total variation -0.25, blur -1 | 2026-11-22 |
| feature-visualization | `screenshots/feature-visualization/fig26.png` | Transformation robustness: jitter 1px, rotate 5°, scale 1.1× | 2026-11-22 |
| feature-visualization | `screenshots/feature-visualization/fig30.png` | Decorrelated space plus transformation robustness, learning rate 0.05 | 2026-11-22 |
| deconv-checkerboard | `screenshots/deconv-checkerboard/fig01.png` | One-dimensional deconvolution overlap: stride 2, size 3 | 2026-11-23 |
| deconv-checkerboard | `screenshots/deconv-checkerboard/fig03.png` | Two stacked deconvolutions: stride 2, size 3 each | 2026-11-23 |
