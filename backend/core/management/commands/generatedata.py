import random
import string

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from funds.models import Collect, Payment, Reason

User = get_user_model()


def get_random_string(length):
    """Генерирует случайную строку заданной длины."""
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


class Command(BaseCommand):
    """Команда для генерации данных."""

    help = 'Generate test data command.'

    def add_arguments(self, parser):
        parser.add_argument("amount", nargs="+", type=int)

    def generate_users(self, amount):
        users = []
        for i in range(amount):
            username = get_random_string(10) + str(i)
            users.append(
                User(username=username,
                     first_name=get_random_string(5),
                     last_name=get_random_string(5),
                     password=get_random_string(10),
                     email=(get_random_string(5) + '@' + 'dom.com')
                     )
                     )
        User.objects.bulk_create(users,
                                 batch_size=100,
                                 ignore_conflicts=True)
        print('Пользователи созданы!')

    def generate_reasons(self):
        reasons = []
        for i in range(10):
            reasons.append(
                Reason(
                    title=get_random_string(5)
                )
            )
        Reason.objects.bulk_create(reasons)
        print('Поводы созданы!')

    def generate_collects(self):
        collects = []
        for user in User.objects.all():
            for reason in Reason.objects.all():
                collects.append(
                    Collect(
                        author=user,
                        title=get_random_string(5),
                        reason=reason,
                        description=get_random_string(100),
                        target_sum=random.randint(1, 100000),
                        finish_date='2024-12-28T11:31:42.863105Z'
                    )
                )
        Collect.objects.bulk_create(collects,
                                    batch_size=100,
                                    ignore_conflicts=True)
        print('Сборы созданы!')

    def generate_payments(self):
        collects = Collect.objects.all()
        users = User.objects.all()
        payments = []
        for collect in collects:
            payments.append(
                    Payment(
                        payer=random.choice(users),
                        amount=random.randint(1, 1000),
                        collect=collect))
        Payment.objects.bulk_create(payments,
                                    batch_size=100,
                                    ignore_conflicts=True)
        print('Платежи созданы!')

    def handle(self, *args, **options):
        amount = options['amount'][0]
        self.generate_users(amount)
        self.generate_reasons()
        self.generate_collects()
        self.generate_payments()
