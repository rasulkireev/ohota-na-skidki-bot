from scrapingbee import ScrapingBeeClient
from django.conf import settings


def get_html(url: str) -> str:
    client = ScrapingBeeClient(api_key=settings.SCRAPING_BEE_TOKEN)
    response = client.get(
        url,
        params={
            "premium_proxy": "True",
            "country_code": "ru",
        },
    )

    return response.content
