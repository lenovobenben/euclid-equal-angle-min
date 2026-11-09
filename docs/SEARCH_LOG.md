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

## 2026-11-09：第四轮，末圆同时定心与五笔替代前缀

本轮未找到完整的通用 8 E 程序，正式一般下界仍为 6 E，全域最坏上界仍为 9 E。
新增两种第一目标圆的五笔前缀，完成参数恒等式与固定实例精确核验。
数值筛查、前缀核验、完整目标生成及全域覆盖在以下分别记录。

### 初态、目标与预算

初态只有 A、B、C、D 及其完整直线，规则为 `collinear-four-equal-angle-e-v1`。
搜索时令 b=1 仅用于数值坐标，不增加免费对象。
目标为至多 8 E 产生原始等角解，标准两圆心路线同时追求两个解。

沿用第三轮的 `all` 和 `chamber` 夹具，另用 `short-chamber`，取
`(47,29,23)、(67,41,31)、(79,47,37)`。`chamber` 的三例均 c>b，
`short-chamber` 的三例均 c<b。各报告保存实际精确整数输入及归一化显示值。
运行环境为 SageMath 10.7，实际镜像 `sagemath/sagemath:latest` 对应固定摘要
`sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528`。

### 最后一只辅助圆同时首次产生 M、N

设 M=(m,0)、N=(n,0)，在一般分支中

\[
m=\frac{ab}{a-b},\qquad n=\frac{b^2}{b-c},\qquad
m-n=-\frac{b(ac-b^2)}{(a-b)(b-c)}\ne0.
\]

若圆心为 (u,v) 的一只圆通过 M、N，比较两点到圆心的距离平方得到

\[
u=\frac{m+n}{2},\qquad r^2=\frac{(m-n)^2}{4}+v^2.
\]

这允许圆心位于轴外。对第 6 笔为该圆的形状，第 5 笔若新提供圆心，
它必须产生直线 x=(m+n)/2 与某个旧对象的交点。若圆心已可用、
半径端点新出现，该端点必须是对应虚拟圆与旧对象的交点。
这些虚拟点只过滤第 5 笔候选，不进入真实点集。最后实际画圆、求交，
再检查两个圆心均成为可用点，末尾两个目标圆另计 2 E。

[search_simultaneous_centers.py](../experiments/search_simultaneous_centers.py)
补查此前联合定心筛查遗漏的“最后一圆同时首次产生两个圆心”形状。
三圆模式允许任意第 4 笔，二圆模式允许任意第 3、4 笔。

| 起始圆数与组 | 时间上限 | 起始组合观察 | 第 4 笔对象 | 结果与恢复点 |
|---|---:|---:|---:|---|
| 3 / all | 90 秒 | 220 | 21226 | 遍历到末尾，未命中 |
| 3 / chamber | 90 秒 | 220 | 22792 | 遍历到末尾，未命中 |
| 3 / short-chamber | 90 秒 | 220 | 22262 | 遍历到末尾，未命中 |
| 2 / chamber | 120 秒 | 18，含末个未完成组合 | 89239 | 达到预算，重启组合 17 |

这四组未筛出含新支持见证的第 5 笔，亦未发现可直接同时定心的圆。
报告分别为 `simultaneous-centers-{all,chamber,short-chamber}-0.json` 和
`simultaneous-two-seed-chamber-0.json`。
跨夹具根数不一致仍被跳过，三圆模式的“遍历到末尾”只针对声明的浮点绑定形状。
二圆模式剩余组合尚未遍历。

阳性控制使用合法圆、直径线和割线，分别验证“新圆心”和“旧圆心加新半径端点”
两类见证不会被过滤掉，并实际求交生成两个校准点。
另有标量 / NumPy 过滤一致性及轴外圆心控制。

### 两圆起步，第五笔画出第一目标载体

[search_early_locus.py](../experiments/search_early_locus.py) 枚举两只输入圆、
任意第三笔、见证过滤的第四笔及实际第五笔目标载体。
随后允许任意第六笔、见证过滤的第七笔和实际第八笔目标载体。
见证复用既有 `search_alternative_locus.py`，覆盖已知轴心圆心、已知半径端点
或目标竖线的情况，仍可能漏掉两个支持点同时新出现或非对称载体。

| 组 | 总时间 / 单前缀尾部预算 | 第一载体记录 | 尾部观察 | 完成情况 |
|---|---|---:|---|---|
| all | 120 秒 / 8 秒，最多 12 条前缀记录 | 12 | 4099 第六笔、1276 第七笔 | 达到前缀数量上限，4 个尾部遍历到末尾、8 个限时停止 |
| chamber | 120 秒 / 4 秒，最多 24 条前缀记录 | 18 | 2637 第六笔、0 个过滤后的第七笔 | 两圆组合扫描到 66，18 个尾部均限时停止 |

两组均未找到最终目标候选。报告为 `early-locus-all-0.json` 和
`early-locus-chamber-0.json`。前者最后观察位置为组合 59、第三笔索引 74、
第四笔见证索引 21，若从组合 59 重启会重复该组合已完成部分。
后者的组合扫描已到末尾，但尾部搜索未完成，报告状态明确记为
`prefix_scan_completed_with_incomplete_tails`。

### 已核验的两种替代五笔前缀

二者均得到现有第一目标圆 ΓM=Circle(M,B)，没有把原始目标点提前生成。
采用 B=(0,0)、A=(-a,0)、C=(b,0)，m=ab/(a-b)。

第一种适用于 a>b>0，免费反向标号后的整个有解域均满足这一条件。

1. Circle(A,B)。
2. Circle(B,C)，取上侧交点 G，并取第二圆与底线除 C 外的交点 E。
3. Ω=Circle(G,E)。
4. 取 Ω 与第二圆除 E 外的交点 Q，画 GQ，与底线交于 M。
5. Circle(M,B)。

令 h²=4a²-b²，可核验

\[
G=\left(-\frac{b^2}{2a},\frac{bh}{2a}\right),\qquad
Q=\left(b-\frac{b^3}{2a^2},\frac{b^2h}{2a^2}\right).
\]

Q 同时位于 Ω 和第二圆，G、Q、M 共线。
Qx-Gx=b(2a-b)(a+b)/(2a²)>0，且 Qx-Ex=b(4a²-b²)/(2a²)>0，
所以支持点和第二交点的选择均合法。此处 Q 就是九笔程序中的共享点 T。
前缀成本为 1 线、4 圆，区别于当前 2 线、3 圆的前缀。

第二种适用于 a>3b/2，是有内部区域的受限路线。

1. Circle(B,A)，与底线除 A 外的交点为 X。
2. ΓC=Circle(C,B)。
3. Ω=Circle(X,C)，取 Ω、ΓC 的上侧交点 U。
4. Circle(U,C)，与底线除 C 外的交点为 M。
5. Circle(M,B)。

此时 X=(a,0)，且

\[
U_x=\frac{b(2a-b)}{2(a-b)},\qquad
U_y^2=\frac{b^2(2a-3b)(2a-b)}{4(a-b)^2}>0.
\]

U 满足两只定义圆的方程，2Ux-b=m，所以第 4 笔确实生成 M。
此五笔全部是圆。a>3b/2 是本路线的辅助条件，原问题在其补集仍可能有解。

[audit_early_loci.py](../experiments/audit_early_loci.py) 验证以上 11 项一般参数恒等式，
并用原 `OriginalReplay` 的 QQ/AA 自动交点闭包重放两份筛查报告。
30 条前缀记录包含镜像、跨组重复，合计 **102 个固定实例**均通过，
其中 46 个第一载体为标准 M 圆，56 个为标准 N 圆。
每例恰执行五次动作，两个观察目标均位于第一载体上，目标点尚未成为交点。
精确报告为 [early-loci-exact-audit.json](../experiments/results/early-loci-exact-audit.json)。

### 两条新前缀的无见证限制收尾预筛

给 [search_eight_suffix.py](../experiments/search_eight_suffix.py) 增加 `--prefix`
与 `--region` 可选参数，默认行为保持原前缀及原夹具。
对上述两种前缀分别允许任意第 6、7 笔，再过滤实际第 8 笔目标载体。
这一阶段允许第 7 笔同时提供最后载体的两个新支持点，也允许非对称末载体，
仍受有限样本、浮点容差和交点绑定限制。

| 前缀 / 组 | 上限 | 第 6 笔观察 | 第 7 笔观察 | 结果 / 重启第 6 笔索引 |
|---|---:|---:|---:|---|
| circle-secant / chamber | 120 秒 | 137 | 143323 | 未命中，172 |
| reflected-circles / chamber | 120 秒 | 158 | 158982 | 未命中，202 |

报告为 `eight-circle-secant-chamber-0.json`、`eight-reflected-circles-chamber-0.json`。
两段均未遍历到末尾，重复索引对应的未完成尾部需要整体重做。
这些计数为实际观察次数，不声明互异程序数量或完整排除。

### 复现与停止边界

在仓库根目录执行，以下为本轮主要入口，其他组的选项及预算见上表。

```powershell
$researchSage = 'sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528'
docker run --rm --network none -e PYTHONDONTWRITEBYTECODE=1 `
  -v "${PWD}:/workspace" -w /workspace $researchSage `
  sage -python experiments/search_simultaneous_centers.py --region chamber --seconds 90 `
  --output experiments/results/simultaneous-centers-chamber-0.json
docker run --rm --network none -e PYTHONDONTWRITEBYTECODE=1 `
  -v "${PWD}:/workspace" -w /workspace $researchSage `
  sage -python experiments/search_early_locus.py --region chamber --seconds 120 `
  --tail-seconds 4 --max-loci 24 --output experiments/results/early-locus-chamber-0.json
docker run --rm --network none -e PYTHONDONTWRITEBYTECODE=1 `
  -v "${PWD}:/workspace" -w /workspace $researchSage `
  sage -python experiments/search_eight_suffix.py --prefix circle-secant --region chamber `
  --first all --seconds 120 --output experiments/results/eight-circle-secant-chamber-0.json
docker run --rm --network none -e PYTHONDONTWRITEBYTECODE=1 `
  -v "${PWD}:/workspace" -w /workspace $researchSage `
  sage -python experiments/audit_early_loci.py experiments/results/early-locus-all-0.json `
  experiments/results/early-locus-chamber-0.json --output experiments/results/early-loci-exact-audit.json
```

为保持精确审计的输入摘要可追溯，续跑结果使用新文件名，保留本轮已有报告。
本轮按上述预算停止，没有候选需要进入完整八笔精确重放或覆盖证明。
26 项研究回归测试通过，包含 7 项新过滤、适用域与前缀控制。
已完成的三圆同时定心筛查保留复用，后续优先依据新的结构线索决定是否续跑。
