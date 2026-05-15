import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

def esperar_elementos(driver, locator, timeout=10):
    """Espera explícita hasta que al menos un elemento de la lista sea visible."""
    return WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located(locator))

def tomar_captura(driver, nombre_prueba):
    """Toma una captura de pantalla en caso de fallo y la guarda en /reports."""
    ruta_reportes = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    if not os.path.exists(ruta_reportes):
        os.makedirs(ruta_reportes)
    
    ruta_archivo = os.path.join(ruta_reportes, f"{nombre_prueba}_error.png")
    driver.save_screenshot(ruta_archivo)
    print(f"\n[INFO] Captura de pantalla guardada en: {ruta_archivo}")