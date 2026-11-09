# 实验结果

跨平台固定 Docker 复现与原有 Windows PowerShell 兼容入口见 [REPRODUCING](../../docs/REPRODUCING.md)。下文已有 PowerShell 命令继续保留为兼容路径。

已有 [existence-verification.json](existence-verification.json)，记录 SageMath 10.7 的 8 项一般参数恒等式与 3375 个整数夹具核验结果。运行命令为从仓库根目录执行 `Get-Content -Raw experiments/verify_existence.sage.py | docker exec -i sage sage -python`；输入范围与一般参数证明见 [EXISTENCE](../../docs/EXISTENCE.md)。

原作图结果为 [original-symbolic-verification.json](original-symbolic-verification.json) 与 [original-replay.json](original-replay.json)，包含 12 个一般参数恒等式、12 个分类夹具、完整交点见证和 E 计分。复现 `pwsh -NoProfile -File experiments/verify-original.ps1`，覆盖证明见 [BASELINE](../../docs/BASELINE.md)。10 E 属于 D_original 的受限域上界，不是整个 D 的上界。

当前改进为 [nine-symbolic-verification.json](nine-symbolic-verification.json) 和 [nine-replay.json](nine-replay.json)，一般 9 E 与特殊 8 E 分支覆盖全部有解输入。复现 `pwsh -NoProfile -File experiments/verify-nine.ps1`，证明见 [NINE](../../docs/NINE.md)。

三个 `*-screen.json` 保存首轮有界数值筛查，其中三圆前缀扩展找到 9 E 候选；结果认证由上面的精确核验独立完成。候选范围、跳过分支、计数含义及停止条件见 [SEARCH_LOG](../../docs/SEARCH_LOG.md)。

第二轮 [refined-symbolic-verification.json](refined-symbolic-verification.json) 与 [refined-replay.json](refined-replay.json) 认证 7 E / 2 E 条件族，一般上界仍是 9 E。[REFINEMENTS](../../docs/REFINEMENTS.md) 解释证明、适用域和两笔下界。

`eight-*.json` 保存一般 8 E 的有界筛查与重启分段；`equal-outer-screen.json`、`equal-neighbor-screen.json` 是条件族筛查的阳性结果。实际参数优先读各报告的 `normalized_lengths` 字段。所有数值筛查的范围与未覆盖分支均在研究日志中说明，不构成全局下界。

记录至少包括脚本与版本、命令、输入或夹具、规则与目标、覆盖范围、候选预算、终止状态、实际结果及限制。未完成的实验明确标为未完成；零命中不得写成全局下界。

[short-carrier-obstruction.json](short-carrier-obstruction.json) 是一般六笔下界的有限精确符号部分：192 种种子、3600 项域检查、1680 项圆心余式检查、840 项 k 单位检查。其完整性与推论见 [LOWER_BOUND](../../docs/LOWER_BOUND.md)，复现 `experiments/verify-lower-bound.ps1`。

[projectivity-symbolic.json](projectivity-symbolic.json) 保存 20 项结构恒等式。`dynamic-*.json`、`output-first-*.json`、`alternative-locus-*.json`、`four-line-*.json`、`four-core-*.json` 及两个 `*field*` / `*discriminant*` 筛查保留第三轮的范围限定结果；零命中不承担六笔下界的证明责任。
