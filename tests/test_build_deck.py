import re
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build_deck  # noqa: E402
import deck_draft  # noqa: E402

TEMPLATE = "<html><body><main id=\"stage\"><!--SLIDES--></main></body></html>\n"

SOURCES = """# Sources

| Slug | Title | Authors | Year | URL | Licence | Downloaded |
|---|---|---|---|---|---|---|
| demo | Demo Paper | Ann Lee, Bob Ray, Cy Fox | 2017 | https://example.org/demo/ | CC BY 4.0 | 2026-11-22 |

## Figures not stored here

| Source | Files | Original work |
|---|---|---|
| demo | `x.png` | Someone else |
"""

WIKI = "# 特徵視覺化（Feature Visualization）\n\n## 步驟\n\n從隨機雜訊開始（§ A）。\n"

DRAFT = """# 怎麼知道一個神經元在找什麼？

- 區段：看神經元
- 地圖：中層

## 重點

- 白話：從雜訊出發 <b>
  依據：methods/fv.md｜從隨機雜訊開始

## 內文

- 白話：第一步
  依據：methods/fv.md｜從隨機雜訊開始

## 圖

- 檔案：raw/demo/fig.png
  裁切：10,20,30,40
  白話：圖說
  依據：methods/fv.md｜從隨機雜訊開始
"""

CELL_DRAFT = DRAFT + """
## 圖內文字

- 白話：1 0 1
  依據：methods/fv.md｜從隨機雜訊開始
"""


def make_repo(tmp, draft=DRAFT, layout=None):
    root = Path(tmp)
    for rel, text in {
        "deck/template.html": TEMPLATE,
        "deck/drafts/p06.md": draft,
        "raw/SOURCES.md": SOURCES,
        "wiki/methods/fv.md": WIKI,
    }.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    figure = root / "raw/demo/fig.png"
    figure.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (100, 80)).save(figure)
    if layout is not None:
        path = root / "deck/layouts/p06.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(layout, encoding="utf-8")
    return root


class FillLayoutTests(unittest.TestCase):
    def render(self, draft, layout):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, draft, layout)
            return build_deck.render_deck(root)[0]

    def test_item_text_is_placed_and_escaped(self):
        slide = self.render(DRAFT, '<div class="x">{{內文.1}}{{圖.1}}</div>')
        self.assertIn('<div class="x">第一步', slide.html)
        self.assertIn("從雜訊出發 &lt;b&gt;", slide.html)

    def test_unknown_placeholder_fails(self):
        with self.assertRaisesRegex(build_deck.BuildError, "unknown"):
            self.render(DRAFT, "{{內文.1}}{{圖.1}}{{內文.2}}")

    def test_unused_item_fails(self):
        with self.assertRaisesRegex(build_deck.BuildError, "used 0"):
            self.render(DRAFT, "{{內文.1}}")

    def test_item_used_twice_fails(self):
        with self.assertRaisesRegex(build_deck.BuildError, "used 2"):
            self.render(DRAFT, "{{內文.1}}{{內文.1}}{{圖.1}}")

    def test_words_in_layout_fail(self):
        with self.assertRaisesRegex(build_deck.BuildError, "words"):
            self.render(DRAFT, "<p>帶走</p>{{內文.1}}{{圖.1}}")

    def test_cells_mode_splits_on_spaces_only(self):
        slide = self.render(CELL_DRAFT, "{{內文.1}}{{圖.1}}{{圖內文字.1|cells}}")
        self.assertEqual(re.findall(r'<span class="cell" data-v="([^"]+)">', slide.html), ["1", "0", "1"])
        self.assertEqual(slide.texts.count("1"), 2)
        self.assertNotIn("1 0 1", slide.texts)


class FigureTests(unittest.TestCase):
    def test_crop_uses_svg_viewbox_and_natural_size(self):
        with tempfile.TemporaryDirectory() as tmp:
            slide = build_deck.render_deck(make_repo(tmp))[0]
        self.assertIn('viewBox="10 20 30 40"', slide.html)
        self.assertIn('width="100" height="80"', slide.html)
        self.assertIn('href="../raw/demo/fig.png"', slide.html)

    def test_crop_is_clipped_when_the_box_has_a_different_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            slide = build_deck.render_deck(make_repo(tmp))[0]
        self.assertIn('<svg class="crop" viewBox="0 0 30 40"', slide.html)
        self.assertIn('<svg width="30" height="40" viewBox="10 20 30 40">', slide.html)

    def test_crop_outside_image_fails(self):
        draft = DRAFT.replace("10,20,30,40", "90,20,30,40")
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(build_deck.BuildError, "crop"):
                build_deck.render_deck(make_repo(tmp, draft))


class SourceLineTests(unittest.TestCase):
    def test_lists_wiki_page_and_figure_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            slide = build_deck.render_deck(make_repo(tmp))[0]
        self.assertEqual(slide.source, "資料來源：Wiki〈特徵視覺化〉｜圖：Lee et al., Demo Paper (2017), CC BY 4.0，經裁切")
        self.assertIn('href="https://example.org/demo/"', slide.html)

    def test_wiki_base_links_the_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            slide = build_deck.render_deck(root, wiki_base="https://example.org/wiki/")[0]
        self.assertIn('href="https://example.org/wiki/methods/fv.md"', slide.html)

    def test_figure_link_is_added(self):
        draft = DRAFT.replace("- 地圖：中層\n", "- 地圖：中層\n- 圖見原文：https://example.org/demo/#fig\n")
        with tempfile.TemporaryDirectory() as tmp:
            slide = build_deck.render_deck(make_repo(tmp, draft))[0]
        self.assertTrue(slide.source.endswith("｜圖見原文"))
        self.assertIn('href="https://example.org/demo/#fig"', slide.html)


TERM = "\n- 白話：導數：函數隨輸入改變的變化率。\n  依據：methods/fv.md｜從隨機雜訊開始\n"
TERM_DRAFT = DRAFT + "\n## 名詞\n" + TERM


class TermStripTests(unittest.TestCase):
    def slide(self, draft):
        with tempfile.TemporaryDirectory() as tmp:
            return build_deck.render_deck(make_repo(tmp, draft))[0]

    def test_terms_are_rendered_above_content(self):
        html = self.slide(TERM_DRAFT).html
        self.assertIn('class="terms"', html)
        self.assertLess(html.index("</header>"), html.index('class="terms"'))
        self.assertLess(html.index('class="terms"'), html.index('class="content'))

    def test_term_and_definition_are_separate_text_nodes(self):
        texts = self.slide(TERM_DRAFT).texts
        self.assertIn(build_deck.TERM_LABEL, texts)
        self.assertIn("導數", texts)
        self.assertIn("函數隨輸入改變的變化率。", texts)

    def test_page_without_terms_has_no_strip(self):
        slide = self.slide(DRAFT)
        self.assertNotIn('class="terms"', slide.html)
        self.assertNotIn(build_deck.TERM_LABEL, slide.texts)

    def test_more_than_three_terms_fail(self):
        with self.assertRaisesRegex(build_deck.BuildError, "at most 3"):
            self.slide(DRAFT + "\n## 名詞\n" + TERM * 4)

    def test_term_without_separator_fails(self):
        with self.assertRaisesRegex(build_deck.BuildError, "term：definition"):
            self.slide(TERM_DRAFT.replace("導數：函數", "導數函數"))


class BridgeAndBadgeTests(unittest.TestCase):
    def slide(self, draft):
        with tempfile.TemporaryDirectory() as tmp:
            return build_deck.render_deck(make_repo(tmp, draft))[0]

    def test_bridge_renders_inside_header(self):
        draft = DRAFT + "\n## 承上\n\n- 白話：上一頁看結構，這頁開始看單一神經元。\n  依據：methods/fv.md｜從隨機雜訊開始\n"
        slide = self.slide(draft)
        self.assertIn('<p class="bridge">上一頁看結構，這頁開始看單一神經元。</p>', slide.html)
        self.assertIn("上一頁看結構，這頁開始看單一神經元。", slide.texts)

    def test_multiple_bridges_fail(self):
        item = "\n- 白話：承上\n  依據：methods/fv.md｜從隨機雜訊開始\n"
        with self.assertRaisesRegex(build_deck.BuildError, "at most one 承上"):
            self.slide(DRAFT + "\n## 承上\n" + item * 2)

    def test_badges_render_on_figure_and_note(self):
        draft = DRAFT.replace("  白話：圖說\n", "  標籤：圖 A\n  白話：圖說\n").replace(
            "- 白話：第一步\n", "- 標籤：對應圖 A\n  白話：第一步\n"
        )
        slide = self.slide(draft)
        self.assertIn('<span class="fig-badge tone-a">圖 A</span>', slide.html)
        self.assertIn('<span class="ref-badge tone-a">對應圖 A</span>', slide.html)
        self.assertIn("圖 A", slide.texts)
        self.assertIn("對應圖 A", slide.texts)

    def test_rail_lists_clickable_sections(self):
        slide = self.slide(DRAFT)
        self.assertIn('<li class="here"><a href="#5">看神經元</a></li>', slide.html)
        self.assertIn('<li><a href="#1">開始之前</a></li>', slide.html)


class MapTests(unittest.TestCase):
    def test_map_has_five_plain_labels(self):
        self.assertEqual(deck_draft.MAP_NODES, ("影像", "低層", "中層", "高層", "類別機率"))

    def test_range_expands(self):
        self.assertEqual(deck_draft.parse_map("低層 → 高層"), ["低層", "中層", "高層"])

    def test_removed_label_is_an_error(self):
        with self.assertRaises(deck_draft.DraftError):
            deck_draft.parse_map("logit")


class BuildTests(unittest.TestCase):
    def test_build_writes_every_draft_word(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            output = build_deck.build(root)
            text = output.read_text(encoding="utf-8")
            draft = deck_draft.parse_draft(root / "deck/drafts/p06.md")
        self.assertNotIn("<!--SLIDES-->", text)
        self.assertIn(draft.title, text)
        self.assertIn('id="p6"', text)
        self.assertIn("06 / 01", text)

    def test_auto_layout_refuses_label_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(build_deck.BuildError, "layout"):
                build_deck.render_deck(make_repo(tmp, CELL_DRAFT))


if __name__ == "__main__":
    unittest.main()
