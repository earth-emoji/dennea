# Generated by Django 2.2.12 on 2020-06-09 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'verbose_name': 'album', 'verbose_name_plural': 'albums'},
        ),
        migrations.AlterModelOptions(
            name='photo',
            options={'verbose_name': 'photo', 'verbose_name_plural': 'photos'},
        ),
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='album',
            name='slug',
            field=models.SlugField(blank=True, max_length=128, unique=True),
        ),
    ]
