@echo off
title AB-GEN AgroVive | M5 Demo Launcher
color 0A

echo ============================================================
echo   ⚖️ AB-GEN AgroVive - M5 INFERENCE ENGINE DEMO
echo ============================================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no detectado. Por favor instale Python 3.10+
    pause
    exit /b
)

:: Create Virtual Environment if not exists
if not exist .venv (
    echo [1/3] Creando entorno virtual .venv...
    python -m venv .venv
)

:: Activate and install requirements
echo [2/3] Verificando dependencias...
call .venv\Scripts\activate.bat
pip install -r requirements.txt --quiet

:: Launching Dashboard
echo [3/3] Iniciando M5 Gateway en http://127.0.0.1:5000...
echo.
echo Presiona Ctrl+C para apagar el motor.
echo.

:: Open browser
start http://127.0.0.1:5000

:: Run app
python app.py

pause
