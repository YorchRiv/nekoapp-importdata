from appium import webdriver
from appium.options.android import UiAutomator2Options

def get_driver():
    caps = {
        "platformName": "Android",
        "automationName": "uiautomator2",
        "deviceName": "emulator-5554",
        "appPackage": "com.tuxedolab.paycheckbuddy",
        "appActivity": ".MainActivity",
        "noReset": True,
        "disableWindowAnimation": True,
        "uiautomator2ServerLaunchTimeout": 10000,
        "uiautomator2ServerInstallTimeout": 10000,
        "waitForIdleTimeout": 0
    }
    options = UiAutomator2Options().load_capabilities(caps)
    driver = webdriver.Remote(command_executor="http://127.0.0.1:4723", options=options)
    return driver
