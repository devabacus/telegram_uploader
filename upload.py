from telethon import TelegramClient
from telethon.errors import FloodWaitError
from pathlib import Path
import os
import asyncio
import logging
from datetime import datetime
from config import *  # API_ID, API_HASH, PHONE_NUMBER должны быть определены в config.py

# Настройка логов
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = os.path.join(LOG_DIR, f"uploader_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_filename, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

# Конфигурация
CHAT_ID = -1002338060250  # Замените на ваш ID чата
TOPIC_ID = 4342  # Замените на ваш ID топика
MAX_FILE_SIZE = 3.5 * 1024 * 1024 * 1024  # Максимальный размер файла 3.5 ГБ
MAX_PARALLEL_UPLOADS = 20  # Максимальное количество параллельных загрузок

# Списки расширений
ARCHIVE_EXTENSIONS = [".zip", ".rar", ".7z", ".tar", ".gz"]
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]

async def send_files(directory):
    """Отправляет файлы из указанной директории."""
    client = TelegramClient("session_name", API_ID, API_HASH)
    logger.info("Инициализация клиента Telegram...")
    await client.start(PHONE_NUMBER)
    logger.info("Клиент Telegram успешно запущен.")

    # Сортируем файлы по типу
    directory_path = Path(directory)
    archives = [f for f in directory_path.iterdir() if f.suffix.lower() in ARCHIVE_EXTENSIONS]
    images = [f for f in directory_path.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS]

    logger.info(f"Найдено {len(archives)} архивов и {len(images)} изображений для загрузки.")

    # Сначала архивы
    logger.info("Начинается загрузка архивов...")
    await upload_files_parallel(client, archives, "архивы")

    # Затем изображения
    logger.info("Начинается загрузка изображений...")
    await upload_files_parallel(client, images, "изображения")

    logger.info("Все файлы успешно обработаны. Завершаем работу клиента Telegram...")
    await client.disconnect()
    logger.info("Клиент Telegram успешно отключен.")

async def upload_files_parallel(client, files, file_type):
    """Отправляет указанные файлы в чат параллельно."""
    semaphore = asyncio.Semaphore(MAX_PARALLEL_UPLOADS)  # Лимит на параллельные задачи

    async def upload_file(file_path):
        """Отправка одного файла."""
        async with semaphore:  # Учитываем лимит на параллельные задачи
            if file_path.is_file():
                # Проверка размера файла
                file_size = file_path.stat().st_size
                if file_size > MAX_FILE_SIZE:
                    logger.error(f"Файл {file_path.name} превышает 3.5 ГБ ({file_size / (1024**3):.2f} ГБ) и не может быть отправлен.")
                    return

                try:
                    # Отправка файла напрямую
                    start_time = datetime.now()
                    logger.info(f"Отправка {file_type}: {file_path.name} в топик {TOPIC_ID}...")
                    await client.send_file(
                        CHAT_ID,
                        file=file_path,  # Используем Path для прямой отправки
                        reply_to=TOPIC_ID,
                        # max_chunk_size=1024 * 1024
                    )
                    end_time = datetime.now()
                    elapsed_time = (end_time - start_time).total_seconds()
                    logger.info(f"Файл {file_path.name} успешно отправлен в топик {TOPIC_ID}. Время отправки: {elapsed_time:.2f} секунд.")
                except FloodWaitError as e:
                    logger.error(f"Flood control: ожидание {e.seconds} секунд перед продолжением.")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    logger.error(f"Не удалось отправить файл {file_path.name}: {e}")

    # Запуск задач параллельно
    tasks = [upload_file(file_path) for file_path in files]
    await asyncio.gather(*tasks)

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