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


class FitsViewportTest(unittest.TestCase):
    def test_box_inside_view_fits(self):
        self.assertTrue(screenshot_figures.fits_viewport(box(92, 492, 716, 296), scroll_y=300, height=1000))

    def test_box_starting_above_view_does_not_fit(self):
        self.assertFalse(screenshot_figures.fits_viewport(box(92, 492, 716, 296), scroll_y=500, height=1000))

    def test_box_ending_below_view_does_not_fit(self):
        self.assertFalse(screenshot_figures.fits_viewport(box(92, 492, 716, 296), scroll_y=0, height=700))

    def test_box_touching_both_edges_fits(self):
        self.assertTrue(screenshot_figures.fits_viewport(box(0, 100, 50, 1000), scroll_y=100, height=1000))


class CaptureWhenStillTest(unittest.TestCase):
    def run_capture(self, positions, tries=3, ready=lambda layout: True):
        reads = iter(positions)
        captured = []

        def capture(layout):
            captured.append(layout)
            return f"shot at {layout}"

        result = screenshot_figures.capture_when_still(lambda: next(reads), capture, ready=ready,
                                                       tries=tries, wait=lambda: None)
        return result, captured

    def test_figure_still_loading_is_not_captured_yet(self):
        loaded = lambda layout: layout.endswith("loaded")  # noqa: E731
        result, captured = self.run_capture(["100 loading", "100 loaded", "100 loaded"], ready=loaded)
        self.assertEqual(result, "shot at 100 loaded")
        self.assertEqual(captured, ["100 loaded"])

    def test_figure_that_never_loads_gives_none(self):
        result, captured = self.run_capture(["loading"] * 3, ready=lambda layout: False)
        self.assertIsNone(result)
        self.assertEqual(captured, [])

    def test_still_layout_is_captured_once(self):
        result, captured = self.run_capture([100, 100])
        self.assertEqual(result, "shot at 100")
        self.assertEqual(captured, [100])

    def test_layout_that_moves_during_capture_is_retried(self):
        result, captured = self.run_capture([100, 685, 685, 685])
        self.assertEqual(result, "shot at 685")
        self.assertEqual(captured, [100, 685])

    def test_layout_that_never_settles_gives_none(self):
        result, captured = self.run_capture([1, 2, 3, 4, 5, 6], tries=3)
        self.assertIsNone(result)
        self.assertEqual(len(captured), 3)


if __name__ == "__main__":
    unittest.main()
