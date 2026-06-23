import os
import logging
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

# ==============================================================================
# CONFIGURACIÓN DE LOGGING
# ==============================================================================
def configurar_logging():
    """Configura el sistema de logging centralizado para toda la suite de pruebas."""
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"test_execution_{timestamp}.log")
    
    # Configurar logger
    logger = logging.getLogger("QA_Automation")
    logger.setLevel(logging.DEBUG)
    
    # Handler para archivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Instancia global del logger
logger = configurar_logging()

# ==============================================================================
# LOCALIZADORES (ELEMENT LOCATORS) - Page Object Style
# ==============================================================================
class LoginLocators:
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

class InventoryLocators:
    TITLE_HEADER = (By.CLASS_NAME, "title")
    APP_LOGO = (By.CLASS_NAME, "app_logo")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    SORT_CONTAINER = (By.CLASS_NAME, "product_sort_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    
    # Selectores para el primer producto del catálogo
    FIRST_ITEM_NAME = (By.XPATH, "(//div[@class='inventory_item_name '])[1]")
    FIRST_ITEM_PRICE = (By.XPATH, "(//div[@class='inventory_item_price'])[1]")
    FIRST_ITEM_ADD_BTN = (By.XPATH, "(//button[contains(@class, 'btn_inventory')])[1]")
    
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

class CartLocators:
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

# ==============================================================================
# FUNCIONES AUXILIARES (HELPERS)
# ==============================================================================
def esperar_elemento(driver, locator, timeout=10):
    """Espera explícita hasta que un elemento sea visible en el DOM."""
    try:
        logger.debug(f"Esperando elemento con locator: {locator}")
        elemento = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
        logger.info(f"✓ Elemento encontrado y visible: {locator}")
        return elemento
    except Exception as e:
        logger.error(f"✗ Error esperando elemento {locator}: {str(e)}")
        raise

def esperar_elementos(driver, locator, timeout=10):
    """Espera explícita hasta que al menos un elemento de la lista sea visible."""
    try:
        logger.debug(f"Esperando lista de elementos con locator: {locator}")
        elementos = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(locator))
        logger.info(f"✓ {len(elementos)} elementos encontrados con locator: {locator}")
        return elementos
    except Exception as e:
        logger.error(f"✗ Error esperando lista de elementos {locator}: {str(e)}")
        raise

def tomar_captura(driver, nombre_prueba):
    """Toma una captura de pantalla en caso de fallo y la guarda en /reports."""
    ruta_reportes = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    if not os.path.exists(ruta_reportes):
        os.makedirs(ruta_reportes)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_archivo = os.path.join(ruta_reportes, f"{nombre_prueba}_error_{timestamp}.png")
    driver.save_screenshot(ruta_archivo)
    logger.warning(f"📸 Captura de pantalla guardada en: {ruta_archivo}")
    return ruta_archivo

# ==============================================================================
# FUNCIONES AUXILIARES PARA APIs
# ==============================================================================
def validar_respuesta_json(response, test_name, expected_status=200):
    """Valida una respuesta de API y extrae el JSON.
    
    Args:
        response: Objeto response de requests
        test_name: Nombre del test para logging
        expected_status: Código de estado esperado
        
    Returns:
        JSON parseado de la respuesta
    """
    logger.info(f"[API] Validando respuesta para: {test_name}")
    logger.debug(f"[API] Status Code: {response.status_code}")
    
    # Validar código de estado
    assert response.status_code == expected_status, \
        f"[API] Status code incorrecto. Esperado: {expected_status}, Obtenido: {response.status_code}"
    logger.info(f"✓ [API] Status code válido: {response.status_code}")
    
    # Intentar parsear JSON
    try:
        json_response = response.json()
        logger.debug(f"[API] Respuesta JSON: {json.dumps(json_response, indent=2)}")
        logger.info(f"✓ [API] JSON válido para {test_name}")
        return json_response
    except ValueError as e:
        logger.error(f"✗ [API] Error parseando JSON: {str(e)}")
        raise

def validar_estructura_json(json_data, campos_requeridos, test_name):
    """Valida que un JSON tenga los campos requeridos.
    
    Args:
        json_data: Diccionario JSON a validar
        campos_requeridos: Lista de campos esperados
        test_name: Nombre del test para logging
    """
    logger.info(f"[API] Validando estructura JSON para: {test_name}")
    logger.debug(f"[API] Campos requeridos: {campos_requeridos}")
    
    for campo in campos_requeridos:
        assert campo in json_data, f"[API] Campo requerido '{campo}' no encontrado en respuesta"
        logger.debug(f"✓ [API] Campo '{campo}' presente en respuesta")
    
    logger.info(f"✓ [API] Estructura JSON válida para {test_name}")

def registrar_resultado_api(metodo, endpoint, status_code, duracion, resultado="PASÓ"):
    """Registra los detalles de una llamada API.
    
    Args:
        metodo: GET, POST, DELETE, etc.
        endpoint: URL del endpoint
        status_code: Código de estado HTTP
        duracion: Tiempo de respuesta en segundos
        resultado: "PASÓ" o "FALLÓ"
    """
    logger.info(f"[API] {resultado} | Método: {metodo} | Endpoint: {endpoint} | Status: {status_code} | Duración: {duracion:.2f}s")