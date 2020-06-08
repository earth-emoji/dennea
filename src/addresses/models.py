import uuid
from datetime import datetime
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

# Create your models here.
class Country(models.Model):
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=5, blank=True)

    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)



class State(models.Model):
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=5, blank=True)
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING, related_name='states', blank=True)

    class Meta:
        verbose_name = 'state'
        verbose_name_plural = 'states'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class City(models.Model):
    slug = models.SlugField(max_length=80, unique=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=5, blank=True)
    state = models.ForeignKey(State, on_delete=models.DO_NOTHING, related_name='cities', blank=True)

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        title_slugified = slugify(self.name)
        self.slug = f'{title_slugified}-{self.state.code}'
        super().save(*args, **kwargs)


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = (
        ('Billing', 'Billing'),
        ('Business', 'Business'),
        ('Primary', 'Primary'),
        ('Shipping', 'Shipping'),
    )
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    line1 = models.CharField(max_length=100, blank=True)
    line2 = models.CharField(max_length=100, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING, related_name='addresses')
    suite = models.CharField(max_length=10, null=True, blank=True)
    postal_code = models.CharField(max_length=12, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    address_type = models.CharField(max_length=11, choices=ADDRESS_TYPE_CHOICES, blank=True)

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'

    def __str__(self):
        return f"{self.line1}, {self.city.name}, {self.city.state.name}"
