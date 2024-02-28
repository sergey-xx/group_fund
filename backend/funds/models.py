from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Reason(models.Model):
    """Модель Поводов."""

    title = models.CharField('Повод', max_length=100)

    def __str__(self) -> str:
        return self.title


class Collect(models.Model):
    """Модель Сборов."""

    author = models.ForeignKey(User,
                               null=True,
                               blank=False,
                               on_delete=models.SET_NULL,
                               verbose_name='Автор')
    title = models.CharField('Название', max_length=100)
    reason = models.ForeignKey(Reason,
                               null=True,
                               blank=False,
                               on_delete=models.SET_NULL,
                               verbose_name='Повод')
    description = models.CharField('Описание', max_length=1000)
    target_sum = models.DecimalField('Целевая сумма',
                                     max_digits=20,
                                     decimal_places=2,
                                     null=False,
                                     blank=False)
    image = models.ImageField(blank=True)
    finish_date = models.DateTimeField('Время окончания')

    def __str__(self) -> str:
        return self.title


class Payment(models.Model):
    """Модель платежей."""

    amount = models.DecimalField('Размер платежа',
                                 max_digits=10,
                                 decimal_places=2,
                                 null=False,
                                 blank=False)

    payer = models.ForeignKey(User,
                              on_delete=models.PROTECT,
                              null=False,
                              verbose_name='Плательщик')
    date = models.DateTimeField('Время платежа',
                                auto_now_add=True)
    collect = models.ForeignKey(Collect,
                                null=False,
                                blank=False,
                                on_delete=models.PROTECT,
                                related_name='payment',
                                verbose_name='Сбор')

    def __str__(self) -> str:
        return str(self.payer) + ' ' + str(self.collect)
