# 🧪 Suite Completa de Automatización de Testing - SauceDemo + API REST

Suite profesional de pruebas automatizadas que combina **testing de UI** con **Selenium** y **testing de APIs** con **requests**. Repositorio con suite de pruebas automatizadas funcionales para el sitio web de prácticas [SauceDemo](https://www.saucedemo.com/). Proyecto con arquitectura modular, logging centralizado, reportes HTML detallados y validaciones exhaustivas con Python.
## 🛠️ Tecnologías Utilizadas

*   **Lenguaje Principal:** Python 3.x
*   **Framework de Testing:** Pytest 7.4.3
*   **Herramienta de Automatización:** Selenium WebDriver 4.15.2
*   **Testing API:** Requests 2.31.0
*   **Gestor de Drivers:** WebDriver Manager 4.0.1 (Autogestiona la versión de ChromeDriver)
*   **Reportes:** pytest-html 4.1.1
*   **Logging:** Python logging (built-in)
*   **Control de Versiones:** Git y GitHub

---

## 📂 Estructura del Repositorio

```
proyecto/
├── tests/
│   ├── test_saucedemo.py          # Tests de UI (3 casos)
│   └── test_api_endpoints.py      # Tests de API (5+ casos)
├── utils/
│   └── helpers.py                 # Funciones auxiliares, logging, localizadores
├── logs/                          # Logs por sesión (auto-creado)
├── reports/
│   ├── report.html                # Reporte HTML
│   ├── *_error_*.png              # Capturas de pantalla
│   └── test_execution_*.log       # Logs detallados
├── conftest.py                    # Configuración global pytest
├── pytest.ini                     # Opciones pytest
├── requirements.txt               # Dependencias
├── install.bat                    # Script instalación Windows
├── install.sh                     # Script instalación Linux/Mac
└── README.md                      # Este archivo
```

---

## 🚀 Requisitos e Instalación

### Opción 1: Script Automático (Recomendado)

**Windows:**
```bash
install.bat
```

**Linux/Mac:**
```bash
bash install.sh
```

### Opción 2: Instalación Manual

**Paso 1: Crear entorno virtual**

Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Paso 2: Instalar Dependencias**

```bash
pip install -r requirements.txt
```

---

## 🧪 Ejecución de Pruebas

### Ejecutar todos los tests (UI + API)
```bash
pytest
```

### Ejecutar solo tests de UI (SauceDemo)
```bash
pytest tests/test_saucedemo.py -v
```

### Ejecutar solo tests de API
```bash
pytest tests/test_api_endpoints.py -v
```

### Ejecutar test específico
```bash
pytest tests/test_api_endpoints.py::TestAPIEndpoints::test_api_01_get_lista_posts -v
```

### Ejecutar con reporte HTML y logs en tiempo real
```bash
pytest -v -s --html=reports/report.html --self-contained-html
```

### Opciones avanzadas
```bash
pytest -v -s                    # Ver output en tiempo real
pytest -x                       # Detener al primer fallo
pytest --lf                     # Re-ejecutar solo fallos anteriores
pytest -k "nombre"              # Filtrar por nombre
pytest --tb=short               # Traceback corto
```

---

## ✅ Casos de Prueba Implementados

### 🌐 Tests de UI - SauceDemo (Selenium)

**test_01_login_exitoso:** Acceso correcto con standard_user, validando URL y elementos visuales de éxito.

**test_02_verificacion_catalogo:** Verificación de que los productos carguen, existencia de filtros y extracción de datos del primer producto.

**test_03_interaccion_carrito:** Flujo de agregar un producto, verificar el contador dinámico y validar que el ítem correcto esté en la lista de compra.

### 🔗 Tests de API - JSONPlaceholder

**test_api_01_get_lista_posts:** GET `/posts` - Valida status 200, estructura JSON y tipos de datos

**test_api_02_post_crear_nuevo_post:** POST `/posts` - Valida status 201, ID y datos reflejados

**test_api_03_delete_eliminar_post:** DELETE `/posts/{id}` - Valida status 200 y eliminación del recurso

**test_api_04_get_post_con_error_404:** GET `/posts/{id_inválido}` - Valida manejo correcto del error 404

**test_api_get_posts_por_usuario:** GET `/posts?userId={id}` - Tests parametrizados (5 usuarios)

**Total:** 8+ pruebas (3 UI + 5+ API)

---

## 📊 Reportes y Logs

### 🔍 Acceder al Reporte HTML

Después de ejecutar los tests:

**Windows:**
```bash
start reports/report.html
```

**Mac:**
```bash
open reports/report.html
```

**Linux:**
```bash
xdg-open reports/report.html
```

**El reporte incluye:**
- ✅ Tests ejecutados (nombre, duración)
- ❌ Tests fallidos (con error trace)
- ⏭️ Tests saltados
- 📊 Estadísticas generales
- 📸 Capturas de pantalla de fallos

### 📝 Ver Logs de Ejecución

Los logs se guardan automáticamente en: `logs/test_execution_YYYYMMDD_HHMMSS.log`

**Ver últimos logs:**

Windows:
```powershell
Get-Content logs/test_execution_*.log -Tail 50
```

Linux/Mac:
```bash
tail -50 logs/test_execution_*.log
```

---

## ✨ Características Principales

### 🌐 Automatización de Endpoints
- ✅ 5+ casos de prueba para API pública (JSONPlaceholder)
- ✅ Cobertura de métodos HTTP: GET, POST, DELETE
- ✅ Pruebas parametrizadas para validar múltiples escenarios
- ✅ Validación de códigos de estado HTTP
- ✅ Estructura y contenido de respuestas JSON

### 🛠️ Validación de Respuestas
- ✅ Verificación de códigos de estado HTTP
- ✅ Validación de estructura JSON
- ✅ Validación de tipos de datos
- ✅ Assertions para escenarios de éxito y error
- ✅ Manejo de errores (404, 500, etc.)

### 📊 Reportes HTML
- ✅ Reportes HTML detallados generados automáticamente
- ✅ Estado de tests: ✅ Pasado / ❌ Fallido / ⏭️ Saltado
- ✅ Duración de cada test y tiempo total
- ✅ Capturas de pantalla para pruebas fallidas
- ✅ Información de trazas y errores

### 📝 Sistema de Logging
- ✅ Logging centralizado con múltiples niveles
- ✅ Logs guardados en archivos por sesión
- ✅ Información detallada para debugging
- ✅ Timestamps y trazabilidad completa
- ✅ Salida formateada en consola y archivo

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue arquitectura modular, separando:
- **Casos de prueba:** `tests/`
- **Localizadores y funciones auxiliares:** `utils/helpers.py`
- **Configuración global:** `conftest.py` y `pytest.ini`

### Flujo de Ejecución

```
pytest.ini (configuración) → conftest.py (hooks globales) 
    ↓
test_saucedemo.py / test_api_endpoints.py
    ↓
helpers.py (funciones compartidas + logging)
    ↓
reports/report.html + logs/test_execution_*.log
```

---

## ❌ Resolución de Problemas

### Error: "ModuleNotFoundError"
Asegúrate de tener activado el entorno virtual:
```powershell
# Windows
.\venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### Error: "Webdriver no encontrado"
WebDriver Manager debería descargarlo automáticamente:
```bash
pip install --upgrade webdriver-manager
```

### Error: "Selenium no encontrado"
Reinstala dependencias:
```bash
pip install -r requirements.txt --force-reinstall
```

### Error: Tests de API fallan
Verifica conexión a jsonplaceholder.typicode.com:
```bash
ping jsonplaceholder.typicode.com
```

### Error: "El navegador Chrome no abre"
1. Instala Chrome/Chromium
2. Ejecuta en headless: `pytest --headless`
3. Verifica permisos de ChromeDriver

---

## ❓ Preguntas Frecuentes

**P: ¿Por dónde comienzo?**
R: Ejecuta `python -m venv venv`, actívalo, `pip install -r requirements.txt` y `pytest`

**P: ¿Dónde veo los resultados?**
R: Abre `reports/report.html` en tu navegador después de ejecutar `pytest`

**P: ¿Cómo agrego nuevos tests?**
R: Sigue los patrones en los archivos existentes. API tests en `test_api_endpoints.py`, UI tests en `test_saucedemo.py`

**P: ¿Dónde están los logs?**
R: En `logs/test_execution_YYYYMMDD_HHMMSS.log` (nuevo archivo por sesión)

**P: ¿Cómo ejecuto solo tests de API?**
R: `pytest tests/test_api_endpoints.py -v`

**P: ¿Cómo veo los logs en tiempo real?**
R: `pytest -v -s`

**P: ¿Cómo debuggeo un test fallido?**
R: `pytest tests/file.py::test_name -v -s --pdb`

---

## 🚀 Próximos Pasos

1. Ejecutar el proyecto siguiendo la sección Instalación
2. Ver resultados en `reports/report.html`
3. Revisar logs en `logs/test_execution_*.log`
4. Agregar tests siguiendo los patrones documentados
5. Integrar CI/CD usando los comandos de la suite

