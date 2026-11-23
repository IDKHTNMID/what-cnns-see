import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_deck_render as render  # noqa: E402


def box(x, y, w, h, name="div"):
    return {"name": name, "x": x, "y": y, "w": w, "h": h}


class TextCompareTests(unittest.TestCase):
    def test_same_text_in_any_order_passes(self):
        self.assertEqual(render.compare_texts(["甲", "乙", "乙"], ["乙", "甲", "乙"]), [])

    def test_missing_text_is_reported(self):
        problems = render.compare_texts(["甲", "乙"], ["甲"])
        self.assertTrue(any("missing" in p and "乙" in p for p in problems), problems)

    def test_extra_text_is_reported(self):
        problems = render.compare_texts(["甲"], ["甲", "帶走"])
        self.assertTrue(any("unexpected" in p and "帶走" in p for p in problems), problems)

    def test_repeated_text_counts(self):
        problems = render.compare_texts(["甲"], ["甲", "甲"])
        self.assertTrue(any("unexpected" in p for p in problems), problems)


class OverflowTests(unittest.TestCase):
    def test_box_inside_passes(self):
        self.assertEqual(render.overflow_problems([box(10, 10, 100, 100)]), [])

    def test_box_past_the_bottom_fails(self):
        problems = render.overflow_problems([box(10, 700, 100, 30, "p.take")])
        self.assertTrue(any("p.take" in p for p in problems), problems)

    def test_box_past_the_right_edge_fails(self):
        self.assertTrue(render.overflow_problems([box(1200, 10, 100, 10)]))

    def test_rounding_tolerance(self):
        self.assertEqual(render.overflow_problems([box(0, 0, 1280.4, 720.4)]), [])

    def test_empty_box_is_ignored(self):
        self.assertEqual(render.overflow_problems([box(5000, 5000, 0, 0)]), [])


class WorkTermTests(unittest.TestCase):
    def test_finds_work_term(self):
        self.assertEqual(render.scan_work_terms(["這頁的帶走", "卷積"]), [("帶走", "這頁的帶走")])

    def test_clean_text_passes(self):
        self.assertEqual(render.scan_work_terms(["卷積核"]), [])


class ReportTests(unittest.TestCase):
    def test_report_is_appended_with_verdict(self):
        with tempfile.TemporaryDirectory() as tmp:
            render.write_report(tmp, "round 1", ["p01: overflow"], [], 15)
            text = render.write_report(tmp, "round 2", [], [], 15)
            saved = (Path(tmp) / render.REPORT).read_text(encoding="utf-8")
        self.assertIn("round 1 | FAIL (1)", saved)
        self.assertIn("round 2 | PASS", saved)
        self.assertIn("PASS", text)


if __name__ == "__main__":
    unittest.main()
