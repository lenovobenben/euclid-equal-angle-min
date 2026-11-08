"""General-parameter proof checks for the original construction module.

Run with SageMath Python. The positivity and exceptional-case arguments are in
docs/BASELINE.md; identities are reduced modulo h^2=4a^2-b^2.
"""

import json
from sage.all import PolynomialRing, QQ
from sage.env import SAGE_VERSION


def main():
    ring = PolynomialRing(QQ, names=("a", "b", "h"))
    a, b, h = ring.gens()
    field = ring.fraction_field()
    ideal = ring.ideal(h*h-4*a*a+b*b)
    A = (-a, 0)
    E = (-b, 0)
    G = (-field(b*b)/(2*a), field(b*h)/(2*a))
    H = (G[0], -G[1])
    K = (-a-field(b)/2, field(h)/2)
    m = field(a*b)/(a-b)
    cross = lambda u, v: u[0]*v[1]-u[1]*v[0]
    sub = lambda u, v: (u[0]-v[0], u[1]-v[1])
    norm2 = lambda u: u[0]*u[0]+u[1]*u[1]
    checks = {
        "G_on_GammaA": norm2(sub(G, A))-a*a,
        "G_on_GammaB": norm2(G)-b*b,
        "H_on_GammaA": norm2(sub(H, A))-a*a,
        "K_on_GammaA": norm2(sub(K, A))-a*a,
        "H_E_K_collinear": cross(sub(H, E), sub(K, E)),
        "K_G_M_collinear": cross(sub(K, (m, 0)), sub(G, (m, 0))),
        "KG_nonzero_x_difference": K[0]-G[0]+field((2*a-b)*(a+b))/(2*a),
        "KG_y_difference": K[1]-G[1]-field((a-b)*h)/(2*a),
        "K_H_y_difference": K[1]-H[1]-field((a+b)*h)/(2*a),
        "left_circle_is_locus": (b-a)*(-2*m)-2*a*b,
    }
    for name, expression in checks.items():
        assert ideal.reduce(field(expression).numerator()) == 0, name
    ring3 = PolynomialRing(QQ, names=("a", "b", "c"))
    a, b, c = ring3.gens()
    f3 = ring3.fraction_field()
    m = f3(a*b)/(a-b)
    n = f3(b*b)/(b-c)
    assert m-n == -f3(b*(a*c-b*b))/((a-b)*(b-c))
    # Reflect the left module: local origin C, local positive axis towards B.
    assert b-f3(c*b)/(c-b) == n
    print(json.dumps({"sage_version": SAGE_VERSION, "status": "passed",
                      "module_identities": len(checks), "pair_identities": 2,
                      "scope": "general rational identities modulo h^2=4a^2-b^2"}, indent=2))


if __name__ == "__main__":
    main()
