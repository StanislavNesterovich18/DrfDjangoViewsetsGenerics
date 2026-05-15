from django.core.management import call_command
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment


class Command(BaseCommand):
    """Добавление фикстур в json файл"""

    help = "Добавление фикстур"

    def handle(self, *args, **kwargs):
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        Payment.objects.all().delete()
        call_command("loaddata", "fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully loaded data from fixture"))