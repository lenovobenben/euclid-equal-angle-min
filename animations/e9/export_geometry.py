"""Export display coordinates from the exact NineReplay construction.

Run with SageMath. All predicates and dependencies come from the replay.
Only the exported Manim coordinates are rounded to binary floating point.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "experiments"))

from sage.all import QQ
from sage.env import SAGE_VERSION
from replay_nine import NineReplay, RULE_ID


OUTPUT = Path(__file__).with_name("geometry.json")


def build_export() -> dict:
    replay = NineReplay(3, 1, QQ(5) / 2)
    assert replay.execute() == "verified"
    assert replay.branch == "shared_circle_9"
    assert replay.target_times == {"0": 9, "1": 9}
    points = {}
    for name, node in replay.bindings.items():
        record = replay.point_records[node]
        points[name] = {
            "node": node,
            "at": [float(value) for value in replay.points[node]],
            "available_after": record["created_at"],
            "witness": record["witness"],
        }
    events = []
    for action in replay.actions:
        kind, value = replay.objects[action["id"]]
        if kind == "line":
            geometry = dict(zip(("a", "b", "c"), map(float, value)))
        else:
            geometry = {
                "center": [float(value[0]), float(value[1])],
                "radius": float(value[2].sqrt()),
            }
        assert action["duplicate_of"] is None
        assert all(points[name]["available_after"] < action["e_move"]
                   for name in action["support_names"])
        events.append({
            "e_move": action["e_move"], "id": action["id"],
            "op": kind, "references": action["support_names"],
            "geometry": geometry,
        })
    assert sum(event["op"] == "line" for event in events) == 4
    assert sum(event["op"] == "circle" for event in events) == 5
    payload = {
        "initial": {"points": ["A", "B", "C", "D"],
                    "line": {"a": 0.0, "b": 1.0, "c": 0.0}},
        "points": points, "events": events, "targets": ["P", "P_prime"],
    }
    digest = hashlib.sha256(json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    return {
        "schema": "euclid-equal-angle-min-manim-e9/v1",
        "source": {
            "replay": "experiments/replay_nine.py", "class": "NineReplay",
            "rule_id": RULE_ID, "sage_version": SAGE_VERSION,
            "arithmetic": "SageMath QQ/AA", "lengths_exact": ["3", "1", "5/2"],
            "reversed_input_labels": bool(replay.reversed),
            "trace_sha256": digest,
        },
        "verified_result": {
            "fixture_status": "verified", "branch": replay.branch,
            "line_draws": 4, "circle_draws": 5, "total_e": 9,
            "first_target_e": 9, "all_targets_e": 9,
            "program_coverage_reference": "docs/NINE.md",
            "minimality_proved": False,
        },
        **payload,
    }


if __name__ == "__main__":
    data = build_export()
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data["verified_result"], ensure_ascii=False))
