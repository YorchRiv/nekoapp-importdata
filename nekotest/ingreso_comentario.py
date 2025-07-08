from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

def ingresar_comentario(driver, comentario):
    wait = WebDriverWait(driver, 10)
    campo = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText[3]')
        )
    )
    campo.click()
    campo.clear()
    campo.send_keys(comentario)
