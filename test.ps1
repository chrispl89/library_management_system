# Library Management System - Test Runner Script
# PowerShell script to run all tests

Write-Host "Running Library Management System Tests..." -ForegroundColor Cyan
Write-Host ""

# Check if containers are running
$containers = docker-compose ps -q
if (-not $containers) {
    Write-Host "Containers are not running. Starting them first..." -ForegroundColor Yellow
    docker-compose up -d
    Start-Sleep -Seconds 10
}

Write-Host "========================================" -ForegroundColor Blue
Write-Host "  Django Backend Tests" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

docker-compose exec -T backend python manage.py test --verbosity=2

$djangoResult = $LASTEXITCODE

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "  React Frontend Tests" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

docker-compose exec -T frontend npm test -- --watchAll=false --passWithNoTests

$reactResult = $LASTEXITCODE

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "  Test Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

if ($djangoResult -eq 0) {
    Write-Host "[PASSED] Django Tests" -ForegroundColor Green
} else {
    Write-Host "[FAILED] Django Tests" -ForegroundColor Red
}

if ($reactResult -eq 0) {
    Write-Host "[PASSED] React Tests" -ForegroundColor Green
} else {
    Write-Host "[FAILED] React Tests" -ForegroundColor Red
}

Write-Host ""

if ($djangoResult -eq 0 -and $reactResult -eq 0) {
    Write-Host "All tests passed!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "Some tests failed. Review the output above." -ForegroundColor Yellow
    exit 1
}
