from rest_framework.permissions import BasePermission


class IsPaymentAccount(BasePermission):
    """Доступ разрешен только для пользователей группы Payment."""

    def has_object_permission(self, request, view, obj):
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(request.user.group)
        return False
