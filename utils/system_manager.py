
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import logging
from typing import List, Dict, Optional

logger = logging.getLogger("SystemManager")

class SystemManager:
    """Класс для выполнения системных команд через ИИ"""
    
    ALLOWED_COMMANDS = {
        'install': ['apt-get', 'apt', 'pip'],
        'file': ['touch', 'mkdir', 'cp', 'mv'],
        'info': ['ls', 'pwd', 'whoami', 'df', 'free'],
    }
    
    @staticmethod
    def execute_command(command: str, args: List[str]) -> Dict[str, any]:
        """
        Выполнение проверенной системной команды
        
        Args:
            command: Команда для выполнения
            args: Аргументы команды
            
        Returns:
            dict: Результат выполнения команды
        """
        try:
            # Проверка команды на разрешенность
            command_type = None
            for cmd_type, allowed in SystemManager.ALLOWED_COMMANDS.items():
                if command in allowed:
                    command_type = cmd_type
                    break
                    
            if not command_type:
                raise Exception(f"Команда {command} не разрешена")
                
            # Формирование полной команды
            full_command = [command] + args
            
            # Выполнение команды
            result = subprocess.run(
                full_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr,
                'code': result.returncode
            }
            
        except Exception as e:
            logger.error(f"Ошибка выполнения команды: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'code': -1
            }
