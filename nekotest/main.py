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
from movimientos_data import movimientos
from util import volver_a_home

driver = get_driver()

try:
    for mov in movimientos:
        try:
            # INICIO del temporizador
            t_inicio = time.time()

            # "+" botón
            element = driver.find_element(
                AppiumBy.XPATH, 
                '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button'
            )
            element.click()
            time.sleep(0.5)

            # Seleccionar "Expense"
            element = driver.find_element(
                AppiumBy.XPATH, 
                '//android.view.View[contains(@content-desc, "Expense")]'
            )
            element.click()
            time.sleep(0.5)

            # Convierte el monto a centavos (int)
            monto_centavos = int(round(mov['monto'] * 100))

            # Resto del flujo
            ingresar_monto(driver, monto_centavos)
            ingresar_descripcion(driver, mov['descripcion'])
            ingresar_comentario(driver, mov['comentario'])
            seleccionar_fecha_datepicker(driver, mov['fecha'])
            seleccionar_cuenta(driver, mov['cuenta'])
            seleccionar_categoria(driver, mov['categoria'])
            guardar_gasto(driver)

            # FIN del temporizador
            t_fin = time.time()
            t_total = t_fin - t_inicio

            print(f"[OK] ID:{mov['id']} | {mov['monto']} | {mov['descripcion']} | {mov['cuenta']} | {mov['categoria']} | {mov['fecha']} | {t_total:.2f}s")
            time.sleep(1)

        except Exception as e:
            print(f"[FAIL] ID:{mov['id']} | {mov['monto']} | {mov['descripcion']} | {mov['cuenta']} | {mov['categoria']} | {mov['fecha']}")
            print(f"[ERROR] {e}")
            # Volver al home seguro con el método universal
            result = volver_a_home(driver)
            if not result:
                print("[ERROR EXTRA] No se pudo volver a Home tras varios intentos.")

finally:
    driver.quit()