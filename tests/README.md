# 验证测试

已有 [test_original_replay.py](test_original_replay.py)，9 项测试覆盖精确几何控制、目标不注入、非法动作、重复绘制计费、正常重放、异常限制与无解输入。测试依赖 SageMath，使用 `pwsh -NoProfile -File experiments/verify-original.ps1` 统一复现。

[test_nine_replay.py](test_nine_replay.py) 新增 5 项测试，核验反向标号后的原目标、共享平行方向、旧限制输入、一般相等间距分支、有理数输入及数值筛查阳性控制。`pwsh -NoProfile -File experiments/verify-nine.ps1` 运行全部 14 项测试。

[test_refined_replay.py](test_refined_replay.py) 再增加 5 项，核验直接两圆、两种七笔分支、原目标映射、九笔回退及黄金比实代数数参数。`pwsh -NoProfile -File experiments/verify-refined.ps1` 运行全部 19 项测试。

保留这些已知合法程序和命中作为后续搜索的阳性校准。一般参数正确性与覆盖另由 [BASELINE](../docs/BASELINE.md) 和 [NINE](../docs/NINE.md) 证明，有限测试不承担全域证明责任。
