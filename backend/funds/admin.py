from django.contrib import admin
from django.db.models import Sum

from .models import Collect, Payment, Reason


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'get_payment_counter',
                    'get_payment_amount'
                    )
    readonly_fields = ('get_payment_counter',
                       'get_payment_amount')

    def get_payment_counter(self, obj):
        """Позволяет увидеть кол-во платежей."""
        return Payment.objects.filter(collect=obj).count()
    get_payment_counter.short_description = 'Всего в пожертвований'

    def get_payment_amount(self, obj):
        """Позволяет увидеть собранную сумму."""
        return Payment.objects.filter(
            collect=obj).aggregate(Sum('amount'))['amount__sum']
    get_payment_amount.short_description = 'Собранная сумма'


@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    pass
