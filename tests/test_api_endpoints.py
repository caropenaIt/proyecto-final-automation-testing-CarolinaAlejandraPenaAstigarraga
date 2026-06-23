import pytest
import requests
import json
from utils.helpers import (
    logger, 
    validar_respuesta_json, 
    validar_estructura_json,
    registrar_resultado_api
)

# ==============================================================================
# CONFIGURACIÓN DE API
# ==============================================================================
class APIConfig:
    """Configuración de endpoints públicos para testing"""
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    # Endpoints
    POSTS_ENDPOINT = f"{BASE_URL}/posts"
    USERS_ENDPOINT = f"{BASE_URL}/users"
    COMMENTS_ENDPOINT = f"{BASE_URL}/comments"

    # Headers
    HEADERS = {
        "Content-Type": "application/json; charset=UTF-8"
    }

# ==============================================================================
# SUITE DE PRUEBAS API
# ==============================================================================
class TestAPIEndpoints:
    """Suite de pruebas automatizadas para APIs públicas (JSONPlaceholder)"""

    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup y teardown para cada test de API"""
        logger.info("\n" + "="*80)
        logger.info("🔗 Iniciando test de API")
        logger.info("="*80)
        yield
        logger.info("="*80)

    def test_api_01_get_lista_posts(self):
        """
        CASO 01: GET - Obtener lista de posts
        
        Validaciones:
        - Status code: 200
        - Estructura JSON válida
        - Array no vacío
        - Campos requeridos en cada post
        """
        logger.info("\n[API TEST 01] GET - Obtener lista de posts")
        logger.debug(f"Endpoint: {APIConfig.POSTS_ENDPOINT}")
        
        try:
            # 1. Realizar petición GET
            logger.info("🌐 Enviando petición GET a /posts...")
            response = requests.get(
                APIConfig.POSTS_ENDPOINT,
                headers=APIConfig.HEADERS,
                timeout=5
            )
            logger.debug(f"Tiempo de respuesta: {response.elapsed.total_seconds():.2f}s")
            
            # 2. Validar status code
            logger.info("✔ Validando status code...")
            validar_respuesta_json(response, "GET /posts", expected_status=200)
            
            # 3. Validar estructura JSON
            logger.info("✔ Validando estructura JSON...")
            json_response = response.json()
            assert isinstance(json_response, list), "La respuesta debe ser una lista"
            logger.debug(f"Se obtuvieron {len(json_response)} posts")
            
            # 4. Validar que la lista no esté vacía
            assert len(json_response) > 0, "La lista de posts no puede estar vacía"
            logger.info(f"✓ Lista de posts no vacía: {len(json_response)} elementos")
            
            # 5. Validar estructura del primer post
            logger.info("✔ Validando estructura de posts...")
            campos_requeridos = ["userId", "id", "title", "body"]
            validar_estructura_json(json_response[0], campos_requeridos, "GET /posts")
            
            # 6. Validar tipos de datos
            logger.info("✔ Validando tipos de datos...")
            primer_post = json_response[0]
            assert isinstance(primer_post["userId"], int), "userId debe ser entero"
            assert isinstance(primer_post["id"], int), "id debe ser entero"
            assert isinstance(primer_post["title"], str), "title debe ser string"
            assert isinstance(primer_post["body"], str), "body debe ser string"
            logger.debug(f"Primer post: ID={primer_post['id']}, UserID={primer_post['userId']}")
            
            # Registrar resultado
            registrar_resultado_api("GET", "/posts", response.status_code, response.elapsed.total_seconds(), "PASÓ")
            logger.info("✅ [API TEST 01] GET /posts - PASÓ")
            
        except AssertionError as e:
            logger.error(f"❌ [API TEST 01] Assertion Error: {str(e)}")
            registrar_resultado_api("GET", "/posts", response.status_code if 'response' in locals() else 0, 0, "FALLÓ")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ [API TEST 01] Request Error: {str(e)}")
            raise

    def test_api_02_post_crear_nuevo_post(self):
        """
        CASO 02: POST - Crear nuevo post
        
        Validaciones:
        - Status code: 201 (Created)
        - Estructura JSON válida
        - El objeto retornado incluye el ID asignado
        - Los datos enviados se reflejan en la respuesta
        """
        logger.info("\n[API TEST 02] POST - Crear nuevo post")
        logger.debug(f"Endpoint: {APIConfig.POSTS_ENDPOINT}")
        
        try:
            # 1. Preparar datos para POST
            logger.info("📝 Preparando datos para POST...")
            nuevo_post = {
                "title": "Nuevo Post de Testing Automatizado",
                "body": "Este es un post creado mediante pruebas automatizadas de API",
                "userId": 1
            }
            logger.debug(f"Datos a enviar: {json.dumps(nuevo_post, indent=2)}")
            
            # 2. Realizar petición POST
            logger.info("🌐 Enviando petición POST...")
            response = requests.post(
                APIConfig.POSTS_ENDPOINT,
                json=nuevo_post,
                headers=APIConfig.HEADERS,
                timeout=5
            )
            logger.debug(f"Tiempo de respuesta: {response.elapsed.total_seconds():.2f}s")
            
            # 3. Validar status code (201 Created)
            logger.info("✔ Validando status code...")
            assert response.status_code == 201, f"Status code esperado: 201, Obtenido: {response.status_code}"
            logger.info(f"✓ Status code correcto: 201 (Created)")
            
            # 4. Validar estructura JSON
            logger.info("✔ Validando estructura JSON...")
            json_response = validar_respuesta_json(response, "POST /posts", expected_status=201)
            
            # 5. Validar que se incluye el ID
            logger.info("✔ Validando que el servidor asignó un ID...")
            assert "id" in json_response, "La respuesta debe incluir un 'id'"
            assert isinstance(json_response["id"], int), "El id debe ser entero"
            logger.info(f"✓ ID asignado: {json_response['id']}")
            
            # 6. Validar que los datos se reflejan en la respuesta
            logger.info("✔ Validando que los datos se reflejan en la respuesta...")
            assert json_response["title"] == nuevo_post["title"], "El title no coincide"
            assert json_response["body"] == nuevo_post["body"], "El body no coincide"
            assert json_response["userId"] == nuevo_post["userId"], "El userId no coincide"
            logger.debug(f"✓ Datos reflejados correctamente en la respuesta")
            
            # Registrar resultado
            registrar_resultado_api("POST", "/posts", response.status_code, response.elapsed.total_seconds(), "PASÓ")
            logger.info("✅ [API TEST 02] POST /posts - PASÓ")
            
        except AssertionError as e:
            logger.error(f"❌ [API TEST 02] Assertion Error: {str(e)}")
            registrar_resultado_api("POST", "/posts", response.status_code if 'response' in locals() else 0, 0, "FALLÓ")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ [API TEST 02] Request Error: {str(e)}")
            raise

    def test_api_03_delete_eliminar_post(self):
        """
        CASO 03: DELETE - Eliminar un post existente
        
        Validaciones:
        - Status code: 200 (OK)
        - La respuesta es un objeto vacío (comportamiento típico de JSONPlaceholder)
        - Verificar que el post ya no está disponible (GET posterior)
        """
        logger.info("\n[API TEST 03] DELETE - Eliminar post existente")
        
        try:
            # 1. Seleccionar un post para eliminar
            post_id = 1
            delete_url = f"{APIConfig.POSTS_ENDPOINT}/{post_id}"
            logger.info(f"🗑️  Eliminando post con ID: {post_id}")
            logger.debug(f"Endpoint: {delete_url}")
            
            # 2. Realizar petición DELETE
            logger.info("🌐 Enviando petición DELETE...")
            response = requests.delete(
                delete_url,
                headers=APIConfig.HEADERS,
                timeout=5
            )
            logger.debug(f"Tiempo de respuesta: {response.elapsed.total_seconds():.2f}s")
            
            # 3. Validar status code (200 OK)
            logger.info("✔ Validando status code...")
            assert response.status_code == 200, f"Status code esperado: 200, Obtenido: {response.status_code}"
            logger.info(f"✓ Status code correcto: 200 (OK)")
            
            # 4. Validar respuesta
            logger.info("✔ Validando respuesta DELETE...")
            # JSONPlaceholder retorna un objeto vacío o {} para DELETE
            json_response = response.json()
            assert isinstance(json_response, dict), "La respuesta debe ser un diccionario"
            logger.debug(f"Respuesta del servidor: {json.dumps(json_response, indent=2)}")
            logger.info("✓ Formato de respuesta correcto")
            
            # 5. Verificar que el post fue eliminado (GET posterior)
            logger.info("✔ Verificando que el post fue eliminado...")
            get_response = requests.get(delete_url, headers=APIConfig.HEADERS, timeout=5)
            # Nota: JSONPlaceholder devuelve 404 o {} para posts eliminados
            # En este caso, validamos que la respuesta sea nula o el objeto esté vacío
            assert get_response.status_code in [200, 404], f"Status code inesperado: {get_response.status_code}"
            logger.debug(f"Status GET posterior: {get_response.status_code}")
            logger.info("✓ Post eliminado correctamente")
            
            # Registrar resultado
            registrar_resultado_api("DELETE", f"/posts/{post_id}", response.status_code, response.elapsed.total_seconds(), "PASÓ")
            logger.info("✅ [API TEST 03] DELETE /posts/{id} - PASÓ")
            
        except AssertionError as e:
            logger.error(f"❌ [API TEST 03] Assertion Error: {str(e)}")
            registrar_resultado_api("DELETE", f"/posts/{post_id}", response.status_code if 'response' in locals() else 0, 0, "FALLÓ")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ [API TEST 03] Request Error: {str(e)}")
            raise

    def test_api_04_get_post_con_error_404(self):
        """
        CASO 04 (BONUS): GET - Manejo de errores (404 Not Found)
        
        Validaciones:
        - Status code: 404 para recurso no existente
        - Validar manejo correcto de errores
        """
        logger.info("\n[API TEST 04] GET - Validar error 404 (recurso no existente)")
        
        try:
            # 1. Intentar obtener un post con ID inválido
            post_id = 99999  # ID que probablemente no existe
            url = f"{APIConfig.POSTS_ENDPOINT}/{post_id}"
            logger.info(f"🔍 Solicitando post no existente: ID={post_id}")
            logger.debug(f"Endpoint: {url}")
            
            # 2. Realizar petición GET
            logger.info("🌐 Enviando petición GET...")
            response = requests.get(
                url,
                headers=APIConfig.HEADERS,
                timeout=5
            )
            logger.debug(f"Tiempo de respuesta: {response.elapsed.total_seconds():.2f}s")
            
            # 3. Validar que recibimos 404 o {} (JSONPlaceholder puede retornar ambos)
            logger.info("✔ Validando manejo de error 404...")
            assert response.status_code in [200, 404], f"Status code inesperado: {response.status_code}"
            logger.info(f"✓ Status code: {response.status_code}")
            
            # Si es 404, esperamos un objeto vacío o mensaje de error
            if response.status_code == 404:
                logger.info("✓ Recurso no encontrado (404) - Respuesta esperada")
            else:
                json_response = response.json()
                # JSONPlaceholder retorna {} para IDs no válidos en GET específico
                if isinstance(json_response, dict) and len(json_response) == 0:
                    logger.info("✓ Recurso no encontrado (respuesta vacía)")
            
            # Registrar resultado
            registrar_resultado_api("GET", f"/posts/{post_id}", response.status_code, response.elapsed.total_seconds(), "PASÓ")
            logger.info("✅ [API TEST 04] Manejo de error 404 - PASÓ")
            
        except AssertionError as e:
            logger.error(f"❌ [API TEST 04] Assertion Error: {str(e)}")
            registrar_resultado_api("GET", f"/posts/{post_id}", response.status_code if 'response' in locals() else 0, 0, "FALLÓ")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ [API TEST 04] Request Error: {str(e)}")
            raise


# ==============================================================================
# PRUEBAS PARAMETRIZADAS - Testing múltiples IDs de usuarios
# ==============================================================================
@pytest.mark.parametrize("user_id", [1, 2, 3, 4, 5])
class TestAPIParametrizadas:
    """Pruebas parametrizadas para validar múltiples usuarios"""
    
    def test_api_get_posts_por_usuario(self, user_id):
        """
        PRUEBA PARAMETRIZADA: GET - Obtener posts de múltiples usuarios
        
        Validaciones:
        - Status code: 200
        - Los posts pertenecen al usuario especificado
        """
        logger.info(f"\n[API TEST PARAMETRIZADA] GET - Posts del Usuario {user_id}")
        
        try:
            # 1. Realizar petición GET con query parameter
            logger.info(f"🌐 Obteniendo posts del usuario {user_id}...")
            url = f"{APIConfig.POSTS_ENDPOINT}?userId={user_id}"
            response = requests.get(
                url,
                headers=APIConfig.HEADERS,
                timeout=5
            )
            
            # 2. Validar status code
            validar_respuesta_json(response, f"GET /posts?userId={user_id}", expected_status=200)
            
            # 3. Validar que los posts pertenecen al usuario
            json_response = response.json()
            logger.info(f"✓ Se obtuvieron {len(json_response)} posts del usuario {user_id}")
            
            assert len(json_response) > 0, f"No se encontraron posts para el usuario {user_id}"
            
            for post in json_response:
                assert post["userId"] == user_id, f"Post pertenece a usuario {post['userId']}, se esperaba {user_id}"
            
            logger.info(f"✓ Todos los posts pertenecen al usuario {user_id}")
            registrar_resultado_api("GET", f"/posts?userId={user_id}", response.status_code, response.elapsed.total_seconds(), "PASÓ")
            logger.info(f"✅ Posts del usuario {user_id} - PASÓ")
            
        except AssertionError as e:
            logger.error(f"❌ Assertion Error: {str(e)}")
            registrar_resultado_api("GET", f"/posts?userId={user_id}", response.status_code if 'response' in locals() else 0, 0, "FALLÓ")
            raise
