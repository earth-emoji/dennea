from datetime import datetime
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

class Vendor(models.Model):
    slug = models.SlugField(max_length=128, unique=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="vendor", on_delete=models.CASCADE, blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'vendor'
        verbose_name_plural = 'vendors'

    @property
    def get_company_name(self):
        return self.user.company_name

    @property
    def get_email(self):
        return self.user.email

    @property
    def get_avatar(self):
        return f"{settings.MEDIA_URL}{self.user.photo}"

    @property
    def get_name(self):
        return self.user.name

    @property
    def get_dob(self):
        return self.user.date_of_birth

    @property
    def get_sex(self):
        return self.user.sex

    @property
    def get_acl(self):
        return self.user.acl.name

    def __str__(self):
        return self.user.email

    def get_products(self):
        return self.products.order_by('-created_at')

    def save(self, *args, **kwargs):
        today = datetime.today()
        title_slugified = slugify(self.get_company_name)
        self.slug = f'{today:%Y%m%d%M%S}-{title_slugified}'
        super().save(*args, **kwargs)
