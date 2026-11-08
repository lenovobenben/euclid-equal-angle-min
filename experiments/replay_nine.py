"""9 E full-domain construction with a separate 8 E equal-neighbor branch.

Reuses the exact AA state, automatic intersections, ledger and goal observer of
the original replay. Orientation is relabeling only; it creates no free point.
"""

import argparse
import json
from pathlib import Path
from sage.all import QQ
from sage.env import SAGE_VERSION
from replay_original import FIXTURES, OriginalReplay, RULE_ID


class NineReplay(OriginalReplay):
    def __init__(self, a, b, c):
        self.input_lengths = tuple(map(QQ, (a,b,c)))
        self.reversed = c > a
        super().__init__(c if self.reversed else a, b, a if self.reversed else c)
        self.branch = None

    def execute(self):
        if self.delta <= 0:
            self.branch = 'no_solution'
            return 'no_solution_input'
        a,b,c = self.a,self.b,self.c
        # Existence implies b<sqrt(ac)<=max(a,c)=a, with strict b<a.
        assert a >= c and a > b
        self.branch = 'equal_neighbor_8' if c == b else 'shared_circle_9'
        self.draw('GammaA','circle','A','B')
        self.draw('GammaB','circle','B','C')
        if c != b:
            self.draw('GammaR','circle','C','D')
        self.bind('E','GammaB','l',other_than='C')
        self.bind('G','GammaA','GammaB',side=1)
        self.bind('H','GammaA','GammaB',side=-1)
        self.draw('HE','line','H','E')
        self.bind('K','HE','GammaA',other_than='H')
        self.draw('KG','line','K','G')
        self.bind('M','KG','l')
        if c == b:
            self.draw('GammaM','circle','M','B')
            self.draw('perpB','circle','B','D')
            self.draw('perpD','circle','D','B')
            self.bind('U','perpB','perpD',side=1)
            self.bind('V','perpB','perpD',side=-1)
            self.draw('perpC','line','U','V')
            self.bind('P','perpC','GammaM',side=1)
            self.bind('P_prime','perpC','GammaM',side=-1)
        else:
            self.bind('T','KG','GammaB',other_than='G')
            self.draw('CT','line','C','T')
            self.bind('R','CT','GammaR',side=1)
            self.draw('GR','line','G','R')
            self.bind('N','GR','l')
            self.draw('GammaM','circle','M','B')
            self.draw('GammaN','circle','N','C')
            self.bind('P','GammaM','GammaN',side=1)
            self.bind('P_prime','GammaM','GammaN',side=-1)
        for name,expected in zip(('P','P_prime'),self.expected_targets):
            actual = self.points[self.bindings[name]]
            assert actual == expected and self.is_target(actual)
        assert len(self.actions) == (8 if c == b else 9)
        assert len(self.target_times) == 2
        return 'verified'

    def report(self, name, status, failure=None, include_trace=True):
        report = super().report(name,status,failure,include_trace)
        report.update({
            'construction':'shared-circle-nine-v1',
            'lengths':[str(v) for v in self.input_lengths],
            'local_lengths':[str(v) for v in (self.a,self.b,self.c)],
            'reversed_input_labels':bool(self.reversed),
            'local_to_original':'(x,y) -> (b-x,y)' if self.reversed else 'identity',
            'branch':self.branch,
            'in_covered_domain':bool(self.delta>0),
        })
        return report


ADDITIONAL_FIXTURES = [
    ('screen_1',(37,19,43)),('screen_2',(41,23,31)),
    ('screen_3',(29,31,53)),('screen_4',(53,31,29)),
    ('near_equal_outer',(101,100,102)),
    ('extreme_ratio',(1,2,100)),
    ('equal_neighbor_general',(3,1,1)),
    ('equal_neighbor_general_reversed',(1,1,3)),
    ('fractional_input',(QQ(9)/2,3,QQ(5)/2)),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    reports=[]
    for name,values in FIXTURES+ADDITIONAL_FIXTURES:
        replay=NineReplay(*values)
        status=replay.execute()
        report=replay.report(name,status)
        reports.append(report)
        print(json.dumps({k:v for k,v in report.items() if k!='trace'},ensure_ascii=False),flush=True)
    result={'construction':'shared-circle-nine-v1','rule_id':RULE_ID,
            'sage_version':SAGE_VERSION,'arithmetic':'SageMath AA',
            'coverage':'rob: a,b,c>0, 3ac>b(a+b+c)',
            'upper_bounds':{'EA-ONE':{'gen':9,'rob':9},'EA-ALL':{'gen':9,'rob':9}},
            'equal_neighbor_branch_upper':8,'minimality_proved':False,'fixtures':reports}
    if args.output:
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
