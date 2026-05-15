from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Добавление фикстур в json файл"""

    help = "Добавление фикстур"

    def handle(self, *args, **kwargs):
        user = User.objects.create(email='admin@admin.ru')
        user.set_password('123')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.stdout.write(self.style.SUCCESS("Пользователь создан"))