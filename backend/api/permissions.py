from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPaymentAccount(BasePermission):
    """Доступ разрешен только для пользователей группы Payment."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Payment').exists()
