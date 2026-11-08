# Euclid-Equal-Angle-Min

[简体中文](README.md) · **English**

Given four distinct collinear points A, B, C, D in that order, determine when an off-line point P satisfies

$$
\angle APB=\angle BPC=\angle CPD,
$$

and minimize the straightedge-and-compass moves needed to construct the solutions.

This is the third project in lenovobenben's construction optimization series, following Euclid-Min (regular 17-gon) and Euclid-CCC-Min (the Apollonius three-circle problem). The directory layout and elementary-move conventions follow Euclid-CCC-Min.

## Status

Initialized on 2026-11-09. Existence and uniqueness have been independently proved: solutions exist exactly when `3ac > b(a+b+c)`, and then there are exactly two mirror solutions. The common angle satisfies `b(a+b+c)/(ac) = 3−4sin²θ`.

The original construction is now proved and exactly replayed on the restricted domain with `b<2a`, `b<2c`, `a!=b`, and `b!=c`. It draws six circles and four lines: a verified 10 E upper bound for both one and all solutions on that domain. It is not a generic or robust upper bound on the entire solvable domain, and is not a minimality claim.

## Rules and goals

- Free input: four ordered collinear points and their line.
- Draw a line through two existing distinct points: 1 E.
- Draw a circle centered at an existing point through another existing point: 1 E.
- All finite real intersections of existing objects: 0 E.
- Collapsible compass; no arbitrary points or free radius transfer.
- Repeated drawing actions still cost 1 E each.

Track one solution in a specified half-plane (`EA-ONE`) and all solutions (`EA-ALL`) separately, with generic (`gen`) and full-domain (`rob`) coverage. Existence, exceptional cases and uniqueness remain proof obligations.

## Layout

`docs/` contains the problems, design, baseline, references, roadmap and research log. [EXISTENCE](docs/EXISTENCE.md) proves existence and uniqueness. [BASELINE](docs/BASELINE.md) proves the original construction and classifies its limitations. `sources/` stores original snapshots and provenance. `experiments/` contains SageMath symbolic verification, exact AA geometry and construction replay; `tests/` contains nine regression tests. `animations/` is reserved for subsequent work.

With an existing Docker container named `sage`, run `pwsh -NoProfile -File experiments/verify-original.ps1`. It checks twelve baseline identities, replays twelve classified fixtures with automatic finite-intersection closure and E accounting, saves provenance traces, and runs the regression tests. The existence verifier separately checks eight identities and 3,375 integer fixtures.

Start with [the design](docs/DESIGN.md), [the baseline](docs/BASELINE.md) and [the roadmap](docs/ROADMAP.md). Detailed research documents are in Chinese.

Original code is licensed under Apache 2.0; original documentation and research data under CC BY 4.0. Archived source material retains its source rights; see [license scope](LICENSE-SCOPE.md).
