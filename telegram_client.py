from telethon import TelegramClient
from telethon.errors import FloodWaitError
import asyncio
import logging
from config import API_ID, API_HASH, PHONE_NUMBER, CHAT_ID, TOPIC_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramHandler:
    def __init__(self):
        self.client = TelegramClient("session_name", API_ID, API_HASH)

    async def start(self):
        """Запускаем клиент Telegram."""
        logger.info("Запуск клиента Telegram...")
        await self.client.start(PHONE_NUMBER)
        logger.info("Клиент Telegram успешно запущен.")

    async def check_file_uploaded(self, file_name):
        """Проверяем, загрузился ли файл в указанный топик."""
        async for message in self.client.iter_messages(CHAT_ID, reply_to=TOPIC_ID):
            if file_name in message.file.name:
                logger.info(f"Файл {file_name} успешно загружен.")
                return True
        logger.warning(f"Файл {file_name} не найден в топике.")
        return False

    async def stop(self):
        """Останавливаем клиент Telegram."""
        await self.client.disconnect()
        logger.info("Клиент Telegram отключён.")
