import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.helpers import LoginLocators, InventoryLocators, CartLocators, esperar_elemento, esperar_elementos, tomar_captura, logger

# ==============================================================================
# CONFIGURACIÓN DE FIXTURES (SETUP & TEARDOWN)
# ==============================================================================
@pytest.fixture(scope="module")
def driver():
    """Inicializa el WebDriver de Chrome antes de las pruebas y lo cierra al finalizar."""
    logger.info("=" * 80)
    logger.info("🚀 INICIANDO SUITE DE PRUEBAS DE SAUCEDEMO")
    logger.info("=" * 80)
    
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless") # Descomentar para ejecutar en segundo plano
    
    _driver = webdriver.Chrome(service=service, options=options)
    logger.info("✓ WebDriver Chrome inicializado correctamente")
    
    yield _driver
    
    logger.info("✓ WebDriver Chrome cerrado")
    logger.info("=" * 80)
    logger.info("✅ SUITE DE PRUEBAS FINALIZADA")
    logger.info("=" * 80)
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
        logger.info("\n" + "="*60)
        logger.info("[TEST 01] Iniciando prueba de LOGIN EXITOSO")
        logger.info("="*60)
        try:
            # 1. Navegar a la página de login
            logger.info(f"🌐 Navegando a: {self.URL_BASE}")
            driver.get(self.URL_BASE)
            logger.debug("✓ Página de login cargada")
            
            # 2. Ingresar credenciales válidas usando esperas explícitas
            logger.info("📝 Ingresando credenciales...")
            esperar_elemento(driver, LoginLocators.USERNAME_INPUT).send_keys("standard_user")
            logger.debug("✓ Usuario ingresado: standard_user")
            esperar_elemento(driver, LoginLocators.PASSWORD_INPUT).send_keys("secret_sauce")
            logger.debug("✓ Contraseña ingresada")
            esperar_elemento(driver, LoginLocators.LOGIN_BUTTON).click()
            logger.info("🔐 Botón de login clickeado")
            
            # 3. Validaciones de Login exitoso
            logger.info("✔ Validando login exitoso...")
            assert "/inventory.html" in driver.current_url, "La URL final no es la de inventario."
            logger.debug(f"✓ URL correcta: {driver.current_url}")
            
            logo_texto = esperar_elemento(driver, InventoryLocators.APP_LOGO).text
            assert logo_texto == "Swag Labs", f"El logo esperado era 'Swag Labs', pero se obtuvo: {logo_texto}"
            logger.debug(f"✓ Logo verificado: {logo_texto}")
            
            titulo_seccion = esperar_elemento(driver, InventoryLocators.TITLE_HEADER).text
            assert titulo_seccion == "Products", f"El título esperado era 'Products', pero se obtuvo: {titulo_seccion}"
            logger.debug(f"✓ Título verificado: {titulo_seccion}")
            logger.info("✅ [TEST 01] LOGIN EXITOSO - PASÓ")
            
        except Exception as e:
            logger.error(f"❌ [TEST 01] LOGIN EXITOSO - FALLÓ: {str(e)}")
            tomar_captura(driver, "test_01_login_exitoso")
            raise e

    def test_02_verificacion_catalogo(self, driver):
        """Caso de Prueba: Navegación y Verificación del Catálogo"""
        logger.info("\n" + "="*60)
        logger.info("[TEST 02] Iniciando prueba de VERIFICACIÓN DE CATÁLOGO")
        logger.info("="*60)
        try:
            # 1. Verificar presencia de componentes importantes de la interfaz
            logger.info("🔍 Verificando componentes de interfaz...")
            assert esperar_elemento(driver, InventoryLocators.BURGER_MENU).is_displayed(), "El menú lateral no está visible."
            logger.debug("✓ Menú lateral visible")
            assert esperar_elemento(driver, InventoryLocators.SORT_CONTAINER).is_displayed(), "El filtro de productos no está visible."
            logger.debug("✓ Filtro de productos visible")
            
            # 2. Comprobar que existan productos visibles
            logger.info("📦 Buscando productos en el catálogo...")
            productos = esperar_elementos(driver, InventoryLocators.INVENTORY_ITEMS)
            assert len(productos) > 0, "No se encontraron productos en el catálogo."
            logger.info(f"✓ {len(productos)} productos encontrados")
            
            # 3. Obtener y listar el nombre y precio del primer producto
            logger.info("💰 Extrayendo información del primer producto...")
            nombre_item = esperar_elemento(driver, InventoryLocators.FIRST_ITEM_NAME).text
            precio_item = esperar_elemento(driver, InventoryLocators.FIRST_ITEM_PRICE).text
            
            # Guardamos la variable en la clase para usarla en el test del carrito
            TestSauceDemo.primer_producto_nombre = nombre_item
            
            logger.info(f"📝 Primer Producto: {nombre_item} | Precio: {precio_item}")
            assert nombre_item != "", "El nombre del primer producto está vacío."
            assert precio_item != "", "El precio del primer producto está vacío."
            logger.info("✅ [TEST 02] VERIFICACIÓN DE CATÁLOGO - PASÓ")
            
        except Exception as e:
            logger.error(f"❌ [TEST 02] VERIFICACIÓN DE CATÁLOGO - FALLÓ: {str(e)}")
            tomar_captura(driver, "test_02_verificacion_catalogo")
            raise e

    def test_03_interaccion_carrito(self, driver):
        """Caso de Prueba: Añadir al carrito y verificar el producto"""
        logger.info("\n" + "="*60)
        logger.info("[TEST 03] Iniciando prueba de INTERACCIÓN CON CARRITO")
        logger.info("="*60)
        try:
            # 1. Añadir el primer producto al carrito
            logger.info("🛒 Añadiendo primer producto al carrito...")
            esperar_elemento(driver, InventoryLocators.FIRST_ITEM_ADD_BTN).click()
            logger.debug("✓ Botón 'Add to Cart' clickeado")
            
            # 2. Verificar que el contador se incremente a '1'
            logger.info("📊 Verificando contador del carrito...")
            contador_carrito = esperar_elemento(driver, InventoryLocators.SHOPPING_CART_BADGE).text
            assert contador_carrito == "1", f"El contador del carrito debería ser 1, pero es: {contador_carrito}"
            logger.debug(f"✓ Contador del carrito correcto: {contador_carrito}")
            
            # 3. Navegar al carrito de compras
            logger.info("📄 Navegando a la página del carrito...")
            esperar_elemento(driver, InventoryLocators.SHOPPING_CART_LINK).click()
            assert "/cart.html" in driver.current_url, "No se redirigió correctamente a la página del carrito."
            logger.debug(f"✓ Redirigido correctamente: {driver.current_url}")
            
            # 4. Comprobar que el producto añadido coincida con el que está en el carrito
            logger.info("✔ Verificando producto en el carrito...")
            producto_en_carrito = esperar_elemento(driver, CartLocators.CART_ITEM_NAME).text
            assert producto_en_carrito == self.primer_producto_nombre, \
                f"El ítem en el carrito ({producto_en_carrito}) no coincide con el agregado ({self.primer_producto_nombre})."
            logger.debug(f"✓ Producto en carrito verificado: {producto_en_carrito}")
            logger.info("✅ [TEST 03] INTERACCIÓN CON CARRITO - PASÓ")
                
        except Exception as e:
            logger.error(f"❌ [TEST 03] INTERACCIÓN CON CARRITO - FALLÓ: {str(e)}")
            tomar_captura(driver, "test_03_interaccion_carrito")
            raise e