from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from users.filters import PaymentFilter
from users.models import Payment
from users.serializers import PaySerializer


class PayList(viewsets.ReadOnlyModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaySerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = PaymentFilter
    ordering_fields = ["date_pay"]
