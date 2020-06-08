import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import AppUserManager
from addresses.models import Address


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_id/<filename>
    return '{0}/{1}'.format(instance.email, filename)

# Create your models here.


class Acl(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    # fields removed from base user model
    first_name = None
    last_name = None
    username = None

    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    email = models.EmailField('email address', unique=True, blank=True)
    photo = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)
    name = models.CharField('full name', max_length=255, blank=True)
    company_name = models.CharField('company name', max_length=100, blank=True)
    date_of_birth = models.DateField('date of birth', null=True, blank=True)
    sex = models.CharField(
        max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    acl = models.ForeignKey(Acl, related_name='users',
                            on_delete=models.DO_NOTHING, null=True, blank=True)
    addresses = models.ManyToManyField(
        Address, related_name='addresses', blank=True)
    is_vendor = models.BooleanField(default=False, blank=True)
    is_customer = models.BooleanField(default=False, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'company_name']

    objects = AppUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email
