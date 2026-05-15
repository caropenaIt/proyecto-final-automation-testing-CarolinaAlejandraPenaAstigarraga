# 🧪 SauceDemo Projecto de Testing Automatizado

Este repositorio contiene una suite de pruebas automatizadas funcionales para el sitio web de prácticas [SauceDemo](https://www.saucedemo.com/). El diseño del proyecto sigue la arquitectura modular, separando los casos de prueba de los localizadores y funciones auxiliares.

## 🛠️ Tecnologías Utilizadas

*   **Lenguaje Principal:** Python 3.x
*   **Framework de Testing:** Pytest
*   **Herramienta de Automatización:** Selenium WebDriver
*   **Gestor de Drivers:** WebDriver Manager (Autogestiona la versión de ChromeDriver)
*   **Control de Versiones:** Git y GitHub

---

## 📂 Estructura del Repositorio

*   `tests/`: Contiene los scripts de prueba principales estructurados bajo Pytest.
*   `utils/`: Aloja funciones de soporte (esperas explícitas, capturas de pantalla) y los selectores web organizados por vistas.
*   `reports/`: Carpeta destinada a almacenar reportes de ejecución y capturas de pantalla en caso de fallos catastróficos.

---
## Se testeó

1. Login
2. Verificación del catálogo
3. interacción del flujo carrito


## 🚀 Requisitos e Instalación

### 1. Clonar el repositorio

git clone <ENLACE_DE_TU_REPOSITORIO>


2. En Windows (PowerShell):

python -m venv venv
.\\venv\\Scripts\\Activate.ps1
En Mac/Linux:


python3 -m venv venv
source venv/bin/activate

3. Instalar Dependencias
Una vez activado el entorno (verás el prefijo (venv)), instala lo necesario:


pip install selenium pytest webdriver-manager pytest-html
🧪 Ejecución de Pruebas
Para ejecutar la suite completa y generar el reporte profesional, usa el siguiente comando desde la raíz del proyecto:


python -m pytest tests/test_saucedemo.py -v -s --html=reports/report.html --self-contained-html
¿Qué validan estas pruebas?
Login: Acceso correcto con standard_user, validando URL y elementos visuales de éxito.

Catálogo: Verificación de que los productos carguen, existencia de filtros y extracción de datos del primer producto.

Carrito: Flujo de agregar un producto, verificar el contador dinámico y validar que el ítem correcto esté en la lista de compra.

📊 Reportes y Evidencias
* HTML Report: Tras la ejecución, abre reports/report.html en cualquier navegador para ver el resumen gráfico.

* Screenshots: Si alguna prueba falla, el sistema guardará automáticamente una captura de pantalla en la carpeta reports/ con el nombre del error.