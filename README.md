# Euclid-Equal-Angle-Min · 共线四点等视角的最短尺规构造

**简体中文** · [English](README.en.md)

给定一条直线上依次排列的四个不同点 A、B、C、D，研究直线外满足

$$
\angle APB=\angle BPC=\angle CPD
$$

的点 P 何时存在，以及构造它们所需的最少尺规步骤。

本项目是 lenovobenben 的**尺规作图优化系列第三个项目**。目录结构、E 步计数和验证标准参照 Euclid-CCC-Min；各项目分别定义输入与目标，步数按各自规则配置比较。

| 项目 | 研究题目 | 本地目录 |
|---|---|---|
| Euclid-Min | 正十七边形 | `../euclid-min/` |
| Euclid-CCC-Min | 阿波罗尼乌斯三圆相切问题 | `../euclid-ccc-min/` |
| Euclid-Equal-Angle-Min | 共线四点的三个相等视角 | 本项目 |

## 当前状态

2026-11-09 已完成存在条件、两解唯一性及原作图的一般参数证明，并用 Docker 中的 SageMath 10.7 精确重放。**原作图在其明确受限域上给出单解与双解均为 10 E 的已验证上界；尚无整个有解域的构造上界或最小性结论。**

原作图的精确适用域为：在 `3ac>b(a+b+c)` 的基础上，还需 `b<2a`、`b<2c`、`a≠b`、`b≠c`。其完整程序为 **4 线 + 6 圆 = 10 E**。限制来自辅助圆不相交/相切，以及定心线平行底线，见 [BASELINE](docs/BASELINE.md)。

## 两问与研究目标

1. **存在性**：设 AB=a、BC=b、CD=c，已证明充要条件为 `3ac > b(a+b+c)`；有解时恰有两个镜像解。公共角满足 `b(a+b+c)/(ac) = 3−4sin²θ`。临界退化分为有限合并点和无穷远两类，见 [EXISTENCE](docs/EXISTENCE.md)。
2. **最短作图**：在有解输入上，分别研究构造指定一侧的一个解与构造全部解的最少 E 步。原作图以 X、X′ 命名输出，本项目统一记作 P、P′。

两问完整表述见 [PROBLEMS](docs/PROBLEMS.md)，原作图展开见 [BASELINE](docs/BASELINE.md)。

## E 步计数

| 操作 | 成本 |
|---|---:|
| 经过两个已有不同点画完整直线 | 1 E |
| 以一个已有点为圆心、经过另一个已有点画圆 | 1 E |
| 获得已有对象的有限实交点 | 0 E |
| 给定的四点和直线 l | 0 E |

采用无刻度直尺与塌圆规。新点来自已有线、圆的有限实交点；不任取点，不免费搬运距离。中点、垂线、平行线等宏须展开。实际重复绘制仍计费，所有有限实交点自动可用。

先区分指定一侧单解 `EA-ONE` 与全部解 `EA-ALL`，再分别记录一般位置 `gen` 和完整有解域 `rob`。输入直线 l 已给出；只有四点、未给直线的变体须另立规则配置。详见 [DESIGN](docs/DESIGN.md)。

## 项目结构

```text
docs/                 题目、模型、基线、来源与研究记录
sources/              两篇原始问答快照与来源清单
experiments/          未来的 replay_ / verify_ / search_ / audit_ 脚本
experiments/results/  未来的重放与搜索结果
tests/                未来的精确验证回归测试
animations/           未来的几何导出、分镜和动画
```

| 内容 | 入口 |
|---|---|
| 两问及边界 | [PROBLEMS](docs/PROBLEMS.md) |
| 长度限制的几何含义与完整存在性证明 | [EXISTENCE](docs/EXISTENCE.md) |
| 输入、目标、工具与声明标准 | [DESIGN](docs/DESIGN.md) |
| 原作图与名义动作表 | [BASELINE](docs/BASELINE.md) |
| 来源、版本与引用 | [LITERATURE](docs/LITERATURE.md)、[原文清单](sources/manifest.json) |
| 下一阶段安排 | [ROADMAP](docs/ROADMAP.md) |
| 研究进展与证据 | [RESEARCH_LOG](docs/RESEARCH_LOG.md) |

当前已完成存在性与原作图的受限域基线，下一步可研究限制条件下的调整分支，或在相同覆盖域上搜索省步方案。尚未启动最短步数搜索。

复现原作图的一般参数核验、自动交点闭包重放、依赖台账与回归测试：

```powershell
pwsh -NoProfile -File experiments/verify-original.ps1
```

12 个一般参数恒等式、12 个分类夹具与 9 项回归测试通过。5 个完整重放均为 10 E；另外 6 个有解输入准确识别原作法限制，1 个输入判为无解。完整证据见 [BASELINE](docs/BASELINE.md#6-精确验证闭环)。

从仓库根目录使用已有 `sage` Docker 容器复现符号核验：

```powershell
Get-Content -Raw experiments/verify_existence.sage.py | docker exec -i sage sage -python
```

存在性核验结果为 8 个一般参数恒等式及 3375 组整数夹具通过；记录见 [existence-verification.json](experiments/results/existence-verification.json)。有限夹具不替代文档中的一般参数证明。

## 许可

沿用参考项目的分范围许可：原创代码采用 [Apache 2.0](LICENSE)，原创文档与研究数据采用 [CC BY 4.0](LICENSE-CONTENT)。归档原文仍依其来源权利与许可处理，见 [LICENSE-SCOPE](LICENSE-SCOPE.md)。
