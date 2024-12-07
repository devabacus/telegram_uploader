import asyncio
from pathlib import Path
from telethon import TelegramClient
from config import API_ID, API_HASH, PHONE_NUMBER, ARCHIVE_EXTENSIONS, IMAGE_EXTENSIONS
from logger import logger
from uploader import upload_files_with_retry


async def send_files(directory):
    client = TelegramClient("session_name", API_ID, API_HASH)
    logger.info("Инициализация клиента Telegram...")
    await client.start(PHONE_NUMBER)
    logger.info("Клиент Telegram успешно запущен.")

    # Сортируем файлы по типу
    directory_path = Path(directory)
    archives = [f for f in directory_path.iterdir() if f.suffix.lower() in ARCHIVE_EXTENSIONS]
    images = [f for f in directory_path.iterdir() if f.suffix.lower() in IMAGE_EXTENSIONS]

    logger.info(f"Найдено {len(archives)} архивов и {len(images)} изображений для загрузки.")

    # Загрузка файлов с адаптивным числом параллельных задач
    logger.info("Начинается загрузка архивов...")
    await upload_files_with_retry(client, archives, "архивы", max_parallel=20)

    logger.info("Начинается загрузка изображений...")
    await upload_files_with_retry(client, images, "изображения", max_parallel=20)

    logger.info("Все файлы успешно обработаны. Завершаем работу клиента Telegram...")
    await client.disconnect()
    logger.info("Клиент Telegram успешно отключен.")


if __name__ == "__main__":
    input_path = input("Введите путь к директории с файлами (нажмите Enter для использования пути по умолчанию): ")
    if not input_path.strip():
        input_path = r"E:/library/3d models/KitBash3D - Spaceships/Render"  # Значение по умолчанию

    if not Path(input_path).is_dir():
        logger.error("Указанная директория не существует. Проверьте путь и попробуйте снова.")
    else:
        asyncio.run(send_files(input_path))
