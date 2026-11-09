param(
    [ValidateSet('Preview', 'Final')]
    [string]$Quality = 'Preview'
)

$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$sageImage = 'sagemath/sagemath@sha256:4f5589eb6c565949a006f8665de2876b8414410daf5ac554f4434a15d4f3d528'
$manimImage = 'euclid-min-manim:0.21.0'

function Assert-Exit([string]$Action) {
    if ($LASTEXITCODE -ne 0) { throw "$Action failed (exit $LASTEXITCODE)." }
}

Get-Command docker, ffmpeg -ErrorAction Stop | Out-Null
Push-Location $projectRoot
try {
    docker image inspect $manimImage *> $null
    if ($LASTEXITCODE -ne 0) {
        docker build -t $manimImage animations/e9
        Assert-Exit 'Build Manim image with Chinese fonts'
    }
    docker run --rm --network none -e PYTHONDONTWRITEBYTECODE=1 `
        -v "${projectRoot}:/workspace" -w /workspace $sageImage `
        sage -python animations/e9/export_geometry.py
    Assert-Exit 'Export exact geometry'

    $resolution = if ($Quality -eq 'Final') { '3840,2160' } else { '1280,720' }
    $height = if ($Quality -eq 'Final') { '2160' } else { '720' }
    $suffix = if ($Quality -eq 'Final') { '4k60' } else { '720p60' }
    docker run --rm --network none -e PYTHONDONTWRITEBYTECODE=1 `
        -v "${projectRoot}:/manim" -w /manim $manimImage `
        manim --config_file animations/e9/manim.cfg -r $resolution --fps 60 `
        animations/e9/e9_progress.py E9EqualAngle
    Assert-Exit 'Render Manim scene'

    $master = Join-Path $PSScriptRoot "media/videos/e9_progress/${height}p60/E9EqualAngle.mp4"
    $output = Join-Path $PSScriptRoot "media/E9EqualAngle_${suffix}.mp4"
    ffmpeg -y -i $master -vf fps=60 -c:v libx264 -preset fast -crf 18 `
        -maxrate 24M -bufsize 48M -g 120 -keyint_min 120 -sc_threshold 0 `
        -bf 2 -refs 2 -pix_fmt yuv420p -fps_mode cfr -movflags +faststart -an $output
    Assert-Exit 'Encode playback copy'
    Write-Output "Animation saved to $output"
}
finally {
    Pop-Location
}
