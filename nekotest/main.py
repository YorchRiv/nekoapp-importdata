from driver_config import get_driver
from ingreso_monto import ingresar_monto
from ingreso_descripcion import ingresar_descripcion
from seleccion_cuenta import seleccionar_cuenta
from seleccion_categoria import seleccionar_categoria
from ingreso_comentario import ingresar_comentario
from guardar_gasto import guardar_gasto
from seleccionar_fecha import seleccionar_fecha_datepicker
from appium.webdriver.common.appiumby import AppiumBy
import time

movimientos = [
    {
        "monto": 151.00,
        "descripcion": "Tienda test0003",
        "cuenta": "Cash",
        "categoria": "Groceries",
        "comentario": "Pan y leche",
        "fecha": "2025-06-24"
    }
    # ... más registros
]

driver = get_driver()

try:
    for mov in movimientos:
        try:
            # "+" botón
            element = driver.find_element(AppiumBy.XPATH, '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button')
            element.click()
            time.sleep(0.5)

            # Seleccionar "Expense"
            element = driver.find_element(AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "Expense")]')
            element.click()
            time.sleep(0.5)

            # Convierte el monto a centavos (int)
            monto_centavos = int(round(mov['monto'] * 100))

            # Resto del flujo
            ingresar_monto(driver, monto_centavos)
            ingresar_descripcion(driver, mov['descripcion'])
            seleccionar_fecha_datepicker(driver, mov['fecha'])
            seleccionar_cuenta(driver, mov['cuenta'])
            seleccionar_categoria(driver, mov['categoria'])
            ingresar_comentario(driver, mov['comentario'])
            guardar_gasto(driver)

            print(f"[OK] Registro: {mov['monto']} | {mov['descripcion']} | {mov['cuenta']} | {mov['categoria']} | {mov['fecha']}")
            time.sleep(1)
        except Exception as e:
            # Si ocurre cualquier error, da tap en el botón Back y muestra log de error
            try:
                back_btn = driver.find_element(AppiumBy.XPATH, '//android.widget.Button[@content-desc="Back"]')
                back_btn.click()
                time.sleep(0.5)
            except Exception as back_error:
                print(f"[ERROR EXTRA] No se pudo volver atrás: {back_error}")

            print(f"[FAIL] Registro: {mov['monto']} | {mov['descripcion']} | {mov['cuenta']} | {mov['categoria']} | {mov['fecha']} | ERROR: {str(e)}")
            continue

finally:
    driver.quit()