from core.parsing.utils import get_html
from bs4 import BeautifulSoup


def get_yandex_market_product_price(url):
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")

    title_element = soup.find("h1", {"data-additional-zone": "title"})
    price_element = soup.find("h3", {"data-auto": "snippet-price-current"})

    title = title_element.get_text(strip=True) if title_element else "Title not found"
    price = (
        int("".join([t for t in price_element.contents if t.name is None]).strip())
        if price_element
        else "Price not found"
    )

    return title, price
