# 复现与报告再生成

## 1. 环境与固定版本

从项目根目录执行。精确核验需要 SageMath 10.7；数值筛查及相应回归用到 NumPy。
默认使用固定镜像 `sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528`，已有镜像后，以下命令断网、只读挂载且不需要常驻容器。
PowerShell 7 仅是已有 Windows 自动化的一条兼容路径，不是所有平台的必要依赖。

## 2. 九笔通用构造

符号恒等式：

```sh
docker run --rm --network none \
  -v "$PWD:/workspace:ro" -w /workspace \
  -e PYTHONDONTWRITEBYTECODE=1 \
  sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528 \
  sage -python experiments/verify_nine_symbolic.py
```

精确交点重放与分支台账：

```sh
docker run --rm --network none \
  -v "$PWD:/workspace:ro" -w /workspace \
  -e PYTHONDONTWRITEBYTECODE=1 \
  sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528 \
  sage -python experiments/replay_nine.py
```

第一条命令打印 14 项恒等式核验；第二条打印 21 个夹具的分行摘要，包含有解/无解及分支信息。
全域覆盖依赖 [NINE](NINE.md) 的一般参数与分支证明，不能用夹具数量代替。

## 3. 回归测试、条件族与下界

完整 19 项回归测试：

```sh
docker run --rm --network none \
  -v "$PWD:/workspace:ro" -w /workspace \
  -e PYTHONDONTWRITEBYTECODE=1 \
  sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528 \
  sage -python -m unittest discover -s tests -v
```

条件族的符号和精确重放分别把容器内命令换成
`sage -python experiments/verify_refined_symbolic.py` 和
`sage -python experiments/replay_refined.py`。
预期为 10 项恒等式、29 个分类夹具；特殊 7 E / 2 E 不更新通用上界。

六笔一般下界的有限符号部分：

```sh
docker run --rm --network none \
  -v "$PWD:/workspace:ro" -w /workspace \
  -e PYTHONDONTWRITEBYTECODE=1 \
  sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528 \
  sage -python experiments/verify_short_carrier_obstruction.py
```

预期 192 种种子、3,600 项域检查、1,680 项圆心条件与 840 项分母单位检查全部通过。
下界还依赖 [LOWER_BOUND](LOWER_BOUND.md) 中的完备分类与理论论证，不由搜索零结果推出。

存在性核验可将容器内命令换成 `sage -python experiments/verify_existence.sage.py`。

## 4. 再生成报告

普通核验仅打印结果，不修改已提交报告。符号脚本的标准输出可显式重定向到对应
experiments/results JSON；必须先检查进程成功退出，避免把失败输出当作认证结果。

精确重放的完整 JSON 需要 --output，可为生成目录单独提供写入挂载：

```sh
docker run --rm --network none \
  -v "$PWD:/workspace:ro" -v "$PWD/experiments/results:/reports" -w /workspace \
  -e PYTHONDONTWRITEBYTECODE=1 \
  sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528 \
  sage -python experiments/replay_nine.py --output /reports/nine-replay.json
```

原始来源快照不属于生成数据，保持原样。各报告用途见
[experiments/results](../experiments/results/README.md)。

## 5. Windows PowerShell 7 兼容入口

已有脚本继续可用，面向一个已经运行的 Sage 容器：

```powershell
pwsh -NoProfile -File experiments/verify-nine.ps1 -Container sage
pwsh -NoProfile -File experiments/verify-refined.ps1 -Container sage
pwsh -NoProfile -File experiments/verify-lower-bound.ps1 -Container sage
```

它们复制依赖到容器临时目录并把报告写回 experiments/results；-Container 可指定其他已有容器。
需要新建兼容容器时，用上述固定镜像启动 sleep infinity 即可，不要求 latest。
旧日志中的 latest 命令反映当时环境；它可能随时间改变，不是系列新的固定复现入口。

## 6. 证据边界

符号恒等式、固定实例、一般参数、分支覆盖和最小性证明分别报告。
原构造 10 E 只在明确受限域成立；正式结果及规则以 [DESIGN](DESIGN.md) 为准。
数值搜索脚本不替代精确核验，不因有界零命中而产生下界。
