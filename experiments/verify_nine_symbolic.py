"""General identities for the shared-circle 9 E construction; SageMath."""

import json
from sage.all import PolynomialRing,QQ
from sage.env import SAGE_VERSION


def main():
    ring=PolynomialRing(QQ,names=('a','b','c','h'))
    a,b,c,h=ring.gens()
    field=ring.fraction_field()
    ideal=ring.ideal(h*h-4*a*a+b*b)
    G=(-field(b*b)/(2*a),field(b*h)/(2*a))
    K=(-a-field(b)/2,field(h)/2)
    T=(b-field(b*b*b)/(2*a*a),field(b*b*h)/(2*a*a))
    R=(b-field(b*c)/(2*a),field(c*h)/(2*a))
    M=(field(a*b)/(a-b),0)
    N=(field(b*b)/(b-c),0)
    C=(b,0)
    sub=lambda u,v:(u[0]-v[0],u[1]-v[1])
    cross=lambda u,v:u[0]*v[1]-u[1]*v[0]
    norm2=lambda u:u[0]*u[0]+u[1]*u[1]
    checks={
        'T_on_GammaB':norm2(T)-b*b,
        'T_on_KG':cross(sub(T,G),sub(K,G)),
        'T_distinct_from_G_x':T[0]-G[0]-field(b*(2*a-b)*(a+b))/(2*a*a),
        'T_C_x_scaled_G':T[0]-b-field(b)/a*G[0],
        'T_C_y_scaled_G':T[1]-field(b)/a*G[1],
        'R_on_GammaR':norm2(sub(R,C))-c*c,
        'R_on_CT':cross(sub(R,C),sub(T,C)),
        'R_C_x_scaled_G':R[0]-b-field(c)/b*G[0],
        'R_C_y_scaled_G':R[1]-field(c)/b*G[1],
        'N_on_GR':cross(sub(N,G),sub(R,G)),
        'GR_y_difference':R[1]-G[1]-field((c-b)*h)/(2*a),
        'M_on_KG':cross(sub(M,G),sub(K,G)),
    }
    # Equal-neighbor branch: x=b, r^2=2mb; y^2=b^2(a+b)/(a-b)>0.
    equal_y2=field(b*b*(a+b))/(a-b)
    checks['equal_branch_on_GammaM']=b*b+equal_y2-2*M[0]*b
    checks['equal_branch_distance_bisector']=(b*b+equal_y2)-((-b)**2+equal_y2)
    for name,expression in checks.items():
        assert ideal.reduce(field(expression).numerator())==0,name
    print(json.dumps({'sage_version':SAGE_VERSION,'status':'passed',
                      'identities':len(checks),'scope':'general identities modulo h^2=4a^2-b^2; see NINE.md for branch and positivity proof'},indent=2))


if __name__=='__main__':
    main()
