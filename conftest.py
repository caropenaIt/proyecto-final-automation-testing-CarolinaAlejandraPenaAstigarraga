"""
Configuración global de pytest para toda la suite de tests
Incluye hooks para logging, captura de pantallas, y generación de reportes mejorados
"""

import pytest
import os
import json
from datetime import datetime
from utils.helpers import logger

# ==============================================================================
# HOOKS DE PYTEST
# ==============================================================================

def pytest_configure(config):
    """Hook llamado después de inicializar la configuración de pytest"""
    logger.info("=" * 80)
    logger.info("📊 INICIANDO EJECUCIÓN DE SUITE DE TESTS AUTOMATIZADOS")
    logger.info("=" * 80)
    logger.info(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Directorio de ejecución: {os.getcwd()}")
    logger.info("=" * 80)

def pytest_sessionstart(session):
    """Hook llamado al inicio de la sesión de tests"""
    logger.info("🚀 Sesión de testing iniciada")
    logger.debug(f"Python version: {session.config.option.verbose}")

def pytest_sessionfinish(session, exitstatus):
    """Hook llamado al final de la sesión de tests"""
    logger.info("=" * 80)
    logger.info("🏁 SESIÓN DE TESTING FINALIZADA")
    logger.info(f"Estado de salida: {exitstatus}")
    logger.info("=" * 80)
    logger.info("📋 Reportes generados en:")
    logger.info(f"   - HTML: {os.path.join(os.getcwd(), 'reports', 'report.html')}")
    logger.info(f"   - LOG: {os.path.join(os.getcwd(), 'logs')}")
    logger.info("=" * 80)

def pytest_runtest_setup(item):
    """Hook llamado antes de ejecutar cada test"""
    logger.debug(f"▶ Configurando test: {item.name}")

def pytest_runtest_teardown(item, nextitem):
    """Hook llamado después de ejecutar cada test"""
    logger.debug(f"⏹ Finalizando test: {item.name}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para capturar información del resultado del test"""
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call":
        if rep.passed:
            logger.info(f"✅ PASÓ: {item.name}")
        elif rep.failed:
            logger.error(f"❌ FALLÓ: {item.name}")
            # Aquí se pueden agregar acciones adicionales en caso de fallo
            if "driver" in item.fixturenames:
                logger.error(f"   Driver disponible para captura de pantalla")
        elif rep.skipped:
            logger.warning(f"⏭️  SALTADO: {item.name}")

def pytest_collection_modifyitems(config, items):
    """Hook para modificar los items recolectados"""
    logger.debug(f"📦 Tests recolectados: {len(items)}")
    
    # Separar tests por categoría
    selenium_tests = []
    api_tests = []
    
    for item in items:
        if "selenium" in item.nodeid.lower() or "saucedemo" in item.nodeid.lower():
            selenium_tests.append(item.name)
        elif "api" in item.nodeid.lower():
            api_tests.append(item.name)
    
    logger.debug(f"  - Tests de Selenium (UI): {len(selenium_tests)}")
    logger.debug(f"  - Tests de API: {len(api_tests)}")

# ==============================================================================
# FIXTURES GLOBALES
# ==============================================================================

@pytest.fixture(scope="session")
def test_summary():
    """Proporciona un diccionario para resumir la ejecución"""
    return {
        "inicio": datetime.now(),
        "tests_ejecutados": 0,
        "tests_pasados": 0,
        "tests_fallidos": 0,
        "tests_saltados": 0
    }

@pytest.fixture(autouse=True)
def log_test_start_end(request):
    """Registra el inicio y fin de cada test automáticamente"""
    test_name = request.node.name
    logger.info(f"\n{'='*60}")
    logger.info(f"▶ Iniciando: {test_name}")
    logger.info(f"{'='*60}")
    
    yield
    
    logger.info(f"⏹ Finalizado: {test_name}")
    logger.info(f"{'='*60}\n")

# ==============================================================================
# CONFIGURACIÓN DE DIRECTORIO DE LOGS Y REPORTS
# ==============================================================================

def pytest_sessionstart(session):
    """Crea directorios necesarios antes de ejecutar tests"""
    # Crear directorio de logs si no existe
    logs_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        logger.debug(f"✓ Directorio de logs creado: {logs_dir}")
    
    # Crear directorio de reports si no existe
    reports_dir = os.path.join(os.getcwd(), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        logger.debug(f"✓ Directorio de reportes creado: {reports_dir}")

# ==============================================================================
# OPCIONES PERSONALIZADAS DE PYTEST
# ==============================================================================

def pytest_addoption(parser):
    """Agrega opciones personalizadas a pytest"""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Ejecutar tests de Selenium en modo headless (sin interfaz gráfica)"
    )
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="Incluir tests lentos en la ejecución"
    )

@pytest.fixture(scope="session")
def headless(request):
    """Proporciona la opción de ejecución headless"""
    return request.config.getoption("--headless")

@pytest.fixture(scope="session")
def include_slow(request):
    """Proporciona la opción de incluir tests lentos"""
    return request.config.getoption("--slow")
