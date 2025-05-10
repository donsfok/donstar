
#!/usr/bin/env python3
import os
import sys

def create_desktop_entry():
    # Получаем текущую директорию
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Создаем содержимое .desktop файла
    desktop_entry = f"""[Desktop Entry]
Name=Qwen3 DevAgent
Comment=AI Development Assistant
Exec=/usr/bin/env python3 {current_dir}/main.py
Icon={current_dir}/generated-icon.png
Terminal=false
StartupNotify=true
Type=Application
Categories=Development;AI;
Path={current_dir}
"""
    
    # Путь к файлу в локальном каталоге приложений
    desktop_path = os.path.expanduser('~/.local/share/applications/qwen3-devagent.desktop')
    
    # Создаем директорию если её нет
    os.makedirs(os.path.dirname(desktop_path), exist_ok=True)
    
    # Записываем файл
    with open(desktop_path, 'w') as f:
        f.write(desktop_entry)
    
    # Делаем файл исполняемым
    os.chmod(desktop_path, 0o755)
    print("Desktop entry created successfully!")

if __name__ == "__main__":
    create_desktop_entry()
