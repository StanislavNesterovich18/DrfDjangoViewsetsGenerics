from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "password")


class PaySerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source="user.email", read_only=True)
    course_name = serializers.CharField(
        source="course.name", read_only=True, allow_null=True
    )
    lesson_name = serializers.CharField(
        source="lesson.name", read_only=True, allow_null=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "user_email",
            "course_name",
            "lesson_name",
            "amount_pay",
            "type_pay",
            "date_pay",
        ]
