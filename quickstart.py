#!/usr/bin/env python3
"""
Quick start script for testing the installer.
Run with: python quickstart.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import config, CURRENT_LANG, APP_VERSION, t
from utils.logger import logger
from utils.system import print_system_info

def print_info():
    """Вывести информацию о проекте."""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Arch Linux Automated Installer v2.0                    ║
    ║   Quick Test Script                                       ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Project Structure:
    ✓ config.py              - Configuration & i18n
    ✓ main.py                - Main entry point
    
    Modules:
    ✓ installer/             - Installation modules
      ├── disk.py            - Disk management
      ├── network.py         - Network configuration
      ├── packages.py        - Package management
      ├── graphics.py        - GPU drivers
      ├── desktop.py         - Desktop environments
      ├── bootloader.py      - Bootloader setup
      ├── localization.py    - Localization
      └── users.py           - User management
    
    ✓ ui/                    - User interface
      ├── dialogs.py         - Dialog wrappers
      └── progress.py        - Progress bars
    
    ✓ utils/                 - Utilities
      ├── logger.py          - Logging
      ├── validators.py      - Input validation
      ├── system.py          - System info
      └── executor.py        - Command execution
    
    ✓ configs/               - Configuration files
      ├── packages.json      - Package lists
      └── profiles.json      - Installation profiles
    
    Dependencies:
    - pythondialog (TUI)
    - psutil (System info)
    - requests (HTTP)
    - pyyaml (Config)
    
    Installation:
    # Install dependencies
    pip install -r requirements.txt
    
    # Run main installer (on Arch Linux Live ISO)
    sudo python main.py
    
    Features:
    ✓ Russian & English UI
    ✓ UEFI & BIOS support
    ✓ Auto disk detection
    ✓ Partition management (ext4, btrfs)
    ✓ GPU auto-detection (NVIDIA, AMD, Intel)
    ✓ Multiple DEs (KDE, GNOME, XFCE, i3, Sway, etc.)
    ✓ Keyboard layout configuration
    ✓ User & group management
    ✓ Comprehensive logging
    ✓ Config save/load
    ✓ Installation profiles
    
    """)

def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")
    
    try:
        import config
        print("  ✓ config")
        
        import main
        print("  ✓ main")
        
        from installer import disk, network, packages, graphics, desktop, bootloader, localization, users
        print("  ✓ installer modules")
        
        from ui import dialogs, progress
        print("  ✓ ui modules")
        
        from utils import logger, validators, system, executor
        print("  ✓ utils modules")
        
        print("\n✓ All imports successful!\n")
        return True
    
    except ImportError as e:
        print(f"\n✗ Import error: {e}\n")
        return False

def test_config():
    """Test configuration system."""
    print("Testing configuration...")
    
    # Test translation function
    ru_welcome = t('welcome', 'ru')
    en_welcome = t('welcome', 'en')
    
    print(f"  Russian: {ru_welcome}")
    print(f"  English: {en_welcome}")
    
    if ru_welcome != en_welcome:
        print("  ✓ Translation working\n")
        return True
    else:
        print("  ✗ Translation not working\n")
        return False

def test_system_info():
    """Test system information gathering."""
    print("Testing system information...")
    print_system_info()
    return True

def main():
    """Main test function."""
    print_info()
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test configuration
    if not test_config():
        success = False
    
    # Test system info
    if not test_system_info():
        success = False
    
    # Final message
    print("=" * 60)
    if success:
        print("✓ All tests passed!")
        print("\nYou can now run the installer:")
        print("  sudo python main.py          # Russian interface")
        print("  sudo python main.py --lang en  # English interface")
    else:
        print("✗ Some tests failed!")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
    print("=" * 60)
    
    return 0 if success else 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
