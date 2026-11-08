"""Refine conditional domains to 2/7 E; retain the certified 9 E fallback."""

import argparse
import json
from pathlib import Path
from sage.all import QQ
from sage.env import SAGE_VERSION
from replay_nine import ADDITIONAL_FIXTURES,NineReplay
from replay_original import FIXTURES,RULE_ID


class RefinedReplay(NineReplay):
    def first_locus(self):
        self.draw('GammaA','circle','A','B')
        self.draw('GammaB','circle','B','C')
        self.bind('E','GammaB','l',other_than='C')
        self.bind('G','GammaA','GammaB',side=1)
        self.bind('H','GammaA','GammaB',side=-1)
        self.draw('HE','line','H','E')
        self.bind('K','HE','GammaA',other_than='H')
        self.draw('KG','line','K','G')
        self.bind('M','KG','l')
        self.draw('GammaM','circle','M','B')

    def execute(self):
        if self.delta<=0:return super().execute()
        a,b,c=self.a,self.b,self.c
        if a*c==b*(a+b):
            self.branch='two_circles_ac_ab_b2'
            self.draw('target1','circle','A','C')
            self.draw('target2','circle','C','D')
            first,second='target1','target2'
            count=2
        elif a*c==b*(b+c):
            self.branch='two_circles_ac_bc_b2'
            self.draw('target1','circle','B','A')
            self.draw('target2','circle','D','B')
            first,second='target1','target2'
            count=2
        elif a==c:
            self.branch='equal_outer_7'
            self.first_locus()
            self.draw('GammaC','circle','C','B')
            self.bind('U','GammaB','GammaC',side=1)
            self.bind('V','GammaB','GammaC',side=-1)
            self.draw('perpBC','line','U','V')
            first,second='GammaM','perpBC'
            count=7
        elif c==b:
            self.branch='equal_neighbor_7'
            self.first_locus()
            self.draw('mirror_center','circle','C','M')
            self.bind('S','mirror_center','l',other_than='M')
            self.draw('GammaS','circle','S','D')
            first,second='GammaM','GammaS'
            count=7
        else:
            return super().execute()
        self.bind('P',first,second,side=1)
        self.bind('P_prime',first,second,side=-1)
        for name,expected in zip(('P','P_prime'),self.expected_targets):
            actual=self.points[self.bindings[name]]
            assert actual==expected and self.is_target(actual)
        assert len(self.actions)==count
        assert len(self.target_times)==2
        return 'verified'

    def report(self,name,status,failure=None,include_trace=True):
        report=super().report(name,status,failure,include_trace)
        report['construction']='conditional-refinements-v1'
        return report


REFINEMENT_FIXTURES=[
    ('direct_primary',(9,3,4)),('direct_primary_reversed',(4,3,9)),
    ('direct_secondary',(15,6,4)),('direct_secondary_reversed',(4,6,15)),
    ('equal_outer_other',(3,1,3)),('equal_outer_close',(7,6,7)),
    ('equal_neighbor_other',(5,2,2)),('equal_neighbor_other_reversed',(2,2,5)),
]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    reports=[]
    for name,values in FIXTURES+ADDITIONAL_FIXTURES+REFINEMENT_FIXTURES:
        replay=RefinedReplay(*values)
        status=replay.execute()
        report=replay.report(name,status)
        reports.append(report)
        print(json.dumps({k:v for k,v in report.items() if k!='trace'},ensure_ascii=False),flush=True)
    result={'construction':'conditional-refinements-v1','rule_id':RULE_ID,
            'sage_version':SAGE_VERSION,'arithmetic':'SageMath AA',
            'coverage':'rob: delta>0','global_upper':9,
            'conditional_uppers':{'equal_outer':7,'equal_neighbor':7,'direct_circle_families':2},
            'two_circle_families_minimal':True,'general_minimality_proved':False,'fixtures':reports}
    if args.output:args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
