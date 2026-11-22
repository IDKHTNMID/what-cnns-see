import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_quotes  # noqa: E402

DEMO_HTML = """<html><head><title>t</title><script>var x = "Hidden script text.";</script></head>
<body><h1>Demo Article</h1>
<h2>Optimization Objectives</h2>
<p>Neurons respond to curves<d-cite key="a"></d-cite> in many layers.</p>
<p>The kernel has size \\(k_l\\) at layer \\(l\\).</p>
<h2>7.2.1. The Cross-Correlation Operation</h2>
<p>It is called a &ldquo;transposed convolution.&rdquo; by some.</p>
<!-- <p>Commented out sentence.</p> -->
</body></html>"""

VALID_SOURCE_PAGE = """# 示範來源

- 作者：Demo

## 重點

神經元會對曲線有反應（§ Optimization Objectives）。

> 原文（demo）：Neurons respond to curves in many layers.

- 第一點（§ The Cross-Correlation Operation）
- 第二點（§ 全文）

## 相關頁面

- [概念](../concepts/curve.md)
"""

VALID_CONCEPT_PAGE = """# 曲線

## 是什麼

曲線偵測器（[Demo](../sources/demo.md) § Optimization Objectives；[Demo](../sources/demo.md) § The Cross-Correlation Operation）。

> 原文（demo）：It is called a “transposed convolution.” by some.

| 名詞 | 說明 |
|---|---|
| kernel | 卷積核（[Demo](../sources/demo.md) § Optimization Objectives） |

![曲線](../../raw/demo/curve.png)
圖：曲線（[Demo](../sources/demo.md) § Optimization Objectives）
"""


class MiniRepo:
    def __init__(self, pages):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "raw" / "demo").mkdir(parents=True)
        (self.root / "raw" / "demo" / "index.html").write_text(DEMO_HTML, encoding="utf-8")
        for rel, text in pages.items():
            path = self.root / "wiki" / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(textwrap.dedent(text), encoding="utf-8")

    def problems(self):
        return check_quotes.check_wiki(self.root)

    def close(self):
        self.tmp.cleanup()


class CheckQuotesTest(unittest.TestCase):
    def run_pages(self, **overrides):
        pages = {"sources/demo.md": VALID_SOURCE_PAGE, "concepts/curve.md": VALID_CONCEPT_PAGE}
        pages.update({k.replace("__", "/") + ".md": v for k, v in overrides.items()})
        repo = MiniRepo(pages)
        try:
            return repo.problems()
        finally:
            repo.close()

    def test_valid_pages_pass(self):
        self.assertEqual(self.run_pages(), [])

    def test_unknown_section_fails(self):
        page = VALID_SOURCE_PAGE.replace("§ Optimization Objectives", "§ Made Up Section")
        problems = self.run_pages(sources__demo=page)
        self.assertTrue(any("section 'Made Up Section' not found" in p for p in problems), problems)

    def test_mutated_quote_fails(self):
        page = VALID_SOURCE_PAGE.replace("respond to curves", "respond to lines")
        problems = self.run_pages(sources__demo=page)
        self.assertTrue(any("quote not found" in p for p in problems), problems)

    def test_script_and_comment_text_is_not_quotable(self):
        page = VALID_SOURCE_PAGE.replace("Neurons respond to curves in many layers.", "Hidden script text.")
        self.assertTrue(any("quote not found" in p for p in self.run_pages(sources__demo=page)))
        page = VALID_SOURCE_PAGE.replace("Neurons respond to curves in many layers.", "Commented out sentence.")
        self.assertTrue(any("quote not found" in p for p in self.run_pages(sources__demo=page)))

    def test_malformed_quote_line_fails(self):
        page = VALID_SOURCE_PAGE.replace("> 原文（demo）：", "> 原文 demo: ")
        problems = self.run_pages(sources__demo=page)
        self.assertTrue(any("not in the form" in p for p in problems), problems)

    def test_paragraph_without_citation_fails(self):
        page = VALID_SOURCE_PAGE.replace("神經元會對曲線有反應（§ Optimization Objectives）。", "神經元會對曲線有反應。")
        problems = self.run_pages(sources__demo=page)
        self.assertIn("wiki/sources/demo.md:7: no citation", problems)

    def test_list_item_without_citation_fails(self):
        page = VALID_SOURCE_PAGE.replace("- 第二點（§ 全文）", "- 第二點")
        problems = self.run_pages(sources__demo=page)
        self.assertIn("wiki/sources/demo.md:12: no citation", problems)

    def test_table_row_without_citation_fails(self):
        page = VALID_CONCEPT_PAGE.replace("卷積核（[Demo](../sources/demo.md) § Optimization Objectives）", "卷積核")
        problems = self.run_pages(concepts__curve=page)
        self.assertTrue(any(p.endswith("no citation") and "curve.md:11" in p for p in problems), problems)

    def test_figure_without_citation_fails(self):
        page = VALID_CONCEPT_PAGE.replace("圖：曲線（[Demo](../sources/demo.md) § Optimization Objectives）", "圖：曲線")
        problems = self.run_pages(concepts__curve=page)
        self.assertTrue(any("curve.md:13: no citation" in p for p in problems), problems)

    def test_bare_section_outside_source_page_fails(self):
        page = VALID_CONCEPT_PAGE.replace("曲線偵測器（[Demo](../sources/demo.md) § Optimization Objectives；",
                                          "曲線偵測器（§ Optimization Objectives；")
        problems = self.run_pages(concepts__curve=page)
        self.assertTrue(any("has no source link" in p for p in problems), problems)

    def test_unknown_source_fails(self):
        page = VALID_CONCEPT_PAGE.replace("../sources/demo.md) § The Cross", "../sources/nope.md) § The Cross")
        problems = self.run_pages(concepts__curve=page)
        self.assertTrue(any("source 'nope' not found" in p for p in problems), problems)

    def test_exempt_section_needs_no_citation(self):
        page = VALID_SOURCE_PAGE + "\n沒有出處的說明文字。\n"
        self.assertEqual(self.run_pages(sources__demo=page), [])

    def test_glossary_rows_need_citation(self):
        glossary = "# 名詞表\n\n| 主名詞 | 出處 |\n|---|---|\n| 曲線 | （[Demo](sources/demo.md) § 全文） |\n| 直線 | 無 |\n"
        problems = self.run_pages(glossary=glossary)
        self.assertEqual([p for p in problems if "glossary" in p], ["wiki/glossary.md:6: no citation"])


class RealSourcesTest(unittest.TestCase):
    """The checker must accept real sentences from raw/ and reject altered ones."""

    REAL = [
        ("deconv-checkerboard",
         "(Deconvolution has a number of interpretations and different names, including “transposed convolution.”"),
        ("feature-visualization",
         "Another is to use ideas from style transfer to force the feature to be displayed in different styles."),
        ("computing-receptive-fields", r"We denote the input image by \(f_0\)."),
    ]

    @classmethod
    def setUpClass(cls):
        cls.sources = {slug: check_quotes.Source(slug, check_quotes.ROOT / "raw") for slug, _ in cls.REAL}

    def test_real_sentences_found(self):
        for slug, sentence in self.REAL:
            with self.subTest(slug=slug):
                self.assertTrue(self.sources[slug].has_quote(sentence))

    def test_altered_sentences_rejected(self):
        for slug, sentence in self.REAL:
            with self.subTest(slug=slug):
                altered = sentence.replace(" ", " not ", 1)
                self.assertNotEqual(altered, sentence)
                self.assertFalse(self.sources[slug].has_quote(altered))

    def test_real_section_titles(self):
        src = self.sources["computing-receptive-fields"]
        self.assertTrue(src.has_section("Solving recurrence equations: receptive field size"))
        self.assertFalse(src.has_section("Receptive field arithmetic"))

    def test_d2l_titles_ignore_numbers_and_notebook_buttons(self):
        src = check_quotes.Source("d2l-ch7", check_quotes.ROOT / "raw")
        self.assertTrue(src.has_section("Convolutions for Images"))
        self.assertTrue(src.has_section("7.2. Convolutions for Images"))
        self.assertTrue(src.has_section("Feature Map and Receptive Field"))
        self.assertFalse(src.has_section("Convolutions for Images colab"))

    def test_d2l_title_with_inline_math(self):
        src = check_quotes.Source("d2l-ch7", check_quotes.ROOT / "raw")
        self.assertTrue(src.has_section("1×1 Convolutional Layer"))
        self.assertTrue(src.has_section("7.4.3. 1×1 Convolutional Layer"))
        self.assertFalse(src.has_section("2×2 Convolutional Layer"))


if __name__ == "__main__":
    unittest.main()
