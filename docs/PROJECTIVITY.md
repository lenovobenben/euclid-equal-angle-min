# 反演与射影变换：另一个构造入口

本页是结构分析，不提供新的 E 步程序。通用上界仍为 9 E。

## 双割线模块就是反演

设一个轴心圆的圆心为 d、半径为 r，G、H 是关于输入轴镜像的圆上点。从轴点 t 连接 H，取第二圆交点 K，再连接 KG，得到的轴交点恰为

\[
s=d+\frac{r^2}{t-d}.
\]

这是 t 关于该圆的反演像。一般恒等式已核验；真正作图还须排除重合点、切线和 t=d 等退化。现有九笔方案的左侧 HE、KG 正是反演 E=−b 得到 M；仅仅把两条割线改称反演不会省步。

## 第三条目标轨迹

除了现有的两个距离比圆，两个目标还位于

\[
(a-c)(x^2+y^2)-2a(b+c)x+ab(b+c)=0.
\]

a≠c 时，其圆心与半径平方为

\[
s=\frac{a(b+c)}{a-c},\qquad r_s^2=s(s-b)>0.
\]

它的反演在输入轴上交换 A↔D、B↔C。a=c 时轨迹退化为 x=b/2，与已知等外段分支一致。这提供了替代最终第二圆的方向，但 s 和合法半径端点目前没有更廉价的通用构造。

## 三次相继对应的射影变换

唯一将 A→B、B→C、C→D 的实 Möbius 变换为

\[
f(z)=\frac{b^2(b+c)(z+a)}{ab(b+c)-(ac-b^2)z}.
\]

其固定点方程为

\[
(ac-b^2)z^2-b(a-b)(b+c)z+ab^2(b+c)=0.
\]

判别式是 −b²(a+b)(b+c)Δ，所以 Δ>0 时两个复固定点恰为 x₀±iy₀，即原问题的镜像目标。它们并不是两个实射影直线上的点；这里使用复坐标表示平面点。

设 Jₘ 是现有第一目标圆的反演，Jₛ 是第三轨迹圆的反演。两次反演合成为保向 Möbius 变换，且 f=Jₛ∘Jₘ。现有两个目标圆的反演则满足 Jₙ∘Jₘ=f²。

对应矩阵

\[
\begin{pmatrix}
b^2(b+c)&ab^2(b+c)\\
-(ac-b^2)&ab(b+c)
\end{pmatrix}
\]

的行列式为 ab²c(a+b)(b+c)>0，且

\[
\frac{\operatorname{tr}^2}{4\det}
=\frac{(a+b)(b+c)}{4ac}=\cos^2\theta.
\]

这把存在条件解释为该变换具有一对非实固定点，并把原来的角度参数联系到矩阵不变量。固定点公式及反演是分析工具，不能作为免费的复合尺规操作。下一步若采用此路线，必须给出各辅助点如何成为合法交点和完整分支成本。

## 核验

[verify_projectivity_symbolic.py](../experiments/verify_projectivity_symbolic.py) 使用 SageMath 验证 20 项恒等式，结果为 [projectivity-symbolic.json](../experiments/results/projectivity-symbolic.json)。前三个输入对应、复合、固定点方程、判别式、第三轨迹、矩阵不变量及双割线反演均已独立代入核验。

复现时将脚本复制到已有 `sage` 容器，执行 `sage -python verify_projectivity_symbolic.py --output projectivity-symbolic.json`。上述恒等式含非零分母假设；特别是第三圆在 a=c 时要使用单独的直线分支。
