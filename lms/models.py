from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    preview = models.ImageField(upload_to="course/image/", blank=True, null=True, verbose_name="Изображение")

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
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name="Связанный курс", related_name="lessons")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


