from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

def seleccionar_fecha_datepicker(driver, fecha_str):
    """
    Selecciona la fecha en el datepicker de la app.
    :param driver: Instancia de Appium.
    :param fecha_str: Fecha en formato 'YYYY-MM-DD' (ej: '2025-07-17')
    """
    # 1. Abre el modal del calendario dando click en el campo de la fecha
    time.sleep(0.5)
    # Este XPATH es robusto y solo busca cualquier botón clickable que contenga un "/"
    try:
        campo_fecha = driver.find_element(
            AppiumBy.XPATH,
            '//android.view.View[contains(@content-desc, "/") and @clickable="true"]'
        )
    except:
        # Alternativa: busca el primer clickable visible después de Transaction Date
        campo_fecha = driver.find_element(
            AppiumBy.XPATH,
            '//android.view.View[@content-desc="Transaction Date"]/following-sibling::android.view.View'
        )
    campo_fecha.click()
    time.sleep(0.5)

    # 2. Click en el botón para editar la fecha manualmente (icono calendario pequeño, normalmente el único button hijo)
    btn_editar_fecha = driver.find_element(
        AppiumBy.XPATH,
        '//android.view.View[contains(@content-desc,"Select date")]/android.view.View/android.widget.Button'
    )
    btn_editar_fecha.click()
    time.sleep(0.5)

    # 3. Selecciona el campo editable de fecha (EditText)
    edit_fecha = driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.EditText')
    edit_fecha.click()
    # Limpiar el campo: presiona BACKSPACE varias veces o usa .clear()
    try:
        edit_fecha.clear()
    except:
        # Si clear falla (a veces en modales), hazlo a mano:
        actual = edit_fecha.text
        for _ in range(len(actual) + 3):  # 3 extras por si hay residuos invisibles
            edit_fecha.send_keys(Keys.BACKSPACE)
    time.sleep(0.2)

    # 4. Escribe la fecha en formato MM/DD/YYYY (con ceros)
    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
    fecha_manual = fecha_obj.strftime("%m/%d/%Y")  # Con ceros a la izquierda

    edit_fecha.send_keys(fecha_manual)
    time.sleep(0.5)

    # 5. Da click al botón OK para confirmar
    btn_ok = driver.find_element(
        AppiumBy.XPATH,
        '//android.widget.Button[@content-desc="OK"]'
    )
    btn_ok.click()
    time.sleep(0.5)
