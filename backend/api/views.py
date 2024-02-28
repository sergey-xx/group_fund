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
    cache_key = 'collect_queryset'

    def get_queryset(self):
        queryset_cache = cache.get(self.cache_key)
        if queryset_cache:
            return queryset_cache
        queryset_cache = super().get_queryset()
        cache.set(key=self.cache_key,
                  value=super().get_queryset(), timeout=30)
        return queryset_cache

    def perform_create(self, serializer):
        cache.delete(self.cache_key)
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        cache.delete(self.cache_key)
        return super().perform_destroy(instance)

    def perform_update(self, serializer):
        cache.delete(self.cache_key)
        return super().perform_update(serializer)


class PaymentViewSet(viewsets.ModelViewSet):
    """Вьюсет Платежей."""

    queryset = Payment.objects.all().order_by('-id')
    serializer_class = PaymentSerializer
    http_method_names = ['get', 'post', 'update', 'delete']
    permission_classes = (IsAuthenticated, IsPaymentAccount, )
    cache_key = 'payment_queryset'

    def get_queryset(self):
        queryset_cache = cache.get(self.cache_key)
        if queryset_cache:
            return queryset_cache
        queryset_cache = super().get_queryset()
        cache.set(key=self.cache_key,
                  value=super().get_queryset(),
                  timeout=30)
        return queryset_cache

    def perform_create(self, serializer):
        cache.delete_many([CollectViewSet.cache_key, self.cache_key])
        return super().perform_create(serializer)

    def perform_destroy(self, instance):
        cache.delete_many([CollectViewSet.cache_key, self.cache_key])
        return super().perform_destroy(instance)

    def perform_update(self, serializer):
        cache.delete_many([CollectViewSet.cache_key, self.cache_key])
        return super().perform_update(serializer)
