from appium.webdriver.common.appiumby import AppiumBy
import time
from logger_config import setup_logger
logger = setup_logger()

def volver_a_home(driver, max_intentos=6, espera=0.8):
    home_xpath = '//android.view.View[@content-desc="Safe to spend"]'
    intentos = 0
    while intentos < max_intentos:
        try:
            driver.find_element(AppiumBy.XPATH, home_xpath)
            logger.info(f"Ya está en Home (intento {intentos+1})")
            return True  # Ya está en Home
        except Exception:
            logger.info(f"Intento {intentos+1}: No está en Home. Haciendo back...")
            try:
                driver.back()
            except Exception as e:
                logger.error(f"Falló el back: {e}")
            time.sleep(espera)
            intentos += 1
    logger.error("No se pudo volver a Home tras varios intentos.")
    return False
