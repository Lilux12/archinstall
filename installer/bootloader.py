"""
Установка загрузчика: GRUB или systemd-boot.
"""

from typing import Optional
from utils.executor import run_command
from utils.logger import logger
from ui.dialogs import get_dialog
from config import t
import os

def detect_boot_mode() -> bool:
    """
    Определить режим загрузки (UEFI или BIOS).
    
    Returns:
        True если UEFI, False если BIOS
    """
    is_uefi = os.path.exists('/sys/firmware/efi')
    logger.info(f"Boot mode: {'UEFI' if is_uefi else 'BIOS'}")
    return is_uefi

def select_bootloader(dialog, is_uefi: bool) -> Optional[str]:
    """
    Выбрать загрузчик через dialog.
    
    Args:
        dialog: Экземпляр InstallerDialog
        is_uefi: True если UEFI, False если BIOS
    
    Returns:
        Выбранный загрузчик ('grub' или 'systemd-boot') или None
    """
    if not is_uefi:
        # BIOS - только GRUB
        logger.info("BIOS mode detected, using GRUB")
        return 'grub'
    
    # UEFI - можно выбрать
    choices = [
        ('grub', 'GRUB (traditional bootloader)'),
        ('systemd-boot', 'systemd-boot (lightweight)')
    ]
    
    result = dialog.radiolist(
        'select_bootloader',
        choices,
        height=10,
        width=60
    )
    
    if result:
        logger.info(f"Bootloader selected: {result}")
        return result
    
    return 'grub'

def install_grub(disk: str, is_uefi: bool, mount_point: str = '/mnt') -> bool:
    """
    Установить GRUB загрузчик.
    
    Args:
        disk: Диск для установки (например /dev/sda)
        is_uefi: True если UEFI
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Installing GRUB bootloader on {disk}")
        
        # Установить пакеты
        packages = ['grub']
        if is_uefi:
            packages.append('efibootmgr')
        
        packages_str = ' '.join(packages)
        run_command(
            f"arch-chroot {mount_point} pacman -S {packages_str} --noconfirm",
            check=True,
            log=True
        )
        
        # Установить GRUB
        if is_uefi:
            logger.debug("Installing GRUB for UEFI")
            run_command(
                f"arch-chroot {mount_point} grub-install --target=x86_64-efi "
                f"--efi-directory=/boot/efi --bootloader-id=GRUB",
                check=True,
                log=True
            )
        else:
            logger.debug("Installing GRUB for BIOS")
            run_command(
                f"arch-chroot {mount_point} grub-install --target=i386-pc {disk}",
                check=True,
                log=True
            )
        
        # Сгенерировать конфиг GRUB
        logger.debug("Generating GRUB config")
        run_command(
            f"arch-chroot {mount_point} grub-mkconfig -o /boot/grub/grub.cfg",
            check=True,
            log=True
        )
        
        logger.info("GRUB installed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to install GRUB: {e}")
        return False

def install_systemd_boot(mount_point: str = '/mnt', kernel: str = 'linux') -> bool:
    """
    Установить systemd-boot загрузчик.
    
    Args:
        mount_point: Точка монтирования системы
        kernel: Имя ядра (linux, linux-lts и т.д.)
    
    Returns:
        True если успешно
    """
    try:
        logger.info("Installing systemd-boot bootloader")
        
        # Установить systemd-boot
        run_command(
            f"arch-chroot {mount_point} bootctl --path=/boot install",
            check=True,
            log=True
        )
        
        # Получить параметры ядра
        logger.debug("Configuring kernel parameters")
        returncode, root_uuid = run_command(
            f"blkid -s UUID -o value $(mount | grep '{mount_point} ' | awk '{{print $1}}')",
            check=False,
            log=False
        )
        
        if returncode != 0:
            logger.warning("Could not determine root UUID")
            root_uuid = "ROOT_UUID_HERE"
        else:
            root_uuid = root_uuid.strip()
        
        # Создать запись для Linux
        entry_content = f"""title   Arch Linux
linux   /vmlinuz-{kernel}
initrd  /initramfs-{kernel}.img
options root=UUID={root_uuid} rw
"""
        
        run_command(
            f"cat > {mount_point}/boot/loader/entries/arch.conf << 'EOF'\n{entry_content}EOF",
            check=True,
            log=True,
            shell=True
        )
        
        # Создать запись для LTS
        entry_lts = f"""title   Arch Linux LTS
linux   /vmlinuz-linux-lts
initrd  /initramfs-linux-lts.img
options root=UUID={root_uuid} rw
"""
        
        run_command(
            f"cat > {mount_point}/boot/loader/entries/arch-lts.conf << 'EOF'\n{entry_lts}EOF",
            check=True,
            log=True,
            shell=True
        )
        
        # Создать конфиг loader
        loader_config = """default arch
timeout 5
console-mode auto
editor yes
"""
        
        run_command(
            f"cat > {mount_point}/boot/loader/loader.conf << 'EOF'\n{loader_config}EOF",
            check=True,
            log=True,
            shell=True
        )
        
        logger.info("systemd-boot installed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to install systemd-boot: {e}")
        return False

def install_bootloader(
    bootloader: str,
    disk: str,
    is_uefi: bool,
    mount_point: str = '/mnt'
) -> bool:
    """
    Установить выбранный загрузчик.
    
    Args:
        bootloader: Тип загрузчика ('grub' или 'systemd-boot')
        disk: Диск для установки
        is_uefi: True если UEFI
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    if bootloader == 'grub':
        return install_grub(disk, is_uefi, mount_point)
    elif bootloader == 'systemd-boot':
        if not is_uefi:
            logger.error("systemd-boot requires UEFI")
            return False
        return install_systemd_boot(mount_point)
    else:
        logger.error(f"Unknown bootloader: {bootloader}")
        return False
