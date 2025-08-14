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
from logger_config import setup_logger
import csv
import os
import time

def procesar_transferencias(driver, movimientos, logger):
    for mov in movimientos:
        try:
            t_inicio = time.time()

            # "+" botón
            driver.find_element(
                AppiumBy.XPATH,
                '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button'
            ).click()
            time.sleep(0.5)
                        
            driver.find_element(AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "Transfer")]').click()
            time.sleep(0.5)
            ingresar_monto(driver, int(round(mov['monto'] * 100)))
            ingresar_descripcion(driver, mov['descripcion'])
            ingresar_comentario(driver, mov['comentario'])
            seleccionar_fecha_datepicker(driver, mov['fecha'])
            # Seleccionar cuenta origen (From Account)
            seleccionar_cuenta(driver, mov['cuenta'], es_destino=False)
            # Seleccionar cuenta destino (To Account)
            seleccionar_cuenta(driver, mov['destino'], es_destino=True)
            time.sleep(0.5)
            guardar_gasto(driver)

            t_total = time.time() - t_inicio
            logger.info(f"ID:{mov['id']} | {mov['monto']} | {mov['descripcion']} | {mov['cuenta']} -> {mov['destino']} | {mov['fecha']} | {mov['tipo']} | {t_total:.2f}s")
            time.sleep(1)

        except Exception as e:
            logger.error(f"ID:{mov['id']} | {mov['monto']} | {mov['descripcion']} | {mov['cuenta']} -> {mov['destino']} | {mov['fecha']} | {mov['tipo']}")
            logger.error(f"{e}")
            result = volver_a_home(driver)
            if not result:
                logger.error("No se pudo volver a Home tras varios intentos.")

def procesar_pagos_tarjeta(driver, movimientos, logger):
    for mov in movimientos:
        try:
            t_inicio = time.time()

            # "+" botón
            driver.find_element(
                AppiumBy.XPATH,
                '//android.widget.FrameLayout[@resource-id="android:id/content"]/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.widget.Button'
            ).click()
            time.sleep(0.5)

            driver.swipe(500, 1800, 500, 900, 500)  # Duración 80ms                        
            driver.find_element(AppiumBy.XPATH, '//android.view.View[contains(@content-desc, "Credit card payment")]').click()
            time.sleep(0.5)
            ingresar_monto(driver, int(round(mov['monto'] * 100)))                        
            seleccionar_fecha_datepicker(driver, mov['fecha'])
            # Seleccionar tarjeta de crédito (Credit Card)
            seleccionar_cuenta(driver, mov['destino'], es_destino=True, es_pago_tc=True)
            # Seleccionar cuenta origen (Pay From)
            seleccionar_cuenta(driver, mov['cuenta'], es_destino=False, es_pago_tc=True)
            time.sleep(0.5)
            guardar_gasto(driver)

            t_total = time.time() - t_inicio
            logger.info(f"ID:{mov['id']} | {mov['monto']} | {mov['cuenta']} -> {mov['destino']} | {mov['fecha']} | {mov['tipo']} | {t_total:.2f}s")
            time.sleep(1)

        except Exception as e:
            logger.error(f"ID:{mov['id']} | {mov['monto']} | {mov['cuenta']} -> {mov['destino']} | {mov['fecha']} | {mov['tipo']}")
            logger.error(f"{e}")
            result = volver_a_home(driver)
            if not result:
                logger.error("No se pudo volver a Home tras varios intentos.")
    return True

def procesar_ingresos_egresos(driver, movimientos, logger):
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
                logger.warning(f"Tipo de movimiento desconocido: {mov['tipo']}. Saltando.")
                continue

            t_total = time.time() - t_inicio
            logger.info(f"ID:{mov['id']} | {mov['monto']} | {mov['descripcion']} | {mov['cuenta']} | {mov['categoria']} | {mov['fecha']} | {mov['tipo']} | {t_total:.2f}s")
            time.sleep(1)

        except Exception as e:
            logger.error(f"ID:{mov['id']} | {mov['monto']} | {mov['descripcion']} | {mov['cuenta']} | {mov['categoria']} | {mov['fecha']} | {mov['tipo']}")
            logger.error(f"{e}")
            result = volver_a_home(driver)
            if not result:
                logger.error("No se pudo volver a Home tras varios intentos.")

def leer_movimientos_csv(path, es_transferencia=False, es_pago_tarjeta=False):
    movimientos = []
    with open(path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                if es_pago_tarjeta:
                    movimientos.append({
                        'id': row['id'],
                        'monto': float(row['monto']),
                        'cuenta': row['cuenta'],
                        'destino': row['destino'],
                        'comentario': row.get('comentario', ''),
                        'fecha': row['fecha'],
                        'tipo': 'Credit Card Payment'
                    })
                elif es_transferencia:
                    movimientos.append({
                        'id': row['id'],
                        'monto': float(row['monto']),
                        'descripcion': row['descripcion'],
                        'cuenta': row['cuenta'],
                        'destino': row['destino'],
                        'comentario': row.get('comentario', ''),
                        'fecha': row['fecha'],
                        'tipo': row['tipo']
                    })
                else:
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
            except ValueError as e:
                # Si hay un error de conversión, mostrar más contexto
                raise ValueError(f'Error en la fila {reader.line_num}: {str(e)}')
    return movimientos

def cargar_datos(logger, es_transferencia=False, es_pago_tarjeta=False):
    print("Selecciona la fuente de movimientos:")
    if not (es_transferencia or es_pago_tarjeta):
        print("1. Lista interna (movimientos_data.py)")
        print("2. Archivo CSV en ./csv/data.csv")
    else:
        archivo = "paytc.csv" if es_pago_tarjeta else "transfers.csv"
        print(f"1. Archivo CSV en ./csv/{archivo}")
    
    if es_transferencia or es_pago_tarjeta:
        opcion = "2"  # Forzar uso de CSV para transferencias y pagos de tarjeta
    else:
        opcion = input("Ingresa 1 o 2: ").strip()
    
    if opcion == "2":
        if es_pago_tarjeta:
            nombre_archivo = "paytc.csv"
        elif es_transferencia:
            nombre_archivo = "transfers.csv"
        else:
            nombre_archivo = "data.csv"
            
        ruta_csv = os.path.join(os.getcwd(), "nekotest", "csv", nombre_archivo)
        if os.path.isfile(ruta_csv):
            movimientos = leer_movimientos_csv(ruta_csv, es_transferencia, es_pago_tarjeta)
            logger.info(f"Se cargaron {len(movimientos)} movimientos desde: {ruta_csv}")
            return movimientos
        else:
            logger.error(f"No se encontró el archivo: {ruta_csv}")
            exit(1)
    else:
        if es_transferencia:
            logger.error("Para transferencias solo se permite cargar desde CSV")
            exit(1)
        elif es_pago_tarjeta:
            logger.error("Para pagos con tarjeta solo se permite cargar desde CSV")
            exit(1)
        logger.info(f"Se usará la lista por defecto con {len(movimientos_default)} movimientos.")
        return movimientos_default

def main():
    logger = setup_logger()
    
    print("\nSelecciona el tipo de operación:")
    print("1. Ingresos / Egresos")
    print("2. Transferencias")
    print("3. Pagos con Tarjeta")
    
    tipo_operacion = input("Ingresa 1, 2 o 3: ").strip()
    
    # Determinar el tipo de operación
    es_transferencia = tipo_operacion == "2"
    es_pago_tarjeta = tipo_operacion == "3"
    
    # Cargar datos según el tipo de operación
    movimientos = cargar_datos(logger, es_transferencia, es_pago_tarjeta)
    driver = get_driver()
    
    try:
        if tipo_operacion == "1":
            procesar_ingresos_egresos(driver, movimientos, logger)
        elif tipo_operacion == "2":
            procesar_transferencias(driver, movimientos, logger)
        elif tipo_operacion == "3":
            procesar_pagos_tarjeta(driver, movimientos, logger)
        else:
            logger.error("Opción inválida")
            return
    finally:
        driver.quit()

if __name__ == "__main__":
    main()