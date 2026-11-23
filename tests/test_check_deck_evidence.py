import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_deck_evidence  # noqa: E402
import deck_draft  # noqa: E402

OUTLINE = """# 大綱

## 第 6 頁：怎麼知道一個神經元在找什麼？

- 段落：一個神經元
- Wiki：`methods/fv.md`
- 圖：`raw/demo/fig.png`
- 地圖位置：中層
"""

WIKI = """# 特徵視覺化

## 步驟

神經網路對輸入大致可微，所以可以算[目標](../concepts/x.md)對輸入影像的導數（[FV](../sources/fv.md) § Optimization）。

圖中依序是第 0、4、48、2048 步的影像（§ Optimization）。

![圖](../../raw/demo/fig.png)
"""

GLOSSARY = """# 名詞表

| 主名詞 | 英文 | 別名 | 一句話解釋 | 出處 | 用語依據 |
|---|---|---|---|---|---|
| 卷積 | convolution | 互相關（cross-correlation） | 說明 | 出處 | 依據 |
| 特徵圖 | feature map | 激活立方體（cube of activations）、激活圖 | 說明 | 出處 | 依據 |
"""

VALID_DRAFT = """# 怎麼知道一個神經元在找什麼？

- 區段：一個神經元
- 地圖：中層

## 重點

- 白話：算目標對輸入影像的導數
  依據：methods/fv.md｜神經網路對輸入大致可微，所以可以算目標對輸入影像的導數

## 圖

- 檔案：raw/demo/fig.png
  裁切：16,17,280,280
  白話：第 2048 步的影像
  依據：methods/fv.md｜圖中依序是第 0、4、48、2048 步的影像
"""


def make_repo(tmp, draft=VALID_DRAFT):
    root = Path(tmp)
    for rel, text in {
        "deck/outline.md": OUTLINE,
        "deck/drafts/p06.md": draft,
        "wiki/methods/fv.md": WIKI,
        "wiki/glossary.md": GLOSSARY,
    }.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    figure = root / "raw/demo/fig.png"
    figure.parent.mkdir(parents=True, exist_ok=True)
    figure.write_bytes(b"png")
    return root


class ParseDraftTests(unittest.TestCase):
    def test_parses_blocks_figure_and_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            draft = deck_draft.parse_draft(make_repo(tmp) / "deck/drafts/p06.md")
        self.assertEqual(draft.number, 6)
        self.assertEqual(draft.section, "一個神經元")
        self.assertEqual(draft.map_nodes, ["中層"])
        figure = draft.block("圖")[0]
        self.assertEqual(figure.file, "raw/demo/fig.png")
        self.assertEqual(figure.crop, (16, 17, 280, 280))
        self.assertEqual(figure.evidence[0].page, "methods/fv.md")

    def test_unknown_block_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, VALID_DRAFT + "\n## 帶走\n\n- 白話：x\n")
            with self.assertRaises(deck_draft.DraftError):
                deck_draft.parse_draft(root / "deck/drafts/p06.md")

    def test_evidence_without_separator_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, VALID_DRAFT.replace("methods/fv.md｜神經", "methods/fv.md 神經"))
            with self.assertRaises(deck_draft.DraftError):
                deck_draft.parse_draft(root / "deck/drafts/p06.md")


class EvidenceCheckTests(unittest.TestCase):
    def problems(self, draft):
        with tempfile.TemporaryDirectory() as tmp:
            return check_deck_evidence.check_deck(make_repo(tmp, draft)).problems

    def assert_problem(self, draft, fragment):
        found = self.problems(draft)
        self.assertTrue(any(fragment in p for p in found), found)

    def test_valid_draft_passes(self):
        self.assertEqual(self.problems(VALID_DRAFT), [])

    def test_item_without_evidence_fails(self):
        draft = VALID_DRAFT.replace("  依據：methods/fv.md｜神經網路對輸入大致可微，所以可以算目標對輸入影像的導數\n", "")
        self.assert_problem(draft, "no evidence")

    def test_sentence_not_in_wiki_fails(self):
        self.assert_problem(VALID_DRAFT.replace("所以可以算目標", "因此一定能算目標"), "not found")

    def test_page_not_in_outline_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, VALID_DRAFT.replace("methods/fv.md｜神經", "methods/other.md｜神經"))
            (root / "wiki/methods/other.md").write_text(WIKI, encoding="utf-8")
            found = check_deck_evidence.check_deck(root).problems
        self.assertTrue(any("not listed" in p for p in found), found)

    def test_number_missing_from_evidence_fails(self):
        self.assert_problem(VALID_DRAFT.replace("第 2048 步的影像", "第 4096 步的影像"), "number 4096")

    def test_alias_instead_of_main_term_fails(self):
        draft = VALID_DRAFT.replace("白話：算目標對輸入影像的導數", "白話：算激活立方體的導數")
        self.assert_problem(draft, "alias")

    def test_title_must_match_outline(self):
        self.assert_problem(VALID_DRAFT.replace("# 怎麼知道", "# 如何知道"), "title")

    def test_map_must_match_outline(self):
        self.assert_problem(VALID_DRAFT.replace("地圖：中層", "地圖：高層"), "map")

    def test_term_item_needs_evidence(self):
        self.assert_problem(VALID_DRAFT + "\n## 名詞\n\n- 白話：導數：函數的變化率。\n", "名詞「導數：函數的變化率。」: no evidence")

    def test_bridge_item_needs_evidence(self):
        self.assert_problem(VALID_DRAFT + "\n## 承上\n\n- 白話：承接上一頁。\n", "承上「承接上一頁。」: no evidence")

    def test_unknown_badge_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, VALID_DRAFT.replace("  白話：第 2048 步的影像\n", "  標籤：隨便寫\n  白話：第 2048 步的影像\n"))
            with self.assertRaises(deck_draft.DraftError):
                deck_draft.parse_draft(root / "deck/drafts/p06.md")

    def test_section_must_match_page(self):
        self.assert_problem(VALID_DRAFT.replace("區段：一個神經元", "區段：一張圖"), "section")

    def test_missing_figure_fails(self):
        self.assert_problem(VALID_DRAFT.replace("raw/demo/fig.png", "raw/demo/none.png"), "figure")

    def test_figure_not_used_by_listed_wiki_page_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp)
            page = root / "wiki/methods/fv.md"
            page.write_text(WIKI.replace("![圖](../../raw/demo/fig.png)\n", ""), encoding="utf-8")
            found = check_deck_evidence.check_deck(root).problems
        self.assertTrue(any("not used" in p for p in found), found)

    def test_work_term_is_listed_for_review_not_failed(self):
        draft = VALID_DRAFT.replace("白話：算目標對輸入影像的導數", "白話：算目標對輸入影像的導數（帶走）")
        with tempfile.TemporaryDirectory() as tmp:
            result = check_deck_evidence.check_deck(make_repo(tmp, draft))
        self.assertTrue(any("帶走" in r for r in result.review), result.review)


class CutHedgeScanTests(unittest.TestCase):
    PARTIAL_EVIDENCE = "依據：methods/fv.md｜所以可以算目標對輸入影像的導數"
    FULL_EVIDENCE = "依據：methods/fv.md｜神經網路對輸入大致可微，所以可以算目標對輸入影像的導數"

    def scan(self, draft):
        with tempfile.TemporaryDirectory() as tmp:
            return check_deck_evidence.check_deck(make_repo(tmp, draft))

    def test_hedge_cut_from_evidence_is_listed_without_failing(self):
        result = self.scan(VALID_DRAFT.replace(self.FULL_EVIDENCE, self.PARTIAL_EVIDENCE))
        self.assertEqual(result.problems, [])
        self.assertEqual(len(result.hedges), 1)
        self.assertIn("大致", result.hedges[0])
        self.assertIn("神經網路對輸入大致可微", result.hedges[0])

    def test_hedge_inside_quoted_evidence_is_not_listed(self):
        self.assertEqual(self.scan(VALID_DRAFT).hedges, [])

    def test_hedge_kept_in_plain_text_is_not_listed(self):
        draft = VALID_DRAFT.replace(self.FULL_EVIDENCE, self.PARTIAL_EVIDENCE).replace(
            "白話：算目標對輸入影像的導數", "白話：大致可微，所以可以算目標對輸入影像的導數"
        )
        self.assertEqual(self.scan(draft).hedges, [])

    def test_report_has_a_hedge_review_section(self):
        draft = VALID_DRAFT.replace(self.FULL_EVIDENCE, self.PARTIAL_EVIDENCE)
        with tempfile.TemporaryDirectory() as tmp:
            root = make_repo(tmp, draft)
            result = check_deck_evidence.check_deck(root)
            text = check_deck_evidence.write_report(root, "test", result)
        self.assertIn("保留語掃描", text)
        self.assertIn("大致", text)


if __name__ == "__main__":
    unittest.main()
