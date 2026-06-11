from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import urls_validator


class LessonSerializer(serializers.ModelSerializer):
    url_video = serializers.CharField(validators=[urls_validator])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ["id", "name", "description", "lessons_count", "preview", "lessons"]
