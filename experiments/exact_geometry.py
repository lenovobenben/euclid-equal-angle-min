"""SageMath AA geometry with exact predicates and finite intersections.

Coordinates are real algebraic numbers. No floating point is used in decisions.
Line keys are normalized; coincident objects have no invented intersections.
"""

from sage.all import AA


def sub(p, q):
    return (p[0]-q[0], p[1]-q[1])


def dot(p, q):
    return p[0]*q[0]+p[1]*q[1]


def distance2(p, q):
    return dot(sub(p, q), sub(p, q))


def line(p, q):
    if p == q:
        raise ValueError("line_requires_distinct_points")
    coeffs = (p[1]-q[1], q[0]-p[0], p[0]*q[1]-q[0]*p[1])
    pivot = next(v for v in coeffs if v != 0)
    return tuple(v/pivot for v in coeffs)


def circle(p, q):
    radius2 = distance2(p, q)
    if radius2 == 0:
        raise ValueError("circle_requires_positive_radius")
    return (p[0], p[1], radius2)


def line_line(first, second):
    a, b, c = first
    d, e, f = second
    det = a*e-b*d
    if det == 0:
        return ()
    return (((b*f-c*e)/det, (c*d-a*f)/det),)


def line_circle(coeffs, circ):
    a, b, c = coeffs
    cx, cy, r2 = circ
    norm2 = a*a+b*b
    offset = a*cx+b*cy+c
    foot = (cx-a*offset/norm2, cy-b*offset/norm2)
    t2 = (r2-offset*offset/norm2)/norm2
    if t2 < 0:
        return ()
    if t2 == 0:
        return (foot,)
    t = AA(t2).sqrt()
    return tuple(sorted(((foot[0]-b*t, foot[1]+a*t),
                         (foot[0]+b*t, foot[1]-a*t))))


def circle_circle(first, second):
    x1, y1, r1 = first
    x2, y2, r2 = second
    if x1 == x2 and y1 == y2:
        return ()
    axis = (2*(x2-x1), 2*(y2-y1),
            x1*x1+y1*y1-r1-x2*x2-y2*y2+r2)
    return line_circle(axis, first)


def intersections(first, second):
    kind1, value1 = first
    kind2, value2 = second
    if kind1 == kind2 == "line":
        return line_line(value1, value2)
    if kind1 == kind2 == "circle":
        return circle_circle(value1, value2)
    if kind1 == "line":
        return line_circle(value1, value2)
    return line_circle(value2, value1)
