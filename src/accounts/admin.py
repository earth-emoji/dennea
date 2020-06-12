from django.contrib import admin

from accounts.models import Customer, Vendor, Driver

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'name', 'customer_type', 'acl',)

    def name(self, obj):
        return obj.user.name

    def company_name(self, obj):
        return obj.user.company_name

    def email(self, obj):
        return obj.user.email

    def acl(self, obj):
        return obj.user.acl.name


admin.site.register(Customer, CustomerAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'name', 'acl', 'is_active')

    def name(self, obj):
        return obj.user.name

    def company_name(self, obj):
        return obj.user.company_name

    def email(self, obj):
        return obj.user.email

    def acl(self, obj):
        return obj.user.acl

admin.site.register(Vendor, VendorAdmin)

class DriverAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'email', 'name',)

    def name(self, obj):
        return obj.user.name

    def company_name(self, obj):
        return obj.user.company_name

    def email(self, obj):
        return obj.user.email

admin.site.register(Driver, DriverAdmin)
