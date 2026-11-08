# 有界搜索记录

## 2026-11-09：从 10 E 降到 9 E

共同筛查夹具为 (37,19,43)、(41,23,31)、(29,31,53)、(53,31,29)。仅为数值预筛，把 BC 归一为 1；坐标规范化不增加实际构造对象。最终候选另由精确重放和一般参数证明认证。

### 固定原四圆后的三步共同定心

初态为四个输入点、l 和原作图四只辅助圆，自动闭包在多夹具绑定中有 14 个点。枚举一个新线/圆，再用载体产生一个圆心，最后产生另一个圆心，预算为后加 3 E；最终两个轨迹圆另计 2 E。

[search_shared_centers.py](../experiments/search_shared_centers.py) 检查了 225 个首步对象、16 个第二步定心候选和 13626 个第三步候选，未命中。122 次跨夹具实根数不同的交点绑定被跳过。结果见 [shared-centers-screen.json](../experiments/results/shared-centers-screen.json)。

限制：只覆盖声明的定心顺序；不包括最后一个对象同时产生两圆心等其他形状，浮点容差、跨夹具分支绑定和跳过的根数不一致分支也限制覆盖。因此不是 9 E 下界。

### 三只起始圆与两段定心

枚举“3 只输入点定心定半径的圆 → 至多 2 E 得到 M → 至多 2 E 得到 N”，也反向尝试 N、M。最后两只轨迹圆另计 2 E。

先检查从原四只辅助圆删去一只的四个前缀，未命中；随后扩展到四点可直接绘制的 12 只圆的三元组合。扩展试验在第 34 个前缀找到候选：

```text
Circle(A,B), Circle(B,C), Circle(C,D)
HE, KG
CT, GR
Circle(M,B), Circle(N,C)
```

首个完成筛查检查 10470 个第一核心对象、437272 个经过数值预筛的第二步候选、24 个首圆心程序；扩展试验在 31961 个第一核心对象、1293874 个经过数值预筛的第二步候选及 63 个首圆心程序后命中。两组“第二步候选”包含随后因重画已有对象等原因拒绝的候选，不能与未向量化版本的全部候选数直接比较。

[search_three_circle_prefix.py](../experiments/search_three_circle_prefix.py) 的原四圆删一筛查约 7.9 秒，扩展到命中约 23.2 秒；这些是本次 SageMath/NumPy 环境的实测耗时。结果为 [three-circle-prefix-screen.json](../experiments/results/three-circle-prefix-screen.json)、[three-circle-all-prefixes-screen.json](../experiments/results/three-circle-all-prefixes-screen.json)。扩展试验命中后停止，没有遍历所有前缀。

跨夹具实根数不同的绑定在首组跳过 8004 次，在扩展组跳过 22771 次。这些计数包含不同状态中的重复绑定观察，不代表不同几何分支数。

### 认证与继续工作的边界

数值候选导向了新的平行关系 T−C=(b/a)G。SageMath 核验、一般参数证明及相等间距补充分支，将结果认证为整个有解域上最坏 9 E，详见 [NINE](NINE.md)。

候选搜索本身不承担精确认证或下界责任。后续不应原样重复已完成筛查；下一步应改变起始状态、共享对象形状或目标表示，并先声明新的预算。当前未开展一般 8 E 的完整搜索。

在已有 `sage` 容器中复现搜索，复制两个搜索脚本至同一目录后运行：

```powershell
docker exec sage sage -python /tmp/euclid-equal-angle-min-baseline/experiments/search_three_circle_prefix.py --seconds 40
docker exec sage sage -python /tmp/euclid-equal-angle-min-baseline/experiments/search_three_circle_prefix.py --seconds 40 --all-prefixes
```

该路径是本轮容器任务目录；新环境应先复制脚本或使用其实际所在路径。搜索依赖 NumPy 时使用向量预筛，无 NumPy 时自动用标量版本，限时内覆盖数量与耗时会改变。确定性几何结论通过 `verify-nine.ps1` 独立复现，不依赖限时搜索能否再次运行到命中点。

## 2026-11-09：第二轮，尝试一般 8 E

一般上界仍为 9 E。本轮认证的进一步改善为明确条件族上的 7 E 与 2 E，步骤、证明和条件边界见 [REFINEMENTS](REFINEMENTS.md)。下列数值零结果不升级为下界。

### 第一目标圆五笔前缀之后，三笔直接取目标

初态固定为 `Circle(A,B), Circle(B,C), HE, KG, Circle(M,B)` 的自动交点闭包。最后三笔允许任意辅助对象、任意辅助对象、一个含目标的线/圆；目标可以是指定一侧的一个点，不强制构造第二圆心。每个含目标候选仍须实际求交，并确认目标出现在可用点集合中。

[search_eight_suffix.py](../experiments/search_eight_suffix.py) 使用原四个不同长度样本，先检查第一笔固定为 Circle(C,D) 的诊断子类：467 个第二步对象，未命中，见 [报告](../experiments/results/eight-right-circle-screen.json)。

任意第一笔的筛查分四段完成，第一笔枚举索引依次从 0、117、232、342 开始；前三段达到 40 秒预算，重新执行未完成的首步，最后一段遍历至结尾。计数包含重复首步及其部分重复后缀：

| 起始索引 | 本段执行的首步 | 第二步对象 | 状态 |
|---:|---:|---:|---|
| 0 | 86 | 57361 | 在 117 处达到预算 |
| 117 | 102 | 62569 | 在 232 处达到预算 |
| 232 | 90 | 58870 | 在 342 处达到预算 |
| 342 | 56 | 33362 | 遍历到结尾 |

合计观察 212162 个第二步对象，没有目标候选。跨夹具实根数不同的绑定共跳过 284341 次，含重启重复观察。报告为 [0](../experiments/results/eight-first-locus-screen.json)、[117](../experiments/results/eight-first-locus-screen-117.json)、[232](../experiments/results/eight-first-locus-screen-232.json)、[342](../experiments/results/eight-first-locus-screen-342.json)。

另用反向标号后长外段在左的四个不同样本 (43,19,37)、(41,23,31)、(53,31,29)、(59,41,37) 筛查，以避免把原样本上不统一的方向当作必要限制。第一段 40 秒检查 109 个首步、64654 个第二步对象，在首步 142 处停止；第二段从 142 重启，再检查 106 个首步、61648 个第二步对象，停在 259。两段均未命中，此变体尚未完整遍历；见 [定向报告 0](../experiments/results/eight-oriented-screen.json)与[定向报告 142](../experiments/results/eight-oriented-screen-142.json)。

分段计数摘要见 [eight-search-summary.json](../experiments/results/eight-search-summary.json)，只汇总实际观察，不去除重启导致的重复状态。

### 三圆前缀与三笔联合定心

[search_eight_joint.py](../experiments/search_eight_joint.py) 检查 220 个输入圆三元集合、19684 个新增首步、186 个第二步定心对象，没有最后一步取得另一圆心的候选。跳过 7412 次根数不一致绑定。最后两个目标圆另计 2 E，因此目标总成本为 8 E。报告见 [eight-joint-screen.json](../experiments/results/eight-joint-screen.json)。

此模型要求第二笔之前或之后至少得到一个圆心，不覆盖最后一个对象同时首次产生两个圆心的形状。

### 二圆前缀与每个圆心至多两笔

[search_three_circle_prefix.py](../experiments/search_three_circle_prefix.py) 增加 `--prefix-size 2`，先取得 M，再取得 N，也尝试相反顺序。检查覆盖全部 66 种二圆集合的 68 个顺序前缀；额外两次来自优先前缀与通用列表中相反的画圆顺序。共 8498 个第一核心对象、220712 个数值预筛后的第二步候选、16 个首圆心程序，未命中，跳过 2751 次根数不一致绑定。报告见 [eight-two-circle-prefix-screen.json](../experiments/results/eight-two-circle-prefix-screen.json)。

它只覆盖“两笔内得到一个圆心，再两笔内得到另一圆心”的形状，不是整个 8 E 程序空间。

### 条件族的阳性结果与认证

把样本改为 a=c 或 c=b 时，固定五笔第一目标圆后用至多两笔收尾，分别找到中垂线程序与镜像圆程序。实际归一化长度存于 `normalized_lengths` 字段，原 `fixtures` 字段仅是基础样本来源；见 [等外段报告](../experiments/results/equal-outer-screen.json)、[等邻段报告](../experiments/results/equal-neighbor-screen.json)。

通过一般距离公式进一步发现 ac=b(a+b) 和 ac=b(b+c) 两族可以直接画两只输入点确定的圆，舍弃整个五笔前缀。它们由独立符号证明和精确重放认证为恰好 2 E，不依赖浮点筛查结论。

本轮没有证明 7 E 条件族最短，也没有证明一般 8 E 不可能。后续应改变固定五笔第一目标圆的前缀或目标表示；相同夹具、相同顺序与相同预算的已完成筛查不应原样重跑。

## 2026-11-09：第三轮，改变前缀与目标载体

一般上界仍为 9 E；本节所有数值筛查都没有找到 8 E。独立新增的一般六笔下界由 [LOWER_BOUND](LOWER_BOUND.md) 的完整分类及精确计算证明，不由本节零结果推断。

### 夹具、初态与共同限制

初态始终只有四个输入点和底线；下面前缀的每一次画圆都计入总预算。数值坐标将 b 归一为 1，不添加免费点。公共组 `all` 为 (43,19,37)、(41,23,31)、(53,31,29)、(59,41,37)，长外段均在左。

- `outer-shorter`： (53,31,29)、(59,41,37)、(40,5,2)，均 c<b。
- `outer-longer`： (43,19,37)、(41,23,31)、(71,37,43)，均 c>b。
- `near`： (23,20,21)、(12,10,11)、(23,20,19)、(30,25,24)。
- `chamber`： (47,29,37)、(67,41,53)、(79,47,61)。相邻比例用于减少跨区域根数变化，不代表覆盖证明。

数值脚本跳过跨夹具实根数不同的交点绑定，根序绑定也可能遗漏其他选择；有限夹具、浮点容差、声明的程序形状均限制结论。完成一次这种筛查不等于完备枚举整个 E 程序空间。

### 自适应起始圆

[search_dynamic_prefix.py](../experiments/search_dynamic_prefix.py) 的 `adaptive-two` 允许第二圆使用第一圆生成的轴反射点，再各用至多两笔取得 M、N，最后两目标圆，总预算 8 E。`point-third` 使用两个输入圆和一个以新轴外交点为心的圆，再用三笔取得两个圆心，最后两目标圆，总预算同为 8 E。

| 模式与组 | 前缀数 | 主要计数 | 状态 |
|---|---:|---|---|
| adaptive-two / all | 216 | 22226 首核心对象、534916 次第二候选、26 首圆心程序 | 完成，未命中 |
| point-third / all | 203 | 29340 联合首对象、1433 第二定心对象 | 完成，未命中 |
| point-third / outer-shorter | 168 | 22999 首对象、960 第二对象 | 完成，未命中 |
| point-third / outer-longer | 217 | 31703 首对象、1433 第二对象 | 完成，未命中 |

报告为 `dynamic-adaptive-two-all.json`、`dynamic-point-third-all.json` 及两个 `dynamic-point-third-outer-*.json`。各模式第三笔之前的种子定义不同；不是互相包含的四次完整 8 E 搜索。联合定心模式仍排除最后一个对象首次同时产生两个圆心等形状。

### 提前画第一目标圆

[search_output_first.py](../experiments/search_output_first.py) 枚举三输入圆，至多两笔取得 M 或 N，然后立刻画第一目标圆，使它的新增交点可参与剩余任意辅助对象及最终目标载体。总预算为 3+2+1+2=8 E。

`all` 组的 220 个三圆集合已分五段遍历到结尾：

| 起始前缀 | 停止 / 恢复前缀 | 第一轨迹程序数 | 尾部首对象数 | 状态 |
|---:|---:|---:|---:|---|
| 0 | 29 | 49 | 44339 | 40 秒耗尽 |
| 29 | 93 | 46 | 36877 | 40 秒耗尽 |
| 93 | 171 | 42 | 39606 | 40 秒耗尽 |
| 171 | 193 | 46 | 43085 | 40 秒耗尽 |
| 193 | 220 | 30 | 30462 | 遍历到结尾 |

合计观察 213 个第一轨迹程序及 194369 个尾部首对象，没有最终目标载体候选。计数包含段首重复前缀的部分重复，不能当成互异程序数。报告为 `output-first-all.json` 和 `output-first-all-{29,93,171,193}.json`，从 0 到结尾的范围已衔接，无需原样重跑。

`near` 组只完成起始索引 0 到前缀 28 的部分：42 第一轨迹程序、38804 尾部首对象，报告 `output-first-near-0.json`；可从 **28** 恢复，不能声称遍历完成。

### 非标准第一目标载体的虚拟见证

[search_alternative_locus.py](../experiments/search_alternative_locus.py) 从三输入圆与任意第四笔开始，利用以下虚拟见证筛第五笔：已有轴心的目标半径端点、经过已有端点的新轴心、目标竖线上的支持点。虚拟点仅筛选候选，不进入真实状态。第六笔实际画第一目标载体，再允许任意第七笔与目标第八笔。标准 M、N 圆在此跳过。

`all` 的首段 40 秒在前缀 **53** 停止，观察 5253 第四对象、80 第五见证对象，没有非标准第一轨迹。报告 `alternative-locus-all.json`。阳性校准验证已知 KG→M 不会被见证过滤器丢弃，且 M 从未被虚拟注入状态。

未覆盖：第五笔同时首次提供某圆的圆心和半径端点，以及一般非对称首载体等。此段尚未遍历完成，若继续从 53 恢复。

### 二输入圆、四辅助笔：允许第一个圆心晚出现

[search_four_line_core.py](../experiments/search_four_line_core.py) 新增 2 个输入圆 + 4 条辅助线 + 2 个标准轨迹圆的形状。前两条线任意；若此时没有圆心，第三条线必须取得 M 或 N，第四条线取得另一个。由于不同于底线的直线不能同时包含两个不同轴点，这覆盖该数值绑定中的四线定心形状，包括先前两笔一圆心模式之外的“三笔首圆心、一笔另一圆心”。

`chamber` 组的全部 66 个二圆集合完成：416 首线、7716 第二线、456 第三线，第四线候选为零，跳过 6 次根数不一致绑定；报告 `four-line-chamber-0.json`。这是已声明形状的浮点筛查，不是四线方案不可能的证明。

`--mixed` 允许四辅助笔为线或圆，但仍要求第三笔之前取得首圆心，排除最后一圆首次同时生成两个圆心。两个 40 秒段从前缀 0、15 启动，分别观察 72243、70642 第二对象，下一恢复前缀 **29**；报告 `four-core-chamber-0.json`、`four-core-chamber-15.json`。报告键名保留 `first_lines` 等，但 mixed 模式的这些键实际统计任意辅助对象。

### 精确平方根域屏障：仅针对声明的三圆 / 四圆形状

[search_target_discriminant.py](../experiments/search_target_discriminant.py) 检查两个可自适应轴心圆产生 G 后，Circle(G,Q) 与已有种子圆求交的因子；192 种种子对、720 个第三圆、2880 次可整除性测试、72 个恒等切触种子跳过，没有 Δ 因子命中。报告 `target-discriminant-screen.json`。这一版是“Δ 可整除”必要性筛查，不单独证明全程序下界。

[search_four_circle_field.py](../experiments/search_four_circle_field.py) 进一步利用 Circle(G,Q) 免费提供的轴点 T=2Gx−Q，第四圆使用 T 为圆心或半径端点。检查 8448 个第四圆、21120 个判别式，没有奇指数 Δ 因子。报告 `four-circle-field-screen.json`。奇偶判定已修正为允许指数 3、5 等，并以 Δ³ / Δ⁴ 等校准；已重跑受影响检查，不能把旧的“指数恰为 1”条件当作奇指数的完整检查。

这两个脚本都只针对特定几何形状。后来六笔一般下界采用独立的完整第三笔分类和额外轴心剩余条件，见 [LOWER_BOUND](LOWER_BOUND.md)。

### 复现与恢复

上述数值筛查默认单段 40 秒，容器工作目录为 `/tmp/euclid-equal-angle-min-nine/experiments`。复制对应脚本和依赖到同一目录后执行，例如：

```powershell
docker exec sage sage -python /tmp/euclid-equal-angle-min-nine/experiments/search_four_line_core.py --mixed --region chamber --seconds 40 --start-prefix 29 --output /tmp/four-core-chamber-29.json
```

未完成入口依次为：mixed 二圆四笔前缀 29、非标准第一载体前缀 53、near 提前目标圆前缀 28。下一轮是否继续这些筛查，需按新结构线索决定；不以重复计数扩大排除声明。
