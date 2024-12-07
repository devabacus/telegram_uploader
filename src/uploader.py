# src/uploader.py
import os
from telegram import Bot
from .logger import logger

class FileUploader:
    def __init__(self, bot: Bot, group_chat_id: int, topic_id: int):
        self.bot = bot
        self.group_chat_id = group_chat_id
        self.topic_id = topic_id

    async def upload_files(self, directory: str):
        files = os.listdir(directory)
        for file_name in files:
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "rb") as file:
                        await self.bot.send_document(
                            chat_id=self.group_chat_id,
                            document=file,
                            caption=f"Загружен файл: {file_name}",
                            message_thread_id=self.topic_id,
                        )
                    logger.info(f"Файл {file_name} успешно отправлен.")
                except Exception as e:
                    logger.error(f"Ошибка при отправке файла {file_name}: {e}")
