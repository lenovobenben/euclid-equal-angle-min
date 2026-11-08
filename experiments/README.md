# 研究脚本

已有 [verify_existence.sage.py](verify_existence.sage.py)，用 SageMath 核验存在性公式、距离比、行列式和对称退化，并补充整数夹具检查。复现命令与证明见 [EXISTENCE](../docs/EXISTENCE.md)。其余实验按以下前缀组织：

原作图验证入口为 [verify-original.ps1](verify-original.ps1)。它调用 [verify_original_symbolic.py](verify_original_symbolic.py) 和 [replay_original.py](replay_original.py)，使用 [exact_geometry.py](exact_geometry.py) 的精确 AA 几何；完成恒等式核验、交点闭包重放、依赖与 E 台账、异常分类和回归测试，详见 [BASELINE](../docs/BASELINE.md)。

| 前缀 | 用途 |
|---|---|
| `verify_` | 存在性、恒等式、目标关系的精确核验 |
| `replay_` | 原构造和优化构造的合法重放与自动 E 计分 |
| `audit_` | 依赖、覆盖、别名、重复绘制与免费交点审计 |
| `search_` / `scan_` | 边界明确的局部搜索与参数扫描 |

存在性和原构造受限域重放已完成，尚未开始搜索。每个脚本说明输入、假设、运行命令、输出位置、证据等级和未覆盖情形。结果存入 [results](results/README.md)。
