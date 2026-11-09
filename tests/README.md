# 验证测试

跨平台固定 Docker 复现与原有 Windows PowerShell 兼容入口见 [REPRODUCING](../docs/REPRODUCING.md)。下文已有 PowerShell 命令继续保留为兼容路径。

已有 [test_original_replay.py](test_original_replay.py)，9 项测试覆盖精确几何控制、目标不注入、非法动作、重复绘制计费、正常重放、异常限制与无解输入。测试依赖 SageMath，使用 `pwsh -NoProfile -File experiments/verify-original.ps1` 统一复现。

[test_nine_replay.py](test_nine_replay.py) 新增 5 项测试，核验反向标号后的原目标、共享平行方向、旧限制输入、一般相等间距分支、有理数输入及数值筛查阳性控制。`pwsh -NoProfile -File experiments/verify-nine.ps1` 运行全部 14 项测试。

[test_refined_replay.py](test_refined_replay.py) 再增加 5 项，核验直接两圆、两种七笔分支、原目标映射、九笔回退及黄金比实代数数参数。`pwsh -NoProfile -File experiments/verify-refined.ps1` 运行全部 19 项测试。

[test_eight_search.py](test_eight_search.py) 增加 7 项，核验同时定心见证、轴外圆心、
标量过滤、五笔替代前缀及其适用条件，并重验 11 项参数恒等式。
用项目 SageMath 镜像执行 `sage -python -m unittest discover -s tests -v`，当前共 26 项通过。
这些搜索控制与第一载体核验不提供完整八笔构造或新的全局下界。

保留这些已知合法程序和命中作为后续搜索的阳性校准。一般参数正确性与覆盖另由 [BASELINE](../docs/BASELINE.md) 和 [NINE](../docs/NINE.md) 证明，有限测试不承担全域证明责任。
