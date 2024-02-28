# group_fund

Тестовое задание

Локальный запуск проекта
```
docker compose up -d
```

Применить миграции
```
docker compose exec backend python manage.py migrate
```

Создать суперпользователя
```
docker compose exec backend python manage.py createsuperuser --username admin --email admin@admin.ru
```

Наполнить базу моковыми данными
Где 200 - количество пользователей
```
docker compose exec backend python manage.py generatedata 200
```

Сгенерировать статику
```
docker compose exec backend python manage.py collectstatic
```

Админка будет доступна по адресу

http://localhost:8051/admin/

API

http://localhost:8051/api/v1/

Письма "отправляются" в консоль. Для тестирования отправки писем
```
docker compose logs worker -f
```

Документация API:
docs/schema.yaml

Для работы с платежами создан кастомный пермишн IsPaymentAccount
Для его работы нужно создать группу "Payment" и добавить в нее нужного пользователя
Но для простоты тестирования используется IsAdminUser (см. IsPaymentAccount)

