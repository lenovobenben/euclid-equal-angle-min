# 来源与参考

## 1. 两篇直接来源

两篇均来自 lenovobenben/ai-math-notes 的 `chatgpt/经典数学题100例-4/`。本次从本地检出复制原文，提交版本为 `50cccad292a296087770a377080dcde9ef40657b`；GitHub 搜索定位到的版本与之相同。

| 编号 | 标题与会话 ID | 本地快照 | 用途 |
|---|---|---|---|
| S1 | 直线外点条件；`6932188d-7dd8-8332-89cc-72d43e41c0df` | [原文](../sources/existence-original.md) | 存在性问题及候选条件 |
| S2 | 尺规作图证明；`694a80c9-aac4-8328-b8b4-38d7635da26e` | [原文](../sources/construction-original.md) | 四阶段构造与待订正的原证明 |

- [S1 固定版本](https://github.com/lenovobenben/ai-math-notes/blob/50cccad292a296087770a377080dcde9ef40657b/chatgpt/经典数学题100例-4/001_直线外点条件__6932188d-7dd8-8332-89cc-72d43e41c0df/001_直线外点条件__6932188d-7dd8-8332-89cc-72d43e41c0df.md)
- [S2 固定版本](https://github.com/lenovobenben/ai-math-notes/blob/50cccad292a296087770a377080dcde9ef40657b/chatgpt/经典数学题100例-4/001_尺规作图证明__694a80c9-aac4-8328-b8b4-38d7635da26e/001_尺规作图证明__694a80c9-aac4-8328-b8b4-38d7635da26e.md)

归档日期为 2026-11-09，逐文件 SHA-256 与仓库路径见 [manifest.json](../sources/manifest.json)。原文中的回答是研究线索，不自动成为可靠定理或已验证程序。

## 2. 项目结构参考

Euclid-CCC-Min，固定参考提交 [3598216](https://github.com/lenovobenben/euclid-ccc-min/tree/35982169e4e4c7e2004d3d03305188d426cb79d5)。

沿用文档、实验、测试和动画分层，以及一般位置 / 全域覆盖、精确重放和上界 / 下界分开记录的方法。不复制其三圆参数、目标或现有研究成绩。

## 3. 基础规则

Euclid-Min 的 E 步计分与正式操作模型，固定提交 `792619b38d749643bc9d80da8110dc9cff5b4877`，规范链接见 [DESIGN](DESIGN.md)。系列共有的工具语义保持一致，题目专属输入与目标独立定义。

## 4. 比赛题来源

本题见于 **1994 年第 17 届奥地利—波兰数学竞赛第 9 题（团体赛第 3 题）**。原题的条件是 (a+b)(b+c)<4ac，与本项目 Δ>0 完全等价，要求在每侧唯一地尺规构造等角点。

- [1994 官方题单的 IMOmath 存档](https://imomath.com/othercomp/Apo/ApoMC94.pdf)，第 2 页第 9 题。
- [Crux Mathematicorum 24 卷第 1 期](https://cms.math.ca/wp-content/uploads/crux-pdfs/CRUXv24n1.pdf)，1998 年印刷页 6 收录同题。

本轮检索确认了题目来源，尚未获得可按本项目塌圆规模型展开并优于九笔的文献解答。不能据此声称本项目九笔是文献最短或世界纪录。原始项目快照与清单保持不变。
