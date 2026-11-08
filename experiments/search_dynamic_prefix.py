"""8 E screens with adaptive circle centers, not a fixed first target circle.

adaptive-two: the second circle may use a reflected point made by the first;
then <=2 objects per locus center. point-third: a third circle centered at a
new off-axis seed intersection, followed by three joint-center objects.
All screening is floating and branch-limited; no lower-bound claim.
"""

import argparse
import itertools
import json
from pathlib import Path
from time import monotonic
from search_shared_centers import available,candidates,describe,extend,fresh,finisher_candidates,obj
from search_three_circle_prefix import completions


REGIONS={
    'all':((43,19,37),(41,23,31),(53,31,29),(59,41,37)),
    'outer-shorter':((53,31,29),(59,41,37),(40,5,2)),
    'outer-longer':((43,19,37),(41,23,31),(71,37,43)),
}


def joint_three(points,objects,targets,deadline,stats):
    for first in candidates(points):
        if monotonic()>deadline:return
        if not fresh(first,objects):continue
        stats['joint_first_objects']+=1
        p1,o1=extend(points,objects,first,'j1',stats)
        present={name for name,t in targets.items() if available(p1,t)}
        seconds=candidates(p1) if present else finisher_candidates(p1,targets)
        for second in seconds:
            if monotonic()>deadline:return
            if not fresh(second,o1):continue
            stats['joint_second_finishers']+=1
            p2,o2=extend(p1,o1,second,'j2',stats)
            missing={name:t for name,t in targets.items() if not available(p2,t)}
            if not missing:
                yield [describe(first),describe(second)]
            if len(missing)!=1:continue
            for third in finisher_candidates(p2,missing):
                if not fresh(third,o2):continue
                p3,o3=extend(p2,o2,third,'j3',stats)
                if all(available(p3,t) for t in targets.values()):
                    yield [describe(first),describe(second),describe(third)]


def search(mode,region,seconds):
    start=monotonic();deadline=start+seconds
    fixtures=REGIONS[region]
    ratios=[(a/b,c/b) for a,b,c in fixtures]
    initial={'A':tuple((-a,0.) for a,c in ratios),'B':tuple((0.,0.) for a,c in ratios),
             'C':tuple((1.,0.) for a,c in ratios),'D':tuple((1.+c,0.) for a,c in ratios)}
    axis=[('l',tuple(('line',(0.,1.,0.)) for _ in ratios))]
    targets={'M':tuple((a/(a-1),0.) for a,c in ratios),'N':tuple((1/(1-c),0.) for a,c in ratios)}
    stats={'prefixes':0,'first_core_objects':0,'second_core_candidates':0,
           'first_center_programs':0,'joint_first_objects':0,'joint_second_finishers':0,
           'mismatched_root_counts':0}
    def result(status,program=None):
        data={'status':status,'mode':mode,'region':region,'fixtures':fixtures,
              'stats':stats,'elapsed':monotonic()-start,
              'scope':'adaptive circle prefixes and declared center order; float screening, skipped mismatched branches; no lower bound'}
        if program is not None:data['program']=program
        return data
    def check_pair(points,objects,prefix):
        stats['prefixes']+=1
        for goal,other in (('M','N'),('N','M')):
            for p1,o1,core in completions(points,objects,targets[goal],'u',deadline,stats):
                stats['first_center_programs']+=1
                for p2,o2,tail in completions(p1,o1,targets[other],'v',deadline,stats):
                    return {'prefix':prefix,'order':[goal,other],'core':core,'tail':tail}
        return None
    if mode=='adaptive-two':
        for first in candidates(initial):
            if first[0]!='circle':continue
            p1,o1=extend(initial,axis,first,'c1',stats)
            for second in candidates(p1):
                if monotonic()>deadline:return result('budget_exhausted')
                if second[0]!='circle' or not fresh(second,o1):continue
                p2,o2=extend(p1,o1,second,'c2',stats)
                hit=check_pair(p2,o2,[describe(first),describe(second)])
                if hit:return result('candidate',hit)
        return result('screen_completed_without_hit')
    preferred=(('A','B'),('B','C'))
    seeds=[preferred]+[pair for pair in itertools.combinations(itertools.permutations('ABCD',2),2) if pair!=preferred]
    for seed_index,pair in enumerate(seeds):
        if monotonic()>deadline:
            answer=result('budget_exhausted');answer['last_seed_index']=seed_index;return answer
        points=dict(initial);objects=list(axis)
        for index,(p,q) in enumerate(pair):
            candidate=('circle',p,q,tuple(obj('circle',x,y) for x,y in zip(points[p],points[q])))
            points,objects=extend(points,objects,candidate,f'c{index+1}',stats)
        thirds=[candidate for candidate in candidates(points)
                if candidate[0]=='circle' and all(p[1]>1e-7 for p in points[candidate[1]]) and fresh(candidate,objects)]
        thirds.sort(key=lambda item:({'D':0,'A':1,'C':2,'B':3}.get(item[2],4),item[1],item[2]))
        for third in thirds:
            if monotonic()>deadline:
                answer=result('budget_exhausted');answer['last_seed_index']=seed_index;return answer
            stats['prefixes']+=1
            p3,o3=extend(points,objects,third,'c3',stats)
            for core in joint_three(p3,o3,targets,deadline,stats):
                return result('candidate',{'seed':pair,'third':describe(third),'core':core})
    return result('screen_completed_without_hit')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=('adaptive-two','point-third'),default='point-third')
    parser.add_argument('--region',choices=tuple(REGIONS),default='all')
    parser.add_argument('--seconds',type=float,default=40)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    answer=search(args.mode,args.region,args.seconds)
    if args.output:args.output.write_text(json.dumps(answer,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(answer,indent=2))
