from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from src.config import *
# Ваш токен бота
BOT_TOKEN = TOKEN

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик входящих сообщений."""
    message_text = update.message.text.lower()  # Приводим текст к нижнему регистру для проверки
    print(message_text)
    chat_id = update.effective_chat.id
    topic_id = update.message.message_thread_id  # ID топика (будет None, если сообщение не из топика)
    
    if message_text == "id":
        response = f"Chat ID: {chat_id}"
        if topic_id is not None:
            response += f"\nTopic ID: {topic_id}"
        await update.message.reply_text(response)

def main():
    # Инициализация приложения
    app = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчик текстовых сообщений
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()
