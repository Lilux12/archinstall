"""
Системные проверки и получение информации о системе.
"""

import os
import json
import psutil
from utils.logger import logger
from utils.executor import run_command
from typing import Dict, List, Optional

def get_total_memory_gb() -> float:
    """
    Получить общий объем RAM в GB.
    
    Returns:
        Объем RAM в GB
    """
    return psutil.virtual_memory().total / (1024 ** 3)

def get_available_memory_gb() -> float:
    """
    Получить доступный объем RAM в GB.
    
    Returns:
        Доступный объем RAM в GB
    """
    return psutil.virtual_memory().available / (1024 ** 3)

def get_cpu_info() -> Dict[str, any]:
    """
    Получить информацию о процессоре.
    
    Returns:
        Словарь с информацией о CPU
    """
    return {
        'count': psutil.cpu_count(),
        'percent': psutil.cpu_percent(interval=1),
        'brand': get_cpu_brand()
    }

def get_cpu_brand() -> str:
    """
    Получить бренд процессора.
    
    Returns:
        Название процессора
    """
    try:
        returncode, output = run_command(
            "grep -m1 'model name' /proc/cpuinfo | cut -d ':' -f 2",
            check=False,
            log=False
        )
        return output.strip() if returncode == 0 else "Unknown CPU"
    except:
        return "Unknown CPU"

def has_efi() -> bool:
    """
    Проверить поддержку EFI.
    
    Returns:
        True если система поддерживает EFI
    """
    return os.path.exists('/sys/firmware/efi')

def has_virtualization() -> bool:
    """
    Проверить поддержку виртуализации.
    
    Returns:
        True если поддерживается
    """
    try:
        returncode, output = run_command(
            "grep -o 'vmx\\|svm' /proc/cpuinfo | head -1",
            check=False,
            log=False
        )
        return returncode == 0 and bool(output.strip())
    except:
        return False

def get_system_info() -> Dict[str, any]:
    """
    Получить полную информацию о системе.
    
    Returns:
        Словарь со всеми параметрами
    """
    logger.debug("Collecting system information...")
    
    return {
        'memory_gb': get_total_memory_gb(),
        'cpu': get_cpu_info(),
        'uefi': has_efi(),
        'virtualization': has_virtualization(),
        'platform': os.uname().machine,
        'kernel': os.uname().release
    }

def print_system_info():
    """Вывести информацию о системе в лог."""
    info = get_system_info()
    logger.info("System Information:")
    logger.info(f"  RAM: {info['memory_gb']:.1f} GB")
    logger.info(f"  CPU cores: {info['cpu']['count']}")
    logger.info(f"  Boot mode: {'UEFI' if info['uefi'] else 'BIOS'}")
    logger.info(f"  Virtualization: {'Yes' if info['virtualization'] else 'No'}")
    logger.info(f"  Platform: {info['platform']}")
