from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CollectViewSet, PaymentViewSet

router = DefaultRouter()

router.register('collects',
                CollectViewSet,
                basename='collects',)

router.register('payments',
                PaymentViewSet,
                basename='payments',)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('', include(router.urls),),
]


# /payments/
# /collects/
