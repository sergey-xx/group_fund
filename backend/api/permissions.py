from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsPaymentAccount(BasePermission):
    """Доступ разрешен только для пользователей группы Payment."""

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.groups.filter(name='Payment').exists()
