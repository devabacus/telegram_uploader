import asyncio
from telegram_client import TelegramHandler
from file_automation import FileAutomation
from pathlib import Path

async def main():
    # Настройки
    telegram_window_name = "Telegram"  # Название окна Telegram
    directory = r"E:\library\3d models\3DSky Pro 3D-Models Collection April 2024\1234"
    files = Path(directory).glob("*")

    # Инициализация
    tg_handler = TelegramHandler()
    file_automation = FileAutomation(telegram_window_name)

    await tg_handler.start()

    for file_path in files:
        if not file_path.is_file():
            continue

        # Переключаемся на Telegram и вставляем файл
        file_automation.focus_telegram()
        file_automation.copy_paste_file(str(file_path))

        # Проверяем загрузку файла через Telegram API
        uploaded = await tg_handler.check_file_uploaded(file_path.name)
        if not uploaded:
            print(f"Не удалось загрузить файл {file_path.name}, пропускаем.")
            continue

    await tg_handler.stop()

if __name__ == "__main__":
    asyncio.run(main())



