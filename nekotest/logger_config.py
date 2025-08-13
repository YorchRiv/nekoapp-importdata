import logging
import os
from datetime import datetime

def setup_logger():
    logger = logging.getLogger()
    
    # Si el logger ya tiene handlers, retornarlo sin modificar
    if logger.hasHandlers():
        return logger
    
    logger.setLevel(logging.INFO)

    # Crear directorio logs si no existe
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Usar fecha y hora para el nombre del archivo
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(logs_dir, f'app_{timestamp}.log')

    # Handler para archivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)

    # Añadir handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info(f'Usando archivo de log: {log_file}')

    return logger