from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import Pagination
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, ModerationPermission
from users.tasks import send_course_update


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = Pagination

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
        elif self.action in ["update", "partial_update"]:
            permission_cls = (
                IsAuthenticated,
                IsOwner | ModerationPermission,
            )
            self.permission_classes = permission_cls
            if all(permission_cls):
                send_course_update.delay("Курс обновлен", "Перейдите на сайт для ознакомление с обновлениями")

        elif self.action == "retrieve":
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
    pagination_class = Pagination

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


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.POST.get("id")
        try:
            course_item = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Курс не найден"}, status=status.HTTP_404_NOT_FOUND)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
        return Response({"message": message})
