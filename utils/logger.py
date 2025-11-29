"""
Логирование установщика.
Все операции логируются в /var/log/archinstall.log
"""

import logging
import os
from datetime import datetime
from config import LOG_FILE, LOG_DIR

class ColoredFormatter(logging.Formatter):
    """Форматер логов с цветным выводом."""
    
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{log_color}{record.levelname}{self.COLORS['RESET']}"
        return super().format(record)

def setup_logger(name='archinstall', log_level=logging.INFO):
    """
    Настройка логирования.
    
    Args:
        name: Имя логгера
        log_level: Уровень логирования
    
    Returns:
        Конфигурированный logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Создать директорию логов если не существует
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)
    
    # Обработчик файла
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Обработчик консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = ColoredFormatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Глобальный логгер
logger = setup_logger()

def log_command(cmd, output, returncode):
    """
    Логировать выполненную команду.
    
    Args:
        cmd: Команда
        output: Вывод команды
        returncode: Код возврата
    """
    logger.debug(f"Command executed: {cmd}")
    if returncode == 0:
        logger.debug(f"Command output: {output[:200]}...")  # Первые 200 символов
    else:
        logger.error(f"Command failed with code {returncode}: {output}")
