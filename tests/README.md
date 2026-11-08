# 验证测试

已有 [test_original_replay.py](test_original_replay.py)，9 项测试覆盖精确几何控制、目标不注入、非法动作、重复绘制计费、正常重放、异常限制与无解输入。测试依赖 SageMath，使用 `pwsh -NoProfile -File experiments/verify-original.ps1` 统一复现。

保留这些已知合法程序和命中作为后续搜索的阳性校准。一般参数正确性与覆盖另由 [BASELINE](../docs/BASELINE.md) 证明，有限测试不承担全域证明责任。
