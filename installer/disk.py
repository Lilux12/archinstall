"""
Управление дисками и разделами.
Определение, выбор и разметка дисков.
"""

import json
import re
from typing import List, Dict, Tuple, Optional
from utils.executor import run_command
from utils.logger import logger
from ui.dialogs import get_dialog
from config import t

def detect_disks() -> List[Tuple[str, str]]:
    """
    Определить все доступные диски через lsblk.
    
    Returns:
        Список кортежей (device, size)
        Пример: [('/dev/sda', '500GB'), ('/dev/nvme0n1', '1TB')]
    """
    logger.debug("Detecting disks...")
    
    try:
        returncode, output = run_command(
            "lsblk -J -o NAME,SIZE,TYPE",
            check=False,
            log=False
        )
        
        if returncode != 0:
            logger.error("Failed to detect disks")
            return []
        
        data = json.loads(output)
        disks = []
        
        for block_device in data.get('blockdevices', []):
            if block_device.get('type') == 'disk':
                name = f"/dev/{block_device['name']}"
                size = block_device.get('size', 'Unknown')
                disks.append((name, size))
        
        logger.info(f"Detected disks: {disks}")
        return disks
    
    except json.JSONDecodeError:
        logger.error("Failed to parse lsblk output")
        return []
    except Exception as e:
        logger.error(f"Error detecting disks: {e}")
        return []

def select_disk(dialog) -> Optional[str]:
    """
    Интерактивный выбор диска через dialog.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Выбранное устройство (например '/dev/sda') или None
    """
    disks = detect_disks()
    
    if not disks:
        dialog.msgbox('error_disk_not_found')
        return None
    
    # Подготовка списка для dialog
    choices = [(disk, f"{disk} ({size})") for disk, size in disks]
    
    selected = dialog.radiolist('select_disk', choices)
    
    if selected and dialog.yesno('confirm_disk'):
        logger.info(f"Disk selected: {selected}")
        return selected
    
    return None

def detect_boot_mode() -> bool:
    """
    Определить режим загрузки.
    
    Returns:
        True если UEFI, False если BIOS
    """
    import os
    is_uefi = os.path.exists('/sys/firmware/efi')
    logger.info(f"Boot mode: {'UEFI' if is_uefi else 'BIOS'}")
    return is_uefi

def get_partition_schemes() -> Dict[str, Dict]:
    """
    Получить доступные схемы разметки.
    
    Returns:
        Словарь с описанием схем
    """
    return {
        'auto_ext4': {
            'name': 'auto_ext4',
            'description': 'Автоматическая (ext4)',
            'filesystem': 'ext4',
            'subvolumes': False
        },
        'auto_btrfs': {
            'name': 'auto_btrfs',
            'description': 'Автоматическая (btrfs)',
            'filesystem': 'btrfs',
            'subvolumes': True,
            'subvolume_list': ['@', '@home', '@var', '@snapshots']
        },
        'manual': {
            'name': 'manual',
            'description': 'Ручная разметка',
            'filesystem': None,
            'manual': True
        }
    }

def select_partition_scheme(dialog) -> Optional[str]:
    """
    Выбрать схему разметки через dialog.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Код выбранной схемы или None
    """
    schemes = get_partition_schemes()
    choices = [
        (key, t(value['description']))
        for key, value in schemes.items()
    ]
    
    return dialog.radiolist('partition_scheme', choices, height=15, width=60)

def setup_swap(dialog) -> Optional[Dict]:
    """
    Настройка swap через диалоги.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Словарь с конфигурацией swap или None
    """
    choices = [
        ('file', 'Swap-файл (рекомендуется)'),
        ('partition', 'Swap-раздел'),
        ('none', 'Без swap')
    ]
    
    swap_type = dialog.radiolist('Выберите тип swap', choices)
    
    if swap_type == 'none':
        return {'type': 'none', 'size_gb': 0}
    elif swap_type == 'file':
        size = dialog.inputbox('swap_size', init='2')
        return {'type': 'file', 'size_gb': int(size) if size else 2}
    elif swap_type == 'partition':
        return {'type': 'partition', 'size_gb': None}
    
    return None

def format_disk(disk: str, is_uefi: bool) -> bool:
    """
    Отформатировать диск (создать таблицу разделов).
    
    Args:
        disk: Путь к диску
        is_uefi: True если UEFI, False если BIOS
    
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Formatting disk {disk}")
        
        # Использовать sgdisk для GPT (UEFI) или fdisk для MBR (BIOS)
        if is_uefi:
            logger.debug(f"Creating GPT table on {disk}")
            run_command(f"sgdisk --zap-all {disk}", check=True)
            run_command(f"sgdisk -n 1:0:+512M -t 1:ef00 {disk}", check=True)
        else:
            logger.debug(f"Creating MBR table on {disk}")
            run_command(f"fdisk -l {disk}", check=False)
            # fdisk требует интерактивного ввода, поэтому используем parted
            run_command(
                f"parted -s {disk} mklabel msdos",
                check=True
            )
        
        logger.info(f"Disk {disk} formatted successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to format disk: {e}")
        return False

def create_partitions(
    disk: str,
    scheme: str,
    is_uefi: bool,
    swap_config: Optional[Dict] = None
) -> bool:
    """
    Создать разделы согласно схеме.
    
    Args:
        disk: Путь к диску
        scheme: Схема разметки
        is_uefi: True если UEFI
        swap_config: Конфигурация swap
    
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Creating partitions on {disk} with scheme {scheme}")
        
        if scheme == 'auto_ext4':
            return _create_auto_ext4(disk, is_uefi, swap_config)
        elif scheme == 'auto_btrfs':
            return _create_auto_btrfs(disk, is_uefi, swap_config)
        elif scheme == 'manual':
            logger.info("Opening manual partitioning tool (cfdisk)")
            run_command(f"cfdisk {disk}", check=False)
            return True
        
        return False
    
    except Exception as e:
        logger.error(f"Failed to create partitions: {e}")
        return False

def _create_auto_ext4(
    disk: str,
    is_uefi: bool,
    swap_config: Optional[Dict]
) -> bool:
    """Создать разделы для автоматической схемы ext4."""
    try:
        # Определить номера разделов
        if is_uefi:
            # EFI раздел уже создан при форматировании
            boot_partition = f"{disk}1"
            root_partition = f"{disk}2"
            
            # Создать корневой раздел
            run_command(
                f"sgdisk -n 2:0:0 -t 2:8300 {disk}",
                check=True
            )
        else:
            root_partition = f"{disk}1"
            boot_partition = None
        
        # Форматировать
        logger.debug(f"Formatting root partition {root_partition}")
        run_command(f"mkfs.ext4 -F {root_partition}", check=True)
        
        if is_uefi:
            logger.debug(f"Formatting EFI partition {boot_partition}")
            run_command(f"mkfs.fat -F 32 {boot_partition}", check=True)
        
        # Монтировать
        logger.debug("Mounting partitions")
        run_command("mkdir -p /mnt", check=True)
        run_command(f"mount {root_partition} /mnt", check=True)
        
        if is_uefi:
            run_command("mkdir -p /mnt/boot/efi", check=True)
            run_command(f"mount {boot_partition} /mnt/boot/efi", check=True)
        
        logger.info("Auto ext4 partitioning completed")
        return True
    
    except Exception as e:
        logger.error(f"Failed to create ext4 partitions: {e}")
        return False

def _create_auto_btrfs(
    disk: str,
    is_uefi: bool,
    swap_config: Optional[Dict]
) -> bool:
    """Создать разделы для автоматической схемы btrfs."""
    try:
        if is_uefi:
            boot_partition = f"{disk}1"
            root_partition = f"{disk}2"
            
            run_command(
                f"sgdisk -n 2:0:0 -t 2:8300 {disk}",
                check=True
            )
        else:
            root_partition = f"{disk}1"
            boot_partition = None
        
        # Форматировать в btrfs
        logger.debug(f"Formatting root partition {root_partition} with btrfs")
        run_command(f"mkfs.btrfs -f {root_partition}", check=True)
        
        if is_uefi:
            logger.debug(f"Formatting EFI partition {boot_partition}")
            run_command(f"mkfs.fat -F 32 {boot_partition}", check=True)
        
        # Монтировать и создать subvolumes
        logger.debug("Creating btrfs subvolumes")
        run_command("mkdir -p /mnt", check=True)
        run_command(f"mount {root_partition} /mnt", check=True)
        
        subvolumes = ['@', '@home', '@var', '@snapshots']
        for subvol in subvolumes:
            run_command(f"btrfs subvolume create /mnt/{subvol}", check=True)
        
        # Перемонтировать с subvolumes
        run_command(f"umount /mnt", check=True)
        run_command(f"mount -o subvol=@ {root_partition} /mnt", check=True)
        run_command("mkdir -p /mnt/home /mnt/var", check=True)
        run_command(f"mount -o subvol=@home {root_partition} /mnt/home", check=True)
        run_command(f"mount -o subvol=@var {root_partition} /mnt/var", check=True)
        
        if is_uefi:
            run_command("mkdir -p /mnt/boot/efi", check=True)
            run_command(f"mount {boot_partition} /mnt/boot/efi", check=True)
        
        logger.info("Auto btrfs partitioning completed")
        return True
    
    except Exception as e:
        logger.error(f"Failed to create btrfs partitions: {e}")
        return False

def generate_fstab() -> bool:
    """
    Генерировать /etc/fstab.
    
    Returns:
        True если успешно
    """
    try:
        logger.info("Generating fstab")
        run_command(
            "genfstab -U /mnt >> /mnt/etc/fstab",
            check=True
        )
        return True
    except Exception as e:
        logger.error(f"Failed to generate fstab: {e}")
        return False
