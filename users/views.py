from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from lms.models import Course
from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import PaySerializer, UserCreateSerializer, UserSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


class PayList(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = PaymentFilter
    ordering_fields = ["date_pay"]

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course_id = request.data["course_id"] if "course_id" in request.data else None
        amount_pay = request.data["amount_pay"] if "amount_pay" in request.data else None
        type_pay = request.data["type_pay"] if "type_pay" in request.data else None
        print(course_id, amount_pay, type_pay)
        if not course_id:
            return Response({"error": "Course ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not amount_pay:
            return Response({"error": "Amount payment is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not type_pay:
            return Response({"error": "Payment type is required cash | check"}, status=status.HTTP_400_BAD_REQUEST)
        course = Course.objects.get(pk=course_id)
        amount_pay = amount_pay * 100
        obj_payment = Payment.objects.create(
            course_id=course.pk,
            amount_pay=amount_pay,
            type_pay=type_pay,
        )
        stripe_product = create_stripe_product(course.name)
        stripe_price = create_stripe_price(stripe_product, amount_pay)
        stripe_session = create_stripe_session(stripe_price)
        obj_payment.stripe_price_id = stripe_price
        obj_payment.stripe_session_id = stripe_session
        obj_payment.stripe_product_id = stripe_product
        obj_payment.save()
        return Response({'url': stripe_session['url'], 'price_id': stripe_price['id']},
                        status=status.HTTP_201_CREATED
                        )


class CreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated()]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated()]
