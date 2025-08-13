from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import time

def seleccionar_cuenta(driver, nombre_cuenta, timeout=10, max_scroll=5):
    wait = WebDriverWait(driver, timeout)

    # Espera y click en el campo "Select account"
    element = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.XPATH, '(//android.view.View[@content-desc="Account" or @content-desc="Deposit Account"]/following-sibling::android.view.View)[1]')
        )
    )
    element.click()
    time.sleep(0.2)  # Menor espera inicial

    def buscar_cuenta_en_lista():
        for i in range(max_scroll):
            cuentas = driver.find_elements(
                AppiumBy.XPATH,
                f'//android.view.View[@clickable="true" and contains(@content-desc, "{nombre_cuenta}")]'
            )
            for cuenta in cuentas:
                desc = cuenta.get_attribute('content-desc') or cuenta.get_attribute('contentDescription')
                if desc and nombre_cuenta in desc:
                    cuenta.click()
                    return True  # Encontró la cuenta y clickeó

            # Scroll rápido
            driver.swipe(500, 1800, 500, 900, 80)  # Duración 80ms
            time.sleep(0.15)  # Espera mínima para recarga de vista
        return False

    # Intento 1: buscar en la primera lista
    if buscar_cuenta_en_lista():
        return  # Ya encontró y salió

    # Si no encuentra en la primera lista, hace tap en el tab "Credit cards"
    try:
        tab_credit_cards = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.XPATH, '//android.view.View[@content-desc="Credit cards\nTab 2 of 2"]')
            )
        )
        tab_credit_cards.click()
        time.sleep(0.5)  # Esperar a que cargue la nueva lista

        # Intento 2: buscar en la lista de credit cards
        if buscar_cuenta_en_lista():
            return  # Encontró y salió

    except Exception as e:
        # Si no encuentra el tab "Credit cards" o no puede hacer click,
        # seguimos con el flujo normal, puede ser que no exista ese tab
        pass

    # Si no encuentra la cuenta después de todos los intentos, lanza excepción
    raise Exception(f'No se encontró la cuenta "{nombre_cuenta}" tras {max_scroll} scrolls en ambas listas.')
