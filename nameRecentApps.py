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
    seen = set()
    last_count = -1
    time.sleep(1)

    # Haz click en "Apps"
    element = driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@resource-id="android:id/title" and @text="Apps"]')
    element.click()
    time.sleep(1)

    apps_names = driver.find_elements(
        AppiumBy.XPATH,
        '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.android.settings:id/recycler_view"]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView[@resource-id="android:id/title"]'
    )
    print("Apps Recientes encontradas:")
    for el in apps_names:
        print(el.text)

    element = driver.find_element(AppiumBy.XPATH, '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.android.settings:id/recycler_view"]/android.widget.LinearLayout[6]/android.widget.RelativeLayout')
    element.click()
    time.sleep(1)

    while True:
        # Encuentra todos los títulos en pantalla
        sections = driver.find_elements(
            AppiumBy.XPATH,
            '//android.view.View/android.widget.TextView[@index="0"]'
        )

        for section in sections:
            name = section.text.strip()
            if name and name not in seen:
                seen.add(name)

        # Si ya no aparecen elementos nuevos, salimos del bucle
        if len(seen) == last_count:
            break
        last_count = len(seen)

        # Hacemos scroll hacia abajo (ajusta valores si es necesario)
        driver.swipe(500, 1500, 500, 500, 500)
        time.sleep(1)

    print("\nListado de Todas las Apps:")
    for name in seen:
        print(name)

        
    time.sleep(3)

finally:
    # Cierra la sesión
    driver.quit()

