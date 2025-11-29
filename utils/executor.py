"""
Выполнение bash команд безопасно с логированием.
"""

import subprocess
import shlex
from typing import Tuple, Optional
from utils.logger import logger, log_command

def run_command(
    cmd: str,
    check: bool = True,
    log: bool = True,
    shell: bool = True
) -> Tuple[int, str]:
    """
    Безопасное выполнение bash команды.
    
    Args:
        cmd: Команда для выполнения
        check: Генерировать исключение при ошибке
        log: Логировать ли команду
        shell: Выполнять через shell
    
    Returns:
        (returncode, output)
    
    Raises:
        subprocess.CalledProcessError: Если check=True и команда вернула ошибку
    """
    try:
        if shell:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                check=False
            )
        else:
            result = subprocess.run(
                shlex.split(cmd),
                capture_output=True,
                text=True,
                check=False
            )
        
        output = result.stdout + result.stderr
        
        if log:
            log_command(cmd, output, result.returncode)
        
        if check and result.returncode != 0:
            raise subprocess.CalledProcessError(
                result.returncode,
                cmd,
                output=output
            )
        
        return result.returncode, result.stdout
    
    except Exception as e:
        logger.error(f"Failed to execute command '{cmd}': {str(e)}")
        raise

def run_in_chroot(cmd: str, mount_point: str = '/mnt') -> Tuple[int, str]:
    """
    Выполнить команду в chroot окружении.
    
    Args:
        cmd: Команда для выполнения
        mount_point: Точка монтирования системы
    
    Returns:
        (returncode, output)
    """
    full_cmd = f"arch-chroot {mount_point} {cmd}"
    return run_command(full_cmd, check=True, log=True)

def run_command_with_progress(cmd: str, description: str = "") -> Tuple[int, str]:
    """
    Выполнить команду с индикатором прогресса.
    
    Args:
        cmd: Команда для выполнения
        description: Описание операции
    
    Returns:
        (returncode, output)
    """
    if description:
        logger.info(f"Executing: {description}")
    
    return run_command(cmd, check=True, log=True)

def command_exists(cmd: str) -> bool:
    """
    Проверить существует ли команда.
    
    Args:
        cmd: Имя команды
    
    Returns:
        True если команда существует
    """
    returncode, _ = run_command(f"which {cmd}", check=False, log=False)
    return returncode == 0
