from django.db import models
from core.base_models import BaseModel


class TelegramUser(BaseModel):
    telegram_user_id = models.BigIntegerField(editable=False)


class Product(BaseModel):
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)

    url = models.URLField(max_length=500)
    title = models.TextField()
    price = models.CharField(max_length=255)


class NotificationSetting(BaseModel):
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    desired_price = models.CharField(max_length=255)
