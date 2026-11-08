"""Independent floating cross-check of carriers through draw 4; not a proof.

Enumerates adaptive first two circles, every third object, and all fourth
objects through the target using the existing numeric geometry engine.
Retains a known fifth-draw target circle as a positive control.
"""

import argparse
import json
from pathlib import Path
from time import monotonic
from math import sqrt
from search_shared_centers import (available,candidates,contains,describe,extend,
                                   finisher_candidates,fresh,near,obj)
from search_four_line_core import REGIONS


def audit():
    start = monotonic()
    fixtures = REGIONS['chamber']
    ratios = [(a/b,c/b) for a,b,c in fixtures]
    initial = {'A':tuple((-a,0.) for a,c in ratios),'B':tuple((0.,0.) for a,c in ratios),
               'C':tuple((1.,0.) for a,c in ratios),'D':tuple((1+c,0.) for a,c in ratios)}
    axis = [('l',tuple(('line',(0.,1.,0.)) for _ in ratios))]
    targets = {'upper':tuple(((a-1)*(1+c)/(2*(a*c-1)),
                              sqrt((a+1)*(1+c)*(3*a*c-a-1-c))/(2*(a*c-1)))
                             for a,c in ratios)}
    stats = {'first_circles':0,'seed_pairs':0,'third_objects':0,
             'fourth_carrier_candidates':0,'mismatched_root_counts':0}
    hits = []
    for first in candidates(initial):
        if first[0] != 'circle':
            continue
        stats['first_circles'] += 1
        p1,o1 = extend(initial,axis,first,'c1',stats)
        for second in candidates(p1):
            if second[0] != 'circle' or not fresh(second,o1):
                continue
            stats['seed_pairs'] += 1
            p2,o2 = extend(p1,o1,second,'c2',stats)
            for third in candidates(p2):
                if not fresh(third,o2):
                    continue
                stats['third_objects'] += 1
                p3,o3 = extend(p2,o2,third,'s3',stats)
                for fourth in finisher_candidates(p3,targets):
                    if not fresh(fourth,o3):
                        continue
                    stats['fourth_carrier_candidates'] += 1
                    hits.append([describe(c) for c in (first,second,third,fourth)])

    # Draw only the first four objects of the known five-draw carrier prefix.
    points,objects = dict(initial),list(axis)
    def draw(kind,p,q,label):
        nonlocal points,objects
        candidate = (kind,p,q,tuple(obj(kind,x,y) for x,y in zip(points[p],points[q])))
        points,objects = extend(points,objects,candidate,label,stats)
    def lookup(bundle):
        return next(name for name,value in points.items()
                    if all(near(p,q) for p,q in zip(bundle,value)))
    draw('circle','A','B','GammaA')
    draw('circle','B','C','GammaB')
    E = lookup(tuple((-1.,0.) for a,c in ratios))
    G = lookup(tuple((-1/(2*a),sqrt(4*a*a-1)/(2*a)) for a,c in ratios))
    H = lookup(tuple((-1/(2*a),-sqrt(4*a*a-1)/(2*a)) for a,c in ratios))
    draw('line',H,E,'HE')
    K = lookup(tuple((-a-.5,sqrt(4*a*a-1)/2) for a,c in ratios))
    draw('line',K,G,'KG')
    M = lookup(tuple((a/(a-1),0.) for a,c in ratios))
    expected = tuple(obj('circle',p,q) for p,q in zip(points[M],points['B']))
    assert all(contains(o,p) for o,p in zip(expected,targets['upper']))
    assert any(candidate[:3] == ('circle',M,'B') for candidate in finisher_candidates(points,targets))
    assert not available(points,targets['upper'])
    assert not hits
    return {'status':'passed','fixtures':fixtures,'stats':stats,'hits':hits,
            'positive_control':'known fifth-draw Circle(M,B) retained; target never injected',
            'elapsed':monotonic()-start,
            'scope':'independent multi-fixture numeric cross-check; skipped bindings; not the lower-bound proof'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    result = audit()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
