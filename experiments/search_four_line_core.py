"""8 E screen: two seed circles, four lines, two canonical target circles.

Unlike the two-plus-two center screen, the first center may first appear on
line 3 and the second on line 4. A fresh line cannot create two distinct
points of the existing input axis, so filtering line 3 when neither center
exists after line 2 preserves this declared shape (subject to float bindings).
No claim about programs using other circle/line patterns or a lower bound.
"""

import argparse
import itertools
import json
from pathlib import Path
from time import monotonic
from search_shared_centers import (available, candidates, describe, extend,
                                   finisher_candidates, fresh, obj)
from search_dynamic_prefix import REGIONS


REGIONS = {**REGIONS,
           'chamber': ((47,29,37),(67,41,53),(79,47,61)),
           'short-chamber': ((47,29,23),(67,41,31),(79,47,37))}


def core_candidates(points, objects, targets=None, lines_only=True):
    source = candidates(points) if targets is None else finisher_candidates(points, targets)
    for candidate in source:
        if (not lines_only or candidate[0] == 'line') and fresh(candidate, objects):
            yield candidate


def search(region, seconds, start_prefix, mixed=False):
    start = monotonic()
    deadline = start + seconds
    fixtures = REGIONS[region]
    ratios = [(a/b,c/b) for a,b,c in fixtures]
    initial = {'A':tuple((-a,0.) for a,c in ratios),
               'B':tuple((0.,0.) for a,c in ratios),
               'C':tuple((1.,0.) for a,c in ratios),
               'D':tuple((1+c,0.) for a,c in ratios)}
    targets = {'M':tuple((a/(a-1),0.) for a,c in ratios),
               'N':tuple((1/(1-c),0.) for a,c in ratios)}
    stats = {'prefixes':0, 'first_lines':0, 'second_lines':0,
             'third_lines':0, 'fourth_lines':0, 'mismatched_root_counts':0}
    preferred = (('A','B'),('B','C'))
    prefixes = [preferred] + [p for p in itertools.combinations(itertools.permutations('ABCD',2),2)
                              if p != preferred]

    def answer(status, index, program=None):
        result = {'status':status,'region':region,'fixtures':fixtures,
                  'start_prefix':start_prefix, 'repeat_prefix_index':index,
                  'stats':stats,'elapsed':monotonic()-start,
                  'mixed':mixed,
                  'scope':'2 input circles + <=4 core draws + 2 canonical loci; first center by core draw 3; float screening; skipped mismatched bindings; no lower bound'}
        if program is not None:
            result['program'] = program
        return result

    def missing(points):
        return {name:t for name,t in targets.items() if not available(points,t)}

    for index, prefix in enumerate(prefixes):
        if index < start_prefix:
            continue
        if monotonic() > deadline:
            return answer('budget_exhausted',index)
        stats['prefixes'] += 1
        points = dict(initial)
        objects = [('l',tuple(('line',(0.,1.,0.)) for _ in ratios))]
        for i,(p,q) in enumerate(prefix):
            candidate = ('circle',p,q,tuple(obj('circle',x,y) for x,y in zip(points[p],points[q])))
            points,objects = extend(points,objects,candidate,f'c{i}',stats)
        for first in core_candidates(points,objects,lines_only=not mixed):
            stats['first_lines'] += 1
            p1,o1 = extend(points,objects,first,'s1',stats)
            for second in core_candidates(p1,o1,lines_only=not mixed):
                if monotonic() > deadline:
                    return answer('budget_exhausted',index)
                stats['second_lines'] += 1
                p2,o2 = extend(p1,o1,second,'s2',stats)
                if not missing(p2):
                    return answer('candidate',index,{'prefix':prefix,'core':[describe(first),describe(second)]})
                filter_targets = missing(p2) if len(missing(p2)) == 2 else None
                for third in core_candidates(p2,o2,filter_targets,lines_only=not mixed):
                    stats['third_lines'] += 1
                    p3,o3 = extend(p2,o2,third,'s3',stats)
                    remaining = missing(p3)
                    if not remaining:
                        return answer('candidate',index,{'prefix':prefix,'core':[describe(first),describe(second),describe(third)]})
                    if len(remaining) == 2:
                        continue
                    for fourth in core_candidates(p3,o3,remaining,lines_only=not mixed):
                        stats['fourth_lines'] += 1
                        p4,o4 = extend(p3,o3,fourth,'s4',stats)
                        if not missing(p4):
                            return answer('candidate',index,{'prefix':prefix,'core':[describe(c) for c in (first,second,third,fourth)]})
    return answer('screen_completed_without_hit',len(prefixes))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--region',choices=tuple(REGIONS),default='chamber')
    parser.add_argument('--seconds',type=float,default=40)
    parser.add_argument('--start-prefix',type=int,default=0)
    parser.add_argument('--mixed',action='store_true',help='Permit circles among core draws; excludes both centers first appearing on the last draw.')
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    result = search(args.region,args.seconds,args.start_prefix,args.mixed)
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
