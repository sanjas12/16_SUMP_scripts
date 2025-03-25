import os
import time
import ftplib
from datetime import datetime
from typing import Optional
import getpass 

# Настройки
FTP_SERVER1 = '192.168.3.93'
FTP_SERVER2 = '192.168.3.92'
FTP_USER = 'rs_pdu'
REMOTE_PATH = '/home/rs_pdu/mpux/data'
LOCAL_BASE_PATH = r'C:\back_up'
INTERVAL = 8 * 60 * 60  # 8 часов в секундах
INITIAL_DELAY = 0  # Задержка перед первым скачиванием (в секундах)

# Логирование
LOG_FILE = os.path.join(LOCAL_BASE_PATH, 'ftp_download.log')

def log(message: str) -> None:
    """Запись сообщения в лог-файл и вывод в консоль."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_message = f"[{timestamp}] {message}"
    
    print(log_message)
    
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    except IOError as e:
        print(f"Ошибка при записи в лог-файл: {e}")

def get_valid_password(attempts_limit: int = 3) -> Optional[str]:
    """
    Запрашивает пароль у пользователя с ограничением попыток.
    Возвращает пароль если он верный, None после исчерпания попыток.
    Ввод пароля скрывается при наборе.
    """
    correct_password = 'rs_pdu'
    
    for attempt in range(1, attempts_limit + 1):
        try:
            # Используем getpass вместо input для скрытия ввода
            # user_pass = getpass.getpass('Введите пароль для доступа: ')
            user_pass = 'rs_pdu'
            if user_pass == correct_password:
                log("Пароль верный. Доступ разрешен.")
                return user_pass
            
            remaining_attempts = attempts_limit - attempt
            if remaining_attempts > 0:
                log(f"Неверный пароль! Осталось попыток: {remaining_attempts}")
            else:
                log("Неверный пароль! Попытки исчерпаны.")
                return None
                
        except Exception as e:
            log(f"Ошибка ввода пароля: {e}")
            return None

def create_download_folder(base_path: str) -> str:
    """Создает папку для скачивания с временной меткой."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    download_folder = os.path.join(base_path, timestamp)
    
    for subfolder in ['us_1(93)', 'us_2(92)']:
        os.makedirs(os.path.join(download_folder, subfolder), exist_ok=True)
    
    log(f"Создана папка для скачивания: {download_folder}")
    return download_folder

def download_ftp_files(server: str, user: str, password: str, 
                      remote_path: str, local_path: str) -> None:
    """Скачивает файлы с FTP-сервера."""
    try:
        log(f"Подключение к {server}...")
        with ftplib.FTP(server, timeout=30) as ftp:
            ftp.login(user, password)
            ftp.cwd(remote_path)
            ftp.set_pasv(True)
            
            files = [f for f in ftp.nlst() if not f.startswith('.')]  # Игнорируем скрытые файлы
            
            if not files:
                log(f"На сервере {server} нет файлов для скачивания.")
                return
                
            for file in files:
                local_file_path = os.path.join(local_path, file)
                try:
                    with open(local_file_path, 'wb') as f:
                        ftp.retrbinary(f'RETR {file}', f.write)
                    log(f"Успешно скачан {file}")
                except Exception as e:
                    log(f"Ошибка при скачивании {file}: {e}")
                    
    except Exception as e:
        log(f"Ошибка подключения к {server}: {e}")

def wait(seconds: int) -> None:
    """Ожидание с выводом оставшегося времени."""
    for remaining in range(seconds, 0, -1):
        hours, remainder = divmod(remaining, 3600)
        mins, secs = divmod(remainder, 60)
        print(f"\rОжидание следующего скачивания: {hours:02d}:{mins:02d}:{secs:02d}", end='')
        time.sleep(1)
    print()

def main() -> None:
    # Получаем пароль
    password = get_valid_password()
    if not password:
        log("Не удалось получить верный пароль. Завершение работы.")
        return

    if INITIAL_DELAY > 0:
        log(f"Ожидание перед первым скачиванием: {INITIAL_DELAY} секунд")
        time.sleep(INITIAL_DELAY)

    while True:
        try:
            download_folder = create_download_folder(LOCAL_BASE_PATH)
            
            # Скачивание с серверов
            download_ftp_files(FTP_SERVER1, FTP_USER, password, 
                             REMOTE_PATH, os.path.join(download_folder, 'us_1(93)'))
            
            download_ftp_files(FTP_SERVER2, FTP_USER, password, 
                             REMOTE_PATH, os.path.join(download_folder, 'us_2(92)'))
            
            wait(INTERVAL)
            
        except KeyboardInterrupt:
            log("Работа скрипта прервана пользователем.")
            break
        except Exception as e:
            log(f"Критическая ошибка: {e}. Повторная попытка через 5 минут.")
            time.sleep(300)

if __name__ == "__main__":
    main()
