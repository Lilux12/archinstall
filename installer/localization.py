"""
Локализация системы: раскладки клавиатуры, часовой пояс, локали.
"""

from typing import Dict, List, Optional
from utils.executor import run_command
from utils.logger import logger
from ui.dialogs import get_dialog
from config import t

# Доступные раскладки клавиатуры
KEYBOARD_LAYOUTS = {
    'ru': 'Russian',
    'us': 'US English',
    'gb': 'UK English',
    'de': 'German',
    'fr': 'French',
    'es': 'Spanish',
    'it': 'Italian',
    'pt-br': 'Brazilian Portuguese',
    'ja': 'Japanese',
    'zh': 'Chinese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'ua': 'Ukrainian',
    'pl': 'Polish',
    'cz': 'Czech',
    'se': 'Swedish',
    'no': 'Norwegian',
    'dk': 'Danish',
    'fi': 'Finnish',
    'tr': 'Turkish',
    'gr': 'Greek',
    'il': 'Hebrew',
}

# Комбинации переключения раскладок
SWITCH_COMBINATIONS = {
    'alt_shift': 'Alt + Shift',
    'ctrl_shift': 'Ctrl + Shift',
    'alt_ctrl': 'Alt + Ctrl',
    'win_space': 'Win + Space',
    'caps': 'CapsLock (toggle)',
    'ctrl_space': 'Ctrl + Space'
}

def search_layouts(dialog, query: str = '') -> Optional[str]:
    """
    Поиск и выбор раскладки с фильтрацией.
    
    Args:
        dialog: Экземпляр InstallerDialog
        query: Начальный поисковый запрос
    
    Returns:
        Выбранный код раскладки или None
    """
    filtered_layouts = KEYBOARD_LAYOUTS
    
    # Если есть начальный запрос, отфильтровать
    if query:
        query = query.lower()
        filtered_layouts = {
            k: v for k, v in KEYBOARD_LAYOUTS.items()
            if query in k.lower() or query in v.lower()
        }
    
    if not filtered_layouts:
        dialog.msgbox('error_invalid_input')
        return None
    
    # Подготовить choices для radiolist
    choices = [(code, name) for code, name in filtered_layouts.items()]
    
    return dialog.radiolist('select_layouts', choices, height=20, width=60)

def configure_keyboards(dialog) -> Optional[Dict]:
    """
    Полная настройка раскладок клавиатуры.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Словарь с конфигурацией раскладок или None
    """
    layouts = []
    switch_combo = None
    
    logger.info("Configuring keyboard layouts...")
    
    # Выбрать основную раскладку
    main_layout = search_layouts(dialog)
    if not main_layout:
        return None
    
    layouts.append(main_layout)
    
    # Цикл для добавления дополнительных раскладок
    while True:
        if not dialog.yesno('add_more_layouts'):
            break
        
        additional = search_layouts(dialog)
        if additional and additional not in layouts:
            layouts.append(additional)
        else:
            break
    
    # Выбрать комбинацию переключения если много раскладок
    if len(layouts) > 1:
        choices = [(k, v) for k, v in SWITCH_COMBINATIONS.items()]
        switch_combo = dialog.radiolist('switch_combination', choices)
    
    if not switch_combo:
        switch_combo = 'alt_shift'
    
    result = {
        'layouts': layouts,
        'switch': switch_combo
    }
    
    logger.info(f"Keyboard configuration: {result}")
    return result

def get_timezones() -> List[str]:
    """
    Получить список доступных часовых поясов.
    
    Returns:
        Список часовых поясов
    """
    try:
        returncode, output = run_command(
            "timedatectl list-timezones",
            check=False,
            log=False
        )
        
        if returncode == 0:
            timezones = output.strip().split('\n')
            return sorted(timezones)
        
        # Fallback список популярных поясов
        return [
            'UTC',
            'Europe/London',
            'Europe/Paris',
            'Europe/Berlin',
            'Europe/Moscow',
            'Europe/Istanbul',
            'Asia/Tokyo',
            'Asia/Shanghai',
            'Asia/Hong_Kong',
            'Asia/Singapore',
            'America/New_York',
            'America/Chicago',
            'America/Denver',
            'America/Los_Angeles',
            'Australia/Sydney',
            'Pacific/Auckland',
        ]
    
    except Exception as e:
        logger.error(f"Failed to get timezones: {e}")
        return ['UTC']

def select_timezone(dialog) -> Optional[str]:
    """
    Выбрать часовой пояс через dialog.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Выбранный часовой пояс или None
    """
    timezones = get_timezones()
    
    # Найти популярные пояса (сделать их вначале)
    favorites = ['UTC', 'Europe/Moscow', 'Europe/London', 'America/New_York', 'Asia/Tokyo']
    
    choices = []
    selected_idx = 0
    
    for idx, tz in enumerate(timezones):
        if tz in favorites:
            choices.insert(0, (tz, tz, 0))
            selected_idx = 0
        else:
            choices.append((tz, tz, 0))
    
    return dialog.radiolist('select_timezone', choices, height=20, width=60)

def set_timezone(timezone: str, mount_point: str = '/mnt') -> bool:
    """
    Установить часовой пояс в системе.
    
    Args:
        timezone: Часовой пояс
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Setting timezone: {timezone}")
        
        # Создать symlink
        run_command(
            f"ln -sf /usr/share/zoneinfo/{timezone} {mount_point}/etc/localtime",
            check=True,
            log=True
        )
        
        # Запустить hwclock
        run_command(
            f"arch-chroot {mount_point} hwclock --systohc",
            check=True,
            log=True
        )
        
        logger.info("Timezone set successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to set timezone: {e}")
        return False

def configure_locales(dialog) -> Optional[List[str]]:
    """
    Выбрать и сконфигурировать локали.
    
    Args:
        dialog: Экземпляр InstallerDialog
    
    Returns:
        Список выбранных локалей или None
    """
    # Популярные локали
    popular_locales = [
        'en_US.UTF-8',
        'ru_RU.UTF-8',
        'de_DE.UTF-8',
        'fr_FR.UTF-8',
        'ja_JP.UTF-8',
        'zh_CN.UTF-8',
    ]
    
    choices = [(locale, locale, 1 if 'en_US' in locale else 0) for locale in popular_locales]
    
    result = dialog.checklist('locale', choices, height=15, width=60)
    
    if result:
        logger.info(f"Locales selected: {result}")
        return result
    
    return ['en_US.UTF-8']

def generate_locale(locales: List[str], mount_point: str = '/mnt') -> bool:
    """
    Генерировать выбранные локали.
    
    Args:
        locales: Список локалей
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Generating locales: {locales}")
        
        # Раскомментировать локали в /etc/locale.gen
        for locale in locales:
            run_command(
                f"sed -i '/{locale}/s/^#//g' {mount_point}/etc/locale.gen",
                check=False,
                log=False
            )
        
        # Запустить locale-gen
        run_command(
            f"arch-chroot {mount_point} locale-gen",
            check=True,
            log=True
        )
        
        # Установить LANG
        if locales:
            lang = locales[0]
            run_command(
                f"echo 'LANG={lang}' > {mount_point}/etc/locale.conf",
                check=True,
                log=True
            )
        
        logger.info("Locales generated successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to generate locales: {e}")
        return False

def set_keyboard_layout(layout: str, mount_point: str = '/mnt') -> bool:
    """
    Установить раскладку клавиатуры.
    
    Args:
        layout: Код раскладки
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Setting keyboard layout: {layout}")
        
        # Создать конфиг vconsole.conf
        config = f"KEYMAP={layout}\n"
        
        run_command(
            f"echo '{config}' > {mount_point}/etc/vconsole.conf",
            check=True,
            log=True
        )
        
        logger.info("Keyboard layout set successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to set keyboard layout: {e}")
        return False

def configure_x11_keyboard(layouts: List[str], switch: str, mount_point: str = '/mnt') -> bool:
    """
    Настроить раскладки для X11.
    
    Args:
        layouts: Список раскладок
        switch: Комбинация переключения
        mount_point: Точка монтирования системы
    
    Returns:
        True если успешно
    """
    try:
        logger.info(f"Configuring X11 keyboard: layouts={layouts}, switch={switch}")
        
        if not layouts:
            return False
        
        # Создать конфигурационный файл
        layout_str = ','.join(layouts)
        
        # Преобразовать switch в X11 формат
        switch_map = {
            'alt_shift': 'grp:alt_shift_toggle',
            'ctrl_shift': 'grp:ctrl_shift_toggle',
            'alt_ctrl': 'grp:alt_ctrl_toggle',
            'win_space': 'grp:win_space_toggle',
            'caps': 'grp:caps_toggle',
            'ctrl_space': 'grp:ctrl_space_toggle',
        }
        
        switch_option = switch_map.get(switch, 'grp:alt_shift_toggle')
        
        # Создать /etc/X11/xorg.conf.d/00-keyboard.conf
        config = f"""
Section "InputClass"
    Identifier "system-keyboard"
    MatchIsKeyboard "on"
    Option "XkbLayout" "{layout_str}"
    Option "XkbOptions" "{switch_option}"
EndSection
"""
        
        run_command(
            f"mkdir -p {mount_point}/etc/X11/xorg.conf.d",
            check=False,
            log=False
        )
        
        with open(f"{mount_point}/etc/X11/xorg.conf.d/00-keyboard.conf", 'w') as f:
            f.write(config)
        
        logger.info("X11 keyboard configured successfully")
        return True
    
    except Exception as e:
        logger.error(f"Failed to configure X11 keyboard: {e}")
        return False
