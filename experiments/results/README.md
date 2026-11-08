# 实验结果

已有 [existence-verification.json](existence-verification.json)，记录 SageMath 10.7 的 8 项一般参数恒等式与 3375 个整数夹具核验结果。运行命令为从仓库根目录执行 `Get-Content -Raw experiments/verify_existence.sage.py | docker exec -i sage sage -python`；输入范围与一般参数证明见 [EXISTENCE](../../docs/EXISTENCE.md)。

原作图结果为 [original-symbolic-verification.json](original-symbolic-verification.json) 与 [original-replay.json](original-replay.json)，包含 12 个一般参数恒等式、12 个分类夹具、完整交点见证和 E 计分。复现 `pwsh -NoProfile -File experiments/verify-original.ps1`，覆盖证明见 [BASELINE](../../docs/BASELINE.md)。10 E 属于 D_original 的受限域上界，不是整个 D 的上界。当前没有搜索成绩。

记录至少包括脚本与版本、命令、输入或夹具、规则与目标、覆盖范围、候选预算、终止状态、实际结果及限制。未完成的实验明确标为未完成；零命中不得写成全局下界。
