from rest_framework import permissions

class IsVisitor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Посетитель').exists() or request.user.is_superuser

class IsWatcher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['Посетитель', 'Смотритель']).exists() or request.user.is_superuser

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Администратор').exists() or request.user.is_superuser
