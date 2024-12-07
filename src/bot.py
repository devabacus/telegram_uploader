# src/bot.py
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from .config import BOT_TOKEN, GROUP_CHAT_ID, TOPIC_ID
from .logger import logger

async def handle_id_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает запрос ID."""
    chat_id = update.effective_chat.id
    topic_id = update.message.message_thread_id
    response = f"Chat ID: {chat_id}\n"
    if topic_id:
        response += f"Topic ID: {topic_id}"
    await update.message.reply_text(response)

def create_bot_application():
    """Создаёт и возвращает объект приложения бота."""
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_id_request))
    logger.info("Бот успешно инициализирован.")
    return app
