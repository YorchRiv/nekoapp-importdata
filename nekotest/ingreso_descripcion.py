from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

def ingresar_descripcion(driver, descripcion):
    wait = WebDriverWait(driver, 10)
    # Buscar y escribir la descripción
    campo = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText[2]')
        )
    )
    campo.click()
    campo.clear()
    campo.send_keys(descripcion)
    
    # --- Tap en Notes para quitar menú autocompletado ---
    try:
        campo_notes = wait.until(
            EC.presence_of_element_located(
                # Universal XPATH para Notes, el último EditText suele ser Notes
                (AppiumBy.XPATH, '(//android.widget.EditText)[last()]')
            )
        )
        campo_notes.click()
        # Opcional: un pequeño sleep para que desaparezca el menú
        import time
        time.sleep(0.3)
    except Exception as e:
        print("[WARN] No se pudo dar focus en Notes para ocultar el menú autocompletado:", e)
