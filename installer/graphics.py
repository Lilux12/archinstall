"""
Определение видеокарты и установка соответствующих драйверов.
"""

from typing import Dict, Optional, Tuple
from utils.executor import run_command
from utils.logger import logger
from ui.dialogs import get_dialog
from config import t

# Конфигурация драйверов
GPU_DRIVERS = {
    'nvidia_proprietary': {
        'packages': ['nvidia', 'nvidia-utils', 'nvidia-settings'],
        'description': 'nvidia_proprietary',
        'conflicts': ['xf86-video-nouveau'],
        'display_manager': 'gdm'
    },
    'nvidia_opensource': {
        'packages': ['xf86-video-nouveau', 'mesa'],
        'description': 'nvidia_opensource',
        'conflicts': ['nvidia', 'nvidia-utils'],
        'display_manager': 'gdm'
    },
    'amd': {
        'packages': ['mesa', 'xf86-video-amdgpu', 'vulkan-radeon',
                     'libva-mesa-driver', 'mesa-vdpau'],
        'description': 'amd_drivers',
        'conflicts': [],
        'display_manager': 'gdm'
    },
    'intel': {
        'packages': ['mesa', 'intel-media-driver', 'vulkan-intel'],
        'description': 'intel_drivers',
        'conflicts': [],
        'display_manager': 'gdm'
    },
    'hybrid': {
        'packages': ['nvidia', 'nvidia-prime', 'mesa'],
        'description': 'gpu_hybrid',
        'conflicts': [],
        'display_manager': 'gdm',
        'extra_config': 'nvidia-prime configuration'
    },
    'generic': {
        'packages': ['xf86-video-vesa'],
        'description': 'generic_drivers',
        'conflicts': [],
        'display_manager': 'gdm'
    }
}

def detect_gpu() -> Dict[str, str]:
    """
    Автоопределение видеокарты через lspci.
    
    Returns:
        Словарь с информацией о видеокарте
        {'vendor': 'NVIDIA', 'model': 'RTX 3080', 'driver_type': 'nvidia_proprietary'}
    """
    logger.debug("Detecting GPU...")
    
    try:
        returncode, output = run_command(
            "lspci | grep -E 'VGA|3D'",
            check=False,
            log=False
        )
        
        if returncode != 0 or not output:
            logger.warning("Could not detect GPU")
            return {
                'vendor': 'Unknown',
                'model': 'Unknown',
                'driver_type': 'generic'
            }
        
        gpu_info = output.strip()
        logger.debug(f"GPU string: {gpu_info}")
        
        # Определить вендора
        if 'NVIDIA' in gpu_info:
            vendor = 'NVIDIA'
            driver_type = 'nvidia_proprietary'
        elif 'AMD' in gpu_info or 'ATI' in gpu_info:
            vendor = 'AMD'
            driver_type = 'amd'
        elif 'Intel' in gpu_info:
            vendor = 'Intel'
            driver_type = 'intel'
        else:
            vendor = 'Unknown'
            driver_type = 'generic'
        
        # Попробовать найти модель
        parts = gpu_info.split(': ')
        model = parts[-1] if len(parts) > 1 else 'Unknown'
        
        result = {
            'vendor': vendor,
            'model': model,
            'driver_type': driver_type
        }
        
        logger.info(f"Detected GPU: {result}")
        return result
    
    except Exception as e:
        logger.error(f"Error detecting GPU: {e}")
        return {
            'vendor': 'Unknown',
            'model': 'Unknown',
            'driver_type': 'generic'
        }

def select_gpu_driver(dialog, detected_gpu: Dict) -> Optional[str]:
    """
    Диалог выбора видеодрайвера.
    
    Args:
        dialog: Экземпляр InstallerDialog
        detected_gpu: Информация об обнаруженной видеокарте
    
    Returns:
        Выбранный тип драйвера или None
    """
    # Показать информацию об обнаруженной видеокарте
    gpu_info = f"{detected_gpu['vendor']} {detected_gpu['model']}"
    
    # Подготовить варианты выбора
    choices = []
    selected_idx = 0
    
    for idx, (key, driver) in enumerate(GPU_DRIVERS.items()):
        desc = t(driver['description'])
        # Автоматический выбор для обнаруженной видеокарты
        if key == detected_gpu['driver_type']:
            selected_idx = idx
        choices.append((key, desc, 1 if key == detected_gpu['driver_type'] else 0))
    
    result = dialog.radiolist('select_gpu', choices, height=20, width=70)
    
    if result:
        logger.info(f"GPU driver selected: {result}")
        return result
    
    return None

def get_gpu_packages(driver_type: str) -> list:
    """
    Получить список пакетов для установки.
    
    Args:
        driver_type: Тип драйвера
    
    Returns:
        Список пакетов
    """
    if driver_type in GPU_DRIVERS:
        return GPU_DRIVERS[driver_type]['packages']
    return GPU_DRIVERS['generic']['packages']

def install_gpu_drivers(driver_type: str, mount_point: str = '/mnt') -> bool:
    """
    Установить видеодрайверы в chroot.
    
    Args:
        driver_type: Тип драйвера
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Installing GPU drivers: {driver_type}")
        
        if driver_type not in GPU_DRIVERS:
            logger.warning(f"Unknown driver type: {driver_type}")
            return False
        
        driver_config = GPU_DRIVERS[driver_type]
        packages = driver_config['packages']
        
        # Удалить конфликтующие пакеты
        for conflict in driver_config.get('conflicts', []):
            logger.debug(f"Removing conflicting package: {conflict}")
            run_command(
                f"arch-chroot {mount_point} pacman -R {conflict} --noconfirm",
                check=False,
                log=True
            )
        
        # Установить пакеты
        packages_str = ' '.join(packages)
        cmd = f"arch-chroot {mount_point} pacman -S {packages_str} --noconfirm"
        logger.info(f"Installing packages: {packages_str}")
        run_command(cmd, check=True, log=True)
        
        logger.info(f"GPU drivers installed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to install GPU drivers: {e}")
        return False

def configure_gpu_hybrid(mount_point: str = '/mnt') -> bool:
    """
    Настроить гибридную графику (NVIDIA Prime).
    
    Args:
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info("Configuring hybrid graphics (NVIDIA Prime)")
        
        # Создать конфигурационный файл для Prime
        config_content = """
# NVIDIA Prime configuration
# Use 'prime-run' command to run programs with dedicated GPU
# Example: prime-run glxinfo | grep NVIDIA
"""
        
        run_command(
            f"echo '{config_content}' > {mount_point}/etc/profile.d/nvidia-prime.sh",
            check=True,
            log=True
        )
        
        logger.info("Hybrid graphics configured")
        return True
    
    except Exception as e:
        logger.error(f"Failed to configure hybrid graphics: {e}")
        return False

def check_nvidia_legacy_needed() -> bool:
    """
    Проверить нужны ли legacy NVIDIA драйверы.
    
    Returns:
        True если нужны
    """
    try:
        returncode, output = run_command(
            "lspci | grep -E 'GeForce (6|7|8|9|GTX [0-9]{3}|GTX [0-9]{4}M)'",
            check=False,
            log=False
        )
        return returncode == 0
    except:
        return False
