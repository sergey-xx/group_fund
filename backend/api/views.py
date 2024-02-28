from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum

from funds.models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from .permissions import IsPaymentAccount


class CollectViewSet(viewsets.ModelViewSet):
    """Вьюсет Сборов."""

    queryset = (
        Collect.objects.annotate(pay_count=Count(
            'payment'))).annotate(collected=Sum('payment__amount'))
    serializer_class = CollectSerializer
    http_method_names = ['get', 'post', 'update', 'delete']
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюсет Платежей."""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    http_method_names = ['get', 'post', 'update', 'delete']
    permission_classes = (IsAuthenticated, IsPaymentAccount, )
