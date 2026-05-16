from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models

from lms.models import Course, Lesson


class UserManager(BaseUserManager):
    """Менеджер для модели User"""

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
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

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"<{self.email}>"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


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
