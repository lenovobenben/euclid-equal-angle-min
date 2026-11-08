"""General identities for the conditional 2/7 E refinements; SageMath."""

import json
from sage.all import PolynomialRing,QQ
from sage.env import SAGE_VERSION


def main():
    ring=PolynomialRing(QQ,names=('a','b','c'))
    a,b,c=ring.gens();field=ring.fraction_field()
    k=a*c-b*b
    x=field(b*(a-b)*(b+c))/(2*k)
    r2=field(a*b*b*(b+c))/k
    pa2=r2+2*a*x+a*a
    pc2=r2-2*b*x+b*b
    pd2=r2-2*(b+c)*x+(b+c)**2
    primary=a*c-b*(a+b)
    secondary=a*c-b*(b+c)
    m=field(a*b)/(a-b)
    s=2*b-m
    outer_y2=field(b*b*(3*a+b))/(4*(a-b))
    neighbor_y2=field(b*b*(a+b))/(a-b)
    checks={
        'primary_circle_A_C':pa2-(a+b)**2+field(b*(a+b)*primary)/k,
        'primary_circle_C_D':pc2-c*c+field(c*(b+c)*primary)/k,
        'secondary_circle_B_A':r2-a*a+field(a*(a+b)*secondary)/k,
        'secondary_circle_D_B':pd2-(b+c)**2+field(b*(b+c)*secondary)/k,
        'equal_outer_target_x':x.subs(c=a)-field(b)/2,
        'equal_outer_on_first_locus':b*b/4+outer_y2-m*b,
        'mirror_center_sum':m+s-2*b,
        'mirror_circle_radius':(2*b-s)**2-m*m,
        'neighbor_on_first_locus':b*b+neighbor_y2-2*m*b,
        'neighbor_on_mirror_circle':(b-s)**2+neighbor_y2-m*m,
    }
    for name,value in checks.items():assert value==0,name
    print(json.dumps({'sage_version':SAGE_VERSION,'identities':len(checks),'status':'passed',
                      'scope':'general rational identities; positivity, branch coverage and 2E lower bound in REFINEMENTS.md'},indent=2))


if __name__=='__main__':main()
