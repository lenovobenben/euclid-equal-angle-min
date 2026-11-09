# Euclid-Equal-Angle-Min · 共线四点等视角的尺规构造

**简体中文** · [English](README.en.md)

**至多 9 E 构造全部两个镜像解；一般分支使用 4 条直线和 5 个圆。**

给定直线上依次排列的 A、B、C、D，作直线外点 P，使

$$
\angle APB=\angle BPC=\angle CPD.
$$

本项目研究存在性与最少尺规步数，提供逐笔构造、一般参数与覆盖证明、精确重放和有界搜索。
**当前通用上界为 9 E，已证明一般下界为 6 E；尚未证明九笔最短。**

[九笔构造与证明](docs/NINE.md) · [存在性](docs/EXISTENCE.md) ·
[精确重放](experiments/results/nine-replay.json) · [一般下界](docs/LOWER_BOUND.md)

![共线四点等视角示意：间距为 3、1、2 时的两个镜像解](docs/assets/equal-angle.svg)

图为 AB=3、BC=1、CD=2 的实例，示意图不计入作图步骤。Manim 动画后续补充。

## 当前已验证上界

| 目标 | 一般分支直线 | 一般分支圆 | 一般位置 `gen` | 完整域 `rob` |
|---|---:|---:|---:|---:|
| 指定半平面内单解 `EA-ONE` | 4 | 5 | **9 E** | **9 E** |
| 全部两个镜像解 `EA-ALL` | 4 | 5 | **9 E** | **9 E** |

九笔程序同时获得两解，为两个目标分别提供上界；这不证明两个最优值相同。
相等间距等分支可少于九笔，完整域成本取所有已证明分支的最坏值。
`gen` 要求相对开稠密、满测度的覆盖；`rob` 覆盖全部有解输入，并计入实际分支成本。

**已证明的一般下界为 6 E**，适用于单解和两解目标，因此一般最优值与完整域最坏最优值
均处在 **6–9 E**。该下界不适用于每个特殊比例实例；证明与有限符号排除见
[LOWER_BOUND](docs/LOWER_BOUND.md)。

原作图的 10 E 是受限域基线；7 E / 2 E 结果属于明确的特殊条件族，
不更新通用上界，详见 [BASELINE](docs/BASELINE.md) 与 [REFINEMENTS](docs/REFINEMENTS.md)。

### 免费输入与有解域

免费输入为四个有序共线点及其完整直线。设 AB=a、BC=b、CD=c，a,b,c>0。
**有解的充要条件**为

$$
\Delta=3ac-b(a+b+c)>0,
$$

等价于 (a+b)(b+c)<4ac；有解时每侧恰有一个解。
无解条件与辅助构造的额外比例限制必须区分：有解而当前路线不适用时，
应重新标号或进入已证明分支，不能因此缩小题目的有解域。证明见 [EXISTENCE](docs/EXISTENCE.md)。

## E 步：唯一采用的计数法

| 操作 | 成本 |
|---|---:|
| 经过两个已有不同点画一条完整直线 | 1 E |
| 以一个已有点为圆心、经过另一个已有点画圆 | 1 E |
| 获得或命名已有对象的确定有限实交点 | 0 E |
| 四个有序共线点及其完整直线 | 0 E |
| 再次执行一次相同的画线或画圆动作 | 仍计 1 E |

采用无刻度直尺与**塌圆规**，不允许任取辅助点、使用无穷远点或免费异地搬运距离。
每画一个新图元，它与全部已有不同对象的有限实交点自动进入点集。
中点、垂线、平行线、三点作圆和反演等宏须展开计费；分支判断新增的图元、
失败尝试和实际重复绘制同样计费。只引用已有对象不增加 E。

基础语义沿用 Euclid-Min 固定版本的 [计分规范](https://github.com/lenovobenben/euclid-min/blob/792619b38d749643bc9d80da8110dc9cff5b4877/docs/METRICS.md)与[正式模型](https://github.com/lenovobenben/euclid-min/blob/792619b38d749643bc9d80da8110dc9cff5b4877/docs/FORMAL_MODEL.md)。
本题的免费输入、目标及覆盖范围以 [DESIGN](docs/DESIGN.md) 为准。
不同题目的分数不能仅凭计数法相同就直接比较。

## 来源与项目贡献

直接来源是 ai-math-notes 中的两篇原始问答，快照保存在 [sources](sources/README.md)。
本题也见于 1994 年奥地利—波兰数学竞赛第 9 题，出处见 [LITERATURE](docs/LITERATURE.md)。
本项目独立证明存在条件，审计原作图的受限 10 E，利用共享交点省去一个辅助圆，
完成九笔分支覆盖、条件族及六笔一般下界的计算机辅助证明。
原文快照不改写，数值候选与正式认证分开记录；不声称文献最短或世界纪录。

## 精确验证

| 核验 | 结果或作用 | 记录 |
|---|---|---|
| 存在性 | 8 项恒等式与 3,375 组整数夹具 | [存在性报告](experiments/results/existence-verification.json) |
| 九笔通用构造 | 14 项恒等式与 21 个分类重放夹具，分支覆盖另有证明 | [符号报告](experiments/results/nine-symbolic-verification.json)、[重放](experiments/results/nine-replay.json) |
| 条件族与回归 | 10 项恒等式、29 个分类夹具及 19 项回归测试 | [符号报告](experiments/results/refined-symbolic-verification.json)、[重放](experiments/results/refined-replay.json) |
| 六笔一般下界 | 192 种种子、3,600 项域检查、1,680 项圆心条件、840 项分母单位检查 | [符号报告](experiments/results/short-carrier-obstruction.json) |

正式重放使用 SageMath QQ/AA 精确运算、自动交点闭包与依赖台账。
有限样本不替代一般参数与分支覆盖证明；下界来自完备分类加精确排除，
不由启发式搜索零结果推出。数值筛查只负责发现候选，不承担正式数学判定。

## 复现

精确验证使用 SageMath 10.7。固定镜像、断网、只读挂载的命令可直接用于 macOS/Linux：

```sh
docker run --rm --network none \
  -v "$PWD:/workspace:ro" -w /workspace \
  -e PYTHONDONTWRITEBYTECODE=1 \
  sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528 \
  sage -python experiments/verify_nine_symbolic.py
```

完整 19 项回归测试可用同一镜像运行：

```sh
docker run --rm --network none \
  -v "$PWD:/workspace:ro" -w /workspace \
  -e PYTHONDONTWRITEBYTECODE=1 \
  sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528 \
  sage -python -m unittest discover -s tests -v
```

已有镜像时无需常驻容器。九笔精确重放、条件族、一般下界、报告再生成与
Windows PowerShell 7 兼容入口见 [完整复现说明](docs/REPRODUCING.md)。
PowerShell 不是所有平台的前置依赖；固定镜像与旧 latest 命令的区别亦在该文档说明。

## 当前研究方向

主线是整个有解域上的最坏成本 **9→8 E**。若先取得一般位置改进，应单独记 gen，
继续研究 rob 补齐；特殊 7 E / 2 E 不更新通用成绩。
新实验先声明初态、目标、覆盖域、预算和停止条件，避免重复无边界扩搜。
后续动画只读取已验证几何轨迹。详见 [ROADMAP](docs/ROADMAP.md) 与 [SEARCH_LOG](docs/SEARCH_LOG.md)。

## 文档与代码入口

| 内容 | 入口 |
|---|---|
| 输入、目标与声明等级 | [DESIGN](docs/DESIGN.md) |
| 题目与存在性 | [EXISTENCE](docs/EXISTENCE.md) |
| 九笔通用构造 | [NINE](docs/NINE.md) |
| 六笔一般下界 | [LOWER_BOUND](docs/LOWER_BOUND.md) |
| 特殊条件族 | [REFINEMENTS](docs/REFINEMENTS.md) |
| 反演与射影变换 | [PROJECTIVITY](docs/PROJECTIVITY.md) |
| 完整复现命令 | [REPRODUCING](docs/REPRODUCING.md) |
| 已有搜索范围 | [SEARCH_LOG](docs/SEARCH_LOG.md) |
| 研究路线与动画计划 | [ROADMAP](docs/ROADMAP.md) |
| 来源与原始快照 | [LITERATURE](docs/LITERATURE.md) |
| 研究脚本 | [experiments](experiments/README.md) |
| 证书与报告 | [experiments/results](experiments/results/README.md) |
| 回归检查 | [tests](tests/README.md) |
| 系列约定与四项目对照 | [SERIES](docs/SERIES.md) |

**尺规作图优化系列**：
[Euclid-Min](https://github.com/lenovobenben/euclid-min) ·
[Euclid-CCC-Min](https://github.com/lenovobenben/euclid-ccc-min) ·
[Euclid-Equal-Angle-Min](https://github.com/lenovobenben/euclid-equal-angle-min) ·
[Euclid-Castillon-Min](https://github.com/lenovobenben/euclid-castillon-min)。


## 许可与引用

代码、测试和配置采用 [Apache 2.0](LICENSE)；数学文档、构造记录、研究数据及
项目引用元数据采用 [CC BY 4.0](LICENSE-CONTENT)。第三方材料保持其原有权利，
详见[许可范围](LICENSE-SCOPE.md)。引用时请使用 [CITATION.cff](CITATION.cff)，
注明 **lenovobenben，Euclid-Equal-Angle-Min**、[仓库地址](https://github.com/lenovobenben/euclid-equal-angle-min)
及所用提交或版本；改编非软件内容时注明修改。
