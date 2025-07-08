from appium.webdriver.common.appiumby import AppiumBy
import time

def volver_a_home(driver, max_intentos=6, espera=0.8):
    home_xpath = '//android.view.View[@content-desc="Safe to spend"]'
    intentos = 0
    while intentos < max_intentos:
        try:
            driver.find_element(AppiumBy.XPATH, home_xpath)
            print(f"[VOLVER_A_HOME] Ya está en Home (intento {intentos+1})")
            return True  # Ya está en Home
        except Exception:
            print(f"[VOLVER_A_HOME] Intento {intentos+1}: No está en Home. Haciendo back...")
            try:
                driver.back()
            except Exception as e:
                print(f"[VOLVER_A_HOME][ERROR] Falló el back: {e}")
            time.sleep(espera)
            intentos += 1
    print("[VOLVER_A_HOME] No se pudo volver a Home tras varios intentos.")
    return False
