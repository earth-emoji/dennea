# Generated by Django 2.2.12 on 2020-06-10 01:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20200610_0019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattributevalue',
            name='name',
        ),
    ]