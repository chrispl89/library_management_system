# Library Management System - Windows Stop Script
# PowerShell script to stop the application

Write-Host "Stopping Library Management System..." -ForegroundColor Cyan
Write-Host ""

docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "All services stopped successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Failed to stop services." -ForegroundColor Red
}
