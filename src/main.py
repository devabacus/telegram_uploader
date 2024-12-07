# src/main.py
import asyncio
from telegram import Bot
from .config import BOT_TOKEN, GROUP_CHAT_ID, TOPIC_ID, FILES_DIRECTORY
from .uploader import FileUploader
from .bot import create_bot_application
from .logger import logger


async def main():
    bot = Bot(token=BOT_TOKEN)
    uploader = FileUploader(bot, GROUP_CHAT_ID, TOPIC_ID)

    # Загружаем файлы
    logger.info("Начинается загрузка файлов.")
    await uploader.upload_files(FILES_DIRECTORY)

    # Запускаем бота
    app = create_bot_application()
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
