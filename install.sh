#!/bin/bash
# ==============================================================================
# SCRIPT DE INSTALACIÓN RÁPIDA PARA LINUX/MAC
# ==============================================================================

echo ""
echo "========================================"
echo " INSTALACION DE QA AUTOMATION TESTING"
echo "========================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    echo "Instala Python desde: https://www.python.org/downloads/"
    exit 1
fi

echo "[1/4] Python encontrado ✓"
python3 --version

# Crear entorno virtual
echo "[2/4] Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "[3/4] Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "========================================"
echo " INSTALACIÓN COMPLETADA ✓"
echo "========================================"
echo ""
echo "El entorno virtual está activado."
echo ""
echo "Próximos pasos:"
echo "1. Para activar el entorno en futuras sesiones:"
echo "   source venv/bin/activate"
echo ""
echo "2. Ejecutar tests:"
echo "   pytest                        (Todos los tests)"
echo "   pytest tests/test_saucedemo.py    (Solo tests de UI)"
echo "   pytest tests/test_api_endpoints.py (Solo tests de API)"
echo ""
echo "3. Ver reporte HTML:"
echo "   open reports/report.html  (Mac)"
echo "   xdg-open reports/report.html  (Linux)"
echo ""
