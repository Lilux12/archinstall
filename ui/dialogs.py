"""
UI диалоги - обертка над pythondialog с преднастроенным стилем.
"""

from typing import List, Tuple, Optional
from config import t, CURRENT_LANG

try:
    from dialog import Dialog
except ImportError:
    Dialog = None

class InstallerDialog:
    """
    Обертка над pythondialog для установщика.
    Все методы используют текущий язык из конфигурации.
    """
    
    def __init__(self, lang: str = 'ru', autowidgetsize: bool = True):
        """
        Инициализация диалога.
        
        Args:
            lang: Язык интерфейса
            autowidgetsize: Автоматический размер окна
        """
        if Dialog is None:
            raise ImportError(
                "pythondialog is not installed. "
                "Install with: pip install pythondialog"
            )
        
        self.d = Dialog(dialog="dialog", autowidgetsize=autowidgetsize)
        self.d.set_background_title("Arch Linux Installer v2.0")
        self.lang = lang
    
    def msgbox(self, key: str, height: int = 10, width: int = 70) -> int:
        """
        Информационное окно.
        
        Args:
            key: Ключ перевода текста
            height: Высота окна
            width: Ширина окна
        
        Returns:
            Код результата
        """
        text = t(key, self.lang)
        return self.d.msgbox(text, height=height, width=width)
    
    def yesno(self, key: str, height: int = 10, width: int = 70) -> bool:
        """
        Диалог подтверждения (Yes/No).
        
        Args:
            key: Ключ перевода текста
            height: Высота окна
            width: Ширина окна
        
        Returns:
            True если ответ "Yes"
        """
        text = t(key, self.lang)
        code = self.d.yesno(text, height=height, width=width)
        return code == self.d.OK
    
    def inputbox(self, key: str, init: str = '', height: int = 10, width: int = 70) -> Optional[str]:
        """
        Ввод текста.
        
        Args:
            key: Ключ перевода подсказки
            init: Начальное значение
            height: Высота окна
            width: Ширина окна
        
        Returns:
            Введенный текст или None если отмена
        """
        text = t(key, self.lang)
        code, value = self.d.inputbox(text, init=init, height=height, width=width)
        return value if code == self.d.OK else None
    
    def passwordbox(self, key: str, height: int = 10, width: int = 70) -> Optional[str]:
        """
        Ввод пароля (скрытый текст).
        
        Args:
            key: Ключ перевода подсказки
            height: Высота окна
            width: Ширина окна
        
        Returns:
            Введенный пароль или None если отмена
        """
        text = t(key, self.lang)
        code, value = self.d.passwordbox(text, height=height, width=width)
        return value if code == self.d.OK else None
    
    def radiolist(
        self,
        key: str,
        choices: List[Tuple[str, str, int]],
        height: int = 20,
        width: int = 70
    ) -> Optional[str]:
        """
        Выбор одного варианта (radio button).
        Формат choices: [(tag, description, selected), ...]
        selected: 1 для выбранного, 0 для остальных
        
        Args:
            key: Ключ перевода заголовка
            choices: Список вариантов
            height: Высота окна
            width: Ширина окна
        
        Returns:
            Выбранный tag или None если отмена
        """
        text = t(key, self.lang)
        code, tag = self.d.radiolist(text, choices, height=height, width=width)
        return tag if code == self.d.OK else None
    
    def checklist(
        self,
        key: str,
        choices: List[Tuple[str, str, int]],
        height: int = 20,
        width: int = 70
    ) -> Optional[List[str]]:
        """
        Выбор нескольких вариантов (checkbox).
        Формат choices: [(tag, description, checked), ...]
        checked: 1 для выбранного, 0 для невыбранного
        
        Args:
            key: Ключ перевода заголовка
            choices: Список вариантов
            height: Высота окна
            width: Ширина окна
        
        Returns:
            Список выбранных tags или None если отмена
        """
        text = t(key, self.lang)
        code, tags = self.d.checklist(text, choices, height=height, width=width)
        return tags if code == self.d.OK else None
    
    def menu(
        self,
        key: str,
        choices: List[Tuple[str, str]],
        height: int = 20,
        width: int = 70
    ) -> Optional[str]:
        """
        Меню для выбора.
        Формат choices: [(tag, text), ...]
        
        Args:
            key: Ключ перевода заголовка
            choices: Список пунктов меню
            height: Высота окна
            width: Ширина окна
        
        Returns:
            Выбранный tag или None если отмена
        """
        text = t(key, self.lang)
        code, tag = self.d.menu(text, choices, height=height, width=width)
        return tag if code == self.d.OK else None
    
    def gauge_start(self, key: str = '', percent: int = 0) -> None:
        """
        Начать прогресс-бар.
        
        Args:
            key: Ключ перевода текста
            percent: Начальный процент (0-100)
        """
        text = t(key, self.lang) if key else ""
        self.d.gauge_start(text, percent=percent, height=10, width=70)
    
    def gauge_update(self, percent: int, key: str = '') -> None:
        """
        Обновить прогресс-бар.
        
        Args:
            percent: Процент выполнения (0-100)
            key: Ключ перевода текста
        """
        text = t(key, self.lang) if key else ""
        self.d.gauge_update(percent, text=text)
    
    def gauge_stop(self) -> None:
        """Остановить прогресс-бар."""
        self.d.gauge_stop()
    
    def textbox(
        self,
        filepath: str,
        height: int = 20,
        width: int = 70
    ) -> int:
        """
        Показать содержимое файла.
        
        Args:
            filepath: Путь к файлу
            height: Высота окна
            width: Ширина окна
        
        Returns:
            Код результата
        """
        return self.d.textbox(filepath, height=height, width=width)
    
    def set_background_title(self, title: str) -> None:
        """
        Установить фоновый заголовок окна.
        
        Args:
            title: Новый заголовок
        """
        self.d.set_background_title(title)

# Глобальный экземпляр диалога
_dialog_instance: Optional[InstallerDialog] = None

def get_dialog(lang: str = 'ru') -> InstallerDialog:
    """
    Получить или создать глобальный экземпляр диалога.
    
    Args:
        lang: Язык интерфейса
    
    Returns:
        Экземпляр InstallerDialog
    """
    global _dialog_instance
    if _dialog_instance is None:
        _dialog_instance = InstallerDialog(lang=lang)
    return _dialog_instance
