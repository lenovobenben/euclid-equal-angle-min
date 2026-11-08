"""Bounded floating multi-fixture screen for a <=3 E joint center core.

Start after the four original circles. Enumerate an arbitrary first line/circle,
then an object containing M or N, then an object containing the other center.
The two final locus circles cost a further 2 E. This is a heuristic candidate
screen, not an exhaustive lower bound. All hits require exact replay and proof.
"""

import argparse
import itertools
import json
import math
from pathlib import Path
from time import monotonic


FIXTURES = ((37,19,43), (41,23,31), (29,31,53), (53,31,29))
EPS = 2e-8

try:
    import numpy as np
except ImportError:
    np = None


def near(p,q):
    return math.hypot(p[0]-q[0],p[1]-q[1]) < EPS*(1+math.hypot(*p)+math.hypot(*q))


def obj(kind,p,q):
    if near(p,q):
        return None
    if kind == 'line':
        a,b=p[1]-q[1],q[0]-p[0]
        norm=math.hypot(a,b)
        a,b=a/norm,b/norm
        c=-(a*p[0]+b*p[1])
        if a < -EPS or (abs(a)<EPS and b<0):
            a,b,c=-a,-b,-c
        return ('line',(a,b,c))
    return ('circle',(p[0],p[1],(p[0]-q[0])**2+(p[1]-q[1])**2))


def roots(o1,o2):
    k1,v1=o1;k2,v2=o2
    if k1==k2=='line':
        a,b,c=v1;d,e,f=v2
        det=a*e-b*d
        return [] if abs(det)<1e-10 else [((b*f-c*e)/det,(c*d-a*f)/det)]
    if k1==k2=='circle':
        x,y,r=v1;u,v,s=v2
        a,b=2*(u-x),2*(v-y)
        norm=math.hypot(a,b)
        if norm<1e-10:return []
        axis=('line',(a/norm,b/norm,(x*x+y*y-r-u*u-v*v+s)/norm))
        return roots(axis,o1)
    if k1=='circle':return roots(o2,o1)
    a,b,c=v1;x,y,r=v2
    offset=a*x+b*y+c
    foot=(x-a*offset,y-b*offset)
    t2=r-offset*offset
    if t2 < -1e-9:return []
    if abs(t2)<1e-9:return [foot]
    t=math.sqrt(t2)
    return sorted([(foot[0]-b*t,foot[1]+a*t),(foot[0]+b*t,foot[1]-a*t)],
                  key=lambda p:(round(p[0],9),round(p[1],9)))


def contains(o,p):
    kind,v=o;x,y=p
    if kind=='line':
        a,b,c=v
        return abs(a*x+b*y+c)<EPS*(1+abs(x)+abs(y)+abs(c))
    cx,cy,r2=v
    value=(x-cx)**2+(y-cy)**2
    return abs(value-r2)<EPS*(1+value+r2)


def candidates(points):
    keys=list(points)
    for i,j in itertools.combinations(keys,2):
        for kind,first,second in (('line',i,j),('circle',i,j),('circle',j,i)):
            bundle=tuple(obj(kind,p,q) for p,q in zip(points[first],points[second]))
            if all(item is not None for item in bundle):
                yield (kind,first,second,bundle)


def available(points,target):
    return any(all(near(p,q) for p,q in zip(bundle,target)) for bundle in points.values())


def fresh(candidate,objects):
    return not any(all(o[0]==p[0] and all(abs(x-y)<EPS*(1+abs(x)+abs(y))
                   for x,y in zip(o[1],p[1])) for o,p in zip(candidate[3],old))
                   for _,old in objects)


def extend(points,objects,candidate,label,stats):
    new_points=dict(points)
    bundle=candidate[3]
    for old_name,old_bundle in objects:
        rows=[roots(o,p) for o,p in zip(bundle,old_bundle)]
        if len({len(row) for row in rows})!=1:
            stats['mismatched_root_counts']+=1
            continue
        for index in range(len(rows[0])):
            values=tuple(row[index] for row in rows)
            if not available(new_points,values):
                new_points[f'{label}&{old_name}:{index}']=values
    return new_points,objects+[(label,bundle)]


def hit_centers(candidate,targets):
    return tuple(name for name,target in targets.items()
                 if all(contains(o,p) for o,p in zip(candidate[3],target)))


def finisher_candidates(points,targets):
    """Vector prefilter; every yielded object is rechecked by contains()."""
    if np is None:
        yield from (candidate for candidate in candidates(points) if hit_centers(candidate,targets))
        return
    keys=list(points)
    coords=np.asarray([points[key] for key in keys],dtype=float)
    count=len(keys)
    line_mask=np.zeros((count,count),dtype=bool)
    circle_mask=np.zeros((count,count),dtype=bool)
    distances=((coords[:,None,:,:]-coords[None,:,:,:])**2).sum(axis=-1)
    for target in targets.values():
        offsets=coords-np.asarray(target,dtype=float)[None,:,:]
        norms=np.sqrt((offsets**2).sum(axis=-1))
        crosses=offsets[:,None,:,0]*offsets[None,:,:,1]-offsets[:,None,:,1]*offsets[None,:,:,0]
        line_mask |= np.all(np.abs(crosses)<EPS*(1+norms[:,None,:]*norms[None,:,:]),axis=-1)
        goal_dist=(offsets**2).sum(axis=-1)[:,None,:]
        circle_mask |= np.all(np.abs(distances-goal_dist)<EPS*(1+distances+goal_dist),axis=-1)
    for kind,mask in (('line',np.triu(line_mask,k=1)),('circle',circle_mask)):
        for i,j in zip(*np.nonzero(mask)):
            if i==j:continue
            first,second=keys[i],keys[j]
            bundle=tuple(obj(kind,p,q) for p,q in zip(points[first],points[second]))
            candidate=(kind,first,second,bundle)
            if all(o is not None for o in bundle) and hit_centers(candidate,targets):
                yield candidate


def describe(candidate):
    return list(candidate[:3])


def search(seconds):
    start=monotonic(); deadline=start+seconds
    ratios=[(a/b,c/b) for a,b,c in FIXTURES]
    points={
        'A':tuple((-a,0.) for a,c in ratios),
        'B':tuple((0.,0.) for a,c in ratios),
        'C':tuple((1.,0.) for a,c in ratios),
        'D':tuple((1.+c,0.) for a,c in ratios),
    }
    objects=[('l',tuple(('line',(0.,1.,0.)) for _ in ratios))]
    stats={'first_candidates':0,'second_finishers':0,'third_candidates':0,'mismatched_root_counts':0}
    for name,p,q in (('GammaA','A','B'),('GammaD','D','C'),('GammaB','B','C'),('GammaC','C','B')):
        bundle=tuple(obj('circle',x,y) for x,y in zip(points[p],points[q]))
        points,objects=extend(points,objects,('circle',p,q,bundle),name,stats)
    targets={'M':tuple((a/(a-1),0.) for a,c in ratios),
             'N':tuple((1/(1-c),0.) for a,c in ratios)}
    base_count=len(points)
    for first in candidates(points):
        if monotonic()>deadline:
            return {'status':'budget_exhausted','stats':stats,'base_points':base_count,'elapsed':monotonic()-start}
        if not fresh(first,objects):continue
        stats['first_candidates']+=1
        p1,o1=extend(points,objects,first,'s1',stats)
        present={name for name,t in targets.items() if available(p1,t)}
        for second in candidates(p1):
            if not fresh(second,o1):continue
            hits=hit_centers(second,targets)
            if not hits and not present:continue
            stats['second_finishers']+=1
            p2,o2=extend(p1,o1,second,'s2',stats)
            done={name for name,t in targets.items() if available(p2,t)}
            if len(done)==2:
                return {'status':'candidate','program':[describe(first),describe(second)],'stats':stats,'elapsed':monotonic()-start}
            if not done:continue
            missing={name:t for name,t in targets.items() if name not in done}
            for third in candidates(p2):
                stats['third_candidates']+=1
                if fresh(third,o2) and hit_centers(third,missing):
                    p3,_=extend(p2,o2,third,'s3',stats)
                    if not all(available(p3,t) for t in targets.values()):continue
                    return {'status':'candidate','program':[describe(first),describe(second),describe(third)],
                            'stats':stats,'base_points':base_count,'elapsed':monotonic()-start}
    return {'status':'screen_completed_without_hit','stats':stats,'base_points':base_count,'elapsed':monotonic()-start}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds',type=float,default=45)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=search(args.seconds)
    result['fixtures']=FIXTURES
    result['scope']='four-circle prefix; arbitrary first object, second center carrier, third other-center carrier; floating prefilter only'
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
