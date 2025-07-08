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
    time.sleep(2)

    seen = set()
    last_count = -1

    while True:
        # Encuentra todos los títulos en pantalla
        sections = driver.find_elements(
            AppiumBy.XPATH,
            '//android.widget.TextView[@resource-id="android:id/title"]'
        )

        for section in sections:
            name = section.text.strip()
            if name and name not in seen:
                print(name)
                seen.add(name)

        # Si ya no aparecen elementos nuevos, salimos del bucle
        if len(seen) == last_count:
            break
        last_count = len(seen)

        # Hacemos scroll hacia abajo (ajusta valores si es necesario)
        driver.swipe(500, 1500, 500, 500, 500)
        time.sleep(1)

    print("\nTodos los apartados (sin repetidos, y en orden):")
    for name in seen:
        print(name)


    time.sleep(5)
finally:
    driver.quit()
