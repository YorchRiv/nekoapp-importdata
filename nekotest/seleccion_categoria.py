from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy
import time

def seleccionar_categoria(driver, nombre_categoria, timeout=10, max_scroll=5):
    wait = WebDriverWait(driver, timeout)

    # Espera y clic en el campo "Select category"
    element = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.XPATH, '(//android.view.View[@content-desc="Category"]/following-sibling::android.view.View)[1]')
        )
    )
    element.click()
    time.sleep(0.2)  # Espera corta tras abrir selector

    for i in range(max_scroll):
        categorias = driver.find_elements(
            AppiumBy.XPATH,
            f'//android.view.View[@clickable="true" and contains(@content-desc, "{nombre_categoria}")]'
        )
        for categoria in categorias:
            desc = categoria.get_attribute('content-desc') or categoria.get_attribute('contentDescription')
            if desc and nombre_categoria in desc:
                categoria.click()

                # Esperar que regrese al formulario (ej. campo "Note")
                wait.until(
                    EC.presence_of_element_located(
                        (AppiumBy.XPATH, '//android.view.View[@content-desc="Notes"]')
                    )
                )
                return  # Éxito: salir

        # Scroll rápido
        driver.swipe(500, 1800, 500, 900, 80)
        time.sleep(0.15)

    # Si no se encuentra la categoría
    raise Exception(f'No se encontró la categoría "{nombre_categoria}" tras {max_scroll} scrolls.')
