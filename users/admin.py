from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as g_l

from .models import User


@admin.action(description=g_l('Promote selected users to admin\
    (is_staff + role=\'admin\')'))
def make_admin(modeladmin, request, queryset):
    updated = 0
    for user in queryset:
        if not user.is_staff or user.role != 'admin':
            user.is_staff = True
            user.role = 'admin'
            user.save(update_fields=['is_staff', 'role'])
            updated += 1
    messages.success(request, g_l('%d user(s) promoted to admin.') % updated)


@admin.action(description=g_l('Revoke admin privileges from selected users\
    (is_staff=False, role=\'regular\')'))
def revoke_admin(modeladmin, request, queryset):
    updated = 0
    for user in queryset:
        if user.is_staff or user.role != 'regular':
            # adjust regular staff/admin flags
            if user.is_superuser:
                continue
            user.is_staff = False
            user.role = 'regular'
            user.save(update_fields=['is_staff', 'role'])
            updated += 1
    messages.success(request, g_l('%d user(s) demoted from admin.') % updated)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # preserve default BaseUserAdmin layout and add role
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role', {'fields': ('role',)}),
    )

    # show is_active in list_display because list_editable references it
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_staff',
        'is_active',
    )

    # allow quick editing of active state and role from changelist
    list_editable = ('is_active', 'role')

    actions = [make_admin, revoke_admin]

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    def get_actions(self, request):
        # only allow these actions for superusers
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            actions.pop('make_admin', None)
            actions.pop('revoke_admin', None)
        return actions
