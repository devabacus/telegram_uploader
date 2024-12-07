import asyncio
from datetime import datetime
from pathlib import Path
from telethon.errors import FloodWaitError
from logger import logger
from config import CHAT_ID, TOPIC_ID, MAX_FILE_SIZE


async def upload_files_with_retry(client, files, file_type, max_parallel=20):
    """Отправляет файлы с адаптивным числом параллельных загрузок."""
    current_parallelism = max_parallel
    while current_parallelism > 0:
        try:
            await upload_files_parallel(client, files, current_parallelism, file_type)
            break  # Успешно завершено
        except Exception as e:
            logger.error(f"Ошибка при загрузке с {current_parallelism} параллельными загрузками: {e}")
            current_parallelism -= 1
            logger.info(f"Пробуем с {current_parallelism} параллельными загрузками...")

    if current_parallelism == 0:
        logger.error("Не удалось загрузить файлы. Параллельные загрузки были уменьшены до 0.")


async def upload_files_parallel(client, files, parallelism, file_type):
    """Отправляет файлы в чат параллельно."""
    semaphore = asyncio.Semaphore(parallelism)

    async def upload_file(file_path):
        """Отправляет один файл."""
        async with semaphore:
            if file_path.is_file():
                file_size = file_path.stat().st_size
                if file_size > MAX_FILE_SIZE:
                    logger.error(f"Файл {file_path.name} превышает 3.5 ГБ ({file_size / (1024**3):.2f} ГБ).")
                    return

                try:
                    start_time = datetime.now()
                    logger.info(f"Отправка {file_type}: {file_path.name} в топик {TOPIC_ID}...")
                    await client.send_file(CHAT_ID, file=file_path, reply_to=TOPIC_ID)
                    elapsed_time = (datetime.now() - start_time).total_seconds()
                    logger.info(f"Файл {file_path.name} успешно отправлен за {elapsed_time:.2f} секунд.")
                except FloodWaitError as e:
                    logger.error(f"Flood control: ожидание {e.seconds} секунд.")
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    logger.error(f"Ошибка отправки файла {file_path.name}: {e}")
                    raise e  # Пробрасываем ошибку для обработки в `upload_files_with_retry`

    tasks = [upload_file(file_path) for file_path in files]
    await asyncio.gather(*tasks)
