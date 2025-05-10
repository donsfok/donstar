#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Qwen3-DevAgent-Core
Главный файл приложения, инициализирующий графический интерфейс 
и компоненты ядра системы
"""

import sys
import os
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDir

from ui.main_window import MainWindow
from models.model_manager import ModelManager
from api.ollama_api import OllamaAPI
from utils.system_check import check_requirements

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("Qwen3-DevAgent")

def main():
    """Основная функция запуска приложения"""
    
    # Отключаем привязку к родительскому процессу
    try:
        if os.fork() > 0:
            sys.exit(0)
    except OSError:
        pass
    
    # Создаем новую сессию
    os.setsid()
    
    try:
        # Проверка системных требований
        if not check_requirements():
            logger.error("Системные требования не удовлетворены. Приложение не может быть запущено.")
            sys.exit(1)
            
        # Установка переменных окружения для Qt
        os.environ["QT_QPA_PLATFORM"] = "xcb"
        os.environ["DISPLAY"] = ":0"
        
        # Проверка графической подсистемы
        if not os.path.exists("/usr/lib/x86_64-linux-gnu/libGL.so.1"):
            logger.error("Отсутствуют графические библиотеки. Установите пакет libgl1-mesa-glx")
            sys.exit(1)
    
    # Настройка путей приложения
    app_dir = os.path.dirname(os.path.abspath(__file__))
    resources_dir = os.path.join(app_dir, "resources")
    
    # Создание экземпляра приложения Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Qwen3-DevAgent")
    
    # Загрузка стилей CSS
    with open(os.path.join(resources_dir, "styles.css"), "r") as f:
        app.setStyleSheet(f.read())
    
    # Инициализация API для Ollama
    ollama_api = OllamaAPI()
    
    # Инициализация менеджера моделей
    model_manager = ModelManager(ollama_api)
    
    # Создание и отображение главного окна
    main_window = MainWindow(model_manager)
    main_window.show()
    
    logger.info("Приложение Qwen3-DevAgent успешно запущено")
    
    # Запуск главного цикла приложения
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
