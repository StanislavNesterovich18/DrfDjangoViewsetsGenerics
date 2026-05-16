from django.contrib import admin

from users.models import User, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Настройки интерфейса администрирования для модели User"""

    list_display = ("id", "email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Настройки интерфейса администрирования для модели Payment"""

    list_display = ("id",)
