# Run Backend and Frontend concurrently
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Starting MI Net Growth Levels Management System" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

$backendPath = Join-Path $PSScriptRoot "backend"
$frontendPath = Join-Path $PSScriptRoot "frontend"

Write-Host "[1/2] Starting Django REST Backend on http://localhost:8000..." -ForegroundColor Yellow
$backendJob = Start-Process python -ArgumentList "manage.py runserver 8000" -WorkingDirectory $backendPath -PassThru

Write-Host "[2/2] Starting React Vite Frontend on http://localhost:5173..." -ForegroundColor Yellow
$frontendJob = Start-Process npm -ArgumentList "run dev" -WorkingDirectory $frontendPath -PassThru

Write-Host "`nSystem started successfully!" -ForegroundColor Green
Write-Host "Backend API:  http://localhost:8000/api/mi-net-growth-levels/" -ForegroundColor White
Write-Host "Frontend App: http://localhost:5173" -ForegroundColor White
Write-Host "`nPress Ctrl+C or close the terminal to stop processes." -ForegroundColor Gray
