from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, ModerationPermission


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~ModerationPermission,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                IsOwner,
            )
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (
                IsAuthenticated,
                IsOwner | ModerationPermission,
            )
        else:
            self.permission_classes = (IsAuthenticated,)

        return super(CourseViewSet, self).get_permissions()

    def get_queryset(self):
        if self.request.user.groups.filter(name="Модератор").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name="Модератор").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        ~ModerationPermission,
    ]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner | ModerationPermission,
    ]


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner | ModerationPermission,
    ]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwner,
    ]
