# Arch Linux Installer v2.0 - Developer Documentation

## Project Overview

Arch Linux Automated Installer - это профессиональный установщик ОС на Python 3 с интерактивным TUI интерфейсом для автоматизации процесса установки Arch Linux.

**Версия**: 2.0  
**Язык**: Python 3.9+  
**Лицензия**: GNU GPL v3  
**Тип**: Système Distribution Tool

## Architecture

### Слои приложения

```
┌─────────────────────────────────────────┐
│         Main Entry Point (main.py)      │
│  - Menu routing                         │
│  - Workflow orchestration               │
│  - Installation process                 │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┬─────────────────┐
    │                 │                 │
┌───▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
│Installer │  │     UI      │  │   Utils    │
│Modules   │  │ Components  │  │ Libraries  │
└──────────┘  └─────────────┘  └────────────┘
    │              │                 │
    ├─ disk        ├─ dialogs       ├─ logger
    ├─ network     ├─ progress      ├─ validators
    ├─ packages    └─ i18n          ├─ executor
    ├─ graphics                     ├─ system
    ├─ desktop                      └─ config
    ├─ bootloader
    ├─ localization
    └─ users
```

### Core Modules

#### 1. **config.py** - Конфигурация и мультиязычность
```python
class InstallationConfig:
    """Глобальная конфигурация установки."""
    - language
    - disk_info
    - desktop_choice
    - user_settings
    - и т.д.

TRANSLATIONS = {
    'ru': {...},
    'en': {...}
}

def t(key, lang=None) -> str:
    """Функция перевода."""
```

**Ответственность**:
- Хранение конфигурации пользователя
- Система переводов (i18n)
- Глобальные переменные

#### 2. **main.py** - Точка входа и главное меню
```python
def main_menu() -> None:
    """Главное меню с инженерной сложностью."""
    
def final_review() -> bool:
    """Финальный обзор перед установкой."""
    
def install_system() -> None:
    """Главный цикл установки."""
```

**Ответственность**:
- Точка входа приложения
- Главное меню
- Координация всех модулей
- Запуск установки

#### 3. **installer/** - Модули установки

**disk.py** - Управление дисками
```python
detect_disks() -> List[Tuple[str, str]]
    """Обнаружить все диски"""

select_disk(dialog) -> Optional[str]
    """Выбрать диск для установки"""

create_partitions(...) -> bool
    """Создать разделы"""

generate_fstab() -> bool
    """Сгенерировать fstab"""
```

**graphics.py** - Видеодрайверы
```python
detect_gpu() -> Dict[str, str]
    """Автоопределить видеокарту"""

select_gpu_driver(dialog, detected_gpu) -> Optional[str]
    """Выбрать видеодрайвер"""

install_gpu_drivers(driver_type, mount_point) -> bool
    """Установить видеодрайверы"""
```

**desktop.py** - Desktop Environment
```python
DESKTOP_ENVIRONMENTS = {
    'kde': {...},
    'gnome': {...},
    ...
}

select_desktop_environment(dialog) -> Optional[str]
    """Выбрать DE"""

install_desktop_environment(de_key, mount_point) -> bool
    """Установить DE"""
```

**localization.py** - Локализация
```python
configure_keyboards(dialog) -> Optional[Dict]
    """Настроить раскладки"""

select_timezone(dialog) -> Optional[str]
    """Выбрать часовой пояс"""

configure_locales(dialog) -> Optional[List[str]]
    """Выбрать локали"""

generate_locale(locales, mount_point) -> bool
    """Сгенерировать локали"""
```

**packages.py** - Управление пакетами
```python
INSTALLATION_PROFILES = {
    'desktop': {...},
    'server': {...},
    ...
}

select_installation_profile(dialog) -> Optional[str]
    """Выбрать профиль"""

install_packages(packages, mount_point) -> bool
    """Установить пакеты"""

setup_aur_helper(helper, mount_point) -> bool
    """Установить AUR helper"""
```

**network.py** - Сеть
```python
configure_hostname(dialog) -> Optional[str]
    """Установить hostname"""

select_network_manager(dialog) -> Optional[str]
    """Выбрать сетевой менеджер"""

set_hostname(hostname, mount_point) -> bool
    """Применить hostname"""

install_network_manager(nm, mount_point) -> bool
    """Установить сетевой менеджер"""
```

**users.py** - Пользователи
```python
set_root_password(dialog) -> Optional[str]
    """Установить пароль root"""

create_user(dialog) -> Optional[dict]
    """Создать пользователя"""

set_root_password_system(password, mount_point) -> bool
    """Применить пароль root"""

setup_sudo(mount_point) -> bool
    """Настроить sudo"""
```

**bootloader.py** - Загрузчик
```python
detect_boot_mode() -> bool
    """Определить UEFI/BIOS"""

select_bootloader(dialog, is_uefi) -> Optional[str]
    """Выбрать загрузчик"""

install_grub(...) -> bool
    """Установить GRUB"""

install_systemd_boot(...) -> bool
    """Установить systemd-boot"""

install_bootloader(...) -> bool
    """Установить выбранный загрузчик"""
```

#### 4. **ui/** - Компоненты интерфейса

**dialogs.py** - Обертки над pythondialog
```python
class InstallerDialog:
    """Основной класс для диалогов."""
    
    def msgbox(key, height, width) -> int
    def yesno(key, height, width) -> bool
    def inputbox(key, init, height, width) -> Optional[str]
    def passwordbox(key, height, width) -> Optional[str]
    def radiolist(key, choices, height, width) -> Optional[str]
    def checklist(key, choices, height, width) -> Optional[List[str]]
    def menu(key, choices, height, width) -> Optional[str]
    def gauge_start(key, percent) -> None
    def gauge_update(percent, key) -> None
```

**progress.py** - Прогресс-бары
```python
class ProgressBar:
    """Обычный прогресс-бар."""
    
class InstallationProgress(ProgressBar):
    """Специализированный для установки."""
    
    STAGES = [
        ('formatting_disk', 5),
        ('mounting_partitions', 10),
        ...
    ]
```

#### 5. **utils/** - Утилиты

**logger.py** - Логирование
```python
setup_logger() -> logging.Logger
    """Настроить логирование"""

log_command(cmd, output, returncode) -> None
    """Залогировать команду"""
```

**executor.py** - Выполнение команд
```python
run_command(cmd, check, log, shell) -> Tuple[int, str]
    """Выполнить bash команду"""

run_in_chroot(cmd, mount_point) -> Tuple[int, str]
    """Выполнить в chroot"""

command_exists(cmd) -> bool
    """Проверить существует ли команда"""
```

**validators.py** - Валидация
```python
check_internet() -> bool
    """Проверить интернет"""

check_boot_mode() -> bool
    """Проверить UEFI/BIOS"""

validate_hostname(hostname) -> bool
    """Валидировать hostname"""

validate_username(username) -> bool
    """Валидировать username"""

check_all_prerequisites() -> bool
    """Проверить все предварительные условия"""
```

**system.py** - Информация о системе
```python
get_total_memory_gb() -> float
get_cpu_info() -> Dict
has_efi() -> bool
get_system_info() -> Dict
print_system_info() -> None
```

## Data Flow

### Installation Process Flow

```
START
  ├─ Language Selection
  ├─ Prerequisite Checks
  ├─ System Info Gathering
  │
  ├─ Main Menu Loop
  │  ├─ Disk Selection
  │  ├─ Partitioning
  │  ├─ GPU Detection
  │  ├─ Desktop Selection
  │  ├─ Keyboard Config
  │  ├─ Profile Selection
  │  ├─ Network Setup
  │  ├─ User Setup
  │  └─ Additional Settings
  │
  ├─ Final Review
  ├─ Installation Start
  │  ├─ Partition Disk
  │  ├─ Mount Filesystems
  │  ├─ Update Mirrors
  │  ├─ Base Installation
  │  ├─ Locale Setup
  │  ├─ Timezone Setup
  │  ├─ Hostname Setup
  │  ├─ Bootloader Install
  │  ├─ GPU Drivers
  │  ├─ Desktop Environment
  │  ├─ User Creation
  │  ├─ Package Installation
  │  └─ Service Enablement
  │
  ├─ Post Installation Options
  └─ END
```

### Configuration Object Lifecycle

```
InstallationConfig
  ├─ __init__()           → Default values
  ├─ update()             → User selections
  ├─ validate()           → Pre-installation check
  ├─ serialize()          → Save to file
  ├─ deserialize()        → Load from file
  └─ apply()              → Execute on system
```

## Design Patterns

### 1. **Singleton Pattern**
```python
# Global dialog instance
_dialog_instance: Optional[InstallerDialog] = None

def get_dialog() -> InstallerDialog:
    global _dialog_instance
    if _dialog_instance is None:
        _dialog_instance = InstallerDialog()
    return _dialog_instance
```

### 2. **Strategy Pattern**
```python
# Different partitioning strategies
_create_auto_ext4()
_create_auto_btrfs()
_create_manual()
```

### 3. **Factory Pattern**
```python
# Create progress bar based on type
def get_progress(progress_type: str) -> ProgressBar:
    if progress_type == 'install':
        return InstallationProgress()
    else:
        return ProgressBar()
```

### 4. **Template Method Pattern**
```python
# Standard installation steps template
def install_system(dialog):
    progress = get_progress('install')
    progress.start()
    
    for stage in INSTALLATION_STAGES:
        execute_stage(stage)
        progress.next_stage()
    
    progress.stop()
```

## Error Handling

### Exception Hierarchy
```
Exception
├─ subprocess.CalledProcessError
│  └─ Command execution failed
├─ FileNotFoundError
│  └─ Configuration file not found
├─ ValueError
│  └─ Invalid input data
└─ RuntimeError
   └─ System state inconsistent
```

### Error Recovery Strategy
```python
try:
    # Attempt operation
    run_command(cmd, check=True)
except subprocess.CalledProcessError as e:
    logger.error(f"Command failed: {e}")
    # Log error
    # Attempt recovery
    # Or abort installation
    raise
```

## Testing

### Unit Tests (примеры)
```python
def test_validate_hostname():
    assert validate_hostname("myhost") == True
    assert validate_hostname("my-host") == True
    assert validate_hostname("-invalid") == False

def test_validate_username():
    assert validate_username("myuser") == True
    assert validate_username("user123") == True
    assert validate_username("INVALID") == False

def test_detect_gpu():
    result = detect_gpu()
    assert 'vendor' in result
    assert 'driver_type' in result
```

### Integration Tests
```python
def test_partitioning_flow():
    disk = "/dev/sda"
    assert create_partitions(disk, 'auto_ext4', True)
    assert generate_fstab()

def test_user_creation():
    user_info = {
        'username': 'testuser',
        'password': 'testpass',
        'groups': ['wheel']
    }
    assert create_user_system(user_info)
```

## Performance Considerations

### Optimization Areas
1. **Parallel Package Installation**: pacman parallel downloads
2. **Mirror Selection**: reflector for fastest mirrors
3. **Disk I/O**: Batch operations
4. **Network**: Parallel downloads where possible

### Benchmarks
- Base system installation: ~5-10 minutes
- With DE + packages: ~15-30 minutes
- Varies by internet speed and hardware

## Security Considerations

### Password Handling
```python
# Passwords only in memory, never logged
password = dialog.passwordbox(...)  # Hidden input
# Use directly in chpasswd
# Never written to disk
```

### Command Injection Prevention
```python
# Use shell=False where possible
run_command(cmd, shell=False)

# Escape special chars when shell=True
escaped = password.replace("'", "'\\''")
```

### Permission Checks
```python
if os.geteuid() != 0:
    logger.error("This script must be run as root!")
    sys.exit(1)
```

## Logging Strategy

### Log Levels
```
DEBUG  - Detailed info for debugging
INFO   - General information
WARNING - Warning messages
ERROR  - Error messages
```

### Log Locations
```
File: /var/log/archinstall.log
Console: STDOUT/STDERR

Format: [YYYY-MM-DD HH:MM:SS] [LEVEL] message
```

## Extension Points

### Adding New Desktop Environment
```python
# 1. Add to DESKTOP_ENVIRONMENTS in desktop.py
DESKTOP_ENVIRONMENTS['myenv'] = {
    'packages': ['myenv', 'dependencies'],
    'display_manager': 'mydm',
    'description': 'my_environment'
}

# 2. Add translation key
TRANSLATIONS['ru']['my_environment'] = 'Моё окружение'

# 3. Create installer function if needed
def install_myenv(mount_point):
    # Custom installation logic
    pass
```

### Adding New Validator
```python
# Add to validators.py
def validate_custom_field(value: str) -> bool:
    """Validate custom field."""
    pattern = r'^[valid_pattern]$'
    return re.match(pattern, value) is not None
```

### Adding New Installation Step
```python
# In main.py install_system()
# Add to INSTALLATION_STAGES
progress.next_stage()  # Update progress

# Add execution
if not custom_step():
    raise Exception("Custom step failed")
```

## Troubleshooting Guide

### Common Issues

**Issue**: "Module not found"
```bash
Solution: pip install -r requirements.txt
```

**Issue**: "Dialog widget not responding"
```bash
Solution: Increase height/width of dialog box
```

**Issue**: "Partitioning failed"
```bash
Solution: Check disk availability with lsblk
```

### Debug Mode
```bash
# Enable debug logging
DEBUG=1 python main.py

# Check detailed logs
tail -f /var/log/archinstall.log
```

## Future Improvements

- [ ] Web UI alternative
- [ ] Multi-disk installation
- [ ] LUKS encryption
- [ ] LVM support
- [ ] Network installation
- [ ] Custom kernel compilation
- [ ] Automated testing suite
- [ ] Docker container for CI/CD
- [ ] Translations for more languages
- [ ] Installation profiles from cloud

## Contributing

### Code Style
- PEP 8 compliance
- Type hints for functions
- Docstrings for all modules
- Comments for complex logic

### Testing Before Submit
```bash
# Check syntax
python -m py_compile *.py

# Run quickstart
python quickstart.py

# Check formatting
python -m autopep8 --check .
```

## References

- Arch Installation Guide: https://wiki.archlinux.org
- Python Documentation: https://docs.python.org
- pythondialog Docs: https://pythonhosted.org/pythondialog
- Shell Scripting: https://mywiki.wooledge.org/BashGuide

---

**Last Updated**: 2024-01-15  
**Version**: 2.0  
**Status**: Production Ready
