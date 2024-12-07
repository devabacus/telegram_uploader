from telethon import TelegramClient
from telethon.errors import FloodWaitError
import os
import asyncio
import logging
from datetime import datetime
import ctypes
from config import *  # API_ID, API_HASH, PHONE_NUMBER должны быть определены в config.py

# Устанавливаем кодировку UTF-8 в консоли Windows
if os.name == "nt":
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)

# Создание папки для логов
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Уникальное имя файла логов
log_filename = os.path.join(LOG_DIR, f"uploader_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# ID супергруппы
CHAT_ID = -1002338060250  # Замените на ваш ID чата (добавьте "-" для супергруппы)

# ID топика
TOPIC_ID = 4342  # Замените на ваш ID топика

MAX_FILE_SIZE = 3.5 * 1024 * 1024 * 1024  # Максимальный размер файла 3.5 ГБ


async def send_files(directory):
    """Отправляет файлы из указанной директории в указанный топик Telegram."""
    # Инициализация клиента
    client = TelegramClient("session_name", API_ID, API_HASH)
    await client.start(PHONE_NUMBER)

    # Получаем список всех файлов в директории
    files = os.listdir(directory)

    for file_name in files:
        file_path = os.path.join(directory, file_name)
        if os.path.isfile(file_path):
            # Проверка размера файла
            file_size = os.path.getsize(file_path)
            if file_size > MAX_FILE_SIZE:
                logger.error(f"Файл {file_name} превышает 3.5 ГБ ({file_size / (1024**3):.2f} ГБ) и не может быть отправлен.")
                continue

            try:
                # Отправка файла в указанный топик
                logger.info(f"Отправка файла: {file_name} в топик {TOPIC_ID}...")
                await client.send_file(
                    CHAT_ID,
                    file_path,
                    caption=f"Загружен файл: {file_name}",
                    reply_to=TOPIC_ID,
                )
                logger.info(f"Файл {file_name} успешно отправлен в топик {TOPIC_ID}.")
            except FloodWaitError as e:
                logger.error(f"Flood control: ожидание {e.seconds} секунд.")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                logger.error(f"Не удалось отправить файл {file_name}: {e}")

    await client.disconnect()


if __name__ == "__main__":
    # Запрос пути к директории у пользователя
    input_path = input("Введите путь к директории с файлами (нажмите Enter для использования пути по умолчанию): ")
    if not input_path.strip():
        input_path = r"E:/library/3d models/KitBash3D - Spaceships/Render"  # Значение по умолчанию

    # Проверяем, существует ли указанная директория
    if not os.path.isdir(input_path):
        logger.error("Указанная директория не существует. Проверьте путь и попробуйте снова.")
    else:
        asyncio.run(send_files(input_path))
