"""8 E candidate screen after a verified five-draw first-locus prefix.

Prefix: GammaA, GammaB, HE, KG, GammaM. Enumerate a first auxiliary,
a second auxiliary and a final line/circle through a target. Floating evidence
only; all root-count mismatches are skipped and all hits need exact replay.
"""

import argparse
import json
from pathlib import Path
from time import monotonic
from math import sqrt
from search_shared_centers import FIXTURES, available, candidates, describe, extend, fresh, finisher_candidates, obj


def fixture_ratios(family='generic'):
    ratios=[(a/b,c/b) for a,b,c in FIXTURES]
    if family!='generic':
        outer=[37/19,41/23,53/31,29/17]
        ratios=[(a,a if family=='equal-outer' else 1. if family=='equal-neighbor' else 1+1/a)
                for a in outer]
    return ratios


def initial_state(stats,family='generic'):
    ratios=fixture_ratios(family)
    points={'A':tuple((-a,0.) for a,c in ratios),'B':tuple((0.,0.) for a,c in ratios),
            'C':tuple((1.,0.) for a,c in ratios),'D':tuple((1.+c,0.) for a,c in ratios)}
    objects=[('l',tuple(('line',(0.,1.,0.)) for _ in ratios))]
    def draw(kind,first,second,label):
        nonlocal points,objects
        candidate=(kind,first,second,tuple(obj(kind,p,q) for p,q in zip(points[first],points[second])))
        points,objects=extend(points,objects,candidate,label,stats)
    def bind(name,values):
        for key,bundle in points.items():
            if all(abs(p[0]-q[0])+abs(p[1]-q[1])<1e-7 for p,q in zip(values,bundle)):
                points[name]=bundle
                return
        raise AssertionError('oracle point not present:'+name)
    draw('circle','A','B','GammaA')
    draw('circle','B','C','GammaB')
    bind('E',tuple((-1.,0.) for a,c in ratios))
    bind('G',tuple((-1/(2*a),sqrt(4*a*a-1)/(2*a)) for a,c in ratios))
    bind('H',tuple((-1/(2*a),-sqrt(4*a*a-1)/(2*a)) for a,c in ratios))
    draw('line','H','E','HE')
    bind('K',tuple((-a-.5,sqrt(4*a*a-1)/2) for a,c in ratios))
    draw('line','K','G','KG')
    bind('M',tuple((a/(a-1),0.) for a,c in ratios))
    draw('circle','M','B','GammaM')
    # Remove point aliases to keep the candidate enumeration small.
    unique={}
    for key,bundle in points.items():
        if not available(unique,bundle):unique[key]=bundle
    aliases={name:next(key for key,value in unique.items() if all(abs(p[0]-q[0])+abs(p[1]-q[1])<1e-7 for p,q in zip(bundle,value)))
             for name,bundle in points.items()}
    targets={}
    for sign,label in ((1,'upper'),(-1,'lower')):
        targets[label]=tuple(((a-1)*(1+c)/(2*(a*c-1)),
                             sign*sqrt((a+1)*(1+c)*(3*a*c-a-1-c))/(2*(a*c-1)))
                            for a,c in ratios)
    return unique,objects,targets,aliases


def search(seconds,first_mode,start_index,tail_budget=3,family='generic'):
    start=monotonic();deadline=start+seconds
    stats={'first_objects':0,'second_objects':0,'finishers':0,'mismatched_root_counts':0}
    points,objects,targets,aliases=initial_state(stats,family)
    if first_mode=='right-circle':
        p,q=aliases['C'],aliases['D']
        firsts=[('circle',p,q,tuple(obj('circle',x,y) for x,y in zip(points[p],points[q])))]
    else:firsts=candidates(points)
    for index,first in enumerate(firsts):
        if index<start_index or not fresh(first,objects):continue
        if monotonic()>deadline:
            return {'status':'budget_exhausted','next_first_index':index,'stats':stats,'elapsed':monotonic()-start}
        stats['first_objects']+=1
        p1,o1=extend(points,objects,first,'s1',stats)
        early=[name for name,target in targets.items() if available(p1,target)]
        if early:
            return {'status':'candidate','first_index':index,'program':[describe(first)],
                    'target_sides':early,'stats':stats,'elapsed':monotonic()-start}
        if tail_budget==2:
            for last in finisher_candidates(p1,targets):
                if not fresh(last,o1):continue
                p2,_=extend(p1,o1,last,'s2',stats)
                hits=[name for name,target in targets.items() if available(p2,target)]
                if hits:
                    return {'status':'candidate','first_index':index,'program':[describe(first),describe(last)],
                            'target_sides':hits,'stats':stats,'elapsed':monotonic()-start}
            continue
        for second in candidates(p1):
            if monotonic()>deadline:
                return {'status':'budget_exhausted','repeat_first_index':index,'stats':stats,'elapsed':monotonic()-start}
            if not fresh(second,o1):continue
            stats['second_objects']+=1
            p2,o2=extend(p1,o1,second,'s2',stats)
            for third in finisher_candidates(p2,targets):
                if not fresh(third,o2):continue
                stats['finishers']+=1
                p3,o3=extend(p2,o2,third,'s3',stats)
                hits=[name for name,target in targets.items() if available(p3,target)]
                if hits:
                    return {'status':'candidate','first_index':index,'program':[describe(first),describe(second),describe(third)],
                            'target_sides':hits,'stats':stats,'elapsed':monotonic()-start}
    return {'status':'screen_completed_without_hit','stats':stats,'elapsed':monotonic()-start}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds',type=float,default=40)
    parser.add_argument('--first',choices=('right-circle','all'),default='right-circle')
    parser.add_argument('--start-index',type=int,default=0)
    parser.add_argument('--tail-budget',type=int,choices=(2,3),default=3)
    parser.add_argument('--family',choices=('generic','equal-outer','equal-neighbor','radius-coincidence'),default='generic')
    parser.add_argument('--oriented',action='store_true',help='Use max(a,c) on the left, with four distinct ratio fixtures')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.oriented:
        FIXTURES=tuple(dict.fromkeys((max(a,c),b,min(a,c)) for a,b,c in FIXTURES))+((59,41,37),)
    result=search(args.seconds,args.first,args.start_index,args.tail_budget,args.family)
    result.update({'fixtures':FIXTURES,'first_mode':args.first,'start_index':args.start_index,
                   'family':args.family,'tail_budget':args.tail_budget,
                   'oriented':args.oriented,
                   'normalized_lengths':[[a,1.,c] for a,c in fixture_ratios(args.family)],
                   'scope':'5E first-locus prefix plus bounded tail; floating prefilter; family changes fixture ratios as documented'})
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
