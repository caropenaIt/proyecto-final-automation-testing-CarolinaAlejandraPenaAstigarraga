import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.helpers import LoginLocators, InventoryLocators, CartLocators, esperar_elemento, esperar_elementos, tomar_captura

# ==============================================================================
# CONFIGURACIÓN DE FIXTURES (SETUP & TEARDOWN)
# ==============================================================================
@pytest.fixture(scope="module")
def driver():
    """Inicializa el WebDriver de Chrome antes de las pruebas y lo cierra al finalizar."""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless") # Descomentar para ejecutar en segundo plano
    
    _driver = webdriver.Chrome(service=service, options=options)
    yield _driver
    _driver.quit()

# ==============================================================================
# SUITE DE PRUEBAS
# ==============================================================================
class TestSauceDemo:
    
    # Variables compartidas entre pruebas para verificar la persistencia del flujo
    URL_BASE = "https://www.saucedemo.com/"
    primer_producto_nombre = ""

    def test_01_login_exitoso(self, driver):
        """Caso de Prueba: Automatización de Login"""
        try:
            # 1. Navegar a la página de login
            driver.get(self.URL_BASE)
            
            # 2. Ingresar credenciales válidas usando esperas explícitas
            esperar_elemento(driver, LoginLocators.USERNAME_INPUT).send_keys("standard_user")
            esperar_elemento(driver, LoginLocators.PASSWORD_INPUT).send_keys("secret_sauce")
            esperar_elemento(driver, LoginLocators.LOGIN_BUTTON).click()
            
            # 3. Validaciones de Login exitoso
            assert "/inventory.html" in driver.current_url, "La URL final no es la de inventario."
            
            logo_texto = esperar_elemento(driver, InventoryLocators.APP_LOGO).text
            assert logo_texto == "Swag Labs", f"El logo esperado era 'Swag Labs', pero se obtuvo: {logo_texto}"
            
            titulo_seccion = esperar_elemento(driver, InventoryLocators.TITLE_HEADER).text
            assert titulo_seccion == "Products", f"El título esperado era 'Products', pero se obtuvo: {titulo_seccion}"
            
        except Exception as e:
            tomar_captura(driver, "test_01_login_exitoso")
            raise e

    def test_02_verificacion_catalogo(self, driver):
        """Caso de Prueba: Navegación y Verificación del Catálogo"""
        try:
            # 1. Verificar presencia de componentes importantes de la interfaz
            assert esperar_elemento(driver, InventoryLocators.BURGER_MENU).is_displayed(), "El menú lateral no está visible."
            assert esperar_elemento(driver, InventoryLocators.SORT_CONTAINER).is_displayed(), "El filtro de productos no está visible."
            
            # 2. Comprobar que existan productos visibles
            productos = esperar_elementos(driver, InventoryLocators.INVENTORY_ITEMS)
            assert len(productos) > 0, "No se encontraron productos en el catálogo."
            
            # 3. Obtener y listar el nombre y precio del primer producto
            nombre_item = esperar_elemento(driver, InventoryLocators.FIRST_ITEM_NAME).text
            precio_item = esperar_elemento(driver, InventoryLocators.FIRST_ITEM_PRICE).text
            
            # Guardamos la variable en la clase para usarla en el test del carrito
            TestSauceDemo.primer_producto_nombre = nombre_item
            
            print(f"\n[Catálogo] Primer Producto Encontrado: {nombre_item} | Precio: {precio_item}")
            assert nombre_item != "", "El nombre del primer producto está vacío."
            assert precio_item != "", "El precio del primer producto está vacío."
            
        except Exception as e:
            tomar_captura(driver, "test_02_verificacion_catalogo")
            raise e

    def test_03_interaccion_carrito(self, driver):
        """Caso de Prueba: Añadir al carrito y verificar el producto"""
        try:
            # 1. Añadir el primer producto al carrito
            esperar_elemento(driver, InventoryLocators.FIRST_ITEM_ADD_BTN).click()
            
            # 2. Verificar que el contador se incremente a '1'
            contador_carrito = esperar_elemento(driver, InventoryLocators.SHOPPING_CART_BADGE).text
            assert contador_carrito == "1", f"El contador del carrito debería ser 1, pero es: {contador_carrito}"
            
            # 3. Navegar al carrito de compras
            esperar_elemento(driver, InventoryLocators.SHOPPING_CART_LINK).click()
            assert "/cart.html" in driver.current_url, "No se redirigió correctamente a la página del carrito."
            
            # 4. Comprobar que el producto añadido coincida con el que está en el carrito
            producto_en_carrito = esperar_elemento(driver, CartLocators.CART_ITEM_NAME).text
            assert producto_en_carrito == self.primer_producto_nombre, \
                f"El ítem en el carrito ({producto_en_carrito}) no coincide con el agregado ({self.primer_producto_nombre})."
                
        except Exception as e:
            tomar_captura(driver, "test_03_interaccion_carrito")
            raise e