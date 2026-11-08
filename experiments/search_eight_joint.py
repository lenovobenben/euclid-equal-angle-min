"""Bounded 8 E screen: 3 initial circles, 3 joint-center draws, 2 loci.

The first added object is arbitrary; the second must produce a first center
unless one is already available, and the last must produce the missing center.
This does not cover a final object producing both centers after two no-center
steps. Floating multi-fixture bindings skip root-count mismatches.
"""

import argparse
import itertools
import json
from pathlib import Path
from time import monotonic
from search_shared_centers import FIXTURES,available,candidates,describe,extend,fresh,finisher_candidates,obj


def search(seconds,start_prefix):
    start=monotonic();deadline=start+seconds
    ratios=[(a/b,c/b) for a,b,c in FIXTURES]
    initial={'A':tuple((-a,0.) for a,c in ratios),'B':tuple((0.,0.) for a,c in ratios),
             'C':tuple((1.,0.) for a,c in ratios),'D':tuple((1.+c,0.) for a,c in ratios)}
    targets={'M':tuple((a/(a-1),0.) for a,c in ratios),'N':tuple((1/(1-c),0.) for a,c in ratios)}
    preferred=(('A','B'),('B','C'),('C','D'))
    prefixes=[preferred]+[prefix for prefix in itertools.combinations(itertools.permutations('ABCD',2),3) if prefix!=preferred]
    stats={'prefixes':0,'first_objects':0,'second_finishers':0,'third_finishers':0,'mismatched_root_counts':0}
    def finish(status,index,program=None):
        result={'status':status,'repeat_prefix_index':index,'stats':stats,'elapsed':monotonic()-start}
        if program is not None:result['program']=program
        return result
    for prefix_index,prefix in enumerate(prefixes):
        if prefix_index<start_prefix:continue
        if monotonic()>deadline:return finish('budget_exhausted',prefix_index)
        stats['prefixes']+=1
        points=dict(initial);objects=[('l',tuple(('line',(0.,1.,0.)) for _ in ratios))]
        for i,(p,q) in enumerate(prefix):
            bundle=tuple(obj('circle',x,y) for x,y in zip(points[p],points[q]))
            points,objects=extend(points,objects,('circle',p,q,bundle),f'c{i}',stats)
        for first in candidates(points):
            if monotonic()>deadline:return finish('budget_exhausted',prefix_index)
            if not fresh(first,objects):continue
            stats['first_objects']+=1
            p1,o1=extend(points,objects,first,'s1',stats)
            present={name for name,target in targets.items() if available(p1,target)}
            seconds=candidates(p1) if present else finisher_candidates(p1,targets)
            for second in seconds:
                if monotonic()>deadline:return finish('budget_exhausted',prefix_index)
                if not fresh(second,o1):continue
                stats['second_finishers']+=1
                p2,o2=extend(p1,o1,second,'s2',stats)
                missing={name:t for name,t in targets.items() if not available(p2,t)}
                if not missing:
                    return finish('candidate',prefix_index,{'prefix':prefix,'core':[describe(first),describe(second)]})
                if len(missing)==2:continue
                for third in finisher_candidates(p2,missing):
                    if not fresh(third,o2):continue
                    stats['third_finishers']+=1
                    p3,o3=extend(p2,o2,third,'s3',stats)
                    if all(available(p3,t) for t in targets.values()):
                        return finish('candidate',prefix_index,{'prefix':prefix,'core':[describe(first),describe(second),describe(third)]})
    return finish('screen_completed_without_hit',len(prefixes))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds',type=float,default=40)
    parser.add_argument('--start-prefix',type=int,default=0)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=search(args.seconds,args.start_prefix)
    result.update({'fixtures':FIXTURES,'start_prefix':args.start_prefix,
                   'scope':'3 input circles plus 3 sequential joint-center objects; floating heuristic only'})
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
