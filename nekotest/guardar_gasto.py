from appium.webdriver.common.appiumby import AppiumBy
import time

def guardar_gasto(driver):
    element = driver.find_element(
        AppiumBy.XPATH,
        '//android.widget.Button[@content-desc="Save"]'
    )
    element.click()
    time.sleep(1)
