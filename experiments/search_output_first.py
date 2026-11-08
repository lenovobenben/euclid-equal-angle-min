"""8 E screen where a first target circle participates in later construction.

Three input circles, <=2 draws to one locus center, draw that locus (<=6 E),
then two arbitrary draws to a target. Unlike the earlier joint-center screen,
new intersections of the first target circle can define the final two draws.
"""

import argparse
import itertools
import json
from math import sqrt
from pathlib import Path
from time import monotonic
from search_shared_centers import available,candidates,describe,extend,fresh,finisher_candidates,obj,near
from search_three_circle_prefix import completions
from search_dynamic_prefix import REGIONS


REGIONS={**REGIONS,'near':((23,20,21),(12,10,11),(23,20,19),(30,25,24))}


def search(region,seconds,start_prefix):
    start=monotonic();deadline=start+seconds
    fixtures=REGIONS[region];ratios=[(a/b,c/b) for a,b,c in fixtures]
    initial={'A':tuple((-a,0.) for a,c in ratios),'B':tuple((0.,0.) for a,c in ratios),
             'C':tuple((1.,0.) for a,c in ratios),'D':tuple((1.+c,0.) for a,c in ratios)}
    centers={'M':tuple((a/(a-1),0.) for a,c in ratios),'N':tuple((1/(1-c),0.) for a,c in ratios)}
    targets={label:tuple(((a-1)*(1+c)/(2*(a*c-1)),
                         sign*sqrt((a+1)*(1+c)*(3*a*c-a-1-c))/(2*(a*c-1))) for a,c in ratios)
             for label,sign in (('upper',1),('lower',-1))}
    preferred=(('A','B'),('B','C'),('C','D'))
    prefixes=[preferred]+[prefix for prefix in itertools.combinations(itertools.permutations('ABCD',2),3) if prefix!=preferred]
    stats={'prefixes':0,'first_core_objects':0,'second_core_candidates':0,'locus_programs':0,
           'tail_first_objects':0,'tail_finishers':0,'mismatched_root_counts':0}
    def answer(status,index,program=None):
        result={'status':status,'repeat_prefix_index':index,'region':region,'fixtures':fixtures,
                'stats':stats,'elapsed':monotonic()-start,
                'scope':'3 input circles; <=2 draws first center; target circle drawn early; 2-draw target tail; floating screening only'}
        if program is not None:result['program']=program
        return result
    for index,prefix in enumerate(prefixes):
        if index<start_prefix:continue
        if monotonic()>deadline:return answer('budget_exhausted',index)
        stats['prefixes']+=1
        points=dict(initial);objects=[('l',tuple(('line',(0.,1.,0.)) for _ in ratios))]
        for i,(p,q) in enumerate(prefix):
            candidate=('circle',p,q,tuple(obj('circle',x,y) for x,y in zip(points[p],points[q])))
            points,objects=extend(points,objects,candidate,f'c{i}',stats)
        for goal,through in (('M','B'),('N','C')):
            for p1,o1,core in completions(points,objects,centers[goal],'u',deadline,stats):
                stats['locus_programs']+=1
                center_id=next(key for key,bundle in p1.items() if all(near(p,q) for p,q in zip(bundle,centers[goal])))
                locus=('circle',center_id,through,tuple(obj('circle',p,q) for p,q in zip(p1[center_id],p1[through])))
                if not fresh(locus,o1):continue
                p2,o2=extend(p1,o1,locus,'locus',stats)
                for first in candidates(p2):
                    if monotonic()>deadline:return answer('budget_exhausted',index)
                    if not fresh(first,o2):continue
                    stats['tail_first_objects']+=1
                    p3,o3=extend(p2,o2,first,'t1',stats)
                    hit=[name for name,target in targets.items() if available(p3,target)]
                    if hit:
                        return answer('candidate',index,{'prefix':prefix,'center':goal,'core':core,
                                      'locus':describe(locus),'tail':[describe(first)],'target_sides':hit})
                    for last in finisher_candidates(p3,targets):
                        if not fresh(last,o3):continue
                        stats['tail_finishers']+=1
                        p4,o4=extend(p3,o3,last,'t2',stats)
                        hit=[name for name,target in targets.items() if available(p4,target)]
                        if hit:
                            return answer('candidate',index,{'prefix':prefix,'center':goal,'core':core,
                                          'locus':describe(locus),'tail':[describe(first),describe(last)],'target_sides':hit})
    return answer('screen_completed_without_hit',len(prefixes))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--region',choices=tuple(REGIONS),default='all')
    parser.add_argument('--seconds',type=float,default=40)
    parser.add_argument('--start-prefix',type=int,default=0)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=search(args.region,args.seconds,args.start_prefix)
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
