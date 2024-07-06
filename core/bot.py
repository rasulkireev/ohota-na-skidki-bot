from asgiref.sync import sync_to_async
from django.conf import settings
from telegram import BotCommand, Update
from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    ContextTypes,
)

from core.utils import get_or_create_telegram_user, get_ohota_na_skidki_bot_logger

logger = get_ohota_na_skidki_bot_logger(__name__)


async def post_init(application) -> None:
    await application.bot.set_my_commands(
        [
            BotCommand("help", "Помощь"),
            BotCommand("start", "Начать диалог"),
        ],
        language_code="ru",
    )
    await application.bot.set_chat_menu_button()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user = await sync_to_async(get_or_create_telegram_user)(
        update.message.from_user.id
    )

    logger.info(
        "/start command requested", telegram_user_id=telegram_user.telegram_user_id
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Привет, как дела?"
    )
    logger.info(
        "/start command executed", telegram_user_id=telegram_user.telegram_user_id
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user = await sync_to_async(get_or_create_telegram_user)(
        update.message.from_user.id
    )

    logger.info(
        "/help command requested", telegram_user_id=telegram_user.telegram_user_id
    )
    text = (
        "Here are the commands you can use:\n\n"
        "/help - Show this help message\n"
        "/start - Get a welcome message\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    logger.info(
        "/help command executed", telegram_user_id=telegram_user.telegram_user_id
    )


def run_bot():
    application = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    logger.info("Started the Telegram Bot Server")

    start_handler = CommandHandler("start", start)
    caps_handler = CommandHandler("help", help)

    application.add_handler(start_handler)
    application.add_handler(caps_handler)

    application.run_polling()
