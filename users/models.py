from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from lms.models import Course, Lesson


class User(AbstractBaseUser):
    """Переопределение абстрактной модели пользователя"""

    username = None
    avatar = models.ImageField(
        null=True, blank=True, upload_to="avatars", verbose_name="Аватар"
    )
    numbers_phone = models.CharField(
        null=True, blank=True, verbose_name="Номер телефона"
    )
    city = models.CharField(max_length=300, null=True, blank=True, verbose_name="Город")

    email = models.EmailField(
        unique=True, verbose_name="почта", null=False, blank=False
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"<{self.email}>"


class Payment(models.Model):
    CASH = "cash"
    CHECK = "check"
    TYPE_PAY = {
        CASH: "Наличные",
        CHECK: "Счет",
    }
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, verbose_name="Пользователь"
    )
    date_pay = models.DateTimeField(auto_now=True, verbose_name="Дата оплаты")
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, verbose_name="Оплата курса"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, null=True, verbose_name="Оплата урока"
    )
    amount_pay = models.PositiveIntegerField(default=0, verbose_name="Сумма оплаты")
    type_pay = models.CharField(
        max_length=5,
        choices=TYPE_PAY,
        default=CHECK,
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"<{self.user}>"
