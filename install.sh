#!/bin/bash
# Installation script for Arch Linux Live ISO
# Usage: chmod +x install.sh && sudo ./install.sh

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Arch Linux Automated Installer v2.0                    ║"
echo "║   Installation script for Live ISO                       ║"
echo "╚═══════════════════════════════════════════════════════════╝"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root!"
   exit 1
fi

# Update system
echo "Updating pacman database..."
pacman -Sy

# Install dependencies
echo "Installing dependencies..."
pacman -S --noconfirm python python-pip dialog git

# Create installation directory
INSTALL_DIR="/opt/arch-installer"
echo "Installing to $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

# Clone or download repository
if command -v git &> /dev/null; then
    echo "Cloning repository..."
    git clone https://github.com/user/arch-installer.git "$INSTALL_DIR" || \
    git clone https://github.com/user/arch-installer.git "$INSTALL_DIR" --depth=1
else
    echo "Git not available, downloading zip..."
    cd "$INSTALL_DIR"
    # Fallback download if git not available
fi

# Install Python dependencies
echo "Installing Python packages..."
pip install -r "$INSTALL_DIR/requirements.txt"

# Create symbolic link
ln -sf "$INSTALL_DIR/main.py" /usr/local/bin/arch-installer

# Set permissions
chmod +x "$INSTALL_DIR/main.py"
chmod +x /usr/local/bin/arch-installer

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║   Installation complete!                                 ║"
echo "╠═══════════════════════════════════════════════════════════╣"
echo "║   Run installer with:                                    ║"
echo "║   # arch-installer                                       ║"
echo "║                                                           ║"
echo "║   Or with options:                                       ║"
echo "║   # arch-installer --lang en                             ║"
echo "║   # arch-installer --lang ru                             ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Ask to start installer
read -p "Start installer now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    arch-installer
fi
