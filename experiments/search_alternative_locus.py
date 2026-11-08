"""8 E virtual-witness screen for noncanonical first target loci.

After three input circles and an arbitrary fourth draw, one more draw is
filtered by witnesses: a point on a target-radius circle about a known axis
center; a new axis center through a known radius endpoint; or points on the
target's vertical line. Witnesses only filter candidates, never enter state.
Draw the actual first target locus at step 6, then allow a two-draw target tail.
"""

import argparse
import itertools
import json
from math import sqrt
from pathlib import Path
from time import monotonic
from search_shared_centers import (available,candidates,contains,describe,extend,
                                  fresh,finisher_candidates,near,obj,roots)
from search_output_first import REGIONS


def target_points(ratios):
    return {label:tuple(((a-1)*(1+c)/(2*(a*c-1)),
                        sign*sqrt((a+1)*(1+c)*(3*a*c-a-1-c))/(2*(a*c-1))) for a,c in ratios)
            for label,sign in (('upper',1),('lower',-1))}


def witnesses(points,objects,target,stats):
    result={}
    def add(name,bundle):
        if all(abs(x)<1e8 and abs(y)<1e8 for x,y in bundle) and not available(points,bundle) and not available(result,bundle):
            result[name]=bundle
    virtual=[('vertical',tuple(('line',(1.,0.,-p[0])) for p in target))]
    for key,bundle in points.items():
        if all(abs(p[1])<1e-8 for p in bundle):
            virtual.append(('radius_'+key,tuple(obj('circle',p,q) for p,q in zip(bundle,target))))
        # With a new axis center O, an old radius endpoint Q implies
        # O_x=(|P|^2-|Q|^2)/(2(P_x-Q_x)).
        if all(abs(p[0]-q[0])>1e-8 for p,q in zip(target,bundle)):
            centers=tuple((((p[0]**2+p[1]**2)-(q[0]**2+q[1]**2))/(2*(p[0]-q[0])),0.)
                          for p,q in zip(target,bundle))
            add('center_through_'+key,centers)
    for name,virtual_bundle in virtual:
        for old_name,old_bundle in objects:
            rows=[roots(v,o) for v,o in zip(virtual_bundle,old_bundle)]
            if len({len(row) for row in rows})!=1:
                stats['virtual_mismatched_roots']+=1
                continue
            for index in range(len(rows[0])):
                add(f'{name}&{old_name}:{index}',tuple(row[index] for row in rows))
    return result


def setup(region):
    fixtures=REGIONS[region];ratios=[(a/b,c/b) for a,b,c in fixtures]
    initial={'A':tuple((-a,0.) for a,c in ratios),'B':tuple((0.,0.) for a,c in ratios),
             'C':tuple((1.,0.) for a,c in ratios),'D':tuple((1.+c,0.) for a,c in ratios)}
    axis=[('l',tuple(('line',(0.,1.,0.)) for _ in ratios))]
    return fixtures,ratios,initial,axis,target_points(ratios)


def calibration():
    fixtures,ratios,points,objects,targets=setup('all')
    stats={'mismatched_root_counts':0,'virtual_mismatched_roots':0}
    for index,(p,q) in enumerate((('A','B'),('B','C'),('C','D'))):
        candidate=('circle',p,q,tuple(obj('circle',x,y) for x,y in zip(points[p],points[q])))
        points,objects=extend(points,objects,candidate,f'c{index}',stats)
    lookup=lambda values:next(k for k,bundle in points.items() if all(near(p,q) for p,q in zip(values,bundle)))
    E=lookup(tuple((-1.,0.) for a,c in ratios))
    H=lookup(tuple((-1/(2*a),-sqrt(4*a*a-1)/(2*a)) for a,c in ratios))
    G=lookup(tuple((-1/(2*a),sqrt(4*a*a-1)/(2*a)) for a,c in ratios))
    HE=('line',H,E,tuple(obj('line',p,q) for p,q in zip(points[H],points[E])))
    points,objects=extend(points,objects,HE,'HE',stats)
    K=lookup(tuple((-a-.5,sqrt(4*a*a-1)/2) for a,c in ratios))
    KG=('line',K,G,tuple(obj('line',p,q) for p,q in zip(points[K],points[G])))
    witness=witnesses(points,objects,targets['upper'],stats)
    m=tuple((a/(a-1),0.) for a,c in ratios)
    assert not available(points,m)
    assert available(witness,m)
    assert any(all(o[0]==p[0] and all(abs(x-y)<1e-7 for x,y in zip(o[1],p[1]))
                   for o,p in zip(candidate[3],KG[3]))
               for candidate in finisher_candidates(points,witness))
    p5,o5=extend(points,objects,KG,'KG',stats)
    assert available(p5,m)
    return {'known_M_witness':True,'known_KG_candidate_retained':True,'oracle_not_injected':True}


def search(region,seconds,start_prefix,skip_canonical=True):
    start=monotonic();deadline=start+seconds
    fixtures,ratios,initial,axis,targets=setup(region)
    centers={'M':tuple((a/(a-1),0.) for a,c in ratios),'N':tuple((1/(1-c),0.) for a,c in ratios)}
    preferred=(('A','B'),('B','C'),('C','D'))
    prefixes=[preferred]+[p for p in itertools.combinations(itertools.permutations('ABCD',2),3) if p!=preferred]
    stats={'prefixes':0,'fourth_objects':0,'fifth_witness_objects':0,'noncanonical_loci':0,
           'tail_objects':0,'mismatched_root_counts':0,'virtual_mismatched_roots':0}
    locus_examples=[]
    def answer(status,index,program=None):
        data={'status':status,'region':region,'repeat_prefix_index':index,'fixtures':fixtures,
              'stats':stats,'elapsed':monotonic()-start,'locus_examples':locus_examples,
              'scope':'specified virtual witness shapes only, finite multi-fixture floats, no lower-bound claim'}
        if program is not None:data['program']=program
        return data
    for prefix_index,prefix in enumerate(prefixes):
        if prefix_index<start_prefix:continue
        if monotonic()>deadline:return answer('budget_exhausted',prefix_index)
        stats['prefixes']+=1
        points=dict(initial);objects=list(axis)
        for index,(p,q) in enumerate(prefix):
            candidate=('circle',p,q,tuple(obj('circle',x,y) for x,y in zip(points[p],points[q])))
            points,objects=extend(points,objects,candidate,f'c{index}',stats)
        for fourth in candidates(points):
            if monotonic()>deadline:return answer('budget_exhausted',prefix_index)
            if not fresh(fourth,objects):continue
            stats['fourth_objects']+=1
            p4,o4=extend(points,objects,fourth,'s4',stats)
            virtual=witnesses(p4,o4,targets['upper'],stats)
            if not virtual:continue
            for fifth in finisher_candidates(p4,virtual):
                if monotonic()>deadline:return answer('budget_exhausted',prefix_index)
                if not fresh(fifth,o4):continue
                stats['fifth_witness_objects']+=1
                p5,o5=extend(p4,o4,fifth,'s5',stats)
                for locus in finisher_candidates(p5,targets):
                    if not fresh(locus,o5):continue
                    center_bundle=p5[locus[1]]
                    if skip_canonical and locus[0]=='circle' and any(all(near(p,q) for p,q in zip(center_bundle,center)) for center in centers.values()):
                        continue
                    stats['noncanonical_loci']+=1
                    description={'prefix':prefix,'fourth':describe(fourth),'fifth':describe(fifth),'locus':describe(locus)}
                    if len(locus_examples)<5:locus_examples.append(description)
                    p6,o6=extend(p5,o5,locus,'locus',stats)
                    for first in candidates(p6):
                        if monotonic()>deadline:return answer('budget_exhausted',prefix_index)
                        if not fresh(first,o6):continue
                        stats['tail_objects']+=1
                        p7,o7=extend(p6,o6,first,'t1',stats)
                        for last in finisher_candidates(p7,targets):
                            if not fresh(last,o7):continue
                            p8,o8=extend(p7,o7,last,'t2',stats)
                            hit=[name for name,target in targets.items() if available(p8,target)]
                            if hit:return answer('candidate',prefix_index,{**description,'tail':[describe(first),describe(last)],'target_sides':hit})
    return answer('screen_completed_without_hit',len(prefixes))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--region',choices=tuple(REGIONS),default='all')
    parser.add_argument('--seconds',type=float,default=40)
    parser.add_argument('--start-prefix',type=int,default=0)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    control=calibration()
    result=search(args.region,args.seconds,args.start_prefix)
    result['positive_control']=control
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
