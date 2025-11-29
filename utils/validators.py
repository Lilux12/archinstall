"""
Валидация данных пользователя.
"""

import re
import subprocess
from utils.logger import logger
from utils.executor import run_command, command_exists
from config import t

def check_internet() -> bool:
    """
    Проверить подключение к интернету.
    Пингует archlinux.org
    
    Returns:
        True если есть интернет
    """
    logger.info("Checking internet connection...")
    returncode, _ = run_command(
        "ping -c 1 archlinux.org",
        check=False,
        log=False
    )
    result = returncode == 0
    logger.info(f"Internet check: {'OK' if result else 'FAILED'}")
    return result

def check_boot_mode() -> bool:
    """
    Проверить режим загрузки.
    
    Returns:
        True если UEFI, False если BIOS
    """
    import os
    return os.path.exists('/sys/firmware/efi')

def check_disk_space(disk: str, required_gb: int) -> bool:
    """
    Проверить достаточно ли места на диске.
    
    Args:
        disk: Путь к диску (например /dev/sda)
        required_gb: Требуемое место в GB
    
    Returns:
        True если места достаточно
    """
    try:
        returncode, output = run_command(
            f"lsblk -J -o NAME,SIZE {disk}",
            check=False,
            log=False
        )
        # Простая проверка - можно расширить
        return returncode == 0
    except Exception as e:
        logger.error(f"Failed to check disk space: {e}")
        return False

def check_pacman_keys() -> bool:
    """
    Инициализация ключей pacman.
    
    Returns:
        True если успешно
    """
    logger.info("Initializing pacman keys...")
    try:
        run_command("pacman-key --init", check=True, log=True)
        run_command("pacman-key --populate archlinux", check=True, log=True)
        return True
    except Exception as e:
        logger.error(f"Failed to initialize pacman keys: {e}")
        return False

def validate_hostname(hostname: str) -> bool:
    """
    Проверить корректность hostname.
    
    Args:
        hostname: Проверяемый hostname
    
    Returns:
        True если валидный
    """
    # Hostname может содержать буквы, цифры и дефис
    # Должен начинаться с буквы или цифры и заканчиваться буквой/цифрой
    pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    return re.match(pattern, hostname) is not None

def validate_username(username: str) -> bool:
    """
    Проверить корректность username.
    
    Args:
        username: Проверяемое имя пользователя
    
    Returns:
        True если валидное
    """
    # Username может содержать буквы, цифры, точки, дефисы
    # Должен начинаться с буквы и быть 3-32 символов
    pattern = r'^[a-z_][a-z0-9_-]{2,31}$'
    return re.match(pattern, username, re.IGNORECASE) is not None

def validate_password(password: str) -> Tuple[bool, str]:
    """
    Проверить надежность пароля.
    
    Args:
        password: Проверяемый пароль
    
    Returns:
        (is_valid, message)
    """
    if not password:
        return False, "Password cannot be empty"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, "Password is valid"

def check_all_prerequisites() -> bool:
    """
    Запустить все проверки перед установкой.
    
    Returns:
        True если все проверки пройдены
    """
    logger.info("=" * 50)
    logger.info("Running prerequisite checks...")
    logger.info("=" * 50)
    
    # Проверка root
    import os
    if os.geteuid() != 0:
        logger.error("This script must be run as root!")
        return False
    
    # Проверка интернета
    if not check_internet():
        logger.error("No internet connection!")
        return False
    
    # Проверка pacman keys
    if not check_pacman_keys():
        logger.warning("Failed to initialize pacman keys")
        # Не критично, продолжаем
    
    # Проверка необходимых команд
    required_commands = ['lsblk', 'parted', 'mkfs.ext4', 'pacstrap', 'arch-chroot']
    for cmd in required_commands:
        if not command_exists(cmd):
            logger.error(f"Required command not found: {cmd}")
            return False
    
    logger.info("All prerequisite checks passed!")
    logger.info("=" * 50)
    return True

from typing import Tuple
