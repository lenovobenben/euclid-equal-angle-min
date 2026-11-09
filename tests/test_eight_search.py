"""Controls for virtual supports, simultaneous-center circles and known E5 seeds."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))

import search_shared_centers as geometry
from search_early_locus import calibration as early_calibration
from search_simultaneous_centers import calibration, simultaneous_circles
from search_eight_suffix import initial_state
from audit_early_loci import verify_prefix_identities


class EightSearchControls(unittest.TestCase):
    def test_new_support_witnesses_and_real_intersections(self):
        self.assertTrue(all(calibration().values()))

    def test_scalar_filter_keeps_the_same_controls(self):
        saved = geometry.np
        try:
            geometry.np = None
            self.assertTrue(all(calibration().values()))
        finally:
            geometry.np = saved

    def test_circle_requires_both_centers_and_allows_off_axis_support(self):
        targets = {'M': ((1., 0.),), 'N': ((3., 0.),)}
        points = {'O': ((0., 0.),), 'Q': ((1., 0.),)}
        self.assertEqual(list(simultaneous_circles(points, [], targets)), [])
        points['O'] = ((2., 1.),)
        candidates = list(simultaneous_circles(points, [], targets))
        self.assertEqual([candidate[:3] for candidate in candidates], [('circle', 'O', 'Q')])

    def test_known_five_draw_carrier_is_retained(self):
        self.assertTrue(all(early_calibration().values()))

    def test_symbolic_prefix_identities(self):
        self.assertEqual(verify_prefix_identities()['identities'], 11)

    def test_alternative_prefixes_have_five_paid_draws(self):
        fixtures = ((3, 1, 2), (47, 29, 37), (40, 5, 2))
        for mode in ('circle-secant', 'reflected-circles'):
            with self.subTest(mode=mode):
                stats = {'mismatched_root_counts': 0}
                points, objects, targets, aliases = initial_state(stats, prefix_mode=mode, fixtures=fixtures)
                self.assertEqual(len(objects)-1, 5)
                locus = dict(objects)['GammaM']
                for target in targets.values():
                    self.assertTrue(all(geometry.contains(circle, point) for circle, point in zip(locus, target)))
                    self.assertFalse(geometry.available(points, target))
                self.assertIn(aliases['M'], points)

    def test_reflected_prefix_checks_its_own_domain(self):
        stats = {'mismatched_root_counts': 0}
        with self.assertRaisesRegex(ValueError, 'a>3b/2'):
            initial_state(stats, prefix_mode='reflected-circles', fixtures=((59, 41, 37),))


if __name__ == '__main__':
    unittest.main()
