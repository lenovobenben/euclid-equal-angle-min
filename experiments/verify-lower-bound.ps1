param([string]$Container = 'sage')
$ErrorActionPreference = 'Stop'
$containerRoot = '/tmp/euclid-equal-angle-min-lower-bound'
function Assert-DockerExit([string]$Action) {
    if ($LASTEXITCODE -ne 0) { throw "$Action failed (exit $LASTEXITCODE)." }
}
docker exec $Container mkdir -p $containerRoot
Assert-DockerExit 'Create task directory'
docker cp (Join-Path $PSScriptRoot 'verify_short_carrier_obstruction.py') "${Container}:$containerRoot/verify_short_carrier_obstruction.py"
Assert-DockerExit 'Copy symbolic verifier'
docker exec $Container sage -python "$containerRoot/verify_short_carrier_obstruction.py" --output "$containerRoot/short-carrier-obstruction.json"
Assert-DockerExit 'Verify generic lower-bound obstructions'
docker cp "${Container}:$containerRoot/short-carrier-obstruction.json" (Join-Path $PSScriptRoot 'results/short-carrier-obstruction.json')
Assert-DockerExit 'Copy verification report'
