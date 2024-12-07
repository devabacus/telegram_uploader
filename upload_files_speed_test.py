from telethon import TelegramClient
from telethon.errors import FloodWaitError
from pathlib import Path
import os
import asyncio
import logging
from datetime import datetime
import speedtest  # Новая библиотека для измерения скорости
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

# Списки расширений
ARCHIVE_EXTENSIONS = [".zip", ".rar", ".7z", ".tar", ".gz"]
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".webp"]

def measure_internet_speed():
    """Измеряет скорость интернет-соединения и возвращает словарь со скоростями."""
    try:
        logger.info("Измерение скорости интернет-соединения...")
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download()  # Скорость загрузки (бит/с)
        upload_speed = st.upload()      # Скорость выгрузки (бит/с)
        download_speed_mbps = download_speed / 1_000_000  # Перевод в Мбит/с
        upload_speed_mbps = upload_speed / 1_000_000      # Перевод в Мбит/с
        logger.info(f"Скорость загрузки: {download_speed_mbps:.2f} Мбит/с")
        logger.info(f"Скорость выгрузки: {upload_speed_mbps:.2f} Мбит/с")
        return {
            'download_speed_mbps': download_speed_mbps,
            'upload_speed_mbps': upload_speed_mbps
        }
    except Exception as e:
        logger.error(f"Не удалось измерить скорость интернета: {e}")
        return None

async def send_files(directory):
    """Отправляет файлы из указанной директории."""
    client = TelegramClient("session_name", API_ID, API_HASH)
    logger.info("Инициализация клиента Telegram...")
    await client.start(PHONE_NUMBER)
    logger.info("Клиент Telegram успешно запущен.")

    # Измеряем скорость интернет-соединения
    measure_internet_speed()

    # Сортируем файлы по типу
    directory_path = Path(directory)
    archives = [f for f in directory_path.iterdir() if f.suffix.lower() in ARCHIVE_EXTENSIONS]
    images = [f for f in directory_path.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS]

    logger.info(f"Найдено {len(archives)} архивов и {len(images)} изображений для загрузки.")

    # Сначала архивы
    logger.info("Начинается загрузка архивов...")
    await upload_files(client, archives, "архивы")

    # Затем изображения
    logger.info("Начинается загрузка изображений...")
    await upload_files(client, images, "изображения")

    logger.info("Все файлы успешно обработаны. Завершаем работу клиента Telegram...")
    await client.disconnect()
    logger.info("Клиент Telegram успешно отключен.")

async def upload_files(client, files, file_type):
    """Отправляет указанные файлы в чат."""
    for file_path in files:
        if file_path.is_file():
            # Проверка размера файла
            file_size = file_path.stat().st_size
            if file_size > MAX_FILE_SIZE:
                logger.error(f"Файл {file_path.name} превышает 3.5 ГБ ({file_size / (1024**3):.2f} ГБ) и не может быть отправлен.")
                continue

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
                file_size_mb = file_size / (1024 * 1024)  # Размер файла в МБ
                speed_mb_s = file_size_mb / elapsed_time if elapsed_time > 0 else 0
                logger.info(f"Файл {file_path.name} успешно отправлен в топик {TOPIC_ID}. Время отправки: {elapsed_time:.2f} секунд.")
                logger.info(f"Средняя скорость отправки файла: {speed_mb_s:.2f} МБ/с")
            except FloodWaitError as e:
                logger.error(f"Flood control: ожидание {e.seconds} секунд перед продолжением.")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                logger.error(f"Не удалось отправить файл {file_path.name}: {e}")

if __name__ == "__main__":
    # Запрос пути к директории у пользователя
    # input_path = input("Введите путь к директории с файлами (нажмите Enter для использования пути по умолчанию): ")
    # if not input_path.strip():
    #     input_path = r"E:\library\3d models\3DSky Pro 3D-Models Collection April 2024\1234"  # Значение по умолчанию
    input_path = r"E:\library\3d models\3DSky Pro 3D-Models Collection April 2024\1234"  # Значение по умолчанию

    # Проверяем, существует ли указанная директория
    if not os.path.isdir(input_path):
        logger.error("Указанная директория не существует. Проверьте путь и попробуйте снова.")
    else:
        asyncio.run(send_files(input_path))
