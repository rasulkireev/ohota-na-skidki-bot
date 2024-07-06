from django.db import models
from core.base_models import BaseModel


class TelegramUser(BaseModel):
    telegram_user_id = models.BigIntegerField(editable=False)
