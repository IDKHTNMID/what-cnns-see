import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import screenshot_figures  # noqa: E402

FIGURE = {"x": 100, "y": 500, "w": 700, "h": 280}


def box(x, y, w, h):
    return {"x": x, "y": y, "w": w, "h": h}


class CaptureBoxTest(unittest.TestCase):
    def test_no_overflow_adds_padding(self):
        got = screenshot_figures.capture_box(FIGURE, [box(150, 520, 100, 50)], pad=8, max_overflow=60)
        self.assertEqual(got, box(92, 492, 716, 296))

    def test_label_below_figure_is_included(self):
        label = box(300, 770, 40, 30)  # ends 20 px below the figure
        got = screenshot_figures.capture_box(FIGURE, [label], pad=8, max_overflow=60)
        self.assertEqual(got["y"] + got["h"], 800 + 8)

    def test_far_away_part_is_capped(self):
        tooltip = box(-9000, 500, 10, 10)
        got = screenshot_figures.capture_box(FIGURE, [tooltip], pad=8, max_overflow=60)
        self.assertEqual(got["x"], 100 - 60 - 8)

    def test_box_never_starts_before_page_origin(self):
        figure = box(4, 2, 300, 200)
        got = screenshot_figures.capture_box(figure, [], pad=8, max_overflow=60)
        self.assertEqual((got["x"], got["y"]), (0, 0))
        self.assertEqual((got["w"], got["h"]), (312, 210))

    def test_zero_size_parts_are_ignored(self):
        hidden = box(100, 2000, 0, 0)
        got = screenshot_figures.capture_box(FIGURE, [hidden], pad=8, max_overflow=60)
        self.assertEqual(got, box(92, 492, 716, 296))


if __name__ == "__main__":
    unittest.main()
