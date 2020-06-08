from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User, Acl

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('company_name', 'email', 'photo', 'password')}),
        (_('Personal info'), {'fields': ('name', 'date_of_birth', 'sex')}),
        (_('Permissions'), {'fields': ('is_active', 'is_customer', 'is_vendor', 'is_staff', 'is_superuser',
                                       'acl', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('company_name', 'email', 'name', 'photo', 'password1', 'password2'),
        }),
    )
    list_display = ('company_name', 'email', 'name', 'acl', 'is_staff', 'is_customer', 'is_vendor',)
    list_filter = ('is_staff', 'is_customer', 'is_vendor',)
    search_fields = ('company_name','email', 'name',)
    ordering = ('company_name',)

admin.site.register(Acl)
