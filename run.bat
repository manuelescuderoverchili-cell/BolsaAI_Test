@echo off
echo ========================================
echo   Market Analyzer - Iniciando...
echo ========================================
echo.
echo Ejecutando aplicacion...
echo.

venv\Scripts\python.exe main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: La aplicacion no pudo iniciarse
    echo Verifica que el entorno virtual este configurado correctamente
    pause
)
