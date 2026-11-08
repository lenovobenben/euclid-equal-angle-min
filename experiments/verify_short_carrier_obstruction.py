"""Exact necessary-condition screen for a target carrier drawn by step 4.

Two circles can supply just one off-axis mirror pair G,H. Enumerate adaptive
axis-centered seeds, then all shapes for the third draw. Test target-Delta
square classes in the third state and possible axis centers on k=ac-b^2=0.
This script reports obstructions, not a lower bound without the accompanying
exhaustiveness and valuation proof.
"""

import argparse
import json
from pathlib import Path
from sage.all import PolynomialRing, QQ
from sage.env import SAGE_VERSION


def verify():
    ring = PolynomialRing(QQ,names=('a','b','c'))
    a,b,c = ring.gens()
    field = ring.fraction_field()
    k = a*c-b*b
    delta = 3*a*c-b*(a+b+c)
    assert len(list(k.factor())) == 1 and list(k.factor())[0][1] == 1
    assert len(list(delta.factor())) == 1 and list(delta.factor())[0][1] == 1
    ik = ring.ideal(k)
    idelta = ring.ideal(delta)
    initial = {'A':-a,'B':ring(0),'C':b,'D':b+c}
    stats = {'seed_pairs':0,'generic_tangencies':0,'field_tests':0,
             'center_residue_tests':0,'k_unit_tests':0}
    field_hits = []
    center_hits = []
    target_residue_center = field(a*b)/(a-b)

    def odd_delta(value):
        value = field(value)
        parity = 0
        for polynomial in (value.numerator(),value.denominator()):
            if polynomial == 0:
                return False
            if idelta.reduce(polynomial) == 0:
                parity += next(exponent for factor,exponent in polynomial.factor()
                               if idelta.reduce(factor) == 0)
        return bool(parity % 2)

    # Positive and negative controls cover odd exponents beyond one.
    assert odd_delta(delta) and odd_delta(delta**3) and odd_delta(1/delta)
    assert not odd_delta(delta**2) and not odd_delta(1/delta**2)
    y2 = field(b*b*(a+b)*(b+c)*delta)/(4*k*k)
    assert odd_delta(y2)
    x0 = field(b*(a-b)*(b+c))/(2*k)
    rho = field(a*b*b*(b+c))/k
    assert rho == 2*target_residue_center*x0
    assert ik.reduce(x0.numerator()) != 0 and ik.reduce(x0.denominator()) == 0

    def field_test(value,description):
        stats['field_tests'] += 1
        if odd_delta(value):
            field_hits.append(description)

    def center_test(value,description):
        stats['center_residue_tests'] += 1
        value = field(value)
        assert ik.reduce(value.denominator()) != 0
        if ik.reduce(value.numerator()) == 0:
            center_hits.append(description)

    def k_unit_test(value):
        # Third-draw secants divide by |G-Q|^2. A pole at k=0 would
        # invalidate the later integral-radius argument, so check units.
        stats['k_unit_tests'] += 1
        value = field(value)
        assert ik.reduce(value.numerator()) != 0
        assert ik.reduce(value.denominator()) != 0

    seen = set()
    for ac,X in initial.items():
        for at,Y in initial.items():
            if X == Y:
                continue
            r1 = (X-Y)**2
            axis1 = {**initial,'E':2*X-Y}
            for bc,Z in axis1.items():
                for bt,W in axis1.items():
                    if Z == W or Z == X:
                        continue
                    r2 = (Z-W)**2
                    key = (X,r1,Z,r2)
                    if key in seen:
                        continue
                    seen.add(key)
                    stats['seed_pairs'] += 1
                    desc = {'first':['circle',ac,at],'second':['circle',bc,bt]}
                    d = Z-X
                    gx = field(r1-r2+Z*Z-X*X)/(2*d)
                    height2 = r1-(gx-X)**2
                    if height2 == 0:
                        stats['generic_tangencies'] += 1
                        continue
                    k_unit_test(height2)
                    field_test(height2,{**desc,'shape':'seed height'})
                    # Third draw GH: its new axis point has coordinate gx.
                    center_test(target_residue_center-gx,{**desc,'shape':'Line(G,H)'})
                    # Third draw Circle(G,H): its axis points are gx +/- sqrt(3 h^2).
                    center_test((target_residue_center-gx)**2-3*height2,
                                {**desc,'shape':'Circle(G,H)'})
                    field_test(3*height2,{**desc,'shape':'Circle(G,H) with axis'})
                    axis2 = {**axis1,'F':2*Z-W}
                    for q,qname in dict((value,name) for name,value in axis2.items()).items():
                        radius2 = (gx-q)**2+height2
                        k_unit_test(radius2)
                        # Circle(G,Q) gives Q and 2gx-Q on the axis.
                        center_test(target_residue_center-(2*gx-q),
                                    {**desc,'third':['circle','G',qname]})
                        # Circle(Q,G) gives q +/- sqrt(radius2).
                        center_test((target_residue_center-q)**2-radius2,
                                    {**desc,'third':['circle',qname,'G']})
                        field_test(radius2,{**desc,'shape':'axis circle radius','Q':qname})
                        for seed,S,ri in ((1,X,r1),(2,Z,r2)):
                            field_test(radius2*(4*ri-radius2),
                                       {**desc,'third':['circle','G',qname],'against':seed})
                            sep = (q-S)**2
                            if sep != 0:
                                discriminant = 4*sep*ri-(sep+ri-radius2)**2
                                field_test(discriminant,
                                           {**desc,'third':['circle',qname,'G'],'against':seed})
    # Guard against a vacuous success if a future edit drops a loop or case.
    assert stats == {'seed_pairs':192,'generic_tangencies':72,'field_tests':3600,
                     'center_residue_tests':1680,'k_unit_tests':840},stats
    assert not field_hits, 'Third-state field obstruction failed'
    assert not center_hits, 'Fourth-carrier center obstruction failed'
    return {'sage_version':SAGE_VERSION,'status':'passed','stats':stats,
            'odd_delta_field_hits':field_hits,'center_residue_hits':center_hits,
            'positive_controls':'Delta, Delta^3, 1/Delta and target y^2 odd; Delta^2 and 1/Delta^2 even',
            'scope':'finite symbolic part of the generic >=6 E proof; exhaustiveness, local-ring and carrier arguments in docs/LOWER_BOUND.md'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
