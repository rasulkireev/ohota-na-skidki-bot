from asgiref.sync import sync_to_async
from django.conf import settings
from telegram import BotCommand, Update
from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

from core.utils.core_utils import get_ohota_na_skidki_bot_logger
from core.utils.bot_utils import (
    check_link_host,
    get_clean_url,
    handle_link,
    get_or_create_telegram_user,
    get_or_create_notification_setting,
)

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
        chat_id=update.effective_chat.id,
        text="Привет, чтобы отслеживать цену товара, просто отправьте ссылку на него.",
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
        "Чтобы отслеживать цену товара, просто отправьте ссылку на него\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    logger.info(
        "/help command executed", telegram_user_id=telegram_user.telegram_user_id
    )


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_user = await sync_to_async(get_or_create_telegram_user)(
        update.message.from_user.id
    )

    logger.info("URL message received", telegram_user_id=telegram_user.telegram_user_id)

    url = get_clean_url(update.message.text)
    try:
        url, platform = check_link_host(url)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Обрабатываем товар из {platform}"
        )
    except ValueError as e:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=f"Неизвестный хост: {e}"
        )
        return

    product = await sync_to_async(handle_link)(url, telegram_user.telegram_user_id)

    context.user_data["product_id"] = product.id
    context.user_data["awaiting_price"] = True

    text = (
        f"Товар найден.\n"
        f"Наименования: {product.title}\n"
        f"Цена: {product.price}\n"
        f"При какой цене вы бы хотели чтобы мы вас уведомили?\n"
        f"Отправьте сообщение в следующем формате: 1000"
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    logger.info(
        "URL message processed", telegram_user_id=telegram_user.telegram_user_id
    )


async def handle_price_threshold(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info("Price threshold message received")
    if not context.user_data.get("awaiting_price"):
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Сначала отправьте ссылку на товар."
        )
        return

    telegram_user = await sync_to_async(get_or_create_telegram_user)(
        update.message.from_user.id
    )
    product_id = context.user_data.get("product_id")
    desired_price = int(update.message.text)

    notification_setting = await sync_to_async(get_or_create_notification_setting)(
        telegram_user.telegram_user_id, product_id, desired_price
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Вам придет уведомление, когда цена на товара достигнет {notification_setting.desired_price} рублей.",
    )
    logger.info(
        "Price threshold set",
        telegram_user_id=telegram_user.telegram_user_id,
        desired_price=desired_price,
    )
    context.user_data["awaiting_price"] = False


def run_bot():
    application = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_BOT_TOKEN)
        .post_init(post_init)
        .build()
    )
    logger.info("Started the Telegram Bot Server")

    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    url_handler = MessageHandler(filters.Entity("url"), handle_url)
    price_handler = MessageHandler(
        filters.TEXT & filters.Regex(r"^\d+$"), handle_price_threshold
    )

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(url_handler)
    application.add_handler(price_handler)

    application.run_polling()
