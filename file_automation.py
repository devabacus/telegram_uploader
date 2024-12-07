import pyautogui
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileAutomation:
    def __init__(self, telegram_window_name):
        self.telegram_window_name = telegram_window_name

    def focus_telegram(self):
        """Фокусируем окно Telegram."""
        logger.info("Ищем окно Telegram...")
        pyautogui.getWindowsWithTitle(self.telegram_window_name)[0].activate()
        logger.info("Окно Telegram найдено и активно.")

    def copy_paste_file(self, file_path):
        """Копируем файл из проводника и вставляем в Telegram."""
        logger.info(f"Копирование файла: {file_path}")
        pyautogui.hotkey("ctrl", "c")  # Копируем файл
        time.sleep(1)
        pyautogui.hotkey("ctrl", "v")  # Вставляем файл в Telegram
        logger.info(f"Файл {file_path} вставлен в Telegram.")
        time.sleep(1)  # Даем время на обработку
