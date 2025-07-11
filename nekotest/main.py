from driver_config import get_driver
from ingreso_monto import ingresar_monto
from ingreso_descripcion import ingresar_descripcion
from seleccion_cuenta import seleccionar_cuenta
from seleccion_categoria import seleccionar_categoria
from ingreso_comentario import ingresar_comentario
from guardar_gasto import guardar_gasto
from seleccionar_fecha import seleccionar_fecha_datepicker
from appium.webdriver.common.appiumby import AppiumBy
from util import volver_a_home
from movimientos_data import movimientos as movimientos_default

import csv
import os
import time

def leer_movimientos_csv(path):
    movimientos = []
    with open(path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            movimientos.append({
                'id': row['id'],
                'tipo': row['tipo'],
                'monto': float(row['monto']),
                'descripcion': row['descripcion'],
                'comentario': row.get('comentario', ''),
                'fecha': row['fecha'],
                'cuenta': row['cuenta'],
                'categoria': row['categoria']
            })
    return movimientos

# Preguntar al usuario de dónde leer los datos
print("Selecciona la fuente de movimientos:")
print("1. Lista interna (movimientos_data.py)")
print("2. Archivo CSV en ./csv/data.csv")

opcion = input("Ingresa 1 o 2: ").strip()

if opcion == "2":
    ruta_csv = os.path.join(os.getcwd(), "nekotest", "csv", "data.csv")
    if os.path.isfile(ruta_csv):
        movimientos = leer_movimientos_csv(ruta_csv)
        print(f"[INFO] Se cargaron {len(movimientos)} movimientos desde: {ruta_csv}")
    else:
        print(f"[ERROR] No se encontró el archivo: {ruta_csv}")
        exit(1)
else:
    movimientos = movimientos_default
    print(f"[INFO] Se usará la lista por defecto con {len(movimientos)} movimientos.")

# Inicia Appium
driver = get_driver()

try:
    for mov in movimientos:
        try:
            t_inicio = time.time()

            # "+" botón
            driver.find_element(
                AppiumBy.XPATH,
                '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button'
            ).click()
            time.sleep(0.5)

            if mov['tipo'] == "Income":
                print(f"[INFO] ID:{mov['id']} | Movimiento tipo INCOME")
                driver.find_element(AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "Income")]').click()
                time.sleep(0.5)
                ingresar_monto(driver, int(round(mov['monto'] * 100)))
                ingresar_descripcion(driver, mov['descripcion'])
                ingresar_comentario(driver, mov['comentario'])
                seleccionar_fecha_datepicker(driver, mov['fecha'])
                seleccionar_cuenta(driver, mov['cuenta'])
                seleccionar_categoria(driver, mov['categoria'])
                guardar_gasto(driver)

            elif mov['tipo'] == "Expense":
                print(f"[INFO] ID:{mov['id']} | Movimiento tipo EXPENSE")
                driver.find_element(AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "Expense")]').click()
                time.sleep(0.5)
                ingresar_monto(driver, int(round(mov['monto'] * 100)))
                ingresar_descripcion(driver, mov['descripcion'])
                ingresar_comentario(driver, mov['comentario'])
                seleccionar_fecha_datepicker(driver, mov['fecha'])
                seleccionar_cuenta(driver, mov['cuenta'])
                seleccionar_categoria(driver, mov['categoria'])
                guardar_gasto(driver)

            else:
                print(f"[WARNING] Tipo de movimiento desconocido: {mov['tipo']}. Saltando.")
                continue

            t_total = time.time() - t_inicio
            print(f"[OK] ID:{mov['id']} | {mov['monto']} | {mov['descripcion']} | {mov['cuenta']} | {mov['categoria']} | {mov['fecha']} | {t_total:.2f}s")
            time.sleep(1)

        except Exception as e:
            print(f"[FAIL] ID:{mov['id']} | {mov['monto']} | {mov['descripcion']} | {mov['cuenta']} | {mov['categoria']} | {mov['fecha']}")
            print(f"[ERROR] {e}")
            result = volver_a_home(driver)
            if not result:
                print("[ERROR EXTRA] No se pudo volver a Home tras varios intentos.")

finally:
    driver.quit()