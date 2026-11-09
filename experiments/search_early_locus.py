"""8 E pilot with two seed circles and a first target carrier at move five.

Enumerate an arbitrary third object, a fourth object filtered by virtual
supports, and an actual fifth target carrier. Search a three-draw tail with
an arbitrary sixth draw, a witness-filtered seventh, and a final carrier.
Witnesses cover an axis circle with an already known center or radius endpoint,
or a vertical carrier. They do not cover both supports first made together.
"""

import argparse
import itertools
import json
from math import sqrt
from pathlib import Path
from time import monotonic

from search_shared_centers import (
    available, candidates, describe, extend, finisher_candidates, fresh, near, obj,
)
from search_alternative_locus import target_points, witnesses
from search_four_line_core import REGIONS


def calibration():
    ratios = [(a / b, c / b) for a, b, c in REGIONS['all']]
    points = {'A': tuple((-a, 0.) for a, c in ratios),
              'B': tuple((0., 0.) for a, c in ratios),
              'C': tuple((1., 0.) for a, c in ratios),
              'D': tuple((1. + c, 0.) for a, c in ratios)}
    objects = [('l', tuple(('line', (0., 1., 0.)) for _ in ratios))]
    stats = {'mismatched_root_counts': 0, 'virtual_mismatched_roots': 0}
    for index, (p, q) in enumerate((('A', 'B'), ('B', 'C'))):
        candidate = ('circle', p, q, tuple(obj('circle', x, y) for x, y in zip(points[p], points[q])))
        points, objects = extend(points, objects, candidate, f'c{index}', stats)
    lookup = lambda bundle: next(name for name, old in points.items()
                                 if all(near(p, q) for p, q in zip(bundle, old)))
    h = tuple(sqrt(4 * a * a - 1) for a, c in ratios)
    e = lookup(tuple((-1., 0.) for _ in ratios))
    lower = lookup(tuple((-1 / (2 * a), -height / (2 * a)) for (a, c), height in zip(ratios, h)))
    upper = lookup(tuple((-1 / (2 * a), height / (2 * a)) for (a, c), height in zip(ratios, h)))
    third = ('line', lower, e, tuple(obj('line', p, q) for p, q in zip(points[lower], points[e])))
    points, objects = extend(points, objects, third, 's3', stats)
    k = lookup(tuple((-a - .5, height / 2) for (a, c), height in zip(ratios, h)))
    virtual = witnesses(points, objects, target_points(ratios)['upper'], stats)
    fourth = next(candidate for candidate in finisher_candidates(points, virtual)
                  if candidate[0] == 'line' and {candidate[1], candidate[2]} == {k, upper})
    center = tuple((a / (a - 1), 0.) for a, c in ratios)
    assert not available(points, center)
    p4, o4 = extend(points, objects, fourth, 's4', stats)
    center_id = next(name for name, bundle in p4.items() if all(near(p, q) for p, q in zip(bundle, center)))
    fifth = next(candidate for candidate in finisher_candidates(p4, target_points(ratios))
                 if candidate[:3] == ('circle', center_id, 'B'))
    p5, _ = extend(p4, o4, fifth, 'locus', stats)
    assert not any(available(p5, target) for target in target_points(ratios).values())
    return {'known_five_draw_locus_retained': True, 'oracle_not_injected': True}


def search(region, seconds, tail_seconds, max_loci, start_prefix):
    start = monotonic()
    deadline = start + seconds
    fixtures = REGIONS[region]
    ratios = [(a / b, c / b) for a, b, c in fixtures]
    targets = target_points(ratios)
    initial = {'A': tuple((-a, 0.) for a, c in ratios),
               'B': tuple((0., 0.) for a, c in ratios),
               'C': tuple((1., 0.) for a, c in ratios),
               'D': tuple((1. + c, 0.) for a, c in ratios)}
    axis = [('l', tuple(('line', (0., 1., 0.)) for _ in ratios))]
    preferred = (('A', 'B'), ('B', 'C'))
    prefixes = [preferred] + [p for p in itertools.combinations(itertools.permutations('ABCD', 2), 2)
                              if p != preferred]
    stats = {'prefixes': 0, 'third_objects': 0, 'fourth_witness_objects': 0,
             'first_loci': 0, 'sixth_objects': 0, 'seventh_witness_objects': 0,
             'final_carriers': 0, 'mismatched_root_counts': 0, 'virtual_mismatched_roots': 0}
    loci = []
    cursor = {'prefix': start_prefix, 'third': 0, 'fourth': 0}

    def answer(status, program=None):
        result = {
            'status': status, 'region': region, 'fixtures': fixtures,
            'normalized_lengths': ratios, 'start_prefix': start_prefix,
            'repeat_cursor': dict(cursor), 'seconds_budget': seconds,
            'tail_seconds_budget_per_locus': tail_seconds, 'max_loci': max_loci,
            'elapsed': monotonic() - start, 'stats': stats, 'loci_observed': loci,
            'prefix_scan_complete': cursor['prefix'] == len(prefixes),
            'incomplete_tails': sum(item['tail_status'] == 'budget_exhausted' for item in loci),
            'initial': 'four ordered collinear points and their complete line only',
            'target': 'EA-ONE or EA-ALL in <=8 E',
            'scope': '2 input circles, arbitrary third object, witness-filtered fourth, first carrier at E5, arbitrary E6, witness-filtered E7, final carrier at E8; floating pilot only',
            'limitations': ['finite fixtures and lexicographic roots', 'root-count mismatches skipped',
                            'witnesses require an old circle center or old radius endpoint, or vertical carrier',
                            'both new supports and asymmetric carriers can be missed',
                            'per-locus tail budgets can leave tails incomplete', 'no lower bound'],
        }
        if program is not None:
            result['program'] = program
        return result

    def actual_finish(points, objects, label):
        for final in finisher_candidates(points, targets):
            if not fresh(final, objects):
                continue
            stats['final_carriers'] += 1
            completed, _ = extend(points, objects, final, label, stats)
            hit = [name for name, target in targets.items() if available(completed, target)]
            if hit:
                return final, hit
        return None

    def tail(points, objects):
        tail_deadline = min(deadline, monotonic() + tail_seconds)
        for sixth in candidates(points):
            if monotonic() > tail_deadline:
                return 'budget_exhausted', None
            if not fresh(sixth, objects):
                continue
            stats['sixth_objects'] += 1
            p6, o6 = extend(points, objects, sixth, 's6', stats)
            hit = [name for name, target in targets.items() if available(p6, target)]
            if hit:
                return 'candidate', {'tail': [describe(sixth)], 'target_sides': hit}
            finished = actual_finish(p6, o6, 's7')
            if finished:
                final, hit = finished
                return 'candidate', {'tail': [describe(sixth), describe(final)], 'target_sides': hit}
            virtual = witnesses(p6, o6, targets['upper'], stats)
            for seventh in finisher_candidates(p6, virtual):
                if monotonic() > tail_deadline:
                    return 'budget_exhausted', None
                if not fresh(seventh, o6):
                    continue
                stats['seventh_witness_objects'] += 1
                p7, o7 = extend(p6, o6, seventh, 's7', stats)
                finished = actual_finish(p7, o7, 's8')
                if finished:
                    final, hit = finished
                    return 'candidate', {'tail': [describe(sixth), describe(seventh), describe(final)], 'target_sides': hit}
        return 'screen_completed_without_hit', None

    for prefix_index, prefix in enumerate(prefixes):
        if prefix_index < start_prefix:
            continue
        cursor.update(prefix=prefix_index, third=0, fourth=0)
        if monotonic() > deadline:
            return answer('budget_exhausted')
        stats['prefixes'] += 1
        points, objects = dict(initial), list(axis)
        for index, (p, q) in enumerate(prefix):
            candidate = ('circle', p, q, tuple(obj('circle', x, y) for x, y in zip(points[p], points[q])))
            points, objects = extend(points, objects, candidate, f'c{index}', stats)
        for third_index, third in enumerate(candidates(points)):
            cursor.update(third=third_index, fourth=0)
            if monotonic() > deadline:
                return answer('budget_exhausted')
            if not fresh(third, objects):
                continue
            stats['third_objects'] += 1
            p3, o3 = extend(points, objects, third, 's3', stats)
            virtual = witnesses(p3, o3, targets['upper'], stats)
            for fourth_index, fourth in enumerate(finisher_candidates(p3, virtual)):
                cursor['fourth'] = fourth_index
                if monotonic() > deadline:
                    return answer('budget_exhausted')
                if not fresh(fourth, o3):
                    continue
                stats['fourth_witness_objects'] += 1
                p4, o4 = extend(p3, o3, fourth, 's4', stats)
                for fifth in finisher_candidates(p4, targets):
                    if not fresh(fifth, o4):
                        continue
                    p5, o5 = extend(p4, o4, fifth, 'locus', stats)
                    program = {'prefix': prefix, 'core': [describe(third), describe(fourth)],
                               'locus': describe(fifth)}
                    stats['first_loci'] += 1
                    status, result = tail(p5, o5)
                    loci.append({**program, 'tail_status': status})
                    if result:
                        return answer('candidate', {**program, **result})
                    if len(loci) >= max_loci:
                        return answer('locus_budget_exhausted')
    cursor.update(prefix=len(prefixes), third=0, fourth=0)
    status = 'prefix_scan_completed_with_incomplete_tails' if any(
        item['tail_status'] == 'budget_exhausted' for item in loci
    ) else 'screen_completed_without_hit'
    return answer(status)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--region', choices=tuple(REGIONS), default='all')
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--tail-seconds', type=float, default=8)
    parser.add_argument('--max-loci', type=int, default=12)
    parser.add_argument('--start-prefix', type=int, default=0)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    control = calibration()
    result = search(args.region, args.seconds, args.tail_seconds, args.max_loci, args.start_prefix)
    result['positive_control'] = control
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
