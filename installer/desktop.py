"""
Выбор и установка Desktop Environment или Window Manager.
"""

from typing import Dict, Optional
from utils.executor import run_command
from utils.logger import logger
from ui.dialogs import get_dialog
from config import t

# Конфигурация Desktop Environments
DESKTOP_ENVIRONMENTS = {
    'kde': {
        'name': 'kde_plasma',
        'packages': ['plasma-meta', 'kde-applications-meta', 'sddm', 'sddm-kcm'],
        'display_manager': 'sddm',
        'description': 'kde_plasma',
        'ram_required': '2GB',
        'disk_space': '8GB'
    },
    'gnome': {
        'name': 'gnome',
        'packages': ['gnome', 'gnome-extra', 'gdm'],
        'display_manager': 'gdm',
        'description': 'gnome',
        'ram_required': '2GB',
        'disk_space': '8GB'
    },
    'xfce': {
        'name': 'xfce',
        'packages': ['xfce4', 'xfce4-goodies', 'lightdm', 'lightdm-gtk-greeter'],
        'display_manager': 'lightdm',
        'description': 'xfce',
        'ram_required': '512MB',
        'disk_space': '3GB'
    },
    'cinnamon': {
        'name': 'cinnamon',
        'packages': ['cinnamon', 'lightdm', 'lightdm-gtk-greeter'],
        'display_manager': 'lightdm',
        'description': 'cinnamon',
        'ram_required': '2GB',
        'disk_space': '5GB'
    },
    'mate': {
        'name': 'mate',
        'packages': ['mate', 'mate-extra', 'lightdm'],
        'display_manager': 'lightdm',
        'description': 'mate',
        'ram_required': '1GB',
        'disk_space': '4GB'
    },
    'i3': {
        'name': 'i3wm',
        'packages': ['i3-wm', 'i3status', 'i3lock', 'dmenu', 'lightdm', 'lightdm-gtk-greeter'],
        'display_manager': 'lightdm',
        'description': 'i3wm',
        'ram_required': '256MB',
        'disk_space': '1GB'
    },
    'sway': {
        'name': 'sway',
        'packages': ['sway', 'swaylock', 'swayidle', 'waybar', 'wofi', 'foot'],
        'display_manager': None,
        'description': 'sway',
        'ram_required': '512MB',
        'disk_space': '2GB'
    },
    'none': {
        'name': 'no_de',
        'packages': [],
        'display_manager': None,
        'description': 'no_de',
        'ram_required': '128MB',
        'disk_space': '500MB'
    }
}

def select_desktop_environment(dialog) -> Optional[str]:
    """
    Интерактивный выбор Desktop Environment через dialog.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Ключ выбранного DE или None
    """
    choices = []
    
    for key, de in DESKTOP_ENVIRONMENTS.items():
        desc = t(de['description'])
        ram = de['ram_required']
        space = de['disk_space']
        
        # Форматированное описание
        full_desc = f"{desc} ({ram} RAM, {space} disk)"
        choices.append((key, full_desc))
    
    result = dialog.radiolist('select_desktop', choices, height=20, width=80)
    
    if result:
        logger.info(f"Desktop environment selected: {result}")
        return result
    
    return None

def get_desktop_packages(de_key: str) -> list:
    """
    Получить список пакетов для DE.
    
    Args:
        de_key: Ключ Desktop Environment
    
    Returns:
        Список пакетов
    """
    if de_key in DESKTOP_ENVIRONMENTS:
        return DESKTOP_ENVIRONMENTS[de_key]['packages']
    return []

def get_display_manager(de_key: str) -> Optional[str]:
    """
    Получить display manager для DE.
    
    Args:
        de_key: Ключ Desktop Environment
    
    Returns:
        Имя display manager или None
    """
    if de_key in DESKTOP_ENVIRONMENTS:
        return DESKTOP_ENVIRONMENTS[de_key]['display_manager']
    return None

def install_desktop_environment(de_key: str, mount_point: str = '/mnt') -> bool:
    """
    Установить Desktop Environment в chroot.
    
    Args:
        de_key: Ключ Desktop Environment
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Installing Desktop Environment: {de_key}")
        
        if de_key not in DESKTOP_ENVIRONMENTS:
            logger.error(f"Unknown desktop environment: {de_key}")
            return False
        
        de_config = DESKTOP_ENVIRONMENTS[de_key]
        packages = de_config['packages']
        
        if not packages:  # Для 'none'
            logger.info("Skipping DE installation (command-line only)")
            return True
        
        # Установить пакеты
        packages_str = ' '.join(packages)
        cmd = f"arch-chroot {mount_point} pacman -S {packages_str} --noconfirm"
        logger.info(f"Installing packages: {packages_str}")
        run_command(cmd, check=True, log=True)
        
        # Включить display manager если нужен
        display_manager = de_config['display_manager']
        if display_manager:
            logger.debug(f"Enabling display manager: {display_manager}")
            run_command(
                f"arch-chroot {mount_point} systemctl enable {display_manager}",
                check=True,
                log=True
            )
        
        logger.info(f"Desktop environment installed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to install desktop environment: {e}")
        return False

def install_wayland_essentials(mount_point: str = '/mnt') -> bool:
    """
    Установить необходимые пакеты для Wayland.
    
    Args:
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info("Installing Wayland essentials")
        
        packages = ['wayland', 'xwayland', 'libxcb']
        packages_str = ' '.join(packages)
        
        cmd = f"arch-chroot {mount_point} pacman -S {packages_str} --noconfirm"
        run_command(cmd, check=True, log=True)
        
        return True
    
    except Exception as e:
        logger.error(f"Failed to install Wayland essentials: {e}")
        return False
