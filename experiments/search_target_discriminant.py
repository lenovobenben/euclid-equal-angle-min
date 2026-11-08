"""Symbolic target-field screen with two input/axis-centered seed circles.

After two circles let G be an off-axis intersection. A third circle centered
at G through an available axis point Q intersects a seed circle. Search for
the target irreducible Delta factor in its intersection discriminant.
This is a necessary field test for this shape, not a construction/lower bound.
"""

import json
import argparse
from pathlib import Path
from sage.all import PolynomialRing,QQ
from sage.env import SAGE_VERSION


def search():
    ring=PolynomialRing(QQ,names=('a','b','c'))
    a,b,c=ring.gens()
    delta=3*a*c-b*(a+b+c)
    ideal=ring.ideal(delta)
    initial={'A':-a,'B':ring(0),'C':b,'D':b+c}
    seen=set();hits=[]
    stats={'seed_pairs':0,'third_circles':0,'tests':0,'generic_tangencies_skipped':0}
    for first_center,X in initial.items():
        for first_through,Y in initial.items():
            if X==Y:continue
            r1=(Y-X)**2
            axis1=dict(initial)
            axis1['E']=2*X-Y
            for second_center,Z in axis1.items():
                for second_through,W in axis1.items():
                    if Z==W or Z==X:continue
                    r2=(W-Z)**2;d=Z-X
                    key=(X,r1,Z,r2)
                    if key in seen:continue
                    seen.add(key);stats['seed_pairs']+=1
                    gx_num=r1-r2+Z*Z-X*X
                    height_num=4*d*d*r1-(gx_num-2*d*X)**2
                    if height_num==0:
                        stats['generic_tangencies_skipped']+=1
                        continue
                    axis2=dict(axis1);axis2['F']=2*Z-W
                    for q,q_name in dict((value,name) for name,value in axis2.items()).items():
                        stats['third_circles']+=1
                        radius_num=d*(r1+q*q-X*X)+(X-q)*gx_num
                        for seed,ri in ((1,r1),(2,r2)):
                            for factor,poly in (('radius2',radius_num),('four_seed_radius2_minus_radius2',4*ri*d-radius_num)):
                                stats['tests']+=1
                                if poly!=0 and ideal.reduce(poly)==0:
                                    hits.append({'first':['circle',first_center,first_through],
                                                 'second':['circle',second_center,second_through],
                                                 'third':['circle','G',q_name],
                                                 'seed_intersection':seed,'factor':factor,
                                                 'factor_polynomial':str(poly.factor()),
                                                 'seed_height_numerator':str(height_num.factor())})
    return {'sage_version':SAGE_VERSION,'status':'completed','stats':stats,'hits':hits,
            'scope':'two axis-centered seed circles plus circle centered at G; divisibility by Delta only; no lower bound'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=search()
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
