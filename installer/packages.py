"""
Профили установки и дополнительные пакеты.
"""

from typing import Dict, List, Optional
from utils.executor import run_command
from utils.logger import logger
from ui.dialogs import get_dialog
from config import t

# Профили установки
INSTALLATION_PROFILES = {
    'desktop': {
        'name': 'Desktop (full installation)',
        'base': ['base', 'base-devel', 'linux', 'linux-firmware'],
        'essential': ['networkmanager', 'wireless_tools', 'wpa_supplicant',
                      'dialog', 'sudo', 'git', 'reflector'],
        'extra': ['firefox', 'file-roller', 'pulseaudio', 'alsa-utils',
                  'xdg-user-dirs', 'ttf-dejavu', 'noto-fonts', 'vim'],
        'description': 'profile_desktop'
    },
    'minimal': {
        'name': 'Minimal (minimal system)',
        'base': ['base', 'linux', 'linux-firmware'],
        'essential': ['networkmanager', 'sudo', 'nano'],
        'extra': [],
        'description': 'profile_minimal'
    },
    'server': {
        'name': 'Server (server configuration)',
        'base': ['base', 'linux', 'linux-firmware'],
        'essential': ['networkmanager', 'openssh', 'sudo', 'htop', 'tmux'],
        'extra': ['curl', 'wget', 'git'],
        'description': 'profile_server'
    },
    'xorg': {
        'name': 'Xorg (basic graphics)',
        'base': ['base', 'base-devel', 'linux', 'linux-firmware'],
        'essential': ['xorg-server', 'xorg-xinit', 'networkmanager', 'sudo'],
        'extra': ['xterm', 'firefox', 'vim'],
        'description': 'profile_xorg'
    }
}

# Дополнительные пакеты по категориям
ADDITIONAL_PACKAGES = {
    'browsers': {
        'firefox': 'Firefox',
        'chromium': 'Chromium',
        'brave': 'Brave',
        'midori': 'Midori',
    },
    'development': {
        'base-devel': 'Build tools (gcc, make, etc.)',
        'code': 'Visual Studio Code',
        'python': 'Python',
        'python-pip': 'Python package manager',
        'nodejs': 'Node.js',
        'npm': 'Node package manager',
        'git': 'Git version control',
        'docker': 'Docker',
        'docker-compose': 'Docker Compose',
    },
    'multimedia': {
        'vlc': 'VLC media player',
        'gimp': 'GIMP image editor',
        'inkscape': 'Inkscape vector graphics',
        'obs-studio': 'OBS Studio (streaming)',
        'audacity': 'Audacity audio editor',
        'blender': 'Blender 3D graphics',
    },
    'utilities': {
        'git': 'Git',
        'vim': 'Vim text editor',
        'neovim': 'Neovim',
        'htop': 'System monitor',
        'tmux': 'Terminal multiplexer',
        'rsync': 'File synchronization',
        'curl': 'cURL',
        'wget': 'Wget',
        'unzip': 'Unzip utility',
        'p7zip': '7-Zip utility',
        'openssh': 'SSH client/server',
    },
    'documents': {
        'libreoffice-fresh': 'LibreOffice',
        'thunderbird': 'Email client',
        'evince': 'Document viewer',
    },
    'system': {
        'man-db': 'Manual pages',
        'man-pages': 'Manual page content',
        'pacman-contrib': 'Pacman utilities',
        'powertop': 'Power consumption monitor',
        'nvtop': 'GPU monitor',
    }
}

def select_installation_profile(dialog) -> Optional[str]:
    """
    Выбрать профиль установки через dialog.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Ключ выбранного профиля или None
    """
    choices = []
    
    for key, profile in INSTALLATION_PROFILES.items():
        desc = t(profile['description'])
        choices.append((key, desc))
    
    result = dialog.radiolist('select_profile', choices, height=15, width=70)
    
    if result:
        logger.info(f"Installation profile selected: {result}")
        return result
    
    return 'desktop'

def get_profile_packages(profile_key: str) -> List[str]:
    """
    Получить все пакеты для профиля.
    
    Args:
        profile_key: Ключ профиля
    
    Returns:
        Список пакетов
    """
    if profile_key not in INSTALLATION_PROFILES:
        profile_key = 'desktop'
    
    profile = INSTALLATION_PROFILES[profile_key]
    return profile['base'] + profile['essential'] + profile['extra']

def select_additional_packages(dialog) -> List[str]:
    """
    Выбрать дополнительные пакеты через checklist.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Список выбранных пакетов
    """
    selected_packages = []
    
    for category, packages in ADDITIONAL_PACKAGES.items():
        choices = [(pkg, name, 0) for pkg, name in packages.items()]
        
        result = dialog.checklist(
            f"Additional packages - {category}",
            choices,
            height=15,
            width=70
        )
        
        if result:
            selected_packages.extend(result)
    
    logger.info(f"Additional packages selected: {selected_packages}")
    return selected_packages

def install_packages(packages: List[str], mount_point: str = '/mnt') -> bool:
    """
    Установить пакеты в chroot.
    
    Args:
        packages: Список пакетов для установки
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        if not packages:
            logger.info("No packages to install")
            return True
        
        logger.info(f"Installing {len(packages)} packages")
        
        packages_str = ' '.join(packages)
        cmd = f"arch-chroot {mount_point} pacman -S {packages_str} --noconfirm"
        
        run_command(cmd, check=True, log=True)
        
        logger.info("Packages installed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to install packages: {e}")
        return False

def enable_multilib(mount_point: str = '/mnt') -> bool:
    """
    Включить multilib репозиторий (32-битные библиотеки).
    
    Args:
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info("Enabling multilib repository")
        
        # Раскомментировать multilib в /etc/pacman.conf
        run_command(
            f"sed -i '/^#\\[multilib\\]/,/^#Include = \\/etc\\/pacman.d\\/mirrorlist/ "
            f"s/^#//' {mount_point}/etc/pacman.conf",
            check=False,
            log=True
        )
        
        # Обновить базы данных
        run_command(
            f"arch-chroot {mount_point} pacman -Sy",
            check=True,
            log=True
        )
        
        logger.info("Multilib enabled successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to enable multilib: {e}")
        return False

def setup_aur_helper(helper: str, mount_point: str = '/mnt') -> bool:
    """
    Установить AUR helper (yay или paru).
    
    Args:
        helper: 'yay' или 'paru'
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        if helper not in ['yay', 'paru']:
            logger.warning(f"Unknown AUR helper: {helper}")
            return False
        
        logger.info(f"Installing AUR helper: {helper}")
        
        # Установить зависимости
        if helper == 'yay':
            packages = ['git', 'base-devel']
            packages_str = ' '.join(packages)
            run_command(
                f"arch-chroot {mount_point} pacman -S {packages_str} --noconfirm",
                check=True,
                log=True
            )
            
            # Клонировать и собрать yay
            run_command(
                f"arch-chroot {mount_point} bash -c 'cd /tmp && "
                f"git clone https://aur.archlinux.org/yay-bin.git && "
                f"cd yay-bin && makepkg -si --noconfirm'",
                check=True,
                log=True
            )
        
        elif helper == 'paru':
            packages = ['git', 'base-devel', 'rust']
            packages_str = ' '.join(packages)
            run_command(
                f"arch-chroot {mount_point} pacman -S {packages_str} --noconfirm",
                check=True,
                log=True
            )
            
            # Клонировать и собрать paru
            run_command(
                f"arch-chroot {mount_point} bash -c 'cd /tmp && "
                f"git clone https://aur.archlinux.org/paru-bin.git && "
                f"cd paru-bin && makepkg -si --noconfirm'",
                check=True,
                log=True
            )
        
        logger.info(f"AUR helper {helper} installed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to install AUR helper: {e}")
        return False

def update_mirrors(mount_point: str = '/mnt') -> bool:
    """
    Обновить список зеркал через reflector.
    
    Args:
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info("Updating mirrors with reflector")
        
        # Установить reflector если нет
        run_command(
            f"arch-chroot {mount_point} pacman -S reflector --noconfirm",
            check=False,
            log=False
        )
        
        # Запустить reflector
        run_command(
            f"arch-chroot {mount_point} reflector --latest 20 --sort rate "
            f"--save /etc/pacman.d/mirrorlist",
            check=True,
            log=True
        )
        
        logger.info("Mirrors updated successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to update mirrors: {e}")
        return False
