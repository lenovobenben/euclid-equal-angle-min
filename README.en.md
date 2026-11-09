# Euclid-Equal-Angle-Min · Equal Viewing Angles from Four Collinear Points

[简体中文](README.md) · **English**

**Construct both mirror solutions in at most 9 E; the main branch uses 4 lines and 5 circles.**

Given A, B, C, D in order on a line, construct an off-line point P satisfying

$$
\angle APB=\angle BPC=\angle CPD.
$$

This project studies existence and minimum construction cost, with elementary traces,
general-parameter and coverage proofs, exact replays, and bounded searches.
**The full-domain upper bound is 9 E and the proved generic lower bound is 6 E.
Nine-move minimality remains open.**

[Nine-move construction](docs/NINE.md) · [Existence](docs/EXISTENCE.md) ·
[Exact replay](experiments/results/nine-replay.json) · [Generic lower bound](docs/LOWER_BOUND.md)

![Equal-angle example with consecutive lengths 3, 1, 2 and two mirror solutions](docs/assets/equal-angle.svg)

The illustration is not a charged construction trace. Manim animations will be added later.
Detailed mathematical documents are currently in Chinese.

## Current verified upper bounds

| Target | Main-branch lines | Main-branch circles | Generic `gen` | Full-domain `rob` |
|---|---:|---:|---:|---:|
| One solution in a specified half-plane `EA-ONE` | 4 | 5 | **9 E** | **9 E** |
| Both mirror solutions `EA-ALL` | 4 | 5 | **9 E** | **9 E** |

The nine-move program obtains both solutions and bounds both targets; it does not prove
that their optimal scores coincide. Equal-gap branches can be shorter. The robust score
is the worst actual cost over the proved branch partition.
`gen` covers a relatively open, dense, full-measure subset; `rob` covers every solvable input.

The **proved generic lower bound is 6 E** for either target, leaving both the generic optimum
and the full-domain worst-case optimum in **6–9 E**. This is not a pointwise lower bound for
special ratios. See [LOWER_BOUND](docs/LOWER_BOUND.md).
The 10 E original construction covers only a restricted domain, while 7 E / 2 E results
apply to specified special families: [BASELINE](docs/BASELINE.md), [REFINEMENTS](docs/REFINEMENTS.md).

### Free inputs and the solvable domain

The four ordered collinear points and their complete line are free. For AB=a, BC=b, CD=c>0,
solutions exist exactly when

$$
\Delta=3ac-b(a+b+c)>0,
$$

equivalently (a+b)(b+c)<4ac. There is then exactly one solution in each half-plane.
Failure of an auxiliary construction on a solvable input requires relabeling or a proved
alternative branch; it does not justify shrinking the original domain. See [EXISTENCE](docs/EXISTENCE.md).

## What counts as an E move

| Operation | Cost |
|---|---:|
| Draw a complete line through two existing distinct points | 1 E |
| Draw a circle centered at an existing point through another existing point | 1 E |
| Obtain or name a determined finite real intersection | 0 E |
| Four ordered collinear points and their complete line | 0 E |
| Execute the same draw again | Still 1 E |

Use an unmarked straightedge and a **collapsing compass**. Arbitrary auxiliary points,
points at infinity, and free distance transfer are forbidden. All finite real intersections
of each new object with existing distinct objects enter the point set automatically.
Composite operations must be expanded. Draws used for branch tests, failed attempts,
and duplicate draws count; referencing an existing object does not add E.

The elementary semantics follow Euclid-Min's fixed-version [metrics](https://github.com/lenovobenben/euclid-min/blob/792619b38d749643bc9d80da8110dc9cff5b4877/docs/METRICS.md) and
[formal model](https://github.com/lenovobenben/euclid-min/blob/792619b38d749643bc9d80da8110dc9cff5b4877/docs/FORMAL_MODEL.md). This project's inputs, targets, and coverage are defined in
[DESIGN](docs/DESIGN.md). Scores for different problems are not directly comparable.

## Sources and project contribution

Two original ai-math-notes conversations are preserved in [sources](sources/README.md).
The problem also appears as Problem 9 of the 1994 Austrian–Polish Mathematical Competition;
see [LITERATURE](docs/LITERATURE.md). This project independently proves existence,
audits the restricted 10 E original construction, shares an intersection to remove one circle,
proves nine-move coverage, and supplies special families and the computer-assisted generic lower bound.
Archived sources remain unchanged. No literature-minimum or world-record claim is made.

## Exact verification

| Check | Result or purpose | Record |
|---|---|---|
| Existence | Eight identities and 3,375 integer fixtures | [Report](experiments/results/existence-verification.json) |
| Full-domain 9 E | 14 identities, 21 replay fixtures, separate branch proof | [Identities](experiments/results/nine-symbolic-verification.json), [replay](experiments/results/nine-replay.json) |
| Special families and regression | Ten identities, 29 fixtures, 19 regression checks | [Identities](experiments/results/refined-symbolic-verification.json), [replay](experiments/results/refined-replay.json) |
| Generic 6 E lower bound | 192 seeds, 3,600 field, 1,680 center, and 840 denominator-unit checks | [Report](experiments/results/short-carrier-obstruction.json) |

Replays use exact SageMath QQ/AA arithmetic, automatic intersection closure, and dependency ledgers.
Finite fixtures do not replace general identities or coverage proofs. The lower bound combines
an exhaustive classification with exact elimination; it is not inferred from heuristic search misses.
Floating screens discover candidates and do not certify mathematical correctness.

## Reproduction

Use SageMath 10.7. On macOS/Linux, the pinned image runs with no network and a read-only mount:

```sh
docker run --rm --network none \
  -v "$PWD:/workspace:ro" -w /workspace \
  -e PYTHONDONTWRITEBYTECODE=1 \
  sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528 \
  sage -python experiments/verify_nine_symbolic.py
```

Run all 19 regression checks with the same image:

```sh
docker run --rm --network none \
  -v "$PWD:/workspace:ro" -w /workspace \
  -e PYTHONDONTWRITEBYTECODE=1 \
  sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528 \
  sage -python -m unittest discover -s tests -v
```

With the image cached, no persistent container is required. See [complete instructions](docs/REPRODUCING.md)
for exact replay, refinements, the lower bound, report regeneration, and existing Windows PowerShell 7
wrappers. PowerShell is not a prerequisite on every platform; the pinned path is distinguished from
older latest-based commands.

## Current research directions

Prioritize a **9→8 E** improvement over the entire solvable domain. A generic result is recorded
separately and needs robust repairs; special 7 E / 2 E families do not improve the general score.
New experiments specify state, target, domain, budget, and stopping conditions.
Future animation consumes verified geometry only. See [ROADMAP](docs/ROADMAP.md) and [SEARCH_LOG](docs/SEARCH_LOG.md).

## Documentation and code

| Content | Entry |
|---|---|
| Inputs, targets, and claim levels | [DESIGN](docs/DESIGN.md) |
| Problem statements and existence | [EXISTENCE](docs/EXISTENCE.md) |
| Nine-move construction | [NINE](docs/NINE.md) |
| Generic lower bound | [LOWER_BOUND](docs/LOWER_BOUND.md) |
| Special families | [REFINEMENTS](docs/REFINEMENTS.md) |
| Inversion and projectivity | [PROJECTIVITY](docs/PROJECTIVITY.md) |
| Full reproduction commands | [REPRODUCING](docs/REPRODUCING.md) |
| Bounded searches already performed | [SEARCH_LOG](docs/SEARCH_LOG.md) |
| Research and animation plans | [ROADMAP](docs/ROADMAP.md) |
| Sources and archived material | [LITERATURE](docs/LITERATURE.md) |
| Research scripts | [experiments](experiments/README.md) |
| Certificates and reports | [experiments/results](experiments/results/README.md) |
| Regression checks | [tests](tests/README.md) |
| Series conventions and four-project comparison | [SERIES](docs/SERIES.md) |

**Construction optimization series**:
[Euclid-Min](https://github.com/lenovobenben/euclid-min) ·
[Euclid-CCC-Min](https://github.com/lenovobenben/euclid-ccc-min) ·
[Euclid-Equal-Angle-Min](https://github.com/lenovobenben/euclid-equal-angle-min) ·
[Euclid-Castillon-Min](https://github.com/lenovobenben/euclid-castillon-min).


## License and citation

Code, tests, and configuration use [Apache 2.0](LICENSE). Mathematical documentation,
construction records, research data, and citation metadata use [CC BY 4.0](LICENSE-CONTENT).
Third-party rights are unchanged; see the [license scope](LICENSE-SCOPE.md).
Use [CITATION.cff](CITATION.cff), citing **lenovobenben, Euclid-Equal-Angle-Min**, the
[repository](https://github.com/lenovobenben/euclid-equal-angle-min), and the commit or version used.
Indicate modifications when adapting non-software content.
