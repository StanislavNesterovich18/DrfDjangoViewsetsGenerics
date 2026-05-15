from django.urls import path, include
from rest_framework import routers

from lms.apps import LmsConfig
from lms.views import CourseViewSet, LessonListAPIView, LessonCreateAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView

app_name = LmsConfig.name
router = routers.DefaultRouter()
router.register(r'course', CourseViewSet)
print(router.urls)

urlpatterns = [
    path('', include(router.urls)),
    path('lesson/', LessonListAPIView.as_view()),
    path('lesson/create/', LessonCreateAPIView.as_view()),
    path('lesson/retrieve/', LessonRetrieveAPIView.as_view()),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view()),
    path('lesson/destroy/<int:pk>/', LessonDestroyAPIView.as_view()),
]
