from django.contrib import admin

from lms.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Настройки интерфейса администрирования для модели Course"""

    list_display = ("id", "name")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Настройки интерфейса администрирования для модели Lesson"""

    list_display = ("id", "name")
