import uuid
from datetime import datetime
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.text import slugify

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_id/<filename>
    return '{0}/{1}'.format(instance.user.username, filename)

# Create your models here.
class Album(models.Model):
    slug = models.SlugField(max_length=128, unique=True, blank=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='albums')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'album'
        verbose_name_plural = 'albums'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        today = datetime.today()
        title_slugified = slugify(self.name)
        self.slug = f'{today:%Y%m%d%M%S}-{title_slugified}'
        super().save(*args, **kwargs)

class Photo(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    url = models.ImageField(upload_to='photos/%Y/%m/%d/', null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

    def __str__(self):
        return str(self.url)