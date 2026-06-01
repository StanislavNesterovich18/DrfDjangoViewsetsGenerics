from datetime import datetime

from celery import shared_task

from users.models import User


@shared_task
def deactivate_users():
    list_users = User.objects.all()
    for user in list_users:
        if not user.last_activ:
            break
        last_active = (datetime.now() - user.last_active).days
        print(last_active)
        if last_active > 30:
            user.is_active = False
            user.save()
