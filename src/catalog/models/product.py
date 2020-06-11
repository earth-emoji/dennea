import uuid
from datetime import datetime
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify

from accounts.models import Vendor
from photos.models import Album
from users.models import Acl

from catalog.models import Category

class ProductAttribute(models.Model):
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    name = models.CharField(max_length=255)
    is_aux = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'product attribute'
        verbose_name_plural = 'product attributes'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        today = datetime.today()
        title_slugified = slugify(self.name)
        self.slug = f'{today:%Y%m%d%M%S}-{title_slugified}'
        super().save(*args, **kwargs)

class PredefineAttributeValue(models.Model):
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    name = models.CharField(max_length=255)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')

    class Meta:
        verbose_name = 'predefined attribute value'
        verbose_name_plural = 'predefined attribute values'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        today = datetime.today()
        title_slugified = slugify(self.name)
        self.slug = f'{today:%Y%m%d%M%S}-{title_slugified}'
        super().save(*args, **kwargs)

class Product(models.Model):
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='variations', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    album = models.OneToOneField(Album, on_delete=models.CASCADE, related_name='product', null=True, blank=True)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    attributes = models.ManyToManyField(PredefineAttributeValue, related_name='products', blank=True)
    acl = models.ForeignKey(Acl, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    is_aux = models.BooleanField(default=False)
    stock_quantity = models.PositiveIntegerField(default=0, blank=True)
    low_stock = models.BooleanField(default=False)
    out_of_stock = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    mark_as_new = models.BooleanField(default=False)
    new_start = models.DateTimeField(null=True, blank=True)
    new_end = models.DateTimeField(null=True, blank=True)
    not_returnable = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    allow_reviews = models.BooleanField(default=False)
    vendor_comments = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    sales_rate = models.FloatField(null=True, blank=True)
    on_sale = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    call_for_price = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    length = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    sold = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_discount(self):
        discount = self.sales_rate * self.price
        return discount

    @property
    def get_sales_price(self):
        sales_price = self.price - self.get_discount
        return sales_price

    @property
    def get_first_photo(self):
        return f"{settings.MEDIA_URL}{self.album.photos.first()}"

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:product-details", kwargs={"slug": self.slug})

    def get_price_url(self):
        return reverse("products:product-price", kwargs={"slug": self.slug})

    def set_attribute_url(self):
        return reverse("products:set-attribute", kwargs={"slug": self.slug})

    def get_attribute_url(self):
        return reverse("products:product-attribute", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        today = datetime.today()
        title_slugified = slugify(self.name)
        self.slug = f'{today:%Y%m%d%M%S}-{title_slugified}'
        super().save(*args, **kwargs)

class ProductBundle(models.Model):
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    album = models.OneToOneField(Album, on_delete=models.CASCADE, related_name='product_bundle', null=True, blank=True)
    vendor = models.ForeignKey(Vendor, related_name='product_bundle', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='product_bundles', blank=True)
    acl = models.ForeignKey(Acl, related_name='product_bundles', on_delete=models.DO_NOTHING, null=True, blank=True)
    is_aux = models.BooleanField(default=False)
    stock_quantity = models.PositiveIntegerField(default=0, blank=True)
    low_stock = models.BooleanField(default=False)
    out_of_stock = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    mark_as_new = models.BooleanField(default=False)
    new_start = models.DateTimeField(null=True, blank=True)
    new_end = models.DateTimeField(null=True, blank=True)
    not_returnable = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    allow_reviews = models.BooleanField(default=False)
    vendor_comments = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    sales_rate = models.FloatField(null=True, blank=True)
    on_sale = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    call_for_price = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    lenght = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    sold = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    products = models.ManyToManyField(Product, related_name="bundels", blank=True)

    class Meta:
        verbose_name = 'product bundle'
        verbose_name_plural = 'product bundles'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        today = datetime.today()
        title_slugified = slugify(self.name)
        self.slug = f'{today:%Y%m%d%M%S}-{title_slugified}'
        super().save(*args, **kwargs)
