from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def seleccionar_categoria(driver, nombre_categoria, max_scroll=8, timeout=5):
    # 1. Click en "Select category"    
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((AppiumBy.XPATH, '//android.view.View[@content-desc="Select category"]'))
    )
    element.click()
    time.sleep(0.5)

    # 2. Buscar la categoría, hacer scroll si no aparece
    for i in range(max_scroll):        
        # Espera explícita a que cargue la lista
        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((AppiumBy.XPATH, '//android.view.View[@clickable="true" and @content-desc]'))
        )

        categorias = driver.find_elements(
            AppiumBy.XPATH,
            '//android.view.View[@clickable="true" and @content-desc]'
        )
        encontradas = False
        for categoria in categorias:
            desc = categoria.get_attribute('contentDescription') or categoria.get_attribute('content-desc')            
            # Comparación robusta
            if desc and nombre_categoria.strip().lower() in desc.strip().lower():                
                categoria.click()
                return True
            encontradas = True

        # Si no se encontró la categoría en este ciclo, hacer scroll
        if not encontradas or i < max_scroll - 1:
            # Ajusta los valores de swipe si es necesario para tu pantalla
            driver.swipe(500, 1800, 500, 900, 500)
            time.sleep(0.8)
    return False
