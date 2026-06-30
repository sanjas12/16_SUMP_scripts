import pytest
import os
import shutil
from datetime import datetime
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Импортируем тестируемые функции
from auto_back_up import log, get_valid_password, create_download_folder, download_ftp_files, wait

@pytest.fixture
def temp_dir():
    """Фикстура для временной директории"""
    test_dir = "test_temp"
    os.makedirs(test_dir, exist_ok=True)
    yield test_dir
    shutil.rmtree(test_dir, ignore_errors=True)

@pytest.fixture
def log_file(temp_dir):
    """Фикстура для тестового лог-файла"""
    return os.path.join(temp_dir, "test.log")

def test_log(log_file):
    """Тест функции логирования"""
    with patch('auto_back_up.LOG_FILE', log_file):
        log("Test message")
        
        assert os.path.exists(log_file)
        with open(log_file, 'r') as f:
            assert "Test message" in f.read()

@pytest.mark.parametrize("input_pass,expected", [
    ("rs_pdu", "rs_pdu"),  # Верный пароль
    ("wrong", None),       # Неверный пароль
])
def test_get_valid_password(input_pass, expected):
    """Параметризованный тест проверки пароля"""
    with patch('getpass.getpass', return_value=input_pass):
        assert get_valid_password(attempts_limit=1) == expected

def test_create_download_folder(temp_dir):
    """Тест создания папки для загрузки"""
    folder_path = create_download_folder(temp_dir)
    
    assert os.path.exists(folder_path)
    assert os.path.exists(os.path.join(folder_path, 'us_1(93)'))
    assert os.path.exists(os.path.join(folder_path, 'us_2(92)'))

def test_download_ftp_files(temp_dir):
    """Тест загрузки файлов с FTP (с моками)"""
    mock_ftp = MagicMock()
    mock_ftp.nlst.return_value = ["file1.txt", "file2.txt"]
    
    with patch('ftplib.FTP', return_value=mock_ftp):
        test_path = os.path.join(temp_dir, "ftp_test")
        os.makedirs(test_path, exist_ok=True)
        
        download_ftp_files(
            server="test.server",
            user="user",
            password="pass",
            remote_path="/remote",
            local_path=test_path
        )
        
        mock_ftp.login.assert_called_once_with("user", "pass")
        assert mock_ftp.retrbinary.call_count == 2

def test_wait(capsys):
    """Тест функции ожидания с перехватом вывода"""
    with patch('time.sleep') as mock_sleep:
        wait(3)
        
        captured = capsys.readouterr()
        assert "00:00:03" in captured.out
        assert "00:00:01" in captured.out
        assert mock_sleep.call_count == 3

@pytest.mark.parametrize("initial_delay,expected_calls", [
    (0, 2),  # Без задержки - два вызова загрузки
    (1, 2),  # С задержкой - тоже два вызова
])
def test_main(initial_delay, expected_calls, temp_dir):
    """Интеграционный тест основной функции"""
    with patch('auto_back_up.INITIAL_DELAY', initial_delay), \
         patch('auto_back_up.INTERVAL', 1), \
         patch('auto_back_up.LOCAL_BASE_PATH', temp_dir), \
         patch('auto_back_up.get_valid_password', return_value="test_pass"), \
         patch('auto_back_up.download_ftp_files') as mock_download, \
         patch('auto_back_up.time.sleep', side_effect=KeyboardInterrupt):
            
        from auto_back_up import main
        main()
        
        assert mock_download.call_count == expected_calls