from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time

caps = {
    "platformName": "Android",
    "automationName": "uiautomator2",
    "deviceName": "emulator-5554",
    "appPackage": "com.android.settings",
    "appActivity": ".Settings"
}

options = UiAutomator2Options().load_capabilities(caps)
driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=options)

try:
    # Espera a que abra Settings
    time.sleep(2)

    # Haz click en "Network & internet"
    element = driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/title" and @text="Network & internet"]')
    element.click()
    time.sleep(1)

    # Haz click en "Internet"
    element = driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/title" and @text="Internet"]')
    element.click()
    time.sleep(1)

    wifi_names = driver.find_elements(
        AppiumBy.XPATH,
        '//android.widget.LinearLayout[contains(@content-desc,"Wifi")]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView[@resource-id="android:id/title"]'
    )
    print("Redes Wi-Fi encontradas:")
    for el in wifi_names:
        print(el.text)
        
    time.sleep(10)

finally:
    # Cierra la sesión
    driver.quit()
