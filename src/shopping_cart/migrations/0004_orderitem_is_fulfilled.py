# Generated by Django 2.2.12 on 2020-06-12 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0003_auto_20200611_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='is_fulfilled',
            field=models.BooleanField(default=False),
        ),
    ]
