from django.contrib import admin

from catalog.models import Category, ProductAttribute, PredefineAttributeValue

admin.site.register(Category)
admin.site.register(ProductAttribute)
admin.site.register(PredefineAttributeValue)
