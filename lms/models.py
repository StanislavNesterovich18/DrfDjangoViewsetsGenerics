from django.conf import settings
from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    preview = models.ImageField(upload_to="course/image/", blank=True, null=True, verbose_name="Изображение")

    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    preview = models.ImageField(upload_to="lesson/image/", blank=True, null=True, verbose_name="Изображение")
    url_video = models.TextField()
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанный курс",
        related_name="lessons",
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Модель подписки пользователя на курс"""

    name = models.CharField(max_length=100, verbose_name="Название подписки", blank=True, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscriptions",
    )

    course = models.ForeignKey(
        settings.AUTH_COURSE_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscribers",
    )

    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = [["user", "course"]]
        ordering = ["-subscribed_at"]

    def __str__(self):
        return f"{self.user.email} -> {self.course.title}"
