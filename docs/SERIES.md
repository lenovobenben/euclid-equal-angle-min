# Euclid 尺规作图优化系列：文档约定与四项目对照

## 1. 对照范围与结论

四个项目的基础 E 规则、精确验证观念与双许可证已经一致。
主要差异来自文档入口、章节顺序、复现环境和题目专属内容，而不是基础计费冲突。
本次以 Euclid-Min 和 Euclid-CCC-Min 为只读参照，仅整理两个新项目。

参照快照：Euclid-Min `0c4a351`、Euclid-CCC-Min `3598216`；
新项目整理前快照：Euclid-Equal-Angle-Min `c154fcf`、Euclid-Castillon-Min `344720a`。
下表中的成绩用于定位各题的范围，不能跨题直接排名。

| 维度 | Euclid-Min | Euclid-CCC-Min | Euclid-Equal-Angle-Min | Euclid-Castillon-Min |
|---|---|---|---|---|
| 题目 | 正十七边形相邻顶点 | 阿波罗尼乌斯三圆相切 | 共线四点等视角 | 指定三点约束的圆内接三角形 |
| 免费输入 | 圆、圆心、指定圆周点 | 三个圆及圆心 | 四个有序共线点及直线 | 圆、圆心、三个圆外/内输入点 |
| 当前主要上界 | 固定配置 12 E | 外切 18 E；八解 gen 49 / rob 55 E | 单解、双解 gen / rob 均 9 E | 完整单解 gen 14 E；双解 gen 17 E |
| 下界/最小性 | 未证明 12 E 全局最小 | 未证明所列上界全局最小 | 一般下界 6 E，不覆盖每个特殊比例 | 尚无全局最小性证明 |
| 验证组织 | Sage 包、Schema、证书、独立核验 | 独立研究脚本、精确重放、一般参数关系 | Sage 精确重放、覆盖证明、完备分类下界 | 标准库内核、独立 Sage 重放与一般参数关系 |
| 数据目录 | qq-ggb、proofs 等历史分层 | experiments/results | experiments/results | experiments/results |
| 题目专属文档 | METRICS、FORMAL_MODEL、证书格式等 | MANNHEIM、GERGONNE、SHARED_INVERSION | EXISTENCE、NINE、LOWER_BOUND、REFINEMENTS | CONSTRUCTION、CLASSIFICATION、SEARCH |
| 来源材料 | QQ 提供的 GGB，原作者未确认 | 历史构造及文献台账 | 原始问答快照、比赛题出处 | 经典不动点轴路线及文献台账 |
| 展示 | Manim、离线网页、GeoGebra | Manim 动画 | 静态 SVG；Manim 待补 | Manim 待补 |
| 软件/内容许可 | Apache 2.0 / CC BY 4.0 | Apache 2.0 / CC BY 4.0 | 相同，保留来源快照权利 | 相同，保留第三方材料权利 |

## 2. 本次对齐的具体差异

| 项目 | 整理前差异 | 两个新项目采用的约定 |
|---|---|---|
| 标题与语言入口 | 等视角标题缺少题目副标题，语言切换形式各异 | `Euclid-…-Min · 题目短名`；中文主 README、英文镜像 |
| 章节结构 | Castillon 中文先计费后成绩，英文把来源/研究/目录合并；等视角章节缺少对应关系 | 统一八个主章节，中英文逐节对应 |
| 成绩呈现 | 条件族、下界与主上界混在同一张结果表 | 首先列当前主上界；随后单列下界和条件族，保留 gen / rob 标签 |
| 系列导航 | 等视角只列三个项目，Castillon 只引用早期两题 | 两个首页均列齐四项目，不依赖“第几个项目”的编号作导航 |
| 复现环境 | 等视角首页要求 PowerShell、latest 镜像与常驻容器 | 首页提供固定 Sage 10.7 镜像、只读挂载、断网命令；Windows 原入口继续可用 |
| 引用元数据 | 仅 Euclid-Min 有 CITATION.cff | 两个新项目补齐 CITATION.cff；旧项目不补改 |
| 许可证说明 | 正文相同，但范围说明详略不同 | 新项目用共同范围结构，保留题目专属第三方来源条款 |
| 子目录入口 | 等视角有实验/结果/测试 README，Castillon 缺少 | 新项目均提供脚本、结果和测试入口及独立复现说明 |

## 3. README 的共同骨架

开头依次放置：项目名称、语言切换、具体成果一句话、题目范围及证据限制、关键入口。
确有演示才展示演示；尚未制作动画时直说后续补充，不伪造预览或空链接。

| 中文主章节 | 英文对应章节 |
|---|---|
| 当前已验证上界 | Current verified upper bounds |
| E 步：唯一采用的计数法 | What counts as an E move |
| 来源与项目贡献 | Sources and project contribution |
| 精确验证 | Exact verification |
| 复现 | Reproduction |
| 当前研究方向 | Current research directions |
| 文档与代码入口 | Documentation and code |
| 许可与引用 | License and citation |

免费输入、有解域、条件族和下界可以作为对应章节的子节。
英文首页应与中文首页在成绩、目标、覆盖、限制、来源和运行条件上保持等价，
不要求把全部中文研究文档翻译为英文。

## 4. 术语和证据口径

- E 步 / E move：实际合法画线与画圆次数；交点和命名免费，重复实际绘制仍计费。
- 塌圆规 / collapsing compass：圆心必须是半径两端点之一，禁止直接搬运异地长度。
- 一般位置 gen / generic：对应研究域中明确的相对开稠密、满测度子域。
- 完整域 rob / full-domain robust：全部有解输入，含分支判断、失败尝试和退化修复的最坏实际成本。
- 上界 / upper bound、下界 / lower bound、最小性 / minimality 不混用。
- restricted 构造和特殊条件族明确列域，不代替通用成绩。
- 原文线索、浮点候选、固定实例、一般恒等式、覆盖证明、完备下界分别报告。
- 免费初始对象、目标条件、规则版本或覆盖域不同，分数不能直接比较。

## 5. 目录与许可

共同入口为 README.md、README.en.md、LICENSE、LICENSE-CONTENT、LICENSE-SCOPE.md；
新项目补 CITATION.cff。docs/DESIGN.md、ROADMAP.md、LITERATURE.md 分别承担题目语义、
研究安排和来源。experiments 保存独立脚本，experiments/results 保存报告，tests 保存回归。

profiles、schemas、sources、sage、qq-ggb、proofs 等按题目需要保留，不为外观一致而空建或搬动。
文件名 NINE、MANNHEIM、CLASSIFICATION 等表达不同数学内容，应保留各自职责。

软件与配置 Apache 2.0，原创数学文档、证书、数据和引用元数据 CC BY 4.0。
第三方原文、图片、论文或输入材料保持其自身权利；不因目录调整而重新授权。

## 6. 复现和展示

首页给最短可运行核验入口，docs/REPRODUCING.md 记录完整命令、预期输出和报告再生成。
需要 Sage 时，默认使用固定 10.7 Docker 镜像；已有镜像后，核验断网、只读挂载。
仅需标准库的检查不额外要求 Sage；Windows PowerShell 入口可以作为兼容路径保留。
文档应说明哪些操作打印到终端、哪些会更新报告，不隐含覆盖既有容器或来源快照。

未来 Manim 的颜色角色沿用早期项目：免费输入洋红、当前动作金色、既有辅助对象淡蓝、目标绿色。
每笔展示已有定位点和累计 E，轨迹来自精确重放；显示中的近似坐标不承担数学证明。

## 7. 旧项目只读与长期维护

本次不修改 Euclid-Min 或 Euclid-CCC-Min 的文件、提交、分支和许可证。
旧项目保留历史布局、成熟演示和原有章节；两者本来就不完全同构，因此不追求逐文件复制。
例如 CCC 当前没有 CITATION.cff，不在此次范围内补齐；两个新项目按共同约定向前整理。

系列后续新增题目时优先复制上述信息架构，再写清自己的输入、目标和证据范围。
同步共同说明时只更新两个新项目的同名文档，不让个别题目的研究结果变成通用系列规则。
