# Examples and Usage Guide

## Quick Start

### Basic Usage (Russian Interface)
```bash
sudo python main.py
```

### English Interface
```bash
sudo python main.py --lang en
```

### Load Configuration
```bash
sudo python main.py --config my_config.json
```

### Automatic Installation (requires config)
```bash
sudo python main.py --config my_config.json --auto
```

## Manual Setup Examples

### Example 1: Desktop with KDE Plasma

#### Preparation
```bash
# Boot into Arch Linux Live USB
# Connect to internet
# Start installer
sudo python main.py --lang ru
```

#### Step by Step
1. **Language**: Select "Русский" (Russian)
2. **Disk**: Select "/dev/sda" (your target disk)
3. **Partitioning**: Select "Автоматическая (ext4)"
4. **GPU**: Auto-detected NVIDIA → Select "nvidia_proprietary"
5. **Desktop**: Select "KDE Plasma"
6. **Keyboard**: 
   - Primary: Russian (ru)
   - Secondary: US (us)
   - Switch: Alt+Shift
7. **Profile**: Desktop (full installation)
8. **Network**: 
   - Hostname: "my-desktop"
   - Manager: NetworkManager
9. **Users**:
   - Root password: ••••••••
   - Username: myuser
   - Password: ••••••••
   - Groups: wheel, audio, video, storage
10. **Additional**:
    - Timezone: Europe/Moscow
    - Locale: Russian, English
    - Multilib: Yes
    - AUR: yay
11. **Final Review**: Confirm all settings
12. **Installation**: Start

#### Post-Installation
- Reboot the system
- Log in with your user
- Use pacman to install additional software
- Configure KDE Plasma

### Example 2: Minimal Server Setup

```bash
# Boot into Live ISO
sudo python main.py --lang en
```

Configuration:
- Language: English
- Disk: /dev/sda
- Partitioning: Auto ext4
- GPU: Generic
- Desktop: None (CLI only)
- Profile: Server
- Network:
  - Hostname: arch-server
  - Manager: systemd-networkd
- Users:
  - Root: password
  - Admin user
- Timezone: UTC
- Locale: English only
- AUR: No

### Example 3: Development Workstation

```bash
# With NVIDIA GPU and development tools
sudo python main.py --lang en
```

Select:
- Desktop: XFCE (lightweight)
- GPU: nvidia_proprietary
- Profile: Desktop
- Add packages:
  - VS Code
  - Python
  - Node.js
  - Docker
  - Git

### Example 4: Using Configuration Files

#### Save Current Configuration
After configuring in the installer:
- Press "S" in main menu to save config
- Config saved to `/tmp/arch_install_config.json`

#### Create Configuration Template
```json
{
  "language": "ru",
  "disk": "/dev/sda",
  "partition_scheme": "auto_ext4",
  "is_uefi": true,
  "gpu_driver": "nvidia_proprietary",
  "desktop_environment": "kde",
  "keyboard_layouts": ["ru", "us"],
  "keyboard_switch": "alt_shift",
  "installation_profile": "desktop",
  "hostname": "archlinux",
  "network_manager": "networkmanager",
  "timezone": "Europe/Moscow",
  "locale": ["ru_RU.UTF-8", "en_US.UTF-8"],
  "multilib": true,
  "aur_helper": "yay",
  "swap_size": 4,
  "use_reflector": true
}
```

#### Use Configuration
```bash
sudo python main.py --config my_config.json
```

## Installation Profiles

### Desktop Profile
Best for: Personal computers, workstations

Includes:
- Full development tools
- Graphics packages
- Multimedia applications
- Office tools

### Minimal Profile
Best for: Servers, embedded systems, testing

Includes:
- Only essential packages
- Minimal dependencies
- Lightweight

### Server Profile
Best for: Servers, production systems

Includes:
- SSH
- System monitoring tools
- Server utilities
- No GUI

### Xorg Profile
Best for: Custom setups, developers

Includes:
- X Window System
- Basic graphics
- Terminal
- No desktop environment

## Desktop Environment Choices

### KDE Plasma
- **Best for**: Modern powerful systems
- **RAM**: 2GB+
- **Disk**: 8GB+
- **Features**: Rich features, highly customizable

### GNOME
- **Best for**: Modern workstations
- **RAM**: 2GB+
- **Disk**: 8GB+
- **Features**: Simple, elegant interface

### XFCE
- **Best for**: Older hardware, speed-focused
- **RAM**: 512MB+
- **Disk**: 3GB+
- **Features**: Lightweight, traditional

### i3wm
- **Best for**: Power users, developers
- **RAM**: 256MB+
- **Disk**: 1GB+
- **Features**: Tiling, keyboard-driven

### Sway
- **Best for**: Modern minimalism, Wayland
- **RAM**: 512MB+
- **Disk**: 2GB+
- **Features**: i3 for Wayland, modern

## GPU Driver Options

### NVIDIA
- **Proprietary**: Best gaming performance
- **Nouveau**: Open-source, stable
- **Hybrid**: For laptops with dual graphics

### AMD
- **AMDGPU**: Modern cards, full support
- **Vulkan**: Gaming performance

### Intel
- **Open-source**: Integrated graphics
- **Media drivers**: Hardware acceleration

## Keyboard Layouts Supported

Common layouts:
- Russian (ru)
- US English (us)
- German (de)
- French (fr)
- Spanish (es)
- Japanese (ja)
- Chinese (zh)
- And 20+ more...

Switch combinations:
- Alt+Shift (default)
- Ctrl+Shift
- Alt+Ctrl
- Win+Space
- CapsLock
- Ctrl+Space

## Troubleshooting

### Installation Fails
1. Check internet: `ping archlinux.org`
2. Check logs: `tail -100 /var/log/archinstall.log`
3. Verify disk is available: `lsblk`

### Dialog Not Found
```bash
pacman -S dialog
```

### Python Dependencies Missing
```bash
pip install -r requirements.txt
```

### Permissions Denied
```bash
sudo python main.py
```

## Advanced Usage

### Manual Disk Configuration
Select "Ручная разметка" (Manual) during partitioning to use `cfdisk`:

```bash
# This will open interactive partitioning tool
# Create partitions as needed
# Format them manually
# Mount to /mnt
```

### Custom Package Selection
During installation, select additional packages:
- Browsers: Firefox, Chromium, Brave
- Development: VS Code, Python, Node.js, Docker
- Multimedia: VLC, GIMP, OBS, Blender
- Utilities: Git, Vim, tmux, htop

### Post-Installation Customization

#### Switch to Development Version
```bash
# After installation, enable testing repos
echo "[testing]
Include = /etc/pacman.d/mirrorlist" >> /etc/pacman.conf
```

#### Install Additional Tools
```bash
# Gaming
pacman -S steam lutris

# Development
pacman -S base-devel git

# Multimedia
pacman -S ffmpeg imagemagick
```

#### Configure AUR
If yay is installed:
```bash
yay -S some-aur-package
```

## Performance Optimization

### Enable Parallel Downloads
```bash
# Edit /etc/pacman.conf
# Uncomment ParallelDownloads = 5
```

### Use SSD Features
```bash
# For btrfs on SSD
mount -o ssd,noatime,space_cache=v2
```

### Enable Reflector for Fast Mirrors
```bash
sudo reflector --latest 20 --sort rate --save /etc/pacman.d/mirrorlist
```

## Security Hardening

### After Installation
```bash
# Update all packages
sudo pacman -Syu

# Install security tools
sudo pacman -S fail2ban aide

# Configure firewall
sudo pacman -S ufw
sudo ufw enable
```

### SSH Hardening
```bash
# If SSH installed
sudo systemctl enable sshd
sudo systemctl start sshd

# Disable root login
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
```

## Uninstall/Reinstall

### Complete Wipe and Reinstall
```bash
# Boot from Live ISO again
# Run installer again
sudo python main.py
```

### Backup Before Installation
```bash
# Create backup of critical data
rsync -av /home/ /backup/home/
```

## Tips & Tricks

1. **Save Configuration Before Install**: Always save your configuration
2. **Create Boot USB Carefully**: Don't format wrong disk
3. **Network First**: Ensure internet works before starting
4. **Test with VM**: Test complex setups in VirtualBox first
5. **Keep ISO Handy**: Keep Live ISO for recovery
6. **Document Your Setup**: Write down what you chose for future reference
7. **Learn Arch Wiki**: Read https://wiki.archlinux.org for deeper knowledge

## Performance Tips

### Faster Installation
- Use wired connection instead of WiFi
- Install on SSD if possible
- Close unnecessary applications before starting
- Use reflector to select fastest mirrors

### Faster First Boot
- Don't install unnecessary packages
- Use lightweight DE for older hardware
- Enable parallel downloads

## Getting Help

### Check Logs
```bash
tail -50 /var/log/archinstall.log
```

### Arch Community
- Arch Wiki: https://wiki.archlinux.org
- Forums: https://bbs.archlinux.org
- IRC: #archlinux on Libera.Chat

### GitHub Issues
- Report bugs at: https://github.com/user/arch-installer/issues
- Suggest features
- Ask questions

## References

- Arch Installation Guide: https://wiki.archlinux.org/title/Installation_guide
- Partitioning: https://wiki.archlinux.org/title/Partitioning
- Bootloader: https://wiki.archlinux.org/title/Arch_boot_process
- Desktop: https://wiki.archlinux.org/title/Desktop_environment
- Display Manager: https://wiki.archlinux.org/title/Display_manager
