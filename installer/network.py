"""
Настройка сети: hostname и сетевой менеджер.
"""

from typing import Optional
from utils.executor import run_command
from utils.logger import logger
from utils.validators import validate_hostname
from ui.dialogs import get_dialog
from config import t

NETWORK_MANAGERS = {
    'networkmanager': {
        'name': 'NetworkManager',
        'packages': ['networkmanager'],
        'service': 'NetworkManager',
        'description': 'networkmanager'
    },
    'systemd_networkd': {
        'name': 'systemd-networkd',
        'packages': [],
        'service': 'systemd-networkd',
        'description': 'systemd_networkd'
    },
    'iwd': {
        'name': 'iwd',
        'packages': ['iwd'],
        'service': 'iwd',
        'description': 'iwd'
    }
}

def configure_hostname(dialog) -> Optional[str]:
    """
    Настроить hostname компьютера.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Установленный hostname или None
    """
    while True:
        hostname = dialog.inputbox(
            'enter_hostname',
            init='archlinux',
            height=10,
            width=60
        )
        
        if hostname is None:
            return None
        
        # Валидация
        if not hostname:
            dialog.msgbox('error_invalid_input')
            continue
        
        if not validate_hostname(hostname):
            dialog.msgbox('error_hostname_invalid')
            continue
        
        logger.info(f"Hostname configured: {hostname}")
        return hostname

def select_network_manager(dialog) -> Optional[str]:
    """
    Выбрать сетевой менеджер.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Выбранный сетевой менеджер или None
    """
    choices = [
        (key, t(nm['description']))
        for key, nm in NETWORK_MANAGERS.items()
    ]
    
    # NetworkManager рекомендуется для Desktop
    result = dialog.radiolist(
        'select_network_manager',
        choices,
        height=10,
        width=60
    )
    
    if result:
        logger.info(f"Network manager selected: {result}")
        return result
    
    return 'networkmanager'

def set_hostname(hostname: str, mount_point: str = '/mnt') -> bool:
    """
    Установить hostname в системе.
    
    Args:
        hostname: Название компьютера
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Setting hostname: {hostname}")
        
        # Создать /etc/hostname
        run_command(
            f"echo '{hostname}' > {mount_point}/etc/hostname",
            check=True,
            log=True
        )
        
        # Обновить /etc/hosts
        hosts_content = f"""127.0.0.1           localhost
::1                 localhost
127.0.1.1           {hostname}.localdomain	{hostname}
"""
        
        run_command(
            f"cat > {mount_point}/etc/hosts << 'EOF'\n{hosts_content}EOF",
            check=True,
            log=True,
            shell=True
        )
        
        logger.info("Hostname set successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to set hostname: {e}")
        return False

def install_network_manager(nm: str, mount_point: str = '/mnt') -> bool:
    """
    Установить и настроить сетевой менеджер.
    
    Args:
        nm: Ключ сетевого менеджера
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        if nm not in NETWORK_MANAGERS:
            logger.error(f"Unknown network manager: {nm}")
            return False
        
        nm_config = NETWORK_MANAGERS[nm]
        logger.info(f"Installing network manager: {nm}")
        
        # Установить пакеты
        if nm_config['packages']:
            packages_str = ' '.join(nm_config['packages'])
            run_command(
                f"arch-chroot {mount_point} pacman -S {packages_str} --noconfirm",
                check=True,
                log=True
            )
        
        # Включить сервис
        service = nm_config['service']
        run_command(
            f"arch-chroot {mount_point} systemctl enable {service}",
            check=True,
            log=True
        )
        
        logger.info(f"Network manager {nm} installed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to install network manager: {e}")
        return False

def enable_dhcp(mount_point: str = '/mnt') -> bool:
    """
    Включить DHCP для сетевых интерфейсов.
    
    Args:
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info("Enabling DHCP")
        
        # Найти сетевые интерфейсы
        returncode, output = run_command(
            "arch-chroot /mnt bash -c 'ip link | grep -E '^[0-9]+:' | grep -v lo | awk -F: '{print $2}' | tr -d ' ''",
            check=False,
            log=False
        )
        
        if returncode == 0 and output:
            interfaces = output.strip().split('\n')
            for iface in interfaces:
                if iface and iface != 'lo':
                    # Включить DHCP для интерфейса
                    run_command(
                        f"arch-chroot {mount_point} systemctl enable dhcpcd@{iface}",
                        check=False,
                        log=False
                    )
        
        logger.info("DHCP enabled")
        return True
    
    except Exception as e:
        logger.error(f"Failed to enable DHCP: {e}")
        return False
