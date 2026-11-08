param(
    [string]$Container = 'sage'
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$containerRoot = '/tmp/euclid-equal-angle-min-baseline'

function Assert-DockerExit([string]$Action) {
    if ($LASTEXITCODE -ne 0) { throw "$Action failed (exit $LASTEXITCODE)." }
}

docker exec $Container mkdir -p "$containerRoot/experiments" "$containerRoot/tests"
Assert-DockerExit 'Create task directory'
foreach ($name in @('exact_geometry.py', 'replay_original.py', 'verify_original_symbolic.py')) {
    docker cp (Join-Path $PSScriptRoot $name) "${Container}:$containerRoot/experiments/$name"
    Assert-DockerExit "Copy $name"
}
foreach ($name in @('__init__.py', 'test_original_replay.py')) {
    docker cp (Join-Path $projectRoot "tests/$name") "${Container}:$containerRoot/tests/$name"
    Assert-DockerExit "Copy $name"
}

$symbolicLines = docker exec $Container sage -python "$containerRoot/experiments/verify_original_symbolic.py"
Assert-DockerExit 'General-parameter symbolic identities'
$symbolicText = $symbolicLines -join "`n"
$null = $symbolicText | ConvertFrom-Json
$symbolicText | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'results/original-symbolic-verification.json') -Encoding utf8
Write-Output $symbolicText

docker exec $Container sage -python "$containerRoot/experiments/replay_original.py" --output "$containerRoot/original-replay.json"
Assert-DockerExit 'Exact construction replay'
docker cp "${Container}:$containerRoot/original-replay.json" (Join-Path $PSScriptRoot 'results/original-replay.json')
Assert-DockerExit 'Copy replay report'

docker exec $Container sage -python -m unittest discover -s "$containerRoot/tests" -v
Assert-DockerExit 'Exact replay regression tests'
