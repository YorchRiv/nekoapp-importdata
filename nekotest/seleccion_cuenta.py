from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import time

def seleccionar_cuenta(driver, nombre_cuenta, timeout=10, max_scroll=5):
    wait = WebDriverWait(driver, timeout)

    # Espera a que aparezca el campo "Select account"
    element = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.XPATH, '(//android.view.View[@content-desc="Account"]/following-sibling::android.view.View)[1]')
        )
    )
    element.click()
    time.sleep(0.2)  # Menor espera inicial

    for i in range(max_scroll):
        cuentas = driver.find_elements(
            AppiumBy.XPATH,
            f'//android.view.View[@clickable="true" and contains(@content-desc, "{nombre_cuenta}")]'
        )
        for cuenta in cuentas:
            desc = cuenta.get_attribute('content-desc') or cuenta.get_attribute('contentDescription')
            if desc and nombre_cuenta in desc:
                cuenta.click()
                return  # Sale si encuentra

        # Scroll rápido
        driver.swipe(500, 1800, 500, 900, 80)  # Duración 80ms
        time.sleep(0.15)  # Espera mínima para recarga de vista

    # Si no se encuentra la cuenta después de los scrolls
    raise Exception(f'No se encontró la cuenta "{nombre_cuenta}" tras {max_scroll} scrolls.')
