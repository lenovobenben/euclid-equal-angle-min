"""Exact general-parameter identities; run with SageMath's Python.

PowerShell (from the repository root, with the existing `sage` container):
  Get-Content -Raw experiments/verify_existence.sage.py | docker exec -i sage sage -python

The geometric necessity, sufficiency, positivity and coverage arguments are in
docs/EXISTENCE.md. Symbolic identities do not replace those arguments.
"""

import json
from sage.all import PolynomialRing, QQ
from sage.env import SAGE_VERSION


def main():
    ring = PolynomialRing(QQ, names=("a", "b", "c"))
    a, b, c = ring.gens()
    field = ring.fraction_field()
    delta = 3*a*c - b*(a+b+c)
    k = a*c - b*b
    x = field(b*(a-b)*(b+c)) / (2*k)
    y2 = field(b*b*(a+b)*(b+c)*delta) / (4*k*k)
    r2 = x*x + y2

    identities = {
        "radius_squared": r2 - field(a*b*b*(b+c))/k,
        "first_bisector_locus": (b-a)*r2 + 2*a*b*x,
        "second_bisector_locus": (c-b)*r2 + 2*b*b*x - b*b*(b+c),
        "first_distance_ratio": b*b*((x+a)**2+y2) - a*a*((x-b)**2+y2),
        "second_distance_ratio": c*c*(x*x+y2) - b*b*((x-b-c)**2+y2),
        "linear_system_determinant": (b-a)*2*b*b - 2*a*b*(c-b) + 2*b*k,
        "symmetric_height": y2.subs(c=a) - field(b*b*(3*a+b))/(4*(a-b)),
        "delta_decomposition": delta - (3*k-b*(a+c-2*b)),
    }
    for name, expression in identities.items():
        assert expression == 0, name

    checked = valid = boundary = singular = 0
    for av in range(1, 16):
        for bv in range(1, 16):
            for cv in range(1, 16):
                checked += 1
                values = {a: QQ(av), b: QQ(bv), c: QQ(cv)}
                dv = delta.subs(values)
                kv = k.subs(values)
                if kv == 0:
                    singular += 1
                    assert dv <= 0
                    continue
                xv = x.subs(values)
                yv2 = y2.subs(values)
                assert (yv2 > 0) == (dv > 0)
                if dv == 0:
                    boundary += 1
                    assert yv2 == 0
                    assert xv < -av or xv > bv+cv
                if dv <= 0:
                    continue
                valid += 1
                assert kv > 0
                assert bv*bv*((xv+av)**2+yv2) == av*av*((xv-bv)**2+yv2)
                assert cv*cv*(xv*xv+yv2) == bv*bv*((xv-bv-cv)**2+yv2)

    assert x.subs({a: 2, b: 1, c: 3}) == QQ(2)/5
    assert y2.subs({a: 2, b: 1, c: 3}) == QQ(36)/25
    assert x.subs({a: 2, b: 3, c: 5}) == -12
    print(json.dumps({
        "sage_version": SAGE_VERSION,
        "symbolic_identities": len(identities),
        "integer_fixtures": checked,
        "valid_fixtures": valid,
        "nonsingular_boundary_fixtures": boundary,
        "singular_fixtures": singular,
        "status": "passed",
        "scope": "general rational-function identities plus finite exact checks; see proof",
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
