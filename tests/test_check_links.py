import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import check_links  # noqa: E402

BASE_PAGES = {
    "wiki/index.md": "- [來源](sources/demo.md)\n- [概念](concepts/curve.md)\n",
    "wiki/log.md": "## [2026-11-22] ingest | Demo\n- [來源](sources/demo.md)\n",
    "wiki/sources/demo.md": "見 [曲線](../concepts/curve.md)。\n![圖](../../raw/demo/fig.png)\n",
    "wiki/concepts/curve.md": "出處 [Demo](../sources/demo.md)；外部 [原文](https://distill.pub/x/#y)\n",
}


def run(pages):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "raw" / "demo").mkdir(parents=True)
        (root / "raw" / "demo" / "fig.png").write_bytes(b"png")
        for rel, text in pages.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        return check_links.check_wiki(root)


class CheckLinksTest(unittest.TestCase):
    def test_valid_wiki_passes(self):
        self.assertEqual(run(BASE_PAGES), [])

    def test_broken_link_fails(self):
        pages = dict(BASE_PAGES, **{"wiki/concepts/curve.md": "出處 [Demo](../sources/missing.md)\n"})
        problems = run(pages)
        self.assertIn("wiki/concepts/curve.md:1: broken link '../sources/missing.md'", problems)

    def test_broken_image_fails(self):
        pages = dict(BASE_PAGES, **{"wiki/sources/demo.md": "見 [曲線](../concepts/curve.md)。\n![圖](../../raw/demo/nope.png)\n"})
        self.assertIn("wiki/sources/demo.md:2: broken link '../../raw/demo/nope.png'", run(pages))

    def test_orphan_fails(self):
        pages = dict(BASE_PAGES, **{"wiki/sources/demo.md": "沒有連到別頁。\n"})
        problems = run(pages)
        self.assertIn("wiki/concepts/curve.md: orphan (no inbound link from another content page)", problems)

    def test_link_from_index_or_log_does_not_count_as_inbound(self):
        pages = dict(BASE_PAGES, **{"wiki/concepts/curve.md": "沒有連出去。\n"})
        problems = run(pages)
        self.assertIn("wiki/sources/demo.md: orphan (no inbound link from another content page)", problems)

    def test_page_missing_from_index_fails(self):
        pages = dict(BASE_PAGES, **{"wiki/index.md": "- [來源](sources/demo.md)\n"})
        self.assertIn("wiki/concepts/curve.md: not listed in wiki/index.md", run(pages))


if __name__ == "__main__":
    unittest.main()
