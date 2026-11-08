"""Certified conditional improvements and unchanged general fallback."""

import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments'))
from sage.all import AA,QQ
from exact_geometry import circle,distance2,intersections
from replay_refined import RefinedReplay
from replay_original import OriginalReplay


class RefinedReplayTests(unittest.TestCase):
    def test_two_circle_families_and_label_reversal(self):
        for values in ((9,3,4),(4,3,9),(15,6,4),(4,6,15),(2,1,1)):
            with self.subTest(values=values):
                replay=RefinedReplay(*values)
                self.assertEqual(replay.execute(),'verified')
                self.assertEqual(len(replay.actions),2)
                self.assertTrue(all(action['kind']=='circle' for action in replay.actions))
                reference=OriginalReplay(*values)
                for name,expected in zip(('P','P_prime'),reference.expected_targets):
                    local=replay.points[replay.bindings[name]]
                    actual=(QQ(values[1])-local[0],local[1]) if replay.reversed else local
                    self.assertEqual(actual,expected)
                self.assertEqual(replay.target_times,{'0':2,'1':2})

    def test_equal_outer_seven(self):
        for a,b in ((2,1),(3,1),(7,6)):
            replay=RefinedReplay(a,b,a)
            self.assertEqual(replay.execute(),'verified')
            self.assertEqual(replay.branch,'equal_outer_7')
            self.assertEqual(len(replay.actions),7)
            self.assertEqual(replay.points[replay.bindings['P']][0],QQ(b)/2)

    def test_equal_neighbor_mirror_seven(self):
        for values in ((3,1,1),(5,2,2),(2,2,5)):
            replay=RefinedReplay(*values)
            self.assertEqual(replay.execute(),'verified')
            self.assertEqual(replay.branch,'equal_neighbor_7')
            self.assertEqual(len(replay.actions),7)
            m=replay.points[replay.bindings['M']][0]
            s=replay.points[replay.bindings['S']][0]
            self.assertEqual(m+s,2*replay.b)
            self.assertEqual(replay.objects['GammaM'][1][2],replay.objects['GammaS'][1][2])

    def test_general_fallback_and_no_solution(self):
        for values in ((37,19,43),(1,2,7),(40,5,2)):
            replay=RefinedReplay(*values)
            self.assertEqual(replay.execute(),'verified')
            self.assertEqual(len(replay.actions),9)
        replay=RefinedReplay(1,1,1)
        self.assertEqual(replay.execute(),'no_solution_input')
        self.assertEqual(len(replay.actions),0)

    def test_algebraic_input_at_overlapping_conditions(self):
        # The general proof includes real parameters, beyond rational fixtures.
        a=(AA(5).sqrt()+1)/2
        A,B,C,D=(-a,AA(0)),(AA(0),AA(0)),(AA(1),AA(0)),(a+1,AA(0))
        roots=intersections(('circle',circle(A,C)),('circle',circle(C,D)))
        self.assertEqual(len(roots),2)
        for point in roots:
            self.assertNotEqual(point[1],0)
            self.assertEqual(distance2(point,A),a*a*distance2(point,C))
            self.assertEqual(a*a*distance2(point,B),distance2(point,D))


if __name__=='__main__':unittest.main()
