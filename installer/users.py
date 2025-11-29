"""
Управление пользователями и группами.
"""

from typing import Optional, List
from utils.executor import run_command
from utils.logger import logger
from utils.validators import validate_username, validate_password
from ui.dialogs import get_dialog
from config import t

DEFAULT_GROUPS = ['wheel', 'audio', 'video', 'storage', 'optical']

def set_root_password(dialog) -> Optional[str]:
    """
    Установить пароль для root.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Установленный пароль или None
    """
    while True:
        password = dialog.passwordbox(
            'enter_root_password',
            height=10,
            width=60
        )
        
        if password is None:
            return None
        
        is_valid, message = validate_password(password)
        if not is_valid:
            dialog.msgbox(f"error: {message}")
            continue
        
        # Подтверждение
        confirm = dialog.passwordbox(
            'confirm_password',
            height=10,
            width=60
        )
        
        if confirm != password:
            dialog.msgbox('passwords_dont_match')
            continue
        
        logger.info("Root password set")
        return password

def create_user(dialog) -> Optional[dict]:
    """
    Создать основного пользователя.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Словарь с информацией о пользователе или None
    """
    # Ввод username
    while True:
        username = dialog.inputbox(
            'enter_username',
            height=10,
            width=60
        )
        
        if username is None:
            return None
        
        if not validate_username(username):
            dialog.msgbox('error_username_invalid')
            continue
        
        break
    
    # Ввод пароля
    while True:
        password = dialog.passwordbox(
            'user_password',
            height=10,
            width=60
        )
        
        if password is None:
            return None
        
        is_valid, message = validate_password(password)
        if not is_valid:
            dialog.msgbox(f"error: {message}")
            continue
        
        # Подтверждение
        confirm = dialog.passwordbox(
            'confirm_password',
            height=10,
            width=60
        )
        
        if confirm != password:
            dialog.msgbox('passwords_dont_match')
            continue
        
        break
    
    # Выбор групп
    group_choices = [
        ('wheel', 'wheel (sudo access)', 1),
        ('audio', 'audio', 1),
        ('video', 'video', 1),
        ('storage', 'storage', 1),
        ('optical', 'optical', 0),
        ('docker', 'docker', 0),
        ('kvm', 'kvm', 0),
    ]
    
    groups = dialog.checklist(
        'user_groups',
        group_choices,
        height=15,
        width=60
    )
    
    if groups is None:
        groups = DEFAULT_GROUPS
    
    result = {
        'username': username,
        'password': password,
        'groups': groups
    }
    
    logger.info(f"User created: {username}")
    return result

def set_root_password_system(password: str, mount_point: str = '/mnt') -> bool:
    """
    Установить пароль root в системе.
    
    Args:
        password: Пароль
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info("Setting root password")
        
        # Экранировать пароль для использования в shell
        escaped_pass = password.replace("'", "'\\''")
        
        # Установить пароль через chpasswd
        cmd = (
            f"echo 'root:{escaped_pass}' | "
            f"arch-chroot {mount_point} chpasswd"
        )
        
        run_command(cmd, check=True, log=False, shell=True)
        
        logger.info("Root password set successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to set root password: {e}")
        return False

def create_user_system(user_info: dict, mount_point: str = '/mnt') -> bool:
    """
    Создать пользователя в системе.
    
    Args:
        user_info: Словарь с информацией о пользователе
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        username = user_info['username']
        password = user_info['password']
        groups = user_info.get('groups', DEFAULT_GROUPS)
        
        logger.info(f"Creating user: {username}")
        
        # Создать пользователя
        groups_str = ','.join(groups)
        run_command(
            f"arch-chroot {mount_point} useradd -m -G {groups_str} {username}",
            check=True,
            log=True
        )
        
        # Установить пароль
        escaped_pass = password.replace("'", "'\\''")
        cmd = (
            f"echo '{username}:{escaped_pass}' | "
            f"arch-chroot {mount_point} chpasswd"
        )
        run_command(cmd, check=True, log=False, shell=True)
        
        logger.info(f"User {username} created successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to create user: {e}")
        return False

def setup_sudo(mount_point: str = '/mnt') -> bool:
    """
    Настроить sudo для группы wheel.
    
    Args:
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info("Configuring sudo for wheel group")
        
        # Раскомментировать wheel в sudoers
        run_command(
            f"sed -i 's/^# %wheel ALL=(ALL) ALL/%wheel ALL=(ALL) ALL/' "
            f"{mount_point}/etc/sudoers",
            check=True,
            log=True
        )
        
        logger.info("Sudo configured successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to configure sudo: {e}")
        return False
