
from django.core.management.base import BaseCommand

from boards.models import Wind

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _delete_data(self):
        w = Wind.objects.all().delete()


    def handle(self, *args, **options):
        self._delete_data()


