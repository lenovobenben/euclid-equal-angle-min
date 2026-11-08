"""Full-domain coverage, label reversal, shared direction and search controls."""

import sys
import unittest
from math import sqrt
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments'))

from sage.all import QQ
from replay_nine import NineReplay
from replay_original import OriginalReplay
import search_shared_centers as screen


class NineReplayTests(unittest.TestCase):
    def test_original_targets_survive_label_reversal(self):
        for values in ((37,19,43),(41,23,31),(29,31,53),(53,31,29)):
            with self.subTest(values=values):
                replay=NineReplay(*values)
                self.assertEqual(replay.execute(),'verified')
                reference=OriginalReplay(*values)
                for name,expected in zip(('P','P_prime'),reference.expected_targets):
                    local=replay.points[replay.bindings[name]]
                    actual=(QQ(values[1])-local[0],local[1]) if replay.reversed else local
                    self.assertEqual(actual,expected)
                    self.assertTrue(reference.is_target(actual))
                self.assertEqual(len(replay.actions),9)

    def test_old_exclusions_and_equal_neighbor_branch(self):
        for values in ((1,2,7),(7,2,1),(2,5,40),(40,5,2),(1,1,3),(3,1,1)):
            with self.subTest(values=values):
                replay=NineReplay(*values)
                self.assertEqual(replay.execute(),'verified')
                count=8 if replay.c==replay.b else 9
                self.assertEqual(len(replay.actions),count)
                self.assertEqual(len(replay.target_times),2)
                if count==8:
                    self.assertNotIn('GammaR',replay.objects)
                    self.assertEqual(replay.objects['perpC'][1],(1,0,-replay.b))

    def test_shared_direction_exact_and_fractional_input(self):
        replay=NineReplay(QQ(9)/2,3,QQ(5)/2)
        self.assertEqual(replay.execute(),'verified')
        point=lambda name:replay.points[replay.bindings[name]]
        G,T,R=map(point,('G','T','R'))
        a,b,c=replay.a,replay.b,replay.c
        self.assertEqual((T[0]-b,T[1]),(b/a*G[0],b/a*G[1]))
        self.assertEqual((R[0]-b,R[1]),(c/b*G[0],c/b*G[1]))
        self.assertEqual(len(replay.actions),9)

    def test_no_solution_keeps_state_unchanged(self):
        replay=NineReplay(1,1,1)
        self.assertEqual(replay.execute(),'no_solution_input')
        self.assertEqual(len(replay.points),4)
        self.assertEqual(len(replay.actions),0)


class SearchCalibrationTests(unittest.TestCase):
    def test_known_center_carrier_found_in_both_filters(self):
        ratios=[(a/b,c/b) for a,b,c in screen.FIXTURES]
        points={
            'E':tuple((-1.,0.) for a,c in ratios),
            'B':tuple((0.,0.) for a,c in ratios),
            'G':tuple((-1/(2*a),sqrt(4*a*a-1)/(2*a)) for a,c in ratios),
            'K':tuple((-a-0.5,sqrt(4*a*a-1)/2) for a,c in ratios),
        }
        targets={'M':tuple((a/(a-1),0.) for a,c in ratios)}
        vector={tuple(screen.describe(candidate)) for candidate in screen.finisher_candidates(points,targets)}
        saved=screen.np
        try:
            screen.np=None
            scalar={tuple(screen.describe(candidate)) for candidate in screen.finisher_candidates(points,targets)}
        finally:
            screen.np=saved
        self.assertEqual(vector,scalar)
        self.assertIn(('line','G','K'),scalar)
        axis=tuple(('line',(0.,1.,0.)) for _ in ratios)
        duplicate=('line','E','B',axis)
        self.assertTrue(screen.hit_centers(duplicate,targets))
        self.assertFalse(screen.fresh(duplicate,[('l',axis)]))
        self.assertFalse(screen.available(points,targets['M']))


if __name__=='__main__':
    unittest.main()
