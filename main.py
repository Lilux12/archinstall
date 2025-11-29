#!/usr/bin/env python3
"""
Arch Linux Automated Installer v2.0
Главная точка входа установщика.
"""

import sys
import os
import json
import argparse
from datetime import datetime

from config import config, CURRENT_LANG, TRANSLATIONS, t, APP_VERSION, APP_NAME
from utils.logger import logger
from utils.validators import check_all_prerequisites
from utils.system import print_system_info
from ui.dialogs import get_dialog
from ui.progress import get_progress

from installer.disk import detect_disks, select_disk, detect_boot_mode, select_partition_scheme, setup_swap, create_partitions, generate_fstab
from installer.graphics import detect_gpu, select_gpu_driver, install_gpu_drivers
from installer.desktop import select_desktop_environment, install_desktop_environment
from installer.localization import configure_keyboards, select_timezone, configure_locales, set_timezone, generate_locale, set_keyboard_layout, configure_x11_keyboard
from installer.packages import select_installation_profile, get_profile_packages, select_additional_packages, install_packages, enable_multilib, setup_aur_helper, update_mirrors
from installer.network import configure_hostname, select_network_manager, set_hostname, install_network_manager
from installer.users import set_root_password, create_user, set_root_password_system, create_user_system, setup_sudo
from installer.bootloader import detect_boot_mode as detect_boot_mode_bl, select_bootloader, install_bootloader

# ASCII Art логотип
ARCH_LOGO = r"""
                   -`
                  .o+`
                 `ooo/
                `+oooo:
               `+oooooo:
               -+oooooo+:
             `/:-:++oooo+:
            `/++++/+++++++:
           `/++++++++++++++:
          `/+++ooooooooooooo/`
         ./ooosssso++osssssso+`
        .oossssso-````/ossssss+`
       -osssssso.      :ssssssso.
      :osssssss/        osssso+++.
     /ossssssss/        +ssssooo/-
   `/ossssso+/:-        -:/+osssso+-
  `+sso+:-`                 `.-/+oso:
 `++:.                           `-/+/
 .`                                 `/

 ╔═══════════════════════════════════════╗
 ║   Arch Linux Automated Installer      ║
 ║            Version 2.0                ║
 ╚═══════════════════════════════════════╝
"""

def show_welcome(dialog):
    """Показать приветственное окно."""
    welcome_text = f"""
{ARCH_LOGO}

{t('welcome')}
{t('welcome_subtitle')}

Нажмите Enter для начала...
"""
    dialog.msgbox('welcome', height=25, width=80)

def select_language(dialog) -> str:
    """Выбрать язык интерфейса."""
    choices = [
        ('ru', 'Русский', 1),
        ('en', 'English', 0)
    ]
    
    result = dialog.radiolist('select_language', choices)
    return result if result else 'ru'

def main_menu(dialog) -> None:
    """
    Главное меню установки.
    Показывает статус каждого этапа.
    """
    while True:
        # Подготовить информацию о выборах
        disk_info = config.disk if config.disk else t('not_selected')
        partition_info = config.partition_scheme if config.partition_scheme else t('not_selected')
        gpu_info = config.gpu_driver if config.gpu_driver else t('auto_detected')
        desktop_info = config.desktop_environment if config.desktop_environment else t('not_selected')
        keyboard_info = f"{', '.join(config.keyboard_layouts)}" if config.keyboard_layouts else t('not_selected')
        profile_info = config.installation_profile if config.installation_profile else t('not_selected')
        hostname_info = config.hostname if config.hostname else t('not_selected')
        users_info = config.username if config.username else t('not_selected')
        
        # Формировать текст меню
        menu_text = f"""
╔════════════════════════════════════════╗
║   {t('main_menu')}            ║
╠════════════════════════════════════════╣
║ ✓ 1. {t('language'):25} [{t('not_selected')}]
║ ✓ 2. {t('disk'):25} [{disk_info[:15]}]
║ ○ 3. {t('partitioning'):25} [{partition_info[:15]}]
║ ○ 4. {t('graphics'):25} [{gpu_info[:15]}]
║ ○ 5. {t('desktop_env'):25} [{desktop_info[:15]}]
║ ○ 6. {t('keyboard'):25} [{keyboard_info[:15]}]
║ ○ 7. {t('installation_profile')}  [{profile_info[:15]}]
║ ○ 8. {t('network'):25} [{hostname_info[:15]}]
║ ○ 9. {t('users'):25} [{users_info[:15]}]
║ ○ 10. {t('additional'):25} [Customize]
╠════════════════════════════════════════╣
║ [1-10: Select] [I: Install] [S: Save] ║
║ [L: Load] [E: Exit]                   ║
╚════════════════════════════════════════╝
"""
        
        dialog.msgbox(menu_text, height=25, width=80)
        
        # Получить выбор от пользователя (в простой версии используем меню)
        choices = [
            ('1', t('language')),
            ('2', t('disk')),
            ('3', t('partitioning')),
            ('4', t('graphics')),
            ('5', t('desktop_env')),
            ('6', t('keyboard')),
            ('7', t('installation_profile')),
            ('8', t('network')),
            ('9', t('users')),
            ('10', t('additional')),
            ('i', t('start_installation')),
            ('s', t('save_config')),
            ('l', t('load_config')),
            ('e', t('exit')),
        ]
        
        result = dialog.menu(t('main_menu'), choices, height=20, width=60)
        
        if result == '1':
            # Выбор языка
            lang = select_language(dialog)
            if lang:
                config.language = lang
                # TODO: Переинициализировать диалог с новым языком
        
        elif result == '2':
            # Выбор диска
            disk = select_disk(dialog)
            if disk:
                config.disk = disk
        
        elif result == '3':
            # Выбор схемы разметки
            if not config.disk:
                dialog.msgbox('error_disk_not_found')
                continue
            
            config.is_uefi = detect_boot_mode()
            scheme = select_partition_scheme(dialog)
            if scheme:
                config.partition_scheme = scheme
                swap_config = setup_swap(dialog)
                if swap_config:
                    config.swap_size = swap_config.get('size_gb', 2)
        
        elif result == '4':
            # Выбор видеодрайвера
            detected = detect_gpu()
            config.gpu_model = f"{detected['vendor']} {detected['model']}"
            driver = select_gpu_driver(dialog, detected)
            if driver:
                config.gpu_driver = driver
        
        elif result == '5':
            # Выбор Desktop Environment
            de = select_desktop_environment(dialog)
            if de:
                config.desktop_environment = de
        
        elif result == '6':
            # Настройка раскладок
            kb_config = configure_keyboards(dialog)
            if kb_config:
                config.keyboard_layouts = kb_config['layouts']
                config.keyboard_switch = kb_config['switch']
        
        elif result == '7':
            # Выбор профиля установки
            profile = select_installation_profile(dialog)
            if profile:
                config.installation_profile = profile
        
        elif result == '8':
            # Настройка сети
            hostname = configure_hostname(dialog)
            if hostname:
                config.hostname = hostname
            
            nm = select_network_manager(dialog)
            if nm:
                config.network_manager = nm
        
        elif result == '9':
            # Создание пользователя
            root_pass = set_root_password(dialog)
            if root_pass:
                config.root_password = root_pass
            
            user_info = create_user(dialog)
            if user_info:
                config.username = user_info['username']
                config.user_password = user_info['password']
                config.user_groups = user_info['groups']
        
        elif result == '10':
            # Дополнительные настройки
            timezone = select_timezone(dialog)
            if timezone:
                config.timezone = timezone
            
            locales = configure_locales(dialog)
            if locales:
                config.locale = locales
            
            # Multilib
            if dialog.yesno('multilib'):
                config.multilib = True
            
            # AUR helper
            aur_choices = [
                ('yay', 'yay'),
                ('paru', 'paru'),
                ('none', t('no_aur'))
            ]
            aur = dialog.radiolist('enable_aur', aur_choices)
            if aur and aur != 'none':
                config.aur_helper = aur
        
        elif result == 'i':
            # Начать установку
            if final_review(dialog):
                install_system(dialog)
                break
        
        elif result == 's':
            # Сохранить конфиг
            save_config()
        
        elif result == 'l':
            # Загрузить конфиг
            load_config()
        
        elif result == 'e' or result is None:
            # Выход
            if dialog.yesno('Do you really want to exit?'):
                break

def final_review(dialog) -> bool:
    """
    Финальный обзор конфигурации перед установкой.
    
    Returns:
        True если пользователь подтвердил установку
    """
    review_text = f"""
╔════════════════════════════════════════╗
║   {t('final_review')}     ║
╠════════════════════════════════════════╣
║ Диск:            {config.disk}
║ Схема разметки:  {config.partition_scheme}
║ Загрузка:        {'UEFI' if config.is_uefi else 'BIOS'}
║ Видеокарта:      {config.gpu_driver}
║ Desktop:         {config.desktop_environment}
║ Раскладки:       {', '.join(config.keyboard_layouts)}
║ Профиль:         {config.installation_profile}
║ Hostname:        {config.hostname}
║ Пользователь:    {config.username}
║ Часовой пояс:    {config.timezone}
║ Локали:          {', '.join(config.locale)}
║ Multilib:        {'Да' if config.multilib else 'Нет'}
║ AUR helper:      {config.aur_helper or 'Нет'}
╚════════════════════════════════════════╝

Все параметры правильны?
"""
    
    logger.info("Final review shown to user")
    return dialog.yesno('Do you confirm these settings?')

def install_system(dialog) -> None:
    """Главная функция установки системы."""
    logger.info("Starting installation...")
    config.installation_started = True
    
    progress = get_progress('install')
    progress.start('installation_progress')
    
    try:
        # 1. Подготовка диска
        progress.next_stage()
        if not create_partitions(config.disk, config.partition_scheme, config.is_uefi):
            raise Exception("Failed to partition disk")
        
        # 2. Монтирование
        progress.next_stage()
        
        # 3. Обновление зеркал
        progress.next_stage()
        if config.use_reflector:
            update_mirrors()
        
        # 4. Установка базовой системы
        progress.next_stage()
        base_packages = ['base', 'linux', 'linux-firmware']
        if not install_packages(base_packages):
            raise Exception("Failed to install base system")
        
        # 5-6. Ядро и fstab
        progress.next_stage()
        progress.next_stage()
        if not generate_fstab():
            raise Exception("Failed to generate fstab")
        
        # 7-9. Локализация
        progress.next_stage()
        progress.next_stage()
        progress.next_stage()
        
        if not generate_locale(config.locale):
            raise Exception("Failed to generate locales")
        
        if not set_timezone(config.timezone):
            raise Exception("Failed to set timezone")
        
        # 10. Hostname
        progress.next_stage()
        if not set_hostname(config.hostname):
            raise Exception("Failed to set hostname")
        
        # 11. Загрузчик
        progress.next_stage()
        bootloader = select_bootloader(dialog, config.is_uefi)
        if not install_bootloader(bootloader, config.disk, config.is_uefi):
            raise Exception("Failed to install bootloader")
        
        # 12. Видеодрайверы
        progress.next_stage()
        if config.gpu_driver:
            if not install_gpu_drivers(config.gpu_driver):
                logger.warning("GPU driver installation failed, continuing...")
        
        # 13. Desktop Environment
        progress.next_stage()
        if config.desktop_environment:
            if not install_desktop_environment(config.desktop_environment):
                logger.warning("Desktop installation failed, continuing...")
        
        # 14. Пользователи
        progress.next_stage()
        if not set_root_password_system(config.root_password):
            raise Exception("Failed to set root password")
        
        if config.username:
            user_info = {
                'username': config.username,
                'password': config.user_password,
                'groups': config.user_groups
            }
            if not create_user_system(user_info):
                raise Exception("Failed to create user")
            
            if not setup_sudo():
                logger.warning("Sudo setup failed")
        
        # 15. Дополнительные пакеты
        progress.next_stage()
        profile_packages = get_profile_packages(config.installation_profile)
        if not install_packages(profile_packages):
            logger.warning("Package installation failed")
        
        # 16. Сервисы
        progress.next_stage()
        if config.network_manager:
            if not install_network_manager(config.network_manager):
                logger.warning("Network manager installation failed")
        
        # Завершение
        progress.set_percent(100, 'installation_complete')
        progress.stop()
        
        logger.info("Installation completed successfully!")
        config.installation_completed = True
        
        dialog.msgbox('success_installation')
        
        # Предложить варианты
        post_install(dialog)
    
    except Exception as e:
        logger.error(f"Installation failed: {e}")
        progress.stop()
        dialog.msgbox(f"Installation failed: {str(e)}")

def post_install(dialog) -> None:
    """Опции после установки."""
    choices = [
        ('reboot', t('reboot_now')),
        ('stay', t('stay_in_livecd')),
        ('chroot', t('open_chroot')),
        ('logs', t('view_logs')),
    ]
    
    result = dialog.menu('Installation complete', choices)
    
    if result == 'reboot':
        os.system('reboot')
    elif result == 'chroot':
        os.system('arch-chroot /mnt')
    elif result == 'logs':
        dialog.textbox('/var/log/archinstall.log')

def save_config() -> None:
    """Сохранить конфигурацию в YAML."""
    config_dict = {
        'language': config.language,
        'disk': config.disk,
        'partition_scheme': config.partition_scheme,
        'is_uefi': config.is_uefi,
        'gpu_driver': config.gpu_driver,
        'desktop_environment': config.desktop_environment,
        'keyboard_layouts': config.keyboard_layouts,
        'keyboard_switch': config.keyboard_switch,
        'installation_profile': config.installation_profile,
        'hostname': config.hostname,
        'network_manager': config.network_manager,
        'username': config.username,
        'user_groups': config.user_groups,
        'timezone': config.timezone,
        'locale': config.locale,
        'multilib': config.multilib,
        'aur_helper': config.aur_helper,
        'swap_size': config.swap_size,
        'timestamp': datetime.now().isoformat()
    }
    
    filename = '/tmp/arch_install_config.json'
    with open(filename, 'w') as f:
        json.dump(config_dict, f, indent=2)
    
    logger.info(f"Configuration saved to {filename}")

def load_config() -> None:
    """Загрузить конфигурацию из JSON."""
    filename = '/tmp/arch_install_config.json'
    
    try:
        with open(filename, 'r') as f:
            config_dict = json.load(f)
        
        # Восстановить конфигурацию
        config.language = config_dict.get('language', 'ru')
        config.disk = config_dict.get('disk')
        config.partition_scheme = config_dict.get('partition_scheme')
        config.is_uefi = config_dict.get('is_uefi', False)
        config.gpu_driver = config_dict.get('gpu_driver')
        config.desktop_environment = config_dict.get('desktop_environment')
        config.keyboard_layouts = config_dict.get('keyboard_layouts', ['us'])
        config.keyboard_switch = config_dict.get('keyboard_switch', 'alt_shift')
        config.installation_profile = config_dict.get('installation_profile', 'desktop')
        config.hostname = config_dict.get('hostname', 'archlinux')
        config.network_manager = config_dict.get('network_manager', 'networkmanager')
        config.username = config_dict.get('username')
        config.user_groups = config_dict.get('user_groups', ['wheel', 'audio', 'video'])
        config.timezone = config_dict.get('timezone', 'UTC')
        config.locale = config_dict.get('locale', ['en_US.UTF-8'])
        config.multilib = config_dict.get('multilib', False)
        config.aur_helper = config_dict.get('aur_helper')
        config.swap_size = config_dict.get('swap_size', 2)
        
        logger.info(f"Configuration loaded from {filename}")
    
    except FileNotFoundError:
        logger.warning(f"Configuration file not found: {filename}")

def main():
    """Главная функция."""
    parser = argparse.ArgumentParser(description='Arch Linux Automated Installer')
    parser.add_argument('--config', help='Load configuration from file')
    parser.add_argument('--auto', action='store_true', help='Run in automatic mode')
    parser.add_argument('--lang', choices=['ru', 'en'], default='ru', help='Interface language')
    
    args = parser.parse_args()
    
    # Логирование
    logger.info("=" * 60)
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    logger.info(f"Start time: {datetime.now()}")
    logger.info("=" * 60)
    
    # Печать информации о системе
    print_system_info()
    
    # Проверка предварительных условий
    if not check_all_prerequisites():
        logger.error("Prerequisite check failed")
        return 1
    
    # Инициализировать диалог
    dialog = get_dialog(args.lang)
    
    # Загрузить конфиг если указан
    if args.config:
        # TODO: Реализовать загрузку из файла
        pass
    
    # Показать приветствие
    show_welcome(dialog)
    
    # Главное меню
    main_menu(dialog)
    
    logger.info("Installer exited normally")
    logger.info("=" * 60)
    
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
