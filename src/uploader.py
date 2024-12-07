import asyncio
from telegram import Bot
from telegram.error import RetryAfter
from src.logger import logger
import os


class FileUploader:
    def __init__(self, bot, group_chat_id, topic_id):
        self.bot = bot
        self.group_chat_id = group_chat_id
        self.topic_id = topic_id

    async def upload_file(self, file_path: str, retries: int = 3):
        """Отправляет файл с несколькими попытками в случае ошибки."""
        attempt = 0
        while attempt < retries:
            try:
                with open(file_path, "rb") as file:
                    await self.bot.send_document(
                        chat_id=self.group_chat_id,
                        document=file,
                        caption=f"Загружен файл: {file_path}",
                        message_thread_id=self.topic_id,
                    )
                logger.info(f"Файл {file_path} успешно отправлен.")
                return  # Успешная отправка, выходим из метода
            except RetryAfter as e:
                wait_time = int(e.retry_after)
                logger.error(f"Flood control exceeded. Ожидание {wait_time} секунд.")
                await asyncio.sleep(wait_time)
            except NetworkError as e:
                attempt += 1
                logger.error(f"Ошибка сети при отправке {file_path}: {e}. Попытка {attempt}/{retries}")
                await asyncio.sleep(5)  # Подождать перед повтором
            except Exception as e:
                logger.error(f"Не удалось отправить файл {file_path}: {e}")
                break  # Прекратить попытки при неизвестной ошибке
        else:
            logger.error(f"Файл {file_path} не удалось отправить после {retries} попыток.")