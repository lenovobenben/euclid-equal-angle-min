"""Regression checks for the E7 support that was clipped in the first preview."""

import unittest

from e9_progress import DETAIL, FINAL, OVERVIEW, clip_line, load_geometry


class ViewportTests(unittest.TestCase):
    def test_all_supports_stay_in_safe_area(self):
        data = load_geometry()
        for event in data["events"]:
            step = event["e_move"]
            center, width = OVERVIEW if step < 6 else (DETAIL if step < 8 else FINAL)
            height = width * 9 / 16
            for name in event["references"]:
                with self.subTest(step=step, point=name):
                    point = data["points"][name]
                    self.assertLess(point["available_after"], step)
                    self.assertLess(abs(point["at"][0] - center[0]), width * 0.46)
                    self.assertLess(abs(point["at"][1] - center[1]), height * 0.40)

    def test_final_view_contains_both_locus_circles(self):
        data = load_geometry()
        center, width = FINAL
        height = width * 9 / 16
        for event in data["events"][-2:]:
            circle = event["geometry"]
            for axis, extent in ((0, width), (1, height)):
                self.assertLess(abs(circle["center"][axis] - center[axis]) + circle["radius"], extent * 0.46)

    def test_clipped_lines_reach_viewport_edges(self):
        bounds = (-4, 4, -2, 2)
        for line in [{"a": 0, "b": 1, "c": 0},
                     {"a": 1, "b": 0, "c": 0},
                     {"a": 1, "b": 1, "c": 2}]:
            for point in clip_line(line, bounds):
                self.assertAlmostEqual(line["a"] * point[0] + line["b"] * point[1] + line["c"], 0)
                self.assertTrue(abs(point[0]) == 4 or abs(point[1]) == 2)


if __name__ == "__main__":
    unittest.main()
