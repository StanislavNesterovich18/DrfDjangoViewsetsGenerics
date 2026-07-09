from django.urls import include, path
from rest_framework import routers

from lms.apps import LmsConfig
from lms.views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

app_name = LmsConfig.name
router = routers.DefaultRouter()
router.register(r"course", CourseViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("lesson/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path(
        "lesson/retrieve/<int:pk>/",
        LessonRetrieveAPIView.as_view(),
        name="lesson_retrieve",
    ),
    path("lesson/update/<int:pk>/", LessonUpdateAPIView.as_view(), name="lesson_update"),
    path(
        "lesson/destroy/<int:pk>/",
        LessonDestroyAPIView.as_view(),
        name="lesson_destroy",
    ),
]
