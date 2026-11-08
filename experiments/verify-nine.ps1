param([string]$Container = 'sage')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$containerRoot = '/tmp/euclid-equal-angle-min-nine'
function Assert-DockerExit([string]$Action) {
    if ($LASTEXITCODE -ne 0) { throw "$Action failed (exit $LASTEXITCODE)." }
}
docker exec $Container mkdir -p "$containerRoot/experiments" "$containerRoot/tests"
Assert-DockerExit 'Create task directory'
foreach ($name in @('exact_geometry.py','replay_original.py','replay_nine.py','verify_nine_symbolic.py','search_shared_centers.py')) {
    docker cp (Join-Path $PSScriptRoot $name) "${Container}:$containerRoot/experiments/$name"
    Assert-DockerExit "Copy $name"
}
foreach ($name in @('__init__.py','test_original_replay.py','test_nine_replay.py')) {
    docker cp (Join-Path $projectRoot "tests/$name") "${Container}:$containerRoot/tests/$name"
    Assert-DockerExit "Copy $name"
}
$symbolic = docker exec $Container sage -python "$containerRoot/experiments/verify_nine_symbolic.py"
Assert-DockerExit '9 E symbolic identities'
$null = ($symbolic -join "`n") | ConvertFrom-Json
$symbolic | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'results/nine-symbolic-verification.json') -Encoding utf8
Write-Output $symbolic
docker exec $Container sage -python "$containerRoot/experiments/replay_nine.py" --output "$containerRoot/nine-replay.json"
Assert-DockerExit '9 E exact replay'
docker cp "${Container}:$containerRoot/nine-replay.json" (Join-Path $PSScriptRoot 'results/nine-replay.json')
Assert-DockerExit 'Copy replay report'
docker exec $Container sage -python -m unittest discover -s "$containerRoot/tests" -v
Assert-DockerExit 'Original and optimized regression tests'
