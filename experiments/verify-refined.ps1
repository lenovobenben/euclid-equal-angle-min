param([string]$Container = 'sage')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$containerRoot = '/tmp/euclid-equal-angle-min-refined'
function Assert-DockerExit([string]$Action) {
    if ($LASTEXITCODE -ne 0) { throw "$Action failed (exit $LASTEXITCODE)." }
}
docker exec $Container mkdir -p "$containerRoot/experiments" "$containerRoot/tests"
Assert-DockerExit 'Create task directory'
foreach ($name in @('exact_geometry.py','replay_original.py','replay_nine.py','replay_refined.py','verify_refined_symbolic.py','search_shared_centers.py')) {
    docker cp (Join-Path $PSScriptRoot $name) "${Container}:$containerRoot/experiments/$name"
    Assert-DockerExit "Copy $name"
}
foreach ($name in @('__init__.py','test_original_replay.py','test_nine_replay.py','test_refined_replay.py')) {
    docker cp (Join-Path $projectRoot "tests/$name") "${Container}:$containerRoot/tests/$name"
    Assert-DockerExit "Copy $name"
}
$symbolic = docker exec $Container sage -python "$containerRoot/experiments/verify_refined_symbolic.py"
Assert-DockerExit 'Refined symbolic identities'
$null = ($symbolic -join "`n") | ConvertFrom-Json
$symbolic | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'results/refined-symbolic-verification.json') -Encoding utf8
Write-Output $symbolic
docker exec $Container sage -python "$containerRoot/experiments/replay_refined.py" --output "$containerRoot/refined-replay.json"
Assert-DockerExit 'Conditional exact replay'
docker cp "${Container}:$containerRoot/refined-replay.json" (Join-Path $PSScriptRoot 'results/refined-replay.json')
Assert-DockerExit 'Copy replay report'
docker exec $Container sage -python -m unittest discover -s "$containerRoot/tests" -v
Assert-DockerExit 'All regression tests'
