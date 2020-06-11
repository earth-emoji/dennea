from django.contrib import admin

from catalog.models import Category, Product, ProductAttribute, PredefineAttributeValue

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductAttribute)
admin.site.register(PredefineAttributeValue)
