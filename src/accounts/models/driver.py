import uuid
from django.conf import settings
from django.db import models
from django.shortcuts import reverse

from accounts.choices import CUSTOMER_TYPE_CHOICES

class Driver(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="driver", on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = 'driver'
        verbose_name_plural = 'drivers'

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
