from datetime import datetime, timedelta


from django.core.management.base import BaseCommand
from django.utils import timezone

from boards.models import Wind

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _create_data(self):
        dt = timezone.now()
        for x in range(1):
            Wind(created_at=dt,wind_speed=12, highest_gust=20).save()
            dt = dt + timedelta(seconds=15)

    def handle(self, *args, **options):
        self._create_data()


