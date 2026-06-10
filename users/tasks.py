from datetime import datetime

from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
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

@shared_task
def send_course_update(theme, body):
    all_users = User.objects.all()
    for user in all_users:
        try:
            send_mail(theme, body, EMAIL_HOST_USER,[user.email])
        except Exception as e:
            raise e


