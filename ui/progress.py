"""
Работа с прогресс-барами и индикаторами.
"""

from ui.dialogs import get_dialog
from config import t
from typing import Optional, Callable

class ProgressBar:
    """Менеджер прогресс-бара."""
    
    def __init__(self, total_steps: int = 100):
        """
        Инициализация.
        
        Args:
            total_steps: Общее количество шагов
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.dialog = get_dialog()
        self.active = False
    
    def start(self, title_key: str = '') -> None:
        """
        Начать прогресс-бар.
        
        Args:
            title_key: Ключ перевода заголовка
        """
        self.current_step = 0
        self.active = True
        self.dialog.gauge_start(title_key, percent=0)
    
    def update(self, steps: int = 1, message_key: str = '') -> None:
        """
        Обновить прогресс.
        
        Args:
            steps: Количество пройденных шагов
            message_key: Ключ перевода сообщения
        """
        if not self.active:
            return
        
        self.current_step = min(self.current_step + steps, self.total_steps)
        percent = int((self.current_step / self.total_steps) * 100)
        self.dialog.gauge_update(percent, message_key)
    
    def set_percent(self, percent: int, message_key: str = '') -> None:
        """
        Установить процент напрямую.
        
        Args:
            percent: Процент (0-100)
            message_key: Ключ перевода сообщения
        """
        if not self.active:
            return
        
        percent = max(0, min(percent, 100))
        self.current_step = int((percent / 100) * self.total_steps)
        self.dialog.gauge_update(percent, message_key)
    
    def stop(self) -> None:
        """Остановить прогресс-бар."""
        if self.active:
            self.dialog.gauge_stop()
            self.active = False

class InstallationProgress(ProgressBar):
    """Специализированный прогресс-бар для установки."""
    
    # Этапы установки с примерными процентами
    STAGES = [
        ('formatting_disk', 5),
        ('mounting_partitions', 10),
        ('updating_mirrors', 15),
        ('installing_base', 40),
        ('installing_kernel', 50),
        ('generating_fstab', 55),
        ('configuring_locale', 60),
        ('configuring_timezone', 65),
        ('setting_hostname', 70),
        ('installing_bootloader', 75),
        ('installing_gpu_drivers', 85),
        ('installing_desktop', 90),
        ('creating_users', 95),
        ('installing_packages', 98),
        ('enabling_services', 100),
    ]
    
    def __init__(self):
        """Инициализация с предопределенными этапами."""
        super().__init__(total_steps=len(self.STAGES))
        self.stage_index = 0
    
    def next_stage(self) -> None:
        """Перейти к следующему этапу установки."""
        if self.stage_index < len(self.STAGES):
            stage_key, percent = self.STAGES[self.stage_index]
            self.set_percent(percent, stage_key)
            self.stage_index += 1

# Глобальный экземпляр
_progress_instance: Optional[ProgressBar] = None

def get_progress(progress_type: str = 'bar') -> ProgressBar:
    """
    Получить экземпляр прогресс-бара.
    
    Args:
        progress_type: 'bar' для обычного, 'install' для установки
    
    Returns:
        Экземпляр прогресс-бара
    """
    global _progress_instance
    
    if progress_type == 'install':
        return InstallationProgress()
    else:
        if _progress_instance is None:
            _progress_instance = ProgressBar()
        return _progress_instance
