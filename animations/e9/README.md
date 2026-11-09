# 九笔等视角双解动画

`E9EqualAngle` 演示 [九笔共享辅助圆构造](../../docs/NINE.md) 的一般分支，
从免费输入 A、B、C、D 及完整直线 l 出发，实际执行 **4 线 + 5 圆 = 9 E**，
最终两圆的交点 P、P′ 同时成为可用目标。

[观看或下载 4K60 成片](https://raw.githubusercontent.com/lenovobenben/euclid-equal-angle-min/main/animations/e9/media/E9EqualAngle_4k60.mp4)，3840 × 2160，60 fps，51.7 秒。

沿用 [Euclid-CCC-Min](https://github.com/lenovobenben/euclid-ccc-min/tree/main/animations)
的深蓝背景、中文字体、洋红输入、金色当前落笔、蓝色辅助对象、绿色目标，
以及细线、小点、定义点空心环、临时半径、整数计数器和移动镜头尺寸补偿。
场景独立存放于本仓库，可单独渲染。

## 几何与声明范围

演示夹具为 `AB=3、BC=1、CD=5/2`，坐标使用 `B=(0,0)`，无需反向标号。
三个间距互不相等，也不满足已认证的两个两笔乘积条件。
本例 Δ=16，两个目标均在第 9 E 首次出现。

`export_geometry.py` 调用正式 `NineReplay`，用 SageMath QQ/AA 执行全部
交点闭包、定义点可用性和目标检查，再将显示坐标转换为浮点数。
导出文件保存交点见证、首次可用时刻、逐笔依赖、精确输入和轨迹摘要。
Manim 只读取 `geometry.json`，并检查摘要、E 台账和定位点的镜头安全区。

整个有解域上的 9 E 上界由 [NINE](../../docs/NINE.md) 的重新标号、九笔分支与
相等间距分支共同保证。此片只播放九笔分支。当前一般下界为 6 E，
九笔最短性尚未证明。末尾连线与角弧单独标注为结果示意，计数器保持 9 E。

## 渲染

需要 Docker、PowerShell 7 和 FFmpeg。已有 Euclid-CCC-Min 的
`euclid-min-manim:0.21.0` 镜像可直接复用，缺少时脚本使用本目录 Dockerfile 构建。
SageMath 使用项目固定镜像，Manim 基础镜像与参考项目相同。

在仓库根目录运行 720p60 预览或 4K60 成片。

```powershell
pwsh -NoProfile -File animations/e9/render.ps1
pwsh -NoProfile -File animations/e9/render.ps1 -Quality Final
```

播放文件分别生成到 `media/E9EqualAngle_720p60.mp4` 和
`media/E9EqualAngle_4k60.mp4`。FFmpeg 输出恒定 60 fps、两秒关键帧间隔，
并将 MP4 索引前置。4K60 播放版、预览图、源码和几何导出纳入版本管理，
中间渲染、缓存及本地 720p60 预览由忽略规则排除。

镜头回归检查覆盖每步定位点、最终两圆的完整视野及可见直线裁剪。

```powershell
docker run --rm --network none -e PYTHONDONTWRITEBYTECODE=1 `
  -v "${PWD}:/manim" -w /manim euclid-min-manim:0.21.0 `
  python -m unittest discover -s animations/e9 -p 'test_*.py' -v
```

单独重新导出精确数据可运行以下命令。

```powershell
docker run --rm --network none -e PYTHONDONTWRITEBYTECODE=1 `
  -v "${PWD}:/workspace" -w /workspace `
  sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528 `
  sage -python animations/e9/export_geometry.py
```

## 许可

程序与配置采用 [Apache 2.0](../../LICENSE)。分镜、几何数据及动画采用
[CC BY 4.0](../../LICENSE-CONTENT)，署名 lenovobenben，Euclid-Equal-Angle-Min。
视觉实现参照同作者 Euclid-CCC-Min 的 Apache 2.0 动画源码，并针对本题改编。
