"""NineReplay's two equal-angle points, in the Euclid-CCC-Min visual style.

Reads the exact replay's geometry.json. Geometry here serves presentation only.
Palette, fine strokes, support rings and integer HUD follow the Apache-2.0
animations/e49 and animations/e18 scenes in lenovobenben/euclid-ccc-min.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from manim import (
    Arc, Circle, Create, Dot, FadeIn, FadeOut, Line, MovingCameraScene,
    Rectangle, Text, UpdateFromAlphaFunc, VGroup, Write, config, linear,
    DOWN, LEFT, RIGHT, UP,
)

BACKGROUND = "#07101F"
FOREGROUND = "#E8F0F7"
MUTED = "#8397A8"
CIRCLE_BLUE = "#56B4D3"
LINE_BLUE = "#8AC6D9"
GOLD = "#FFC857"
TARGET = "#5DE2A5"
ALERT = "#FF7A90"
INPUT = "#F45BFF"
FONT = "Noto Sans CJK SC"
BASE_WIDTH = 12.8
OVERVIEW = ((-1.5, 0.4), BASE_WIDTH)
DETAIL = ((-0.3, 1.1), 8.0)
FINAL = ((0.15, 0.0), 8.5)
BOUNDS = (-15.0, 13.0, -10.0, 10.0)
DATA_PATH = Path(__file__).with_name("geometry.json")


def position(point):
    return np.array([point[0], point[1], 0.0])


def clip_line(geometry, bounds):
    a, b, c = (geometry[key] for key in ("a", "b", "c"))
    xmin, xmax, ymin, ymax = bounds
    candidates = []
    if abs(b) > 1e-12:
        for x in (xmin, xmax):
            y = (-a * x - c) / b
            if ymin - 1e-9 <= y <= ymax + 1e-9:
                candidates.append((x, y))
    if abs(a) > 1e-12:
        for y in (ymin, ymax):
            x = (-b * y - c) / a
            if xmin - 1e-9 <= x <= xmax + 1e-9:
                candidates.append((x, y))
    if len(candidates) < 2:
        raise ValueError("Line misses viewport")
    first, second = max(
        ((p, q) for p in candidates for q in candidates),
        key=lambda pair: math.dist(*pair),
    )
    if math.dist(first, second) < 1e-9:
        raise ValueError("Line only touches viewport")
    return position(first), position(second)


def load_geometry(path=DATA_PATH):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["schema"] != "euclid-equal-angle-min-manim-e9/v1":
        raise ValueError("Unsupported geometry schema")
    payload = {key: data[key] for key in ("initial", "points", "events", "targets")}
    digest = hashlib.sha256(json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()).hexdigest()
    if digest != data["source"]["trace_sha256"]:
        raise ValueError("Geometry digest mismatch. Re-export the exact replay.")
    events = data["events"]
    if len(events) != 9 or sum(e["op"] == "line" for e in events) != 4:
        raise ValueError("Expected four lines and five circles")
    for step, event in enumerate(events, 1):
        if event["e_move"] != step or event["op"] not in ("line", "circle"):
            raise ValueError("Invalid E ledger")
        for name in event["references"]:
            if data["points"][name]["available_after"] >= step:
                raise ValueError(f"E{step} uses unavailable point {name}")
    return data


class E9EqualAngle(MovingCameraScene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        self.data = load_geometry()
        self.labels = {}
        self.strokes = []
        self.anchors = []
        self.hud = {}
        self.auxiliaries = VGroup()
        self.loci = VGroup()
        self.viewport_key = None
        self.intro()
        self.setup_geometry()
        self.draw_construction()
        self.finish()

    def text(self, content, **kwargs):
        return Text(content, font=FONT, color=kwargs.pop("color", FOREGROUND), **kwargs)

    def intro(self):
        title = self.text("共线四点，两个等视角点", font_size=52, weight="MEDIUM").move_to(UP * 2.3)
        equation = self.text("∠APB = ∠BPC = ∠CPD", font_size=37, color=TARGET).move_to(UP * 1.15)
        rules = self.text(
            "四个有序共线点及其完整直线免费\n"
            "每画一条直线或一个圆计 1 E，已有对象的交点免费\n"
            "不任选辅助点，不搬运圆规开度",
            font_size=24, line_spacing=1.2,
        ).move_to(DOWN * 0.25)
        count = self.text("4 条直线 + 5 个圆 = 9 E", font_size=33, color=GOLD).move_to(DOWN * 1.7)
        scope = self.text("全有解域上界 9 E · 本片演示共享圆分支", font_size=21, color=MUTED).move_to(DOWN * 2.5)
        page = VGroup(title, equation, rules, count, scope)
        self.play(Write(title), FadeIn(equation), run_time=1)
        self.play(FadeIn(rules), run_time=0.6)
        self.play(FadeIn(count), FadeIn(scope), run_time=0.5)
        self.wait(2.8)
        self.play(FadeOut(page), run_time=0.5)

    def size(self, value):
        return value * self.camera.frame.width / BASE_WIDTH

    def point(self, name):
        return position(self.data["points"][name]["at"])

    def keep_stroke(self, drawable, width):
        drawable.screen_width = width
        self.strokes.append(drawable)

    def keep_size(self, group, anchor):
        self.anchors.append([group, anchor.copy(), self.camera.frame.width / BASE_WIDTH])

    def update_mobjects(self, dt):
        super().update_mobjects(dt)
        if getattr(self, "geometry_ready", False):
            self.sync_viewport()

    def sync_viewport(self):
        frame = self.camera.frame
        key = (frame.width, *frame.get_center())
        if key == self.viewport_key:
            return
        self.viewport_key = key
        scale = frame.width / BASE_WIDTH
        for drawable in self.strokes:
            drawable.set_stroke(width=drawable.screen_width * scale)
        for record in self.anchors:
            group, anchor, previous = record
            group.scale(scale / previous, about_point=anchor)
            record[2] = scale
        for slot, (group, original_width) in self.hud.items():
            group.set(width=original_width * scale)
            horizontal = LEFT if slot == "counter" else RIGHT
            vertical = UP if slot == "footer" else DOWN
            corner = (RIGHT if slot == "counter" else LEFT) + (DOWN if slot == "footer" else UP)
            group.move_to(
                frame.get_corner(corner)
                + horizontal * (group.width / 2 + 0.28 * scale)
                + vertical * (group.height / 2 + 0.22 * scale)
            )

    def set_hud(self, slot, content, font_size=23, color=FOREGROUND):
        old = self.hud.get(slot)
        if old:
            self.remove(old[0])
        label = self.text(content, font_size=font_size, color=color)
        backdrop = Rectangle(
            width=label.width + 0.28, height=label.height + 0.2,
            stroke_width=0, fill_color=BACKGROUND, fill_opacity=0.92,
        ).move_to(label)
        group = VGroup(backdrop, label).set_z_index(25)
        self.hud[slot] = (group, group.width)
        self.viewport_key = None
        self.sync_viewport()
        self.add(group)

    def move_camera(self, center, width):
        frame = self.camera.frame
        start = frame.get_center().copy()
        end = position(center)
        old_width = frame.width
        zoom = math.log(width / old_width)

        def interpolate(camera_frame, alpha):
            camera_frame.set(width=old_width * math.exp(zoom * alpha))
            camera_frame.move_to((1 - alpha) * start + alpha * end)

        self.play(UpdateFromAlphaFunc(frame, interpolate), run_time=1.2)
        self.sync_viewport()
        self.wait(0.2)

    def label_point(self, name, direction=UP, color=FOREGROUND):
        if name in self.labels:
            return
        at = self.point(name)
        dot = Dot(at, radius=self.size(0.016), color=color)
        label = self.text("P′" if name == "P_prime" else name, font_size=18, color=color)
        label.scale(self.camera.frame.width / BASE_WIDTH)
        label.next_to(dot, direction, buff=self.size(0.09))
        group = VGroup(dot, label).set_z_index(12)
        self.labels[name] = group
        self.keep_size(group, at)
        self.play(FadeIn(group), run_time=0.2)

    def hide_labels(self, names):
        groups = [self.labels.pop(name) for name in names if name in self.labels]
        if groups:
            self.play(FadeOut(VGroup(*groups)), run_time=0.25)

    def setup_geometry(self):
        self.camera.frame.move_to(position(OVERVIEW[0])).set(width=OVERVIEW[1])
        self.geometry_ready = True
        self.set_hud("counter", "00 / 09", font_size=42, color=GOLD)
        self.set_hud("caption", "免费输入 · A、B、C、D 与直线 l")
        self.set_hud("footer", "AB = 3    BC = 1    CD = 5/2", font_size=21, color=MUTED)
        start, end = clip_line(self.data["initial"]["line"], BOUNDS)
        self.baseline = Line(start, end, color=INPUT, stroke_width=0.95).set_z_index(3)
        self.keep_stroke(self.baseline, 0.95)
        self.play(FadeIn(self.baseline), run_time=0.6)
        for name in self.data["initial"]["points"]:
            self.label_point(name, DOWN, INPUT)
        self.wait(1.3)

    def reference_marker(self, name, color):
        at = self.point(name)
        ring = Circle(radius=self.size(0.046), color=color, stroke_width=self.size(0.65)).move_to(at)
        dot = Dot(at, radius=self.size(0.010), color=color)
        return VGroup(ring, dot).set_z_index(16)

    def show_references(self, event):
        first, second = event["references"]
        for name in (first, second):
            record = self.data["points"][name]
            assert record["available_after"] < event["e_move"]
            delta = self.point(name) - self.camera.frame.get_center()
            if abs(delta[0]) > self.camera.frame.width * 0.46 or abs(delta[1]) > self.camera.frame.height * 0.40:
                raise ValueError(f"E{event['e_move']} support {name} outside safe viewport")
        center_color = ALERT if event["op"] == "circle" else GOLD
        overlay = VGroup(self.reference_marker(first, center_color), self.reference_marker(second, GOLD))
        if event["op"] == "circle":
            overlay.add(Line(self.point(first), self.point(second), color=ALERT, stroke_width=self.size(0.6)))
        self.play(FadeIn(overlay), run_time=0.25)
        self.wait(0.3)
        return overlay

    def drawable(self, event):
        geometry = event["geometry"]
        if event["op"] == "circle":
            result = Circle(radius=geometry["radius"], color=GOLD, stroke_width=self.size(0.85))
            result.move_to(position(geometry["center"]))
        else:
            result = Line(*clip_line(geometry, BOUNDS), color=GOLD, stroke_width=self.size(0.85))
        self.keep_stroke(result, 0.85)
        return result

    def draw_construction(self):
        captions = {
            1: "1–3 E · 三个辅助圆", 4: "4–5 E · 定位第一个圆心 M",
            6: "6–7 E · 复用交点 T，定位圆心 N", 8: "8–9 E · 两条等角轨迹相交",
        }
        definitions = {
            1: "以 A 为圆心，经过 B", 2: "以 B 为圆心，经过 C",
            3: "以 C 为圆心，经过 D", 4: "连接 H、E，取得 K",
            5: "连接 K、G，取得 M 和共享交点 T", 6: "连接 C、T，取得上侧交点 R",
            7: "连接 G、R，与底线相交于 N", 8: "以 M 为圆心，经过 B",
            9: "以 N 为圆心，经过 C",
        }
        reveals = {
            2: [("E", DOWN + LEFT), ("G", UP + RIGHT), ("H", DOWN)],
            4: [("K", UP + LEFT)], 5: [("M", DOWN), ("T", UP + RIGHT)],
            6: [("R", UP + RIGHT)], 7: [("N", DOWN + LEFT)],
            9: [("P", UP + RIGHT), ("P_prime", DOWN + RIGHT)],
        }
        for event in self.data["events"]:
            step = event["e_move"]
            if step == 6:
                self.hide_labels(["E", "H", "K"])
                self.move_camera(*DETAIL)
            if step == 8:
                self.move_camera(*FINAL)
                self.hide_labels(["G", "T", "R"])
            if step in captions:
                self.set_hud("caption", captions[step])
            self.set_hud("footer", definitions[step], font_size=22, color=MUTED)
            references = self.show_references(event)
            drawable = self.drawable(event)
            visible = drawable
            if event["op"] == "line":
                frame = self.camera.frame
                x, y = frame.get_center()[:2]
                bounds = (x - frame.width * 0.51, x + frame.width * 0.51,
                          y - frame.height * 0.51, y + frame.height * 0.51)
                visible = Line(*clip_line(event["geometry"], bounds), color=GOLD, stroke_width=self.size(0.85))
            self.set_hud("counter", f"{step:02d} / 09", font_size=42, color=GOLD)
            self.play(Create(visible, rate_func=linear), run_time=1.5 if event["op"] == "circle" else 1.1)
            if visible is not drawable:
                self.remove(visible)
                self.add(drawable)
            is_locus = step >= 8
            drawable.screen_width = 0.95 if is_locus else 0.40
            color = TARGET if is_locus else (CIRCLE_BLUE if event["op"] == "circle" else LINE_BLUE)
            self.play(
                drawable.animate.set_stroke(color=color, width=self.size(drawable.screen_width), opacity=0.85 if is_locus else 0.28),
                FadeOut(references), run_time=0.3,
            )
            (self.loci if is_locus else self.auxiliaries).add(drawable)
            for name, direction in reveals.get(step, []):
                self.label_point(name, direction, TARGET if step == 9 else FOREGROUND)
            if step == 5:
                self.set_hud("footer", "T 是 KG 与已有圆 ΓB 的另一交点 · 0 E", font_size=22, color=GOLD)
                self.wait(1.2)
            self.wait(0.6)

    def finish(self):
        self.set_hud("caption", "9 E · 两个镜像解 P、P′", color=TARGET)
        self.set_hud("footer", "4 条直线 + 5 个圆 · 目标在第 9 E 同时出现", font_size=22)
        self.wait(2)
        self.hide_labels(["M", "N"])
        for drawable in self.auxiliaries:
            drawable.screen_width = 0.30
        self.play(self.auxiliaries.animate.set_stroke(width=self.size(0.30), opacity=0.045), run_time=0.7)
        self.wait(0.8)
        self.play(self.loci.animate.set_stroke(opacity=0.12), run_time=0.6)
        self.set_hud("caption", "∠APB = ∠BPC = ∠CPD", font_size=25, color=TARGET)
        self.set_hud("footer", "等角连线与弧为结果示意 · 作图已在 9 E 完成", font_size=21, color=MUTED)
        rays = VGroup()
        arcs = VGroup()
        for target in self.data["targets"]:
            origin = self.point(target)
            for name in self.data["initial"]["points"]:
                rays.add(Line(origin, self.point(name), color=TARGET, stroke_width=self.size(0.75), stroke_opacity=0.65))
            vectors = [self.point(name) - origin for name in self.data["initial"]["points"]]
            angles = [math.atan2(vector[1], vector[0]) for vector in vectors]
            for first, second in zip(angles, angles[1:]):
                sweep = (second - first + math.pi) % (2 * math.pi) - math.pi
                gap = math.copysign(0.025, sweep)
                arcs.add(Arc(radius=0.30, start_angle=first + gap, angle=sweep - 2 * gap,
                             arc_center=origin, color=GOLD, stroke_width=self.size(0.9)))
                middle = first + sweep / 2
                direction = np.array([math.cos(middle), math.sin(middle), 0.0])
                arcs.add(Line(origin + direction * 0.275, origin + direction * 0.325,
                              color=GOLD, stroke_width=self.size(0.9)))
        self.play(FadeIn(rays), FadeIn(arcs), run_time=1)
        self.wait(3.8)
        self.set_hud("footer", "有解条件  3ac > b(a+b+c)    ·    当前已知一般最优值 6–9 E", font_size=20, color=MUTED)
        self.wait(3)
