"""Bounded 8 E screen for two centers first appearing on the last core circle.

Two or three input circles, arbitrary objects through move four, one
witness-filtered object, then a circle producing M and N simultaneously,
followed by the two target circles.
The midpoint and radius witnesses are filters only and never enter the state.
All candidate predicates are floating, with root-count mismatches skipped.
"""

import argparse
import itertools
import json
from math import isfinite, sqrt
from pathlib import Path
from time import monotonic

from search_shared_centers import (
    EPS, available, candidates, contains, describe, extend, finisher_candidates,
    fresh, near, obj, roots,
)
from search_four_line_core import REGIONS


def midpoint_witnesses(points, objects, targets, stats):
    """Necessary new supports for a circle through two specified axis points."""
    first, second = targets.values()
    middle = tuple((p[0] + q[0]) / 2 for p, q in zip(first, second))
    virtual = [('center_vertical', tuple(('line', (1., 0., -x)) for x in middle))]
    for name, bundle in points.items():
        if all(abs(point[0] - x) < EPS * (1 + abs(x)) for point, x in zip(bundle, middle)):
            virtual.append(('radius_' + name, tuple(obj('circle', p, q) for p, q in zip(bundle, first))))
    witnesses = {}
    for virtual_name, virtual_objects in virtual:
        for old_name, old_objects in objects:
            rows = [roots(v, old) for v, old in zip(virtual_objects, old_objects)]
            if len({len(row) for row in rows}) != 1:
                stats['virtual_mismatched_roots'] += 1
                continue
            for root in range(len(rows[0])):
                bundle = tuple(row[root] for row in rows)
                if all(isfinite(x) and isfinite(y) and abs(x) < 1e8 and abs(y) < 1e8 for x, y in bundle):
                    if not available(points, bundle) and not available(witnesses, bundle):
                        witnesses[f'{virtual_name}&{old_name}:{root}'] = bundle
    return witnesses


def simultaneous_circles(points, objects, targets):
    first, second = targets.values()
    middle = tuple((p[0] + q[0]) / 2 for p, q in zip(first, second))
    for center, bundle in points.items():
        if not all(abs(point[0] - x) < EPS * (1 + abs(x)) for point, x in zip(bundle, middle)):
            continue
        for through, endpoint in points.items():
            geometry = tuple(obj('circle', p, q) for p, q in zip(bundle, endpoint))
            if any(circle is None for circle in geometry):
                continue
            if not all(contains(circle, p) and contains(circle, q)
                       for circle, p, q in zip(geometry, first, second)):
                continue
            candidate = ('circle', center, through, geometry)
            if fresh(candidate, objects):
                yield candidate


def calibration():
    """A legal diameter construction tests the new-center witness filter."""
    fixtures = REGIONS['all']
    ratios = [(a / b, c / b) for a, b, c in fixtures]
    points = {'A': tuple((-a, 0.) for a, c in ratios),
              'B': tuple((0., 0.) for a, c in ratios),
              'C': tuple((1., 0.) for a, c in ratios),
              'D': tuple((1. + c, 0.) for a, c in ratios)}
    objects = [('l', tuple(('line', (0., 1., 0.)) for _ in ratios))]
    stats = {'mismatched_root_counts': 0, 'virtual_mismatched_roots': 0}
    for label, p, q in (('c0', 'A', 'B'), ('c1', 'B', 'C')):
        candidate = ('circle', p, q, tuple(obj('circle', x, y) for x, y in zip(points[p], points[q])))
        points, objects = extend(points, objects, candidate, label, stats)
    heights = tuple(sqrt(4 * a * a - 1) / (2 * a) for a, c in ratios)
    abscissas = tuple(-1 / (2 * a) for a, c in ratios)
    targets = {'left': tuple((x - h, 0.) for x, h in zip(abscissas, heights)),
               'right': tuple((x + h, 0.) for x, h in zip(abscissas, heights))}
    lookup = lambda bundle: next(name for name, old in points.items()
                                 if all(near(p, q) for p, q in zip(old, bundle)))
    upper = lookup(tuple((x, h) for x, h in zip(abscissas, heights)))
    lower = lookup(tuple((x, -h) for x, h in zip(abscissas, heights)))
    witnesses = midpoint_witnesses(points, objects, targets, stats)
    core = list(finisher_candidates(points, witnesses))
    diameter = next(candidate for candidate in core if candidate[0] == 'line'
                    and {candidate[1], candidate[2]} == {upper, lower})
    assert not any(available(points, target) for target in targets.values())
    before = dict(points)
    p1, o1 = extend(points, objects, diameter, 'diameter', stats)
    assert points == before
    final = next(simultaneous_circles(p1, o1, targets))
    p2, _ = extend(p1, o1, final, 'final', stats)
    assert all(available(p2, target) for target in targets.values())

    # A second legal chord tests an old center with a newly made radius point.
    chord = ('line', 'D', upper, tuple(obj('line', p, q) for p, q in zip(points['D'], points[upper])))
    chord_points, chord_objects = extend(points, objects, chord, 'chord', stats)
    seed_circle = dict(objects)['c0']
    rows = [roots(line, circle) for line, circle in zip(chord[3], seed_circle)]
    new_endpoint = next(tuple(row[index] for row in rows) for index in range(2)
                        if all(not near(row[index], known) for row, known in zip(rows, points[upper])))
    radii = tuple(((p[0] - q[0])**2 + (p[1] - q[1])**2)**.5
                  for p, q in zip(points['D'], new_endpoint))
    old_center_targets = {
        'left': tuple((p[0] - radius, 0.) for p, radius in zip(points['D'], radii)),
        'right': tuple((p[0] + radius, 0.) for p, radius in zip(points['D'], radii)),
    }
    old_center_witnesses = midpoint_witnesses(points, objects, old_center_targets, stats)
    assert any(candidate[:3] == chord[:3] for candidate in finisher_candidates(points, old_center_witnesses))
    assert not any(available(chord_points, target) for target in old_center_targets.values())
    last = next(simultaneous_circles(chord_points, chord_objects, old_center_targets))
    completed, _ = extend(chord_points, chord_objects, last, 'old_center_final', stats)
    assert all(available(completed, target) for target in old_center_targets.values())
    return {'new_center_witness_retained': True, 'simultaneous_circle_retained': True,
            'old_center_new_endpoint_retained': True,
            'both_points_created_by_intersection': True, 'oracle_not_injected': True}


def search(region, seconds, start_prefix, stop_prefix=None, seed_count=3):
    start = monotonic()
    deadline = start + seconds
    fixtures = REGIONS[region]
    ratios = [(a / b, c / b) for a, b, c in fixtures]
    initial = {'A': tuple((-a, 0.) for a, c in ratios),
               'B': tuple((0., 0.) for a, c in ratios),
               'C': tuple((1., 0.) for a, c in ratios),
               'D': tuple((1. + c, 0.) for a, c in ratios)}
    axis = [('l', tuple(('line', (0., 1., 0.)) for _ in ratios))]
    targets = {'M': tuple((a / (a - 1), 0.) for a, c in ratios),
               'N': tuple((1 / (1 - c), 0.) for a, c in ratios)}
    preferred = (('A', 'B'), ('B', 'C'), ('C', 'D'))[:seed_count]
    prefixes = [preferred] + [p for p in itertools.combinations(itertools.permutations('ABCD', 2), seed_count)
                              if p != preferred]
    stats = {'prefixes': 0, 'third_objects': 0, 'fourth_objects': 0, 'fifth_witness_objects': 0,
             'states_with_midpoint_support': 0, 'final_circles': 0,
             'mismatched_root_counts': 0, 'virtual_mismatched_roots': 0}

    def answer(status, index, program=None):
        result = {
            'status': status, 'region': region, 'fixtures': fixtures,
            'normalized_lengths': ratios, 'start_prefix': start_prefix,
            'seed_count': seed_count,
            'stop_prefix': stop_prefix, 'repeat_prefix_index': index,
            'seconds_budget': seconds, 'elapsed': monotonic() - start, 'stats': stats,
            'initial': 'four ordered collinear points and their complete line only',
            'target': 'EA-ALL via canonical M,N circles, total budget <=8 E',
            'scope': f'{seed_count} input circles; arbitrary objects through move four; witness-filtered fifth; both canonical centers first appear together on a final core circle; floating heuristic only',
            'limitations': ['root-count mismatches skipped', 'lexicographic roots bound across finite fixtures',
                            'no exhaustive general 8 E exclusion', 'all hits require exact replay and coverage proof'],
        }
        if program is not None:
            result['program'] = program
        return result

    def finish_state(points, objects, prefix, core, index):
        for last in simultaneous_circles(points, objects, targets):
            stats['final_circles'] += 1
            completed, _ = extend(points, objects, last, 'last_core', stats)
            if all(available(completed, target) for target in targets.values()):
                return answer('candidate', index, {'prefix': prefix, 'core': core + [describe(last)]})
        return None

    def fourth_states(points, objects):
        if seed_count == 3:
            for fourth in candidates(points):
                if monotonic() > deadline:
                    return
                if fresh(fourth, objects):
                    stats['fourth_objects'] += 1
                    p4, o4 = extend(points, objects, fourth, 's4', stats)
                    yield p4, o4, [describe(fourth)]
            return
        for third in candidates(points):
            if monotonic() > deadline:
                return
            if not fresh(third, objects):
                continue
            stats['third_objects'] += 1
            p3, o3 = extend(points, objects, third, 's3', stats)
            if any(available(p3, target) for target in targets.values()):
                continue
            for fourth in candidates(p3):
                if monotonic() > deadline:
                    return
                if fresh(fourth, o3):
                    stats['fourth_objects'] += 1
                    p4, o4 = extend(p3, o3, fourth, 's4', stats)
                    yield p4, o4, [describe(third), describe(fourth)]

    stop = len(prefixes) if stop_prefix is None else min(stop_prefix, len(prefixes))
    for index in range(start_prefix, stop):
        prefix = prefixes[index]
        if monotonic() > deadline:
            return answer('budget_exhausted', index)
        stats['prefixes'] += 1
        points, objects = dict(initial), list(axis)
        for step, (p, q) in enumerate(prefix):
            candidate = ('circle', p, q, tuple(obj('circle', x, y) for x, y in zip(points[p], points[q])))
            points, objects = extend(points, objects, candidate, f'c{step}', stats)
        if any(available(points, target) for target in targets.values()):
            continue
        for p4, o4, core in fourth_states(points, objects):
            if any(available(p4, target) for target in targets.values()):
                continue
            hit = finish_state(p4, o4, prefix, core, index)
            if hit:
                return hit
            witnesses = midpoint_witnesses(p4, o4, targets, stats)
            if not witnesses:
                continue
            for fifth in finisher_candidates(p4, witnesses):
                if monotonic() > deadline:
                    return answer('budget_exhausted', index)
                if not fresh(fifth, o4):
                    continue
                stats['fifth_witness_objects'] += 1
                p5, o5 = extend(p4, o4, fifth, 's5', stats)
                if any(available(p5, target) for target in targets.values()):
                    continue
                middle = tuple((p[0] + q[0]) / 2 for p, q in zip(*targets.values()))
                if any(all(abs(p[0] - x) < EPS * (1 + abs(x)) for p, x in zip(bundle, middle))
                       for bundle in p5.values()):
                    stats['states_with_midpoint_support'] += 1
                hit = finish_state(p5, o5, prefix, core + [describe(fifth)], index)
                if hit:
                    return hit
        if monotonic() > deadline:
            return answer('budget_exhausted', index)
    return answer('screen_completed_without_hit', stop)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--region', choices=tuple(REGIONS), default='all')
    parser.add_argument('--seconds', type=float, default=90)
    parser.add_argument('--start-prefix', type=int, default=0)
    parser.add_argument('--stop-prefix', type=int)
    parser.add_argument('--seed-count', type=int, choices=(2, 3), default=3)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    control = calibration()
    result = search(args.region, args.seconds, args.start_prefix, args.stop_prefix, args.seed_count)
    result['positive_control'] = control
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
