from telegram import Bot
import os
import time
import asyncio
from config import *

# Ваш токен бота
BOT_TOKEN = TOKEN
GROUP_CHAT_ID = -1002338060250  # ID группы
TOPIC_ID = 4342  # ID топика

# Путь к папке с файлами
FILES_DIRECTORY = r"E:\library\3d models\KitBash3D - Spaceships\Render"

async def upload_files_to_telegram():
    # Инициализация бота
    bot = Bot(token=BOT_TOKEN)

    # Получаем список всех файлов в папке
    files = os.listdir(FILES_DIRECTORY)

    for file_name in files:
        file_path = os.path.join(FILES_DIRECTORY, file_name)
        
        if os.path.isfile(file_path):
            try:
                # Асинхронная отправка файла
                with open(file_path, "rb") as file:
                    await bot.send_document(chat_id=GROUP_CHAT_ID, document=file, caption=f"Загружен файл: {file_name}", message_thread_id=TOPIC_ID)
                print(f"Файл {file_name} успешно отправлен в топик {TOPIC_ID}.")
            except Exception as e:
                print(f"Ошибка при отправке файла {file_name}: {e}")

            # Пауза между отправками (опционально)
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(upload_files_to_telegram())