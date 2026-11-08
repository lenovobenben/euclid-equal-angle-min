"""Symbolic 4-circle target-field screen, changing the first-locus prefix.

Two axis-centered seed circles give G. Circle(G,Q) creates a rational axis
point T=2Gx-Q. The fourth circle uses T as center or through-point. Search for
an odd target-Delta factor in its intersections with existing circles.
"""

import argparse
import json
from pathlib import Path
from sage.all import PolynomialRing,QQ
from sage.env import SAGE_VERSION


def search():
    ring=PolynomialRing(QQ,names=('a','b','c'))
    a,b,c=ring.gens();field=ring.fraction_field()
    delta=3*a*c-b*(a+b+c)
    ideal=ring.ideal(delta)
    def target_factor(poly):
        if poly==0 or ideal.reduce(poly)!=0:
            return False
        # An exponent of 3, 5, ... is just as relevant as an exponent of 1.
        return next(exponent % 2 == 1 for factor,exponent in poly.factor()
                    if ideal.reduce(factor)==0)
    assert target_factor(delta) and target_factor(delta**3)
    assert not target_factor(delta**2) and not target_factor(delta**4)
    # Known final pair is a positive control for the symbolic factor test.
    m=field(a*b)/(a-b);n=field(b*b)/(b-c)
    dist2=(m-n)**2
    known=4*dist2*m*m-(dist2+m*m-(n-b)**2)**2
    assert target_factor(known.numerator())
    initial={'A':-a,'B':ring(0),'C':b,'D':b+c}
    seen=set();hits=[]
    stats={'seed_pairs':0,'third_circles':0,'fourth_circles':0,'discriminants':0}
    for ac,X in initial.items():
        for at,Y in initial.items():
            if X==Y:continue
            r1=(Y-X)**2
            axis1={**initial,'E':2*X-Y}
            for bc,Z in axis1.items():
                for bt,W in axis1.items():
                    if Z==W or Z==X:continue
                    r2=(W-Z)**2;d=Z-X
                    key=(X,r1,Z,r2)
                    if key in seen:continue
                    seen.add(key);stats['seed_pairs']+=1
                    gx_num=r1-r2+Z*Z-X*X
                    hnum=4*d*d*r1-(gx_num-2*d*X)**2
                    if hnum==0:continue
                    axis2={**axis1,'F':2*Z-W}
                    unique=dict((value,name) for name,value in axis2.items())
                    for q,qname in unique.items():
                        stats['third_circles']+=1
                        radius3_num=d*(r1+q*q-X*X)+(X-q)*gx_num
                        tnum=gx_num-q*d
                        for through,pname in unique.items():
                            r4num=(tnum-d*through)**2
                            if r4num==0:continue
                            for center_T in (True,False):
                                stats['fourth_circles']+=1
                                for seed,S,ri in ((1,X,r1),(2,Z,r2)):
                                    sepnum=(tnum-d*S)**2 if center_T else d*d*(through-S)**2
                                    disc=4*sepnum*ri*d*d-(sepnum+ri*d*d-r4num)**2
                                    stats['discriminants']+=1
                                    if target_factor(disc):
                                        hits.append({'first':['circle',ac,at],'second':['circle',bc,bt],
                                                     'third':['circle','G',qname],
                                                     'fourth':['circle','T',pname] if center_T else ['circle',pname,'T'],
                                                     'against':seed,'factor':str(disc.factor()),
                                                     'seed_height_numerator':str(hnum.factor())})
                                if center_T:
                                    disc=4*radius3_num*d-r4num
                                    stats['discriminants']+=1
                                    if target_factor(disc):
                                        hits.append({'first':['circle',ac,at],'second':['circle',bc,bt],
                                                     'third':['circle','G',qname],
                                                     'fourth':['circle','T',pname],'against':3,
                                                     'factor':str(disc.factor()),
                                                     'seed_height_numerator':str(hnum.factor())})
    return {'sage_version':SAGE_VERSION,'status':'completed','stats':stats,'hits':hits,
            'positive_control':'known GammaM/GammaN discriminant has odd Delta factor',
            'scope':'restricted four-circle shape; exact polynomial divisibility; no global lower bound'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=search()
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
