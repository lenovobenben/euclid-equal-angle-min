"""Independent geometry controls and baseline applicability regression cases."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from sage.all import AA
from exact_geometry import circle_circle, line_circle, line_line
from replay_original import OriginalReplay, ReplayFailure, replay_fixture


class GeometryControls(unittest.TestCase):
    def test_two_irrational_intersections(self):
        roots = circle_circle((AA(0), AA(0), AA(1)), (AA(1), AA(0), AA(1)))
        height = AA(3).sqrt()/2
        self.assertEqual(roots, ((AA(1)/2, -height), (AA(1)/2, height)))

    def test_tangent_disjoint_and_coincident(self):
        unit = (AA(0), AA(0), AA(1))
        self.assertEqual(circle_circle(unit, (AA(2), AA(0), AA(1))), ((AA(1), AA(0)),))
        self.assertEqual(circle_circle(unit, (AA(3), AA(0), AA(1))), ())
        self.assertEqual(circle_circle(unit, unit), ())
        self.assertEqual(line_line((AA(0), AA(1), AA(0)), (AA(0), AA(1), AA(-1))), ())

    def test_vertical_line_circle(self):
        self.assertEqual(line_circle((AA(1), AA(0), AA(0)), (AA(0), AA(0), AA(4))),
                         ((AA(0), AA(-2)), (AA(0), AA(2))))


class ReplayControls(unittest.TestCase):
    def test_goal_oracle_does_not_inject_points(self):
        replay = OriginalReplay(2, 1, 3)
        self.assertEqual(len(replay.points), 4)
        for target in replay.expected_targets:
            self.assertNotIn(target, replay.point_ids)
        with self.assertRaisesRegex(ReplayFailure, "unknown_draw_kind"):
            replay.draw("bad_kind", "parallel", "A", "B")
        self.assertEqual(len(replay.actions), 0)
        replay.draw("GammaA", "circle", "A", "B")
        self.assertEqual(len(replay.points), 5)
        self.assertEqual(replay.target_times, {})
        with self.assertRaisesRegex(ReplayFailure, "unknown_support_point"):
            replay.draw("bad", "line", "A", "P")
        self.assertEqual(len(replay.actions), 1)

    def test_repeated_draw_costs_and_zero_radius_rejected(self):
        replay = OriginalReplay(2, 1, 3)
        with self.assertRaisesRegex(ReplayFailure, "positive_radius"):
            replay.draw("bad", "circle", "A", "A")
        self.assertEqual(len(replay.actions), 0)
        replay.draw("first", "circle", "A", "B")
        count = len(replay.points)
        replay.draw("again", "circle", "A", "B")
        self.assertEqual(len(replay.actions), 2)
        self.assertEqual(len(replay.points), count)
        self.assertEqual(replay.actions[-1]["duplicate_of"], "first")

    def test_regular_exact_targets_and_ten_draws(self):
        replay = OriginalReplay(2, 1, 3)
        self.assertEqual(replay.execute(), "verified")
        p = replay.points[replay.bindings["P"]]
        self.assertEqual(p, (AA(2)/5, AA(6)/5))
        self.assertEqual(replay.points[replay.bindings["P_prime"]], (p[0], -p[1]))
        self.assertEqual(len(replay.actions), 10)
        self.assertEqual(replay.target_times, {"0": 10, "1": 10})
        # A real early alias: M=F in this fixture. No late point is injected.
        self.assertEqual(replay.bindings["M"], replay.bindings["F"])
        self.assertLess(replay.point_records[replay.bindings["M"]]["created_at"], 7)

    def test_regular_fixtures_across_length_orderings(self):
        for lengths in ((3, 2, 4), (5, 6, 9), (9, 6, 5), (2, 1, 2)):
            with self.subTest(lengths=lengths):
                report = replay_fixture("control", lengths, False)
                self.assertEqual(report["status"], "verified")
                self.assertEqual(report["score"], {"lines": 4, "circles": 6, "total": 10})

    def test_exact_failures_are_unscored_and_classified(self):
        for lengths, marker, draws in (
                ((1, 1, 2), "binding:M", 7), ((2, 1, 1), "binding:N", 8),
                ((1, 2, 7), "binding:G", 4), ((7, 2, 1), "binding:I", 4),
                ((2, 5, 40), "binding:G", 4), ((40, 5, 2), "binding:I", 4)):
            with self.subTest(lengths=lengths):
                report = replay_fixture("exception", lengths, False)
                self.assertEqual(report["status"], "construction_not_applicable")
                self.assertGreater(int(report["delta"]), 0)
                self.assertIsNone(report["score"])
                self.assertIn(marker, report["failure"])
                self.assertEqual(report["diagnostic_executed_draws"]["total"], draws)

    def test_no_solution_is_not_a_construction_failure(self):
        report = replay_fixture("no_solution", (1, 1, 1), False)
        self.assertEqual(report["status"], "no_solution_input")
        self.assertIsNone(report["score"])
        self.assertEqual(report["diagnostic_executed_draws"]["total"], 0)


if __name__ == "__main__":
    unittest.main()
