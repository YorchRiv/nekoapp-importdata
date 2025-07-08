from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import time

def seleccionar_cuenta(driver, nombre_cuenta, timeout=10, max_scroll=5):
    wait = WebDriverWait(driver, timeout)
    
    # 1. Espera a que aparezca el botón/campo de "Select account"
    element = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.XPATH, '//android.view.View[@content-desc="Select account"]')
        )
    )
    element.click()
    time.sleep(0.5)

    # 2. Busca la cuenta por nombre, con intentos de scroll
    for i in range(max_scroll):
        cuentas = driver.find_elements(
            AppiumBy.XPATH,
            f'//android.view.View[@clickable="true" and contains(@content-desc, "{nombre_cuenta}")]'
        )
        for cuenta in cuentas:
            desc = cuenta.get_attribute('contentDescription') or cuenta.get_attribute('content-desc')
            if desc and nombre_cuenta in desc:
                cuenta.click()                
                return True
        # Si no se encontró, haz scroll hacia arriba (ajusta si hace falta)
        driver.swipe(500, 1800, 500, 900, 150)
        time.sleep(0.5)
    
    # Si no se encuentra la cuenta, lanza excepción
    raise Exception(f'No se encontró la cuenta "{nombre_cuenta}" tras {max_scroll} scrolls.')
