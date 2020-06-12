import uuid
from django.db import models

from catalog.models import Product
from accounts.models import Vendor, Customer, Driver

# Create your models here.
class Order(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    ref_code = models.CharField(max_length=15)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.SET_NULL, null=True)
    is_fulfilled = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.customer, self.ref_code)


class OrderItem(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    product = models.OneToOneField(Product, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, related_name='order_items', on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, related_name='deliveries', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, blank=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    def __str__(self):
        return self.product.name