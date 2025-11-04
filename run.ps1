# Market Analyzer - Script de inicio
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Market Analyzer - Iniciando..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Ejecutando aplicacion..." -ForegroundColor Green
Write-Host ""

& .\venv\Scripts\python.exe main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: La aplicacion no pudo iniciarse" -ForegroundColor Red
    Write-Host "Verifica que el entorno virtual este configurado correctamente" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
}
