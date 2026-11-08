# 研究脚本

已有 [verify_existence.sage.py](verify_existence.sage.py)，用 SageMath 核验存在性公式、距离比、行列式和对称退化，并补充整数夹具检查。复现命令与证明见 [EXISTENCE](../docs/EXISTENCE.md)。其余实验按以下前缀组织：

原作图验证入口为 [verify-original.ps1](verify-original.ps1)。它调用 [verify_original_symbolic.py](verify_original_symbolic.py) 和 [replay_original.py](replay_original.py)，使用 [exact_geometry.py](exact_geometry.py) 的精确 AA 几何；完成恒等式核验、交点闭包重放、依赖与 E 台账、异常分类和回归测试，详见 [BASELINE](../docs/BASELINE.md)。

当前改进的验证入口为 [verify-nine.ps1](verify-nine.ps1)，调用 [verify_nine_symbolic.py](verify_nine_symbolic.py) 与 [replay_nine.py](replay_nine.py)，认证整个有解域上的最坏 9 E。[search_shared_centers.py](search_shared_centers.py) 和 [search_three_circle_prefix.py](search_three_circle_prefix.py) 是发现候选的数值筛查，范围与结果见 [SEARCH_LOG](../docs/SEARCH_LOG.md)，不承担证明责任。

第二轮验证入口为 [verify-refined.ps1](verify-refined.ps1)，调用 [verify_refined_symbolic.py](verify_refined_symbolic.py) 与 [replay_refined.py](replay_refined.py)，认证 7 E / 2 E 条件族并保留原 9 E 回退。新增 [search_eight_suffix.py](search_eight_suffix.py)、[search_eight_joint.py](search_eight_joint.py) 与两圆前缀模式尝试一般 8 E；零结果只按声明形状解释。

一般六笔下界的入口为 [verify-lower-bound.ps1](verify-lower-bound.ps1)，调用 [verify_short_carrier_obstruction.py](verify_short_carrier_obstruction.py)。完整分类与一般参数证明见 [LOWER_BOUND](../docs/LOWER_BOUND.md)，不是由先前搜索零结果推断。

[verify_projectivity_symbolic.py](verify_projectivity_symbolic.py) 核验 20 项反演、第三轨迹和射影固定点恒等式。第三轮筛查为 `search_dynamic_prefix.py`、`search_output_first.py`、`search_alternative_locus.py`、`search_four_line_core.py` 及两个判别式脚本；预算、已完成范围和恢复索引均在 [SEARCH_LOG](../docs/SEARCH_LOG.md)。

| 前缀 | 用途 |
|---|---|
| `verify_` | 存在性、恒等式、目标关系的精确核验 |
| `replay_` | 原构造和优化构造的合法重放与自动 E 计分 |
| `audit_` | 依赖、覆盖、别名、重复绘制与免费交点审计 |
| `search_` / `scan_` | 边界明确的局部搜索与参数扫描 |

存在性、原构造受限域重放与首轮 9 E 改进已完成。每个脚本说明输入、假设、运行命令、输出位置、证据等级和未覆盖情形。结果存入 [results](results/README.md)。
