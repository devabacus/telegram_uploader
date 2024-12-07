import asyncio
from telegram import Bot
from src.config import BOT_TOKEN, GROUP_CHAT_ID, TOPIC_ID, FILES_DIRECTORY
from src.uploader import FileUploader
from src.bot import create_bot_application
from src.logger import logger

async def upload_files(bot):
    """Функция для загрузки файлов."""
    uploader = FileUploader(bot, GROUP_CHAT_ID, TOPIC_ID)
    logger.info("Начинается загрузка файлов.")
    await uploader.upload_files(FILES_DIRECTORY)

def main():
    """Основная функция для запуска загрузки и бота."""
    bot = Bot(token=BOT_TOKEN)
    app = create_bot_application()

    # Используем asyncio для выполнения загрузки перед запуском бота
    loop = asyncio.get_event_loop()
    loop.run_until_complete(upload_files(bot))

    # Запускаем бота
    logger.info("Бот успешно инициализирован.")
    app.run_polling()

if __name__ == "__main__":
    main()
