"""Exact original-program replay, automatic intersection closure and E ledger.

Run inside SageMath: sage -python experiments/replay_original.py --output PATH
All fixtures use exact rational inputs. The target oracle is an observer only:
it never adds points to the construction state.
"""

import argparse
import json
from pathlib import Path
from sage.all import AA, QQ
from sage.env import SAGE_VERSION
from exact_geometry import circle, distance2, intersections, line


RULE_ID = "collinear-four-equal-angle-e-v1"
FIXTURES = [
    ("regular", (2, 1, 3)),
    ("regular_other", (3, 2, 4)),
    ("middle_longer_than_left", (5, 6, 9)),
    ("reflected", (9, 6, 5)),
    ("symmetric_outer", (2, 1, 2)),
    ("left_parallel", (1, 1, 2)),
    ("right_parallel", (2, 1, 1)),
    ("left_tangent", (1, 2, 7)),
    ("right_tangent", (7, 2, 1)),
    ("left_disjoint", (2, 5, 40)),
    ("right_disjoint", (40, 5, 2)),
    ("no_solution", (1, 1, 1)),
]


class ReplayFailure(Exception):
    pass


class OriginalReplay:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = map(QQ, (a, b, c))
        if min(self.a, self.b, self.c) <= 0:
            raise ValueError("positive_lengths_required")
        a, b, c = self.a, self.b, self.c
        self.delta = 3*a*c-b*(a+b+c)
        self.points = {}
        self.point_ids = {}
        self.point_records = {}
        self.bindings = {}
        self.objects = {"l": ("line", (AA(0), AA(1), AA(0)))}
        self.object_ids = {self.objects["l"]: "l"}
        self.actions = []
        self.target_times = {}
        self.dependencies = {"l": ()}
        for name, x in (("A", -a), ("B", 0), ("C", b), ("D", b+c)):
            point = (AA(x), AA(0))
            self.points[name] = point
            self.point_ids[point] = name
            self.dependencies[name] = ()
            self.point_records[name] = {"created_at": 0, "witness": {"kind": "input"}}
            self.bindings[name] = name
        self.expected_targets = ()
        if self.delta > 0:
            k = a*c-b*b
            x = AA(b*(a-b)*(b+c)/(2*k))
            y = AA(b*b*(a+b)*(b+c)*self.delta/(4*k*k)).sqrt()
            self.expected_targets = ((x, y), (x, -y))

    def add_point(self, point, objects, root_index):
        if point in self.point_ids:
            return self.point_ids[point]
        node = f"p{len(self.points)}"
        self.points[node] = point
        self.point_ids[point] = node
        self.dependencies[node] = tuple(objects)
        self.point_records[node] = {
            "created_at": len(self.actions),
            "witness": {"objects": list(objects), "lexicographic_root_index": root_index},
        }
        return node

    def draw(self, name, kind, first, second):
        if kind not in ("line", "circle"):
            raise ReplayFailure("unknown_draw_kind:"+kind)
        if first not in self.bindings or second not in self.bindings:
            raise ReplayFailure("unknown_support_point:"+name)
        support_ids = (self.bindings[first], self.bindings[second])
        p, q = (self.points[node] for node in support_ids)
        try:
            value = line(p, q) if kind == "line" else circle(p, q)
        except ValueError as exc:
            raise ReplayFailure(str(exc)+":"+name) from exc
        obj = (kind, value)
        existing = self.object_ids.get(obj)
        self.actions.append({"id": name, "kind": kind, "supports": list(support_ids),
                             "support_names": [first, second], "e_move": len(self.actions)+1,
                             "duplicate_of": existing})
        self.dependencies[name] = support_ids
        self.objects[name] = obj
        if existing is None:
            old_objects = list(self.object_ids.items())
            self.object_ids[obj] = name
            for old_obj, old_name in old_objects:
                for root_index, point in enumerate(intersections(obj, old_obj)):
                    self.add_point(point, (name, old_name), root_index)
        # Membership is checked exactly against existing closure; no target injection.
        for index, point in enumerate(self.expected_targets):
            if point in self.point_ids and str(index) not in self.target_times:
                assert self.is_target(point)
                self.target_times[str(index)] = len(self.actions)

    def bind(self, name, first, second, *, side=None, other_than=None):
        roots = intersections(self.objects[first], self.objects[second])
        if side is not None:
            roots = tuple(point for point in roots if point[1]*side > 0)
        if other_than is not None:
            known = self.points[self.bindings[other_than]]
            roots = tuple(point for point in roots if point != known)
        if len(roots) != 1:
            raise ReplayFailure(f"intersection_binding:{name}:candidates={len(roots)}")
        point = roots[0]
        if point not in self.point_ids:
            raise AssertionError("binding_without_automatic_closure")
        self.bindings[name] = self.point_ids[point]

    def is_target(self, point):
        if point[1] == 0:
            return False
        a, b, c = self.a, self.b, self.c
        A, B, C, D = (self.points[name] for name in ("A", "B", "C", "D"))
        return (b*b*distance2(point, A) == a*a*distance2(point, C)
                and c*c*distance2(point, B) == b*b*distance2(point, D))

    def execute(self):
        if self.delta <= 0:
            return "no_solution_input"
        self.draw("GammaA", "circle", "A", "B")
        self.draw("GammaD", "circle", "D", "C")
        self.draw("GammaB", "circle", "B", "C")
        self.draw("GammaC", "circle", "C", "B")
        self.bind("E", "GammaB", "l", other_than="C")
        self.bind("F", "GammaC", "l", other_than="B")
        for name, first, second, side in (
                ("G", "GammaA", "GammaB", 1), ("H", "GammaA", "GammaB", -1),
                ("I", "GammaC", "GammaD", 1), ("J", "GammaC", "GammaD", -1)):
            self.bind(name, first, second, side=side)
        self.draw("HE", "line", "H", "E")
        self.bind("K", "HE", "GammaA", other_than="H")
        self.draw("FJ", "line", "F", "J")
        self.bind("L", "FJ", "GammaD", other_than="J")
        self.draw("KG", "line", "K", "G")
        self.bind("M", "KG", "l")
        self.draw("LI", "line", "L", "I")
        self.bind("N", "LI", "l")
        self.draw("GammaM", "circle", "M", "B")
        self.draw("GammaN", "circle", "N", "C")
        self.bind("P", "GammaM", "GammaN", side=1)
        self.bind("P_prime", "GammaM", "GammaN", side=-1)
        assert self.points[self.bindings["P"]] == self.expected_targets[0]
        assert self.points[self.bindings["P_prime"]] == self.expected_targets[1]
        assert len(self.target_times) == 2
        return "verified"

    def paid_ancestors(self, root):
        visited = set()
        pending = [root]
        while pending:
            node = pending.pop()
            if node not in visited:
                visited.add(node)
                pending.extend(self.dependencies[node])
        paid = {action["id"] for action in self.actions}
        return sorted(visited & paid)

    def report(self, name, status, failure=None, include_trace=True):
        a, b, c = self.a, self.b, self.c
        legal_domain = self.delta > 0 and b < 2*a and b < 2*c and a != b and b != c
        counts = {kind: sum(action["kind"] == kind for action in self.actions)
                  for kind in ("line", "circle")}
        score = {"lines": counts["line"], "circles": counts["circle"], "total": len(self.actions)}
        ancestors = {label: self.paid_ancestors(self.point_ids[point])
                     for label, point in zip(("upper", "lower"), self.expected_targets)
                     if point in self.point_ids}
        report = {
            "fixture": name, "lengths": [str(v) for v in (a, b, c)],
            "delta": str(self.delta), "in_original_domain": bool(legal_domain),
            "status": status, "failure": failure,
            "score": score if status == "verified" else None,
            "diagnostic_executed_draws": score,
            "distinct_objects": len(self.object_ids),
            "duplicate_draws": sum(action["duplicate_of"] is not None for action in self.actions),
            "available_points": len(self.points),
            "first_target_e_move": min(self.target_times.values(), default=None),
            "all_targets_e_move": max(self.target_times.values()) if len(self.target_times) == 2 else None,
            "target_paid_ancestors": ancestors,
        }
        if include_trace:
            report["trace"] = {
                "actions": self.actions,
                "bindings": self.bindings,
                "points": {node: {**self.point_records[node],
                                   "display_coordinates_only": [str(v) for v in point]}
                           for node, point in self.points.items()},
                "coordinate_note": "AA decimal strings are display only; witnesses and exact replay determine points.",
            }
        return report


def replay_fixture(name, values, include_trace=True):
    replay = OriginalReplay(*values)
    failure = None
    try:
        status = replay.execute()
    except ReplayFailure as exc:
        status, failure = "construction_not_applicable", str(exc)
    report = replay.report(name, status, failure, include_trace)
    assert (status == "verified") == report["in_original_domain"]
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    reports = []
    for name, values in FIXTURES:
        report = replay_fixture(name, values)
        reports.append(report)
        print(json.dumps({k: v for k, v in report.items() if k != "trace"}, ensure_ascii=False), flush=True)
    result = {"rule_id": RULE_ID, "sage_version": SAGE_VERSION,
              "arithmetic": "SageMath AA exact real algebraic numbers",
              "coverage": "restricted: delta>0, b<2a, b<2c, a!=b, b!=c",
              "global_gen_upper": None, "global_rob_upper": None,
              "restricted_verified_upper": 10,
              "fixtures": reports}
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
