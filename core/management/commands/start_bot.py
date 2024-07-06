from django.core.management.base import BaseCommand
from core.bot import run_bot


class Command(BaseCommand):
    help = "Start the Telegram Bot Server"

    def handle(self, *args, **options):
        run_bot()
