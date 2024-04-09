from django.contrib.auth import mixins as auth_mixins
from django.core.exceptions import PermissionDenied


class OwnerRequiredMixin(auth_mixins.LoginRequiredMixin):
    user_field = "user"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj_user = getattr(obj, self.user_field, None)
        if obj_user != self.request.user:
            raise PermissionDenied

        return obj


class AdminPermissionsRequiredMixin(auth_mixins.UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser


class IsStaffPermissionsRequiredMixin(auth_mixins.UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_staff


class IsSuperuserOrIsStaffPermissionsRequiredMixin(auth_mixins.UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.is_staff