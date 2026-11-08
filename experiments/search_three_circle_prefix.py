"""Heuristic 8/9 E screen: 2/3 circles, <=2 objects per center, 2 loci.

No result is a lower bound. Multi-fixture root-count mismatches are skipped.
"""

import argparse
import itertools
import json
from pathlib import Path
from time import monotonic
from search_shared_centers import FIXTURES, available, candidates, describe, extend, fresh, finisher_candidates, obj


def completions(points,objects,target,label,deadline,stats):
    for first in candidates(points):
        if monotonic()>deadline:return
        if not fresh(first,objects):continue
        stats['first_core_objects']+=1
        p1,o1=extend(points,objects,first,label+'1',stats)
        if available(p1,target):
            yield p1,o1,[describe(first)]
            continue
        for second in finisher_candidates(p1,{'goal':target}):
            stats['second_core_candidates']+=1
            if not fresh(second,o1):continue
            p2,o2=extend(p1,o1,second,label+'2',stats)
            if available(p2,target):
                yield p2,o2,[describe(first),describe(second)]


def search(seconds,all_prefixes=False,prefix_size=3):
    start=monotonic();deadline=start+seconds
    ratios=[(a/b,c/b) for a,b,c in FIXTURES]
    initial={'A':tuple((-a,0.) for a,c in ratios),'B':tuple((0.,0.) for a,c in ratios),
             'C':tuple((1.,0.) for a,c in ratios),'D':tuple((1.+c,0.) for a,c in ratios)}
    targets={'M':tuple((a/(a-1),0.) for a,c in ratios),
             'N':tuple((1/(1-c),0.) for a,c in ratios)}
    originals=(('A','B'),('D','C'),('B','C'),('C','B'))
    prefixes=list(itertools.combinations(originals,prefix_size))
    if all_prefixes:
        others=itertools.combinations(itertools.permutations('ABCD',2),prefix_size)
        prefixes += [prefix for prefix in others if prefix not in prefixes]
    stats={'prefixes':0,'first_core_objects':0,'second_core_candidates':0,'center_programs':0,'mismatched_root_counts':0}
    for prefix in prefixes:
        if monotonic()>deadline:break
        stats['prefixes']+=1
        points=dict(initial);objects=[('l',tuple(('line',(0.,1.,0.)) for _ in ratios))]
        for index,(p,q) in enumerate(prefix):
            bundle=tuple(obj('circle',x,y) for x,y in zip(points[p],points[q]))
            points,objects=extend(points,objects,('circle',p,q,bundle),f'c{index}',stats)
        for goal,other in (('M','N'),('N','M')):
            for p1,o1,core in completions(points,objects,targets[goal],'u',deadline,stats):
                stats['center_programs']+=1
                for p2,o2,tail in completions(p1,o1,targets[other],'v',deadline,stats):
                    return {'status':'candidate','prefix':prefix,'center_order':[goal,other],
                            'core':core,'tail':tail,'stats':stats,'elapsed':monotonic()-start}
                if monotonic()>deadline:break
    return {'status':'budget_exhausted' if monotonic()>deadline else 'screen_completed_without_hit',
            'stats':stats,'elapsed':monotonic()-start,'all_initial_circle_prefixes_requested':all_prefixes}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds',type=float,default=45)
    parser.add_argument('--all-prefixes',action='store_true')
    parser.add_argument('--prefix-size',type=int,choices=(2,3),default=3)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=search(args.seconds,args.all_prefixes,args.prefix_size)
    result['fixtures']=FIXTURES
    result['prefix_size']=args.prefix_size
    result['scope']=f'{args.prefix_size} input-centered circles; <=2 objects per center, sequential; floating prefilter only'
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
