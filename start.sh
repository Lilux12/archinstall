#!/bin/bash
# Arch Linux Automated Installer - Start Script
# Для быстрого старта на Arch Linux Live ISO
# Usage: chmod +x start.sh && sudo ./start.sh

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции вывода
print_header() {
    echo -e "${BLUE}╔═════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC} $1"
    echo -e "${BLUE}╚═════════════════════════════════════════════════════════════╝${NC}"
}

print_step() {
    echo -e "${YELLOW}➜${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Проверка прав доступа
if [[ $EUID -ne 0 ]]; then
   print_error "This script must be run as root (use: sudo ./start.sh)"
   exit 1
fi

# Получить директорию скрипта
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_header "Arch Linux Automated Installer v2.0"
echo ""

# ============================================================================
# ШАГ 1: Установка кириллицы и русского шрифта
# ============================================================================
print_step "Configuring Russian locale and fonts..."

if command -v setfont &> /dev/null; then
    # Установить русский шрифт для консоли
    if [ -f /usr/share/kbd/consolefonts/cyr-sun16.psf.gz ]; then
        setfont cyr-sun16
        print_success "Russian font (cyr-sun16) loaded"
    else
        print_info "Font cyr-sun16 not found, trying cyr-SCREEN-KMAP..."
        setfont cyr-SCREEN-KMAP 2>/dev/null || print_info "Could not set Cyrillic font"
    fi
else
    print_info "setfont not found, skipping font setup"
fi

# Установить русскую раскладку для консоли (опционально)
if command -v loadkeys &> /dev/null; then
    loadkeys ru 2>/dev/null || print_info "Russian keymap not available in Live CD"
fi

echo ""

# ============================================================================
# ШАГ 2: Обновление pacman базы данных
# ============================================================================
print_step "Updating pacman database..."
pacman -Sy --noconfirm > /dev/null 2>&1
print_success "Pacman database updated"

echo ""

# ============================================================================
# ШАГ 3: Установка Python 3 и pip
# ============================================================================
print_step "Installing Python 3..."

if ! command -v python3 &> /dev/null; then
    print_info "Python not found, installing..."
    pacman -S --noconfirm python > /dev/null 2>&1
    print_success "Python 3 installed"
else
    python_version=$(python3 --version | awk '{print $2}')
    print_success "Python $python_version already installed"
fi

echo ""

# ============================================================================
# ШАГ 4: Установка Python зависимостей
# ============================================================================
print_step "Installing Python dependencies..."

# Убедиться что pip обновлен
python3 -m pip install --upgrade pip > /dev/null 2>&1

# Список зависимостей
dependencies="pythondialog psutil requests pyyaml"

print_info "Installing: $dependencies"

if python3 -m pip install $dependencies > /dev/null 2>&1; then
    print_success "Python dependencies installed"
else
    print_error "Failed to install Python dependencies"
    print_info "Trying alternative installation method..."
    
    # Установить через pacman
    pacman -S --noconfirm python-requests > /dev/null 2>&1 || true
    
    # Попытаться установить pip пакеты снова
    python3 -m pip install --no-cache-dir pythondialog psutil pyyaml > /dev/null 2>&1 || true
fi

echo ""

# ============================================================================
# ШАГ 5: Установка системных утилит (если нужны)
# ============================================================================
print_step "Checking system utilities..."

required_tools=("lsblk" "parted" "pacstrap" "arch-chroot" "genfstab")
missing_tools=()

for tool in "${required_tools[@]}"; do
    if ! command -v $tool &> /dev/null; then
        missing_tools+=("$tool")
    fi
done

if [ ${#missing_tools[@]} -gt 0 ]; then
    print_info "Installing missing system utilities: ${missing_tools[*]}"
    pacman -S --noconfirm parted arch-install-scripts > /dev/null 2>&1
    print_success "System utilities installed"
else
    print_success "All required utilities found"
fi

echo ""

# ============================================================================
# ШАГ 6: Проверка конфигурации установщика
# ============================================================================
print_step "Checking installer configuration..."

if [ -f "$SCRIPT_DIR/main.py" ]; then
    print_success "main.py found"
else
    print_error "main.py not found in $SCRIPT_DIR"
    exit 1
fi

if [ -f "$SCRIPT_DIR/config.py" ]; then
    print_success "config.py found"
else
    print_error "config.py not found"
    exit 1
fi

if [ -d "$SCRIPT_DIR/installer" ]; then
    print_success "installer modules found"
else
    print_error "installer directory not found"
    exit 1
fi

echo ""

# ============================================================================
# ШАГ 7: Информация о системе
# ============================================================================
print_step "System information:"

boot_mode="BIOS"
if [ -d /sys/firmware/efi ]; then
    boot_mode="UEFI"
fi
print_info "Boot mode: $boot_mode"

ram_gb=$(free -h | awk '/^Mem:/ {print $2}')
print_info "RAM: $ram_gb"

cpu_cores=$(nproc)
print_info "CPU cores: $cpu_cores"

# Проверить интернет
if ping -c 1 archlinux.org &> /dev/null; then
    print_info "Internet: ✓ Connected"
else
    print_info "Internet: ✗ No connection (may be needed during installation)"
fi

echo ""

# ============================================================================
# ШАГ 8: Финальная информация и запуск
# ============================================================================
print_header "Setup Complete!"

echo ""
print_info "Everything is ready to start the installation!"
echo ""

# Предложить варианты
echo -e "${BLUE}Options:${NC}"
echo -e "  1) Start installer in ${GREEN}Russian${NC} (рус) - RECOMMENDED"
echo -e "  2) Start installer in ${GREEN}English${NC} (eng)"
echo -e "  3) ${YELLOW}Exit${NC}"
echo ""

read -p "Choose option (1/2/3): " choice

case $choice in
    1)
        echo ""
        print_info "Starting Arch Linux Installer in Russian..."
        echo ""
        cd "$SCRIPT_DIR"
        python3 main.py --lang ru
        ;;
    2)
        echo ""
        print_info "Starting Arch Linux Installer in English..."
        echo ""
        cd "$SCRIPT_DIR"
        python3 main.py --lang en
        ;;
    3)
        echo ""
        print_info "Exiting. Run the installer manually with:"
        echo "  cd $SCRIPT_DIR"
        echo "  sudo python3 main.py"
        echo ""
        exit 0
        ;;
    *)
        print_error "Invalid option. Exiting."
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Installation process finished!${NC}"
echo ""
