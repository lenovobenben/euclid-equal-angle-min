"""Inversion and projectivity identities; structural results, not E programs."""

import argparse
import json
from pathlib import Path
from sage.all import PolynomialRing, QQ, matrix
from sage.env import SAGE_VERSION


def verify():
    ring = PolynomialRing(QQ,names=('a','b','c','z','d','r','t','u','v'))
    a,b,c,z,d,r,t,u,v = ring.gens()
    field = ring.fraction_field()
    k = a*c-b*b
    delta = 3*a*c-b*(a+b+c)
    m = field(a*b)/(a-b)
    n = field(b*b)/(b-c)
    s = field(a*(b+c))/(a-c)
    x = field(b*(a-b)*(b+c))/(2*k)
    rho = field(a*b*b*(b+c))/k
    y2 = field(b*b*(a+b)*(b+c)*delta)/(4*k*k)
    jm = lambda value: m+m*m/(value-m)
    jn = lambda value: n+(n-b)**2/(value-n)
    js = lambda value: s+s*(s-b)/(value-s)
    f = lambda value: field(b*b*(b+c)*(value+a))/(a*b*(b+c)-k*value)
    checks = {
        'M_inversion_A_to_C':jm(-a)-b,
        'M_inversion_B_fixed':jm(0),
        'M_inversion_C_to_A':jm(b)+a,
        'S_inversion_A_to_D':js(-a)-(b+c),
        'S_inversion_B_to_C':js(0)-b,
        'S_inversion_C_to_B':js(b),
        'S_inversion_D_to_A':js(b+c)+a,
        'composition_is_projectivity':js(jm(z))-f(z),
        'old_inversions_are_projectivity_squared':jn(jm(z))-f(f(z)),
        'projectivity_A_to_B':f(-a),
        'projectivity_B_to_C':f(0)-b,
        'projectivity_C_to_D':f(b)-(b+c),
        'target_norm':x*x+y2-rho,
        'third_locus':(a-c)*rho-2*a*(b+c)*x+a*b*(b+c),
        'third_locus_radius':s*s-s*(s-b)-b*s,
        'fixed_quadratic':(k*z*z-b*(a-b)*(b+c)*z+a*b*b*(b+c))
                          -(z-f(z))*(k*z-a*b*(b+c)),
    }
    disc = (b*(a-b)*(b+c))**2-4*k*a*b*b*(b+c)
    checks['fixed_quadratic_discriminant'] = disc+b*b*(a+b)*(b+c)*delta
    transform = matrix(field,[[b*b*(b+c),a*b*b*(b+c)],[-k,a*b*(b+c)]])
    checks['projectivity_determinant'] = transform.det()-a*b*b*c*(a+b)*(b+c)
    checks['projectivity_trace_ratio'] = transform.trace()**2/(4*transform.det())-field((a+b)*(b+c))/(4*a*c)

    # For a circle about d, mirrored G,H=(u,+/-v) on it, secants tH and KG
    # meet the input axis at the circle inverse of t. Only collinearity and
    # membership are certified here; branch distinctness is separate.
    inversion = d+field(r*r)/(t-d)
    G = (u,v)
    H = (u,-v)
    direction = (H[0]-t,H[1])
    # The other line-circle root has product ((t-d)^2-r^2)/|H-t|^2.
    parameter = field((t-d)**2-r*r)/(direction[0]**2+direction[1]**2)
    K = (t+parameter*direction[0],parameter*direction[1])
    cross = (K[0]-G[0])*(-G[1])-(K[1]-G[1])*(inversion-G[0])
    ideal = ring.ideal((u-d)**2+v*v-r*r)
    assert ideal.reduce(field(cross).numerator()) == 0
    for name,expression in checks.items():
        assert field(expression) == 0,name
    return {'sage_version':SAGE_VERSION,'status':'passed','identities':len(checks)+1,
            'scope':'rational identities and mirrored-secant inversion; special denominators require branches; no new E upper bound'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
