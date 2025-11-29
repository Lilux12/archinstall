"""
Глобальные конфигурации и переменные установщика.
Система мультиязычности (i18n).
"""

import os
from typing import Dict, Any

# ============================================================================
# ВЕРСИЯ И ИНФОРМАЦИЯ
# ============================================================================
APP_VERSION = "2.0"
APP_NAME = "Arch Linux Automated Installer"
APP_AUTHOR = "Arch Community"
LOG_DIR = "/var/log"
LOG_FILE = os.path.join(LOG_DIR, "archinstall.log")

# ============================================================================
# ТЕКУЩИЙ ЯЗЫК И ПЕРЕВОДЫ
# ============================================================================
CURRENT_LANG = 'ru'  # По умолчанию русский

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    'ru': {
        # Основные сообщения
        'welcome': 'Добро пожаловать в установщик Arch Linux',
        'welcome_subtitle': f'Версия {APP_VERSION} - Профессиональный автоматический установщик',
        'select_language': 'Выберите язык интерфейса',
        'select_disk': 'Выберите диск для установки',
        'warning_data_loss': '⚠️  ПРЕДУПРЕЖДЕНИЕ: ВСЕ ДАННЫЕ БУДУТ УДАЛЕНЫ!',
        'confirm_disk': 'Вы уверены? Это необратимая операция!',
        'disk_selected': 'Диск выбран',
        
        # Разметка диска
        'partition_scheme': 'Выберите схему разметки',
        'auto_ext4': 'Автоматическая (ext4)',
        'auto_btrfs': 'Автоматическая (btrfs)',
        'manual': 'Ручная разметка',
        'scheme_description': 'Описание схемы:',
        'uefi_mode': 'Режим загрузки: UEFI',
        'bios_mode': 'Режим загрузки: BIOS',
        
        # Видеокарта
        'select_gpu': 'Выберите драйверы видеокарты',
        'gpu_detected': 'Обнаружена видеокарта:',
        'gpu_auto_select': 'Автоматический выбор',
        'nvidia_proprietary': 'NVIDIA (проприетарные драйверы)',
        'nvidia_opensource': 'NVIDIA (Nouveau open-source)',
        'amd_drivers': 'AMD (open-source)',
        'intel_drivers': 'Intel (встроенная графика)',
        'gpu_hybrid': 'Гибридная графика',
        'generic_drivers': 'Базовые драйверы',
        
        # Desktop Environment
        'select_desktop': 'Выберите Desktop Environment',
        'kde_plasma': 'KDE Plasma - современное полнофункциональное окружение',
        'gnome': 'GNOME - элегантный и простой интерфейс',
        'xfce': 'XFCE - легковесное и быстрое окружение',
        'cinnamon': 'Cinnamon - традиционный рабочий стол',
        'mate': 'MATE - классическое окружение',
        'i3wm': 'i3wm - тайловый менеджер окон',
        'sway': 'Sway - Wayland тайловый композитор',
        'no_de': 'Только командная строка (серверная установка)',
        'ram_required': 'Требуемая RAM:',
        'disk_space': 'Место на диске:',
        
        # Раскладки
        'select_layouts': 'Выберите раскладки клавиатуры',
        'keyboard_layout': 'Основная раскладка:',
        'add_more_layouts': 'Добавить ещё раскладку?',
        'switch_combination': 'Комбинация переключения:',
        'alt_shift': 'Alt + Shift',
        'ctrl_shift': 'Ctrl + Shift',
        'caps_lock': 'CapsLock',
        'search_layout': 'Найти раскладку:',
        
        # Профили
        'select_profile': 'Выберите профиль установки',
        'profile_desktop': 'Desktop - полная установка',
        'profile_minimal': 'Minimal - минимальная система',
        'profile_server': 'Server - серверная конфигурация',
        'profile_xorg': 'Xorg - базовая графика',
        
        # Сеть и пользователи
        'hostname': 'Hostname:',
        'enter_hostname': 'Введите имя компьютера',
        'select_network_manager': 'Выберите сетевой менеджер',
        'networkmanager': 'NetworkManager (рекомендуется)',
        'systemd_networkd': 'systemd-networkd (серверы)',
        'iwd': 'iwd (минимализм)',
        
        'root_password': 'Пароль администратора (root)',
        'enter_root_password': 'Введите пароль для root:',
        'confirm_password': 'Подтверждение пароля:',
        'passwords_dont_match': 'Пароли не совпадают!',
        'password_empty': 'Пароль не может быть пустым!',
        
        'username': 'Имя пользователя:',
        'enter_username': 'Введите имя пользователя:',
        'user_password': 'Пароль пользователя:',
        'user_groups': 'Группы пользователя:',
        'wheel_group': 'wheel (доступ к sudo)',
        'audio_group': 'audio',
        'video_group': 'video',
        'storage_group': 'storage',
        'docker_group': 'docker',
        'kvm_group': 'kvm',
        
        # Дополнительные настройки
        'additional_settings': 'Дополнительные настройки',
        'timezone': 'Часовой пояс:',
        'select_timezone': 'Выберите часовой пояс',
        'locale': 'Локали:',
        'multilib': 'Multilib (32-битные библиотеки)',
        'aur_helper': 'Помощник AUR:',
        'enable_aur': 'Включить AUR?',
        'yay': 'yay (рекомендуется)',
        'paru': 'paru (на Rust)',
        'no_aur': 'Без помощника AUR',
        'enable_reflector': 'Автоматизировать выбор зеркал',
        'swap_size': 'Размер swap-файла (GB):',
        
        # Дополнительные пакеты
        'additional_packages': 'Дополнительные пакеты',
        'browsers': 'Браузеры:',
        'firefox': 'Firefox',
        'chromium': 'Chromium',
        'brave': 'Brave',
        'development': 'Разработка:',
        'vscode': 'Visual Studio Code',
        'python': 'Python',
        'nodejs': 'Node.js',
        'docker': 'Docker',
        'multimedia': 'Мультимедиа:',
        'vlc': 'VLC',
        'gimp': 'GIMP',
        'inkscape': 'Inkscape',
        'obs': 'OBS Studio',
        'utilities': 'Утилиты:',
        'git': 'Git',
        'vim': 'Vim/Neovim',
        'htop': 'htop',
        'tmux': 'tmux',
        'rsync': 'rsync',
        
        # Загрузчик
        'select_bootloader': 'Выберите загрузчик',
        'grub': 'GRUB',
        'systemd_boot': 'systemd-boot',
        
        # Финальный обзор
        'final_review': 'Итоговая конфигурация установки',
        'start_installation': 'Начать установку',
        'save_config': 'Сохранить конфиг',
        'load_config': 'Загрузить конфиг',
        'back': 'Назад',
        'cancel': 'Отмена',
        'exit': 'Выход',
        
        # Установка
        'installation_progress': 'Прогресс установки',
        'formatting_disk': 'Форматирование диска...',
        'mounting_partitions': 'Монтирование разделов...',
        'updating_mirrors': 'Обновление списка зеркал...',
        'installing_base': 'Установка базовой системы...',
        'installing_kernel': 'Установка ядра...',
        'generating_fstab': 'Генерация fstab...',
        'configuring_locale': 'Настройка локали...',
        'configuring_timezone': 'Настройка часового пояса...',
        'setting_hostname': 'Установка hostname...',
        'installing_bootloader': 'Установка загрузчика...',
        'installing_gpu_drivers': 'Установка видеодрайверов...',
        'installing_desktop': 'Установка Desktop Environment...',
        'creating_users': 'Создание пользователей...',
        'installing_packages': 'Установка дополнительных пакетов...',
        'enabling_services': 'Включение сервисов...',
        'installation_complete': 'Установка завершена!',
        
        # Ошибки
        'error': 'Ошибка',
        'error_internet': 'Нет подключения к интернету!',
        'error_root': 'Этот скрипт должен быть запущен от root!',
        'error_invalid_input': 'Некорректный ввод!',
        'error_disk_not_found': 'Диск не найден!',
        'error_hostname_invalid': 'Некорректный hostname!',
        'error_username_invalid': 'Некорректное имя пользователя!',
        'error_partition_failed': 'Ошибка при разметке диска!',
        'error_installation_failed': 'Ошибка при установке!',
        
        # Успех
        'success': 'Успешно',
        'success_installation': 'Система установлена успешно!',
        'reboot_now': 'Перезагрузить сейчас?',
        'stay_in_livecd': 'Остаться в LiveCD',
        'open_chroot': 'Открыть chroot для ручных настроек',
        'view_logs': 'Посмотреть логи установки',
        
        # Главное меню
        'main_menu': 'Главное меню',
        'language': '1. Язык интерфейса',
        'disk': '2. Выбор диска',
        'partitioning': '3. Схема разметки',
        'graphics': '4. Видеокарта',
        'desktop_env': '5. Окружение рабочего стола',
        'keyboard': '6. Раскладки клавиатуры',
        'installation_profile': '7. Профиль установки',
        'network': '8. Сеть',
        'users': '9. Пользователи',
        'additional': '10. Дополнительно',
        'not_selected': 'Не выбрано',
        'auto_detected': 'Автоопределение',
        
        # Проверки
        'checking_prerequisites': 'Проверка предварительных условий...',
        'checking_internet': 'Проверка интернета...',
        'checking_pacman_keys': 'Инициализация ключей pacman...',
        'prerequisite_failed': 'Проверка не пройдена:',
    },
    'en': {
        # Basic messages
        'welcome': 'Welcome to Arch Linux Installer',
        'welcome_subtitle': f'Version {APP_VERSION} - Professional Automated Installer',
        'select_language': 'Select interface language',
        'select_disk': 'Select installation disk',
        'warning_data_loss': '⚠️  WARNING: ALL DATA WILL BE ERASED!',
        'confirm_disk': 'Are you sure? This is an irreversible operation!',
        'disk_selected': 'Disk selected',
        
        # Disk partitioning
        'partition_scheme': 'Select partitioning scheme',
        'auto_ext4': 'Automatic (ext4)',
        'auto_btrfs': 'Automatic (btrfs)',
        'manual': 'Manual partitioning',
        'scheme_description': 'Scheme description:',
        'uefi_mode': 'Boot mode: UEFI',
        'bios_mode': 'Boot mode: BIOS',
        
        # GPU
        'select_gpu': 'Select graphics drivers',
        'gpu_detected': 'Graphics card detected:',
        'gpu_auto_select': 'Auto-select',
        'nvidia_proprietary': 'NVIDIA (proprietary drivers)',
        'nvidia_opensource': 'NVIDIA (Nouveau open-source)',
        'amd_drivers': 'AMD (open-source)',
        'intel_drivers': 'Intel (integrated graphics)',
        'gpu_hybrid': 'Hybrid graphics',
        'generic_drivers': 'Basic drivers',
        
        # Desktop Environment
        'select_desktop': 'Select Desktop Environment',
        'kde_plasma': 'KDE Plasma - modern full-featured environment',
        'gnome': 'GNOME - elegant and simple interface',
        'xfce': 'XFCE - lightweight and fast environment',
        'cinnamon': 'Cinnamon - traditional desktop',
        'mate': 'MATE - classic environment',
        'i3wm': 'i3wm - tiling window manager',
        'sway': 'Sway - Wayland tiling compositor',
        'no_de': 'Command-line only (server installation)',
        'ram_required': 'Required RAM:',
        'disk_space': 'Disk space:',
        
        # Keyboard layouts
        'select_layouts': 'Select keyboard layouts',
        'keyboard_layout': 'Main layout:',
        'add_more_layouts': 'Add more layout?',
        'switch_combination': 'Switch combination:',
        'alt_shift': 'Alt + Shift',
        'ctrl_shift': 'Ctrl + Shift',
        'caps_lock': 'CapsLock',
        'search_layout': 'Find layout:',
        
        # Profiles
        'select_profile': 'Select installation profile',
        'profile_desktop': 'Desktop - full installation',
        'profile_minimal': 'Minimal - minimal system',
        'profile_server': 'Server - server configuration',
        'profile_xorg': 'Xorg - basic graphics',
        
        # Network and users
        'hostname': 'Hostname:',
        'enter_hostname': 'Enter computer name',
        'select_network_manager': 'Select network manager',
        'networkmanager': 'NetworkManager (recommended)',
        'systemd_networkd': 'systemd-networkd (servers)',
        'iwd': 'iwd (minimalist)',
        
        'root_password': 'Root password',
        'enter_root_password': 'Enter root password:',
        'confirm_password': 'Confirm password:',
        'passwords_dont_match': 'Passwords do not match!',
        'password_empty': 'Password cannot be empty!',
        
        'username': 'Username:',
        'enter_username': 'Enter username:',
        'user_password': 'User password:',
        'user_groups': 'User groups:',
        'wheel_group': 'wheel (sudo access)',
        'audio_group': 'audio',
        'video_group': 'video',
        'storage_group': 'storage',
        'docker_group': 'docker',
        'kvm_group': 'kvm',
        
        # Additional settings
        'additional_settings': 'Additional settings',
        'timezone': 'Timezone:',
        'select_timezone': 'Select timezone',
        'locale': 'Locales:',
        'multilib': 'Multilib (32-bit libraries)',
        'aur_helper': 'AUR helper:',
        'enable_aur': 'Enable AUR?',
        'yay': 'yay (recommended)',
        'paru': 'paru (Rust-based)',
        'no_aur': 'No AUR helper',
        'enable_reflector': 'Automate mirror selection',
        'swap_size': 'Swap file size (GB):',
        
        # Additional packages
        'additional_packages': 'Additional packages',
        'browsers': 'Browsers:',
        'firefox': 'Firefox',
        'chromium': 'Chromium',
        'brave': 'Brave',
        'development': 'Development:',
        'vscode': 'Visual Studio Code',
        'python': 'Python',
        'nodejs': 'Node.js',
        'docker': 'Docker',
        'multimedia': 'Multimedia:',
        'vlc': 'VLC',
        'gimp': 'GIMP',
        'inkscape': 'Inkscape',
        'obs': 'OBS Studio',
        'utilities': 'Utilities:',
        'git': 'Git',
        'vim': 'Vim/Neovim',
        'htop': 'htop',
        'tmux': 'tmux',
        'rsync': 'rsync',
        
        # Bootloader
        'select_bootloader': 'Select bootloader',
        'grub': 'GRUB',
        'systemd_boot': 'systemd-boot',
        
        # Final review
        'final_review': 'Final installation configuration',
        'start_installation': 'Start installation',
        'save_config': 'Save config',
        'load_config': 'Load config',
        'back': 'Back',
        'cancel': 'Cancel',
        'exit': 'Exit',
        
        # Installation
        'installation_progress': 'Installation progress',
        'formatting_disk': 'Formatting disk...',
        'mounting_partitions': 'Mounting partitions...',
        'updating_mirrors': 'Updating mirror list...',
        'installing_base': 'Installing base system...',
        'installing_kernel': 'Installing kernel...',
        'generating_fstab': 'Generating fstab...',
        'configuring_locale': 'Configuring locale...',
        'configuring_timezone': 'Configuring timezone...',
        'setting_hostname': 'Setting hostname...',
        'installing_bootloader': 'Installing bootloader...',
        'installing_gpu_drivers': 'Installing GPU drivers...',
        'installing_desktop': 'Installing Desktop Environment...',
        'creating_users': 'Creating users...',
        'installing_packages': 'Installing additional packages...',
        'enabling_services': 'Enabling services...',
        'installation_complete': 'Installation complete!',
        
        # Errors
        'error': 'Error',
        'error_internet': 'No internet connection!',
        'error_root': 'This script must be run as root!',
        'error_invalid_input': 'Invalid input!',
        'error_disk_not_found': 'Disk not found!',
        'error_hostname_invalid': 'Invalid hostname!',
        'error_username_invalid': 'Invalid username!',
        'error_partition_failed': 'Disk partitioning failed!',
        'error_installation_failed': 'Installation failed!',
        
        # Success
        'success': 'Success',
        'success_installation': 'System installed successfully!',
        'reboot_now': 'Reboot now?',
        'stay_in_livecd': 'Stay in LiveCD',
        'open_chroot': 'Open chroot for manual configuration',
        'view_logs': 'View installation logs',
        
        # Main menu
        'main_menu': 'Main menu',
        'language': '1. Interface language',
        'disk': '2. Select disk',
        'partitioning': '3. Partitioning scheme',
        'graphics': '4. Graphics card',
        'desktop_env': '5. Desktop environment',
        'keyboard': '6. Keyboard layouts',
        'installation_profile': '7. Installation profile',
        'network': '8. Network',
        'users': '9. Users',
        'additional': '10. Additional',
        'not_selected': 'Not selected',
        'auto_detected': 'Auto-detected',
        
        # Checks
        'checking_prerequisites': 'Checking prerequisites...',
        'checking_internet': 'Checking internet...',
        'checking_pacman_keys': 'Initializing pacman keys...',
        'prerequisite_failed': 'Prerequisite check failed:',
    }
}

def t(key: str, lang: str = None) -> str:
    """
    Получить перевод по ключу.
    
    Args:
        key: Ключ перевода
        lang: Язык (если None, используется CURRENT_LANG)
    
    Returns:
        Переведенная строка или ключ если не найдено
    """
    if lang is None:
        lang = CURRENT_LANG
    
    if lang in TRANSLATIONS and key in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang][key]
    return key

# ============================================================================
# КОНФИГУРАЦИЯ УСТАНОВКИ
# ============================================================================
class InstallationConfig:
    """Глобальная конфигурация установки."""
    
    def __init__(self):
        # Язык
        self.language = 'ru'
        
        # Диск
        self.disk = None
        self.partition_scheme = None
        self.is_uefi = False
        
        # Видеокарта
        self.gpu_vendor = None
        self.gpu_model = None
        self.gpu_driver = None
        
        # Desktop Environment
        self.desktop_environment = None
        self.display_manager = None
        
        # Раскладки
        self.keyboard_layouts = ['us']
        self.keyboard_switch = 'alt_shift'
        
        # Профиль установки
        self.installation_profile = 'desktop'
        
        # Сеть
        self.hostname = 'archlinux'
        self.network_manager = 'networkmanager'
        
        # Пользователи
        self.root_password = None
        self.username = None
        self.user_password = None
        self.user_groups = ['wheel', 'audio', 'video', 'storage', 'optical']
        
        # Дополнительные настройки
        self.timezone = 'UTC'
        self.locale = ['en_US.UTF-8']
        self.multilib = False
        self.aur_helper = None
        self.swap_size = 2
        self.use_reflector = True
        
        # Дополнительные пакеты
        self.additional_packages = []
        
        # Загрузчик
        self.bootloader = 'grub'
        
        # Статус установки
        self.installation_started = False
        self.installation_completed = False

# Глобальный экземпляр конфигурации
config = InstallationConfig()
