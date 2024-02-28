from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum

from funds.models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from .permissions import IsPaymentAccount

from django.core.cache import cache


class CollectViewSet(viewsets.ModelViewSet):
    """Вьюсет Сборов."""

    queryset = (
        Collect.objects.annotate(pay_count=Count(
            'payment'))).annotate(
                collected=Sum('payment__amount')).order_by('-id')
    serializer_class = CollectSerializer
    http_method_names = ['get', 'post', 'update', 'delete']
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        cache.delete('collect_queryset')
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset_cache = cache.get('collect_queryset')
        if queryset_cache:
            return queryset_cache
        queryset_cache = super().get_queryset()
        cache.set(key='collect_queryset',
                  value=super().get_queryset(), timeout=30)
        return queryset_cache


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюсет Платежей."""

    queryset = Payment.objects.all().order_by('-id')
    serializer_class = PaymentSerializer
    http_method_names = ['get', 'post', 'update', 'delete']
    permission_classes = (IsAuthenticated, IsPaymentAccount, )

    def perform_create(self, serializer):
        cache.delete_many(['collect_queryset', 'payment_queryset'])
        return super().perform_create(serializer)

    def get_queryset(self):
        queryset_cache = cache.get('payment_queryset')
        if queryset_cache:
            return queryset_cache
        queryset_cache = super().get_queryset()
        cache.set(key='payment_queryset',
                  value=super().get_queryset(), timeout=30)
        return queryset_cache
