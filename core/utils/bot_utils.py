from urllib.parse import urlparse, urlunparse
from core.models import NotificationSetting, Product
from core.parsing.yandex_market import get_yandex_market_product_price
from core.models import TelegramUser


def get_or_create_telegram_user(telegram_user_id):
    telegram_user, _ = TelegramUser.objects.get_or_create(
        telegram_user_id=telegram_user_id
    )

    return telegram_user


def get_or_create_notification_setting(telegram_user_id, product_id, desired_price):
    telegram_user = TelegramUser.objects.get(telegram_user_id=telegram_user_id)
    product = Product.objects.get(id=product_id)

    notification_setting, _ = NotificationSetting.objects.get_or_create(
        telegram_user=telegram_user, product=product, desired_price=desired_price
    )

    return notification_setting


def get_clean_url(url):
    parsed_url = urlparse(url)
    return urlunparse(
        (parsed_url.scheme, parsed_url.netloc, parsed_url.path, "", "", "")
    )


def check_link_host(url):
    parsed_url = urlparse(url)
    host_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    if host_url == "https://market.yandex.ru":
        return url, "Яндекс Маркет"
    else:
        raise ValueError("Unsupported host", host_url)


def handle_link(url: str, user_id: int) -> tuple[str, int]:
    host_url, platform = check_link_host(url)
    telegram_user = get_or_create_telegram_user(user_id)

    if Product.objects.filter(url=url).exists():
        return Product.objects.get(url=url, telegram_user=telegram_user)

    if platform == "Яндекс Маркет":
        title, price = get_yandex_market_product_price(host_url)
    else:
        raise ValueError("Unsupported host", host_url)

    product = Product.objects.create(
        title=title, price=price, telegram_user=telegram_user, url=url
    )

    return product
