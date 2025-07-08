from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

def ingresar_monto(driver, monto):
    wait = WebDriverWait(driver, 10)
    campo_monto = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.EditText[@text="$0.00"]')
        )
    )
    campo_monto.click()
    campo_monto.clear()
    campo_monto.send_keys(str(monto))
