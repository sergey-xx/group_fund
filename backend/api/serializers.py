import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from funds.models import Collect, Payment, Reason


class Base64ImageField(serializers.ImageField):
    """Сериализатор картинок в Base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор объектов Платежей."""

    class Meta:
        model = Payment
        fields = ('id',
                  'amount',
                  'payer',
                  'date',
                  'collect',
                  )
        read_only_fields = ('id',)


class CollectSerializer(serializers.ModelSerializer):
    """Сериализатор объектов Сбора."""

    pay_count = serializers.IntegerField(read_only=True)
    collected = serializers.DecimalField(max_digits=10,
                                         decimal_places=2,
                                         read_only=True)
    payments = PaymentSerializer(source='payment', many=True, read_only=True)
    image = Base64ImageField(required=False)
    reason = serializers.PrimaryKeyRelatedField(required=True,
                                                queryset=Reason.objects.all())

    class Meta:
        model = Collect
        fields = ('id',
                  'author',
                  'title',
                  'reason',
                  'description',
                  'target_sum',
                  'collected',
                  'pay_count',
                  'image',
                  'finish_date',
                  'payments'
                  )
        read_only_fields = ('id',)
