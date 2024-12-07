from telethon import TelegramClient, events
from config import *  # API_ID, API_HASH, PHONE_NUMBER должны быть определены в config.py

async def main():
    # Инициализация клиента
    client = TelegramClient("session_name", API_ID, API_HASH)
    await client.start(PHONE_NUMBER)

    @client.on(events.NewMessage)
    async def handler(event):
        """Обработчик сообщений."""
        # Реагируем только на сообщения с текстом 'id'
        if event.message.text.lower() == "id":
            # Получаем ID чата
            chat_id = event.chat_id

            # Получаем ID топика (если это форум)
            topic_id = event.message.reply_to.reply_to_msg_id if event.message.reply_to else None
            if not topic_id and event.is_channel and event.is_group:
                topic_id = event.message.id if event.is_reply else None

            # Формируем сообщение с информацией об ID
            response = f"Chat ID: {chat_id}\n"
            if topic_id:
                response += f"Topic ID: {topic_id}"
            else:
                response += "Topic ID: Not applicable (not a forum)."

            # Отправляем сообщение с ID
            await event.reply(response)

            # Удаляем сообщение "id"
            await event.delete()

    print("Бот запущен. Напишите 'id' в чат или топик, чтобы получить ID.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
