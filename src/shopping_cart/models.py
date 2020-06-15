import uuid
from django.db import models

from catalog.models import Product
from accounts.models import Vendor, Customer, Driver

# Create your models here.
class Basket(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, blank=True)

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.product.price for item in self.items.all()])

    def add_to_basket(self, product):
        order_item = OrderItem.objects.create(product=product, basket=self, vendor=product.vendor)
        self.items.add(order_item)

    def empty_basket(self):
        self.items.clear()

    def __str__(self):
        return f"{self.customer.get_name}'s basket"


class Order(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    ref_code = models.CharField(max_length=15)
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.SET_NULL, null=True)
    is_fulfilled = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{0} - {1}'.format(self.customer, self.ref_code)

    @property
    def get_order_total(self):
        return sum([item.product.price for item in self.items.all()])


class OrderItem(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.SET_NULL, null=True, blank=True)
    basket = models.ForeignKey(Basket, on_delete=models.SET_NULL, related_name='items', null=True, blank=True)
    vendor = models.ForeignKey(Vendor, related_name='order_items', on_delete=models.SET_NULL, null=True, blank=True)
    driver = models.ForeignKey(Driver, related_name='deliveries', on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    is_fulfilled = models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)

    @property
    def get_customer(self):
        return self.order.customer.get_company_name

    def __str__(self):
        return self.product.name