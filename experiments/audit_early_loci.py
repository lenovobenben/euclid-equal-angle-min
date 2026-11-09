"""Exact fixed-fixture audits of screened E5 carriers and two prefix identities.

The goal points are observers only. A passed first-carrier audit is not a
completed equal-angle construction and gives no new eight-move upper bound.
"""

import argparse
import hashlib
import json
from pathlib import Path

from sage.all import PolynomialRing, QQ
from sage.env import SAGE_VERSION
from exact_geometry import intersections
from replay_original import OriginalReplay, RULE_ID


def verify_prefix_identities():
    ring = PolynomialRing(QQ, names=('a', 'b', 'h'))
    a, b, h = ring.gens()
    field = ring.fraction_field()
    relation = ring.ideal(h*h - (4*a*a - b*b))
    m = field(a*b) / (a-b)
    g = (-field(b*b)/(2*a), field(b*h)/(2*a))
    q = (b-field(b**3)/(2*a*a), field(b*b*h)/(2*a*a))
    e = (-b, 0)
    square_distance = lambda p, r: (p[0]-r[0])**2 + (p[1]-r[1])**2
    u = field(b*(2*a-b))/(2*(a-b))
    v2 = field(b*b*(2*a-3*b)*(2*a-b))/(4*(a-b)**2)
    checks = {
        'G_on_left_seed': square_distance(g, (-a, 0)) - a*a,
        'G_on_B_seed': square_distance(g, (0, 0)) - b*b,
        'Omega_radius': square_distance(g, e) - field(b*b*(2*a-b))/a,
        'Q_on_B_seed': square_distance(q, (0, 0)) - b*b,
        'Q_on_Omega': square_distance(q, g) - square_distance(e, g),
        'G_Q_M_collinear': (q[0]-g[0])*(-g[1]) - (q[1]-g[1])*(m-g[0]),
        'Q_distinct_from_G': q[0]-g[0] - field(b*(2*a-b)*(a+b))/(2*a*a),
        'Q_distinct_from_E': q[0]+b - field(b*(4*a*a-b*b))/(2*a*a),
        'U_on_C_seed': (u-b)**2 + v2 - b*b,
        'U_on_reflected_circle': (u-a)**2 + v2 - (a-b)**2,
        'reflected_axis_endpoint_M': 2*u-b-m,
    }
    for name, value in checks.items():
        assert relation.reduce(field(value).numerator()) == 0, name
    return {'status': 'passed', 'identities': len(checks),
            'circle_secant_domain': 'a>b>0',
            'reflected_circles_domain': 'a>3b/2, b>0',
            'result': 'two alternative five-draw prefixes produce Circle(M,B) with M=ab/(a-b)',
            'eight_move_construction_proved': False}


def replay_carrier(program, lengths):
    replay = OriginalReplay(*lengths)
    assert replay.delta > 0
    bindings = []

    def resolve(name):
        if name in replay.bindings:
            return
        pair, root_text = name.rsplit(':', 1)
        first, second = pair.split('&')
        roots = intersections(replay.objects[first], replay.objects[second])
        point = roots[int(root_text)]
        assert point in replay.point_ids
        replay.bindings[name] = replay.point_ids[point]
        bindings.append({'alias': name, 'objects': [first, second], 'root': int(root_text),
                         'point_id': replay.point_ids[point]})

    def draw(label, action):
        kind, first, second = action
        resolve(first)
        resolve(second)
        replay.draw(label, kind, first, second)

    for index, (first, second) in enumerate(program['prefix']):
        draw(f'c{index}', ['circle', first, second])
    for index, action in enumerate(program['core'], 3):
        draw(f's{index}', action)
    draw('locus', program['locus'])
    assert len(replay.actions) == 5
    assert not any(action['duplicate_of'] for action in replay.actions)
    kind, value = replay.objects['locus']
    for point in replay.expected_targets:
        if kind == 'line':
            assert sum(x*y for x, y in zip(value, (*point, 1))) == 0
        else:
            assert (point[0]-value[0])**2 + (point[1]-value[1])**2 == value[2]
    assert not replay.target_times
    center_type = 'vertical'
    if kind == 'circle':
        m = replay.a*replay.b/(replay.a-replay.b)
        n = replay.b**2/(replay.b-replay.c)
        if value[:2] == (m, 0):
            center_type = 'M'
        elif value[:2] == (n, 0):
            center_type = 'N'
        elif value[1] == 0:
            center_type = 'other_axis'
        else:
            center_type = 'off_axis'
    return {'status': 'verified_first_carrier_only', 'lengths': list(map(str, lengths)),
            'e_moves': len(replay.actions), 'carrier_type': center_type,
            'prefix_score': {'lines': sum(action['kind'] == 'line' for action in replay.actions),
                             'circles': sum(action['kind'] == 'circle' for action in replay.actions),
                             'total': len(replay.actions)},
            'carrier_contains_both_targets': True, 'target_points_generated': False,
            'available_points': len(replay.points), 'actions': replay.actions,
            'support_bindings': bindings}


def audit(paths):
    reports = []
    failures = []
    for path in paths:
        source = json.loads(path.read_text(encoding='utf-8'))
        cases = []
        for index, program in enumerate(source['loci_observed']):
            for lengths in source['fixtures']:
                try:
                    cases.append({'program_index': index, **replay_carrier(program, lengths)})
                except Exception as error:
                    failures.append({'source': path.name, 'program_index': index,
                                     'lengths': lengths, 'error': f'{type(error).__name__}: {error}'})
        reports.append({'source': path.as_posix(), 'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                        'programs': len(source['loci_observed']), 'exact_cases': cases})
    return {'rule_id': RULE_ID, 'sage_version': SAGE_VERSION, 'arithmetic': 'SageMath QQ/AA',
            'general_prefix_identities': verify_prefix_identities(),
            'status': 'passed' if not failures else 'failed',
            'verified_fixed_cases': sum(len(report['exact_cases']) for report in reports),
            'reports': reports, 'failures': failures,
            'scope': 'exact first-carrier prefixes only; no complete eight-move construction or new lower bound'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('reports', nargs='+', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(args.reports)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key != 'reports'}, indent=2))
    raise SystemExit(bool(result['failures']))
