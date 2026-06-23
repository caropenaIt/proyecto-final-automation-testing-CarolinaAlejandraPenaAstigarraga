@echo off
REM ==============================================================================
REM SCRIPT DE INSTALACIÓN RÁPIDA PARA WINDOWS
REM ==============================================================================

echo.
echo ========================================
echo  INSTALACION DE QA AUTOMATION TESTING
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Descarga Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Python encontrado ✓

REM Crear entorno virtual
echo [2/4] Creando entorno virtual...
python -m venv venv
call venv\Scripts\activate.bat

echo [3/4] Instalando dependencias...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo  INSTALACIÓN COMPLETADA ✓
echo ========================================
echo.
echo El entorno virtual está activado.
echo.
echo Próximos pasos:
echo 1. Para activar el entorno en futuras sesiones:
echo    .\venv\Scripts\Activate.ps1  (PowerShell)
echo    .\venv\Scripts\activate.bat  (CMD)
echo.
echo 2. Ejecutar tests:
echo    pytest                        (Todos los tests)
echo    pytest tests/test_saucedemo.py    (Solo tests de UI)
echo    pytest tests/test_api_endpoints.py (Solo tests de API)
echo.
echo 3. Ver reporte HTML:
echo    start reports/report.html
echo.
pause
