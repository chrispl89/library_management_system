# Library Management System - Windows Startup Script
# PowerShell script to start the application with Docker

Write-Host "Starting Library Management System..." -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker..." -ForegroundColor Yellow
$dockerRunning = docker info 2>$null
if (-not $dockerRunning) {
    Write-Host "Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
    exit 1
}
Write-Host "Docker is running" -ForegroundColor Green
Write-Host ""

# Build and start containers
Write-Host "Building and starting containers..." -ForegroundColor Yellow
docker-compose up -d --build

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "All services started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Application URLs:" -ForegroundColor Cyan
    Write-Host "   Frontend:  http://localhost:3000" -ForegroundColor White
    Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
    Write-Host "   API:       http://localhost:8000/api/" -ForegroundColor White
    Write-Host "   Admin:     http://localhost:8000/admin/" -ForegroundColor White
    Write-Host ""
    Write-Host "View logs with: docker-compose logs -f" -ForegroundColor Yellow
    Write-Host "Stop services with: docker-compose down" -ForegroundColor Yellow
    Write-Host ""
    
    # Wait for services to be ready
    Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    
    # Check service health
    Write-Host "Checking service health..." -ForegroundColor Yellow
    
    $maxAttempts = 30
    $attempt = 0
    $backendReady = $false
    
    while ($attempt -lt $maxAttempts -and -not $backendReady) {
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/api/books/" -UseBasicParsing -TimeoutSec 2 -ErrorAction SilentlyContinue
            if ($response.StatusCode -eq 200 -or $response.StatusCode -eq 401) {
                $backendReady = $true
                Write-Host "Backend is ready!" -ForegroundColor Green
            }
        } catch {
            $attempt++
            Write-Host "." -NoNewline
            Start-Sleep -Seconds 2
        }
    }
    
    Write-Host ""
    
    if (-not $backendReady) {
        Write-Host "Backend took longer than expected to start. Check logs: docker-compose logs backend" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "System is ready! Opening browser..." -ForegroundColor Green
    Start-Sleep -Seconds 2
    Start-Process "http://localhost:3000"
    
} else {
    Write-Host ""
    Write-Host "Failed to start services. Check the error messages above." -ForegroundColor Red
    Write-Host "View detailed logs with: docker-compose logs" -ForegroundColor Yellow
}
