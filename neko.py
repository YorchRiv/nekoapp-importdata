from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

caps = {
    "platformName": "Android",
    "automationName": "uiautomator2",
    "deviceName": "emulator-5554",
    "appPackage": "com.tuxedolab.paycheckbuddy",
    "appActivity": ".MainActivity",
    "noReset": True
}

options = UiAutomator2Options().load_capabilities(caps)
driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=options)

try:
    # Haz click en "+"
    element = driver.find_element(AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button')
    element.click()

    # Expense
    element = driver.find_element(
        AppiumBy.XPATH,
        '//android.view.View[contains(@content-desc, "Expense")]'
    )
    element.click()

    # Ingresar Cantidad
    wait = WebDriverWait(driver, 10)
    campo_monto = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.EditText[@text="$0.00"]')
        )
    )
    campo_monto.click()
    campo_monto.clear()
    campo_monto.send_keys("150.00")

    # Descripción
    campo_texto = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText[2]')
        )
    )
    campo_texto.click()
    campo_texto.clear()
    campo_texto.send_keys("Texto de ejemplo")

    # Account
    element = driver.find_element(
        AppiumBy.XPATH,
        '//android.view.View[@content-desc="Select account"]'
    )
    element.click()
    time.sleep(1)

    # --------- Seleccionar la cuenta por nombre ---------
    nombre_cuenta = "Cash"  # Cambia esto por la cuenta que desees seleccionar

    # Busca todas las cuentas visibles con clickable y el nombre en content-desc
    cuentas = driver.find_elements(
        AppiumBy.XPATH,
        '//android.view.View[@clickable="true" and contains(@content-desc, "{}")]'.format(nombre_cuenta)
    )
    seleccionada = False
    for cuenta in cuentas:
        # Puede que 'content-desc' esté en 'contentDescription' según la versión de Appium, probamos ambos:
        desc = cuenta.get_attribute('contentDescription') or cuenta.get_attribute('content-desc')
        if desc and nombre_cuenta in desc:
            cuenta.click()
            seleccionada = True
            print(f'¡Cuenta "{nombre_cuenta}" seleccionada!')
            break

    if not seleccionada:
        print(f'No se encontró la cuenta "{nombre_cuenta}"')

    
    # 1. Click en "Select category"
    element = driver.find_element(
        AppiumBy.XPATH,
        '//android.view.View[@content-desc="Select category"]'
    )
    element.click()
    time.sleep(1)

    # 2. Buscar y seleccionar la categoría (con scroll)
    categoria_a_buscar = "Groceries"  # <-- Cambia aquí el nombre de la categoría que necesitas

    def buscar_y_seleccionar_categoria(nombre_categoria, max_scroll=6):
        """
        Busca la categoría por nombre (content-desc) y hace click.
        Si no la encuentra, hace scroll y sigue buscando.
        """
        for i in range(max_scroll):
            categorias = driver.find_elements(
                AppiumBy.XPATH,
                '//android.view.View[@clickable="true" and contains(@content-desc, "{}")]'.format(nombre_categoria)
            )
            seleccionada = False
            for categoria in categorias:
                desc = categoria.get_attribute('contentDescription') or categoria.get_attribute('content-desc')
                if desc and nombre_categoria in desc:
                    categoria.click()
                    print(f'¡Categoría "{nombre_categoria}" seleccionada!')
                    seleccionada = True
                    return True
            if not seleccionada:
                # Scroll hacia arriba (ajusta valores si hace falta)
                driver.swipe(500, 1800, 500, 900, 500)
                time.sleep(1)
        print(f'No se encontró la categoría "{nombre_categoria}"')
        return False

    buscar_y_seleccionar_categoria(categoria_a_buscar)

    # Espera que esté presente el campo de descripción (puedes ajustar el timeout si lo ves necesario)
    wait = WebDriverWait(driver, 10)
    campo_descripcion = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText[3]')
        )
    )

    # Limpia y escribe el texto de la descripción
    campo_descripcion.click()       # Opcional, si el campo requiere foco
    campo_descripcion.clear()       # Limpia si hay texto previo
    campo_descripcion.send_keys("Descripción de prueba automática")  # Cambia aquí tu texto

    # 1. Click en "Select category"
    element = driver.find_element(
        AppiumBy.XPATH,
        '//android.widget.Button[@content-desc="Save"]'
    )
    element.click()
    time.sleep(1)

    time.sleep(3)

finally:
    driver.quit()
